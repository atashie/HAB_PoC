# Weather (ERA5 reanalysis + ECMWF medium-range forecast) — Dataset Metadata

**Dataset short name:** `weather` — a paired layer of two products that share one 0.25° grid:
- `era5` — **ERA5 hourly single-levels reanalysis** (historical weather *truth*).
- `ecmwf_fc` — **ECMWF open-data IFS medium-range forecast** (the operational *extension into the future*).

**Product this file describes:** ERA5 `reanalysis-era5-single-levels` (CDS) + ECMWF open-data `oper`
(IFS medium-range control, ex-HRES) surface fields, both at 0.25° regular lat/lon.
**Version / processing level documented:** ERA5 (CDS, new store since 2024-09-26) + ECMWF open data as served on the date below; IFS cycle in force = Cy49r1 (operational since Oct 2024).
**Compiled:** 2026-07-02 · **Access date for all checks below:** 2026-07-02
**Compiled by:** Claude (Fable 5) with Arik Tashie. Every quantitative claim traces to a cited primary
source or an empirical check we ran on 2026-07-02. Facts confirmed by our own live probe (script + run,
not just docs) are marked **[probe]**. Ambiguities are flagged, not smoothed over.

> **AI-shaped-judgment flag (per `../../CLAUDE.md`).** The characterization below was drafted by an LLM
> from primary sources + live probes (installed `cdsapi`/`ecmwf-opendata`/`cfgrib`, pulled a live forecast,
> decoded it, QA'd + mapped it). A human should still spot-check the **reconciliation recipe (§6)**, the
> **accumulation handling (§4)**, and the **ERA5T provenance policy (§4/§11)** before backing any claim.

---

## 0. TL;DR for the modeler

| Question | `era5` (history) | `ecmwf_fc` (forecast) |
|---|---|---|
| What is it? | ECMWF reanalysis — a physically consistent, gap-free hourly estimate of past weather, 1940→present. | ECMWF IFS deterministic medium-range forecast (ex-HRES), free real-time "open data". |
| Native form / format | Gridded raster; **GRIB** (CDS also converts to NetCDF). ARCO copy exists as Zarr. | Gridded raster; **GRIB2** (one concatenated file per run). |
| Spatial resolution & extent | **0.25° regular lat/lon** (~28 km), global. (Native spectral T639 ~31 km, regridded.) | **0.25° regular lat/lon**, global. Same mesh as ERA5 **[probe]** (721×1440, lon −180..179.75). |
| Temporal span, cadence, gaps | 1940→present, **hourly**. Latency ~5 days (ERA5T) → final ~2–3 mo. No gaps. | Real-time. Runs **00/06/12/18 UTC**; steps 0–144 h (3-hourly) then 150–360 h (6-hourly) for 00/12. ⚠ **rolling archive ≈ last 12 runs (~2–3 days) only — no history.** |
| The value in a cell | One variable at one hour (e.g. 2 m temp K, total precip m). | One variable at one forecast step from one run. |
| Encoding / how to read | Instantaneous vs **accumulation** vars; `expver` 1=final, **5=ERA5T (preliminary)**. | Instantaneous vs **accumulation-from-forecast-start** (`tp`); GRIB2 keys. |
| Nodata / fill | Physical fields, generally complete over the globe; land/sea masks matter for land vars. | Same. |
| Access (auth) | **CDS API (`cdsapi`), account + token + accept-terms-once**; queued/throttled. | **`ecmwf-opendata`, NO AUTH** (CC-BY-4.0). 500 concurrent-conn cap; AWS/Azure/GCP replicas **[probe]**. |
| Bulk or subset? | **Subset** (region×vars×time) — global ERA5 is petabyte-scale. ARCO Zarr for bulk lazy reads. | Pull the **latest run** on demand (small). No bulk history to mirror; capture runs to build an archive. |
| Likely role | **Feature / driver** (temp, wind, precip, radiation) + the *truth* forecasts are scored against. | **Operational driver** for the Part B action-window; extends the driver series ahead of "now". |

**Three headline traps, read first:**
1. **The forecast archive is ephemeral.** Open data keeps only ~2–3 days of runs **[probe]**. You **cannot backfill**
   historical forecasts from it — for forecast-skill verification you must either capture runs going forward (a
   scheduled pull) or use ECMWF's paid archive (MARS). ERA5 supplies the *history*; open data supplies *today's* forecast.
2. **`tp` accumulation conventions differ.** ERA5 total precipitation is **de-accumulated to hourly**; forecast `tp`
   is **accumulated from forecast start**. Naively differencing them is wrong — de-accumulate the forecast to
   comparable increments before any ERA5↔forecast comparison (§4, §6).
3. **Reanalysis is homogeneous; forecasts are not.** ERA5 is one frozen system across 1940→present (ideal for
   training). The forecast model is **upgraded periodically** (resolution unified to TCo1279/9 km Jun 2023;
   Cy49r1 Oct 2024) → any self-captured forecast archive has version seams; log the IFS cycle.

---

## 1. What it is

**ERA5** is the fifth-generation ECMWF atmospheric **reanalysis**: observations from 1940→present assimilated
through a *single, fixed* forecast model + data-assimilation system to produce a physically consistent, gap-free
hourly reconstruction of the atmosphere, land surface, and ocean waves. Its defining property for us is
**internal homogeneity** — the same grid, variables, and physics across the whole record — which makes it a
sound training substrate and the natural "truth" against which forecasts are scored. Produced by ECMWF for the
EU **Copernicus Climate Change Service (C3S)**; distributed via the **Climate Data Store (CDS)**.

**ECMWF open-data forecasts** are the free, real-time subset of ECMWF's operational output: the **IFS**
(Integrated Forecast System) deterministic medium-range forecast (the `oper` stream, formerly "HRES") and
ensemble (`enfo`), plus the AI model **AIFS**, released under CC-BY-4.0 at 0.25°. This is the operational
"what happens next" layer — the same physical variables as ERA5, projected 10–15 days ahead.

Together they form one continuous driver series: **ERA5/ERA5T for the past → the latest IFS forecast for the
future**, on a shared 0.25° grid.

## 2. Temporal coverage, cadence & gaps

| Aspect | `era5` | `ecmwf_fc` | Source |
|---|---|---|---|
| Span | 1940 → present | Real-time only (rolling) | CDS dataset page; ECMWF open data |
| Cadence | **Hourly** | Runs 00/06/12/18 UTC; steps 0–144 h @3 h then 150–360 h @6 h (00/12); 06/18 to 144 h | ECMWF open data / Set-I |
| Latency | **ERA5T ~5 days**; final ERA5 ~2–3 months | ~hours (latest available run = **2026-07-02 06:00 UTC** at 2026-07-02 probe) **[probe]** | ERA5 docs; probe |
| Retention | Full archive kept | **~12 most-recent runs (~2–3 days), then dropped** | ECMWF open data |
| Reprocessing / version | ERA5T (`expver=5`) overwritten by final ERA5 (`expver=1`) ~2 months later; occasional stream fixes | IFS upgraded periodically (Cy49r1 Oct 2024) → forecast behavior/skill changes over time | ERA5 docs; IFS cycle notes |
| Gaps | None (reanalysis is gap-free) | None within a run; but no cross-run history in open data | — |

**Consequences we must handle:**
- The **last ~5 days→~3 months of ERA5 is ERA5T** — preliminary and revisable. Log `expver`; plan a refresh of
  recent windows (§11).
- **Forecast history is not retrievable** from open data. If we want to score forecast skill against ERA5, we
  must **capture runs as they publish** (scheduled `ecmwf_forecast.py`) or use MARS.
- A self-built forecast archive spans **IFS version changes** — record the cycle so skill trends aren't confounded
  by model upgrades.

## 3. Spatial characteristics & geotagging (watershed linkage)

- **Geometry:** both are **regular latitude/longitude grids**, cell-centered. ERA5 0.25° (native spectral T639
  ~31 km, MIR-regridded to 0.25°); forecast 0.25°. **[probe]** the forecast grid is 721 lat × 1440 lon, latitude
  90..−90, **longitude −180..179.75** (the −180..180 convention, *not* 0..360) — verified by decoding a live field.
- **They align cell-for-cell.** Choosing ERA5 *single-levels* (0.25°) over ERA5-Land (0.1°) was deliberate: it
  puts history and forecast on the **identical mesh**, so fusion needs no regridding (§6). (ERA5-Land is finer/
  better for local hydrology but would require regridding to the 0.25° forecast grid — documented as a future option.)
- **No watershed identifiers.** Unlike NARS/WQP/NWIS (which carry HUC/COMID natively), ERA5 and the forecast have
  **only lat/lon** — no HUC, no COMID, no reach. Any watershed association is *ours to construct*:
  - **To a HUC watershed:** spatial overlay against the USGS **Watershed Boundary Dataset** — either point-in-polygon
    (cell center → containing HUC8/HUC12) or **area-weighted aggregation** of the cells inside a polygon. ⚠ Area-
    weighting is *aggregation* → per the project rule it needs explicit per-case permission; **native grid is the default**.
  - **To a lake / CyAN pixel / monitoring site:** nearest-cell or bilinear interpolation from the 0.25° grid. Note
    0.25° (~28 km) is coarse for a single lake — a real limitation to state, and the reason ERA5-Land is on the
    table for a v2 driver layer.
- **Minimum reliable unit:** one 0.25° cell (~28 km). Sub-cell structure is not resolved.

## 4. Encoding & quality flags — EXACT values (authoritative)

- **Units (SI, GRIB):** 2 m temperature **K**; precipitation **m** (of water equivalent); wind components **m s⁻¹**;
  pressure **Pa**; radiation **J m⁻²** (accumulated). Convert intentionally (K→°C, m→mm, Pa→hPa) at a labeled step.
  **[probe]** decoded forecast `t2m` over Lake Erie = 292–303 K (≈19–30 °C, sensible early-July values); `msl` ≈
  1.01–1.02×10⁵ Pa; `tp` 0→0.022 m by +72 h.
- **Instantaneous vs accumulation** — the load-bearing distinction:
  - *Instantaneous* (`2t`, `10u`, `10v`, `msl`, `2d`): the value at the valid time. **[probe]** GRIB `stepType=instant`.
  - *Accumulation* (`tp` total precip, `ssrd` solar radiation, `ro` runoff, `e` evaporation): a running total.
    - **ERA5:** accumulations are **de-accumulated to the hour** ending at the valid time.
    - **Forecast:** `tp` is **accumulated from forecast start** (step 0 = 0). **[probe]** GRIB `stepType=accum`, and
      the QA saw `tp` rising monotonically 0→0.022 m across steps 0,24,48,72. **De-accumulate** (difference
      successive steps) before comparing to ERA5 hourly precip.
- **ERA5 provenance flag — `expver`:** `expver=1` = **final ERA5**; `expver=5` = **ERA5T** (preliminary, last
  ~5 days→~2 months). In GRIB the header carries it; in **NetCDF you cannot tell them apart** unless a single
  request straddles both (then an `expver` dim appears). This is why `era5_cds.py` defaults to **GRIB**. A request
  over a recent window can return a *mix* (e.g. 00–06 UTC final + 07–23 UTC ERA5T on the boundary day).
- **Nodata / masks:** atmospheric fields are globally complete; land-surface variables carry a land–sea mask (over
  ocean they are undefined/fill). Forecasts: no missing over the domain. Read a real file's mask, don't assume.
- **Forecast has no `expver`** — provenance = (run datetime, IFS cycle, stream, step). **[probe]** QA reported
  `expver: (none)` for the forecast file; record the run datetime + cycle instead.

## 5. Known issues & limitations (the honest list)

- **Coarse for a single lake.** 0.25° (~28 km) smooths local land/lake contrasts; a lake smaller than a cell is
  represented by its cell's blend. ERA5-Land (0.1°) mitigates but adds a regrid.
- **ERA5T is preliminary** (§4) — recent weeks can change on final release.
- **Forecast archive is ephemeral** (§2) — no built-in history; skill verification requires captured runs or MARS.
- **Forecasts drift with lead time and carry model bias** — not a bias-free observation; treat as a *forecast*,
  bias-correct against ERA5 climatology before fusing (§6).
- **Forecast model version seams** (§2) break temporal homogeneity of any captured archive.
- **Reanalysis ≠ observation.** ERA5 is a model-obs blend; it is excellent but can be biased for convective
  precipitation and in complex terrain / near coasts. State this where precip drives a claim.
- **CC-BY, not public domain.** Unlike our US-federal sources, **attribution is a licence condition** (see §8) —
  carry it on every derived artifact (slides, tool, figures).
- **CDS throttling** (§7) makes large historical pulls slow; keep requests bounded.

## 6. Reconciling ERA5 history ↔ ECMWF forecast (the fusion recipe)

The goal is **one continuous, comparable driver series** — ERA5/ERA5T for the past, the latest IFS forecast ahead —
so a HAB model trained on history can be *served* on a forecast without train/serve skew.

| Axis | `era5` | `ecmwf_fc` | Reconciliation step |
|---|---|---|---|
| **Grid** | 0.25° reg. lat/lon | 0.25° reg. lat/lon **[probe]** | **Already identical** — same 721×1440 mesh, −180..180 lon. No regrid. (ERA5-Land 0.1° *would* need one.) |
| **Cadence** | Hourly | 3-hourly → 6-hourly | Resample to a common step. **Daily** aggregates (daily mean temp/wind, daily precip sum) are the natural HAB cadence — an explicit, labeled aggregation step (needs sign-off per project rule). |
| **Latency / seam** | Final ~2–3 mo; ERA5T ~5 days | Real-time | ERA5(+ERA5T) fills up to ~now; the forecast covers now→+10 d. Stitch at "now": last ERA5T hour → forecast step 0. |
| **Container / chunking** | GRIB (CDS) / NetCDF / Zarr (ARCO) | GRIB2, one file per run | Normalize both to xarray on ingest; write a common analysis store (NetCDF/Zarr) keyed by (var, valid_time, lat, lon). |
| **Variable names** | CDS long names (`2m_temperature`, `total_precipitation`, …) | short names (`2t`, `tp`, …) | Maintain an explicit crosswalk (in `era5_cds.py::CORE_VARIABLES`): `2m_temperature↔2t`, `total_precipitation↔tp`, `10m_u/v_component_of_wind↔10u/10v`, `mean_sea_level_pressure↔msl`, `surface_solar_radiation_downwards↔ssrd`, `2m_dewpoint_temperature↔2d`. |
| **Units** | SI (K, m, Pa, J m⁻²) | SI (same) | Same SI base — but convert to model units once, in one place. |
| **Accumulations** | precip de-accumulated to hourly | `tp` accumulated from forecast start | **De-accumulate the forecast** (difference successive steps) → per-interval increments, then aggregate to the common step. The #1 correctness gotcha. |
| **Systematic bias** | reanalysis (consistent) | model bias + lead-time drift | **Bias-correct / anomaly-standardize** the forecast against an ERA5 climatology (MOS-style: subtract the ERA5 mean seasonal cycle, optionally scale variance) so the forecast feature distribution matches what the model was trained on. **Validate** forecast skill vs ERA5-as-truth at each lead time. |
| **Provenance** | `expver` 1 vs 5 | run datetime + IFS cycle | Carry provenance columns on every derived row; treat ERA5T tail as provisional. |

**Recommended pipeline:** (1) shared 0.25° grid + shared variable set present in both; (2) harmonize names/units +
**de-accumulate** forecast precip/radiation; (3) resample to the common (daily) step; (4) bias-correct the forecast
to ERA5 climatology; (5) join to CyAN with a **leakage-safe as-of** rule (§10) — no future weather informs a past
prediction; blocked spatial (waterbody/HUC) + temporal (season/year) splits, never a random shuffle on
autocorrelated grids. **Correlation ≠ causation** on any weather→bloom association.

## 7. Bulk-download vs on-the-fly — the feasibility call

- **ERA5 — subset, don't mirror.** Global ERA5 is **petabyte-scale**; even one variable-year globally is large.
  For our bounded scope (western Lake Erie, a few drivers) CDS pulls are small. For *bulk* historical analysis the
  efficient path is the free **ARCO-ERA5 Zarr** on Google Cloud — read lazily with xarray, no multi-TB download
  (documented as the bulk option; our chosen access is bounded CDS pulls, §8 decisions).
- **Forecast — pull on demand.** One run of a few drivers is tens of MB **[probe]** (5 params × 4 steps = one
  **13.2 MB** GRIB2; a single field = **637 KB**). Trivial to fetch operationally; nothing to mirror. To retain
  history, **capture each run** (schedule the pull) since open data drops runs after ~2–3 days.
- **RAM** is never the bottleneck at this scope (one basin, per-run). Processing is per-file/per-step.

## 8. How to access it (verified 2026-07-02)

### 8.1 ERA5 via CDS API — `access/era5_cds.py`
- **Client:** `cdsapi` (installed **0.7.7 [probe]**; pulls `ecmwf-datastores-client`). New CDS (legacy
  decommissioned **2024-09-26**). Dataset id `reanalysis-era5-single-levels`.
- **Auth (required):** free CDS account → API key from https://cds.climate.copernicus.eu/how-to-api → `~/.cdsapirc`
  **or** `CDSAPI_URL`/`CDSAPI_KEY` in `../.env` (gitignored; loaded via `_common/net.load_dotenv`). **You must
  accept the dataset licence ONCE, manually, on the dataset page**, or `retrieve()` returns 403.
- **Throttling:** the CDS **queues** and penalizes large/heavy requests. Keep each bounded (small area, few vars,
  a year or two) and loop. Request format is `{product_type, variable, year, month, day, time, area:[N,W,S,E],
  grid:[0.25,0.25], data_format}`. **[probe]** `--dry-run` builds a valid request with no account.
- **Format:** default **GRIB** (keeps `expver`); NetCDF optional.

### 8.1b ERA5 **daily** statistics — `access/era5_cds.py --daily`
For a daily driver series (the natural HAB cadence, §6) prefer the derived
**`derived-era5-single-levels-daily-statistics`** dataset over aggregating hours yourself — it
is far smaller and native-daily. Key facts (**[probe] 2026-07-02**):
- **Per-variable statistic:** accumulated fields (`total_precipitation`, `surface_solar_radiation_downwards`,
  runoff, evaporation) require **`daily_sum`**; instantaneous fields (`2m_temperature`, `10m_u/v`) use
  **`daily_mean`**. `era5_cds.py --daily` splits the request into these two groups automatically.
- **Output = NetCDF** (a single `.nc` for one variable, a **`.zip` of per-variable `.nc`** for several) — the
  client handles both and manifests each `.nc`. (This dataset does **not** offer GRIB, so no `expver` tag —
  provenance is the request + access date.)
- **⚠ Slow:** the server **computes the aggregation on demand** — a one-month Florida request ≈ 1 min, but a
  full year is several minutes. **Loop per year; prefer a background run** for multi-year spans.
- **Separate licence:** it is a distinct dataset → **accept its Terms of Use once** on its own CDS page.
- **Size is tiny:** Florida (27×31 cells) daily = ~78 KB per variable-month → the full 5-variable
  **2016→present** set ≈ **~50 MB** (worked example, §11).
- **Known issue (upstream):** CDS currently flags `maximum/minimum_2m_temperature…`, `10m_wind_gust…`, and
  `maximum/minimum_total_precipitation_rate…` as unreliable — *we do not request those*; `daily_mean`/`daily_sum`
  of the core fields are unaffected. (See the CDS forum announcement.)

### 8.2 ECMWF forecast via open data — `access/ecmwf_forecast.py`
- **Client:** `ecmwf-opendata` (installed **0.3.30 [probe]**). **No auth.** `Client(source="ecmwf")`;
  `.latest(**req)` resolves the newest run, `.retrieve(target=..., **req)` downloads. **[probe]** latest `oper`
  run at probe time = **2026-07-02 06:00 UTC**; one `retrieve` writes **all** requested (param×step) fields into
  **one** GRIB2 file; the client prints the CC-BY-4.0 attribution notice on download.
- **Limits:** 500 simultaneous connections; replicated on **AWS / Azure / GCP** (`source="aws"|"azure"|"gcp"`) if the
  primary is busy. **[probe]**
- **Reading GRIB:** `cfgrib` (**0.9.15.1**) + `eccodes` (**2.47.0**) — binary wheels install cleanly on Python 3.13
  win32 **[probe]**; `cfgrib.open_datasets()` handles the multi-hypercube file.

### 8.3 Bulk / alternative (documented, secondary)
- **ARCO-ERA5** (Google Cloud public Zarr, free): `gs://gcp-public-data-arco-era5` — cloud-optimized ERA5 for lazy
  xarray reads; 0.25° ARCO analysis-ready copy, monthly updates ~3-month lag. Best for *bulk* history without a mirror.
- **Earthmover Icechunk-ERA5** (commercial): a daily-updating hosted ARCO cube. Convenient but a **paid vendor
  dependency, no public pricing** — heavier than a PoC needs; the free CDS + ARCO paths cover the same need.

### 8.4 Ancillary
- USGS **Watershed Boundary Dataset (WBD)** HUC polygons for the grid→watershed overlay (§3).
- ECMWF open-data parameter list / IFS cycle notes for available fields per stream.

## 9. Sources (all accessed 2026-07-02)
1. **ERA5 CDS dataset page** — https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels (resolution, hourly, 1940→present, GRIB, CC-BY).
2. **ERA5: data documentation (ECMWF Confluence)** — https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation (T639/regrid, ERA5T `expver` 1/5, accumulations).
3. **CDS API how-to** — https://cds.climate.copernicus.eu/how-to-api (`cdsapi`, key, accept-terms-once).
4. **New CDS / legacy decommissioned (2024-09-26)** — https://forum.ecmwf.int/t/goodbye-legacy-climate-data-store-hello-new-climate-data-store-cds/6380
5. **Licence: CC-BY replaces Licence-to-use-Copernicus (2025-07-02)** — https://forum.ecmwf.int/t/cc-by-licence-to-replace-licence-to-use-copernicus-products-on-02-july-2025/13464 ; licence text https://cds.climate.copernicus.eu/licences/licence-to-use-copernicus-products
6. **ECMWF open data** — https://www.ecmwf.int/en/forecasts/datasets/open-data (0.25°, GRIB2, CC-BY-4.0, cycles/steps, rolling archive).
7. **`ecmwf-opendata` client** — https://github.com/ecmwf/ecmwf-opendata
8. **IFS medium-range (Set-I) + TCo1279 unification** — https://www.ecmwf.int/en/forecasts/datasets/set-i ; https://www.ecmwf.int/en/newsletter/176/earth-system-science/ifs-upgrade-brings-many-improvements-and-unifies-medium
9. **ERA5-Land** — https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land (0.1°, 1950→present, ~3-mo lag) — documented alternative.
10. **ARCO-ERA5 (Google)** — https://github.com/google-research/arco-era5 ; https://cloud.google.com/storage/docs/public-datasets/era5
11. **Earthmover** — https://www.earthmover.io/ (commercial Icechunk-ERA5).
12. **Live probes (2026-07-02)** — installed `cdsapi`/`ecmwf-opendata`/`cfgrib`/`eccodes`; pulled the 2026-07-02 06z `oper` run; decoded to a 721×1440 0.25° grid; QA + native map over W. Lake Erie. Reproducible via `access/` + `qaqc/` + `viz/`. Verbatim quotes + probe log: `reference/PRIMARY-SOURCES.md`.
13. **Attribution to reproduce (required, CC-BY):** "Generated using Copernicus Climate Change Service information [2026]" (ERA5) and "Contains ECMWF open data (IFS forecasts), CC-BY-4.0" (forecast).

## 10. Likely role in the SePRO HAB analysis

- **Feature / driver source:** air temperature (bloom-favoring warmth), wind (mixing / scum accumulation & transport),
  precipitation & runoff proxies (nutrient delivery, stratification), solar radiation (photosynthesis) — candidate
  covariates for CyAN-based HAB risk. ERA5 provides the historical driver series for training.
- **Operational extension:** the ECMWF forecast projects those drivers **ahead of "now"**, powering the Part B
  *action-window* readout (the brief's "right-water-body call two weeks early").
- **What it is NOT:** not an observation of the lake itself, not watershed-resolved, not causal. **Correlation ≠
  causation** — a warm-windless-week↔bloom association is not a treatment effect.
- **Leakage policy (mirrors WQP §9):** **as-of joins only** — no future weather (or forecast issued after the
  prediction time) informs a past label; **blocked spatial** (waterbody/HUC) + **temporal** (season/year) splits;
  never a random shuffle on autocorrelated grids; keep native valid-times + run datetimes on every derived row and
  report sensitivity to the join/aggregation window.

## 11. Reproducibility & version pinning (rules for this dataset)

- **Temporal bound for the HAB fusion = 2016→present.** We ingest ERA5 only from **2016 onward** — the
  OLCI-era CyAN period of record we fuse against (`cyan` OLCI POR **2016-04-24→present**). ERA5's full
  1940→present exists but is not needed; bounding here keeps the driver history aligned with the satellite label.
- **Daily-stats per-request COST limit (empirical, 2026-07-02).** The derived daily dataset rejects large requests
  with **HTTP 403 `{"title":"cost limits exceeded","detail":"Your request is too large, please reduce your
  selection."}`** — **3 variables × a full year fails; 1 variable × a year (or any × 1 month) succeeds.** This is a
  size limit, *not* a rate/auth limit, so retrying can't help. `era5_cds.py --daily` therefore requests **one
  variable per (year, variable)**, **fails fast** on a cost-limit 403 (retries only genuine 429/5xx), and
  **cache-skips** done `(var, year)` `.nc` files (resumable). Full Florida 5-var 2016→present = **55 requests**.
- **Scripted, cached, manifested.** `access/era5_cds.py` + `access/ecmwf_forecast.py` write a JSONL manifest
  (`data/raw/{era5,forecast}_manifest.jsonl`) with path, bytes, **sha256**, params/steps/area, source, licence, and
  UTC access time — every weather-driven number traces to exact bytes. `data/` is gitignored → **regenerates from code**.
- **Provenance recorded at QA.** `qaqc/qa_weather.py` re-verifies sha256, reads the **0.25° grid** from the file (not
  the filename), and records **`expver`** (ERA5 1 vs 5) / run datetime (forecast). Recent ERA5 windows (ERA5T) are
  provisional → **plan a refresh** once final ERA5 (`expver=1`) overwrites them (~2 months).
- **Forecast archive by capture.** Open data has no history → to retain forecasts, **schedule `ecmwf_forecast.py`**
  (one file per run, manifested); log the **IFS cycle** so version seams are visible.
- **De-accumulation is explicit.** Any precip/radiation differencing happens in a labeled derived step, never silently.
- **Aggregation is opt-in.** Grid→watershed area-weighting and time→daily rollups are explicit steps requiring
  sign-off (project rule); default outputs are native-cell / native-hour.
- **Determinism:** fixed request params, pinned deps (`../requirements.txt`: `cdsapi==0.7.7`, `ecmwf-opendata==0.3.30`,
  `cfgrib==0.9.15.1`, `eccodes==2.47.0`), scripted access — no manual steps except the one-time CDS licence accept.
- **Attribution travels with the data** (CC-BY) — carried in the manifest `license` field and required on every
  derived artifact.
