"""Unit tests for the pure (no-network) logic of the ERA5 daily-statistics path.

Run: python -m pytest data-sources/weather/tests/ -q
"""
import sys
from pathlib import Path

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from weather.access import era5_cds as e  # noqa: E402


def test_split_by_statistic_separates_accumulated_from_instantaneous():
    variables = [
        "2m_temperature", "total_precipitation",
        "10m_u_component_of_wind", "10m_v_component_of_wind",
        "surface_solar_radiation_downwards",
    ]
    groups = e.split_by_statistic(variables)
    # accumulated → daily_sum; instantaneous → daily_mean
    assert groups["daily_sum"] == ["total_precipitation", "surface_solar_radiation_downwards"]
    assert groups["daily_mean"] == [
        "2m_temperature", "10m_u_component_of_wind", "10m_v_component_of_wind",
    ]


def test_split_by_statistic_omits_empty_groups():
    assert set(e.split_by_statistic(["2m_temperature"])) == {"daily_mean"}
    assert set(e.split_by_statistic(["total_precipitation"])) == {"daily_sum"}


def test_build_daily_request_shape_and_values():
    req = e.build_daily_request(
        ["2m_temperature"], 2016, "daily_mean", e.FLORIDA_AREA,
        months=["07"], days=["01", "02"],
    )
    assert req["product_type"] == "reanalysis"
    assert req["variable"] == ["2m_temperature"]
    assert req["year"] == "2016"                 # coerced to string
    assert req["daily_statistic"] == "daily_mean"
    assert req["frequency"] == "1_hourly"        # default
    assert req["time_zone"] == "utc+00:00"       # default
    assert req["area"] == e.FLORIDA_AREA         # [N, W, S, E]
    assert req["data_format"] == "netcdf"        # this dataset is NetCDF-only


def test_florida_area_is_north_west_south_east():
    n, w, s, ee = e.FLORIDA_AREA
    assert n > s and w < ee                       # N>S, W<E
    assert 24 < s < 26 and 30 < n < 32            # spans the FL peninsula
    assert -88 < w < -87 and -81 < ee < -79       # panhandle to Atlantic
