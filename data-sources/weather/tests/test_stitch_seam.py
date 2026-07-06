"""Unit tests for the stitch/seam helpers (build_feature_ensemble stage 4).

Focus: the user's gap-fill rule (LINEAR for temp/solar/wind; CLIMATOLOGICAL-MEDIAN for precip, never
linear), the honest effective-member-days metric, and fail-closed seam validation. Pure synthetic.

Run: python -m pytest data-sources/weather/tests/test_stitch_seam.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from weather.forecast import build_feature_ensemble as B   # noqa: E402


def _grid():
    return np.array([30.0, 29.75]), np.array([-85.0, -84.75])


def _daily(dates, fields):
    lat, lon = _grid()
    shape = (len(dates), len(lat), len(lon))
    return xr.Dataset({k: (("date", "latitude", "longitude"), np.full(shape, v))
                       for k, v in fields.items()},
                      coords={"date": dates, "latitude": lat, "longitude": lon})


def test_precip_climatology_is_per_doy_median():
    dates = pd.date_range("2016-01-01", "2019-12-31", freq="D")
    lat, lon = _grid()
    rng = np.random.default_rng(0)
    tp = rng.gamma(1.0, 3.0, (len(dates), len(lat), len(lon)))
    ds = xr.Dataset({"tp_sum_mm": (("date", "latitude", "longitude"), tp)},
                    coords={"date": dates, "latitude": lat, "longitude": lon})
    clim = B.precip_climatology(ds)
    assert "doy" in clim.dims
    # doy=1 median equals the median of all Jan-1 values across years, per cell
    jan1 = ds["tp_sum_mm"].sel(date=ds["date"].dt.dayofyear == 1)
    assert np.allclose(clim.sel(doy=1).values, jan1.median("date").values)


def test_interpolate_residual_linear_temp_but_climatological_precip():
    dates = pd.date_range("2020-01-01", "2020-01-10", freq="D")
    # temp: 10 through day3, NaN days4-6, 16 days7-10  -> linear fill 11.5/13/14.5
    tmean = np.array([10, 10, 10, np.nan, np.nan, np.nan, 16, 16, 16, 16], float)
    tp = np.array([2, 2, 2, np.nan, np.nan, np.nan, 9, 9, 9, 9], float)
    lat, lon = _grid()
    def bcast(a):
        return np.broadcast_to(a[:, None, None], (len(dates), len(lat), len(lon))).copy()
    ds = xr.Dataset({"t2m_mean_c": (("date", "latitude", "longitude"), bcast(tmean)),
                     "t2m_max_c": (("date", "latitude", "longitude"), bcast(tmean + 5)),
                     "t2m_min_c": (("date", "latitude", "longitude"), bcast(tmean - 5)),
                     "ssrd_sum_mj": (("date", "latitude", "longitude"), bcast(tmean)),
                     "wspd_mean_ms": (("date", "latitude", "longitude"), bcast(tmean)),
                     "wspd_max_ms": (("date", "latitude", "longitude"), bcast(tmean)),
                     "wspd_min_ms": (("date", "latitude", "longitude"), bcast(tmean)),
                     "calm_hours": (("date", "latitude", "longitude"), bcast(tmean)),
                     "tp_sum_mm": (("date", "latitude", "longitude"), bcast(tp))},
                    coords={"date": dates, "latitude": lat, "longitude": lon})
    # precip climatology = 5.0 everywhere (distinct from any linear interp of tp, which would be 4/5/6)
    clim = xr.DataArray(np.full((366, len(lat), len(lon)), 5.0),
                        dims=("doy", "latitude", "longitude"),
                        coords={"doy": np.arange(1, 367), "latitude": lat, "longitude": lon})
    residual = dates[3:6]                                   # days 4,5,6
    out = B.interpolate_residual(ds, residual, clim)

    tm = out["t2m_mean_c"].isel(latitude=0, longitude=0).values
    assert np.allclose(tm[3:6], [11.5, 13.0, 14.5])        # temp linearly interpolated
    pr = out["tp_sum_mm"].isel(latitude=0, longitude=0).values
    assert np.allclose(pr[3:6], 5.0)                       # precip = climatological median, NOT linear
    assert not np.allclose(pr[3:6], [4.0, 5.0, 6.0])       # explicitly NOT the linear fill
    # non-residual precip untouched
    assert np.allclose(pr[[0, 1, 2, 6]], [2, 2, 2, 9])


def test_effective_member_days_ramps_with_lead():
    ed = B.effective_member_days(["spei_6", "precip_trail_7d_mm", "pet_hargreaves_mm"], 15)
    s6 = ed.sel(feature="spei_6").values
    assert s6[0] == 1 and s6[14] == 15                     # day1=1/180 ... day15=15/180
    p7 = ed.sel(feature="precip_trail_7d_mm").values
    assert p7[0] == 1 and p7[6] == 7 and p7[7] == 7        # caps at the 7-day window
    pet = ed.sel(feature="pet_hargreaves_mm").values
    assert (pet == 1).all()                                # daily feature: always 1 member-day


def test_seam_validate_passes_clean_and_fails_on_gap_and_nan():
    dates = pd.date_range("2020-01-01", "2020-01-20", freq="D")
    clean = _daily(dates, {v: 1.0 for v in B.SPEI_CRITICAL})
    B.seam_validate(clean, upto_date=dates[-1])            # no raise

    gapped = clean.isel(date=[i for i in range(20) if i != 10])   # drop one day → non-daily gap
    with pytest.raises(ValueError, match="non-daily gaps"):
        B.seam_validate(gapped, upto_date=dates[-1])

    holed = clean.copy(deep=True)
    holed["tp_sum_mm"][5, 0, 0] = np.nan                   # NaN in a SPEI-critical field
    with pytest.raises(ValueError, match="NaNs in SPEI-critical"):
        B.seam_validate(holed, upto_date=dates[-1])
