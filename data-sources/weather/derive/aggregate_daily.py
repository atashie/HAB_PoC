#!/usr/bin/env python
"""Aggregate hourly ERA5 (GRIB) → daily base variables, at native 0.25° resolution.

We pull HOURLY ERA5 and aggregate locally (rather than the derived daily-statistics dataset)
so we control the aggregation and get fields the daily dataset can't reliably give: true daily
**Tmax/Tmin/Tmean** (the daily-stats max/min temp has an upstream bug), sub-daily **wind** for
air-stillness, and correctly-summed precip/solar. This is the base for the algal-growth indices
(SPEI, GDD, trailing precip/solar, air-stillness) — see DECISIONS-LOG 2026-07-02.

Aggregation rule (temporal aggregation to DAILY is explicitly requested by the user):
  * 2t (instantaneous, K)        → daily **mean, max, min** → °C
  * tp (accumulation, m h⁻¹)     → daily **sum**            → mm day⁻¹
  * ssrd (accumulation, J m⁻²)   → daily **sum**            → MJ m⁻² day⁻¹
  * 10u,10v (instantaneous m s⁻¹)→ hourly speed √(u²+v²) → daily **mean, max, min** + **calm_hours**
                                    (hours below --calm-threshold; an air-stillness precursor)
Each hourly ERA5 accumulation value is the accumulation over the hour ending at the valid time,
so a plain daily groupby-sum is correct. Output = one NetCDF per year in data/derived/ + manifest.
⚠ These are NATIVE per-cell daily fields (no spatial aggregation).

Usage
-----
python aggregate_daily.py                       # aggregate every hourly GRIB in data/raw/era5/
python aggregate_daily.py --file <hourly.grib>  # one file
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

_WEATHER_DIR = _DATA_SOURCES / "weather"
_RAW = _WEATHER_DIR / "data" / "raw" / "era5"
_DERIVED = _WEATHER_DIR / "data" / "derived"
_MANIFEST = _DERIVED / "era5_daily_agg_manifest.jsonl"


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def _rel(p) -> str:
    """Repo-relative path string, robust to relative/absolute inputs."""
    try:
        return str(Path(p).resolve().relative_to(_DATA_SOURCES))
    except Exception:
        return str(p)


def _hourly_series(ds, var):
    """Flatten one variable to a 1-D hourly series indexed by valid_time.

    Handles both ERA5 layouts:
      * instantaneous (t2m/u10/v10): dims (time, lat, lon), time IS the hourly axis.
      * accumulation (tp/ssrd): dims (time, step, lat, lon) — ERA5's twice-daily forecast
        accumulations; the true hour is valid_time = time + step, so we flatten (time×step).
    """
    import numpy as np
    import xarray as xr
    da = ds[var]
    nlat, nlon = ds.sizes["latitude"], ds.sizes["longitude"]
    if "step" in da.dims and ds.sizes.get("step", 1) > 1:
        da = da.transpose("time", "step", "latitude", "longitude")
        vt = ds["valid_time"].transpose("time", "step").values.reshape(-1)
        arr = da.values.reshape(-1, nlat, nlon)
    else:
        tdim = "time" if "time" in da.dims else "valid_time"
        da = da.transpose(tdim, "latitude", "longitude")
        vt = (ds["valid_time"].values.reshape(-1)
              if ds["valid_time"].ndim == 1 else ds[tdim].values.reshape(-1))
        arr = da.values.reshape(-1, nlat, nlon)
    out = xr.DataArray(arr, dims=("valid_time", "latitude", "longitude"),
                       coords={"valid_time": vt,
                               "latitude": ds["latitude"].values,
                               "longitude": ds["longitude"].values})
    out = out.sortby("valid_time")
    # de-duplicate any repeated valid_time (run/step boundary overlaps) — keep first
    _, keep = np.unique(out["valid_time"].values, return_index=True)
    return out.isel(valid_time=np.sort(keep))


def aggregate_file(path: Path, calm_threshold: float = 2.0):
    """Return (daily xr.Dataset, summary dict) for one hourly GRIB."""
    import cfgrib
    import numpy as np
    import xarray as xr

    series = {}
    for ds in cfgrib.open_datasets(str(path)):
        for var in ds.data_vars:
            series[var] = _hourly_series(ds, var)

    t = "valid_time"
    day = lambda da, how: getattr(da.resample({t: "1D"}), how)()  # noqa: E731
    out = xr.Dataset()
    # --- temperature (K → °C) ---
    if "t2m" in series:
        out["t2m_mean_c"] = day(series["t2m"], "mean") - 273.15
        out["t2m_max_c"] = day(series["t2m"], "max") - 273.15
        out["t2m_min_c"] = day(series["t2m"], "min") - 273.15
    # --- precipitation (m h⁻¹ summed → mm day⁻¹) ---
    if "tp" in series:
        out["tp_sum_mm"] = day(series["tp"], "sum") * 1000.0
    # --- solar radiation (J m⁻² summed → MJ m⁻² day⁻¹) ---
    if "ssrd" in series:
        out["ssrd_sum_mj"] = day(series["ssrd"], "sum") / 1.0e6
    # --- wind speed from hourly components (m s⁻¹) ---
    if "u10" in series and "v10" in series:
        wspd = np.sqrt(series["u10"] ** 2 + series["v10"] ** 2)
        out["wspd_mean_ms"] = day(wspd, "mean")
        out["wspd_max_ms"] = day(wspd, "max")
        out["wspd_min_ms"] = day(wspd, "min")
        out["calm_hours"] = (wspd < calm_threshold).resample({t: "1D"}).sum()
        out["calm_hours"].attrs["threshold_ms"] = calm_threshold

    # Drop incomplete days (< 24 hourly steps for an instantaneous var) — e.g. the ERA5T
    # tail can end mid-day (2026-06-28 had 3 h). A partial day biases means/extremes and
    # under-counts precip/solar sums, so it must not enter the daily series.
    n_dropped = 0
    if "t2m" in series:
        per_day = series["t2m"].resample({t: "1D"}).count().isel(latitude=0, longitude=0)
        complete = (per_day.values == 24)
        n_dropped = int((~complete).sum())
        if n_dropped:
            out = out.isel({t: np.where(complete)[0]})

    out = out.rename({t: "date"})
    out.attrs["dropped_incomplete_days"] = n_dropped
    # units metadata
    _units = {"t2m_mean_c": "degC", "t2m_max_c": "degC", "t2m_min_c": "degC",
              "tp_sum_mm": "mm/day", "ssrd_sum_mj": "MJ/m2/day",
              "wspd_mean_ms": "m/s", "wspd_max_ms": "m/s", "wspd_min_ms": "m/s",
              "calm_hours": "hours/day"}
    for k, u in _units.items():
        if k in out:
            out[k].attrs["units"] = u
    out.attrs["source"] = _rel(path)
    out.attrs["aggregation"] = "daily from hourly ERA5; native 0.25 deg; UTC days"
    out.attrs["calm_threshold_ms"] = calm_threshold

    # summary (labeled diagnostic over the file's AOI)
    def _rng(v):
        a = out[v].values
        a = a[np.isfinite(a)]
        return (round(float(a.min()), 2), round(float(a.max()), 2), round(float(a.mean()), 2))
    summary = {"days": int(out.sizes["date"]),
               "nlat": int(out.sizes["latitude"]), "nlon": int(out.sizes["longitude"]),
               "vars": {v: _rng(v) for v in out.data_vars}}
    return out, summary


def process(path: Path, calm_threshold: float = 2.0):
    _DERIVED.mkdir(parents=True, exist_ok=True)
    out, summary = aggregate_file(path, calm_threshold)
    # derive a year label from the date coord
    import pandas as pd  # noqa: F401  (xarray pulls it; used for stamping)
    y0 = str(out["date"].values[0])[:4]
    y1 = str(out["date"].values[-1])[:4]
    dest = _DERIVED / (f"era5_daily_agg_{y0}.nc" if y0 == y1 else f"era5_daily_agg_{y0}-{y1}.nc")
    out.to_netcdf(dest)
    rec = {
        "kind": "era5_daily_aggregate", "source": _rel(path),
        "path": str(dest.relative_to(_DATA_SOURCES)), "bytes": dest.stat().st_size,
        "sha256": _sha256(dest), "days": summary["days"],
        "grid": [summary["nlat"], summary["nlon"]], "variables": list(summary["vars"]),
        "calm_threshold_ms": calm_threshold, "accessed_utc": net._utc_now_iso(),
        "license": "CC-BY-4.0 (Copernicus / ERA5)",
    }
    net.append_manifest(_MANIFEST, rec)
    return dest, summary


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", type=Path, default=None, help="one hourly GRIB (default: all in raw/era5/)")
    p.add_argument("--calm-threshold", type=float, default=2.0,
                   help="wind speed (m/s) below which an hour counts as 'calm' (default 2.0)")
    args = p.parse_args(argv)

    files = [args.file] if args.file else sorted(_RAW.glob("*.grib"))
    if not files:
        print("No hourly GRIB files under data/raw/era5/. Pull first (access/era5_cds.py).")
        return 0
    for f in files:
        dest, s = process(f, args.calm_threshold)
        print(f"{f.name} → {dest.name}: {s['days']} days, {s['nlat']}×{s['nlon']} cells")
        for v, (lo, hi, mean) in s["vars"].items():
            print(f"    {v:14s} {lo} .. {hi} (mean {mean})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
