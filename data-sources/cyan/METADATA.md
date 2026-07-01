# EPA/NASA CyAN — Cyanobacteria Index (CI_cyano) — Dataset Metadata

**Dataset short name:** CyAN (Cyanobacteria Assessment Network) satellite cyanobacteria index
**Product this file describes:** `CI_cyano` Level-3 mapped (L3m) GeoTIFF tiles (daily & 7-day maximum composites)
**Processing version documented:** V6 (a.k.a. `V6T`), released Feb 2025
**Compiled:** 2026-07-01 · **Access date for all live checks below:** 2026-07-01
**Compiled by:** Claude (Opus 4.8) with Arik. Every quantitative claim traces to a cited primary source or to an empirical check we ran (script noted). Ambiguities are flagged, not smoothed over.

> **Scope note.** This file documents the **NASA-produced CI_cyano raster product** distributed by the OB.DAAC (the spectral signal SePRO's brief asks us to fuse). It is the authoritative, gridded source. EPA also serves *lake-aggregated* views of the same underlying data through the CyANWeb app / mobile REST API (see §7.3); those are a convenience layer over this product, documented but not the primary pull here.

> **📦 CANONICAL LOCAL DATA STORE (start here in future sessions).**
> The full working dataset lives under **`data-sources/cyan/data/raw/`** (gitignored — regenerate via `access/pull_cyan.py`):
> - **`conus_mosaic_weekly/`** — **the primary bulk dataset**: the **entire weekly CONUS mosaic period of record**, consistent `CYAN` / `OBPG_version 6.0` stream. **Verified 2026-07-01: 752 files, 4.04 GB, 0 failed/incomplete**, all 64-hex sha256 in `manifest.jsonl`. Coverage: **MERIS 2008-01-06 → 2012 (221 wks; 2012 = 14 wks, Envisat failure)**, empty 2013–2015 gap, **OLCI 2016-04-24 → 2026-06-21 (531 wks)**. Each file is the whole-CONUS 300 m EPSG:5070 grid (26,328×15,138; land a constant 33.25%). Per-file ~3.7–8.4 MB.
> - **`*.tif` at the top level** — the small **Lake Erie tile `7_2`, 2022 weekly** demo sample (52 files) used by the default QA/viz. Tiles are byte-identical crops of the mosaics (§3).
>
> Pulled & validated 2026-07-01. **Newest record = weekly composite 2026-06-21 → 06-27** (already at the API frontier for weekly). Weekly is the default cadence; daily is available on demand (`--period daily`) and reaches ~2 days fresher. Re-pull/extend anytime via `access/pull_cyan.py --tiles all --sdate … --edate … --outdir …/conus_mosaic_weekly`. **For operational freshness / near-real-time serving, see §13.**

---

## 0. TL;DR for the modeler (read this first)

| Question | Answer |
|---|---|
| What is it? | Satellite-derived **Cyanobacteria Index** (`CI_cyano`), a spectral proxy for cyanobacteria abundance in inland/near-coastal U.S. waters. |
| Native form | **8-bit GeoTIFF**, 1 band, digital numbers (DN) 0–255, delivered as **regional tiles**. |
| Resolution | **~300 m** (nominally; exactly 289.894507 m — [V6 release notes Appendix A](#8-sources)). |
| Coverage (space) | **CONUS** (9×6 tile grid) and **Alaska** (4×3 tile grid). Only waterbodies ≥ ~900 m across (≥3×3 pixels) are considered reliable. |
| Coverage (time) | **MERIS** 2002–2012, then a **~2012→2016 gap**, then **OLCI/Sentinel-3** 2016–present (see §2 for the date caveat). |
| Cadence | **Daily** and **7-day max composite**; archive updated **weekly** (new week available ~COB the following Monday). |
| The value in a pixel | The **maximum** CI over the period (both daily and 7-day are *max* composites). |
| How to read the number | `CI_cyano = 10^(DN*0.011714 − 4.1870866)` for DN 1–253. DN 0 / 254 / 255 are special (see §4). |
| Access | Search: `cyan_file_search` API (no auth). Download: OB.DAAC `getfile` (**needs free Earthdata Login**). See §7. |
| Bulk or on-the-fly? | **Do not bulk-download the whole archive** (~hundreds of GB–TB, see §6). Subset by tile + date range, or use the per-lake EPA layer. |
| Likely role in our model | Primarily the **target / label** (the bloom signal we predict or detect); secondarily a **feature** (lagged autoregressive CI) and a **water mask**. See §9. |

---

## 1. What CyAN is

CyAN is a multi-agency U.S. program (**EPA, NASA, NOAA, USGS**; **USACE** joined 2023) that turns ocean-color satellite imagery into a consistent, national **cyanobacteria detection product** for lakes and reservoirs. NASA's Ocean Biology Processing Group (OBPG/GSFC) produces and distributes the `CI_cyano` data; EPA builds the management-facing applications on top of it. ([EPA CyAN page](#8-sources); [V6 release notes Introduction](#8-sources).)

The underlying algorithm is the **Cyanobacteria Index (CI)** — a spectral-shape (second-derivative around 681 nm) method developed by Wynne & Stumpf et al. and refined by Matthews & Odermatt; it responds to the pigment/optical signature of cyanobacteria-dominated water. `CI_cyano` is the cyanobacteria-specific variant. (Algorithm lineage: Wynne et al. 2008/2010; Matthews et al. 2012; Matthews & Odermatt 2015; Coffer et al. 2020; Seegers et al. 2022 — all in the release notes reference list. Cross-references in our literature layer: `Research/_sources/ACAD-083, ACAD-062, ACAD-006, ACAD-045`.)

**Data maturity:** NASA rates this **Stage 2 of 4** — "accuracy estimated using a significant (but not full) set of independent measurements … some peer-reviewed publications on accuracy, but for limited spatial areas." The release notes state the data are **"preliminary and to be used for evaluation purposes only."** We treat CyAN as a strong but not ground-truth signal, and pair it with in-situ data accordingly.

---

## 2. Temporal coverage, cadence & the gaps that matter

| Sensor / platform | Period | Product cadence | Notes |
|---|---|---|---|
| MERIS / Envisat | **2002–2007** | 14-day composites | Instrument "irregularly viewed the US" in this window. |
| MERIS / Envisat | **2008–2012** | 7-day composites **and** dailies | Regular U.S. collection. Envisat failed **Apr 2012**. |
| — gap — | **~2012 → 2016** | — | **No CI record.** MERIS ended 2012; OLCI began 2016. Any multi-year time series must handle this discontinuity. |
| OLCI / Sentinel-3A | **2016–present** ⚠ | daily + 7-day | See date caveat below. |
| OLCI / Sentinel-3B | **2018–present** | daily + 7-day | From 2018 the OLCI product is a **merged S3A+S3B max-per-pixel** composite (V3+). |

✅ **OLCI start-date discrepancy — RESOLVED empirically (2026-07-01).** Docs disagreed (EPA/Earthdata "2016–present" vs release-notes intro "2017–present"). We enumerated the actual CONUS weekly mosaic archive: **the earliest OLCI file is `L20161152016121` = week starting 2016-04-24** (day 115 of 2016). So the record **begins 2016-04-24** — "2016" is correct. **Latest available (as of 2026-07-01): week of 2026-06-21** (`L20261722026178`), i.e. ~1-week latency. The **2013–2015 gap is confirmed empty** (0 files). MERIS 7-day mosaics run **2008 → April 2012** (2012 has ~14 weeks, consistent with Envisat's failure).

**Refresh / latency.** The archive is **updated weekly**; the newest weekly composite is available via the API **by close-of-business the following Monday** ([EPA CyAN App page](#8-sources)). So near-real-time lag is up to ~1 week — acceptable for a "2 weeks early" decision, tight for same-week response.

**Reprocessing cadence.** OBPG reprocesses/redistributes the entire MERIS+OLCI time series **every 10–16 months**, which bumps the version (V4 Mar 2022 → V5 May 2023 → V6 Feb 2025). **Implication:** pixel values are *not* frozen — a value pulled today may differ after the next reprocessing. We must **record the processing version of every file we use** (see §5, §10).

**📌 Project preference (Arik, 2026-07-01):** work only with the **consistent-refresh periods** — **MERIS 2008–2012** (regular 7-day + daily) and the **modern OLCI record 2016–present** — and **skip the sparse MERIS 2002–2007** (14-day, irregular) and the **2012–2016 gap**. **Weekly (7-day)** composites are the default working cadence (soft preference over daily, for now). Combined with the consistent `6.0` stream (§10), this gives ~**806 weekly composites** per tile over the usable POR.

---

## 3. Spatial characteristics

- **Pixel size:** the **distributed GeoTIFF tiles are exactly 300.0 m** (verified 2026-07-01 from a pulled tile). The 289.894507 m figure in release-notes Appendix A is the *upstream L3-binned* resolution before mapping.
- **Projection (distributed GeoTIFFs):** **NAD83 / CONUS Albers Equal Area — `EPSG:5070`** (verified from a pulled tile's CRS), consistent with the release-notes "Albers Equal Area … matched to the NHD projection." (The intermediate L3-binned `.nc` files use an Integerized Sinusoidal Grid; that's upstream of the tiles we use.)
- **Tile extent:** each CONUS tile spans **600 km × 600 km** = 2000 × 2000 pixels (verified; e.g. tile `7_2` bounds ≈ easting 1,034,403–1,634,403, northing 2,114,826–2,714,826 in EPSG:5070).
- **Land mask:** SRTM 60 m SWBD for CONUS; a coarser `landmask_GMT15ARC_AK_v2021.nc` for Alaska.
- **Tiling:** CONUS delivered as a **9 (col) × 6 (row)** grid of tiles; Alaska as **4 × 3**. Filenames end in `<col>_<row>` (e.g. `7_2` = Lake Erie region; `3_3` = Utah Lake; `6_2` = central Wisconsin). A single CONUS tile is **2000 × 2000 px = 600 km × 600 km** (verified). A tile-grid shapefile is published (see §7.4) — needed to map a lat/lon or lake to its tile(s).
- **Full-region mosaic (verified 2026-07-01):** querying `areaids=all` returns **one whole-region mosaic file** instead of tiles — a CONUS mosaic of **26,328 × 15,138 px** (≈6.7 MB compressed weekly; ≈399 MB uncompressed in RAM) and an Alaska mosaic (≈0.8 MB). Filenames drop the `<col>_<row>` suffix (`…_CYAN_CONUS_300m.tif`, `…_CYANAK_CI_cyano_CYAN_AK_300m.tif`). The mosaic is the efficient path for **national** coverage; tiles are efficient for a **lake/state**. **Verified identical (2026-07-01):** for 4 weeks across seasons, tile `7_2` is a **byte-for-byte crop of the CONUS mosaic** — same EPSG:5070 grid, integer pixel offset (16612, 3589), **0 of 4,000,000 pixels differ**. So tile vs mosaic is purely a download-efficiency/scope choice, not a data choice. (Caveat: compare like-for-like streams — a `6.0` tile vs a `6T` mosaic could differ. The mosaic canvas is a large Albers extent well beyond CONUS, mostly nodata outside populated areas; tiles are exact 2000×2000 windows onto that grid.)
- **Minimum reliable waterbody size:** retrievals are "considered more robust for lakes **≥ 900 m window width**" = a **≥3×3-pixel** array of water (Clark et al. 2017, cited in release notes Known Issue #5). **Smaller lakes and rivers are *not masked* and their values may be erroneous.** Independent literature (`Research/_sources/ACAD-013`) notes only ~5% of U.S. lakes are resolvable at 300 m. This is the single biggest fitness-for-use caveat for SePRO's likely smaller-waterbody customers.

---

## 4. The pixel encoding & quality flags — EXACT values (authoritative)

The distributed `CI_cyano` GeoTIFF is **8-bit, single-band**. Per the **V6 release notes** (verbatim):

| DN value | Meaning | Handling |
|---|---|---|
| **0** | **Below CI detection threshold** ("non-detect") — water *was* observed, no cyano detected | **Informative, not missing.** Treat as "measured, below limit." In EPA imagery these render grey (vs black for no-data). |
| **1–253** | **Valid CI data** | Convert to CI via the formula below. |
| **254** | **Land** | Mask out. |
| **255** | **No data** (e.g., cloud, ice cover, no valid retrieval) | Missing. Exclude. |

**DN → index conversion (DN 1–253 only):**

```
CI_cyano = 10 ** (DN * 0.011714 − 4.1870866)      # units: sr^-1 (a spectral index)
```

**DN → approximate cell density.** The standard CyAN relation is **`cells/mL ≈ 1e8 × CI_cyano`** (Lunetta et al. 2015), which maps DN 1–253 to roughly **6.7×10³ … 6×10⁶ cells/mL** (consistent with the commonly-quoted ~10⁴–7×10⁶ range). Implemented as `cyan_api.ci_to_cells_per_ml`. Treat cells/mL as an **approximate, literature-derived conversion with real scatter/uncertainty**, not an exact measurement — cite it as such in any claim.

**No NaN / no raster nodata flag (verified 2026-07-01).** The GeoTIFF has **no `nodata` metadata flag and contains no NaNs** — *every* pixel is an explicit integer code 0–255. So there is **no automatic "NA" for land or missing data**: land is the literal value `254`, clear-but-no-bloom water is `0`, and cloud/ice/no-retrieval is `255`. Translating those codes into masks/NaN is **on us** (done in `cyan_api.classify_dn` / `dn_to_ci`). Empirical composition of one peak-bloom tile: land 72.9%, below-detection 23.6%, no-data 3.3%, valid CI 0.27%.

> **Two critical modeling consequences:**
> 1. **DN 0 (non-detect) ≠ missing.** Collapsing 0 into NaN throws away true absence information and biases any bloom-frequency statistic. Keep them distinct.
> 2. **The floor is a detection limit, not zero cyanobacteria.** "Below threshold" means below the sensor's ~10^4 cells/mL sensitivity, not sterile water. State this wherever we report absence.

### 4.1 Do NOT confuse CyAN with the NOAA CI product
The release notes explicitly warn that NOAA/NCCOS produces a *different* CI product with a **different DN encoding**:

| | Valid range | Land | Invalid/no-data |
|---|---|---|---|
| **CyAN (NASA — this dataset)** | 0–253 | **254** | 255 |
| NOAA/NCCOS | 0–250 | **252** | 251, 253, 254, 255 |

Values also differ due to different binning/mapping and land masks. **We use the CyAN encoding above.** Any code or threshold copied from a NOAA CI workflow is wrong for these files.

### 4.2 Additional QA flags exist but are NOT in the GeoTIFF DN
The general CyAN documentation mentions flags for snow/ice, land-adjacency, and mixed (land+water) pixels. **These are not encoded in the 1-band `CI_cyano` GeoTIFF** (which only carries the 0/1–253/254/255 scheme above). Per the release notes **Known Issues**, the snow/ice and mixed-pixel flags "have been added" but are **"not yet verified"**, and a separate biophysical water-quality **flag dataset** exists (Urquhart & Schaeffer 2019, *Data in Brief*). **Fitness-for-use flags we must apply ourselves are in §5.**

---

## 5. Known issues & limitations (from the source — the honest list)

Straight from the V6 release notes "Known Issues" + validation caveats. These are deliverables in their own right (the brief rewards naming limitations):

1. **Ice/snow → false highs.** Ice can register as **high CI**. The snow/ice flag is applied but **unverified**. Use extreme caution for cold-season / high-latitude pixels. Unknown whether cyano under thin ice is detectable at all.
2. **Thin clouds → false highs.** Undetected thin cloud can push CI above the detection threshold (false positive bloom).
3. **Land mask is imperfect.** SRTM mask "may cover dry lakes and may exclude other lakes"; an eroded land mask is still needed. Expect edge/nearshore contamination.
4. **Mixed pixels (land+water) at shorelines** — flag exists but **unverified**; nearshore pixels are suspect.
5. **Small waterbodies & rivers unreliable** — only ≥900 m (≥3×3 px) water is robust; smaller features are unmasked and "may be erroneous" (§3).
6. **No water-level correction** — drought/flood changes in lake extent are not accounted for (affects which pixels are water over time).
7. **7-day max can be < daily max** — occasionally, due to averaging during reprojection to Albers. So the 7-day composite is not a strict upper bound on that week's dailies.
8. **Turbid-water false positives** — reduced (not eliminated) in V5/V6 via an improved turbid-water test; highly turbid inland waters can still mislead the CI.
9. **Preliminary / Stage-2 maturity** — validated against a limited set of U.S. locations (Lake Erie, FL, OH, VT, NH, RI, CT, MA, OR, CA, IN, NJ, NY, UT, ME, ID). Accuracy outside validated regions is less characterized.

**Bias/representativeness summary for the prep stage:** cloud/ice gaps are non-random (seasonal, latitudinal); non-detects are frequent and meaningful; small/urban/turbid waters are under-served; and values are version-dependent. All of this must surface in the "inspect & prepare" narrative.

---

## 6. Bulk-download vs. on-the-fly — the feasibility call

**Recommendation: subset, don't bulk-mirror.** Rationale (order-of-magnitude, documented so it's auditable):

- A CONUS daily `CI_cyano` archive is **54 tiles/day × ~365 days × ~9 years (2016–present) ≈ 1.8×10^5 files**. At ~1–3 MB/tile that is **~0.2–0.5 TB for CONUS daily CI alone** — before 7-day composites, Alaska, or true-color. Mirroring the whole product is impractical and unnecessary.
- **But per-study-area subsetting is very reasonable:** one tile's full daily time series ≈ 365 × ~9 ≈ **~3,300 files (~3–10 GB)** — a comfortable local working set for a focused analysis (e.g., the Lake Erie tile `7_2`).

**Chosen strategy (this repo):**
1. **Enumerate** exactly the (region, period, product, tiles, date-range) we need via `cyan_file_search` (no auth).
2. **Download** only those files via `getfile` (Earthdata auth), **cached** to `data/raw/` and never re-fetched if present.
3. For per-lake time series, either (a) extract from the cached tiles using a lake polygon, or (b) use the EPA per-lake API (§7.3) as a cross-check.

This honors "acquire only what you need, script it, cache it, regenerate from code."

---

## 7. How to access it (verified 2026-07-01)

### 7.1 Search / enumerate — `cyan_file_search` (no authentication)
- **Endpoint:** `POST https://oceandata.sci.gsfc.nasa.gov/api/cyan_file_search`
- **Form params:**
  - `region`: `1` = CONUS, `0` = Alaska
  - `period`: `2` = Daily, `1` = Weekly (7-day)
  - `product`: `1` = Cyanobacteria Index (`CI_cyano`), `2` = True Color
  - `areaids`: a single tile `7_2`, several joined with `+` (`1_1+2_1`), or **`all`** — but note **`all` returns the single whole-region mosaic file, not the set of tiles** (§3). To pull specific tiles you must list them.
  - `sdate`, `edate`: `YYYY-MM-DD`
  - `addurl`: `1` to return full download URLs
  - `results_as_file`: `1` to return a plain newline-delimited list
  - `wgetflag`: `1` (**mandatory**)
- **Returns:** newline-delimited `https://oceandata.sci.gsfc.nasa.gov/getfile/<filename>` URLs.
- **⚠ Reliability:** we observed **intermittent HTTP 502** from this endpoint on 2026-07-01; it succeeded on retry. **Always wrap calls in retry-with-backoff** (our client does). The generic `/api/file_search` does **not** index CyAN correctly ("database error"/"No Results") — use `cyan_file_search`.
- **⚠ Zero-result quirk:** with `results_as_file=1`, a query with **no matches** (e.g. the 2013–2015 gap) returns the **full HTML search-UI page** (or an empty body), *not* a plain "No Results" — our client treats an HTTP-200 HTML/empty response as an empty result set (`[]`), not an error.
- **Whole-region mosaic vs tiles:** `areaids=all` → one mosaic file/date (§3); list explicit tiles for per-tile pulls.
- **⚠ Two file families per date (verified 2026-07-01).** A single daily/weekly query returns *both*:
  1. **Merged product** — `L<date>.L3m_<DAY|7D>_<stream>_CI_cyano_CYAN_<CONUS|AK>_300m_<tile>.tif`. This is the **merged Sentinel-3A + 3B max-per-pixel** composite (V3+). **This is what we use** — best coverage, matches the documented merged product.
  2. **Per-satellite products** — `S3A_OLCI_EFRNT.<YYYYMMDD>.L3m.DAY.<stream>.CI_cyano.CYAN_CONUS.300m_<tile>.tif` (and `S3B_…`), a *different, dot-separated* naming. These are the single-sensor inputs to the merge; we **do not** use them for the primary series.
  Our acquisition code keeps only the merged `L…`/`M…` family and **logs the count of each family kept/dropped** so the exclusion is explicit, never silent.

### 7.2 Download — OB.DAAC `getfile` (**Earthdata Login required**)
- **Pattern:** `GET https://oceandata.sci.gsfc.nasa.gov/getfile/<filename>`
- Unauthenticated requests **302-redirect to `urs.earthdata.nasa.gov` OAuth** (verified). You must authenticate via one of (auth precedence in our code: token → appkey → netrc):
  - **EDL bearer token** (what we use; verified working 2026-07-01): send header `Authorization: Bearer <token>`. Generate at `https://urs.earthdata.nasa.gov/` → *Generate Token* (JWT, ~60-day life).
  - **AppKey**: append `?appkey=<KEY>`; generate at `https://oceandata.sci.gsfc.nasa.gov/appkey/`.
  - **`.netrc`**: `machine urs.earthdata.nasa.gov login <USER> password <PASS>` (chmod 600).
- **Setup:** free account at `https://urs.earthdata.nasa.gov/users/new`. This repo reads `OB_DAAC_EDL_TOKEN` (preferred) or `OB_DAAC_APPKEY` from `data-sources/.env` (gitignored) or the environment. **No credentials are committed.** ⚠ Note: AWS S3 "s3credentials" (temporary `ASIA…` keys) are a *different* mechanism and do **not** authenticate `getfile` — use an EDL token/AppKey.

### 7.3 EPA per-lake layer (convenience; documented, secondary)
- **CyANWeb app:** `https://qed.epa.gov/cyanweb/` — satellite CI for **2,000+ of the largest U.S. lakes/reservoirs** (released 2021). Good for eyeballing and for a per-lake cross-check.
- **CyAN mobile REST API:** base `https://cyan.epa.gov/cyan/cyano/`, endpoints `.../location/data`, `.../location/images`, `.../notifications` (GET, JSON). Documented in "CyAN mobile app client REST API — A programmer's and user's guide" (Galvin 2018, EPA Science Inventory). **Status: not yet verified by us** — may require app registration/token. Flagged for follow-up before relying on it.

### 7.4 Ancillary
- **Tile-grid & lake shapefiles** for CONUS/Alaska (MERIS/OLCI coverage) are published by CyAN — needed to map lat/lon ↔ tile and to define per-lake polygons.
- **DOI (merged S3 OLCI L3B, V6T):** `10.5067/MERGED-S3/OLCI/L3B/CYAN/CI/6T` (this is the upstream L3-binned product; the L3m tiles are derived from it).

---

## 8. Sources (all accessed 2026-07-01)

1. **V6 release notes (primary, authoritative)** — "Release notes for NASA-produced MERIS and OLCI cyanobacteria index (CI_cyano) data product…", NASA OBPG, V6 (Feb 2025; known-issues update Aug 2025). PDF: `https://oceancolor.gsfc.nasa.gov/images/cyan/version/6/CyAN_NASA_MERISOLCI_CI_release_notes_V6_Aug_2025.pdf`. Local cache of extracted text: `data-sources/cyan/reference/CyAN_V6_release_notes_extracted.txt`.
2. **EPA — Cyanobacteria Assessment Network (CyAN):** `https://www.epa.gov/water-research/cyanobacteria-assessment-network-cyan`
3. **EPA — CyAN App / CyANWeb:** `https://www.epa.gov/water-research/cyanobacteria-assessment-network-application-cyan-app`; app at `https://qed.epa.gov/cyanweb/`; User's Guide `https://qed.epa.gov/cyanweb/assets/CYANWEB-USERS-GUIDE_09314022-Final.pdf`
4. **NASA Earthdata — CyAN project:** `https://www.earthdata.nasa.gov/data/projects/cyan`; CyAN File Search tool: `https://www.earthdata.nasa.gov/data/tools/cyan-file-search`
5. **OB.DAAC download methods / auth:** `https://www.earthdata.nasa.gov/learn/tutorials/search-download-methods-data-archived-ob-daac`; AppKey: `https://oceandata.sci.gsfc.nasa.gov/appkey/`
6. **EPA CyAN REST API guide (metadata record):** `https://cfpub.epa.gov/si/si_public_record_report.cfm?LAB=NERL&dirEntryID=346396`
7. **Empirical checks we ran (2026-07-01):** `cyan_file_search` live queries confirming filename conventions, the `CYANV6T`/`CYAN` variant coexistence, weekly vs daily naming, and the Earthdata redirect on `getfile`. Reproducible via `data-sources/cyan/access/` scripts.

---

## 9. Likely role in the SePRO HAB analysis

CyAN `CI_cyano` is **the remote-sensing half of the spectral-meets-aquatic fusion** the brief centers on. Concretely:

- **Primary — target / label.** For a risk-forecasting or early-warning framing, CI (or a CI-derived bloom flag, e.g. CI above an advisory threshold) is the **outcome we predict**. This is the most natural fit given the brief's "which waterbodies will bloom in the coming weeks" steer.
- **Secondary — feature.** **Lagged** CI (last week's / last month's bloom state, plus climatology and trend) is typically the single strongest predictor of near-future blooms; it enters the feature set autoregressively. *(Guard against target leakage: lagged CI as a feature must be strictly past-dated relative to the target date.)*
- **Supplemental — mask / context.** The land/no-data/detection encoding defines valid water pixels and observation availability; non-detect frequency is itself a useful lake descriptor.

**What it is *not*:** a direct toxin measurement. CI ↔ cell density ↔ toxin concentration are successively looser links (correlation ≠ causation; toxin depends on strain/conditions). Toxin claims must come from in-situ data, not CI alone.

---

## 10. Reproducibility & version pinning (project rules for this dataset)

- **Record the processing version of every file used.** Because filenames are ambiguous (both `CYANV6T` and plain `CYAN` appear, and plain `CYAN` carries no version token), we **read the embedded version from each GeoTIFF's `OBPG_version` metadata tag during QA** and log it — version is verified *from the data*, not inferred from the name.
- **✅ Resolved empirically (2026-07-01):** across a full-year 2022 pull of tile `7_2`, the `OBPG_version` tag showed **plain `CYAN` files → `6.0` (41 files)** and **`CYANV6T` files → `6T` (11 files)**. **Both are Version 6** — so the historical plain-`CYAN` files are *not* an older V4/V5 processing; they are V6-reprocessed. The `6T` variant appears only for a mid-season subset. This removes the earlier concern that mixed filenames implied mixed algorithm versions. (Still: log the tag per file, since a future reprocessing will change it.)
- **Default stream = `CYAN` (`OBPG_version 6.0`) for a CONSISTENT series (updated 2026-07-01).** `6.0` is available across the whole record; `6T` only for a subset, so preferring `6T` would *mix batches mid-series*. The `pull_cyan.py` default is now `--stream CYAN`; `--stream CYANV6T` remains available for single-date work. Verified: a re-pulled 2022 weekly `7_2` series is uniformly `6.0` (52/52).
- **Default cadence = weekly** (`--period weekly`), per project preference (§2).
- **Cache & manifest:** every download is cached under `data/raw/` and recorded in `manifest.jsonl` — **filename, URL, bytes, sha256, `processing_version` (read from the GeoTIFF), `integrity`, stream, dates, region, tile, is_mosaic, access timestamp** — so any figure/metric traces to the exact bytes it used. **Cache hits are validated against the manifest sha256:** a stale/corrupt cached file is detected and re-fetched (surfaced as `integrity=refetched_stale_cache`); if freshly-fetched bytes still differ from the manifest, that's flagged `integrity=mismatch` (upstream reprocessing). Re-runs dedupe (no manifest bloat) but always record real integrity events.
- **QA provenance:** `qa_cyan.py` flags any raster **not present in the manifest** (traceability gap), any **sha256 mismatch**, and checks **CRS + shape + transform** consistency across files.
- **Access date** for this documentation and all live checks: **2026-07-01**.

---

## 11. Download cost & scaling (empirical, 2026-07-01)

Grounded in measured values: per-tile weekly file ≈ **207 KB** (mean of 52); **CONUS mosaic ≈ 6.7 MB** (26,328×15,138 px → **399 MB uncompressed RAM**); **Alaska mosaic ≈ 0.8 MB**. Throughput measured: small files ~**0.6 MB/s** (latency-bound, serial) / ~2.9 files/s; large mosaics ~**9.8 MB/s** (bandwidth-bound). Usable weekly POR ≈ **806 composites** (2008–2012 + 2016–present). Daily ≈ 7× weekly.

| Scope | Approach | Weekly-POR size | Download time* | Peak RAM (streamed per-file) |
|---|---|---|---|---|
| 1 tile (e.g. `7_2`) | per-tile | ~806 files ≈ **170 MB** | ~5 min | 4 MB/tile (full stack ≈ 3.2 GB) |
| 1 state — IN (~1–2 tiles) | per-tile | **170–340 MB** | ~5–10 min | 4 MB/tile |
| 1 state — NC (~2–3 tiles) | per-tile | **340–510 MB** | ~10–15 min | 4 MB/tile |
| Entire US (CONUS+AK) | **mosaic** | ~1,612 files ≈ **~6.0 GB** | **~15–30 min** | ~400 MB per CONUS mosaic |
| Entire US | per-tile (alt) | ~54 tiles ≈ **~9 GB**, ~43k files | hours (latency) | 4 MB/tile |
| **Entire world** | — | **N/A — CyAN = CONUS + Alaska only** | — | — |

\*Current serial downloader; concurrency would cut small-file cases ~5–10×. Enumerate = 1 `cyan_file_search` per scope+range (retry 502s). Ongoing refresh ≈ 1 file/scope/week (US ≈ 7.5 MB/week — trivial).

**RAM verdict for a 16–32 GB machine:** never the bottleneck **if we process per-tile / per-date** (≤400 MB for a CONUS mosaic; 4 MB per tile). The only way to exhaust RAM is naively stacking a multi-year archive into one array (100s of GB) — which the pipeline avoids. **State-tile counts are approximate** (from geometry); exact sets come from the CyAN tile-grid shapefile (§7.4) or by clipping the CONUS mosaic to a state polygon.

---

## 12. Aggregation policy (project rule)

**Never spatially or temporally aggregate CyAN data — in analysis or visualization — without explicit permission.** Aggregation (downsampling, binning, averaging, resampling-with-averaging) can distort values with hard-to-trace downstream effects. Practical consequences here:

- Work at **native 300 m** and the source's **native temporal composites** by default.
- CyAN's own **daily/7-day *max* composites are provider-side aggregation** intrinsic to the product — fine to *use* as-is; we simply don't add more on top.
- The interactive map's hover grid is **native 300 m** by default; the `viz/viz_cyan.py --agg N` flag is an **explicit, default-off opt-in** for mean-aggregation, and reprojection to lat/lon uses **nearest-neighbour** (resampling, not averaging — values preserved).
- When a viz would be too heavy at native resolution, reduce **scope** (extent via `--bbox`, or number of weeks) — not resolution.

---

## 13. Operational freshness & near-real-time (train-on-old → serve-on-fresh)

This matters because we will **train a model on the historical archive and then operationalize forecasts on fresh live pulls**. The key facts (all verified live 2026-07-01; "today" = 2026-07-01):

**Freshness snapshot — what's the newest data, and how fresh can we get?**

| | Newest available (2026-07-01) | Latency vs today | Granularity |
|---|---|---|---|
| **In our ingest** (weekly canonical set) | 7-day composite **2026-06-21 → 06-27** (`L20261722026178`) | window-end **4 days** old | 7-day max |
| **Live API — weekly** | **same** (2026-06-21 → 06-27) | 4 days | 7-day max |
| **Live API — daily** | **2026-06-29** (`L2026180`) | **2 days** | single-day max |

So: **our weekly ingest is already at the API frontier** — there is *no fresher weekly composite* to pull today. The only way to get *fresher* data live is the **daily** product, which reaches **2026-06-29** — **~2 days newer** than the latest weekly composite's window-end, at daily (not 7-day-max) granularity. Recent dailies are continuous (06-22…06-29) but daily products are generally gappier (more cloud/no-data) than the 7-day max.

**Refresh cadence (how often new data appears):**
- **Weekly** composites post **~COB the Monday after the 7-day window closes** — so the current in-progress week (2026-06-28 → 07-04) should appear ~**2026-07-06**. Practical steady-state latency for weekly: **up to ~1 week**.
- **Daily** products appear with **~1–3 day latency** after the satellite overpass/processing.
- Fundamental floor: Sentinel-3 revisit + atmospheric-correction/processing time. No public route is fresher than the daily product for this CI algorithm (EPA CyANWeb/mobile serve the *same* underlying data, not fresher).

**Operational implications for the model:**
1. **No train/serve representation skew.** The operational feed is the *same product, API, encoding, EPSG:5070 grid, and `CYAN`/6.0 stream* as the training archive. A model trained on the archive consumes live pulls with zero schema/units translation. Enumerate-and-download is identical (`pull_cyan.py --tiles all --period {weekly|daily} --sdate <recent> --edate <today>`); only the date window changes.
2. **⚠ Recent data is *preliminary* and version-mutable.** NASA labels the product "preliminary / evaluation" and **reprocesses the whole series every 10–16 months** (version bump; §2). The newest near-real-time weeks are most likely to shift on reprocessing. Therefore, at serve time: **record the `OBPG_version` of every operational pull** (QA already does), treat the latest 1–2 composites as provisional, and **plan a periodic re-pull + retrain after each reprocessing** so training and serving stay on the same product version.
3. **Forecast horizon vs latency.** The brief values a call *"two weeks early."* Weekly latency (~up to 1 week to the current week) is acceptable inside a multi-week forecast horizon; **switch to daily only if we need the freshest possible nowcast**, accepting more gaps. Either way the *target* the model forecasts is a *future* CI, so input latency eats into (but does not by itself defeat) the lead time.
4. **Leakage guard when mixing cadences.** If daily is used to "top off" recency near the frontier while training used weekly max, align them carefully — a 7-day-max target must not be fed a same-window daily as a feature (that is look-ahead). Keep feature/target windows strictly past-dated (§9).

*Re-verify these dates before any operational launch — they advance weekly.*
