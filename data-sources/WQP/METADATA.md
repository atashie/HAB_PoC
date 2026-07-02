# Water Quality Portal (WQP) — Dataset Metadata

**Dataset short name:** `wqp`
**Product this file describes:** WQP discrete water-quality **Stations, Results, Activities, Detection/Quantitation
Limits, and periodOfRecord Summaries**, served as **WQX-Outbound** records across TWO coexisting schemas:
**legacy WQX 2.2** (`/data/…`) and **WQX 3.0 beta** (`/wqx3/…`).
**Version / processing level documented:** WQX 2.2 (production) + WQX 3.0 (beta) as served on the dates below.
**Compiled:** 2026-07-01 · **Access date for all checks below:** 2026-07-01
**Compiled by:** Claude (Opus 4.8) with Arik Tashie, reviewed by Codex (GPT-5). Every quantitative claim traces
to a cited primary source or an empirical check we ran on 2026-07-01 (curl probes; scripts to be added under
`access/`). Ambiguities are flagged, not smoothed over. Facts confirmed by our own live probe (vs. only by doc)
are marked **[probe]**.

> **AI-shaped-judgment flag (per `../../CLAUDE.md`).** The characterization below was drafted by an LLM from
> primary sources + live probes and hardened against a structured Codex review (15 findings, all verifiable ones
> confirmed by probe — see `../DECISIONS-LOG.md` 2026-07-01 WQP entry). A human should still spot-check the
> reconciliation key (§10), the censoring logic (§4), and the leakage policy (§9) before they back any claim.

---

## 0. TL;DR for the modeler

| Question | Answer |
|---|---|
| What is it? | National aggregation of **discrete** (grab-sample) water-quality data from **USGS + EPA + 400+ agencies**; the in-situ chemistry/biology layer to fuse with the CyAN satellite signal. |
| Native form / format | Tabular **WQX-Outbound** records (CSV/TSV/xlsx/JSON/GeoJSON/XML). Point stations → activities → results. **Not** a grid. |
| Spatial resolution & extent | Irregular **point** monitoring locations, national (US + territories + some beyond). Each has lat/lon + datum; HUC8 (legacy) / **HUC8 + HUC12** (WQX3). |
| Temporal span, cadence, gaps | Century-scale historical → present, but **per-site, ad-hoc, wildly uneven**. Refresh: **NWIS every 24 h; WQX weekly (Thu evening)**. Many sites are **permanently stale** (one-off surveys). |
| The value in a record | One measured result: `CharacteristicName` + `ResultMeasureValue` + unit + fraction + method, with detection/qualifier/status metadata. |
| Encoding / how to read a value | `ResultMeasureValue` is a **string** (can be `"NA"`, blank, or numeric). Read *with* `ResultDetectionConditionText`, `MeasureQualifierCode`, `ResultStatusIdentifier`, and the **Detection/Quantitation Limit (DQL)** rows. |
| Nodata / fill / detection limit | **No single fill code.** Distinguish: numeric value · **non-detect/censored** (detection-condition text + DQL) · qualified · missing. `"NA"` string ≠ zero, ≠ non-detect by itself. **[probe]** |
| Access (search / download / auth) | **Public REST, no auth.** `…/data/{Station,Result,Activity,ResultDetectionQuantitationLimit,summary/monitoringLocation}/search` (legacy) and `…/wqx3/{Station,Result,…}/search` (beta). ⚠ **No `/wqx3/summary`** (404 **[probe]**). |
| Bulk or subset? (size estimate) | **Subset — never mirror.** Full portal ≈ hundreds of millions of results. Subset by **space × characteristic × time**. |
| Likely role | **Feature** (nutrients, temp, chl-a drivers) **and validation label** (chl-a, microcystin, cyano counts) for the CyAN-based HAB model. |

**Two headline traps, read before anything else:**
1. **The 2024-03-11 USGS split.** Legacy WQX 2.2 **does not contain USGS data added *or modified* after
   2024-03-11**; that data lives only in WQX 3.0. Do **not** treat legacy as a complete/stable USGS archive.
2. **Dual-schema double-counting.** WQX 3.0 is backward-compatible and re-serves old submissions, while WQX 2.2
   continues. A **blind union of both = duplicated records** → inflated density, corrupted labels, train/test
   leakage. We ingest both but **reconcile to one canonical de-duplicated record set** (§10).

---

## 1. What it is

The Water Quality Portal is a cooperative service of the **USGS**, the **EPA**, and the **National Water Quality
Monitoring Council (NWQMC)** that aggregates **discrete** water-quality data — physical, chemical, and biological
grab samples — from **over 400 state, federal, tribal, and local organizations** into one queryable store
delivered in the **WQX-Outbound** format. It is described by its operators as *"the premiere source of discrete
water-quality data in the United States and beyond"* ([WQP home](https://www.waterqualitydata.us/), 2026-07-01).

Two contributing systems feed it:
- **NWIS (USGS)** — *"current and historical water data from more than 1.5 million sites across the nation"*
  ([WQP Description](https://www.waterqualitydata.us/wqp_description/), 2026-07-01). Served under `ProviderName=NWIS`,
  site IDs like `USGS-04193500`, with a `USGSPCode` on each result.
- **WQX (EPA)** — submissions from *"states, tribes, watershed groups, other federal agencies, volunteer groups,
  and universities"* (ibid.). Served under `ProviderName=STORET`. **EPA's National Aquatic Resource Surveys /
  National Lakes Assessment submit here too**, as organization `NARS_WQX` (e.g. site `NARS_WQX-NGL_OH-10001`,
  Microcystin) — **[probe]**, so NARS ↔ WQP is a **shared key**, not merely a spatial join.
  *(NARS org-code linkage confirmed by probe, **not yet by primary doc** — verify via a `Codes/Organization`
  discovery step before hard-coding, per Codex #14.)*
  - ⚠ **Double-source caution (sibling datasets).** NARS is **also** onboarded standalone in `../EPA-NARS/`, and
    NWIS hydrology in `../NWIS/`. NARS records can therefore enter a fusion **twice** (via WQP `NARS_WQX` *and* via
    EPA-NARS). **Prefer `../EPA-NARS/` as canonical for NARS** (it carries the richer NHD/WBD keys —
    COMID/REACHCODE/HUC8); treat WQP `NARS_WQX` as a cross-check and **exclude `NARS_WQX` from WQP pulls that are
    merged with EPA-NARS**. WQP↔`../NWIS/` share the `USGS-<id>` key (WQP = discrete chemistry; NWIS = streamflow/gage).

It is a **living aggregation, not a curated product**: what exists is whatever contributors chose to submit, so
coverage, parameters, methods, units, and recency are **heterogeneous by design** (see §5). This is the single
most important fact for modeling with WQP.

## 2. Temporal coverage, cadence & gaps

| Aspect | Detail | Source |
|---|---|---|
| Span | Historical (some records >100 yr old) → present, **but per-site and highly uneven**. | portal data |
| Refresh — NWIS | *"NWIS (USGS) is updated every 24 hours."* | [User Guide](https://www.waterqualitydata.us/portal_userguide/) |
| Refresh — WQX | *"WQX (EPA) is updated weekly on Thursday evening."* | User Guide |
| **USGS 2024-03-11 split** | *"USGS data that was collected or analyzed after March 11, 2024, as well as any modification to existing data made after this date will not appear in the WQX2.2 profiles."* Fresh/updated USGS data → **WQX 3.0 only**. | [WQX3 blog](https://waterdata.usgs.gov/blog/wqx3/) |
| Provisional status | *"Results are initially coded with a result status of provisional. After review by a project hydrologist, the result status is usually changed to accepted."* … *"accepted status does not guarantee that results will never be updated."* | User Guide |
| Version churn | WQX 3.0 is in **beta**; *"After the beta user interface has been tested, WQX3.0 data will become the default output"* and *"WQX2.2 data profiles and web services will remain available for a period of time, then they will be deprecated."* No dates given. | WQX3 blog |

**Consequences we must handle:**
- **Freshness is provider-specific** — an operational HAB alert can silently lag for WQX (state) contributors
  (weekly) while USGS updates daily. Measure *actual* recency per run from submission/result dates; don't assume
  one portal cadence (Codex #12).
- **Permanent staleness is normal** — many stations are single-campaign (e.g. a NARS survey year). "No recent
  data" is often a property of the site, not an outage.
- **Revision churn** — a value can change between pulls (provisional→accepted, or post-2024 USGS reprocessing).
  Two pulls with identical query URLs are **not guaranteed byte-identical**. We pin every pull and run a
  **revision-delta check** (§10).

## 3. Spatial characteristics (geotagging & linkage)

- **Geometry:** irregular **points** (monitoring locations). No grid, no native raster.
- **Coordinates:** every station carries `LatitudeMeasure`/`LongitudeMeasure` **plus a datum**
  (`HorizontalCoordinateReferenceSystemDatumName`) and accuracy/collection-method/source-scale fields. WQX 3.0
  adds **standardized** lat/lon (`Location_LatitudeStandardized`) and a standardized datum. **[probe]**
  - ⚠ **Datum & frame pitfalls (Codex #7):** WQP **web-service spatial filters expect WGS84**; the UI documents
    NAD83 point/bbox entry. **Station** coordinates and **Activity** coordinates can differ (an activity may
    carry its own location). **Reproject explicitly**; store station vs activity coords separately; keep
    datum/accuracy/method; **prefer activity coordinates when present**; flag low-precision or withheld locations.
    Blindly using a station centroid can misassign a nearshore/offshore CyAN pixel.
- **Watershed identifiers (the link to hydrology):**
  - Legacy: `HUCEightDigitCode` (**HUC8**). **[probe]**
  - WQX 3.0: `Location_HUCEightDigitCode` **and `Location_HUCTwelveDigitCode` (HUC12)** — finer watershed. **[probe]**
  - The `huc` query parameter accepts one or more 8-digit HUCs (semicolon-delimited);
    [web-services doc](https://www.waterqualitydata.us/webservices_documentation/).
- **Linkage to USGS NWIS — trivial (shared key).** WQP **re-serves NWIS**: `MonitoringLocationIdentifier` is
  literally `USGS-<siteno>` (e.g. `USGS-04193500`, "Maumee River at Waterville OH"), `ProviderName=NWIS`, and each
  result has a `USGSPCode`. Joining WQP↔NWIS is an ID equality, not a spatial match. **[probe]**
- **Linkage to EPA NARS/NLA — direct (shared key).** NARS submits into WQP as org `NARS_WQX` (§1). **[probe]**
  Also spatially/HUC-joinable for programs that do not submit to WQP.
- **Linkage to CyAN (satellite):** **spatial** (point-in-pixel / nearest, ~300 m CyAN cells) **+ temporal**
  (as-of). This is the project's main **leakage surface** — see §9.

## 4. Encoding & quality flags — EXACT values (authoritative)

Delivered per the **WQX-Outbound schema**. There is **no single nodata code**; a value's meaning comes from
several columns read together. The legacy `resultPhysChem` profile has **63 columns** **[probe]**; the fields
that decide a value's meaning:

| Field | Meaning / trap |
|---|---|
| `ResultMeasureValue` | **String**, not numeric. Observed `"NA"` with an *empty* `ResultDetectionConditionText` **[probe]** — ambiguous (missing vs non-detect vs literal). Never coerce blanks/`"NA"` to `0`. |
| `ResultDetectionConditionText` | e.g. "Not Detected", "Present Below Quantification Limit". The primary **censoring** signal. |
| `ResultMeasure/MeasureUnitCode` | Units (`ug/L`, `mg/l`, …). Same characteristic appears in multiple units → must harmonize (§ below). |
| `ResultSampleFractionText` | Total / Dissolved / etc. **Changes what the number means** — a feature key, not cosmetic. |
| `MeasureQualifierCode` | Lab/field qualifiers. |
| `ResultStatusIdentifier` | provisional / accepted / … (§2). |
| `ResultValueTypeName`, `StatisticalBaseCode`, `*BasisText` | Actual vs estimated/calculated; mean/max; weight/time basis. |
| `USGSPCode` | USGS parameter code — the precise analyte key for NWIS records. |
| `ResultAnalyticalMethod/*`, `LaboratoryName` | Method/lab — needed for comparability. |

**Censored / non-detect handling (Codex #2 — a blocker).** *"There can be multiple Result Detection Quantitation
limits per result, and they can be linked to results retrieved using the 'narrow' result profile using
ResultIdentifier."* ([User Guide](https://www.waterqualitydata.us/portal_userguide/)). Therefore:
- The **`ResultDetectionQuantitationLimit`** profile is a **first-class pull**, not optional QA. Join to results
  via `ResultIdentifier` (through the `narrow` profile).
- Preserve raw value text, detection-condition, qualifier, DQL type/value/unit, and result status; **derive an
  explicit censoring state** (`detected` / `non_detect` / `below_quant` / `qualified` / `missing`).
- **No imputation** (½-DL substitution, drops, etc.) until an explicit, labeled modeling step. Treating non-detects
  as `0` biases nutrients/toxins and manufactures false "absence" labels.

**Analyte identity is composite (Codex #3, #10).** *"The nomenclature for WQX (EPA) and USGS characteristics are
not identical"* — e.g. EPA lists specific dissolved-oxygen characteristics while USGS files DO under "oxygen"
(User Guide). A `CharacteristicName` alone does **not** encode units, fraction, basis, method, or speciation.
Define an **analyte feature key** = characteristic (+ `USGSPCode` where present) + fraction + unit + method/
speciation + value-type/basis + media + depth, and only then build **explicit, human-reviewed harmonization
groups** (`reference/analyte-dictionary.md`). Discover the space via characteristic **groups + names + pCodes +
WQX domain/alias tables**, not names alone.

## 5. Known issues & limitations (the honest list)

- **Heterogeneity is the headline.** 400+ contributors → no guaranteed parameter panel per site; units, methods,
  fractions, and detection limits vary within the "same" characteristic.
- **Sampling bias.** Sites are placed for many programs' own reasons (impairment studies, compliance, surveys) —
  **not a random or gridded sample** of waterbodies. Any spatial/temporal model must treat presence as biased.
- **Dual-schema overlap** (§0 trap 2) → double-counting risk on a naive union.
- **The 2024-03-11 USGS split** (§2) → legacy is not a complete/stable USGS record.
- **Ambiguous nulls / censoring** (§4).
- **Coordinate/datum/precision variance** (§3).
- **Provisional & revisable values** (§2) → results are *"released on the condition that neither the USGS nor the
  United States Government may be held liable for any damages resulting from its authorized or unauthorized use"*
  and USGS data *"may include data that have not received Director's approval and as such are provisional and
  subject to revision"* (User Guide).
- **Non-water / non-relevant media** (groundwater, sediment, tissue, wastewater) coexist with surface water — must
  be filtered intentionally (§7 filters; Codex #15).
- **`"every column renamed"` is an over-generalization** (Codex #9): legacy↔WQX3 column names differ substantially
  (our Station probe showed a full rename **[probe]**), but treat **EPA's published WQX3 outbound schema + legacy
  crosswalk** as the source of truth and validate **per profile**, rather than assuming a blanket rule.

## 6. Bulk-download vs on-the-fly — the feasibility call

**Subset, do not mirror.** The full portal is on the order of **hundreds of millions of results**; mirroring is
neither necessary nor auditable for a PoC. The API is fast and reliable for **bounded** queries (spatial + a
characteristic list + a date window return in seconds; the count comes back in a response header, e.g.
`Total-Site-Count: 20` for Chlorophyll-a sites in Lucas County OH **[probe]**). Guidance from the
[web-services doc](https://www.waterqualitydata.us/webservices_documentation/): use `zip=yes` (*"compression often
greatly increases throughput"*), leave `sorted=no` (sorting *"increases response time significantly"* and is
disabled by default above 5M rows), and switch to **HTTP POST** for very long queries. Strategy: **discovery-first**
(§7.2) → predeclared inclusion rules (§10) → targeted Result + DQL pulls, all cached + manifested.

## 7. How to access it (verified 2026-07-01)

Base: `https://www.waterqualitydata.us`. **Public, no auth.** Two schema families coexist:

### 7.1 Endpoints & schemas
| Endpoint | Legacy (WQX 2.2) | WQX 3.0 beta | Notes |
|---|---|---|---|
| Stations | `/data/Station/search` | `/wqx3/Station/search` | Both **200**; WQX3 = 56 cols incl. HUC12 + standardized coords + `AlternateLocation_Identifier` crosswalks. **[probe]** |
| Results | `/data/Result/search` | `/wqx3/Result/search` | WQX3 `dataProfile` = `fullPhysChem` / `basicPhysChem` / `narrow` all **200**. **[probe]** Legacy `resultPhysChem` = 63 cols. |
| Activities | `/data/Activity/search` | `/wqx3/Activity/search` | Collection events. |
| Detection/Quant limits | `/data/ResultDetectionQuantitationLimit/search` | (via `narrow` + `ResultIdentifier`) | Censoring — first-class (§4). |
| **Summary** | `/data/summary/monitoringLocation/search` (`dataProfile=periodOfRecord`) | **❌ 404 — does not exist in WQX3** **[probe]** | Discovery backbone (§7.2). |

### 7.2 Discovery-first (the availability/recency step)
Because WQX3 has **no Summary service**, discovery is a **two-part** step (Codex #5):
1. **Broad discovery** via the **legacy** Summary service — per site × year × characteristic it returns
   `ActivityCount`, `ResultCount`, `LastResultSubmittedDate`, lat/lon, HUC8, media/site type (1,903 rows for
   Lucas County OH in one call **[probe]**). *Caveat: legacy Summary omits post-2024-03-11 USGS data.*
2. **Post-2024 USGS freshness** via targeted **WQX3 Station/Result** probes over the same scope.
Output: an availability + recency table that drives parameter selection.

### 7.3 Query parameters (filtering)
Spatial: `bBox`, `lat`/`long`/`within` (WGS84 decimal degrees + miles), `statecode` (`US:39`), `countycode`
(`US:39:095`), `huc` (8-digit, `;`-delimited), `siteid` (`USGS-04193500`). Also `characteristicName`,
`characteristicType`, `siteType`, `sampleMedia`, `startDateLo/Hi`, `providers`, `mimeType`, `zip`, `dataProfile`,
`sorted`, `pagesize`/`pagenumber`. **HAB media/site filters (Codex #15):** default to `sampleMedia=Water` and
lake/reservoir/stream/open-water site types; **report excluded counts** (no silent truncation).

### 7.4 Alternative / convenience access (secondary — cross-check only)
The USGS **`dataretrieval`** Python package (and R `dataRetrieval`) can query WQP; R `readNWISqw()` was retired and
NWIS discrete WQ folded into WQP/WQX ([dataRetrieval Status](https://water.code-pages.usgs.gov/dataretrieval/articles/Status.html)).
We use it **only for sampled cross-validation + version/status reporting**, never as a second canonical ingestion
path (Codex #13) — raw REST via `../_common/net.py` stays canonical.

### 7.5 Ancillary
EPA-published **WQX 3.0 outbound schema, profile definitions, and the WQX legacy crosswalk** (source of truth for
§4/§10 reconciliation) — [EPA WQP quick-reference](https://www.epa.gov/waterdata/water-quality-portal-quick-reference-guide);
Characteristic domain CSV (`cdx.epa.gov/wqx/download/DomainValues/Characteristic_CSV.zip`); USGS SRS/pCode
crosswalk (`waterqualitydata.us/public_srsnames/`). Preserve locally under `reference/`.

### 7.6 Verified API quirks (gotchas that cost real debugging time) — all **[probe]** 2026-07-01
- **Date params are `MM-DD-YYYY`, not ISO.** `startDateLo=2024-03-12` → **HTTP 400**;
  `startDateLo=03-12-2024` → 200. We keep ISO internally and convert in `build_query_url`.
- **An unrecognized `characteristicName` 400s the WHOLE query.** `"Microcystins, total"` → 400,
  `"Microcystin"` → 200. One bad name poisons the request → the pull code **must validate names
  against the Characteristic domain** before querying (Codex #10).
- **Count-header asymmetry.** Legacy returns `Total-Site-Count`/`Total-Activity-Count`/
  `Total-Result-Count` headers (counts for free); **WQX3 returns none** → WQX3 counts require
  fetching + counting rows. `discover_wqp.py` handles both.
- **Empirical proof of the split.** Post-`2024-03-12` USGS (`providers=NWIS`) Results in Lucas
  County OH: **legacy = 0, WQX3 = 7,528** (`outputs/discovery_report.md`). Operational USGS use
  therefore *requires* WQX3.
- **⚠ Large WQX3 pulls truncate silently.** WQP streams big (cold) responses and can close the
  connection with a **clean but premature EOF** → the client caches a **partial CSV as if complete**
  (observed: a county WQX3 pull returned 1,828/7,320 rows; warm re-requests returned the full 7,320).
  **Mitigation** (`fetch_results_verified` in `access/wqp_api.py`): verify record counts —
  legacy must **equal** its free `Total-Result-Count` header; WQX3 must be **≥ the legacy count**
  for the same query (WQX3 ⊇ shared history) — and **retry** on a short read. Caught only because the
  `dataretrieval` cross-check disagreed (legacy matched exactly: 119 sites / 7,163 results).

## 8. Sources (all accessed 2026-07-01)
1. **WQP home** — https://www.waterqualitydata.us/ · cache: `reference/PRIMARY-SOURCES.md`.
2. **Web-services documentation** — https://www.waterqualitydata.us/webservices_documentation/
3. **WQP User Guide** — https://www.waterqualitydata.us/portal_userguide/ (cadence, provisional/accepted, DQL, naming, profiles, citation, disclaimer).
4. **WQP Description** — https://www.waterqualitydata.us/wqp_description/ (source systems, 1.5M NWIS sites).
5. **USGS "WQX3.0 Data Now Available" blog** — https://waterdata.usgs.gov/blog/wqx3/ (2024-03-11 split; beta→default; deprecation direction).
6. **USGS dataRetrieval Status** — https://water.code-pages.usgs.gov/dataretrieval/articles/Status.html (readNWISqw retired; WQX3 options).
7. **EPA WQP quick-reference / WQX3 schema + crosswalk** — https://www.epa.gov/waterdata/water-quality-portal-quick-reference-guide
8. **Live REST probes (2026-07-01)** — Station/Result/Summary/DQL on `/data/` and `/wqx3/`; the `/wqx3/summary` 404;
   the NARS_WQX Microcystin rows; count headers. Reproducible via `access/` (to be added).
9. **Citation to reproduce (required):** *National Water Quality Monitoring Council, YYYY, Water Quality Portal,
   accessed mm, dd, yyyy, <query URL>, https://doi.org/10.5066/P9QRKUVJ.*

## 9. Likely role in the SePRO HAB analysis

- **Feature source:** nutrients (total P, orthophosphate, N species), water temperature, DO, pH, turbidity, Secchi
  — candidate drivers/covariates for CyAN-based HAB risk.
- **Validation label source:** in-situ **chlorophyll-a, microcystin/cyanotoxins, phyto/cyano cell counts** — the
  ground truth to check the satellite CI against.
- **What it is NOT:** not a complete or unbiased census of any waterbody; presence of a sample is **biased** by
  program design (§5). **Correlation ≠ causation** — a nutrient↔bloom association in WQP is not a treatment effect.
- **Leakage policy for the CyAN join (Codex #4 — the biggest leakage surface):**
  - **As-of joins only** — for a prediction timestamp, use **no in-situ or satellite data from the future**.
  - **Blocked splits** — spatial by waterbody/site/HUC, temporal by season/year; **never** a random shuffle on
    autocorrelated points, **never** same-station rows split across train/test.
  - Keep **native sample timestamps + CyAN acquisition timestamps** on every derived row; **report sensitivity to
    the join window**. Post-event toxin results must not inform a pre-event prediction.

## 10. Reproducibility & version pinning (rules for this dataset)

- **Canonical reconciliation key (Codex #1 — the anti-double-count rule).** Ingest legacy + WQX3, then reduce to
  **one** record per real observation:
  - Primary key = `schema` + `OrganizationIdentifier` + `MonitoringLocationIdentifier` + `ActivityIdentifier` +
    `ResultIdentifier` (when present).
  - Fallback content hash over: activity date/time · characteristic/observed-property · fraction · unit · method ·
    value · detection-condition · depth.
  - **Preference:** WQX3 for USGS records (full + freshest); a single schema (WQX3-only *or* legacy-only) for each
    non-USGS record **unless overlap tests prove no duplication**. Log kept-vs-dropped counts (no silent drop).
- **Revision-delta check.** Record for every pull: access date, exact query URL/body, response headers,
  source profile/schema, `ResultStatusIdentifier`, and content **sha256** (via `../_common/net.py` manifest).
  On re-pull, diff canonical keys + changed values → `outputs/revision_report.md`. Two identical URLs may return
  different bytes (provisional→accepted; USGS reprocessing) — this makes that visible, not silent.
- **Predeclared inclusion rules (Codex #8 — anti result-shopping).** *Before* selecting features from the
  discovery table, freeze objective thresholds in `reference/inclusion-rules.md`: min years, min samples/season,
  max staleness, required fields, allowed media/site types, and what a valid label requires (toxin/chl-a/cell
  count). Feature selection must not become outcome-driven.
- **Schema handling.** Validate columns **per profile** against EPA's published WQX3 outbound schema + legacy
  crosswalk (`reference/schema_crosswalk.csv`); do not assume a blanket rename.
- **Determinism.** Scripted access only (`access/`), cached + sha256-manifested, fixed query params, pinned deps
  (`../requirements.txt`). `data/` is gitignored and **regenerates from checked-in code**.
- **dataRetrieval** is a **cross-check**, not a source of record (§7.4).
