"""Unit tests for forecast tp/ssrd de-accumulation (Codex #2).

The forecast accumulations are cumulative-from-step-0 — a different data contract than ERA5's hourly
increments. These tests pin the differencing across the 3h->6h step change at +144h and across UTC
00Z day boundaries, plus the monotonic-nonnegative guard. Pure synthetic; no network / no real data.

Run: python -m pytest data-sources/weather/tests/test_deaccum.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from weather.forecast import aggregate_forecast as A   # noqa: E402


def _steps():
    """Faithful ladder: 3-hourly to 144, then 6-hourly to 360 (includes the transition)."""
    return list(range(0, 145, 3)) + list(range(150, 361, 6))


def _cumulative_from_increments(inc_true, steps, t0="2026-07-05T12:00", nlat=2, nlon=2, member=None):
    """Build a cumulative DataArray from a known per-interval increment series.

    inc_true[i] is the increment realised over (step[i-1], step[i]]; inc_true[0] is unused (cum=0 at
    step 0). Returns (cum_da, valid_times, inc_true_broadcast)."""
    vt = pd.to_datetime(t0) + pd.to_timedelta(steps, unit="h")
    cum1d = np.concatenate([[0.0], np.cumsum(inc_true[1:])])           # cum[0]=0
    # broadcast to (valid_time, lat, lon) [+ member]
    base = cum1d[:, None, None] * np.ones((len(steps), nlat, nlon))
    dims = ("valid_time", "latitude", "longitude")
    coords = {"valid_time": vt, "latitude": [30.0, 29.75], "longitude": [-85.0, -84.75]}
    if member is not None:
        base = base[None] * np.ones((member, 1, 1, 1))
        dims = ("number",) + dims
        coords["number"] = np.arange(1, member + 1)
    return xr.DataArray(base, dims=dims, coords=coords), vt, cum1d


def test_deaccumulate_recovers_known_increments():
    steps = _steps()
    rng = np.random.default_rng(1)
    inc_true = np.abs(rng.gamma(1.0, 2.0, len(steps)))
    inc_true[0] = 0.0
    cum, vt, _ = _cumulative_from_increments(inc_true, steps)
    inc = A.deaccumulate(cum)                                  # labelled at interval end (drops step0)
    # recovered increments (per valid_time from the 2nd step on) must equal the truth
    got = inc.isel(latitude=0, longitude=0).values
    np.testing.assert_allclose(got, inc_true[1:], rtol=0, atol=1e-9)


def test_transition_144_to_150_is_single_difference():
    """The 144h(3-hourly)->150h(6-hourly) interval is ONE difference of width 6h — not double-counted."""
    steps = _steps()
    i144, i150 = steps.index(144), steps.index(150)
    assert i150 == i144 + 1                                    # consecutive in the ladder
    inc_true = np.ones(len(steps)); inc_true[0] = 0.0
    inc_true[i150] = 5.0                                       # a big 6-h-interval increment
    cum, vt, _ = _cumulative_from_increments(inc_true, steps)
    inc = A.deaccumulate(cum).isel(latitude=0, longitude=0).values
    # the increment carried at valid_time[150h] equals exactly the 6h increment, once
    assert np.isclose(inc[i150 - 1], 5.0)                      # inc index shifted by 1 (step0 dropped)
    assert np.isclose(inc[i144 - 1], 1.0)


def test_daily_sum_crosses_00z_correctly():
    """Daily totals partition increments by the UTC day of each interval's END time."""
    steps = _steps()
    inc_true = np.ones(len(steps)); inc_true[0] = 0.0          # 1 unit per interval
    cum, vt, _ = _cumulative_from_increments(inc_true, steps)
    daily, inc = A.daily_sum_from_cumulative(cum)
    # reference: assign each increment to the day it COVERS (floor of end-1s), matching the code
    inc_vt = vt[1:]                                            # step0 dropped
    covering = (inc_vt - pd.Timedelta("1s")).floor("D")
    ref = pd.Series(inc_true[1:], index=covering).groupby(level=0).sum()
    got = daily.isel(latitude=0, longitude=0).to_series()
    got.index = pd.to_datetime(got.index.values)
    for day, val in ref.items():
        assert np.isclose(got.loc[pd.Timestamp(day)], val), (day, got.loc[pd.Timestamp(day)], val)
    # total conservation: sum of daily == sum of all increments == final cumulative
    assert np.isclose(float(daily.isel(latitude=0, longitude=0).sum()), inc_true[1:].sum())


def test_daily_sum_equals_cumulative_endpoints_for_a_full_day():
    """For a fully-covered UTC day, daily total == cum(day end) - cum(day start)."""
    steps = _steps()
    rng = np.random.default_rng(3)
    inc_true = np.abs(rng.gamma(1.0, 1.5, len(steps))); inc_true[0] = 0.0
    cum, vt, cum1d = _cumulative_from_increments(inc_true, steps)
    daily, _ = A.daily_sum_from_cumulative(cum)
    # 2026-07-06 is the first fully covered UTC day (T0 is 07-05 12z). Its start=07-06 00z (step12),
    # end=07-07 00z (step36) at 3-hourly cadence.
    s_start, s_end = steps.index(12), steps.index(36)
    expected = cum1d[s_end] - cum1d[s_start]
    got = float(daily.sel(_day=np.datetime64("2026-07-06")).isel(latitude=0, longitude=0))
    assert np.isclose(got, expected), (got, expected)


def test_monotonic_guard_clips_small_negative_noise():
    steps = _steps()
    inc_true = np.ones(len(steps)); inc_true[0] = 0.0
    cum, vt, _ = _cumulative_from_increments(inc_true, steps)
    cum.values[5] -= 5e-4                                      # tiny packing dip (< tolerance)
    inc = A.deaccumulate(cum).isel(latitude=0, longitude=0).values
    assert (inc >= 0).all()                                   # no negative increments leak through


def test_deaccumulate_preserves_member_dim():
    steps = _steps()
    inc_true = np.ones(len(steps)); inc_true[0] = 0.0
    cum, vt, _ = _cumulative_from_increments(inc_true, steps, member=5)
    inc = A.deaccumulate(cum)
    assert inc.sizes["number"] == 5 and "valid_time" in inc.dims


def test_reindex_to_offset_era5_grid_is_nearest():
    """Forecast (whole-degree 0.25 grid) reindexed onto the offset ERA5 grid picks nearest cells."""
    fc_lat = np.array([31.0, 30.75, 30.5]); fc_lon = np.array([-87.5, -87.25])
    da = xr.DataArray(np.arange(6).reshape(3, 2).astype("float64"),
                      dims=("latitude", "longitude"),
                      coords={"latitude": fc_lat, "longitude": fc_lon})
    era_lat = np.array([30.9, 30.65]); era_lon = np.array([-87.45])   # offset ~0.05-0.2 deg
    out = A.reindex_to_era5(da, era_lat, era_lon)
    assert list(out["latitude"].values) == [30.9, 30.65]
    # 30.9 nearest 31.0 (row0); 30.65 nearest 30.75 (row1); lon -87.45 nearest -87.5 (col0)
    assert out.sel(latitude=30.9, longitude=-87.45).item() == da.sel(latitude=31.0, longitude=-87.5).item()
    assert out.sel(latitude=30.65, longitude=-87.45).item() == da.sel(latitude=30.75, longitude=-87.5).item()
