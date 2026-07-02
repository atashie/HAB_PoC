"""Water Quality Portal (WQP) access primitives: URL building, schema crosswalk,
cross-schema dedup key, censoring logic, and cached/manifested fetch helpers.

Grounded in ``../METADATA.md`` and the verified column names in
``../reference/PRIMARY-SOURCES.md`` (every crosswalk entry below was read off a live
Result/Station profile header on 2026-07-01, not assumed).

No network side effects on import. The only functions that touch the network
(``count_headers``, ``fetch_csv_to_cache``) take a caller-provided requests.Session
(see ``_common/net.py``) and import it lazily, so the pure logic is testable offline.
"""
from __future__ import annotations

import csv as _csv
import hashlib
import re
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlencode

BASE = "https://www.waterqualitydata.us"

# schema family -> URL path segment. Legacy = WQX 2.2 (`/data`), beta = WQX 3.0 (`/wqx3`).
SCHEMA_PATH = {"legacy": "data", "wqx3": "wqx3"}

# endpoint alias -> path under the schema root. `summary` has ONE profile path and
# exists ONLY on legacy (verified: /wqx3/summary -> HTTP 404, 2026-07-01).
ENDPOINT_PATH = {
    "Station": "Station",
    "Result": "Result",
    "Activity": "Activity",
    "ResultDetectionQuantitationLimit": "ResultDetectionQuantitationLimit",
    "dql": "ResultDetectionQuantitationLimit",       # convenience alias
    "summary": "summary/monitoringLocation",
}

# Response headers WQP returns with row counts -> short key. Lets us get a count
# without downloading the body (cheap discovery). Verified header: `Total-Site-Count`.
_COUNT_RE = re.compile(r"^total-(.+)-count$")

# WQP QUIRK (verified 2026-07-01): date params want US format MM-DD-YYYY. An ISO
# YYYY-MM-DD value returns HTTP 400. We keep ISO everywhere internally and convert
# these params on the way out. See METADATA §7.3.
_ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
WQP_DATE_PARAMS = ("startDateLo", "startDateHi")


def wqp_date(value) -> str:
    """Convert an ISO date (YYYY-MM-DD) to WQP's MM-DD-YYYY; pass anything else through."""
    m = _ISO_DATE_RE.match(str(value).strip())
    return f"{m.group(2)}-{m.group(3)}-{m.group(1)}" if m else str(value)


# --------------------------------------------------------------------------- #
# Legacy WQX 2.2  <->  WQX 3.0 crosswalk (VERIFIED column names, Result profiles)
# --------------------------------------------------------------------------- #
# Only the ~modeling/identity columns are mapped here; the FULL column crosswalk is
# EPA's published WQX3 outbound schema (see METADATA §7.5). "" means the schema's
# Result profile does not carry that field inline (e.g. legacy Result has no coords).
COLUMN_CROSSWALK: dict[str, dict[str, str]] = {
    #  canonical           legacy (WQX 2.2)                      wqx3 (WQX 3.0)
    "org_id":              {"legacy": "OrganizationIdentifier",        "wqx3": "Org_Identifier"},
    "location_id":         {"legacy": "MonitoringLocationIdentifier",  "wqx3": "Location_Identifier"},
    "activity_id":         {"legacy": "ActivityIdentifier",            "wqx3": "Activity_ActivityIdentifier"},
    "result_id":           {"legacy": "ResultIdentifier",              "wqx3": "Result_MeasureIdentifier"},
    "activity_date":       {"legacy": "ActivityStartDate",             "wqx3": "Activity_StartDate"},
    "activity_time":       {"legacy": "ActivityStartTime/Time",        "wqx3": "Activity_StartTime"},
    "characteristic":      {"legacy": "CharacteristicName",            "wqx3": "Result_Characteristic"},
    "fraction":            {"legacy": "ResultSampleFractionText",      "wqx3": "Result_SampleFraction"},
    "value":              {"legacy": "ResultMeasureValue",            "wqx3": "Result_Measure"},
    "unit":               {"legacy": "ResultMeasure/MeasureUnitCode", "wqx3": "Result_MeasureUnit"},
    "detection_condition": {"legacy": "ResultDetectionConditionText",  "wqx3": "Result_ResultDetectionCondition"},
    "qualifier":           {"legacy": "MeasureQualifierCode",          "wqx3": "Result_MeasureQualifierCode"},
    "status":              {"legacy": "ResultStatusIdentifier",        "wqx3": "Result_MeasureStatusIdentifier"},
    "method_name":         {"legacy": "ResultAnalyticalMethod/MethodName", "wqx3": "ResultAnalyticalMethod_Name"},
    "pcode":               {"legacy": "USGSPCode",                     "wqx3": "USGSpcode"},
    "depth":               {"legacy": "ActivityDepthHeightMeasure/MeasureValue", "wqx3": "Activity_DepthHeightMeasure"},
    # coordinates: inline on WQX3 Result, but legacy Result has none (join to Station).
    "latitude":            {"legacy": "", "wqx3": "Location_Latitude"},
    "longitude":           {"legacy": "", "wqx3": "Location_Longitude"},
    "huc8":                {"legacy": "", "wqx3": "Location_HUCEightDigitCode"},
    "huc12":               {"legacy": "", "wqx3": "Location_HUCTwelveDigitCode"},
}

# Identity fields for the cross-schema dedup hash. EXCLUDES value/status/qualifier/
# detection (so a provisional->accepted revision collapses to ONE observation) and
# EXCLUDES the id columns (legacy ResultIdentifier vs wqx3 Result_MeasureIdentifier are
# not guaranteed equal across schemas) — see METADATA §10. Known trade-off: true field
# replicates sharing site+datetime+analyte+fraction+depth collapse; log if it matters.
IDENTITY_FIELDS = ("org_id", "location_id", "activity_date", "activity_time",
                   "characteristic", "fraction", "depth", "pcode")

# HAB-relevant characteristics — a STARTING probe set, NOT a harmonized feature set.
# Real selection comes from discovery + the reviewed analyte dictionary (METADATA §4).
# Note WQX vs USGS naming differs (e.g. dissolved oxygen filed under "Oxygen" by USGS).
#
# ⚠ WQP QUIRK (verified 2026-07-01): an UNRECOGNIZED characteristicName returns HTTP 400
# for the WHOLE query — one bad name poisons the request (e.g. "Microcystins, total" -> 400,
# but "Microcystin" -> 200). So every name below is a verified domain value, and the pull
# code must validate names against the Characteristic domain before querying (Codex #10).
HAB_CHARACTERISTICS = [
    "Chlorophyll a", "Chlorophyll a, corrected for pheophytin",
    "Microcystin",
    "Phosphorus", "Orthophosphate", "Total Phosphorus, mixed forms",
    "Nitrogen", "Inorganic nitrogen (nitrate and nitrite)", "Ammonia",
    "Temperature, water", "Dissolved oxygen (DO)", "Oxygen",
    "pH", "Turbidity", "Depth, Secchi disk depth",
]


# --------------------------------------------------------------------------- #
# URL / query building (pure)
# --------------------------------------------------------------------------- #
def build_query_url(endpoint: str, params: Optional[dict] = None, *,
                    schema: str = "legacy", **extra) -> str:
    """Build a WQP REST search URL for ``endpoint`` under ``schema``.

    - ``schema`` is 'legacy' (WQX 2.2, ``/data``) or 'wqx3' (WQX 3.0 beta, ``/wqx3``).
    - ``params``/``extra`` are query params; list values become repeated params
      (e.g. ``characteristicName=[a, b]`` -> ``characteristicName=a&characteristicName=b``).
    - ``mimeType`` defaults to ``csv``.
    - Raises ValueError for the WQX3 summary endpoint (verified nonexistent: 404).
    """
    if schema not in SCHEMA_PATH:
        raise ValueError(f"unknown schema {schema!r} (expected {list(SCHEMA_PATH)})")
    if endpoint not in ENDPOINT_PATH:
        raise ValueError(f"unknown endpoint {endpoint!r} (expected {list(ENDPOINT_PATH)})")
    if endpoint == "summary" and schema == "wqx3":
        raise ValueError("WQX3 has no summary service (/wqx3/summary -> 404); "
                         "use legacy summary for discovery (METADATA §7.2).")

    q = dict(params or {})
    q.update(extra)
    q.setdefault("mimeType", "csv")
    for dp in WQP_DATE_PARAMS:                    # ISO -> WQP MM-DD-YYYY (else 400)
        if q.get(dp):
            q[dp] = wqp_date(q[dp])
    # doseq=True expands list values into repeated params; quote_plus encodes ':' -> %3A.
    query = urlencode(q, doseq=True)
    return f"{BASE}/{SCHEMA_PATH[schema]}/{ENDPOINT_PATH[endpoint]}/search?{query}"


def parse_counts(headers) -> dict:
    """Extract WQP `Total-<thing>-Count` response headers into {thing: int} (lowercased)."""
    out: dict[str, int] = {}
    for k, v in dict(headers).items():
        m = _COUNT_RE.match(str(k).strip().lower())
        if m:
            try:
                out[m.group(1)] = int(v)
            except (TypeError, ValueError):
                continue
    return out


# --------------------------------------------------------------------------- #
# Schema normalization, dedup key, censoring (pure)
# --------------------------------------------------------------------------- #
def normalize_record(row: dict, schema: str) -> dict:
    """Map a raw WQP result row (legacy or wqx3) to canonical field names.

    Unmapped/absent columns become "" so downstream code is schema-agnostic.
    """
    if schema not in SCHEMA_PATH:
        raise ValueError(f"unknown schema {schema!r}")
    out = {"schema": schema}
    for canon, cols in COLUMN_CROSSWALK.items():
        col = cols.get(schema, "")
        val = row.get(col, "") if col else ""
        out[canon] = ("" if val is None else str(val)).strip()
    return out


def observation_key(norm: dict) -> str:
    """Stable cross-schema identity hash of a normalized record.

    Same physical observation served by either schema -> same key (see IDENTITY_FIELDS).
    Value/status excluded so revisions reconcile rather than duplicate. Use to dedup a
    legacy+WQX3 union to one canonical record set (METADATA §10, Codex #1).
    """
    parts = [norm.get(f, "").strip().lower() for f in IDENTITY_FIELDS]
    return hashlib.sha1("\x1f".join(parts).encode("utf-8")).hexdigest()


def censoring_state(norm: dict) -> str:
    """Classify a result as detected / non_detect / below_quant / present / censored / missing.

    Distinguishes MEASURED ABSENCE from MISSING (a project rule). Never returns 0 and
    never imputes — that is a later, explicit modeling step (METADATA §4, Codex #2).
    """
    value = (norm.get("value") or "").strip()
    dc = (norm.get("detection_condition") or "").strip().lower()
    if dc:
        if "below" in dc and ("quant" in dc or "report" in dc):
            return "below_quant"
        if "not detected" in dc or "non-detect" in dc or "not-detect" in dc:
            return "non_detect"
        if "present" in dc:
            return "present"
        return "censored"          # some detection condition set, but unrecognized text
    if value == "" or value.upper() == "NA":
        return "missing"
    try:
        float(value)
        return "detected"
    except ValueError:
        return "missing"           # non-numeric, no detection condition -> can't use as a number


# --------------------------------------------------------------------------- #
# Network helpers (take a _common.net session; import net lazily)
# --------------------------------------------------------------------------- #
def _net():
    from _common import net       # noqa: PLC0415 — lazy so pure logic imports offline
    return net


def count_headers(session, url: str, timeout: int = 90) -> dict:
    """GET ``url`` but read only the response headers -> {thing: int} counts.

    Streams and closes without consuming the body, so a station/result count is cheap.
    """
    with session.get(url, stream=True, timeout=timeout, allow_redirects=True) as r:
        r.raise_for_status()
        return parse_counts(r.headers)


def query_dest(dest_dir: Path, endpoint: str, schema: str, url: str, ext: str = "csv") -> Path:
    """Deterministic cache path for a query URL: <endpoint>_<schema>_<sha1[:12]>.<ext>."""
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return Path(dest_dir) / f"{endpoint}_{schema}_{h}.{ext}"


def fetch_csv_to_cache(session, url: str, dest: Path, manifest_path: Path,
                       *, endpoint: str = "", schema: str = "") -> "object":
    """Cached GET of a WQP CSV query to ``dest`` (via net.download_file) + manifest append.

    Returns the net.DownloadResult. Re-runs are cache hits; the manifest is the audit
    trail (url, sha256, bytes, access time). No auth is needed for WQP.
    """
    net = _net()
    dest = Path(dest)
    res = net.download_file(session, url, dest, min_bytes=1)
    net.append_manifest(Path(manifest_path), {
        "url": res.url, "path": str(res.path), "bytes": res.bytes, "sha256": res.sha256,
        "cached": res.cached, "accessed_utc": res.accessed_utc,
        "endpoint": endpoint, "schema": schema,
    })
    return res


def count_csv_records(path) -> int:
    """Count DATA records in a CSV (excludes header; handles quoted embedded newlines)."""
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        n = sum(1 for _ in _csv.reader(f))
    return max(0, n - 1)


def _download_fresh(session, url, dest, manifest_path, endpoint, schema):
    """download_file caches by path; delete first so a retry actually re-fetches."""
    dest = Path(dest)
    if dest.exists():
        dest.unlink()
    return fetch_csv_to_cache(session, url, dest, manifest_path,
                              endpoint=endpoint, schema=schema)


def fetch_results_verified(session, params: dict, schema: str, dest_dir: Path,
                           manifest_path: Path, *, tries: int = 3):
    """Fetch Result rows with a TRUNCATION GUARD, and retry if short.

    WQP streams large (cold) responses and can close the connection early (a clean but
    premature EOF), which otherwise gets cached as if complete (observed 2026-07-01:
    a county WQX3 pull truncated to 1,828/7,320 rows). We verify record counts:
      * legacy: must EQUAL the free `Total-Result-Count` header.
      * wqx3:   must be >= the legacy count for the same query (WQX3 is a superset of the
                shared history; it only adds post-2024 USGS data). This uses the free legacy
                header as a lower bound — no double download.
    Returns (path, n_records, expected, ok). ``ok=False`` means it never verified (caller warns).
    A zero legacy lower bound (e.g. a post-split USGS-only query) can't bound wqx3 -> ok=True
    but the count is only diagnostic.
    """
    leg_url = build_query_url("Result", params, schema="legacy")
    expected = count_headers(session, leg_url).get("result")     # free; also wqx3 lower bound
    url = (leg_url if schema == "legacy"
           else build_query_url("Result", params, schema="wqx3", dataProfile="narrow"))
    last_path, last_n = None, 0
    for _ in range(max(1, tries)):
        dest = query_dest(dest_dir, "Result", schema, url)
        res = _download_fresh(session, url, dest, manifest_path, "Result", schema)
        n = count_csv_records(res.path)
        last_path, last_n = res.path, n
        if expected is None:
            return last_path, n, expected, True          # nothing to verify against
        if schema == "legacy" and n == expected:
            return last_path, n, expected, True
        if schema == "wqx3" and n >= expected:
            return last_path, n, expected, True
        # else: short read (truncation) -> loop and re-fetch (warm server returns full)
    return last_path, last_n, expected, False


def hab_query_params(scope: dict, characteristics: Optional[Iterable[str]] = None) -> dict:
    """Assemble a HAB-relevant query param dict from a scope + characteristic list.

    ``scope`` may contain any of: bBox, statecode, countycode, huc, siteid, startDateLo,
    startDateHi, siteType, sampleMedia, providers. Adds the HAB characteristic list and a
    default ``sampleMedia=Water`` unless the scope overrides it (Codex #15).
    """
    q = {k: v for k, v in dict(scope or {}).items() if v not in (None, "", [])}
    q.setdefault("sampleMedia", "Water")
    chars = list(characteristics) if characteristics is not None else list(HAB_CHARACTERISTICS)
    if chars:
        q["characteristicName"] = chars
    return q
