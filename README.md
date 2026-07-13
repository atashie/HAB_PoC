# Freshwater Harmful Algal Bloom Forecasting & Risk Dashboard

An end-to-end system that forecasts **cyanobacteria (blue-green algae) blooms in freshwater lakes**
and presents the results as an interactive risk dashboard. It fuses a satellite bloom signal with
weather, in-situ water chemistry, and lake morphology to answer one operational question, per lake,
every week: **is this lake likely to bloom in the next 0–4 weeks, and how sure are we?**

The pipeline runs on **real, public data** end-to-end, is **reproducible from checked-in code**, and
reports **every number against a baseline and an uncertainty** — including the results that didn't
work. It currently covers **Florida's 133 satellite-resolvable lakes** over the Sentinel-3 OLCI era
(2016→present) and is built to extend to other regions.

---

## What it does

- **Forecasts bloom risk** as the probability of a **WHO Alert-Level-1 (AL1) bloom** — lake-median
  chlorophyll-a ≥ 12 µg/L with cyanobacteria dominance — for each lake, each week, at lead times of
  **0 to 4 weeks**.
- **Benchmarks honestly.** Every forecast is scored against naïve baselines (latency-aware
  persistence, per-lake climatology, a satellite-autoregressive ladder) **and** against the U.S.
  federal EPA CyanoHAB forecast on the same lakes and weeks.
- **Explains itself.** Models are transparent classifiers (logistic regression, gradient-boosted
  trees). The pipeline reports feature importance, ablations, and per-lake skill so you can see *why*
  a prediction is what it is — not just what it predicts.
- **Ships a tool.** A one-page, offline-capable dashboard turns the forecasts into an alert list, an
  onset-lead indicator, per-lake deep-dives, and a fleet-wide map.

### The headline result (stated plainly)

Early warning works: among lakes that are currently clear, the system ranks which will bloom next
week at **onset-AUC ≈ 0.94**, beating both per-lake climatology (0.90) and the EPA forecast (0.82).
But essentially **all of that skill comes from the real-time satellite signal itself** — fusing
weather, in-situ chemistry, and morphology adds **no robust incremental held-out skill** that
survives rigorous importance testing. So the **deployable model is deliberately small**: a compact
real-time-satellite autoregression (two features — the lake's median satellite index and its area) —
plus the EPA forecast as a second opinion. A well-validated simple model beat the complex one, and
that is reported as the finding, not hidden.

What the system does **not** do (by design, stated as limits): it predicts a **satellite bloom
label**, not toxin concentration or cell counts; it forecasts bloom **levels** well but bloom
**transitions** (exact onset/offset timing) only weakly; it is validated on **known lakes forecasting
into future weeks**, not transfer to unseen lakes; and it can only see lakes the ~300 m satellite
sensor resolves (roughly ≥ 900 m across).

---

## How it works

Five loosely-coupled layers hand off through checked-in files (cited raw pulls → derived tables →
result markdown → precomputed predictions), so the whole chain is reproducible and auditable.

```
Public data sources                 What we do with them
────────────────────                ───────────────────────────────────────────────
Satellite bloom index (CyAN)   ┐
EPA CyanoHAB forecast          │    data-sources/  → scripted, cited, QA'd acquisition
Water Quality Portal (in-situ) │        (each source: pull → integrity/QA → visualize)
USGS NWIS (hydrology)          │                     │
EPA National Lakes Assessment  │                     ▼
ERA5 / ECMWF (weather)         ┘    models/  → prepare a fused lake-week table,
                                        train + evaluate forecasters, write result files
                                                     │
                                                     ├──────────────┐
                                                     ▼              ▼
                                    dashboard/  → interactive     presentation/ → an
                                    risk tool reading             interactive scrolling
                                    precomputed predictions       explainer of the whole study
```

1. **`data-sources/` — acquisition & QA.** Each public source is a self-contained module that
   documents the dataset, scripts a cached pull (with a sha256 manifest), runs quality checks, and
   renders summary maps/plots. Raw pulls are never hand-edited; everything regenerates from code.
2. **`models/` — the forecaster.** A four-stage pipeline (acquire → prepare → model → evaluate)
   builds a fused lake-week table, trains explainable classifiers across a feature × architecture
   grid, and writes one result file per experiment (baselines, head-to-heads, ablations, importance).
3. **`dashboard/` — the tool.** A deterministic build reuses the exact estimator code from the model
   layer, scores the freshest forecast snapshot, and emits precomputed predictions the static page
   reads. Two self-checks refuse to publish if the numbers drift from the validated analysis.
4. **`presentation/` — the explainer.** A self-contained HTML scrolling story that walks through the
   problem, the data (a live Florida map that layers each source), and the findings.
5. **`Research/` — the evidence base.** A cited literature landscape (real public sources) that
   grounds the modeling choices.

A standalone, minimal **operational slice** lives in **`ex-operational-poc/`**: an end-to-end
pipeline (ingest → prepare → train → evaluate → run) for just the deployable lean 2-feature model —
the study-selected **HistGBM** on `cyan_median` + `area_sqkm` — with the autoregressive-leakage
handling documented and tested.

For the full folder/document map see **[`ARCHITECTURE.md`](ARCHITECTURE.md)**; for the function-level
code tour see **[`CODE-MAP.md`](CODE-MAP.md)** (and **[`CODE-MAP-PoC-SIMPLE.md`](CODE-MAP-PoC-SIMPLE.md)**
for the operational lean-model workflow).

---

## The dashboard

A single page, two tabs, fully offline once loaded (geometry and predictions ship as local JS):

- **Alerts** — a map beside a ranked list. *New-bloom risk*: lakes that are clear now, ranked by
  forecast probability of an AL1 bloom, with a target-week selector and an **onset-lead** column (the
  earliest horizon at which risk crosses the warning line). *Current active blooms*: lakes blooming
  now, ranked by how long they've been blooming.
- **Deep dive** — pick a lake and see its forecast by week (the shipped model vs. the lean model vs.
  climatology vs. EPA), its observed history (satellite index + real in-situ chlorophyll samples),
  where the forecast disagrees with climatology/EPA, current feature values by family, and a
  sortable fleet table beside an explorer map that shades every lake by any chosen metric.

Forecasts are shown as **probabilities of a bloom (0–100%)**, never as an invented chlorophyll
number; risk tiers are labeled illustrative and tunable; and the view is dated as a demonstration on
a fixed real snapshot, not a live operational feed.

---

## Running it

Each layer has its own README with the detail. In short:

```bash
# 1. Acquire — each source module scripts its own cached, manifested pull + QA
python data-sources/cyan/access/pull_cyan.py               # satellite index (worked example)
python data-sources/cyan/qaqc/qa_cyan.py                   # integrity + QA report
#   other modules name their own scripts (e.g. weather/access/pull_hourly_async.py,
#   cyano-forecasts/access/pull_forecasts.py) — see each data-sources/<source>/README.md

# 2. Prepare + model (Florida lake-week forecaster)
python models/prepare/assemble_fusion_table.py             # build the fused lake-week table
python models/model/eval_experiments.py                    # train + score the experiment grid
#   ... plus the other model/eval_*.py and model/exp_*.py drivers -> models/outputs/*.md

# 3. Build the dashboard's precomputed predictions, then open it
python dashboard/build_dashboard_data.py
#   -> open dashboard/index.html in a browser

# 4. Build the presentation assets, then open it
python presentation/build_story_assets.py
#   -> open presentation/story.html in a browser
```

Python 3.13; dependencies are pinned in `data-sources/requirements.txt` (acquisition/QA) with
per-layer notes for the modeling and visualization stacks (`pandas`, `numpy`, `scikit-learn`,
`xgboost`, `geopandas`, `rasterio`, `xarray`). Pipelines are deterministic (fixed seeds); results
regenerate from source.

## Live demos

- **Dashboard:** https://harmful-algal-bloomspoc.vercel.app/
- **Interactive explainer:** https://harmful-algal-blooms-poc-story.vercel.app/

Both are static sites (no server, no backend); each `git push` redeploys them.

---

## Data sources

All public, all cited with access dates in `data-sources/DATA-REGISTRY.md`:

| Source | What it provides | Role |
|--------|------------------|------|
| **EPA/NASA CyAN** | Satellite cyanobacteria index (~300 m, weekly) | Target label + real-time signal + water mask |
| **EPA CyanoHAB forecast** | Federal experimental per-lake bloom forecast | Independent benchmark |
| **Water Quality Portal** | In-situ nutrients, chlorophyll, temperature | Fusion feature + validation |
| **USGS NWIS** | Streamflow / gage height | Hydrology driver |
| **EPA NARS / NLA** | Lab lake chemistry + cyanotoxins | Validation + context |
| **ERA5 / ECMWF** | Weather reanalysis + forecast | Weather drivers |

---

## Principles

The system is built to stand behind a claim, so four rules gate every number it produces:

1. **Real, cited data only** — no fabricated values; synthetic data (if ever used) is labeled as such
   everywhere it appears.
2. **Reproducible** — data access is scripted and cached; pipelines are deterministic; results
   regenerate from checked-in code.
3. **Baselined + bounded** — every metric carries a naïve baseline and an uncertainty, and is stated
   with the limits of where it applies.
4. **Explainable over sophisticated** — a well-validated simple model is preferred to an opaque
   complex one, and negative/weak results are reported as findings rather than hidden.
