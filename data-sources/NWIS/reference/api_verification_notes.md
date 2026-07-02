# NWIS Water Data OGC API — empirical verification notes

Raw facts established by hitting the live API on **2026-07-01/02** (reproducible via
`access/pull_nwis.py` and the queries below). Preserved here so the audit trail survives even
if the docs move. Base: `https://api.waterdata.usgs.gov/ogcapi/v0`.

## Service & auth
- OGC API – Features implementation; landing `/`, `/collections`, `/openapi`, `/conformance`.
- **Service build version** in the `X-Build-Version` response header — was `0.59.3-6385dcba`.
- **No auth required.** Gateway = **API Umbrella** (`X-Api-Umbrella-Request-Id`, `Via: … api-umbrella`).
- **Optional API key** raises limits; pass via `X-Api-Key` header or `api_key=` query param.
  Signup: `https://api.waterdata.usgs.gov/signup/`.

## Rate limit (verified)
- Keyless: **`X-Ratelimit-Limit: 1000`** requests/hour. Exceeded → **HTTP 429**, body
  `{"error":{"code":"OVER_RATE_LIMIT", ...}}`, header **`Retry-After`** (observed 122–330 s).
- ~20 rapid requests under the limit all returned 200 (no per-request throttle headers until near/over).
- Keyed limit is higher (per-key; exact value not published — contact `wdfn@usgs.gov`).
- ⚠ Heavy keyless use can also cause **connection stalls** (gateway/CloudFront), not just clean 429s
  → the client uses short read timeouts + `read=0` retry so a stall fails fast instead of hanging.

## Pagination & formats
- **No total count**: `numberMatched: null`. Page by following `rel=next` links (cursor).
- `limit` verified working up to **20000** (16 MB response); a full page still carries a `next` link.
- Empty result → 0 features (and no `next`); the client also stops on any empty page (loop guard).
- Formats: `f=json` (GeoJSON) and `f=csv` (compact; columns incl. `x,y`). `Cache-Control: public, max-age=3600`.

## Collections used
- Data: `daily`, `continuous`, `latest-daily`, `latest-continuous`, `field-measurements`, `peaks`.
- Metadata: `monitoring-locations`, `time-series-metadata`, `combined-metadata`.
- Reference (counts verified): `parameter-codes` **19,675**; `hydrologic-unit-codes` **125,119**
  (full WBD hierarchy w/ names + classification codes); plus `states`, `counties`, `statistic-codes`, etc.
- Full list captured in `ogc_v0_collections.json`.

## Filter parameters (verified) — **they differ by collection!**
- `monitoring-locations`: `hydrologic_unit_code` (**prefix** match — HUC-8 returns its HUC-12 children),
  `bbox=minlon,minlat,maxlon,maxlat`, `state_code`, `county_code`, `site_type_code`, **`id`** (full
  `USGS-…`). ⚠ `monitoring_location_id` **400s here** (and a comma-joined id list 400s everywhere).
- `daily`: `monitoring_location_id` (full `USGS-…`), `parameter_code`, `statistic_id`,
  `datetime=START/END` (OGC interval, `..` open-ended). ⚠ does **not** accept `hydrologic_unit_code`/`bbox`.
- `continuous`: same as daily minus `statistic_id`.
- `time-series-metadata`: `monitoring_location_id`, `parameter_code`, **and AOI filters** —
  `hydrologic_unit_code`, `state_name` (verified keyed 2026-07-02; an early keyless probe wrongly
  returned empty, likely throttled). So an AOI-wide catalog IS possible in one paged query. (Our
  `pull_nwis.py` still catalogs per enumerated site: the site set is already narrowed by
  enumeration + the `--max-sites` guard, so per-site is targeted and uniform across AOI types.)
  Queryables: `…/time-series-metadata/queryables`. NB the data collections (`daily`/`continuous`)
  do **not** accept AOI filters — site (`monitoring_location_id`) + param + datetime only.

## Record shape (data collections)
`time_series_id, monitoring_location_id (USGS-…), parameter_code, statistic_id (daily only),
time, value (STRING), unit_of_measure, approval_status ∈ {Provisional, Approved}, qualifier (list
e.g. ["Ice"], ["DISCONTINUED"], or null), last_modified`. No fill value — missing obs are omitted.

## Catalog shape (time-series-metadata)
`id (=time_series_id), parameter_code, parameter_name, statistic_id, computation_period_identifier
(Daily / Points / Water Year / …), computation_identifier (Mean / Instantaneous / …), begin, end,
begin_utc, end_utc, last_modified, primary, unit_of_measure, hydrologic_unit_code, thresholds[]`.
→ `Daily` maps to the `daily` collection; `Points` to `continuous`. `end` far in the past = discontinued.

## Geotagging / linkage (verified)
- `monitoring-locations` properties include: `id` (`USGS-01646500`), `monitoring_location_number`
  (`01646500`), lat/lon (GeoJSON Point, EPSG:4326; `original_horizontal_datum` usually NAD83),
  `hydrologic_unit_code` (HUC-8…HUC-12; `020700081005` for 01646500), `state_code`/`county_code`
  (FIPS), `drainage_area`, `altitude`+`vertical_datum`.
- **WQP join is exact:** WQP returns `USGS-01646500` with `OrganizationIdentifier=USGS-MD`,
  `ProviderName=NWIS`, `HUCEightDigitCode=02070008`. The OGC id == WQP MonitoringLocationIdentifier.
- A HUC-8 (`02070008`) monitoring-locations query returns **1,903 sites** in 1.6 s (one page):
  GW=1565, ST=241, SP=61, AT=10, LK=4, … across agencies USGS=1869, MD007=13, VA087=19, USEPA=1.
  (Legacy `siteStatus=active` returned only 52 — OGC includes all types + inactive.)

## Licensing
- USGS data = **U.S. Public Domain**; requested credit "U.S. Geological Survey".
- Provisional disclaimer (verbatim in `provisional_and_disclaimer_verbatim.txt`): provisional data
  are *"subject to revision"*, provided with no warranty, USGS/US-Gov not liable for damages from use.
