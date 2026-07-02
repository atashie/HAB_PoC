# Data-sources layer — decisions & assumptions log

Running log of choices made building the acquisition layer, with rationale. Newest first.

## 2026-07-02 — EPA experimental cyanoHAB forecast onboarding (`cyano_forecasts`, session 9)
- **Thorough review of EPA's experimental 7-day cyanoHAB forecast** (Schaeffer et al. 2024, INLA
  Bayesian) from primary sources + **live probes** → answered the onboarding questions. **⚠ This is a
  *modeled forecast*, distinct from the `cyan` satellite CI product — and it is itself CyAN-derived.**
  1. **Restrictions:** underlying data are U.S. public-domain (EPA disclaimers); official model **code**
     is under the **ScienceHub License** (DOI `10.23719/1529140`). The real caveat is the **access
     method**, not copyright (see #3).
  2. **Features/consistency:** a **perfectly rectangular per-lake-week panel** `[probe]` — 10 fields
     (`COMID`, centroid lat/lon, `State`, `EPA_region`, `WeekEndDate` (Sat), `Year`,
     `Percent_chance_of_cyanoHAB` 0–100, `Lake_name_for_public`), **identical for every lake**, **zero
     nulls**. **105,168 rows = 2,191 lakes × 48 weeks**. Weekly, Apr–Nov; latest week ~5 d old (current).
  3. **API — the big finding:** the live values have **NO official REST/CSV/file/ArcGIS API**
     `[probe]` — they exist only in **three EPA Qlik Sense dashboards** (`awsedap.epa.gov`, anon `public`
     virtual proxy). We reverse-engineered the anonymous **Qlik QIX WebSocket** and pull the whole panel
     (106 pages → 105,168 rows, ~30 s). Tiny → **pull the whole thing weekly**; no subsetting. The
     **official artifact** = the model-code ZIP at the DOI (33 KB, HTTP, sha-pinned).
  4. **Geotagging:** **`COMID` (NHDPlus V2)** on every lake `[probe]` + centroid lat/lon + State/Region
     → joins by identity to `EPA-NARS`/`WQP`/`NWIS`/LakeCat/NLDI (same backbone as those modules).
- **User decisions (this session):** (1) role = **document to support ALL roles** (benchmark / feature /
  context), defer the framing; (2) extraction = **scripted QIX pull + WEEKLY SNAPSHOT** (accumulate the
  history the dashboard's rolling ~2-season window discards), documented honestly as unofficial/fragile.
  (3, **added by user mid-build**) **document the "solid baseline to judge against / leverage" finding in
  BOTH the module docs AND the higher-level deliverable docs** → new
  `../docs/plans/2026-07-02-epa-cyano-forecast-as-baseline.md` + cross-ref in the slides-design doc.
- **Codex design review BEFORE build (user-requested): 8 must-fixes + MED/LOW, all folded in.**
  1. (blocker) **Unofficial QIX not defensible alone** → research surfaced the **official DOI code +
     data.gov record + paper**; adopted a **two-tier** design (official science anchor + explicitly
     unofficial live-values tier) + EPA escalation contact (Schaeffer). METADATA §7/§12.
  2. (blocker) **Provable completeness** → fail-closed contract: `ClearAll` → read `qSize.qcy` → page →
     **assert exact row count** (verified 105,168). 3. (blocker) **App-state contamination** → mandatory
     `ClearAll`, record selection state, pull only canonical `AllWeeks` apps (not app1's default-week view).
  4. (high) **Destructive dedup would erase revisions** → append-only immutable snapshots +
     `(COMID,WeekEndDate)` current view + **revision table**. 5. (high) **Thin manifest** → full
     provenance (engine/single URLs, appid, vproxy, object def, field order, selection state, qSize, page
     geometry, sha256, client version). 6. (high) **QA hard-coded shape** → split **live-snapshot QA**
     (tolerance vs probe baseline) from **archive QA** (shape-agnostic). 7. (high) **Leakage policy** →
     METADATA §9: benchmark/context default, **never a CyAN-model label**, feature only as-of, always vs
     persistence/climatology w/ temporal blocking. 8. (high) **Baseline/uncertainty on skill** → recorded
     EPA point estimates (AUC 0.95, acc 0.90 vs 0.84–0.85 ML baselines, sens 0.88, spec 0.91,
     **precision 0.49**, base rate ~9–10%), **no CIs**, labeled EPA-reported not repo-validated.
     MED/LOW: dual-date→ISO + Saturday assert; stable-coords-per-COMID; cross-app consistency mode;
     offline QIX fixture+tests; predeclared sentinel + peak-week rule (no cherry-pick); diagnostic-labeled
     summaries.
- **Built + validated end-to-end (2026-07-02, Py3.13 win32):** `METADATA.md` (14-section) +
  `reference/PRIMARY-SOURCES.md` (verbatim + probe log) + cached EPA pages + official README + QIX
  fixture; `access/qlik_public.py` (fail-closed QIX client) + `pull_forecasts.py` (snapshots+revisions)
  + `pull_official.py`; `qaqc/qa_forecasts.py`; `viz/viz_forecasts.py`; `tests/` (5 offline tests green).
  **Full snapshot = 105,168 rows, 0 QA flags, two canonical apps agree exactly; official ZIP
  sha-verified.** Native peak-week map is scientifically sensible — HAB hotspots (Upper Midwest/N.
  Plains, FL chains, **Grand Lake St Marys OH 99%**) light up; arid West low (visual sanity check passed).
  `websocket-client==1.9.0` pinned; `.gitignore` already covers `raw/`+`derived/`+`*_map.html`.
- **Honest limits recorded:** unofficial/fragile access (pin app IDs; fails loud on change); **rolling
  window — 2024 beta season already gone** (need our snapshots for history); model **over-predicts**
  (precision 0.49); resolvable-area blind spots; **2,191 delivered vs 2,192 advertised** (flagged);
  COMID is dashboard-added (validate vs NHDPlus before load-bearing joins); **correlation≠causation**;
  and the **CyAN-derived circularity** that gates its use as a label.
- **Higher-level finding (per user):** the forecast is a **validated federal baseline** → our Part-A
  model can be **judged against it** (in addition to naïve baselines) or **leverage it as a signal**;
  matches the deck's "established-operational" quality tier for the EPA 7-day forecast [ACAD-050].

## 2026-07-02 — Weather layer (ERA5 + ECMWF forecast) review + build (session 8)
- **Thorough review of ERA5 (history) + ECMWF open-data forecasts (operational)** from primary sources +
  **live probes** → answered the five onboarding questions:
  1. **Restrictions:** both **CC-BY-4.0** (ERA5's Copernicus licence flipped to CC-BY on **2025-07-02**; ECMWF
     open data CC-BY-4.0). Free to use/redistribute/**commercialize** with **attribution** (a licence condition,
     unlike our US-federal public-domain sources). ERA5 also needs **accept-terms-once** per dataset. Earthmover is
     a paid vendor layer over the same CC-BY data.
  2. **Features/consistency:** ERA5 single-levels (2t, tp, 10u/10v, msl, ssrd, 2d, runoff, soil…), hourly,
     1940→present, **internally homogeneous** (its key strength). ERA5-Land (0.1°) is finer for hydrology but a
     different grid. Forecasts carry the same vars but are **not temporally homogeneous** (IFS upgrades: TCo1279
     Jun-2023, Cy49r1 Oct-2024). ERA5T tail (`expver=5`) is preliminary/revisable.
  3. **API — operational vs bulk:** forecast open-data pull is **easy/fast/no-auth** for the *latest run*; ERA5 CDS
     is **queued/throttled** (bounded pulls fine, heavy pulls penalized). Bulk ERA5 → free **ARCO-ERA5 Zarr** (lazy
     cloud read, no mirror). ⚠ **open data keeps only ~2–3 days of runs — no forecast history** (capture or MARS).
  4. **Geotagging:** both are **plain 0.25° lat/lon grids — NO watershed/HUC/COMID IDs** (unlike NARS/WQP/NWIS).
     Watershed linkage is ours to build via WBD overlay (area-weighting = opt-in aggregation); lake linkage via
     nearest-cell/bilinear.
  5. **Reconciliation:** ERA5 single-levels 0.25° **↔ forecast 0.25° share the identical mesh** (no regrid); reconcile
     cadence (hourly vs 3/6-hourly → daily), **de-accumulate forecast `tp`** (accumulated-from-start) vs ERA5 hourly,
     normalize GRIB/GRIB2→xarray, and **bias-correct the forecast to ERA5 climatology** (MOS). See `weather/METADATA.md §6`.
- **User decisions (this session):** (1) ERA5 product = **single-levels 0.25° only** (aligns cell-for-cell with the
  forecast grid); (2) access = **bounded CDS pulls** (scripted/cached/manifested, matching CyAN/NARS/WQP/NWIS), ARCO
  documented as the bulk alternative; (3) forecasts = **build the operational pull now**; (4) scope = **western Lake
  Erie basin, 2008→present** (matches CyAN tile `7_2` + WQP Maumee HUC8 `04100009`).
- **Built + validated (live probes 2026-07-02, Py3.13 win32):** installed `cdsapi==0.7.7` / `ecmwf-opendata==0.3.30`
  / `cfgrib==0.9.15.1` / `eccodes==2.47.0`. **Forecast path validated end-to-end:** pulled the **2026-07-02 06z**
  `oper` run via `access/ecmwf_forecast.py` (5 params × 4 steps → one **13.2 MB** GRIB2, sha256-manifested) → decoded
  (**721×1440 @ 0.25°**, lon −180..179.75) → `qaqc/qa_weather.py` (integrity verified, 0 flags; `t2m` 292–303 K,
  `tp` accum flagged) → `viz/viz_weather.py` native per-cell map (coherent warm band). **ERA5 path built** with a
  no-auth `--dry-run` verified; **live pull pending the CDS key** in `../.env` (+ one-time licence accept).
- **Docs:** `weather/METADATA.md` (11-section, every claim cited + access-dated, `[probe]`-marked), `weather/README.md`
  (run-guide), `weather/reference/PRIMARY-SOURCES.md` (verbatim quotes + probe log). Registry rows `era5`+`ecmwf_fc`
  added; `noaa_ncei` annotated as complementary station obs. `.gitignore` += `*.grib*`/`*.idx`; deps pinned.
- **Honest limits recorded:** 0.25° (~28 km) is coarse for a single lake (ERA5-Land is the v2 option); ERA5T revises;
  forecast archive is ephemeral + version-seamed; reanalysis≠observation (convective precip caveat); **correlation≠
  causation** on weather→bloom. Leakage policy = as-of joins + blocked spatial/temporal splits (mirrors WQP §9).
- **✅ RESOLVED — CDS key configured + ERA5 live-validated (2026-07-02).** `CDSAPI_URL`/`CDSAPI_KEY` set in `../.env`
  (gitignored; `cdsapi` reads them via `_common/net.load_dotenv`), ERA5 dataset licence accepted. Smoke-test pull
  (Aug 2022, 7 core vars, W. Lake Erie 12:00) ran **accepted→running→successful in ~14 s** → 1.8 KB GRIB, decoded to
  a native **7×11 @0.25°** crop over lat 41.0–42.5/lon −84.5–−82.0, QA integrity verified, **0 flags**. **Both weather
  paths now 🟢 live.** (Token was pasted in chat → flagged to the user to regenerate if privacy is a concern.)
- **Next:** the daily-driver reconciliation (de-accumulate → daily → bias-correct) + the leakage-safe as-of join to
  CyAN; optionally a scheduled `ecmwf_forecast.py` capture to accrue a forecast archive.

## 2026-07-01 — NWIS onboarding: review + OGC-first client + QA (session 7)
- **Thorough review of USGS NWIS** (primary-source docs + **live API probes**) → answered the three onboarding
  questions. **Restrictions:** U.S. Public Domain (credit "U.S. Geological Survey"); provisional data *"subject to
  revision"*, no-warranty/liability disclaimer; **no auth**. **Features:** small consistent core (discharge/stage at
  streamgages) + a long **site-variable** tail (temp, SC, DO, pH, turbidity, nitrate sondes); continuous ~5 min &
  daily; provisional→approved lifecycle; **discontinued series are real** (read the per-site catalog). **Geotagging:**
  lat/lon (NAD83), **HUC-8…HUC-12**, FIPS, drainage area; site id **is** the WQP `USGS-<siteno>` (exact 1:1 join);
  NARS links **spatially by HUC** (no shared id).
- **⚠ MAJOR finding — legacy `waterservices` is decommissioned early 2027.** Decision (user): **build on the new
  Water Data OGC API** (`api.waterdata.usgs.gov/ogcapi/v0`); keep only thin `legacy_*` cross-check helpers.
- **Build scope (user): METADATA + access + QA/QC** (defer viz — NWIS is a feature/context source, not the target).
- **Variables (user):** full HAB set — hydrology (00060/00065) + temp (00010) + WQ sonde (99133/00095/00300/00400/63680);
  **daily = modeling core**, continuous available. **Geo scope (user): general/national-capable** — AOI-parameterized
  (HUC/bbox/state/site-ids), **no pinned study region**; per-AOI subset, **never mirror** (~1.9M sites).
- **Design = catalog-driven pull.** Data collections (`daily`/`continuous`) filter by **site only** (no HUC/bbox —
  verified); `time-series-metadata` **does** accept AOI filters (`hydrologic_unit_code`/`state_name`/`parameter_code`
  — verified keyed 2026-07-02, corrected post-Codex from an earlier keyless probe that wrongly read empty). We still
  enumerate sites (monitoring-locations) → catalog **per enumerated site** (set already narrowed by the `--max-sites`
  guard; uniform across AOI types) → pull only series that exist → tidy row-per-obs CSV + sha256 manifest (records
  `approval_status` split, `last_modified`, `ogc_build_version`). Concurrency = **thread-local** sessions, default 4
  workers. (AOI-wide catalog via `hydrologic_unit_code` is documented as the efficient alternative for whole-HUC pulls.)
- **Empirically discovered & handled quirks (all fed back into code/docs):** (1) **keyless rate limit = 1000 req/hr**
  → HTTP 429 + `Retry-After`; client **does not blind-retry 429** (would burn quota + hang) — raises `RateLimitError`;
  key optional via `X-Api-Key`. (2) **Site-id filter differs by collection** (`monitoring-locations`→`id`;
  data→`monitoring_location_id`; comma-lists 400). (3) **A HUC-8 returns ~1,903 sites incl. 1,565 GW wells** →
  added a **--max-sites guard** that refuses runaway fan-out (narrow with `--site-types`). (4) Stalled keyless sockets
  → short read timeout + `read=0` retry so one bad request fails fast instead of hanging minutes. (5) UTF-8 console
  + dedup plan by (site,param,stat).
- **Validated end-to-end (2026-07-01/02):** 2 Potomac gages daily discharge+temp 2020–2024 → 4 series, sensible
  ranges (discharge 450–102k ft³/s; temp 0–32 °C), 0 QA flags, sha-manifested; AOI enumerate/guard/catalog-plan on
  HUC-8 (lakes correctly show 0 continuous series — they live as discrete samples in WQP).
- **✅ RESOLVED — API key configured + keyed multi-site validated (2026-07-02).** `NWIS_API_KEY` set in `../.env`
  (gitignored, `X-Api-Key` header). Keyed **20-site HUC-8 AOI pull** (discharge+temp+SC, 2015–2024) ran cleanly in
  **seconds** (vs keyless throttling/stalls) → catalog-driven plan of 9 series, 8 pulled + 1 correctly-empty, **0
  failed**; combined QA over **12 series / 8 sites = 0 flags**, real qualifier flags surfaced (ICE/ESTIMATED/EQUIP/
  FLOOD/REVISED), and the site-variable/discontinued-series story visible in data (2 sondes 2016–2020 vs long
  discharge records). METADATA §0 now carries a **⚡ QUICK API ACCESS** block for future instances.
- **✅ Codex-reviewed (2026-07-02), findings applied.** No blockers. Fixed/hardened: (1) `iter_items` now validates
  the 2xx body is well-formed OGC JSON (`OGCResponseError` vs silent zero-rows on an HTML gateway body); (2) worker
  threads use **thread-local `requests.Session`s** (a shared Session isn't a safe concurrency boundary); (3) catalog
  failures now count → **nonzero exit** unless `--allow-partial` (no silent incomplete AOI); (4) empty series get an
  `series_empty` manifest record (reproducibility). **Doc-accuracy corrections:** `monitoring-locations` site filter
  is `id`/`monitoring_location_number`, **not** `monitoring_location_id` (per queryables); `time-series-metadata`
  **does** support AOI filters (corrected the "site-only" claim); "key configured" reworded to be clone-portable
  (`.env` is gitignored → a fresh clone has none); QA's `active` renamed **`recent_in_pulled_window`** (it reflects
  the pulled window, not live catalog activity). Re-tested named-site + 20-site keyed AOI pulls → still 0 QA flags.

## 2026-07-01 — WQP onboarding: review + design, Codex-reviewed (session 6)
- **Thorough review of the Water Quality Portal** (primary-source docs + **live REST probes**) → answered the
  three onboarding questions. Restrictions: essentially public-domain (liability disclaimer + provisional caveat;
  DOI `10.5066/P9QRKUVJ` citation), no hard rate limits. Features: heterogeneous "characteristics" that vary by
  site/org (no guaranteed panel); Summary service = cheap per-site availability/recency discovery. Geotagging:
  lat/lon+datum + HUC8 (HUC8+**HUC12** in WQX3); **NWIS linkage trivial** (`USGS-<id>` shared key) and **NARS
  submits into WQP** as org `NARS_WQX` (shared key) **[probe]**.
- **MAJOR finding — the 2024-03-11 USGS split + dual schemas.** Legacy **WQX 2.2** has **no USGS data added *or
  modified* after 2024-03-11**; fresh USGS data is **WQX 3.0 beta** only. WQX3 is backward-compatible (re-serves
  old submissions) while 2.2 continues → a **blind union double-counts**.
- **User decisions (this session):** (1) target = **DUAL** (ingest legacy + WQX3, reconcile); (2) tooling =
  **HYBRID** (`dataretrieval` for discovery/cross-check, our `_common/net.py` raw-REST for canonical cached+
  manifested pulls); (3) parameter scope = **DISCOVERY-FIRST** (Summary discovery → then choose characteristics
  from real availability). Start scope = western Lake Erie basin (Maumee HUC8 `04100009` + Lucas County OH + OH/MI)
  to fuse with CyAN tile `7_2`; scripts parameterized to widen to CONUS.
- **Cross-dataset note (sibling `EPA-NARS/` + `NWIS/` onboarded in parallel, session 5):** NARS data now lives in
  **two places** — standalone `EPA-NARS/` CSVs **and** inside WQP as org `NARS_WQX`. ⚠ **Double-source caution:**
  do not count NARS twice when fusing WQP + EPA-NARS; pick one as canonical for NARS records (EPA-NARS carries the
  richer NHD/WBD keys — COMID/REACHCODE/HUC — so prefer it for NARS, and treat WQP's `NARS_WQX` as a cross-check).
  NWIS is likewise re-served inside WQP (`USGS-<id>`); the standalone `NWIS/` dataset is for hydrology
  (streamflow/gage), WQP for discrete chemistry — same site keys link them.
- **Codex review (task-mr2oyi9a-ruuf46, GPT-5): 15 findings; every verifiable one confirmed by our own probe.**
  Folded in:
  1. (blocker) **No blind union** → canonical reconciliation key (schema+org+location+activity+result id, fallback
     content hash) with **WQX3-preferred-for-USGS**; log kept-vs-dropped. Prevents label corruption + split leakage.
  2. (blocker) **DQL profile is a first-class pull** (via `narrow` + `ResultIdentifier`; multiple per result) →
     explicit censoring state, **no imputation** before modeling. `ResultMeasureValue` is a string (`"NA"`≠0). **[probe]**
  3. (high) **Analyte feature keys**, not names: characteristic+pCode+fraction+unit+method/speciation+basis+media+
     depth → human-reviewed dictionary. WQX vs USGS naming differs (DO vs "oxygen").
  4. (high) **CyAN-join leakage policy documented now**: as-of joins; blocked spatial (site/HUC) + temporal splits.
  5. (high, **probe-flipped a design detail**) **`/wqx3/summary` returns 404** — WQX3 has no Summary service.
     Discovery = **legacy Summary (broad) + WQX3 Station/Result freshness probes**.
  6. (high) 2024-03-11 split covers **modifications**, not just new rows → prefer WQX3 for full USGS record +
     revision-delta check.
  7. (high) Coordinates: WGS84 filters vs NAD83 UI; station vs **activity** coords; keep datum/accuracy; reproject
     explicitly. 8. (high) **Predeclared inclusion rules** before feature selection (anti result-shopping).
  9. (med) "every column renamed" softened → validate per-profile vs EPA's published WQX3 schema + legacy crosswalk.
  10–15. characteristic discovery via groups+pCodes+alias tables; operationalize revision churn (query/headers/
     hashes/status + report); provider-specific freshness (**NWIS 24h / WQX Thu weekly**, verbatim); `dataretrieval`
     = cross-check only (not a 2nd canonical path); NARS linkage labeled "probe-verified, not doc-verified" + add
     org-code discovery; explicit **Water + lake/reservoir/stream** media/site filters (report excluded counts).
- **Built the "document-before-you-pull" foundation:** `WQP/METADATA.md` (10-section, all findings cited + access-
  dated), `WQP/README.md`, `WQP/reference/PRIMARY-SOURCES.md` (verbatim quotes + probe log), folder scaffold.
  **Next:** `access/` (discovery-first), then `qaqc/` (reconcile/dedup + censoring + revision report), then `viz/`.

## 2026-07-01 — Onboarded EPA NARS / National Lakes Assessment (`nars_nla`, session 5)
- **Scope = NLA only** (National Lakes Assessment: lakes 2007/2012/2017/2022) — the HAB-relevant NARS
  survey. Built the `EPA-NARS/` folder/framework so NRSA/NCCA/NWCA can be added later with the same
  catalog→pull→QA→viz pattern. (User decision.) Worked-example pull = **NLA 2022 only** (~33 MB);
  the pull script supports all cycles via `--cycle`.
- **Full cyan-style onboarding** built and verified end-to-end: `METADATA.md` (14 sections),
  `access/nars_catalog.py` (pinned URL manifest + filename parsers + live-page drift `reconcile`,
  13 unit tests green), `access/pull_nars.py` (cached, sha256-manifested, `--dry-run`/`--check-drift`/
  `--limit`, **no auth**), `qaqc/qa_nars.py` (integrity + header-vs-dictionary + distributions +
  join-key + geotag → `outputs/qa_report.md`/`.json`), `viz/viz_nars.py` (per-lake map + summary + PNG).
- **Access reality (answers the brief's feasibility Q):** NARS has **no REST API** — only static flat
  CSVs at stable `epa.gov` URLs + an interactive R-Shiny download tool. Archive is tiny → **decision:
  bulk-mirror locally, cache + sha256**, and diff the live page vs a pinned manifest to catch EPA's
  incremental re-publishing (drift check reported **clean**, 25 files matched, 2026-07-01).
- **License:** U.S. **public domain** by default (EPA disclaimers, 17 U.S.C. §105) — free to use/
  redistribute/commercialize; obligations are attribution (EPA recommended citation) + carry the
  no-warranty disclaimer. Real constraint is fitness-for-use (probability-survey design), not licensing.
- **Geotagging = the standout:** `siteinfo` carries the full NHD/WBD key suite — `COMID` (100%),
  `REACHCODE` (100%), `PERM_ID` (91%), `GNIS_ID` (100%), `HUC2`/`HUC8` (100%), lat/lon **NAD83**, and
  Omernik ecoregions — the same backbone as USGS NWIS/WQP. **Decision: document the WQP/NWIS/CyAN/
  LakeCat linkage design now (COMID→NLDI, HUC8, spatial, GNIS), implement/validate the join with the
  fusion analysis later.** Honest limit recorded: NLA lakes are polygons, NWIS is stream gages →
  linkage is watershed/catchment-based, not identity; NLA ships no direct station crosswalk.
- **Baked-in honesty (carried in QA + viz + docs):** (a) raw site file (3,880 rows / 3,784 lakes) ≠
  the published **981** probability lakes → national/regional %s require survey weights
  (`WGT_TP_CORE_NLA`; `WGT_DSGN` is explicitly *do-not-use*); (b) `NARS_FLAG=ND` is a **measured**
  non-detect (left-censored), never coerced to 0/NaN; (c) viz is **per-lake, native-coordinate,
  UNWEIGHTED** (no aggregation), labeled "not a national estimate".
- **Empirical validation vs prior Research:** raw unweighted microcystin detection **49%**,
  cylindrospermopsin **9.5%**, **28 lakes (2.3%) ≥ 8 ug/L** — consistent with EPA's weighted ~50% /
  ~12% / ~2% headline (Research FED-027/028). The microcystin map's high-toxin lakes cluster in the
  Upper Midwest/Northern Plains — the known nutrient-rich cyanoHAB hotspot (visual sanity-check passed).

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
