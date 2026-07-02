"""Unit tests for WQP pure logic (no network).

Runnable two ways (no new dependency required):
    python -m pytest data-sources/WQP/tests/test_wqp_api.py
    python data-sources/WQP/tests/test_wqp_api.py      # self-contained runner

Covers the logic worth trusting: URL/param building for both schemas, the
legacy<->WQX3 identifier crosswalk, the cross-schema observation key (the
anti-double-count backbone), censoring-state derivation, and count-header parsing.
All column names used here are VERIFIED from live probes (see reference/PRIMARY-SOURCES.md).
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from WQP.access import wqp_api as w  # noqa: E402


# --- representative rows: the SAME observation as served by each schema ------ #
# (identifiers + value semantics verified from live Result-profile headers)
LEGACY_ROW = {
    "OrganizationIdentifier": "USGS-OH",
    "MonitoringLocationIdentifier": "USGS-04193500",
    "ActivityIdentifier": "USGS-OH-A1",
    "ResultIdentifier": "R1",
    "ActivityStartDate": "2022-06-01",
    "ActivityStartTime/Time": "14:30:00",
    "CharacteristicName": "Phosphorus",
    "ResultSampleFractionText": "Total",
    "ResultMeasureValue": "0.05",
    "ResultMeasure/MeasureUnitCode": "mg/l",
    "ResultDetectionConditionText": "",
    "MeasureQualifierCode": "",
    "ResultStatusIdentifier": "Accepted",
    "USGSPCode": "00665",
    "ActivityDepthHeightMeasure/MeasureValue": "0.5",
}
WQX3_ROW = {
    "Org_Identifier": "USGS-OH",
    "Location_Identifier": "USGS-04193500",
    "Activity_ActivityIdentifier": "USGS-OH-A1",
    "Result_MeasureIdentifier": "R1",
    "Activity_StartDate": "2022-06-01",
    "Activity_StartTime": "14:30:00",
    "Result_Characteristic": "Phosphorus",
    "Result_SampleFraction": "Total",
    "Result_Measure": "0.05",
    "Result_MeasureUnit": "mg/l",
    "Result_ResultDetectionCondition": "",
    "Result_MeasureQualifierCode": "",
    "Result_MeasureStatusIdentifier": "Accepted",
    "USGSpcode": "00665",
    "Activity_DepthHeightMeasure": "0.5",
}


def _qs(url):
    """Return (path, list-of-(k,v)) with percent-decoding, preserving repeats."""
    parts = urlsplit(url)
    return parts.path, parse_qsl(parts.query, keep_blank_values=True)


# --------------------------------------------------------------------------- #
# build_query_url
# --------------------------------------------------------------------------- #
def test_build_url_legacy_station_default_csv():
    url = w.build_query_url("Station", {"statecode": "US:39"}, schema="legacy")
    path, qs = _qs(url)
    assert path == "/data/Station/search"
    assert ("statecode", "US:39") in qs           # decoded; encoding checked below
    assert ("mimeType", "csv") in qs              # csv is the default
    assert "%3A" in url                           # colon is percent-encoded on the wire


def test_build_url_wqx3_result_path():
    url = w.build_query_url("Result", {"countycode": "US:39:095"},
                            schema="wqx3", dataProfile="fullPhysChem")
    path, qs = _qs(url)
    assert path == "/wqx3/Result/search"
    assert ("dataProfile", "fullPhysChem") in qs


def test_build_url_summary_is_monitoring_location():
    url = w.build_query_url("summary", {"countycode": "US:39:095"},
                            schema="legacy", dataProfile="periodOfRecord")
    path, _ = _qs(url)
    assert path == "/data/summary/monitoringLocation/search"


def test_build_url_wqx3_summary_rejected():
    # Verified live: /wqx3/summary -> 404. The builder must refuse to fabricate it.
    try:
        w.build_query_url("summary", {"countycode": "US:39:095"}, schema="wqx3")
    except ValueError:
        return
    raise AssertionError("expected ValueError for wqx3 summary (endpoint does not exist)")


def test_wqp_date_iso_to_us():
    # Verified live: startDateLo=2024-03-12 -> HTTP 400; 03-12-2024 -> 200.
    assert w.wqp_date("2024-03-12") == "03-12-2024"
    assert w.wqp_date("03-12-2024") == "03-12-2024"   # already US: pass through
    assert w.wqp_date("") == ""


def test_build_url_converts_iso_start_date():
    url = w.build_query_url("Result", {"startDateLo": "2024-03-12"}, schema="legacy")
    _, qs = _qs(url)
    assert ("startDateLo", "03-12-2024") in qs         # builder auto-converts to WQP format


def test_build_url_repeatable_characteristic():
    url = w.build_query_url(
        "Result", {"characteristicName": ["Chlorophyll a", "Microcystin"]}, schema="legacy")
    _, qs = _qs(url)
    chars = [v for (k, v) in qs if k == "characteristicName"]
    assert chars == ["Chlorophyll a", "Microcystin"]   # both present, repeated param


# --------------------------------------------------------------------------- #
# normalize_record — the legacy<->WQX3 identifier crosswalk
# --------------------------------------------------------------------------- #
def test_normalize_maps_both_schemas_to_same_identity():
    nl = w.normalize_record(LEGACY_ROW, "legacy")
    nw = w.normalize_record(WQX3_ROW, "wqx3")
    for field in ("org_id", "location_id", "activity_id", "result_id",
                  "characteristic", "fraction", "value", "unit", "pcode",
                  "activity_date", "status"):
        assert nl[field] == nw[field], f"{field}: {nl[field]!r} != {nw[field]!r}"
    assert nl["org_id"] == "USGS-OH"
    assert nl["pcode"] == "00665"


# --------------------------------------------------------------------------- #
# observation_key — cross-schema dedup backbone (the anti-double-count rule)
# --------------------------------------------------------------------------- #
def test_observation_key_matches_across_schemas():
    kl = w.observation_key(w.normalize_record(LEGACY_ROW, "legacy"))
    kw = w.observation_key(w.normalize_record(WQX3_ROW, "wqx3"))
    assert kl == kw, "same observation across schemas must collapse to one key"


def test_observation_key_ignores_value_revision():
    # A provisional->accepted value change must NOT create a second observation;
    # it is a revision of the same identity (value is reconciled, not duplicated).
    revised = dict(WQX3_ROW, Result_Measure="0.06")
    k0 = w.observation_key(w.normalize_record(WQX3_ROW, "wqx3"))
    k1 = w.observation_key(w.normalize_record(revised, "wqx3"))
    assert k0 == k1


def test_observation_key_distinguishes_characteristic():
    other = dict(LEGACY_ROW, CharacteristicName="Nitrogen")
    k0 = w.observation_key(w.normalize_record(LEGACY_ROW, "legacy"))
    k1 = w.observation_key(w.normalize_record(other, "legacy"))
    assert k0 != k1


# --------------------------------------------------------------------------- #
# censoring_state — measured-absence vs missing vs detected
# --------------------------------------------------------------------------- #
def test_censoring_detected():
    assert w.censoring_state(w.normalize_record(LEGACY_ROW, "legacy")) == "detected"


def test_censoring_non_detect():
    row = dict(LEGACY_ROW, ResultMeasureValue="",
               ResultDetectionConditionText="Not Detected")
    assert w.censoring_state(w.normalize_record(row, "legacy")) == "non_detect"


def test_censoring_below_quant():
    row = dict(LEGACY_ROW, ResultMeasureValue="",
               ResultDetectionConditionText="Present Below Quantification Limit")
    assert w.censoring_state(w.normalize_record(row, "legacy")) == "below_quant"


def test_censoring_na_string_is_missing_not_zero():
    # Verified live: ResultMeasureValue can be the literal "NA" with empty detection
    # condition. That is ambiguous -> 'missing', never 0 and never assumed non-detect.
    row = dict(LEGACY_ROW, ResultMeasureValue="NA", ResultDetectionConditionText="")
    assert w.censoring_state(w.normalize_record(row, "legacy")) == "missing"


# --------------------------------------------------------------------------- #
# parse_counts — response-header counts (cheap discovery)
# --------------------------------------------------------------------------- #
def test_count_csv_records_handles_embedded_newlines():
    import tempfile
    import os
    # 2 data rows; the 2nd has a quoted field containing a newline (file has 4 lines).
    content = 'a,b\n1,"x"\n2,"line1\nline2"\n'
    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        assert w.count_csv_records(path) == 2      # not 3 (naive file-line count would be wrong)
    finally:
        os.unlink(path)


def test_parse_counts_from_headers():
    counts = w.parse_counts({"Total-Site-Count": "20", "Total-Result-Count": "7",
                             "Content-Type": "text/csv"})
    assert counts["site"] == 20
    assert counts["result"] == 7
    assert "content-type" not in counts


def test_parse_counts_case_insensitive_and_missing():
    counts = w.parse_counts({"total-site-count": "5"})
    assert counts["site"] == 5
    assert counts == {"site": 5}


# --------------------------------------------------------------------------- #
# self-contained runner (so no pytest dependency is required)
# --------------------------------------------------------------------------- #
def _run_all():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS {t.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if _run_all() else 0)
