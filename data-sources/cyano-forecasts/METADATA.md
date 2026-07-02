# EPA Experimental CyanoHAB Forecast (INLA) — Dataset Metadata

**Dataset short name:** `cyano_forecasts`
**Product this file describes:** EPA's **experimental weekly 7-day cyanobacterial-HAB probability
forecast** for Sentinel-3-resolvable U.S. lakes (Schaeffer et al. 2024, *J. Environ. Manage.*
349:119518). One number per lake per week: the probability (0–100%) that the lake's satellite-
resolvable area will exceed a bloom threshold in the next 7 days.
**Version / processing level documented:** the **operational/beta** product as served on EPA's HAB
Forecasts dashboards, snapshot **2026-07-02** (dashboard span 2025-04-05 → 2026-06-27); plus the
**official archived model code** at DOI `10.23719/1529140` (deposited 2023, last-modified 2023-11-11).
**Compiled:** 2026-07-02 · **Access date for all checks below:** 2026-07-02
**Compiled by:** HAB PoC data-sources work. Every quantitative claim traces to a cited EPA/primary
source (URL + access date) **or** to an empirical check we ran (a `[probe]` script in `access/` /
scratchpad, regenerable via `qaqc/`). Ambiguities are flagged, not smoothed over. This source
required more reverse-engineering than our file-based sources, so the AI-assistance and
access-legitimacy caveats in §12 and §14 are load-bearing — read them.

> ⚠️ **Access is two-tier and the operational tier is UNOFFICIAL.** The *live forecast values* are
> published **only** through interactive EPA **Qlik Sense dashboards** — there is **no official REST/
> CSV/file API**. We extract them via the dashboards' anonymous **Qlik QIX WebSocket** engine: a
> **reverse-engineered, undocumented, not-EPA-supported** path (§7.2). Treat this module as a
> **research/benchmark ingestion**, not a production dependency. The *official, citeable* artifact is
> the **model code** at DOI `10.23719/1529140` (§7.1). Escalation for a supported feed: EPA contact
> **Blake Schaeffer (schaeffer.blake@epa.gov)**.

---

## 0. TL;DR for the modeler

| Question | Answer |
|---|---|
| What is it? | EPA's **experimental 7-day-ahead probability** that each resolvable U.S. lake will have a cyanobacteria-dominated bloom next week. A **model output**, not an observation. Bayesian **INLA** spatiotemporal model built *from CyAN + weather + lake morphology*. |
| Native form / format | A **per-lake-week table** (not a raster). Served only via 3 **Qlik Sense dashboards**; we extract the tidy table over the Qlik **QIX WebSocket**. |
| Spatial resolution & extent | **Per lake** (one probability for the lake's satellite-resolvable area), CONUS. **2,191 lakes** delivered `[probe]` (EPA advertises "2,192" — see §5). Lake centroid lat/lon + **COMID**. |
| Temporal span, cadence, gaps | **Weekly**, week-ending **Saturday**, **~April–November** season. Dashboard holds a **rolling ~2 seasons** `[probe]` (2025-04-05 → 2026-06-27 on 2026-07-02); **the 2024 beta season is already gone**. Not a long archive unless *we* snapshot weekly. |
| The value in a cell/record | `Percent_chance_of_cyanoHAB` = **0–100 probability** of exceeding the bloom threshold in the next 7 days. |
| Encoding / how to read a value | Bloom = **lake-wide median surface chlorophyll-a ≥ 12 µg/L with cyanobacteria dominance** (WHO Alert Level 1), over resolvable pixels. Probability is a modeled likelihood, **not** an intensity. |
| Nodata / fill / detection limit | **Rectangular panel, zero nulls** `[probe]`: every delivered lake has a value every delivered week. "Missing" only appears as weeks the dashboard hasn't published (off-season / future). |
| Access (search / download / auth) | **No official API.** Live values: anonymous **Qlik QIX** extraction (§7.2, unofficial). Model code: **HTTP** download of the DOI ZIP (§7.1, official, no auth). |
| Bulk or subset? (with size estimate) | **Pull the whole thing** — the entire panel is **105,168 rows ≈ a few MB** `[probe]`; the official code ZIP is **33 KB**. No subsetting needed. |
| Likely role (target / feature / mask / context) | **Benchmark / context by default** — a *validated federal baseline to judge our own model against, or to leverage as a signal.* **Never a ground-truth label** for our CyAN-derived models (circular — it is itself CyAN-derived). See the leakage policy in §9. |

---

## 1. What it is

EPA's **experimental cyanobacterial-HAB forecast** issues, once a week during the bloom season, a
**7-day-ahead probability** that each of ~2,192 Sentinel-3-resolvable U.S. lakes will exceed a
cyanobacteria-bloom threshold. It is the operational realization of **Schaeffer et al. 2024**
("Forecasting freshwater cyanobacterial harmful algal blooms for Sentinel-3 satellite resolved U.S.
lakes and reservoirs," *J. Environ. Manage.* 349:119518; open access at PMC10842250).

The model is a **hierarchical Bayesian spatiotemporal model** fit with **INLA** (Integrated Nested
Laplace Approximation): a **binomial logistic** response (bloom / no-bloom per lake-week) with a
**first-order temporal autoregressive (AR1)** term on the previous week's condition and a **spatial
random field** (SPDE mesh over lake centroids). Its predictors are themselves derived products
(§4/§13): the **CyAN** satellite cyanobacteria signal (antecedent state), **PRISM** precipitation,
a **random-forest-modeled lake surface-water temperature**, and fixed **lake morphology** (mean depth,
surface area). The official code README (preserved at `reference/INLA_CONUS_forecast-README.md`) lays
out the full workflow, including an **ice-mask step** that relabels ice-covered winter lake-weeks as
"no bloom" to balance the training set.

**Maturity: experimental / beta.** EPA launched a public beta in **July 2024**, paused, and **resumed
for 2025**; the dashboards and research page carry explicit "experimental," "should not replace
sampling," and "over-predicts positive events" disclaimers (§5, §12). It is a **published, peer-
reviewed, out-of-sample-validated federal product** (§13 metrics) — which is exactly why it is a
credible **baseline** — but it is *not* a finished operational commitment, and its access path is not
an official data feed (§7.2).

**It is distinct from the `cyan` dataset in this repo.** `cyan` is the CyAN **satellite CI_cyano
raster** (the observed signal). This is the **modeled forecast built on top of that signal**. Do not
conflate them; in particular, do not validate a CyAN-derived model against a CyAN-derived forecast and
call it independent (§9 leakage policy).

---

## 2. Temporal coverage, cadence & gaps

| Property | Value | Basis |
|---|---|---|
| Cadence | **Weekly**, one forecast per lake per week | EPA HAB Forecasts page |
| Week label | `WeekEndDate` = the **Saturday** ending the 7-day window (Sun–Sat) | `[probe]` (all 48 dates are Saturdays) |
| Season | **~April–November** (probabilities low in cold months, not published off-season) | EPA research page |
| Release day | **Tuesday or Wednesday** each week | EPA research page |
| Dashboard span (2026-07-02) | **2025-04-05 → 2026-06-27**, 48 week-endings | `[probe]` |
| Per-season weeks | 2025 = **35 weeks** (Apr 5 – Nov 29); 2026 = **13 weeks** so far (Apr 4 – Jun 27, in progress) | `[probe]` |
| Freshness | latest week (2026-06-27) was **~5 days** before access → **current, not stale** | `[probe]` |
| History retained | **Rolling ~2 seasons only.** The **2024 beta season is NOT in the dashboard** — history begins 2025-04-05. | `[probe]` |

**The rolling-window fact is the single most important temporal caveat.** The published product is a
*live, changing view*, not an append-only archive. To build any multi-season training/evaluation set,
**we must snapshot the dashboard weekly ourselves** and accumulate — which is the explicit purpose of
`access/pull_forecasts.py` (append-only snapshots + revision tracking, §7.2, §10). A source that
silently drops old weeks and can revise past ones is a versioning hazard; we handle it, not ignore it.

**Reprocessing / revision:** because the model is retrained iteratively (the paper describes weekly
retraining in the 2021 test year), a probability shown for a past week **can change** if EPA re-issues
it. We do **not** treat a changed value as corruption; we record it as a **revision** (§10).

---

## 3. Spatial characteristics

- **Unit = the lake (its satellite-resolvable area).** Each record is **one probability for one lake**
  for one week — there is **no raster grid** and no sub-lake spatial detail in the published product.
- **Count: 2,191 lakes delivered** `[probe]` (distinct `COMID` = distinct lake names = 2,191). EPA's
  pages advertise **"2,192"**; the one-lake gap is unresolved and flagged (§5).
- **Extent:** contiguous U.S. Centroids span the CONUS envelope; QA asserts CONUS bounds and
  per-COMID coordinate stability (§ QA).
- **Coordinates:** `Lat_centroid` / `Lon_centroid` = the lake **centroid** (decimal degrees). These are
  a single point per lake — **not** the lake polygon, and **not** the sampled area. For polygon-level
  work, join `COMID` to NHDPlus V2 `NHDWaterbody` (§11).
- **The "resolvable area" caveat (from EPA, verbatim-preserved):** the Sentinel-3 sensor does not
  resolve shallow edges, small embayments, or narrow arms; a lake's probability reflects **only the
  pixels the satellite sees accurately**. Blooms isolated in unresolved embayments can be under-counted;
  long/thin reservoirs may be represented by only their wide segments. This is a real spatial-
  representativeness limit, not a data error (§5).

---

## 4. Encoding & fields — EXACT values (authoritative, `[probe]`-verified 2026-07-02)

The canonical table is **`AllWeeks_CyanForecasts`** (present in dashboard apps `9727f5d1…` and
`c00e1007…`). Ten fields, one row per lake-week:

| Field | Type (Qlik tags) | Meaning / how to read |
|---|---|---|
| `Percent_chance_of_cyanoHAB` | numeric | **THE value.** Probability **0–100** of exceeding the bloom threshold in the next 7 days. A likelihood, **not** an intensity/concentration. Observed range [0, 99.98], mean ≈10. |
| `COMID` | numeric integer | **NHDPlus V2 lake id** — the join key (§11). 100% populated, no nulls `[probe]`. |
| `Lat_centroid`, `Lon_centroid` | numeric | Lake centroid, decimal degrees (lon negative in CONUS). |
| `WeekEndDate` | dual (`$timestamp,$date`) | **Saturday** ending the forecast week. A Qlik **dual** (numeric serial + display text) — normalize to **ISO `YYYY-MM-DD`** and assert Saturday cadence on extract. |
| `Date` | text | A secondary date/label string carried by the app (preserve raw; prefer `WeekEndDate`). |
| `Year` | numeric integer | Calendar year of `WeekEndDate` (derivable; we recompute and cross-check). |
| `State` | text | U.S. state postal code. |
| `EPA_region` | text/number | EPA administrative Region (1–10). |
| `Lake_name_for_public` | text | Public display name (may disambiguate same-named lakes, e.g. "Pleasant Lake (ME 1)"). |

**The bloom definition being predicted (authoritative, Schaeffer 2024 + EPA dashboard, verbatim in
`reference/PRIMARY-SOURCES.md`):** a **lake-wide median surface chlorophyll-a ≥ 12 µg/L with
cyanobacteria dominance** (WHO **Alert Level 1**), evaluated over the satellite-resolvable area, as a
**binary** weekly presence/absence. The forecast is `P(exceed | current & prior week)`.

**Panel shape (`[probe]`):** **105,168 rows = 2,191 lakes × 48 weeks, zero nulls** — a *perfectly
rectangular* panel (every delivered lake has a value for every delivered week). Value distribution over
the 105,168 lake-weeks: **164** exactly 0; **81,309** in (0,10%); **15,224** in [10,50%); **8,471**
≥50%; mean ≈10%, max 99.98% — heavily right-skewed (most lake-weeks are low-probability), which is the
expected shape given a ~9–10% bloom base rate (§13).

**App1 (`c98935c5…`) is different — do not pull from it.** It has a table named `Data` (same fields
minus `EPA_region`/`Year`) but **opens with a default single-week selection** `[probe]` (its
aggregations returned 1 week, not 48). Selections are app/session state in Qlik and would silently
truncate an extract. Our client pulls only from the canonical `AllWeeks` apps and **`ClearAll` first**
(§7.2).

---

## 5. Known issues & limitations (the honest list)

- **It is a model output, not an observation.** Every value is a prediction; errors are model errors.
  Do not treat a probability as measured truth for a lake.
- **It deliberately over-predicts positives.** EPA states the model "overpredicts positive events" and
  is tuned conservative (health-protective). The paper's holdout **precision is 0.49** (≈half of
  positive forecasts at the 0.10 cutoff are false alarms) against **sensitivity 0.88** and **false-
  omission-rate 0.01** (§13). Any use MUST carry this asymmetry; it is the defining behavior.
- **Resolvable-area blind spots** (§3): edges/embayments/narrow arms are under-seen; the probability is
  for the resolvable footprint only.
- **Rolling ~2-season window** (§2): the dashboard is not an archive; the 2024 beta season is already
  gone; past weeks can be revised. Long histories require our own weekly snapshots.
- **2,191 vs 2,192 lakes** `[probe]`: the delivered panel has 2,191 distinct COMIDs (all non-null,
  all uniquely named); EPA advertises 2,192. The missing lake is **not identifiable from the product
  itself**. Flagged, not smoothed; reconcile against EPA's resolvable-lakes list if it ever matters.
- **Training-set balancing via ice relabeling:** the official workflow relabels ice-covered winter
  lake-weeks as "no bloom" to balance classes (README). This is defensible but means the model's
  off-season behavior is partly a labeling choice, not purely learned — relevant if extending outside
  the Apr–Nov season.
- **Experimental / beta status:** methods, lake set, and even the dashboard structure can change with
  little notice; the access path is unofficial and fragile (§7.2, §12).
- **Predictor circularity for our purposes:** the forecast is built **from CyAN** (plus weather/
  morphology). Using it as a label or feature alongside our own CyAN features risks target leakage /
  circular validation (§9).
- **Correlation ≠ causation.** The model's internal associations (temperature, precipitation, prior
  state) are predictive structure, **not** demonstrated drivers, and must not be reported as treatment
  causation.

---

## 6. Bulk-download vs on-the-fly — the feasibility call

- **The live product is tiny → pull the whole thing, every time.** The complete panel is **105,168
  rows ≈ a few MB**; a full QIX extract reads all 106 pages in **~30 s** `[probe]`. There is no reason
  to subset by space or time — a weekly run captures the entire current dashboard.
- **The official code artifact is 33 KB** (a ZIP of R scripts; §7.1, §13) — trivially mirrored.
- **Decision: mirror both, locally and completely.** Snapshot the full `AllWeeks` table weekly
  (append-only, §10) and cache the official ZIP once (sha256). This is the opposite of `cyan`
  (hundreds of GB → subset): here bulk *is* the whole thing and the constraint is not size but the
  **fragility/legitimacy** of the operational access path (§7.2, §12).

---

## 7. How to access it (verified 2026-07-02)

Access is **two-tier**. Tier 1 is official and citeable; Tier 2 is the (unofficial) live-values path.

### 7.1 OFFICIAL tier — the archived model + the paper (no auth, HTTP)
- **Paper (primary method source):** Schaeffer et al. 2024, *J. Environ. Manage.* 349:119518,
  DOI `10.1016/j.jenvman.2023.119518`. Open access: `https://pmc.ncbi.nlm.nih.gov/articles/PMC10842250/`.
- **Official data/code deposit:** DOI **`https://doi.org/10.23719/1529140`** → EPA **ScienceHub** /
  data.gov record **`INLA_CONUS_forecast`** (U.S. EPA ORD). Single resource:
  `https://pasteur.epa.gov/uploads/10.23719/1529140/INLA_CONUS_forecast.zip` (**33,677 bytes**,
  `Last-Modified 2023-11-11`, `Content-Type application/zip`; sha256
  `126f7f3fd9f79bdb36083009f726ecbe2d9047b728b7ac95bb2498545cf84afb`) `[probe]`. **Contents = R source
  code only** (the model workflow; the README says input files are *not* included but are all publicly
  downloadable). License: **ScienceHub License** (`https://pasteur.epa.gov/license/sciencehub-license.html`).
  `access/pull_official.py` downloads + sha256 + manifests it. **This is the artifact any scientific
  claim about the *method* should cite** — it is official and reproducible.
- **Note the scope mismatch:** this deposit is the **paper-era code (2017–2021 study)**, *not* the live
  2025–present forecast values. It gives method transparency + a way to reproduce the approach; it does
  **not** contain the operational probabilities we ingest in Tier 2.

### 7.2 OPERATIONAL tier — the live forecast values (Qlik QIX, UNOFFICIAL)
The weekly probabilities are published **only** inside three EPA **Qlik Sense** dashboards embedded on
`https://www.epa.gov/habs/hab-forecasts` (host **`awsedap.epa.gov`**, Qlik Sense Enterprise on Windows,
anonymous **`public`** virtual proxy). **There is no official REST/CSV/file/ArcGIS endpoint** — verified
`[probe]`: `/hub/`, `/api/v1/apps`, `/sense/app/` all 302→forms-auth; only the published public apps
render anonymously. The page's "downloadable data" is an **in-dashboard Qlik export** for humans.

We therefore extract over the Qlik **QIX engine JSON-RPC WebSocket** — the same channel the dashboard's
own browser client uses. `access/qlik_public.py` implements a **fail-closed extraction contract**:
1. HTTP GET the public single URL → capture the anonymous **`X-Qlik-Session-public`** cookie.
2. Open `wss://awsedap.epa.gov/public/app/<appid>?Xrfkey=<16-char>` with header `X-Qlik-Xrfkey` +
   the session cookie + `Origin` (Qlik CSRF: xrfkey in query **and** header must match).
3. `OpenDoc` → **`ClearAll`** (drop any default selection state; record state before/after).
4. Create a straight-table **hypercube of exactly the 10 expected fields**; read `qSize.qcy`
   (rows) & `qSize.qcx` (cols) from the layout.
5. **Page `GetHyperCubeData`** in ≤10,000-cell pages (⇒ 1,000 rows × 10 cols) until **exactly `qcy`
   rows** are read; **assert** the count and fail closed on any short/over page.
6. Normalize (dual `WeekEndDate`→ISO, Saturday assert), write tidy CSV, close the socket.

⚠️ **This is reverse-engineered and undocumented.** It is not an EPA-supported API; it can break
whenever EPA re-publishes the app (pinned app IDs + virtual proxy will then need updating), and it must
be used respectfully (single small read per week, identifying User-Agent). See §12 for the
legitimacy/reputational framing and the official-feed escalation contact.

### 7.3 The three dashboard apps (`[probe]`, pin these IDs)
| appid | canonical table | rows | notes |
|---|---|---|---|
| `9727f5d1-11d5-4522-9a59-1835a1885159` | `AllWeeks_CyanForecasts` (10 fields) | 105,168 | **canonical pull target** |
| `c00e1007-19bc-48c1-9a93-2c6f54569778` | `AllWeeks_CyanForecasts` (+ `MaxYear` helper) | 105,168 | canonical; cross-check |
| `c98935c5-a660-41b9-b1c0-abe31e649bf7` | `Data` (+ `MaxWeekEndDate`) | 105,168 | **default single-week selection — do NOT pull** |

### 7.4 Ancillary
- **CyAN resolvable-lakes shapefile** (the lake universe + COMID backbone) — from the CyAN project /
  NHDPlus V2 `NHDWaterbody` (`COMID`); see the `cyan` and `EPA-NARS` modules for the same key.
- **PRISM** (precip), **NHDPlus/LakeCat** (morphology), and the **CyAN** signal are the model's inputs
  — all already covered or coverable by sibling modules (`cyan`, `weather`, `EPA-NARS`).

---

## 8. Sources (all accessed 2026-07-02)

1. **EPA — Cyanobacterial HABs Forecasting Research** (product description, disclaimers, 2,192 lakes,
   cadence) — https://www.epa.gov/water-research/cyanobacterial-harmful-algal-blooms-forecasting-research
   · cached `reference/cyanobacterial-hab-forecasting-research.html`.
2. **EPA — HAB Forecasts** (the dashboards; bloom definition; resolvable-area caveat; over-prediction
   disclaimer) — https://www.epa.gov/habs/hab-forecasts · cached `reference/habs_hab-forecasts.html`.
3. **Schaeffer et al. 2024** (method, predictors, metrics, base rate, data-availability) — *J. Environ.
   Manage.* 349:119518, DOI 10.1016/j.jenvman.2023.119518 · open access PMC10842250.
4. **Official model code** — DOI 10.23719/1529140 (EPA ScienceHub `INLA_CONUS_forecast`) · README
   preserved at `reference/INLA_CONUS_forecast-README.md`.
5. **EPA ScienceMatters summary** (plain-language method + accuracy) —
   https://www.epa.gov/sciencematters/epa-researchers-develop-forecasting-approach-predict-harmful-cyanobacterial-blooms
6. **EPA disclaimers / public-domain & no-warranty** (§12 basis) —
   https://www.epa.gov/web-policies-and-procedures/epa-disclaimers ·
   **ScienceHub License** — https://pasteur.epa.gov/license/sciencehub-license.html
7. **Preserved verbatim quotes + full live-probe log:** `reference/PRIMARY-SOURCES.md`.
8. **Empirical checks we ran** (reproducible): `access/qlik_public.py` + `access/pull_forecasts.py`
   → `qaqc/qa_forecasts.py` → `outputs/qa_report.md` + `qa_summary.json`; `access/pull_official.py`.
9. **Prior literature review** (this repo): `../../Research/_sources/ACAD-050-*.md` and `FED-017-*.md`
   (the Schaeffer forecast dossier) and the deck design `../../docs/plans/2026-07-01-hab-landscape-slides-design.md`.

---

## 9. Likely role in the SePRO HAB analysis — and the LEAKAGE POLICY

**Headline (why we ingested it):** the EPA forecast is a **validated federal baseline** — a peer-
reviewed, out-of-sample-tested 7-day bloom-probability product for the same lakes we care about. That
makes it, per the deck's own quality rubric, an **"established-operational"** benchmark. Two defensible
uses:
- **(a) Benchmark to judge against.** Compare any risk/early-warning model *we* build to EPA's forecast
  as a **strong published baseline** (in addition to naïve persistence/climatology). "As explainable
  as, and competitive with, a federal product" is a credible product claim.
- **(b) Leverage as a signal/context.** Use it as an ensemble input or a corroborating overlay for a
  lake/week — *as an operational, as-of covariate only* (see policy).

**Allowed uses (pre-declared to prevent leakage — Codex-reviewed):**
1. **Default = benchmark / context.** Compare against it; show it alongside our outputs.
2. **Feature = only in explicit as-of, operational comparisons** — i.e., only the probability that was
   *published before* the target time, joined as-of, never a future/current-week value.
3. **NEVER a ground-truth label** for any model that itself uses CyAN features. The forecast is
   **CyAN-derived**, so using it to label/validate a CyAN-based model is **circular** and leaks the
   target. Ground truth for bloom presence must come from **independent in-situ** sources (WQP/NARS
   chl-a & toxins) or the raw CyAN observation *treated as observation*, not from this forecast.
4. **Always report a baseline + uncertainty** with any comparison (persistence, climatology), and
   **split by space and time with blocking** (no random shuffles on autocorrelated lake-weeks).
5. **Correlation ≠ causation** on any driver/treatment implication.

**What it is NOT:** not an observation, not a toxin forecast (it predicts a chl-a/dominance threshold,
not microcystin), not a sub-lake map, not a long archive, and not an official data feed.

---

## 10. Reproducibility & version pinning (rules for this dataset)

- **Pin the app IDs + virtual proxy** in `access/qlik_public.py` (verified 2026-07-02, §7.3). A change
  upstream must *fail loudly* (row-count/schema assertions), never silently truncate.
- **Snapshot, don't mutate.** `pull_forecasts.py` writes an **append-only, immutable snapshot**
  (dated, keyed `(snapshot_utc, appid, COMID, WeekEndDate)`), computes sha256, and appends a
  **full-provenance** manifest record: dashboard URL, engine URL, appid, virtual proxy, Xrfkey
  *presence* (never the value), the hypercube object definition, field order, selection state
  (before/after ClearAll), `qSize`, page geometry, row count, distinct COMID, min/max `WeekEndDate`,
  `MaxWeekEndDate`, client version, and access timestamp.
- **Track revisions, don't bless drift.** A "current" view keyed `(COMID, WeekEndDate)` is derived from
  the newest snapshot; when a past week's probability reappears **changed**, emit a **revision record**
  (old→new, both snapshot times) rather than overwrite silently — mirroring `_common/net.py`'s
  integrity discipline for HTTP sources.
- **Official artifact:** `pull_official.py` caches the DOI ZIP with the sha256 above; re-runs are
  cache-hits unless bytes change.
- **Deterministic:** pinned deps (`../requirements.txt`, incl. `websocket-client`), scripted access,
  fixed field order for stable CSV sha256. An **offline QIX fixture** (`reference/*.sample.json`) lets
  the parser be unit-tested without hitting EPA.
- **Cite** the operational product as: *U.S. EPA. Experimental cyanobacterial HAB forecast (7-day),
  HAB Forecasts dashboards, https://www.epa.gov/habs/hab-forecasts, accessed 2026-07-02*, alongside the
  **paper** (method) and the **DOI 10.23719/1529140** (code).

---

## 11. Geotagging & linkage — COMID is the standout (DESIGN NOW, JOIN LATER)

**Why this matters:** unlike a bare lat/lon feed, every forecast lake carries a **`COMID` (NHDPlus V2
waterbody id)** `[probe]` — the *same hydrographic backbone* our `EPA-NARS`, `WQP`, and `NWIS` modules
already sit on. So the forecast can be bridged to in-situ chemistry, streamflow, watershed covariates,
and the CyAN raster **by identity**, not just proximity.

| Key | What it links to | Populated |
|---|---|---|
| `COMID` | **NHDPlus V2** `NHDWaterbody`; EPA **LakeCat** (watershed metrics); **USGS NLDI** | 100% (2,191/2,191) `[probe]` |
| `Lat_centroid` / `Lon_centroid` | anything spatial; nearest CyAN pixels; buffer joins | 100% |
| `State`, `EPA_region` | administrative stratification / reporting | 100% |
| `Lake_name_for_public` | fuzzy match to WQP/NARS lake names (fallback) | 100% |

**Recommended linkage recipes (to build with the fusion analysis):**
- **Forecast ↔ EPA-NARS:** direct **`COMID` join** — the NARS `siteinfo` carries `COMID` too, so the
  forecast probability and NARS lab chl-a/toxins align on the same lake by identity.
- **Forecast ↔ WQP / NWIS:** feed `COMID` to the **USGS NLDI** to enumerate on-network monitoring
  sites, or match by shared **HUC** (derive HUC from COMID via NHDPlus), or spatial buffer on centroid.
- **Forecast ↔ CyAN raster:** the forecast *is* CyAN-derived, so this join is for **diagnostics only**
  (see §9 — not independent validation); sample CI at the centroid / lake polygon.
- **Forecast ↔ LakeCat:** `COMID` join for hundreds of pre-computed watershed drivers.

**Honest limits of the linkage:**
- **COMID is a dashboard-added convenience key** — the *paper* identifies lakes by lat/lon mesh, not
  COMID; we verified COMID is present and non-null in the delivered product `[probe]`, but its exact
  provenance/curation is EPA's, and it should be validated against NHDPlus before load-bearing joins.
- **Centroid, not polygon:** the coordinate is one point; lake-shape work needs the NHD polygon.
- **Timing:** a weekly forecast rarely coincides with an in-situ sample date — matchups need a
  tolerance window (its own analysis), and the as-of rule of §9 applies.

---

## 12. Restrictions / license (the answer to "can we use it")

- **The underlying data are public.** EPA-produced data are **U.S. public domain by default** (17
  U.S.C. §105; EPA disclaimers) — free to use, redistribute, and build a commercial product on, subject
  to (1) **attribution** (cite EPA + the paper + DOI) and (2) carrying the **no-warranty** disclaimer.
- **The official code deposit** is under the **ScienceHub License** (permissive; preserve the license
  text and citation).
- **The operational access method is the caveat, not the copyright.** Extracting from an anonymous Qlik
  dashboard is an **undocumented, non-sanctioned** path. Nothing observed requires auth or bypasses a
  paywall (the apps are published for anonymous public viewing), and we access read-only, minimally, and
  with an identifying User-Agent — but this is **not an EPA-supported API**, and building a *product
  claim* on a reverse-engineered federal endpoint is a **business/reputational risk** distinct from
  licensing.
- **Hedge (how we square it with the claim gate):**
  1. Anchor all **scientific/method claims** on the **official** paper + DOI code (§7.1), which are
     fully citeable and reproducible.
  2. Present the live-values module as **research/benchmark**, explicitly labeled unofficial —
     **not** a production dependency.
  3. Document **Blake Schaeffer (schaeffer.blake@epa.gov)** as the **escalation contact** to request an
     official/supported feed (and, for any real deployment, seek written EPA confirmation).
- **The real constraint is fitness-for-use** (§5): experimental status, positive bias, resolvable-area
  limits, rolling window — not licensing.

---

## 13. Data & code inventory (verified 2026-07-02)

**Operational panel — `AllWeeks_CyanForecasts` (`[probe]`):** 10 fields (§4); **105,168 rows = 2,191
lakes × 48 weeks**, zero nulls; span 2025-04-05 → 2026-06-27; value distribution in §4. Extractable in
full in ~30 s over QIX.

**Reported model skill (EPA/Schaeffer 2024 — point estimates; NO confidence intervals reported).** Cite
as *EPA-reported*, not repo-validated; pair with a naïve baseline before any reuse:

| Metric (2021 test year) | Value | Note |
|---|---|---|
| AUC | 0.95 | |
| Accuracy | **0.90** | vs **0.84–0.85** for SVC / RF / DNN / LSTM / RNN / GRU baselines (INLA beat all) |
| Sensitivity (recall) | 0.88 | |
| Specificity | 0.91 | |
| **Precision** | **0.49** | ≈half of positive forecasts are false alarms → the "over-predicts" number |
| False-omission rate | 0.01 | low missed-bloom rate → health-protective |
| F1 | 0.63 | |
| Brier | 0.04 | |
| Cohen's κ | 0.58 | |
| **Base rate (prevalence)** | **~9–10%** | 43,482 / 432,030 lake-weeks were blooms (10.1%); 9.1% annualized — the critical context for the metrics above |

Validation scheme: temporal — train 70% of 2017–2020, 30% holdout of 2017–2020, **independent 2021
test year**; classification cutoff 0.10. Predictors: **CyAN** (weekly per-lake mean/median/SD of the
cyanobacteria signal), **PRISM** precipitation, **RF-modeled surface water temperature** (from
`github.com/bschaeff/SW_Model`), **lake mean depth & surface area**; AR1 on prior week; SPDE spatial
field; ice-relabeled winter no-bloom weeks (§1, §5).

**Official code ZIP (`INLA_CONUS_forecast.zip`, 33,677 B, sha256 `126f7f3f…4afb`):** 12 files — R
scripts `generate_week_assignments_tibble.R`, `lake_morpho_code.R`, `parallel.step1plus2.R`,
`cyanoCONUS_ice_step3/step4_adjusted.R`, `generate_ice_tibble.R`, `cyan_processing_conus.R`,
`prism_download.R`, `prism_processing_conus.R`, `compile_data.R`, `conus_inla.R` (the model), and
`README.md` (workflow; preserved at `reference/INLA_CONUS_forecast-README.md`). **Code only — no input
data** (README: inputs are separately, publicly downloadable).

---

## 14. AI-assisted judgment flag

This characterization, the access/QA/viz code, and the two-tier design were drafted with LLM assistance
and then **verified against the live source's bytes**. Provenance of the key facts:

- **`[probe]`-derived (independently verified by scripts we ran against EPA, 2026-07-02):** the QIX
  access method and anonymous session; the `AllWeeks_CyanForecasts` schema and 10 field names; the
  panel shape (2,191 × 48 = 105,168, zero nulls); the temporal span and Saturday cadence; the value
  distribution; COMID completeness and the 2,191-vs-2,192 gap; the three apps and app1's default
  selection; the official ZIP size/sha256/contents; that `/hub`,`/api`,`/sense` require auth.
- **Primary-source-cited (EPA pages / paper / DOI):** the bloom definition, cadence/season, over-
  prediction disclaimer, model type and predictors, and all §13 skill metrics + base rate.
- **LLM-assisted judgment a human should double-check:** the *framing* choices — the two-tier access
  strategy, the leakage policy (§9), and the legitimacy/reputational hedge (§12). These are reasoned
  positions, not facts; they are exactly where a reviewer's judgment should land.
- **Reverse-engineered-protocol flag:** the QIX extraction (§7.2) is our reconstruction of an
  undocumented interface. It is `[probe]`-verified to work today but is **not** an EPA specification and
  may change; the offline fixture + assertions exist so breakage is detected, not silently absorbed.
