"""Unit tests for the pure feature math (no network, no CDS).

Run: python -m pytest data-sources/weather/tests/test_features.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from weather.derive import features as F  # noqa: E402


def _toy(days=10, tmax=30.0, tmin=20.0, tp=2.0, ssrd=18.0, calm=5.0, wspd=4.0):
    dates = pd.date_range("2020-01-01", periods=days, freq="D")
    shape = (days, 1, 1)
    def da(v):
        return xr.DataArray(np.full(shape, v), dims=("date", "latitude", "longitude"),
                            coords={"date": dates, "latitude": [25.0], "longitude": [-82.0]})
    return xr.Dataset({"t2m_max_c": da(tmax), "t2m_min_c": da(tmin),
                       "t2m_mean_c": da((tmax + tmin) / 2),
                       "tp_sum_mm": da(tp), "ssrd_sum_mj": da(ssrd),
                       "calm_hours": da(calm), "wspd_mean_ms": da(wspd)})


def test_gdd_daily_formula():
    ds = _toy(tmax=30.0, tmin=20.0)
    _, gdd = F.add_trailing_and_gdd(ds, gdd_base_c=10.0)
    # (30+20)/2 - 10 = 15
    assert np.allclose(gdd.values, 15.0)


def test_gdd_clips_at_zero_when_cold():
    ds = _toy(tmax=8.0, tmin=2.0)                       # mean 5 < base 10 → 0
    _, gdd = F.add_trailing_and_gdd(ds, gdd_base_c=10.0)
    assert np.allclose(gdd.values, 0.0)


def test_trailing_precip_is_backward_looking_sum():
    ds = _toy(days=5, tp=2.0)
    feats, _ = F.add_trailing_and_gdd(ds, gdd_base_c=10.0)
    p7 = feats["precip_trail_7d_mm"].squeeze().values
    # window 7 with min_periods 7 → first 6 are NaN, day7 onward = 7*2=14 (only 5 days here → all NaN)
    assert np.all(np.isnan(p7))
    # a shorter window present:
    p = ds["tp_sum_mm"].rolling(date=7, min_periods=7).sum().squeeze().values
    assert np.all(np.isnan(p))                          # sanity: same behavior


def test_trailing_window_values_when_enough_history():
    ds = _toy(days=40, tp=3.0)
    feats, _ = F.add_trailing_and_gdd(ds, gdd_base_c=10.0)
    p30 = feats["precip_trail_30d_mm"].squeeze().values
    assert np.isnan(p30[28])                            # day 29 (<30 days) still NaN
    assert np.isclose(p30[29], 30 * 3.0)               # day 30 → 90 mm
    assert np.isclose(p30[-1], 30 * 3.0)


def test_calm_hours_and_wind_trailing_present():
    ds = _toy(days=40, calm=6.0, wspd=5.0)
    feats, _ = F.add_trailing_and_gdd(ds, gdd_base_c=10.0)
    assert np.isclose(feats["calm_hours_trail_30d"].squeeze().values[-1], 30 * 6.0)
    assert np.isclose(feats["wspd_trail_30d_mean_ms"].squeeze().values[-1], 5.0)


def test_feature_families_are_named_as_expected():
    ds = _toy(days=100)
    feats, _ = F.add_trailing_and_gdd(ds, gdd_base_c=10.0)
    for w in F.PRECIP_WINDOWS:
        assert f"precip_trail_{w}d_mm" in feats
    for w in F.GDD_WINDOWS:
        assert f"gdd_trail_{w}d" in feats
    for w in F.STILL_WINDOWS:
        assert f"calm_hours_trail_{w}d" in feats
        assert f"wspd_trail_{w}d_mean_ms" in feats


def test_hargreaves_pet_is_positive_and_sensible():
    # 3 years of warm days at a FL latitude → PET in a few-mm/day band
    ds = _toy(days=365 * 3, tmax=30.0, tmin=20.0)
    pet = F.hargreaves_pet(ds).values
    pet = pet[np.isfinite(pet)]
    assert (pet > 0).all()
    assert 1.0 < pet.mean() < 8.0                      # daily PET plausibility


def test_hargreaves_matches_library_on_aligned_leap_year():
    # On a SINGLE 366-day year the library's day-of-year aligns correctly, so our vectorized
    # FAO-56 PET should match it closely. (The bug we fixed only appears across multi-year series.)
    from climate_indices import eto
    dates = pd.date_range("2016-01-01", "2016-12-31", freq="D")   # 366 days (leap)
    n = len(dates)
    tmin = 18.0 + 5.0 * np.sin(np.arange(n) * 2 * np.pi / 366)
    tmax = tmin + 8.0
    tmean = (tmin + tmax) / 2.0
    lat = 27.5
    ref = eto.eto_hargreaves(tmin, tmax, tmean, lat)             # correct on one aligned year
    ds = xr.Dataset(
        {"t2m_min_c": (("date", "latitude", "longitude"), tmin[:, None, None]),
         "t2m_max_c": (("date", "latitude", "longitude"), tmax[:, None, None]),
         "t2m_mean_c": (("date", "latitude", "longitude"), tmean[:, None, None])},
        coords={"date": dates, "latitude": [lat], "longitude": [-82.0]})
    ours = F.hargreaves_pet(ds).squeeze().values
    assert np.allclose(ours, ref, rtol=0.03, atol=0.1)
