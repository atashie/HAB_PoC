# Data-sources layer — decisions & assumptions log

Running log of choices made building the acquisition layer, with rationale. Newest first.

## 2026-07-01 — Data freshness / operational near-real-time documented (session 4)
- **Freshness verified live:** newest data = weekly composite **2026-06-21→06-27** (our ingest is already at
  the API frontier for weekly). Fresher live option = **daily**, latest **2026-06-29** (~2 days newer, daily
  granularity). Weekly refreshes ~COB the Monday after the window closes (~1-week steady-state latency);
  daily ~1–3 day latency. Documented in METADATA **§13** (train-on-old → serve-on-fresh): no train/serve
  representation skew (same product/API/encoding/grid/6.0 stream); ⚠ recent weeks are preliminary &
  version-mutable (reprocessing every 10–16 mo) → log OBPG_version at serve time, plan periodic retrain;
  leakage guard when mixing daily/weekly cadences.
- **Codex/GPT-5 review of the ingest/analysis code** (6 findings; core DN→CI math & masks confirmed sound).
  Verified each against the code, then applied 5 clear fixes + labeled 1:
  1. (high) QA now **flags rasters missing from the manifest** (was silently `sha256_ok=None`, no flag).
  2. (high) **Cache hits validated against manifest sha256** — stale/corrupt cache is detected, refetched,
     and surfaced (`integrity=refetched_stale_cache`); persistent diff → `mismatch` (upstream reprocessing).
  3. (med) Manifest now records **`processing_version`** (read from each GeoTIFF) + `integrity` + `is_mosaic`;
     re-runs dedupe. Fixes a prior doc/code mismatch (net.py had claimed version was recorded).
  4. (med) `prefer_stream()` **library default flipped `CYANV6T`→`CYAN`** (matches the consistent-series policy;
     the CLI already defaulted to CYAN, but direct API callers got the wrong default).
  5. (med) Summary chart **relabeled as an explicit "SPATIALLY AGGREGATED diagnostic, not model input"**
     (it reduces each scene to per-date stats). **Resolved (Arik, session 4): keep it, clearly labeled** —
     a per-date summary inherently aggregates; the label makes it honest/non-silent. Map + raw GeoTIFFs
     remain the native source of truth.
  6. (med) QA cross-file consistency now also checks **`transform`** (was CRS+shape only; docstring had over-claimed).
  All re-tested (fresh pull, cache-verify, corruption→refetch, missing-manifest flag, transform check); no regressions.

## 2026-07-01 — Canonical dataset = full weekly CONUS-mosaic POR (session 3)
- **Downloaded the entire weekly CONUS mosaic period of record** (consistent `CYAN`/`6.0`) to
  `cyan/data/raw/conus_mosaic_weekly/` — **the canonical local dataset going forward**. Verified complete:
  **752 files, 4.04 GB, 0 failed**, all sha256'd; MERIS 221 wks (2008→Apr 2012) + OLCI 531 wks (2016-04-24→2026-06-21).
  Prominently pointed to in METADATA (top callout), README, and DATA-REGISTRY so future sessions know where
  to look. Verified the mosaic spans the **same POR + weekly cadence** as tiles and is the same 6.0 stream.
- **Empirically resolved the OLCI start date:** earliest CONUS weekly mosaic = **2016-04-24** (`L2016115…`),
  latest = **2026-06-21**. 2013–2015 gap confirmed empty. MERIS 7-day mosaics 2008→Apr 2012. Updated METADATA §2.
- **Kept the demo tiles at `data/raw/` top level** (52 `7_2` 2022 files) so the default QA/viz keep working;
  the bulk mosaics live in the subfolder (non-recursive glob → default QA won't try to open 752×399 MB files).
- **Extended the parser** (`CyanFile.is_mosaic`, mosaic filename handling) so pull/QA/manifest work for the
  `areaids=all` whole-region mosaics, not just tiles.
- **Fixed `search_files` robustness:** a zero-result `cyan_file_search` (e.g. the 2013–2015 gap) returns the
  HTML search-UI page or an empty body — now treated as "no results" (return `[]`) instead of raising.

## 2026-07-01 — CyAN preferences, aggregation policy, cost model (session 2)
- **Aggregation requires explicit permission (project rule, user directive).** Never spatially/temporally
  aggregate — analysis *or* viz — without asking. Triggered by my mistake: the map hovers had silently
  mean-aggregated pixels to ~1.8 km. **Fix:** hover is now **native 300 m** by default; `viz --agg N` is an
  explicit opt-in; reprojection uses nearest (no averaging). When native is too heavy, reduce **scope**
  (`--bbox`, fewer weeks), not resolution. Saved to persistent memory `aggregation-requires-permission`.
- **Period of record = consistent-refresh only (user).** Use **MERIS 2008–2012** + **OLCI 2016–present**;
  skip sparse MERIS 2002–2007 and the 2012–2016 gap. ≈806 weekly composites/tile over the usable POR.
- **Cadence default = weekly** (`--period weekly`), soft preference over daily (user).
- **Stream default flipped to `CYAN` (6.0)** for a consistent series (was `CYANV6T`). `6.0` spans the whole
  record; `6T` is a partial batch, so preferring it mixed batches mid-series. Re-pulled 2022 `7_2` weekly →
  uniformly `6.0` (52/52), re-QA'd, re-viz'd.
- **Full-region mosaic discovered.** `areaids=all` returns ONE whole-region mosaic (CONUS 6.7 MB /
  26,328×15,138 px; AK 0.8 MB), not the tile set. Mosaic = efficient for national; tiles = efficient for
  a lake/state. Documented in METADATA §3/§7/§11.
- **Download-cost model (empirical).** Measured file sizes + throughput → cost table in METADATA §11.
  Headlines: 1 tile POR ≈170 MB/~5 min; entire US (mosaic) ≈6 GB/~15–30 min; **"entire world" N/A**
  (CyAN is CONUS+AK only). RAM never the bottleneck if processed per-tile/per-date.
- **Auth = EDL bearer token** now the primary path (verified). User first supplied AWS S3 temp creds
  (wrong mechanism for getfile) then an EDL JWT token, which works via `Authorization: Bearer`.
- **Map UX:** added per-cell hover (DN, CI, ~cells/mL), live lat/lon (MousePosition), exclusive week
  selection (GroupedLayerControl), `--bbox` scope crop, coord rounding to 4 dp. Demo map cropped to Lake
  Erie, 8 weeks, native → ~9 MB.

## 2026-07-01 — Layer foundations
- **Stack = Python** (user decision). Best fit for satellite raster + in-situ + the Part B tool;
  matches the existing Python 3.13 env. All deps already installed; pinned in `requirements.txt`.
- **Viz = Folium + Plotly** (user decision). Self-contained interactive HTML maps + charts, no server.
- **Structure = per-dataset subfolders** (user decision). Each source self-contained
  (`docs/access/qaqc/viz/outputs/data`), shared helpers in `_common/`, top-level `DATA-REGISTRY.md`.
- **Env/deps = venv + pinned requirements.txt** (assumption; user may prefer uv/conda). Most
  portable on Windows; geospatial wheels installed cleanly, so conda wasn't needed.

## 2026-07-01 — CyAN (first dataset)
- **Product chosen = CI_cyano L3m GeoTIFF tiles (merged S3A+S3B)**, not the per-satellite
  `S3A_/S3B_` files nor the L3-binned `.nc`. Merged = best coverage + matches documented product.
  Per-satellite files are enumerated but excluded, with counts logged (no silent drop).
- **Access = OB.DAAC `cyan_file_search` (enumerate, no auth) + `getfile` (download, EDL auth).**
  The specialized `cyan_file_search` is required (generic `file_search` doesn't index CyAN).
  Endpoint 502s intermittently → retry/backoff in `_common/net.py`.
- **Auth = Earthdata Login JWT bearer token** (`Authorization: Bearer`), verified working
  2026-07-01. AppKey (`?appkey=`) and `.netrc` also supported as fallbacks. Credentials live in
  gitignored `.env`. (User initially supplied AWS S3 temp creds — wrong type for the getfile
  HTTPS path — then the EDL token, which works.)
- **Bulk vs subset = subset by tile + date.** Full CONUS daily archive ≈ 0.2–0.5 TB; not mirrored.
  Justification recorded in `cyan/METADATA.md` §6.
- **Version handling = read `OBPG_version` GeoTIFF tag at QA, don't trust filename.** Verified
  empirically that plain `CYAN` files = `6.0` and `CYANV6T` = `6T` — **both Version 6** (historical
  files are not stale V4/V5). Prefer `CYANV6T` when present, else `CYAN`.
- **Validation sample = tile `7_2` (Lake Erie region), full-year 2022 weekly (52 files).** Chosen
  because western Lake Erie is the canonical, CyAN-validated U.S. cyanoHAB site → clear seasonal
  signal for visual validation. Peak-week render reproduced the known Maumee-Bay bloom.

## Assumptions still open / to revisit
- **OLCI start date (2016 vs 2017):** docs disagree; not yet bracketed empirically. To confirm via
  `cyan_file_search` when a longer time series is needed.
- **EPA per-lake REST API (`cyan.epa.gov`):** documented but unverified (may need app registration);
  the raster path is our primary route. Revisit if per-lake time series are needed at scale.
- **Env manager:** venv assumed; switch to uv/conda if the team prefers.
