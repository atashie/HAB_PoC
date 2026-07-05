#!/usr/bin/env python
"""Weather feature engineering for HAB risk — algal-growth-relevant indices, per 0.25° cell.

Builds a daily, per-cell feature cube from the daily ERA5 aggregates (derive/aggregate_daily.py):

  DROUGHT / WATER BALANCE
  * SPEI-1, -2, -4, -6  — Standardized Precipitation-Evapotranspiration Index at 1/2/4/6-month
    scales. Water balance D = P − PET; PET via **Hargreaves** (temp-based; we have Tmax/Tmin/Tmean).
    **DAILY cadence** (a distinct value every day), standardized per calendar month via **Pearson III**
    (method-of-moments). Standardization uses a **FROZEN climatology** fit once on the calibration
    years and reused unchanged at serve time.

  ANTECEDENT / TRAILING (backward-looking → leakage-safe for as-of joins with CyAN)
  * precip_trail_{7,14,30,60,90}d_mm        — cumulative rainfall (nutrient-loading / runoff proxy)
  * gdd_trail_{30,60,90}d                    — trailing Growing Degree-Days, base --gdd-base (default 10 °C)
  * ssrd_trail_{14,30}d_mj                   — trailing downward solar (light availability)
  * calm_hours_trail_{7,14,30}d              — trailing calm-hours (AIR-STILLNESS: scum/stratification)
  * wspd_trail_{7,14,30}d_mean_ms            — trailing mean wind speed (lower = stiller)

FROZEN-CLIMATOLOGY API (added 2026-07-05 for the forecast-ensemble pipeline; see
docs/plans/2026-07-05-forecast-ensemble-features-design.md):
  * fit_climatology(daily_ds, gdd_base)  → the frozen per-month SPEI Pearson-III moments.
  * apply_features(daily_ds, clim, ...)  → the 22 features for ANY daily series (history OR a
    stitched forecast member), applying the frozen climatology. **apply_features NEVER fits** — it
    errors if the climatology is missing. This makes forecast SPEI leakage-safe by construction:
    a stitched series containing forecast days can never re-fit its own standardization.
  * build_features()                     → the historical product: load → fit → apply. Proven
    OUTPUT-IDENTICAL to the pre-refactor single-pass code by tests/test_features_regression.py.

DESIGN DECISIONS (flagged for review — see DECISIONS-LOG):
  * PET = Hargreaves (not Penman-Monteith): we have T but not humidity/net-radiation; ssrd is on hand
    for a future Penman upgrade. Hargreaves is the standard SPEI PET when only temperature is available.
  * SPEI distribution = Pearson III, calibrated on **complete years only**.
    ⚠ The 2016→present record (~10 yr) is SHORT for a stable SPEI fit — values are provisional;
    a longer ERA5 baseline for calibration is the recommended upgrade (to discuss).
  * GDD base temperature = 10 °C default (tunable): a placeholder to calibrate against the HAB
    literature / a cyanobacteria-relevant threshold.
  * Trailing features exclude the current-day's future; SPEI uses a fixed calibration-period fit
    (at serve time, apply the SAME stored fit — do not re-fit including the target window).

Native 0.25° per cell — NO spatial aggregation. Output: data/derived/weather_features_<span>.nc + manifest.

Usage
-----
python features.py                 # all daily aggregates present in data/derived/
python features.py --gdd-base 12   # override GDD base temperature
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

from _common import net                          # noqa: E402

# Quiet climate_indices' per-cell structlog INFO spam (thousands of lines over 864 cells).
import logging                                    # noqa: E402
try:
    import structlog
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))
except Exception:
    pass
logging.getLogger("climate_indices").setLevel(logging.WARNING)

_WEATHER = _DATA_SOURCES / "weather"
_DERIVED = _WEATHER / "data" / "derived"
_MANIFEST = _DERIVED / "weather_features_manifest.jsonl"

# Trailing windows (days) per feature family.
PRECIP_WINDOWS = [7, 14, 30, 60, 90]
GDD_WINDOWS = [30, 60, 90]
SSRD_WINDOWS = [14, 30]
STILL_WINDOWS = [7, 14, 30]
SPEI_SCALES = [1, 2, 4, 6]                        # months
SPEI_WINDOWS = {1: 30, 2: 60, 4: 120, 6: 180}    # days of trailing water balance per scale
DEFAULT_GDD_BASE_C = 10.0
_NAN_SENTINEL = -1.234567e30                      # for content-hashing arrays with NaNs


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def load_daily(derived: Path = _DERIVED):
    """Concatenate all per-year daily aggregates into one continuous daily Dataset."""
    import xarray as xr
    files = sorted(derived.glob("era5_daily_agg_*.nc"))
    if not files:
        raise SystemExit("No daily aggregates in data/derived/. Run derive/aggregate_daily.py first.")
    ds = xr.open_mfdataset(files, combine="by_coords", engine="netcdf4").load()
    ds = ds.sortby("date")
    # drop any duplicate dates from overlapping files (keep first)
    _, idx = __import__("numpy").unique(ds["date"].values, return_index=True)
    return ds.isel(date=sorted(idx)), [f.name for f in files]


def hargreaves_pet(ds):
    """Daily Hargreaves PET (mm/day) per cell — FAO-56, vectorized, TRUE calendar day-of-year.

    NB: we deliberately do NOT use `climate_indices.eto.eto_hargreaves`, which reshapes the input
    to (years, 366) and assumes every year is 366 days — feeding a continuous multi-year series
    drifts the day-of-year (hence extraterrestrial radiation Ra) after each non-leap year. Here Ra
    is computed from the actual date's day-of-year, so there is no drift. Cross-checked against the
    library on a single leap-year-aligned series in tests/test_features.py.
    """
    import numpy as np
    import pandas as pd
    import xarray as xr

    tmin, tmax, tmean = ds["t2m_min_c"], ds["t2m_max_c"], ds["t2m_mean_c"]
    doy = pd.to_datetime(ds["date"].values).dayofyear.to_numpy().astype("float64")  # 1..365/366
    phi = np.radians(ds["latitude"].values)                                          # (nlat,)
    GSC = 0.0820                                                                      # MJ m-2 min-1
    w = 2.0 * np.pi / 365.0
    dr = 1.0 + 0.033 * np.cos(w * doy)                                                # (nt,)
    decl = 0.409 * np.sin(w * doy - 1.39)                                             # (nt,)
    # sunset hour angle ws(time, lat); clip arg for high-lat edge cases
    x = np.clip(-np.tan(phi)[None, :] * np.tan(decl)[:, None], -1.0, 1.0)
    ws = np.arccos(x)                                                                 # (nt, nlat)
    Ra = ((24.0 * 60.0 / np.pi) * GSC * dr[:, None]
          * (ws * np.sin(phi)[None, :] * np.sin(decl)[:, None]
             + np.cos(phi)[None, :] * np.cos(decl)[:, None] * np.sin(ws)))            # (nt,nlat) MJ/m2/d
    Ra_mm = xr.DataArray(0.408 * Ra, dims=("date", "latitude"),
                         coords={"date": ds["date"], "latitude": ds["latitude"]})     # → mm/day equiv
    trange = (tmax - tmin).clip(min=0)
    pet = (0.0023 * (tmean + 17.8) * np.sqrt(trange) * Ra_mm).transpose(
        "date", "latitude", "longitude")
    pet.name = "pet_hargreaves_mm"
    return pet


def add_trailing_and_gdd(ds, gdd_base_c):
    """Trailing precip / solar / air-stillness + GDD features (daily rolling, backward-looking)."""
    import numpy as np
    out = {}
    # trailing precip (min_periods = full window → NaN until enough history, leakage-safe)
    for w in PRECIP_WINDOWS:
        out[f"precip_trail_{w}d_mm"] = ds["tp_sum_mm"].rolling(date=w, min_periods=w).sum()
    # GDD: daily then trailing sum
    gdd_daily = (0.5 * (ds["t2m_max_c"] + ds["t2m_min_c"]) - gdd_base_c).clip(min=0)
    for w in GDD_WINDOWS:
        out[f"gdd_trail_{w}d"] = gdd_daily.rolling(date=w, min_periods=w).sum()
    # trailing solar (downward)
    for w in SSRD_WINDOWS:
        out[f"ssrd_trail_{w}d_mj"] = ds["ssrd_sum_mj"].rolling(date=w, min_periods=w).sum()
    # air-stillness: trailing calm-hours + trailing mean wind speed
    for w in STILL_WINDOWS:
        out[f"calm_hours_trail_{w}d"] = ds["calm_hours"].rolling(date=w, min_periods=w).sum()
        out[f"wspd_trail_{w}d_mean_ms"] = ds["wspd_mean_ms"].rolling(date=w, min_periods=w).mean()
    return out, gdd_daily


# ----------------------------------------------------------------------------------------------
# SPEI — split into FIT (frozen climatology) + APPLY (standardize only). The two share the exact
# same backward-looking accumulation so fit-then-apply is arithmetically identical to the former
# single-pass add_spei (pinned by tests/test_features_regression.py).
# ----------------------------------------------------------------------------------------------

def _water_balance_cumulative(ds, pet_da):
    """Trailing k×30-day water-balance accumulation D=P−PET per SPEI scale (backward-looking).

    Returns ({scale: cum_array (nt, nlat, nlon)}, windows). min_periods=window → NaN until a full
    window of history. IDENTICAL in fit and apply so the two stay consistent to the bit.
    """
    D = ds["tp_sum_mm"] - pet_da
    cums = {}
    for scale, w in SPEI_WINDOWS.items():
        cums[scale] = (D.rolling(date=w, min_periods=w).sum()
                       .transpose("date", "latitude", "longitude").values)
    return cums, SPEI_WINDOWS


def _calendar(ds):
    """Return (years, months) numpy arrays for the daily date axis."""
    import pandas as pd
    dates = pd.to_datetime(ds["date"].values)
    return dates.year.to_numpy(), dates.month.to_numpy()


def _calibration_mask(years):
    """Complete-years-only calibration window (>=365 days present). Returns (mask, cal0, cal1)."""
    import pandas as pd
    yc = pd.Series(1, index=years).groupby(level=0).sum()
    complete_years = [int(y) for y in yc.index if yc[y] >= 365]
    cal0, cal1 = min(complete_years), max(complete_years)
    calib = (years >= cal0) & (years <= cal1)
    return calib, cal0, cal1


def fit_spei_climatology(ds, pet_da):
    """Fit the FROZEN per-calendar-month Pearson III moments for each SPEI scale.

    method-of-moments (mean/std/skew) over the trailing water-balance accumulation, computed on
    CALIBRATION YEARS ONLY (complete years). Months with <5 finite reference values are left NaN
    (→ apply emits NaN there). Fit ONCE on ERA5 history; reused unchanged at serve time.
    Returns an xr.Dataset dims (scale, month, latitude, longitude).
    """
    import numpy as np
    import xarray as xr
    from scipy.stats import skew as sp_skew

    cums, _ = _water_balance_cumulative(ds, pet_da)
    years, months = _calendar(ds)
    calib, cal0, cal1 = _calibration_mask(years)
    nlat, nlon = ds.sizes["latitude"], ds.sizes["longitude"]

    mean = np.full((len(SPEI_SCALES), 12, nlat, nlon), np.nan)
    std = np.full_like(mean, np.nan)
    skew = np.full_like(mean, np.nan)
    for si, scale in enumerate(SPEI_SCALES):
        cum = cums[scale]
        for m in range(1, 13):
            ref = cum[calib & (months == m)]                # calibration values ending in month m
            if ref.shape[0] < 5 or not np.isfinite(ref).any():
                continue
            with np.errstate(all="ignore"):
                mean[si, m - 1] = np.nanmean(ref, axis=0)
                std[si, m - 1] = np.nanstd(ref, axis=0)
                skew[si, m - 1] = np.asarray(sp_skew(ref, axis=0, nan_policy="omit"), dtype="float64")

    clim = xr.Dataset(
        {"spei_mean": (("scale", "month", "latitude", "longitude"), mean),
         "spei_std": (("scale", "month", "latitude", "longitude"), std),
         "spei_skew": (("scale", "month", "latitude", "longitude"), skew)},
        coords={"scale": SPEI_SCALES, "month": list(range(1, 13)),
                "latitude": ds["latitude"].values, "longitude": ds["longitude"].values})
    clim.attrs.update({
        "spei_calibration_years": f"{cal0}-{cal1}", "cal0": int(cal0), "cal1": int(cal1),
        "spei_windows_days": "1:30, 2:60, 4:120, 6:180",
        "spei_distribution": "pearson3, method-of-moments, per calendar month (seasonal climatology)",
        "note": "FROZEN SPEI climatology — fit once on ERA5 history; apply_spei reuses it unchanged "
                "(no re-fit at serve time). Leakage-safe.",
    })
    return clim


def apply_spei(ds, pet_da, clim):
    """Standardize the trailing water balance into SPEI using the FROZEN climatology (no fitting).

    Recomputes the same backward-looking accumulation as the fit, then probit-transforms via the
    stored per-month Pearson III moments. Errors if `clim` is missing — there is deliberately NO
    fitting fallback, so a forecast/stitched series can never re-fit its own standardization.
    """
    import numpy as np
    import xarray as xr
    from scipy.stats import pearson3, norm

    if clim is None or not {"spei_mean", "spei_std", "spei_skew"} <= set(clim.data_vars):
        raise ValueError("apply_spei requires a fitted climatology (spei_mean/std/skew); call "
                         "fit_spei_climatology() on ERA5 history first — there is no re-fit here.")

    cums, _ = _water_balance_cumulative(ds, pet_da)
    _, months = _calendar(ds)
    results = {}
    for scale in SPEI_SCALES:
        cum = cums[scale]
        z = np.full(cum.shape, np.nan, dtype="float64")
        cmean = clim["spei_mean"].sel(scale=scale).values       # (12, nlat, nlon)
        cstd = clim["spei_std"].sel(scale=scale).values
        cskew = clim["spei_skew"].sel(scale=scale).values
        for m in range(1, 13):
            sel = (months == m)
            if not sel.any():
                continue
            mean, std, sk = cmean[m - 1], cstd[m - 1], cskew[m - 1]
            with np.errstate(all="ignore"):
                x = cum[sel]
                cdf = pearson3.cdf(x, sk[None, :, :], loc=mean[None, :, :], scale=std[None, :, :])
                zz = norm.ppf(np.clip(cdf, 1e-6, 1 - 1e-6))
            zz = np.where(std[None, :, :] > 1e-9, zz, np.nan)   # guard degenerate / unfit cells
            z[sel] = np.clip(zz, -3.09, 3.09)
        results[f"spei_{scale}"] = xr.DataArray(
            z, dims=("date", "latitude", "longitude"),
            coords={"date": ds["date"], "latitude": ds["latitude"], "longitude": ds["longitude"]})
    return results


def _climatology_content_hash(clim) -> str:
    """sha256 of the fitted moments (NaN-canonicalized) — provenance + serve-time verification."""
    import numpy as np
    h = hashlib.sha256()
    for v in ("spei_mean", "spei_std", "spei_skew"):
        a = np.where(np.isnan(clim[v].values), np.float64(_NAN_SENTINEL), clim[v].values)
        h.update(np.ascontiguousarray(a, dtype="float64").tobytes())
    return h.hexdigest()


def fit_climatology(ds, gdd_base_c=DEFAULT_GDD_BASE_C):
    """Fit all frozen parameters needed to serve features (currently: the SPEI climatology).

    GDD base + trailing windows are fixed constants (no fitting). Returns the climatology Dataset,
    stamped with gdd_base_c and a content hash of the fitted moments.
    """
    pet = hargreaves_pet(ds)
    clim = fit_spei_climatology(ds, pet)
    clim.attrs["gdd_base_c"] = float(gdd_base_c)
    clim.attrs["climatology_sha256"] = _climatology_content_hash(clim)
    return clim


def apply_features(ds, clim, gdd_base_c=None):
    """Compute the 22 features for ANY daily series (history OR a stitched forecast member) using a
    FROZEN climatology. NO fitting branch — errors if `clim` is missing (enforces SPEI leakage-safety).
    """
    import xarray as xr
    if clim is None:
        raise ValueError("apply_features requires a fitted climatology (fit_climatology / "
                         "open_climatology). It never fits — that is what keeps forecast SPEI "
                         "leakage-safe.")
    if gdd_base_c is None:
        gdd_base_c = float(clim.attrs.get("gdd_base_c", DEFAULT_GDD_BASE_C))

    pet = hargreaves_pet(ds)
    trailing, gdd_daily = add_trailing_and_gdd(ds, gdd_base_c)
    spei = apply_spei(ds, pet, clim)

    feats = xr.Dataset({**trailing, **spei})
    feats["pet_hargreaves_mm"] = pet
    feats["gdd_daily"] = gdd_daily
    cal0, cal1 = clim.attrs.get("cal0"), clim.attrs.get("cal1")
    feats.attrs.update({
        "title": "HAB weather features (Florida, native 0.25 deg, daily)",
        "gdd_base_c": gdd_base_c,
        "spei_scales_days": "DAILY cadence; trailing 30/60/120/180 d for spei_1/2/4/6",
        "spei_distribution": "pearson3, method-of-moments, per calendar month (seasonal climatology)",
        "spei_pet_method": "hargreaves FAO-56 (vectorized, true calendar day-of-year; not the "
                           "climate_indices 366-day-reshape path which drifts DOY)",
        "spei_calibration_years": f"{cal0}-{cal1}",
        "spei_climatology_sha256": clim.attrs.get("climatology_sha256", ""),
        "spei_caveat": "FUTURE ISSUE — short (~10yr) calibration record; values provisional; "
                       "pull a longer ERA5 baseline (e.g. 1991-2020) for calibration only",
        "leakage": "trailing features + SPEI trailing-window accumulation are backward-looking "
                   "(min_periods=window); SPEI standardization uses a FROZEN calibration-period "
                   "per-month climatology (apply_features never re-fits)",
        "license": "CC-BY-4.0 (Copernicus / ERA5)",
    })
    for w in PRECIP_WINDOWS:
        feats[f"precip_trail_{w}d_mm"].attrs["units"] = "mm"
    return feats


def build_features(gdd_base_c=DEFAULT_GDD_BASE_C):
    """Historical product: load daily aggregates → fit climatology on them → apply.

    Output-IDENTICAL to the pre-refactor single-pass implementation (pinned by
    tests/test_features_regression.py). Returns (feats, src_files, cal0, cal1).
    """
    ds, src_files = load_daily()
    clim = fit_climatology(ds, gdd_base_c)
    feats = apply_features(ds, clim, gdd_base_c)
    feats.attrs["source_files"] = ", ".join(src_files)
    return feats, src_files, int(clim.attrs["cal0"]), int(clim.attrs["cal1"])


def write_climatology(clim, path):
    """Persist a frozen SPEI climatology to NetCDF (float64 preserved). Returns the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    clim.to_netcdf(path)
    return path


def open_climatology(path):
    """Load a frozen SPEI climatology written by write_climatology()."""
    import xarray as xr
    return xr.open_dataset(path).load()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--gdd-base", type=float, default=DEFAULT_GDD_BASE_C,
                   help=f"GDD base temperature °C (default {DEFAULT_GDD_BASE_C})")
    args = p.parse_args(argv)

    import pandas as pd
    ds, src = load_daily()
    clim = fit_climatology(ds, args.gdd_base)                    # fit once, reuse for feats + persist
    feats = apply_features(ds, clim, args.gdd_base)
    feats.attrs["source_files"] = ", ".join(src)
    cal0, cal1 = int(clim.attrs["cal0"]), int(clim.attrs["cal1"])

    _DERIVED.mkdir(parents=True, exist_ok=True)
    d0 = str(pd.to_datetime(feats["date"].values[0]).date())
    d1 = str(pd.to_datetime(feats["date"].values[-1]).date())
    dest = _DERIVED / f"weather_features_{d0}_{d1}.nc"
    feats.to_netcdf(dest)

    # Persist the FROZEN SPEI climatology — the forecast-ensemble pipeline consumes THIS exact file
    # so forecast SPEI is on the same standardized scale as the served history.
    clim_dest = _DERIVED / f"spei_climatology_{cal0}-{cal1}.nc"
    write_climatology(clim, clim_dest)

    rec = {"kind": "weather_features", "path": str(dest.relative_to(_DATA_SOURCES)),
           "bytes": dest.stat().st_size, "sha256": _sha256(dest),
           "n_features": len(feats.data_vars), "span": [d0, d1],
           "gdd_base_c": args.gdd_base, "spei_calibration": f"{cal0}-{cal1}",
           "spei_climatology_path": str(clim_dest.relative_to(_DATA_SOURCES)),
           "spei_climatology_sha256": clim.attrs["climatology_sha256"],
           "source_files": src, "accessed_utc": net._utc_now_iso(),
           "license": "CC-BY-4.0 (Copernicus / ERA5)"}
    net.append_manifest(_MANIFEST, rec)

    print(f"Wrote {dest.name}: {len(feats.data_vars)} features, "
          f"{feats.sizes['date']} days × {feats.sizes['latitude']}×{feats.sizes['longitude']} cells")
    print(f"  SPEI calibration years: {cal0}-{cal1}  | GDD base: {args.gdd_base} °C")
    print(f"  Frozen climatology: {clim_dest.name}  (sha256 {clim.attrs['climatology_sha256'][:12]}…)")
    print("  features:", ", ".join(sorted(feats.data_vars)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
