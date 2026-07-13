# ⚠️ Regenerate these outputs

The code in this folder was reworked to ship the **optimized lean model — a
HistGradientBoostingClassifier** on `cyan_median + area_sqkm` (the architecture the full study
selected for this feature set; see `../../models/outputs/exp_feature_ablation.md` and
`presentation/story.html`). The **committed artifacts here have not yet been regenerated** because
the raw CyAN rasters and the lakes layer are not present in this checkout (they are gitignored /
pulled separately), so the pipeline could not be run end-to-end during the rework.

**Until you re-run it, the numeric outputs below reflect the *previous logistic-GLM* model, not the
model the code now ships.**

| File | Status | Depends on model? |
|------|--------|-------------------|
| `prepare_summary.md` | current | no — panel stats only |
| `models.json` | **stub placeholder** | yes — needs `03_train` |
| `models/hgb_h{0..4}.joblib` | **missing** | yes — written by `03_train` |
| `eval_metrics.md` | **stale (logistic)** | yes — needs `03_train` + `04_evaluate` |
| `predictions.csv`, `predictions_summary.md` | **stale (logistic)** | yes — needs `03_train` + `05_predict` |

## To regenerate

From the repo root, ensure the CyAN weekly-CONUS-mosaic cache and the FL lakes layer are present
(`config.CYAN_RAW_DIR`, `config.FL_LAKES_GPKG` — `01_ingest.py` verifies and, if empty, points you at
the cited pull in `data-sources/cyan`). Then:

```bash
cd ex-operational-poc
python 01_ingest.py
python 02_prepare.py        # -> data/lake_week.parquet (+ prepare_summary.md)
python 03_train.py          # -> outputs/models/*.joblib + models.json
python 04_evaluate.py       # -> outputs/eval_metrics.md
python 05_predict.py        # -> outputs/predictions.csv + predictions_summary.md
python -m pytest tests/     # 13 tests (leakage core + model + metrics)
```

## Expected result (study reference, HistGBM, held-out test @ h=1)

These are the shipped model's numbers from the study's own feature table
(`greedy_lean · histgbm` in `../../models/outputs/exp_feature_ablation.md`, the figures the deck
ships). This standalone pipeline rebuilds `cyan_median` independently from the rasters, so its
regenerated `eval_metrics.md` should land **very close** but need not be bit-identical:

- all-sample AUC-ROC **0.982**
- onset-AUC **0.916**  (vs logistic 0.823 — the reason for switching architecture)
- onset-MCC **0.314**  (vs logistic 0.158)

Delete this file once the outputs have been regenerated and verified.
