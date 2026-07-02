# EPA National Aquatic Resource Surveys — National Lakes Assessment (NLA) — Dataset Metadata

**Dataset short name:** `nars_nla`
**Product this file describes:** EPA NARS **National Lakes Assessment (NLA)** in-situ lake
survey — site information, water chemistry (incl. chlorophyll-a), and algal toxins
(microcystin, cylindrospermopsin). Worked example = **NLA 2022**.
**Version / processing level documented:** NLA 2022 public data files as published on the
NARS data page (files dated 2024-04 → 2025-01; each record carries a `PUBLICATION_DATE`).
**Compiled:** 2026-07-01 · **Access date for all checks below:** 2026-07-01
**Compiled by:** HAB PoC data-sources work. Every quantitative claim traces to a cited EPA
primary source (URL + access date) **or** to an empirical check we ran (script + the
regenerable `outputs/qa_report.md`). Ambiguities are flagged, not smoothed over. Content
shaped with LLM assistance was verified against the downloaded bytes (see §14).

---

## 0. TL;DR for the modeler

| Question | Answer |
|---|---|
| What is it? | EPA's **probability-based national survey of U.S. lakes** — standardized in-situ chemistry, chlorophyll-a, 2 cyanotoxins, biology, physical habitat, and rich watershed/geospatial metadata per lake. |
| Native form / format | Flat **CSV** files (one per indicator) + companion `.txt` data-dictionary; spatial layers as shapefile `.zip`. |
| Spatial resolution & extent | **Point/polygon per lake**, conterminous US (48 states) + some territories. ~1,225 sampled lake-visits in 2022; lake polygons available separately. |
| Temporal span, cadence, gaps | **5-year cycles: 2007, 2012, 2017, 2022** (next ≈2027). One index visit per lake per cycle (subset revisited); **multi-year gaps** — NOT a time series. |
| The value in a cell/record | A lab/field **measurement** for one analyte at one lake-visit (e.g. `MICX RESULT = 0.19 ug/L`), or a site descriptor (e.g. `COMID`, `HUC8`, `LAT_DD83`). |
| Encoding / how to read a value | Long toxin file: `ANALYTE`∈{MICX, CYLSPER}, `RESULT`+`RESULT_UNITS`. Wide chem file: `<ANALYTE>_RESULT` columns (CHLA, NTL, PTL, …). Every result has `MDL`, `RL`, `NARS_FLAG`, `QA_FLAG`. |
| Nodata / fill / detection limit | Missing = blank. **Non-detect is a MEASURED result**, flagged `NARS_FLAG=ND` with an `MDL` — left-censored, **not** missing and **not** zero. |
| Access (search / download / auth) | **No API.** Static CSVs at stable `epa.gov` URLs (+ an interactive Shiny download tool). **No authentication.** |
| Bulk or subset? (with size estimate) | **Bulk-download & mirror locally.** Tiny: NLA 2022 = 22 CSVs ≈ **33 MB** (+ report zip 71 MB, lake polygons 23 MB, basins 41 MB). |
| Likely role (target / feature / mask / context) | **In-situ feature + label-validation + context** — pairs with CyAN (satellite) and WQP/NWIS via `COMID`/`HUC8`/lat-lon. See §9, §11. |

---

## 1. What it is

The **National Aquatic Resource Surveys (NARS)** are EPA's family of statistical, probability-based
surveys of the condition of the nation's waters — Lakes (**NLA**), Rivers & Streams (NRSA),
Coastal (NCCA), and Wetlands (NWCA). This dataset documents the **National Lakes Assessment
(NLA)**: a nationally and regionally representative survey of lake and reservoir condition run on a
**5-year cycle** (2007, 2012, 2017, 2022). Each sampled lake is visited once during a summer index
period (a random subset is revisited for QA), and a **standardized** set of indicators is measured
the same way everywhere: water chemistry (nutrients, ions, carbon, clarity), **chlorophyll-a**, two
**cyanotoxins** (microcystin, cylindrospermopsin), phytoplankton/zooplankton, benthic
macroinvertebrates, physical habitat, and a rich block of per-lake geospatial/watershed descriptors.

The design goal is **population inference**: because sites are drawn by a probability design, weighted
results extrapolate to the full population of U.S. lakes (NLA 2022: **981 probability lakes
representing an estimated 268,020 lakes**, margin of error ≈ ±5% at 95% confidence — EPA *NLA 2022
Key Findings*). It is a **survey**, not a monitoring network: it answers "what fraction of U.S. lakes
are in poor condition / have detectable toxin," not "what is happening in lake X this week."

Maturity: four completed cycles, peer-reviewed methods, full field/lab manuals and technical support
documents published. It is an authoritative national baseline; at least one EPA effort has fused CyAN
satellite imagery with NLA to flag at-risk lakes (Research `FED-041` — a conference-presentation
record, no full text/validation metrics available, so treat as *precedent that it has been done*, not
as a benchmarked result).

---

## 2. Temporal coverage, cadence & gaps

| Cycle | Fieldwork | Data published | Notes |
|---|---|---|---|
| NLA 2007 | 2007 | ~2010 | First cycle; uses `SITE_ID`+`VISIT_NO` keys (no `UID`). |
| NLA 2012 | 2012 | ~2016 | Adds algal toxins, atrazine. |
| NLA 2017 | 2017 | ~2021 | |
| NLA 2022 | 2022 | 2024-04 → 2025-01 (incremental) | The worked example here. Next cycle ≈ **2027**. |

- **Cadence: one summer index visit per lake, every 5 years.** There are **multi-year gaps** between
  cycles and **no within-year time series**. Treating NLA as temporally dense would be wrong.
- **Publication is incremental and lagged.** NLA 2022 fieldwork was 2022; core files posted 2024-04/08;
  **phytoplankton counts landed 2025-01** (~2.5 yr later). Files carry a `PUBLICATION_DATE`.
- **Older cycles are effectively static/final** but can still receive late indicator files or a
  re-publish (note the `_0`/`_1` suffixes and mixed date folders). → We **pin exact URLs + sha256**
  and run a drift check (§7.1) so any change is *detected*, never silently absorbed.
- **Cross-cycle comparability is real work:** frame membership (`FRAME07/12/17/22`), design weights,
  and some indicators change between cycles. Do not assume columns are identical across years.

---

## 3. Spatial characteristics

- **Unit = the lake.** Each record is a lake (point at a coordinate; polygon available separately).
  There is no raster grid. "Resolution" = the lake itself; the survey is a **sample**, not a census.
- **Extent:** conterminous US (48 states); `PSTL_CODE` also allows AS/GU/MP/PR/VI. Empirically the
  2022 lat/lon spans **24.6–49.0 °N, −124.6 to −67.4 °W** (`qa_report.md` §4) — CONUS, no stray points.
- **Coordinates (verified from the file):**
  - `LAT_DD83` / `LON_DD83` — **NAD83** decimal degrees, the lake **centroid** from the NHD sample
    frame (100% populated).
  - `INDEX_LAT_DD` / `INDEX_LON_DD` — the **actual sampled index point** (decimal degrees), populated
    only for sampled sites (~31.6% of the frame file). **Use these for satellite/in-situ matchups.**
  - `XCOORD` / `YCOORD` — US Contiguous Albers Equal Area Conic (AK/HI use their own Albers).
- **Lake polygons + watershed basins** ship as separate shapefiles (`nla2022_lakes.zip`,
  `nla2022_basins.zip`) — enabling **polygon-based CyAN pixel extraction** instead of a single point.
- **Morphometry** per lake: `AREA_HA`, `PERIM_KM`, `ELEVATION`, `LAKE_ORGN` (man-made/natural),
  `AREA_CAT6` (size class).

---

## 4. Encoding & quality flags — EXACT values (authoritative)

**Two file shapes:**
- **Long** (algal toxins): one row per (lake-visit × analyte). `ANALYTE`∈{`MICX`=microcystin,
  `CYLSPER`=cylindrospermopsin}; value in `RESULT` (+ `RESULT_UNITS`, typically `ug/L`).
- **Wide** (water chemistry): one row per lake-visit; each analyte expands to
  `<A>_RESULT`, `<A>_UNITS` (or `<A>_RESULT_UNITS`), `<A>_MDL`, `<A>_RL`, `<A>_NARS_FLAG`,
  `<A>_QA_FLAG`, `<A>_HOLDING_TIME`, `<A>_DATE_ANALYZED`, `<A>_LAB_SAMPLE_ID`, `<A>_DILUTION_FACTOR`.
  HAB-relevant analytes present: **`CHLA`** (chlorophyll-a), **`NTL`** (total N), **`PTL`** (total P),
  `NTL_DISS`, `PTL_DISS`, `NITRATE_N`, `NITRATE_NITRITE_N`, `NITRITE_N`, `AMMONIA_N`, `DOC`, `TURB`,
  `COND`, `PH`, `ANC`, `COLOR`, `SILICA`, and major ions.

**Values & flags (exact):**
- `RESULT` — the measured value. `RESULT_UNITS`/`<A>_UNITS` gives the unit **per row** — read it, don't
  assume (e.g. `NTL` appears as `mg/L` *and* `mg N/L`; `COND` as `uS/cm` and `uS/cm AT 25 C`).
- `MDL` — method detection limit; `RL` — laboratory reporting limit.
- **`NARS_FLAG` (authoritative):** `ND` = **Non-detect (measured below detection)**, `L` = Estimated
  (below RL but above MDL), `Q` = Quality-related issue, `S` = Shipping-time exceedance,
  `H` = Holding-time exceedance, `NR` = No lab result. Flags can **combine** (e.g. `ND,Q`, `H,ND`).
- `QA_FLAG` — raw laboratory QA flag (not necessarily mapped to `NARS_FLAG`).
- **Missing vs non-detect (critical):** a blank `RESULT` = *not measured / missing*. `NARS_FLAG=ND`
  = *measured, below detection* — **left-censored data**, not missing, not zero. Our QA counts these
  separately and never coerces `ND` to 0/NaN.

**Identifiers & how to join:**
- **NLA 2022 (current):** join child files to `siteinfo` on **`UID`** (unique per site-visit).
- **NLA 2007 & older:** use **`SITE_ID` + `VISIT_NO`** (no `UID`).
- `UNIQUE_ID` (form `NLA_ss_nnnnn`) is a **cross-cycle, location-based lake ID** — the key for
  tracking the same physical lake across 2007/2012/2017/2022 (see the "NARS Site Id Unique ID
  Crosswalk" xlsx on the data page). `SITE_ID` (form `NLA22_MM-xxxxx`) is per-cycle.

---

## 5. Known issues & limitations (the honest list)

- **It's a probability survey, not a monitoring feed.** One summer visit per lake per 5-year cycle;
  no sub-seasonal dynamics. A bloom that formed the week after sampling is invisible.
- **EPA states NLA is not designed for site-specific/local management inference** — it is built for
  national/regional statistical estimation. Using a single lake's row as ground truth for that lake is
  outside the survey's design intent (though the *measurement itself* at that lake-visit is real).
- **Only 2 cyanotoxins** (microcystin, cylindrospermopsin). No anatoxins/saxitoxins; toxin production
  is class-specific and variable. Chlorophyll/abundance proxies **over-predict** toxin risk (a
  well-replicated finding across NLA cycles).
- **The raw data file ≠ the published sample.** The 2022 site file holds **3,880 rows / 3,784 lakes**
  including oversample, NES-legacy, and revisit sites — **not** just the **981** probability lakes.
  Verified composition (2026-07-01): **981** core probability sites (`WGT_TP_CORE_NLA > 0`; their
  weights sum to **268,018**, i.e. the represented lake population), **2,762** oversample-panel sites
  (`PANEL_USE` ~ `Over`), **153** NES-legacy (`WGT_TP_NES > 0`), and **1,691** `NonTarget` sites
  (`TNT_CAT`, drawn but dry / not-a-lake / inaccessible). **National/regional percentages require the
  probability filter + survey weights** (`WGT_TP_CORE_NLA`, `WGT_TP_EXT_NLA`). The metadata literally
  says **`WGT_DSGN` "DO NOT USE FOR POPULATION ESTIMATION!"**. (See `qa_report.md` §3.)
- **`NITRATE_N` is sparsely populated (~63%)** because many labs report combined
  `NITRATE_NITRITE_N` instead — use the combined field where nitrate alone is blank.
- **Units vary within a column** — always read the per-row unit field.
- **Extreme-but-real values are retained** (e.g. `PTL` to 4,130 ug/L, `TURB` to 722 NTU in
  hypereutrophic lakes) — do not clip blindly.
- **Cross-cycle column/weight drift** (see §2). Harmonization across years is a deliberate task.
- **Correlation ≠ causation.** Cross-sectional nutrient/clarity↔toxin associations here cannot
  establish drivers on their own.

---

## 6. Bulk-download vs on-the-fly — the feasibility call

- **There is no operational REST API.** Access is (a) static flat files at stable `epa.gov` URLs, and
  (b) an interactive **R-Shiny "NARS Data Download Tool"** (browser form; not machine-callable).
- **The archive is tiny.** NLA 2022 = **22 CSVs ≈ 33 MB** (report zip 71 MB; lake polygons 23 MB;
  basins 41 MB — HEAD-verified 2026-07-01). All four NLA cycles together are a few hundred MB at most.
- **Decision: mirror the flat files locally and work entirely offline/local.** This is the opposite of
  CyAN (hundreds of GB–TB → subset). Here, bulk is trivial and there is no API to lean on operationally,
  so we cache the CSVs with sha256 and never re-fetch unless drift is detected. See `access/`.

---

## 7. How to access it (verified 2026-07-01)

### 7.1 Enumerate / discover (no auth)
The canonical listing is the HTML **[Data from the NARS](https://www.epa.gov/national-aquatic-resource-surveys/data-national-aquatic-resource-surveys)**
page. `access/nars_catalog.py` holds a **pinned, verified manifest** of NLA file URLs and a
`discover()`/`reconcile()` pair that parses the live page and **diffs it against the pin** to catch any
added/renamed/re-published file (run `python pull_nars.py --check-drift`).

### 7.2 Download (no auth)
Direct `GET` of the pinned `https://www.epa.gov/system/files/other-files/<yyyy-mm>/<file>` URLs.
`access/pull_nars.py` downloads selected indicators for a cycle, caches them (skip-if-present),
and writes a JSONL **manifest** (url, bytes, sha256, indicator, access time). No credentials.

### 7.3 Alternative/convenience access (documented, secondary)
- **NARS Data Download Tool** (interactive Shiny): https://rconnect-public.epa.gov/nars-data-download/
  — select survey → year → indicator → state(s) → export CSV/XLSX. Good for humans; not for pipelines.
- **NLA 2022 "all data" archive zip** (as used for the report):
  `https://www.epa.gov/system/files/other-files/2024-08/data-files-for-nla-2022-report.zip` (~71 MB).
- **data.gov** catalog entries mirror the same files with dataset-level metadata.

### 7.4 Ancillary (grids/shapefiles/crosswalks)
- Lake polygons: `nla2022_lakes.zip`; watershed basins: `nla2022_basins.zip`.
- **NARS Site Id Unique ID Crosswalk (xlsx)** on the data page — maps `SITE_ID`↔`UNIQUE_ID` across
  cycles/surveys.
- Underlying hydrography: NHDPlus V2 (keys `COMID`, `REACHCODE`, `PERM_ID`), WBD HUCs, Omernik
  ecoregions — all referenced by columns in `siteinfo` (§11).

---

## 8. Sources (all accessed 2026-07-01)

1. **Data from the NARS** (file listing + citation guidance) —
   https://www.epa.gov/national-aquatic-resource-surveys/data-national-aquatic-resource-surveys
2. **What data are available to download** —
   https://www.epa.gov/national-aquatic-resource-surveys/what-data-are-available-download-national-aquatic-resource
3. **Frequent Questions about NARS Data** (UID vs SITE_ID/VISIT_NO; site info location fields) —
   https://www.epa.gov/national-aquatic-resource-surveys/frequent-questions-about-data-national-aquatic-resource-surveys
4. **NLA 2022 Reports and Data** —
   https://www.epa.gov/national-aquatic-resource-surveys/reports-and-data-national-lakes-assessment-2022
5. **NLA 2022 Key Findings** (981 lakes → 268,020; ±5%; toxin findings) —
   https://www.epa.gov/national-aquatic-resource-surveys/national-lakes-assessment-2022-key-findings
6. **EPA disclaimers / public-domain & no-warranty** —
   https://www.epa.gov/web-policies-and-procedures/epa-disclaimers
7. **NARS Data Download Tool** (interactive) — https://rconnect-public.epa.gov/nars-data-download/
8. **Preserved primary docs:** field dictionaries in `reference/` (`nla22_siteinfo.txt`,
   `nla22_algaltoxins.txt`, `nla22_waterchem_wide.txt`).
9. **Empirical checks we ran** (reproducible): `access/pull_nars.py` → `qaqc/qa_nars.py` →
   `outputs/qa_report.md` + `qa_summary.json`; `viz/viz_nars.py` → `outputs/*`.
10. **Prior literature review** (this repo): `../../Research/in-situ-and-weather-data/README.md`
    (NLA design, biases, cyanotoxin findings; source keys ACAD-034, FED-027, FED-028, FED-078).

---

## 9. Likely role in the SePRO HAB analysis

- **In-situ feature / covariate:** per-lake nutrients (`NTL`, `PTL`), `CHLA`, clarity (secchi/`TURB`),
  and watershed/landscape metrics as candidate drivers or context for a lake's HAB susceptibility.
- **Label / validation of the satellite signal:** `MICX`/`CYLSPER` and `CHLA` at a known lake+date are
  independent ground checks for CyAN's cyanobacteria index at the same lake — a genuine
  remote-sensing ↔ in-situ **matchup** opportunity (the brief's core ask).
- **Context / stratification:** ecoregion, lake origin, size, HUC — to segment models and report by
  region honestly.
- **What it is NOT:** not a time series, not a site-level early-warning feed, not a full toxin panel,
  and not (in raw form) a national estimate. Any "% of lakes …" statement needs the survey weights.
- **Correlation ≠ causation** must accompany every driver/treatment implication drawn from it.

---

## 10. Reproducibility & version pinning (rules for this dataset)

- **Pin exact file URLs** in `access/nars_catalog.py` (verified 2026-07-01); **sha256 every download**
  in the manifest; re-runs are cache-hits unless bytes change.
- **Record `PUBLICATION_DATE`** (it's a column) as the dataset's provenance stamp; note the file's
  date-folder (`2024-08` etc.) in citations.
- **Run `--check-drift`** before trusting a re-pull: it diffs the live page vs the pin and reports
  new/removed files (EPA publishes incrementally).
- **Cite** per EPA's recommended form: *U.S. EPA. [pub year]. National Aquatic Resource Surveys.
  National Lakes Assessment [year] (data and metadata files). https://www.epa.gov/national-aquatic-resource-surveys/data-national-aquatic-resource-surveys. Date accessed: 2026-07-01.*
- **Deterministic:** fixed URL manifest, pinned deps (`../requirements.txt`), scripted access — no
  manual clicks; `data/` regenerates from `access/`.

---

## 11. Geotagging & linkage design — the standout (DESIGN NOW, JOIN LATER)

**Why this matters:** NLA's `siteinfo` is geotagged far beyond lat/lon. It carries the full **NHD /
Watershed-Boundary hydrography key suite**, which is the same backbone USGS NWIS and the Water Quality
Portal (WQP) sit on — so NLA lakes can be bridged to streamflow, upstream chemistry, and watershed
covariates, and to CyAN pixels. **We document the join keys and method now; we implement/validate the
actual join when we build the fusion analysis.**

**Keys available (per-lake, % populated from `qa_report.md` §4):**

| Key | What it links to | Populated |
|---|---|---|
| `LAT_DD83`/`LON_DD83` (NAD83, centroid) | anything spatial; CyAN pixel by point | 100% |
| `INDEX_LAT_DD`/`INDEX_LON_DD` (sampled point) | **preferred for matchups** | sampled sites only |
| `COMID` | **NHDPlus V2** catchment/flowline; **USGS NLDI**; EPA **LakeCat** | 100% |
| `REACHCODE`, `PERM_ID` | NHD reach / National Map permanent id | 100% / 91% |
| `GNIS_ID`, `GNIS_NAME` | USGS place name; match to WQP lake monitoring-location names | 100% |
| `HUC2`, `HUC8` (+ names) | Watershed Boundary Dataset units | 100% |
| Omernik `US_L3/L4`, CEC `NA_L1/L2`, NARS `AG_ECO3/9`, `FEOW_ID` | ecoregion stratification | 100% |

**Recommended linkage recipes (to build later):**
- **NLA → USGS NWIS / WQP:** feed `COMID` to the **USGS NLDI** (`/linked-data/comid/<COMID>/…`) to
  enumerate upstream/downstream NWIS gages and WQP sites on the same NHD network; or match by shared
  `HUC8`; or spatial buffer on `INDEX_LAT/LON`; or `GNIS`/name match to WQP lake sites.
- **NLA → EPA LakeCat:** direct `COMID` join for hundreds of pre-computed watershed metrics
  (land cover, soils, roads, dams) — a ready-made feature block.
- **NLA → CyAN:** point-sample the CI raster at `INDEX_LAT/LON`, **or** (better) zonal-extract over the
  `nla2022_lakes.zip` polygon for the lake — native resolution, no aggregation across lakes.

**Honest limits of the linkage (document with it):**
- **NLA ships no direct WQP/NWIS station-ID crosswalk** — linkage is *constructed and must be
  validated*, not looked up.
- **NLA lakes are polygons; NWIS is mostly stream gages** on flowlines → linkage is **watershed /
  catchment-based, not identity**. A "linked" gage measures a feeder/outlet stream, not the lake.
- Datum is **NAD83**; reconcile with WGS84/other sources before joining on coordinates.
- Timing mismatch: an NLA summer index visit rarely coincides with a WQP/NWIS observation or a
  cloud-free CyAN pixel on the same date — matchups need a tolerance window, which is its own analysis.

---

## 12. Restrictions / license (the answer to "can we use it")

- **U.S. public domain by default.** Per EPA's disclaimers: EPA-produced (geospatial) data "is by
  default in the public domain and is not subject to domestic copyright protection under 17 U.S.C.
  § 105." Free to use, redistribute, and build a **commercial** product on.
- **Two soft obligations, not restrictions:** (1) **attribution** — use EPA's recommended citation
  (§10); (2) carry the **no-warranty disclaimer** — EPA "makes [no] warranty … for the accuracy,
  completeness, or usefulness" and assumes no liability.
- **The real constraint is fitness-for-use,** not licensing: the probability-survey design limits (§5),
  the 2-toxin scope, and the not-for-site-specific-inference caveat.

---

## 13. File inventory (NLA 2022 — the pinned manifest)

The authoritative machine-readable list is `access/nars_catalog.py::PINNED[2022]`. Core HAB indicators
pulled by default (`DEFAULT_INDICATORS`): **siteinfo, waterchem, algaltoxins, secchi, lakes_shp**.
Full set (`--indicators all`) also includes profile, phab, landscape, atrazine, phytoplankton,
zooplankton, benthic, enterococci, condition, popest, sample_grid, basins_shp. Empirically confirmed
2026-07-01: 22 CSVs ≈ 33 MB; `--check-drift` reports **clean** (25 pinned files match the live page).

Key files & what they hold (verified by download + `qa_report.md`):
- `nla22_siteinfo.csv` (86 cols, 3,880 rows) — the join hub: identifiers, coordinates, `COMID`/`HUC8`/
  ecoregions, morphometry, **survey weights**.
- `nla22_waterchem_wide.csv` (220 cols, 1,225 rows) — `CHLA`, `NTL`, `PTL`, dissolved N/P, nitrate,
  ammonia, DOC, turbidity, pH, conductivity, ANC, major ions — each with MDL/RL/flags.
- `nla22_algaltoxins.csv` (24 cols, 2,450 rows = 1,225 lakes × {MICX, CYLSPER}) — cyanotoxins with
  detect/non-detect flags. Empirical (unweighted, raw): microcystin detected at **49%** of sampled
  lakes, cylindrospermopsin at **9.5%**, **28 lakes (2.3%) ≥ 8 ug/L** microcystin — consistent with
  EPA's weighted ~50% / ~12% / ~2% headline figures.
- `nla22_secchi.csv` — water clarity. `nla2022_lakes.zip` — lake polygons for CyAN extraction.

---

## 14. AI-assisted judgment flag

This characterization, the acquisition/QA/viz code, and the linkage design were drafted with LLM
assistance and then **verified against the downloaded bytes**: column names, detection rates, geotag
completeness, and file sizes are all reproduced by `qaqc/qa_nars.py` / HEAD checks, not asserted from
memory. Numbers here that a human should spot-check are exactly those in `outputs/qa_report.md` (which
regenerates from source). Where EPA's own pages were ambiguous (e.g. licensing not stated on the data
page), we traced to the authoritative EPA disclaimers page rather than infer.
