# ex-operational-poc — the lean 2-feature bloom forecaster, end to end

A **self-contained, minimal** pipeline that ingests, prepares, trains, evaluates, and
runs the operational **lean model** — a logistic regression on just two features,
`cyan_median` (the lake's recent satellite index) + `area_sqkm` — to forecast WHO
Alert-Level-1 cyanobacteria blooms in Florida's 133 resolvable lakes, at lead times of
0–4 weeks.

We already know (from the full study in `../models/`) that this 2-feature model is the
right operational choice, so this folder builds *only* that model and *only* the data it
needs — nothing else. Simplicity is the point.

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
python 03_train.py        # fit lean LogReg per horizon; tune threshold on validation
python 04_evaluate.py     # held-out test vs persistence + climatology, with CIs
python 05_predict.py      # refit on all history; store the latest per-lake forecast
python -m pytest tests/   # leakage-alignment + metric tests
```

Runs against the CyAN rasters already cached in the repo; with a fresh cache, `01_ingest`
downloads from NASA Earthdata (needs a free `OB_DAAC_EDL_TOKEN` in `../data-sources/.env`).

## Files

```
config.py        every path, threshold, split boundary (one place)
common.py        the trusted core: leakage-safe alignment, split, scoring, metrics
01_ingest.py     step 1 - ensure inputs present (CyAN OLCI mosaics + FL lakes)
02_prepare.py    step 2 - rasters -> data/lake_week.parquet (per-lake median + bloom)
03_train.py      step 3 - train/val: fit per-horizon LogReg -> outputs/models.json
04_evaluate.py   step 4 - test: metrics vs baselines, block-bootstrap CIs -> outputs/eval_metrics.md
05_predict.py    step 5 - run: latest forecast -> outputs/predictions.csv (+ summary)
tests/           unit tests for the leakage-safe core
outputs/         committed real results (models, metrics, predictions, summaries)
data/            gitignored intermediate (lake_week.parquet)
```

## Outputs (committed, real)

`outputs/prepare_summary.md` · `outputs/models.json` (readable coefficients) ·
`outputs/eval_metrics.md` (test AUC / onset-AUC / MCC vs baselines, with CIs) ·
`outputs/predictions.csv` + `outputs/predictions_summary.md` (the latest forecast).

## Honest result

Held-out onset-AUC (early warning on currently-clear lakes) is real (~0.75–0.84 across
horizons) but a per-lake seasonal **climatology baseline is competitive-to-better** on the
onset alert. This 2-feature model's value is **simplicity + explainability while staying
competitive**, not beating every baseline — the richer real-time-CyAN ladder in `../models/`
is what pushes onset skill higher. Forecasts are AL1 *probabilities*, not chlorophyll;
the label is a satellite realization, not toxin. Correlation, not causation.
