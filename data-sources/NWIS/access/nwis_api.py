#!/usr/bin/env python
"""USGS NWIS **Water Data OGC API** client + constants for the SePRO HAB PoC.

Everything here targets the modern service at ``https://api.waterdata.usgs.gov/ogcapi/v0``.
The legacy ``waterservices.usgs.gov`` REST/RDB service is scheduled for **decommission in
early 2027** (see ``METADATA.md`` §0/§7); a couple of thin legacy helpers are kept ONLY for
cross-checking during the transition, clearly marked ``legacy_*``.

Design goals (per the project fidelity/reproducibility rules and the CyAN reference impl):
  * No fabrication — every constant/behaviour below was verified live against the API on
    2026-07-01 (probes reproduced by ``pull_nwis.py``). Ambiguities are flagged, not smoothed.
  * Auth-optional — the OGC API is public; an optional free API key (``NWIS_API_KEY`` in
    ``../.env``) only raises rate limits. It is sent as the ``X-Api-Key`` header (never in the
    URL, so it can't leak into logs/manifests).
  * Cursor pagination — the OGC API returns **no total count** (``numberMatched: null``); you
    page by following ``rel=next`` links. ``iter_items`` handles this transparently.

Key encodings (verified 2026-07-01):
  * A monitoring-location ``id`` is already in **Water Quality Portal form**, e.g.
    ``USGS-01646500`` (agency-prefixed). Non-USGS agencies appear too (e.g. ``MD007-...``).
  * Data records carry ``approval_status`` ∈ {``Provisional``, ``Approved``} and an optional
    ``qualifier`` list (e.g. ``["DISCONTINUED"]``); ``last_modified`` is per-record.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- make `_common` importable when this module is used from anywhere -------- #
_DATA_SOURCES = Path(__file__).resolve().parents[2]
import sys
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))
from _common import net  # noqa: E402  (.env loader, manifest helpers, sha/utc utils)

# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #
OGC_BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"
LEGACY_BASE = "https://waterservices.usgs.gov/nwis"   # ⚠ decommissioned early 2027

# Data collections (OGC "collections"); see reference/ogc_v0_collections.json for the full list.
COLL_DAILY = "daily"                       # daily statistic values (DV) — the modeling core
COLL_CONTINUOUS = "continuous"             # instantaneous / real-time values (IV), ~5–60 min
COLL_LATEST_DAILY = "latest-daily"         # latest daily value per series
COLL_LATEST_CONTINUOUS = "latest-continuous"
COLL_FIELD = "field-measurements"          # discrete field measurements (ad hoc)
COLL_SITES = "monitoring-locations"        # site metadata (geotagging + HUC + FIPS)
COLL_TS_META = "time-series-metadata"      # per-series catalog (period of record, active/stale)

# --------------------------------------------------------------------------- #
# HAB-relevant parameters (USGS 5-digit "pcodes"). The full system has 19,675
# pcodes (verified); these are the subset the brief's fusion needs. Discrete
# nutrients (e.g. total P 00665, nitrate+nitrite 00631) live mostly in the Water
# Quality Portal — pull those from `wqp`, not here (see METADATA.md §9).
# tuple = (short_name, unit, group, plausible_range_for_QA) — range is a LOOSE
# encoding-sanity bound (flag values outside it), NOT a scientific judgement.
# --------------------------------------------------------------------------- #
HAB_PARAMETERS: dict[str, tuple[str, str, str, tuple[float, float]]] = {
    "00060": ("Discharge",            "ft3/s",  "hydrology", (-1e5, 5e6)),   # tidal sites can be < 0
    "00065": ("Gage height",          "ft",     "hydrology", (-50.0, 200.0)),
    "00010": ("Water temperature",    "degC",   "physical",  (-1.0, 45.0)),
    "00095": ("Specific conductance", "uS/cm",  "physical",  (0.0, 2e5)),
    "00300": ("Dissolved oxygen",     "mg/L",   "chemistry", (0.0, 30.0)),
    "00400": ("pH",                   "std",    "chemistry", (0.0, 14.0)),
    "63680": ("Turbidity",            "FNU",    "physical",  (0.0, 5e4)),
    "99133": ("Nitrate (in situ)",    "mg/L-N", "chemistry", (0.0, 5e3)),
}

# Daily statistic codes (verified present at real sites).
STAT_CODES = {"00001": "maximum", "00002": "minimum", "00003": "mean", "00008": "median"}
DEFAULT_STAT = "00003"   # daily mean — the standard streamflow/DV statistic

# Site types most relevant to a lake/stream HAB study (full list in reference collection `site-types`).
SITE_TYPES = {"ST": "Stream", "LK": "Lake/Reservoir/Impoundment", "SP": "Spring",
              "ES": "Estuary", "GW": "Groundwater well", "AT": "Atmospheric"}

# Legacy WaterML fill value (only relevant to the legacy_* helpers).
LEGACY_NODATA = -999999.0

APPROVAL_APPROVED = "Approved"
APPROVAL_PROVISIONAL = "Provisional"


# --------------------------------------------------------------------------- #
# Credentials (optional)
# --------------------------------------------------------------------------- #
def resolve_api_key(dotenv_path: Optional[Path] = None) -> Optional[str]:
    """Return an optional USGS Water Data API key from env or a .env file, or None.

    The OGC API is public; a key only raises rate limits. Accepts ``NWIS_API_KEY`` or
    ``USGS_API_KEY``. Get one (free) at https://api.waterdata.usgs.gov/signup/.
    Passed as the ``X-Api-Key`` header (see ``_headers``) so it never lands in a URL/log.
    """
    if dotenv_path is not None:
        net.load_dotenv(dotenv_path)
    for var in ("NWIS_API_KEY", "USGS_API_KEY"):
        v = os.environ.get(var, "").strip()
        if v:
            return v
    return None


def _headers(api_key: Optional[str]) -> dict:
    h = {"Accept": "application/json"}
    if api_key:
        h["X-Api-Key"] = api_key
    return h


class OGCResponseError(RuntimeError):
    """Raised when a 2xx response is not a well-formed OGC Features payload.

    The API-Umbrella/CloudFront gateway can return HTML or truncated bodies on some errors,
    and schema drift is possible on a young service — so we validate rather than assume every
    2xx is valid GeoJSON with a list ``features`` (which would otherwise fail obscurely or
    silently yield zero rows).
    """


class RateLimitError(RuntimeError):
    """Raised on HTTP 429 from the OGC gateway (keyless limit = 1000 requests/hour).

    Carries ``retry_after`` (seconds) and ``limit`` from the response headers so callers
    can print a clear, actionable message instead of hanging on blind retries.
    """
    def __init__(self, retry_after: Optional[int], limit: Optional[str]):
        self.retry_after = retry_after
        self.limit = limit
        super().__init__(
            f"NWIS OGC API rate limit hit (limit={limit or '?'}/hour, keyless). "
            f"Retry-After≈{retry_after or '?'}s. Set a free API key (NWIS_API_KEY in "
            f"data-sources/.env — https://api.waterdata.usgs.gov/signup/) to raise the limit, "
            f"or wait and retry."
        )


def make_nwis_session(user_agent: str = "SePRO-HAB-PoC/0.1 (data-sources/NWIS)") -> requests.Session:
    """A session that retries only transient 5xx — NOT 429.

    Deliberately excludes 429 from the retry list: the gateway's ``Retry-After`` on a 429 is
    ~330 s, and urllib3 would block on it *and* each retry burns more of the hourly quota.
    We instead surface 429 as a clear ``RateLimitError`` (see ``_raise_for_rate_limit``).
    """
    # read=0: do NOT retry a stalled socket read. A hung keyless connection with read-retries
    # would block up to read*timeout seconds (minutes) per request; instead fail that one request
    # fast and let the caller move on / --refresh it. Still retry connection resets and 5xx.
    retry = Retry(
        total=3, connect=3, read=0, status=3,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 503, 504),   # note: 429 intentionally absent (raised, not retried)
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    s = requests.Session()
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({"User-Agent": user_agent})
    return s


def _raise_for_rate_limit(r: requests.Response) -> None:
    if r.status_code == 429:
        ra = r.headers.get("Retry-After")
        raise RateLimitError(int(ra) if ra and ra.isdigit() else None,
                             r.headers.get("X-Ratelimit-Limit"))


# --------------------------------------------------------------------------- #
# Monitoring location (site) model
# --------------------------------------------------------------------------- #
@dataclass
class MonitoringLocation:
    """A parsed OGC monitoring-location feature (the fields we care about)."""
    id: str                       # e.g. "USGS-01646500" (== WQP MonitoringLocationIdentifier)
    agency_code: Optional[str]
    site_no: Optional[str]        # bare NWIS number, e.g. "01646500"
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    huc: Optional[str]            # hydrologic_unit_code (HUC-8 … HUC-12; varies by site)
    state_code: Optional[str]
    county_code: Optional[str]
    site_type_code: Optional[str]
    site_type: Optional[str]
    drainage_area: Optional[float]
    altitude: Optional[float]
    vertical_datum: Optional[str]
    horizontal_datum: Optional[str]
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def wqp_id(self) -> str:
        """Water Quality Portal identifier — identical to ``id`` for USGS sites."""
        return self.id

    @property
    def huc8(self) -> Optional[str]:
        return self.huc[:8] if self.huc else None


def _f(v) -> Optional[float]:
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def parse_monitoring_location(feature: dict) -> MonitoringLocation:
    p = feature.get("properties", {})
    geom = feature.get("geometry") or {}
    coords = geom.get("coordinates") or [None, None]
    lon, lat = (coords + [None, None])[:2]
    # Prefer geometry coords; fall back to any property lat/lon.
    return MonitoringLocation(
        id=feature.get("id") or p.get("id"),
        agency_code=p.get("agency_code"),
        site_no=p.get("monitoring_location_number"),
        name=p.get("monitoring_location_name"),
        latitude=_f(lat), longitude=_f(lon),
        huc=p.get("hydrologic_unit_code"),
        state_code=p.get("state_code"),
        county_code=p.get("county_code"),
        site_type_code=p.get("site_type_code"),
        site_type=p.get("site_type"),
        drainage_area=_f(p.get("drainage_area")),
        altitude=_f(p.get("altitude")),
        vertical_datum=p.get("vertical_datum"),
        horizontal_datum=p.get("original_horizontal_datum"),
        raw=p,
    )


def to_wqp_id(site_no: str, agency: str = "USGS") -> str:
    """Build the WQP/OGC identifier from a bare NWIS site number: ``USGS-01646500``."""
    site_no = str(site_no).strip()
    return site_no if "-" in site_no else f"{agency}-{site_no}"


# --------------------------------------------------------------------------- #
# Core OGC paging
# --------------------------------------------------------------------------- #
def _next_href(links: list[dict]) -> Optional[str]:
    for l in links or []:
        if l.get("rel") == "next" and l.get("href"):
            return l["href"]
    return None


def iter_items(
    session: requests.Session,
    collection: str,
    params: dict,
    api_key: Optional[str] = None,
    page_size: int = 10000,
    max_items: int = 0,
    timeout: tuple = (10, 45),   # (connect, read) — short read so a stalled socket fails fast
) -> Iterator[dict]:
    """Yield features from an OGC ``collection``, transparently following ``next`` links.

    ``params`` are the query filters (e.g. ``monitoring_location_id``, ``parameter_code``,
    ``datetime``). ``page_size`` sets ``limit`` (verified working up to 20000). ``max_items``
    caps the total yielded (0 = no cap) — useful for ``--limit`` sampling.

    The OGC API does not return a total count, so callers cannot know progress up-front;
    we simply page until there is no ``next`` link or the cap is hit.
    """
    q = dict(params)
    q.setdefault("f", "json")
    q["limit"] = page_size
    url = f"{OGC_BASE}/collections/{collection}/items"
    yielded = 0
    while True:
        r = session.get(url, params=q if url.endswith("/items") else None,
                        headers=_headers(api_key), timeout=timeout)
        _raise_for_rate_limit(r)
        r.raise_for_status()
        try:
            doc = r.json()
        except ValueError as e:
            raise OGCResponseError(
                f"Non-JSON 2xx response from {r.url} (status {r.status_code}, "
                f"content-type {r.headers.get('Content-Type')!r}): {r.text[:200]!r}") from e
        if not isinstance(doc, dict) or not isinstance(doc.get("features"), list):
            raise OGCResponseError(
                f"Unexpected OGC payload from {r.url}: "
                f"{list(doc)[:8] if isinstance(doc, dict) else type(doc).__name__}")
        feats = doc["features"]
        for feat in feats:
            yield feat
            yielded += 1
            if max_items and yielded >= max_items:
                return
        nxt = _next_href(doc.get("links", []))
        # Stop on no-next OR an empty page — guards against an empty trailing page that
        # still advertises a `next` link (would otherwise loop forever).
        if not nxt or not feats:
            return
        # The next link is a fully-formed URL carrying the cursor; GET it verbatim.
        url, q = nxt, None


def get_response_build_version(session: requests.Session, api_key: Optional[str] = None) -> Optional[str]:
    """Return the OGC service build version (``X-Build-Version`` header) for provenance.

    Analogue of CyAN's ``OBPG_version``: records which server build produced a pull, so a
    later value change is attributable. Cheap HEAD-like GET of the landing page.
    """
    try:
        r = session.get(f"{OGC_BASE}/?f=json", headers=_headers(api_key), timeout=30)
        _raise_for_rate_limit(r)
        return r.headers.get("X-Build-Version")
    except (requests.RequestException, RateLimitError):
        return None


# --------------------------------------------------------------------------- #
# Site enumeration (geotagging / AOI discovery — auth-free & cheap)
# --------------------------------------------------------------------------- #
def enumerate_sites(
    session: requests.Session,
    *,
    huc: Optional[str] = None,               # HUC prefix (HUC-8 matches its HUC-12 children)
    bbox: Optional[Iterable[float]] = None,  # (min_lon, min_lat, max_lon, max_lat)
    state_code: Optional[str] = None,        # FIPS, e.g. "24" (Maryland)
    county_code: Optional[str] = None,
    site_type_code: Optional[str] = None,    # e.g. "ST", "LK"; comma-joined allowed
    site_ids: Optional[Iterable[str]] = None,
    extra: Optional[dict] = None,
    api_key: Optional[str] = None,
    page_size: int = 10000,
    max_sites: int = 0,
) -> list[MonitoringLocation]:
    """Enumerate monitoring locations for an area of interest.

    Verified filters (2026-07-01): ``hydrologic_unit_code`` (prefix match — HUC-8 returns
    sites in that HUC), ``bbox``, ``state_code``, ``county_code``, ``site_type_code``,
    ``monitoring_location_id``. Note: monitoring-locations has no direct "active" flag —
    activity/staleness comes from the time-series catalog (``time-series-metadata``); we do
    not silently assume a site is active here.
    """
    # Explicit site ids. NOTE (verified 2026-07-01): on `monitoring-locations` the id filter
    # is the OGC-standard `id` (full form, e.g. USGS-01646500) — NOT `monitoring_location_id`
    # (that 400s here, though it IS the correct filter on daily/continuous/time-series-metadata).
    # `id` takes a single value, so query per id and merge.
    if site_ids:
        out: list[MonitoringLocation] = []
        for sid in site_ids:
            feats = iter_items(session, COLL_SITES, {"id": sid},
                               api_key=api_key, page_size=page_size)
            out.extend(parse_monitoring_location(f) for f in feats)
            if max_sites and len(out) >= max_sites:
                return out[:max_sites]
        return out

    params: dict = {}
    if huc:
        params["hydrologic_unit_code"] = huc
    if bbox:
        params["bbox"] = ",".join(str(x) for x in bbox)
    if state_code:
        params["state_code"] = state_code
    if county_code:
        params["county_code"] = county_code
    if site_type_code:
        params["site_type_code"] = site_type_code
    if extra:
        params.update(extra)
    if not params:
        raise ValueError("enumerate_sites needs at least one filter (huc/bbox/state/site_ids/…) — "
                         "refusing to enumerate the entire national network.")
    feats = iter_items(session, COLL_SITES, params, api_key=api_key,
                       page_size=page_size, max_items=max_sites)
    return [parse_monitoring_location(f) for f in feats]


# --------------------------------------------------------------------------- #
# Time-series catalog (which parameters exist where, and are they stale?)
# --------------------------------------------------------------------------- #
def catalog_series(
    session: requests.Session,
    site_id: str,
    parameter_codes: Optional[Iterable[str]] = None,
    api_key: Optional[str] = None,
    page_size: int = 10000,
) -> list[dict]:
    """Return the per-series catalog for a site (period of record + computation type).

    Each dict (verified fields, 2026-07-01): ``time_series_id`` (``id``), ``parameter_code``,
    ``parameter_name``, ``statistic_id``, ``computation_period_identifier`` (``Daily`` /
    ``Points`` / ``Water Year`` / …), ``computation_identifier`` (``Mean`` / ``Instantaneous`` /
    …), ``begin`` / ``end`` (period of record), ``last_modified``, ``primary``,
    ``unit_of_measure``, ``hydrologic_unit_code``. Optionally filtered to ``parameter_codes``
    (client-side, so multiple codes are fine).

    This is the honest answer to "which features exist at this site, and which are stale":
    a series whose ``end`` is far in the past is discontinued; ``end`` near today is active.
    """
    feats = iter_items(session, COLL_TS_META, {"monitoring_location_id": site_id},
                       api_key=api_key, page_size=page_size)
    want = set(parameter_codes) if parameter_codes else None
    out = []
    for f in feats:
        p = f.get("properties", {})
        if want and p.get("parameter_code") not in want:
            continue
        out.append(p)
    return out


def series_service(series: dict) -> Optional[str]:
    """Map a catalog series' computation period to the data collection that serves it.

    ``Daily`` → the ``daily`` collection; ``Points`` (instantaneous) → ``continuous``.
    Other periods (``Water Year`` peaks, etc.) return None — not pulled by this tool.
    """
    cpi = (series.get("computation_period_identifier") or "").strip().lower()
    if cpi == "daily":
        return COLL_DAILY
    if cpi == "points":
        return COLL_CONTINUOUS
    return None


def series_is_active(series: dict, today: str, within_days: int = 60) -> Optional[bool]:
    """True if the series' ``end`` date is within ``within_days`` of ``today`` (YYYY-MM-DD).

    Returns None if the end date can't be parsed. Cheap staleness heuristic for reporting;
    no external tz/date libs (avoids importing datetime-with-tz churn) — compares date ordinals.
    """
    end = (series.get("end") or "")[:10]
    if len(end) != 10 or len(today) != 10:
        return None
    try:
        from datetime import date
        ey, em, ed = (int(x) for x in end.split("-"))
        ty, tm, td = (int(x) for x in today.split("-"))
        return (date(ty, tm, td) - date(ey, em, ed)).days <= within_days
    except (ValueError, TypeError):
        return None


# --------------------------------------------------------------------------- #
# Time-series pulls (daily / continuous)
# --------------------------------------------------------------------------- #
def _datetime_interval(start: Optional[str], end: Optional[str]) -> Optional[str]:
    """Build an OGC ``datetime`` interval 'start/end' from YYYY-MM-DD bounds (open-ended ok)."""
    if not start and not end:
        return None
    return f"{start or '..'}/{end or '..'}"


def fetch_series(
    session: requests.Session,
    service: str,                 # COLL_DAILY or COLL_CONTINUOUS
    site_id: str,                 # "USGS-01646500"
    parameter_code: str,
    statistic_id: Optional[str] = None,   # daily only (e.g. "00003"); ignored for continuous
    start: Optional[str] = None,
    end: Optional[str] = None,
    api_key: Optional[str] = None,
    page_size: int = 20000,
    max_items: int = 0,
) -> list[dict]:
    """Return a list of observation ``properties`` dicts for one site+parameter(+stat) series.

    Each record has: time_series_id, monitoring_location_id, parameter_code, statistic_id
    (daily), time, value, unit_of_measure, approval_status, qualifier, last_modified.
    Values are returned **as strings** by the API — kept verbatim here; typed in QA/analysis.
    """
    if service not in (COLL_DAILY, COLL_CONTINUOUS):
        raise ValueError(f"service must be '{COLL_DAILY}' or '{COLL_CONTINUOUS}', got {service!r}")
    params: dict = {"monitoring_location_id": site_id, "parameter_code": parameter_code}
    if service == COLL_DAILY and statistic_id:
        params["statistic_id"] = statistic_id
    dti = _datetime_interval(start, end)
    if dti:
        params["datetime"] = dti
    return [f.get("properties", {}) for f in
            iter_items(session, service, params, api_key=api_key,
                       page_size=page_size, max_items=max_items)]


# --------------------------------------------------------------------------- #
# Legacy cross-check helpers (⚠ decommissioned early 2027 — do NOT build on these)
# --------------------------------------------------------------------------- #
def legacy_site_catalog_rdb(session: requests.Session, sites: str) -> str:
    """Return the legacy period-of-record catalog (RDB text) for one or more sites.

    Convenient during the transition to sanity-check the OGC ``time-series-metadata``
    (parameters × statistics × begin/end dates × counts, with ``[Discontinued]`` flags).
    """
    params = {"format": "rdb", "sites": sites, "seriesCatalogOutput": "true"}
    r = session.get(f"{LEGACY_BASE}/site/", params=params, timeout=60)
    r.raise_for_status()
    return r.text


def parse_rdb(text: str) -> list[dict]:
    """Parse USGS RDB (tab-delimited, '#'-comments, header row + type row) into dicts."""
    rows: list[dict] = []
    header: Optional[list[str]] = None
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        if header is None:
            header = cols
            continue
        if len(cols) == len(header) and re.match(r"^\d+[sndx]$", cols[0] or "x"):
            continue  # RDB type/width row, e.g. "5s\t15s\t..."
        rows.append(dict(zip(header, cols)))
    return rows
