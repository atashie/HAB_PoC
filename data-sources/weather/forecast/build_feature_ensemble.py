#!/usr/bin/env python
"""Stitch ERA5 history + forecast per member → the 22-feature forecast ENSEMBLE (stages 4-6).

Pipeline (docs/plans/2026-07-05-forecast-ensemble-features-design.md):
  4. Build ONE shared history-to-T0 daily series: ERA5 spine → gap-fill oper forecast (recent days)
     → interpolate the residual sub-gap (LINEAR for temp/solar/wind; CLIMATOLOGICAL-MEDIAN precip —
     never linear-interpolate precip, per the user rule).
  5. For each ENS member m: member_series = shared_history + member_forecast; run apply_features()
     with the FROZEN climatology; slice the forecast days.
  6. Store the feature ensemble (member × valid_time × lat × lon) + honest quality/provenance:
     - `effective_member_days_in_window`: how many days in each feature's window are member-specific
       (day-1 spei_6 = 1/180 → members near-agree at T0; the spread is forecast divergence only).
     - per-day quality flags carried from aggregate_forecast (source_class, temp_extreme_source, ...).

Leakage posture: apply_features NEVER re-fits — it applies the ERA5-fit frozen climatology to every
stitched member, so forecast SPEI is on the same scale as history and cannot leak. Seam validation is
fail-closed: a discontinuous / NaN-holed base series raises rather than emitting a mostly-NaN cube.
"""
from __future__ import annotations

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

from weather.derive import features as F          # noqa: E402  (shared feature math + frozen clim)

# Base daily fields apply_features() consumes (must match aggregate_daily.py / aggregate_forecast.py).
BASE_FIELDS = ["t2m_mean_c", "t2m_max_c", "t2m_min_c", "tp_sum_mm", "ssrd_sum_mj",
               "wspd_mean_ms", "wspd_max_ms", "wspd_min_ms", "calm_hours"]
# Fields safe to fill by LINEAR interpolation across the residual gap (user rule).
LINEAR_FIELDS = ["t2m_mean_c", "t2m_max_c", "t2m_min_c", "ssrd_sum_mj",
                 "wspd_mean_ms", "wspd_max_ms", "wspd_min_ms", "calm_hours"]
PRECIP_FIELD = "tp_sum_mm"                          # NEVER linear — climatological median only
# SPEI-used base fields that must be NaN-free across the stitched window (seam validation).
SPEI_CRITICAL = ["t2m_mean_c", "t2m_max_c", "t2m_min_c", "tp_sum_mm"]
HISTORY_DAYS = 200                                  # > spei_6's 180-day window, with buffer


def feature_window_days():
    """Map each of the 22 features to the number of trailing days that inform it (for the
    effective-member-days honesty metric). Daily features (pet, gdd_daily) → 1."""
    w = {}
    for k in F.SPEI_SCALES:
        w[f"spei_{k}"] = F.SPEI_WINDOWS[k]
    for d in F.PRECIP_WINDOWS:
        w[f"precip_trail_{d}d_mm"] = d
    for d in F.GDD_WINDOWS:
        w[f"gdd_trail_{d}d"] = d
    for d in F.SSRD_WINDOWS:
        w[f"ssrd_trail_{d}d_mj"] = d
    for d in F.STILL_WINDOWS:
        w[f"calm_hours_trail_{d}d"] = d
        w[f"wspd_trail_{d}d_mean_ms"] = d
    w["pet_hargreaves_mm"] = 1
    w["gdd_daily"] = 1
    return w


# --------------------------------------------------------------------------- #
# Stage 4 helpers (pure — unit-tested in tests/test_stitch_seam.py)
# --------------------------------------------------------------------------- #
def precip_climatology(era5_daily):
    """Median daily precip per (day-of-year, cell) over the ERA5 record — the residual-precip fill."""
    doy = era5_daily["date"].dt.dayofyear
    clim = era5_daily[PRECIP_FIELD].groupby(doy).median()
    return clim.rename({"dayofyear": "doy"}) if "dayofyear" in clim.dims else clim


def interpolate_residual(daily, residual_dates, precip_clim):
    """Fill residual (all-NaN) gap dates: LINEAR for temp/solar/wind; CLIMATOLOGICAL-MEDIAN for precip.

    `daily` is a (date, lat, lon) Dataset with the residual dates present but NaN. Linear fields are
    interpolated along date; precip is set to the per-doy climatological median (never interpolated).
    """
    import numpy as np
    import pandas as pd
    out = daily.copy()
    for v in LINEAR_FIELDS:
        if v in out:
            out[v] = out[v].interpolate_na(dim="date", method="linear", fill_value="extrapolate")
    doy_dim = [d for d in precip_clim.dims if d not in ("latitude", "longitude")][0]
    for d in pd.DatetimeIndex(residual_dates):
        doy = min(int(d.dayofyear), int(precip_clim[doy_dim].max()))
        out[PRECIP_FIELD].loc[{"date": np.datetime64(d, "ns")}] = precip_clim.sel({doy_dim: doy})
    return out


def effective_member_days(feature_names, n_forecast_days, windows=None):
    """Per (feature, forecast-day) count of member-specific days inside the feature's window.

    On forecast day k (1-indexed from T0+1), a feature with window W has min(k, W) member-specific
    days; the rest of the window is shared history/gap-fill. So day-1 spei_6 = 1/180 (members
    near-identical), day-15 = 15/180. Honest-uncertainty label, NOT a spread correction.
    """
    import numpy as np
    import xarray as xr
    windows = windows or feature_window_days()
    days = np.arange(1, n_forecast_days + 1)
    data = np.stack([np.minimum(days, windows[f]) for f in feature_names])
    return xr.DataArray(data, dims=("feature", "lead_day"),
                        coords={"feature": list(feature_names), "lead_day": days})


# --------------------------------------------------------------------------- #
# Stage 4/5: assemble shared history, seam-validate, stitch per member
# --------------------------------------------------------------------------- #
def assemble_shared_history(era5_daily, gapfill_daily, ens_first_day, precip_clim,
                            history_days=HISTORY_DAYS):
    """Build the shared [ens_first_day-history_days .. ens_first_day-1] daily base series.

    Priority per day: ERA5 (<= frontier) → gap-fill oper forecast → interpolated residual. Returns
    (history_ds, source_by_date) where history_ds has BASE_FIELDS on (date, lat, lon).
    """
    import numpy as np
    import pandas as pd
    import xarray as xr

    start = pd.Timestamp(ens_first_day) - pd.Timedelta(days=history_days)
    end = pd.Timestamp(ens_first_day) - pd.Timedelta(days=1)
    full_dates = pd.date_range(start, end, freq="D")

    era = era5_daily[BASE_FIELDS].reindex(date=full_dates)
    src = np.array(["missing"] * len(full_dates), dtype=object)
    era_dates = set(pd.to_datetime(era5_daily["date"].values))
    for i, d in enumerate(full_dates):
        if d in era_dates:
            src[i] = "era5"

    hist = era
    if gapfill_daily is not None:
        gf = gapfill_daily[[v for v in BASE_FIELDS if v in gapfill_daily]].reindex(date=full_dates)
        gf_dates = set(pd.to_datetime(gapfill_daily["date"].values))
        # gap-fill only where ERA5 is absent (do not overwrite reanalysis)
        take_gf = xr.DataArray([(d not in era_dates) and (d in gf_dates) for d in full_dates],
                               dims="date", coords={"date": full_dates})
        hist = xr.where(take_gf, gf, hist)
        for i, d in enumerate(full_dates):
            if src[i] == "missing" and d in gf_dates:
                src[i] = "gapfill_forecast"

    residual_dates = [d for i, d in enumerate(full_dates) if src[i] == "missing"]
    for i, d in enumerate(full_dates):
        if src[i] == "missing":
            src[i] = "interpolated"
    if residual_dates:
        hist = interpolate_residual(hist, residual_dates, precip_clim)

    hist = hist.assign_coords(source_class=("date", src))
    return hist, src


def seam_validate(series, upto_date, critical=SPEI_CRITICAL):
    """Fail-closed checks before apply_features: contiguous daily index, no dupes, SPEI-critical base
    fields NaN-free through `upto_date`. Raises ValueError on any violation."""
    import numpy as np
    import pandas as pd
    dates = pd.to_datetime(series["date"].values)
    if len(dates) != len(set(dates)):
        raise ValueError("seam_validate: duplicate dates in stitched series")
    gaps = np.diff(dates.values).astype("timedelta64[D]").astype(int)
    if not (gaps == 1).all():
        bad = dates[np.where(gaps != 1)[0]]
        raise ValueError(f"seam_validate: non-daily gaps after {list(bad)[:3]}")
    window = series.sel(date=slice(None, pd.Timestamp(upto_date)))
    for v in critical:
        if v in window and bool(window[v].isnull().any()):
            n = int(window[v].isnull().sum())
            raise ValueError(f"seam_validate: {n} NaNs in SPEI-critical '{v}' before {upto_date}")


def build_ensemble(era5_daily, ens_daily, gapfill_daily, clim, precip_clim):
    """Stitch each member and apply the frozen climatology → forecast feature ensemble.

    ens_daily: (number, date, lat, lon) forecast base fields (aggregate_forecast on the ENS run).
    Returns (feature_ensemble Dataset [number, date, lat, lon], forecast_dates, quality Dataset).
    """
    import numpy as np
    import pandas as pd
    import xarray as xr

    fdates = pd.to_datetime(ens_daily["date"].values)
    ens_first_day = fdates.min()
    hist, src = assemble_shared_history(era5_daily, gapfill_daily, ens_first_day, precip_clim)

    members = ens_daily["number"].values
    per_member = []
    for m in members:
        mem_fc = ens_daily[[v for v in BASE_FIELDS if v in ens_daily]].sel(number=m)
        series = xr.concat([hist[BASE_FIELDS], mem_fc[BASE_FIELDS]], dim="date").sortby("date")
        seam_validate(series, upto_date=fdates.max())
        feats = F.apply_features(series, clim)
        per_member.append(feats.sel(date=fdates))          # slice forecast horizon
    ens = xr.concat(per_member, dim="number").assign_coords(number=members)
    ens = ens.rename({"date": "valid_time"})
    return ens, fdates


def main(argv=None):
    import argparse
    import numpy as np
    import pandas as pd
    import xarray as xr

    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ens-daily", type=Path, required=True, help="aggregate_forecast output for the ENS run")
    p.add_argument("--gap-daily", type=Path, default=None, help="aggregate_forecast output for the gap-fill run")
    p.add_argument("--climatology", type=Path, default=None, help="frozen spei_climatology_*.nc (default: latest)")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args(argv)

    era5, _ = F.load_daily()
    ens_daily = xr.open_dataset(args.ens_daily)
    gap_daily = xr.open_dataset(args.gap_daily) if args.gap_daily and args.gap_daily.exists() else None
    clim_path = args.climatology
    if clim_path is None:
        cands = sorted((_DATA_SOURCES / "weather" / "data" / "derived").glob("spei_climatology_*.nc"))
        clim_path = cands[-1] if cands else None
    if clim_path is None:
        raise SystemExit("No frozen climatology found — run derive/features.py first.")
    clim = F.open_climatology(clim_path)

    pclim = precip_climatology(era5)
    ens, fdates = build_ensemble(era5, ens_daily, gap_daily, clim, pclim)

    feat_names = list(ens.data_vars)
    ens["effective_member_days_in_window"] = effective_member_days(feat_names, len(fdates))
    # carry per-day quality flags from the ENS aggregate onto the forecast valid_times
    for q in ("temp_extreme_source", "subdaily_step_hours", "calm_proxy", "aggregation_complete"):
        if q in ens_daily:
            ens[q] = ens_daily[q].sel(date=fdates).rename({"date": "valid_time"})
    ens.attrs.update({
        "title": "HAB weather FORECAST feature ensemble (Florida, 0.25 deg, daily)",
        "n_members": int(ens.sizes["number"]),
        "climatology": Path(clim_path).name,
        "climatology_sha256": clim.attrs.get("climatology_sha256", ""),
        "spread_meaning": "ensemble spread = forecast divergence ONLY (history/gap-fill/model error "
                          "excluded); near-T0 memory features are history-dominated — see "
                          "effective_member_days_in_window",
        "members_note": "open-data ENS has no cf control -> 50 pf members (not 51)",
        "license": "CC-BY-4.0 (ECMWF open data + Copernicus/ERA5)",
    })

    out = args.out or (_DATA_SOURCES / "weather" / "data" / "derived" /
                       f"forecast_feature_ensemble_{pd.Timestamp(fdates.min()).date()}.nc")
    out.parent.mkdir(parents=True, exist_ok=True)
    ens.to_netcdf(out)
    print(f"Wrote {out.name}: {ens.sizes['number']} members × {ens.sizes['valid_time']} valid days "
          f"× {ens.sizes['latitude']}×{ens.sizes['longitude']}; {len(feat_names)} features")
    print("  valid_time:", str(fdates.min().date()), "→", str(fdates.max().date()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
