# USGS NWIS (Water Data OGC API) — In-situ Hydrology & Water-Quality — Dataset Metadata

**Dataset short name:** NWIS (National Water Information System), served via the **USGS Water Data OGC API**
**Product this file describes:** point **monitoring-location** metadata + **daily (DV)** and **continuous/real-time (IV)** time-series for a HAB-relevant parameter set
**Service version documented:** OGC API build `0.59.3` (read from the `X-Build-Version` response header, 2026-07-01)
**Compiled:** 2026-07-01 · **Access date for all live checks below:** 2026-07-01 (keyed multi-site validation 2026-07-02)
**Compiled by:** Claude (Opus 4.8) with Arik. Every quantitative claim traces to a cited primary source or to an empirical check we ran (endpoint + script noted). Ambiguities are flagged, not smoothed over.

> **⚠️ MIGRATION — the single most important fact.** The **legacy `waterservices.usgs.gov` REST/RDB service is scheduled for decommission in early 2027** (banner on `https://waterservices.usgs.gov/`, verified 2026-07-01). This is the backend the classic `dataRetrieval`/`dataretrieval` calls historically used. **We therefore build on the new OGC API at `https://api.waterdata.usgs.gov/ogcapi/v0`** and keep only thin legacy helpers for cross-checking during the transition (`access/nwis_api.py: legacy_*`). Anything built on legacy endpoints must be rewritten before early 2027.

> **⚡ QUICK API ACCESS (future Claude instances start here).**
> - **Base:** `https://api.waterdata.usgs.gov/ogcapi/v0` · **no auth required.** The client auto-uses an **API key** from `NWIS_API_KEY` (or `USGS_API_KEY`) in `data-sources/.env` if present — it lifts the keyless **1000 req/hr** limit, which you *will* hit on any multi-site pull. *This working copy has a key configured; a fresh clone must add its own (`.env` is gitignored — see §7.3).*
> - **Use the repo client (preferred — handles auth, paging, rate limits, the per-collection filter quirks):**
>   ```python
>   from NWIS.access import nwis_api as nw          # run from data-sources/ (on sys.path)
>   s = nw.make_nwis_session(); key = nw.resolve_api_key(Path("data-sources/.env"))
>   sites = nw.enumerate_sites(s, huc="04100009", site_type_code="ST,LK", api_key=key)   # AOI -> sites
>   cat   = nw.catalog_series(s, "USGS-04193500", api_key=key)                            # what exists + POR
>   rows  = nw.fetch_series(s, nw.COLL_DAILY, "USGS-04193500", "00060", "00003",
>                           start="2015-01-01", end="2024-12-31", api_key=key)            # the data
>   ```
> - **Or the CLI** (`access/pull_nwis.py`) for cached+manifested pulls; **or raw HTTP** — e.g.
>   `GET /collections/daily/items?monitoring_location_id=USGS-04193500&parameter_code=00060&statistic_id=00003&datetime=2015-01-01/2024-12-31&f=csv` with header `X-Api-Key: <key>`.
> - **Three things that bite:** (1) site-id filter is `id` on `monitoring-locations` but `monitoring_location_id` on data collections (§7.2); (2) `numberMatched` is null — page via `next` links; (3) an unfiltered HUC returns ~1000s of sites (mostly groundwater) — always pass `site_type_code`/`--site-types`.

> **📦 CANONICAL LOCAL DATA STORE (start here in future sessions).** Pulled series live under **`data-sources/NWIS/data/raw/`** (gitignored — regenerate via `access/pull_nwis.py`):
> - **`sites/<aoi>_sites.csv`** — enumerated monitoring-location metadata (id, lat/lon, HUC, FIPS, drainage area) for each area of interest pulled.
> - **`daily/<site>__<param>__<stat>.csv`** and **`continuous/<site>__<param>.csv`** — one **tidy, row-per-observation** CSV per series (no aggregation), plus **`manifest.jsonl`** (sha256, counts, date span, provisional/approved split, OGC build version, access time).
> - This is a **feature/context source pulled per study area**, not a national mirror — NWIS is far too large to mirror and there is no need to (see §6).
> - **Validated demo on disk (2026-07-02, keyed):** 12 daily series across 8 stream sites (Potomac `01646500`/`01638500` + a HUC-8 `02070008` sample) — discharge/temperature/specific-conductance, sha-manifested, **0/12 QA flags**. Regenerate: `pull_nwis.py --sites 01646500 01638500 --params 00060 00010 --start 2015-01-01` and `--huc 02070008 --site-types ST --limit 20 --params 00060 00010 00095 --start 2015-01-01`.

---

## 0. TL;DR for the modeler (read this first)

| Question | Answer |
|---|---|
| What is it? | USGS **in-situ** water data: streamflow/stage + physical/chemical water-quality (temp, DO, pH, specific conductance, turbidity, nitrate) at **point monitoring locations** nationwide. |
| Native form | Per-observation records via an **OGC API Features** service (GeoJSON or CSV). One feature = one measurement (`time`, `value`, `approval_status`, `qualifier`, `last_modified`). |
| Resolution (space) | **Point** stations (lat/lon), not a grid. National, **~1.9M sites** total; density and parameter mix vary enormously by place (§3). |
| Resolution (time) | **Continuous** ≈ every **5–60 min** (real-time); **Daily** = one statistic/day; field measurements/peaks = ad hoc/annual (§2). |
| The value in a record | A measured quantity in the parameter's unit; **strings** in the API (typed downstream). Daily values carry a **statistic** (mean/max/min/median). |
| How to read it | `parameter_code` (5-digit pcode) + `unit_of_measure` + (daily) `statistic_id`; `approval_status` ∈ {Provisional, Approved}; `qualifier` list (e.g. `["Ice"]`, `["DISCONTINUED"]`) (§4). |
| Nodata / fill | OGC API simply **omits** missing observations (no fill). Legacy WaterML uses `-999999`. Provisional ≠ missing (it's real but revisable). |
| Access | **OGC API, no auth required.** Optional free **API key** raises rate limits (keyless = **1000 requests/hour**, verified) (§7). |
| Bulk or on-the-fly? | **API-first, per-AOI.** Enumerate sites by HUC/bbox/state → pull only the series you need → cache locally. **Do not mirror** NWIS (§6). |
| Likely role in our model | **Feature (drivers):** streamflow/temperature/nutrients that modulate blooms; **in-situ cross-check** for the CyAN satellite signal. **Not** the satellite target itself (§9). |
| Geotagging & linkage | lat/lon (NAD83), **HUC-8…HUC-12**, state/county **FIPS**, drainage area. Site id is already in **WQP form** `USGS-<siteno>` → **exact 1:1 join to the Water Quality Portal**; HUC gives a **spatial** link to EPA NARS (§13). |

---

## 1. What NWIS is

The **National Water Information System (NWIS)** is USGS's national archive of water data: streamflow, gage height, groundwater levels, and physical/chemical water quality, collected at fixed **monitoring locations** (gages, wells, springs, lake/estuary stations) by USGS and cooperating agencies. It is the in-situ counterpart to the CyAN satellite signal — the "ground" in a satellite-meets-in-situ fusion.

Historically NWIS was served through `waterservices.usgs.gov` (REST returning RDB/WaterML/JSON). USGS is consolidating everything under **Water Data for the Nation** and its **Water Data OGC API** (`api.waterdata.usgs.gov`), an **OGC API – Features** implementation with collections for data (`daily`, `continuous`, `field-measurements`, `peaks`, …), metadata (`monitoring-locations`, `time-series-metadata`), and reference tables (`parameter-codes`, `hydrologic-unit-codes`, `states`, `counties`, …). See `reference/ogc_v0_collections.json` for the full collection list captured 2026-07-01.

**Maturity / status:** NWIS is the authoritative, long-standing U.S. water-data system (records back to the 19th century for some gages). The **OGC API is newer** (build `0.59.3`) and is the *designated replacement* for legacy services (decommission early 2027). We treat the OGC API as production-appropriate but young — hence we pin the service build version and cross-check against legacy during the transition.

---

## 2. Temporal coverage, cadence & staleness

| Series kind | OGC collection | Cadence | Example (site 01646500, verified) |
|---|---|---|---|
| **Continuous / real-time (IV)** | `continuous` | **~5–60 min** | Discharge (00060) sub-hourly since 1972; latest value timestamped **minutes ago** (Provisional). |
| **Daily statistic (DV)** | `daily` | **1 value/day** per statistic | Daily-mean discharge since **1930-03-01**, ~35,186 days. |
| Field measurements | `field-measurements` | ad hoc (site visits) | discrete measurements, irregular. |
| Annual peaks | `peaks` | 1/water-year | peak-flow series. |

**Refresh / latency.** Real-time (continuous) data post with **~minutes-to-hours** latency (telemetry). Daily values are computed once the day closes. **This is far fresher than the CyAN weekly composite** — NWIS in-situ can *lead* the satellite signal.

**Provisional → Approved lifecycle (critical).** Recent data are **`Provisional`** ("subject to revision until … final approval"); older data become **`Approved`**. Even approved values can change on review/reprocessing — every record carries a **`last_modified`** timestamp, which we record so a later value change is attributable. (Verbatim disclaimer preserved in `reference/provisional_and_disclaimer_verbatim.txt`.)

**Staleness / discontinued series (a real feature of the data).** A site's parameter mix changes over time: sensors are added, retired, or replaced. The **per-site catalog** (`time-series-metadata`) gives each series' `begin`/`end` — an `end` far in the past = **discontinued**; `end` near today = **active**. Example (01646500): daily water-temperature ran 1988–2019 on one time-series, then a **new** series from 2019–present; specific conductance and DO show the same replace-in-place pattern. So **some series are permanently stale while a co-located newer series is live** — the catalog is the honest source of truth, and `pull_nwis.py --active-only` filters on it.

**Known temporal gaps.** Gaps are **per-site and non-random** (sensor outages, ice, funding, station relocation). There is no single national gap; each series must be inspected. Ice-affected periods are often qualifier-flagged rather than dropped.

---

## 3. Spatial characteristics

- **Geometry:** **point** monitoring locations — a `Point` in **EPSG:4326** (decimal lat/lon). Native stored datum is usually **NAD83** (`original_horizontal_datum`); positional accuracy and method are per-site fields (e.g. "Accurate to ± 1 sec", mapping-grade GPS).
- **National extent, wildly uneven density.** NWIS spans the U.S. and territories (**~1.9M sites** across all types; verify per-AOI rather than quoting nationally). We enumerated one HUC-8 (`02070008`, Middle Potomac) and got **52 active sites: 30 stream, 16 groundwater, 6 atmospheric** — a concrete illustration that **what's available is entirely place-dependent**.
- **Watershed tagging — `hydrologic_unit_code`.** Every site carries a HUC. Length **varies by site**: many older sites carry **HUC-8**; newer/updated sites carry down to **HUC-12** (site 01646500 = `020700081005`, a HUC-12). The reference collection `hydrologic-unit-codes` holds **125,119 HUCs** (full WBD hierarchy: region → subregion → … → HUC-12, with names + classification codes). This is the hook to Watershed Boundary Dataset polygons and to any HUC-indexed dataset (§13).
- **Administrative tagging:** `state_code` + `county_code` (**FIPS**), `minor_civil_division_code`, `district_code`, `country_code`.
- **Hydrologic descriptors:** `drainage_area` (sq mi), `contributing_drainage_area`, `altitude` + `vertical_datum` (e.g. NAVD88).
- **Minimum reliable unit:** a **station** — NWIS makes no claim about the area a point represents. For a lake HAB question, associating a gage to a lake is a modeling choice (nearest inflow/outflow gage, same HUC-12), **not** a property of the data. State it explicitly wherever a gage is used as a lake driver (correlation ≠ causation).
- **Non-USGS agencies present.** `monitoring-locations` includes cooperator sites with **non-`USGS-` ids** (e.g. `MD007-385839077055701`); most time-series data are on `USGS-` sites, but don't assume every enumerated id is `USGS-`.

---

## 4. Encoding & quality flags — EXACT scheme (authoritative)

A data record's `properties` (verified 2026-07-01, `daily`/`continuous` collections):

| Field | Meaning |
|---|---|
| `monitoring_location_id` | `USGS-01646500` (WQP form) |
| `parameter_code` | 5-digit USGS pcode (e.g. `00060`); **19,675** exist system-wide |
| `statistic_id` | daily only: `00001` max, `00002` min, `00003` mean, `00008` median (null for continuous) |
| `time` | observation timestamp (date for daily; datetime for continuous) |
| `value` | **string** measurement in `unit_of_measure` (typed downstream, not in the API) |
| `unit_of_measure` | e.g. `ft^3/s`, `degC`, `mg/l`, `uS/cm`, `pH Units`, `_FNU` |
| `approval_status` | **`Provisional`** (revisable) or **`Approved`** (final-but-revisable) |
| `qualifier` | list, e.g. `["Ice"]`, `["Estimated"]`, `["DISCONTINUED"]`, or `null` |
| `last_modified` | per-record revision timestamp (provenance / change-detection) |
| `time_series_id` | opaque id linking to `time-series-metadata` |

**HAB-relevant parameter codes** (the subset this repo pulls; see `access/nwis_api.py: HAB_PARAMETERS`):

| pcode | Name | Unit | Group |
|---|---|---|---|
| `00060` | Discharge | ft³/s | hydrology |
| `00065` | Gage height | ft | hydrology |
| `00010` | Water temperature | °C | physical |
| `00095` | Specific conductance | µS/cm | physical |
| `00300` | Dissolved oxygen | mg/L | chemistry |
| `00400` | pH | std units | chemistry |
| `63680` | Turbidity | FNU | physical |
| `99133` | Nitrate (in-situ sensor) | mg/L as N | chemistry |

**Nodata handling.** The OGC API **omits** missing observations (no fill value) — an absent day is simply not returned. Legacy WaterML/RDB uses **`-999999`** for gaps (relevant only to the `legacy_*` helpers). **Provisional is not missing** — it is a real, revisable measurement; keep the distinction (the NWIS analogue of CyAN's "measured non-detect ≠ missing").

**Discrete water chemistry lives in the Water Quality Portal, not here.** Lab-analyzed nutrients (total phosphorus `00665`, nitrate+nitrite `00631`, chlorophyll-a, cyanotoxins) are **discrete samples** surfaced through WQP (`wqp` dataset). NWIS here = **continuous/daily sensor** series. Pull discrete chemistry from WQP and **join by the shared `USGS-<siteno>` id** (§13).

---

## 5. Known issues & limitations (the honest list)

1. **Provisional data are revisable.** The newest (and most operationally useful) data are Provisional and *"subject to revision"*; USGS/US-Gov disclaim liability. Record `approval_status` + `last_modified`; re-pull before any launch and after time passes. See §4 and `reference/`.
2. **Coverage is biased and site-variable.** Gages cluster on managed rivers and populated basins; small lakes and headwaters are under-served. Parameter availability is **entirely per-site** — never assume a site has temperature/nutrients without checking the catalog (§2/§3).
3. **Discharge is a rating-curve estimate, not a direct measurement.** Streamflow is derived from stage via a rating that carries uncertainty (worse at extremes/ice). Treat as an estimate with error.
4. **Sensor artifacts.** Sonde parameters (DO, turbidity, pH, nitrate) are prone to fouling/drift; ice and debris cause flagged/estimated values. Qualifiers (`Ice`, `Estimated`, …) matter — don't silently drop them.
5. **Datum & unit heterogeneity.** Horizontal datums vary (mostly NAD83; some NAD27/older); units are US-customary (ft³/s, ft). Normalize explicitly; don't mix.
6. **HUC length varies** (HUC-8 vs HUC-12 by site) — align to a common level before HUC joins (§13).
7. **OGC API is young.** Build `0.59.3`; no total counts (`numberMatched: null`), cursor-only paging; some filter combinations behave differently than legacy. We pin the build version and cross-check against legacy until it sunsets.
8. **Rate limits are real.** Keyless = **1000 requests/hour**; exceed it and you get **HTTP 429** with `Retry-After` (~330 s). Get a free API key for any non-trivial pull (§7/§11).

**Bias/representativeness summary for the prep stage:** availability is non-random (managed rivers over-represented, small lakes under-represented); provisional recency is revisable; discharge is modeled; sensor series drift. All must surface in the "inspect & prepare" narrative.

---

## 6. Bulk-download vs. on-the-fly — the feasibility call

**Recommendation: API-first, per-AOI subset. Do NOT mirror NWIS.** Rationale (auditable):

- NWIS is **~1.9M sites** with sub-hourly histories for many; a full mirror is enormous and pointless for a HAB study that needs a bounded study area.
- The OGC API returns **one feature per observation** and gives **no total count** (`numberMatched: null`) — you **page via `next` cursor links**. A single site+parameter daily history is modest (e.g. 01646500 discharge ≈ 35k rows ≈ **~2 requests at `limit=20000`**, verified). CSV output (`f=csv`) is ~3× more compact than GeoJSON.
- **Chosen strategy (this repo):**
  1. **Enumerate** monitoring locations for the AOI (`monitoring-locations`, filters: HUC / bbox / state / county / site-type) — auth-free, cheap.
  2. **Catalog** each site (`time-series-metadata`) → plan **only series that exist** for the requested parameters (no empty pulls; also reports active vs stale).
  3. **Download** each planned series (`daily`/`continuous`) over the date window → tidy CSV, sha256, manifest.
  4. **Refresh** operationally by re-pulling a recent date window (or filtering on `last_modified`).

This honors "acquire only what you need, script it, cache it, regenerate from code," and keeps within the keyless rate budget for small AOIs (an API key removes the ceiling for large ones).

---

## 7. How to access it (verified 2026-07-01)

### 7.1 Base & discovery (no auth)
- **Base:** `https://api.waterdata.usgs.gov/ogcapi/v0` → `/collections` lists all collections; `/openapi` is the schema.
- **Service build version** is in the **`X-Build-Version`** response header (`0.59.3` today) — recorded per pull for provenance.

### 7.2 Data collections & verified filters
- **Sites:** `GET /collections/monitoring-locations/items` — filters verified working: `hydrologic_unit_code` (**prefix** match — HUC-8 returns its HUC-12 children), `bbox=minlon,minlat,maxlon,maxlat`, `state_code`, `county_code`, `site_type_code`, and the single-site id filter **`id`** (full `USGS-…`) or **`monitoring_location_number`** (bare, `01646500`). ⚠ `monitoring_location_id` is **not** a valid filter here (it 400s) — that's the data-collections' name (below). Confirm names via `…/monitoring-locations/queryables`.
- **Daily:** `GET /collections/daily/items?monitoring_location_id=…&parameter_code=…&statistic_id=…&datetime=START/END`. (Data collections filter by **site only** — no HUC/bbox.)
- **Continuous (real-time):** `GET /collections/continuous/items?monitoring_location_id=…&parameter_code=…&datetime=START/END`.
- **Catalog:** `GET /collections/time-series-metadata/items?monitoring_location_id=…` → per-series `parameter_code`, `statistic_id`, `computation_period_identifier` (`Daily`/`Points`/`Water Year`), `begin`/`end`, `last_modified`. Unlike the data collections, this one **also accepts AOI filters** — `hydrologic_unit_code`, `state_name`, `parameter_code` (verified keyed 2026-07-02) — so an AOI-wide catalog in one paged query is possible (efficient when you want (nearly) all sites in a HUC). Our `pull_nwis.py` catalogs **per enumerated site** instead, because the site set is already narrowed (enumeration + `--max-sites` guard) and per-site is uniform across all AOI types.
- **Latest value:** `latest-daily` / `latest-continuous` return the most recent value per series.
- **Formats:** `f=json` (GeoJSON) or `f=csv`. **Pagination:** `limit` up to **20000** (verified); follow `rel=next` links (no total count).

### 7.3 Authentication & rate limits
- **No auth required.** An **optional free API key** (from `https://api.waterdata.usgs.gov/signup/`) raises limits; pass it as the **`X-Api-Key`** header (this repo) or `api_key=` query param.
- **Keyless limit = `X-Ratelimit-Limit: 1000` requests/hour** (verified empirically). Exceeding it → **HTTP 429**, body `{"error":{"code":"OVER_RATE_LIMIT",…}}`, header `Retry-After` (~330 s). Keyed limits are higher (per-key; exact value not published — contact `wdfn@usgs.gov`).
- This repo reads `NWIS_API_KEY` (or `USGS_API_KEY`) from `data-sources/.env` (gitignored) or the environment; the key is sent as a header so it never lands in a URL/log/manifest. **No credentials are committed** — so a fresh clone has no key and must add its own (`resolve_api_key()` returns `None` and pulls fall back to keyless). In *this* working copy a key was configured on 2026-07-02, and the keyed 20-site AOI pull then ran cleanly in seconds where keyless throttled/stalled.
- ⚠ Our client (`make_nwis_session`) **retries only 5xx, not 429** — blindly retrying 429 both blocks on `Retry-After` and *burns more quota*; instead we raise a clear `RateLimitError`.

### 7.4 Legacy (⚠ decommissioned early 2027 — cross-check only)
- `https://waterservices.usgs.gov/nwis/{site,dv,iv}/` returning RDB/WaterML/JSON; `seriesCatalogOutput=true` gives the period-of-record catalog; `siteStatus=active` filters active sites. Used only by `nwis_api.legacy_*` for transition cross-checks.

### 7.5 Convenience libraries (documented, secondary)
- **R `dataRetrieval`** and **Python `dataretrieval`** have added `read_waterdata_*` functions targeting this OGC API. We use a thin in-repo client (reusing `_common/`) for full control/traceability, but these are the community-standard alternative and a good cross-check. **Not installed here by default** (add to `requirements.txt` if adopted).

---

## 8. Sources (all accessed 2026-07-01)

1. **USGS Water Data APIs (primary):** `https://api.waterdata.usgs.gov/` · collections `…/ogcapi/v0/collections` (cached: `reference/ogc_v0_collections.json`) · signup `…/signup/`.
2. **Legacy WaterServices + decommission notice:** `https://waterservices.usgs.gov/` (banner: "WaterServices will be decommissioned in early 2027").
3. **Provisional Data Statement + disclaimer:** `https://waterdata.usgs.gov/provisional-data-statement/`; verbatim text captured from a live DV response in `reference/provisional_and_disclaimer_verbatim.txt`.
4. **USGS copyright/credit (public domain):** `https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits`.
5. **Water Quality Portal (for the join):** `https://www.waterqualitydata.us/` — confirmed `USGS-01646500` resolves with `OrganizationIdentifier=USGS-MD`, `ProviderName=NWIS`, `HUCEightDigitCode=02070008`.
6. **EPA National Aquatic Resource Surveys / NLA:** `https://www.epa.gov/national-aquatic-resource-surveys` (spatial/HUC linkage target; not yet empirically onboarded).
7. **Empirical checks we ran (2026-07-01):** live OGC queries confirming collections, filter params (HUC/bbox/state/site-type/datetime), `limit=20000`, CSV output, cursor paging, the `USGS-<id>`↔WQP join, the 1000/hr keyless rate limit + 429/`Retry-After`, and the provisional/approved + qualifier encoding. Reproducible via `access/pull_nwis.py`.

---

## 9. Likely role in the SePRO HAB analysis

NWIS is the **in-situ half** of the satellite-meets-in-situ fusion. Concretely:

- **Primary — features (drivers).** Antecedent **streamflow / residence-time** (00060, 00065), **water temperature** (00010), and **in-situ nutrients / sonde chemistry** (99133, 00095, 00300, 00400, 63680) are physically-motivated bloom drivers. Used as **strictly past-dated** predictors of a future CyAN bloom state (guard against look-ahead leakage).
- **Secondary — in-situ cross-check / partial label.** Sonde series near a monitored waterbody help validate or contextualize the CyAN signal (which is a spectral proxy, not a measurement). Discrete cyano/toxin/chlorophyll ground truth comes from **WQP**, joined by `USGS-<id>`.
- **Context — watershed descriptors.** Drainage area, HUC, and site type frame each gage's hydrologic role.

**What it is *not*:** the satellite target (that's CyAN `CI_cyano`), nor a direct bloom/toxin measurement. Any driver→bloom or treatment implication is **correlational** unless a causal design supports it — state so explicitly.

---

## 10. Reproducibility & version pinning (project rules for this dataset)

- **Record the OGC service build version** (`X-Build-Version`, `0.59.3` today) on every pull, and each record's **`approval_status`** + **`last_modified`** — so a later value change (provisional→approved, or reprocessing) is detectable and attributable. (NWIS analogue of CyAN's `OBPG_version`.)
- **Cache & manifest:** every series is cached as a tidy CSV under `data/raw/{daily,continuous}/` and recorded in `manifest.jsonl` — **filename, sha256, bytes, service, site_id, parameter_code, statistic_id, n_rows, date_min/max, n_provisional/n_approved, last_modified_max, ogc_build_version, access timestamp**. Any figure/metric traces to exact bytes + query. Re-runs dedupe (only re-write a manifest line when sha changes).
- **Deterministic:** fixed AOI + parameter + date args; stable CSV column order → stable sha256; scripted access, no manual steps.
- **Tidy CSV = faithful normalization, not aggregation.** We convert the OGC JSON to columnar CSV **row-per-observation** with no averaging/binning — every measurement is preserved (§12).
- **Access date** for this documentation and all live checks: **2026-07-01**.

---

## 11. Access cost & scaling (empirical, 2026-07-01)

- **Rate budget:** keyless **1000 requests/hour**. The catalog-driven pull costs ≈ `1 (build) + 1..k (enumerate pages) + N_sites (catalog) + N_series (data)` requests. A HUC-8 with ~52 sites ⇒ ~55–110 requests — comfortably keyless. **National / multi-state ⇒ get an API key.**
- **Payload:** a single site+param daily history (~35k rows) ≈ **~2 requests at `limit=20000`**; CSV output keeps files small (a few MB per long series). RAM is never a concern at per-series granularity.
- **Refresh** is trivial: re-pull a recent date window per site (or filter on `last_modified`) — a few requests/site/update.

| Scope | Approach | ~Requests | Keyless OK? |
|---|---|---|---|
| A few named sites | `--sites …` | ~5–20 | ✅ |
| One HUC-8 (~50 sites) | `--huc ########` | ~55–110 | ✅ |
| A state | `--state ##` | 100s–1000s | ⚠ get an API key |
| Multi-state / national | — | ≫1000 | ❌ API key required; consider staged pulls |

---

## 12. Aggregation policy (project rule)

**Never spatially or temporally aggregate NWIS data — analysis *or* visualization — without explicit permission.** Practical consequences here:

- We store the **native per-observation** series (daily statistic or continuous sample) — **no** resampling/binning/averaging on ingest. The tidy CSV is a 1:1 normalization of the API records.
- NWIS's **daily statistics (mean/max/min)** are a **provider-side** computation intrinsic to the DV product — fine to *use* as-is; we simply don't add aggregation on top.
- If an analysis needs a coarser cadence or a spatial roll-up (e.g. HUC-mean), that is an **explicit, opt-in** step recorded in `DECISIONS-LOG.md`, not a silent default.

---

## 13. Geotagging & cross-dataset linkage (the strong suit)

Every monitoring location carries the keys to join NWIS to the rest of the palette:

- **↔ Water Quality Portal (WQP) — exact 1:1 join.** The OGC site `id` **is** the WQP `MonitoringLocationIdentifier`: `USGS-01646500`. Verified: WQP returns that site with `OrganizationIdentifier=USGS-MD`, `ProviderName=NWIS`, `HUCEightDigitCode=02070008`. So NWIS continuous/daily sensor data and WQP discrete lab chemistry **join on the site id with zero transformation** (`nwis_api.to_wqp_id` builds it from a bare number if needed).
- **↔ HUC / Watershed Boundary Dataset.** `hydrologic_unit_code` (HUC-8…HUC-12) links each site to a WBD polygon and to any HUC-indexed layer. The `hydrologic-unit-codes` reference collection (125,119 HUCs) provides names + hierarchy.
- **↔ EPA NARS / National Lakes Assessment — spatial join, not a shared key.** NARS uses its own **probabilistic-survey site IDs** and is **lake-based**, so there is *no common station identifier* with NWIS. Associate a NWIS gage to a NARS lake by **HUC-12 containment / proximity / same-waterbody** — a modeling choice, stated explicitly. *(Reasoned from the data model; to be confirmed empirically when `nars_nla` is onboarded.)*
- **↔ Administrative joins.** `state_code`/`county_code` (FIPS) link to Census/other FIPS-indexed data.

---

## 14. Restrictions / licensing (the short version)

- **U.S. Public Domain.** USGS-produced data are U.S. Government works — **no copyright, no license fee, no usage restriction**. USGS *requests* the credit line **"U.S. Geological Survey."** (The only copyright carve-outs are third-party photos/graphics — irrelevant to numeric water data.) Source: USGS Copyrights & Credits (§8).
- **Provisional disclaimer must ride along.** When redistributing or building products on recent data, carry the provisional caveat: data are provisional, **subject to revision**, and provided *"as is"* with **no warranty** and USGS/US-Gov **not liable** for damages from use (verbatim in `reference/provisional_and_disclaimer_verbatim.txt`). Caution against using provisional data for safety/decision-critical uses without noting the caveat.
- **No auth, but be a good citizen:** honor rate limits, use an API key at scale, set a descriptive User-Agent (our client does).
