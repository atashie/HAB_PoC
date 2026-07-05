"""Deterministic synthetic daily ERA5-aggregate data for regression tests.

Shared by the golden-capture script and `test_features_regression.py` so both build the
*identical* input. No network, no real data — pure seeded numpy. The values are physically
plausible (FL-ish) only so the feature math exercises non-degenerate paths (finite per-month
SPEI moments, skewed water balance, positive PET); exact values are irrelevant since the
regression test compares new-vs-golden on the same synthetic input.

Grid: 3 latitudes x 2 longitudes = 6 cells. Span: 6 full calendar years (2016-2021, incl. leap
years) so every calendar month has ~6 samples/day for a stable SPEI calibration fit.
"""
from __future__ import annotations

SYNTH_SEED = 20260705


def make_synthetic_daily(seed: int = SYNTH_SEED):
    import numpy as np
    import pandas as pd
    import xarray as xr

    rng = np.random.default_rng(seed)
    dates = pd.date_range("2016-01-01", "2021-12-31", freq="D")   # 6 full years (2192 days)
    lats = np.array([30.0, 27.5, 25.0])                            # panhandle -> south FL
    lons = np.array([-85.0, -82.0])
    nt, nlat, nlon = len(dates), len(lats), len(lons)
    doy = dates.dayofyear.to_numpy().astype("float64")

    # Seasonal mean temperature: warmer to the south, summer peak ~ day 200.
    seasonal = 7.0 * np.sin(2 * np.pi * (doy - 110) / 365.25)      # (nt,)
    lat_offset = (25.0 - lats) * 0.8                               # south warmer  (nlat,)
    base = 24.0 + seasonal[:, None, None] + lat_offset[None, :, None]  # (nt,nlat,1)
    base = np.broadcast_to(base, (nt, nlat, nlon)).copy()
    tmean = base + rng.normal(0.0, 1.5, (nt, nlat, nlon))
    half_range = np.abs(rng.normal(5.0, 1.0, (nt, nlat, nlon)))    # >0
    tmax = tmean + half_range
    tmin = tmean - half_range

    # Precipitation: non-negative, right-skewed (gamma). Wetter summer.
    wet = 0.4 + 0.5 * (0.5 + 0.5 * np.sin(2 * np.pi * (doy - 150) / 365.25))  # (nt,)
    tp = rng.gamma(shape=0.7, scale=6.0, size=(nt, nlat, nlon)) * wet[:, None, None]

    # Downward solar (MJ/m2/day): seasonal, positive.
    ssrd = 18.0 + 7.0 * np.sin(2 * np.pi * (doy - 110) / 365.25)[:, None, None] \
        + rng.normal(0.0, 1.2, (nt, nlat, nlon))
    ssrd = np.clip(ssrd, 1.0, None)

    # Wind + calm-hours (air-stillness).
    wspd = np.clip(rng.gamma(shape=4.0, scale=0.8, size=(nt, nlat, nlon)), 0.1, None)
    calm = rng.integers(0, 25, size=(nt, nlat, nlon)).astype("float64")

    def da(arr):
        return xr.DataArray(arr, dims=("date", "latitude", "longitude"),
                            coords={"date": dates, "latitude": lats, "longitude": lons})

    return xr.Dataset({
        "t2m_mean_c": da(tmean), "t2m_max_c": da(tmax), "t2m_min_c": da(tmin),
        "tp_sum_mm": da(tp), "ssrd_sum_mj": da(ssrd),
        "wspd_mean_ms": da(wspd), "calm_hours": da(calm),
    })
