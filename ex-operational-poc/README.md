# ex-operational-poc — the optimized lean bloom forecaster, end to end

A **self-contained, minimal** pipeline that ingests, prepares, trains, evaluates, and
runs the operational **lean model** — a **HistGradientBoostingClassifier** on just two
features, `cyan_median` (the lake's recent satellite index) + `area_sqkm` — to forecast
WHO Alert-Level-1 cyanobacteria blooms in Florida's 133 resolvable lakes, at lead times
of 0–4 weeks.

The full study in `../models/` settled two things about the operational model, and we
ship exactly those: (1) the **feature set** — a greedy backward ablation dropped 42 of 44
features with no significant held-out AUC cost, leaving `cyan_median` + `area_sqkm`; and
(2) the **architecture** — on that identical 2-feature set the gradient-boosted trees
beat a logistic GLM on the decision-relevant early-warning metric (h=1 onset-AUC **0.916
vs 0.823**, onset-MCC **0.314 vs 0.158**; `../models/outputs/exp_feature_ablation.md`,
mirrored in `presentation/story.html`). The trees capture the non-linear
`cyan_median × area` interaction a linear logit cannot. So this folder builds *only* that
model and *only* the data it needs — nothing else.

> **Transparency note.** A tree ensemble is not human-readable coefficients like the GLM
> this pipeline used to ship. We keep it defensible by persisting the fitted booster and
> emitting, in `outputs/models.json`, a **permutation-importance** breakdown (how hard the
> model leans on each feature) and a **partial-dependence** curve (how AL1 risk responds to
> CyAN) — the "why" in behaviour terms rather than weights.

> **The one thing to get right: no autoregressive leakage.** The target is a threshold on
> the CyAN median; the feature is the CyAN median from an earlier week. The rule that keeps
> that honest — feature week = `target − (h+1)` weeks, freshest-available, never the target
> week — lives in `common.build_horizon_frame` and is covered by `tests/`. See
> [`../CODE-MAP-PoC-SIMPLE.md`](../CODE-MAP-PoC-SIMPLE.md) for the full explanation.

## Run it

```bash
pip install -r requirements.txt
python 01_ingest.py       # ensure CyAN OLCI mosaics + FL lakes are present (cache-verified)
python 02_prepare.py      # rasters -> per-lake weekly cyan_median + AL1 label  (~1 min)
python 03_train.py        # fit lean HistGBM per horizon; tune threshold on validation
python 04_evaluate.py     # held-out test vs persistence + climatology, with CIs
python 05_predict.py      # refit on all history; store the latest per-lake forecast
python -m pytest tests/   # leakage-alignment + model + metric tests
```

Runs against the CyAN rasters already cached in the repo. With an empty cache, `01_ingest` points
you to the repo's cited CyAN pull (`data-sources/cyan`, which fetches the weekly CONUS mosaics from
NASA Earthdata with a free `OB_DAAC_EDL_TOKEN`) rather than re-implementing that multi-GB download.

## Files

```
config.py        every path, threshold, split boundary, HGB hyperparameters (one place)
common.py        the trusted core: leakage-safe alignment, split, model, scoring, metrics
01_ingest.py     step 1 - ensure inputs present (CyAN OLCI mosaics + FL lakes)
02_prepare.py    step 2 - rasters -> data/lake_week.parquet (per-lake median + bloom)
03_train.py      step 3 - train/val: fit per-horizon HistGBM -> outputs/models/*.joblib + models.json
04_evaluate.py   step 4 - test: metrics vs baselines, block-bootstrap CIs -> outputs/eval_metrics.md
05_predict.py    step 5 - run: latest forecast -> outputs/predictions.csv (+ summary)
tests/           unit tests for the leakage-safe core + the model
outputs/         committed real results (models, metrics, predictions, summaries)
data/            gitignored intermediate (lake_week.parquet)
```

## Outputs (committed, real)

`outputs/prepare_summary.md` · `outputs/models.json` (hyperparameters, thresholds,
permutation importance, CyAN partial-dependence) + `outputs/models/hgb_h{0..4}.joblib`
(the fitted boosters) · `outputs/eval_metrics.md` (test AUC / onset-AUC / MCC / onset-MCC
vs baselines, with CIs) · `outputs/predictions.csv` + `outputs/predictions_summary.md`
(the latest forecast).

## Honest result

Held-out **onset-AUC** (early warning on currently-clear lakes) is real and, with the
gradient-boosted trees, materially better than the logistic GLM this pipeline previously
shipped — the study's reason for selecting this architecture on the lean set. A per-lake
seasonal **climatology baseline stays competitive**, especially at longer lead, where the
real-time feature goes stale while climatology (calendar-only) pays no lead-time penalty.
So the lean model's value is **a cheap, deployable early-warning forecaster that extends
EPA's single 1-week nowcast to a 0–4-week horizon** while staying competitive with the
baselines — not beating every one; the richer real-time-CyAN + fusion ladder in
`../models/` is the unproven avenue for pushing onset skill higher. Forecasts are AL1
*probabilities*, not chlorophyll; the label is a satellite realization, not toxin.
Correlation, not causation.
