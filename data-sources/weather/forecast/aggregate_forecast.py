#!/usr/bin/env python
"""Aggregate ECMWF open-data forecast fields → daily base variables on the ERA5 master grid.

Stage 3 of the forecast-ensemble pipeline. Mirrors derive/aggregate_daily.py's OUTPUT schema
(t2m_{mean,max,min}_c, tp_sum_mm, ssrd_sum_mj, wspd_{mean,max,min}_ms, calm_hours) so the stitched
history+forecast series feeds the SAME apply_features() unchanged — but from lower-cadence forecast
data, so several fields carry honest quality flags.

Key differences from the hourly-ERA5 path (all documented in the design, Codex #2/#6):
  * Forecast `tp`/`ssrd` are **cumulative from step 0** (a different data contract than ERA5's hourly
    increments). We DE-ACCUMULATE by differencing consecutive lead steps within each member, guard
    monotonic-nonnegative, then sum the per-interval increments into UTC days. This is correct across
    the 3h→6h step change at +144 h and across 00Z (a variable-width interval is still one difference).
  * Daily Tmax/Tmin come from `mx2t3`/`mn2t3` (3-hourly max/min) where available (to +144 h); beyond
    that only instantaneous `2t` exists, so Tmax/Tmin **degrade** to a sub-daily-sample proxy — flagged
    per day via `temp_extreme_source`.
  * The forecast is 3/6-hourly, so `calm_hours` is a **scaled proxy** (fraction of sub-daily steps below
    the calm threshold × 24) — flagged via `calm_proxy`. `subdaily_step_hours` records the day's cadence.
  * The open-data global 0.25° grid is offset ≤0.2° from our ERA5 grid, so forecast fields are
    **nearest-neighbour reindexed onto the ERA5 master grid** (values preserved; no interpolation).

Per-day quality variables travel IN the output: `temp_extreme_source`, `subdaily_step_hours`,
`calm_proxy`, `aggregation_complete`, `source_class` (= 'member_forecast' | 'gapfill_forecast').
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

CALM_THRESHOLD_MS = 2.0        # matches derive/aggregate_daily.py
_ACCUM_NOISE_TOL = -1e-3       # cumulative dips shallower than this are numerical noise → clip to 0


# --------------------------------------------------------------------------- #
# De-accumulation (the highest-risk piece; unit-tested in tests/test_deaccum.py)
# --------------------------------------------------------------------------- #
def deaccumulate(cum, dim="valid_time"):
    """Cumulative-from-step-0 field → per-interval increments, labelled at each interval's END.

    increment[i] = cum[i] − cum[i-1], carried at valid_time[i]. The first step (cum=0 at step 0) has
    no preceding interval and is dropped by the difference — correct, since the 0→first-step increment
    is captured at the first step. Differencing CONSECUTIVE available steps makes the 3h→6h width
    change automatic (a 6-h interval is one difference just like a 3-h one), and a genuine reset would
    show as a large negative (guarded). Small negative dips (packing noise) are clipped to 0.
    """
    inc = cum.diff(dim)                          # xarray diff labels at the upper point (interval end)
    return inc.where(inc >= _ACCUM_NOISE_TOL, 0.0).clip(min=0.0)


def _floor_day(valid_time_values):
    """UTC calendar day (numpy datetime64[D]) for each valid_time — the resample key."""
    import numpy as np
    return valid_time_values.astype("datetime64[D]")


def daily_sum_from_cumulative(cum, dim="valid_time"):
    """Daily total of a cumulative field = sum of de-accumulated increments per **true UTC day**.

    Each increment covers (previous step, this step]; we assign it to the day it COVERS by flooring
    (end − 1 s). So an increment ending exactly at 00:00 belongs to the day just ending, and
    daily[D] == cum(D+1 00:00) − cum(D 00:00) for a fully-covered day. (ERA5's hourly path labels at
    the raw end time, a ≤1 h offset — negligible for trailing/SPEI features; noted in the design.)
    """
    import numpy as np
    inc = deaccumulate(cum, dim)
    covering_day = (inc[dim].values - np.timedelta64(1, "s")).astype("datetime64[D]")
    inc = inc.assign_coords(_day=(dim, covering_day))
    return inc.groupby("_day").sum(dim), inc


# --------------------------------------------------------------------------- #
# Loading + grid reconciliation
# --------------------------------------------------------------------------- #
def load_param(run_dir: Path, param: str):
    """Open one <param>_fl.nc, return a DataArray with a `valid_time` dimension.

    Drops scalar level coords (heightAboveGround/surface). Keeps `number` if present (ENS members).
    """
    import xarray as xr
    ds = xr.open_dataset(run_dir / f"{param}_fl.nc")
    var = list(ds.data_vars)[0]
    da = ds[var]
    for c in ("heightAboveGround", "surface", "meanSea"):
        if c in da.coords and da[c].ndim == 0:
            da = da.drop_vars(c)
    if "step" in da.dims and "valid_time" in da.coords:
        da = da.swap_dims({"step": "valid_time"})
    return da.sortby("valid_time")


def reindex_to_era5(da, era_lat, era_lon):
    """Nearest-neighbour reindex onto the ERA5 master grid (grids offset ≤0.2°; values preserved)."""
    return da.reindex(latitude=era_lat, longitude=era_lon, method="nearest", tolerance=0.2)


def era5_grid(derived: Path = None):
    """Read the ERA5 master lat/lon from an existing daily aggregate."""
    import xarray as xr
    derived = derived or (_DATA_SOURCES / "weather" / "data" / "derived")
    files = sorted(derived.glob("era5_daily_agg_*.nc"))
    if not files:
        raise SystemExit("No ERA5 daily aggregate to read the master grid from.")
    g = xr.open_dataset(files[-1])
    return g["latitude"].values, g["longitude"].values


# --------------------------------------------------------------------------- #
# Daily aggregation
# --------------------------------------------------------------------------- #
def _complete_day_mask(valid_times, day_index):
    """A UTC day is complete if its sub-daily samples span 00Z→(next)00Z at the day's cadence.

    We infer the day's cadence from its own sample spacing and require the expected count
    (24 / spacing_h). The T0 partial day and the final partial day fail this and are dropped —
    mirroring aggregate_daily.py dropping incomplete ERA5 days.
    """
    import numpy as np
    import pandas as pd
    vt = pd.to_datetime(valid_times)
    days = vt.floor("D")
    complete = {}
    subdaily_h = {}
    for d in day_index:
        sel = days == d
        hrs = np.sort(vt[sel].hour.to_numpy())
        if hrs.size < 2:
            complete[d] = False; subdaily_h[d] = np.nan; continue
        spacing = int(np.min(np.diff(np.r_[hrs, hrs[-1] + 24]))) if hrs.size else 0
        spacing = spacing if spacing > 0 else 24
        expected = 24 // spacing
        # need the day's samples to start at 00 and cover the cadence (allow the 00Z of next day
        # to belong to the following day — so a full day has samples at 0,spacing,...,24-spacing)
        complete[d] = (hrs.size >= expected) and (hrs[0] == 0)
        subdaily_h[d] = spacing
    return complete, subdaily_h


def aggregate_run(run_dir: Path, era_lat, era_lon, source_class: str,
                  calm_threshold=CALM_THRESHOLD_MS, extreme_cutoff_h=144):
    """Aggregate one forecast run's per-param FL NetCDFs to a daily Dataset on the ERA5 grid.

    Returns an xr.Dataset with dims (number?, date, latitude, longitude): the aggregate_daily.py base
    fields + per-day quality variables. `number` is present iff the run is an ensemble (ENS pf).
    """
    import numpy as np
    import pandas as pd
    import xarray as xr

    # --- load + reindex the fields we have ---
    fields = {}
    for param in ("2t", "10u", "10v", "tp", "ssrd", "mx2t3", "mn2t3"):
        f = run_dir / f"{param}_fl.nc"
        if f.exists():
            fields[param] = reindex_to_era5(load_param(run_dir, param), era_lat, era_lon)

    t2m = fields["2t"]
    vt = pd.to_datetime(t2m["valid_time"].values)
    day_vals = vt.floor("D")
    day_index = pd.DatetimeIndex(sorted(day_vals.unique()))
    complete, subdaily_h = _complete_day_mask(t2m["valid_time"].values, day_index)

    def by_day(da, how):
        d = da.assign_coords(_day=("valid_time", _floor_day(da["valid_time"].values)))
        return getattr(d.groupby("_day"), how)("valid_time").rename({"_day": "date"})

    out = xr.Dataset()
    # temperature mean from instantaneous 2t
    out["t2m_mean_c"] = by_day(t2m, "mean") - 273.15

    # Tmax/Tmin: mx2t3/mn2t3 within the 3-hourly window, else degrade to instantaneous 2t.
    extreme_days = pd.DatetimeIndex([d for d in day_index
                                     if (vt[day_vals == d].max() - vt[0]).total_seconds() / 3600 <= extreme_cutoff_h])
    tmax_src = {}
    if "mx2t3" in fields:
        tmax_hi = by_day(fields["mx2t3"], "max") - 273.15
        tmin_lo = by_day(fields["mn2t3"], "min") - 273.15
    else:
        tmax_hi = tmin_lo = None
    tmax_proxy = by_day(t2m, "max") - 273.15
    tmin_proxy = by_day(t2m, "min") - 273.15
    use_hi = xr.DataArray([d in extreme_days and tmax_hi is not None for d in day_index],
                          dims="date", coords={"date": day_index})
    if tmax_hi is not None:
        tmax_hi = tmax_hi.reindex(date=day_index)
        tmin_lo = tmin_lo.reindex(date=day_index)
        out["t2m_max_c"] = xr.where(use_hi, tmax_hi, tmax_proxy.reindex(date=day_index))
        out["t2m_min_c"] = xr.where(use_hi, tmin_lo, tmin_proxy.reindex(date=day_index))
    else:
        out["t2m_max_c"] = tmax_proxy.reindex(date=day_index)
        out["t2m_min_c"] = tmin_proxy.reindex(date=day_index)

    # precip / solar: de-accumulate → daily sum
    tp_daily, _ = daily_sum_from_cumulative(fields["tp"])
    out["tp_sum_mm"] = tp_daily.rename({"_day": "date"}) * 1000.0
    ssrd_daily, _ = daily_sum_from_cumulative(fields["ssrd"])
    out["ssrd_sum_mj"] = ssrd_daily.rename({"_day": "date"}) / 1.0e6

    # wind + calm proxy from sub-daily components
    wspd = np.sqrt(fields["10u"] ** 2 + fields["10v"] ** 2)
    out["wspd_mean_ms"] = by_day(wspd, "mean")
    out["wspd_max_ms"] = by_day(wspd, "max")
    out["wspd_min_ms"] = by_day(wspd, "min")
    calm_frac = by_day((wspd < calm_threshold).astype("float64"), "mean")
    out["calm_hours"] = (calm_frac * 24.0)      # PROXY: fraction-of-subdaily-steps-calm × 24 h

    # align every field on the same date index, drop incomplete days (T0 partial + final partial)
    out = out.reindex(date=day_index)
    keep = np.array([complete[d] for d in day_index], dtype=bool)

    # --- quality variables (travel in the NetCDF) ---
    out["subdaily_step_hours"] = xr.DataArray([subdaily_h[d] for d in day_index],
                                              dims="date", coords={"date": day_index})
    out["temp_extreme_source"] = xr.DataArray(
        [("mx2t3_mn2t3" if (d in extreme_days and "mx2t3" in fields) else "instant_2t_proxy")
         for d in day_index], dims="date", coords={"date": day_index})
    out["calm_proxy"] = xr.DataArray(np.ones(len(day_index), bool),
                                     dims="date", coords={"date": day_index})
    out["aggregation_complete"] = xr.DataArray(keep, dims="date", coords={"date": day_index})
    out["source_class"] = xr.DataArray([source_class] * len(day_index),
                                       dims="date", coords={"date": day_index})

    out = out.isel(date=np.where(keep)[0])       # drop partial end days from the served series
    _units = {"t2m_mean_c": "degC", "t2m_max_c": "degC", "t2m_min_c": "degC",
              "tp_sum_mm": "mm/day", "ssrd_sum_mj": "MJ/m2/day", "wspd_mean_ms": "m/s",
              "wspd_max_ms": "m/s", "wspd_min_ms": "m/s", "calm_hours": "hours/day (proxy)"}
    for k, u in _units.items():
        if k in out:
            out[k].attrs["units"] = u
    out.attrs.update({
        "run_dir": run_dir.name, "source_class": source_class,
        "calm_threshold_ms": calm_threshold, "extreme_cutoff_h": extreme_cutoff_h,
        "grid": "reindexed nearest-neighbour onto the ERA5 master 0.25 deg grid",
        "deaccumulation": "tp/ssrd differenced over consecutive lead steps per member; UTC-day sum",
    })
    return out


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run-dir", type=Path, required=True, help="a forecast_ens/<run> or forecast_gapfill/<run> dir")
    p.add_argument("--source-class", default="member_forecast",
                   choices=["member_forecast", "gapfill_forecast"])
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args(argv)

    lat, lon = era5_grid()
    ds = aggregate_run(args.run_dir, lat, lon, args.source_class)
    out = args.out or (args.run_dir / "daily_forecast.nc")
    ds.to_netcdf(out)
    nmem = int(ds.sizes.get("number", 1))
    print(f"{args.run_dir.name}: {ds.sizes['date']} complete days × {nmem} member(s) "
          f"× {ds.sizes['latitude']}×{ds.sizes['longitude']} → {out.name}")
    print("  vars:", ", ".join(v for v in ds.data_vars))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
