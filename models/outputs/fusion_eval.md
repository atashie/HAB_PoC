# Fusion model evaluation -- SAME-LAKE held-out time (Codex-reconciled, critical)

HistGradientBoosting; **no explicit lake ID / lat-lon**; validation = held-out YEAR 2025 (matches EPA temporal holdout). **Scope caveat:** this is same-lake future prediction only -- NOT transfer to unseen lakes; static morphology + nearest-cell weather can still fingerprint place under a same-lake split. Climatology is a BASELINE (D-35). Threshold tuned on VAL 2024; early stopping on.

## h=1 (EPA-comparable)

| track | AUC-ROC | AUC-PR | Brier | MCC | AUC_within(n) | flip_MCC | flip_AUC | n_flip | onset-MCC | onset-AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | 0.918 | 0.809 | 0.063 | 0.838 | 0.705 (60) | -1.000 | 0.000 | 429 | 0.000 | 0.500 |
| climatology (baseline) | 0.955 | 0.887 | 0.076 | 0.750 | 0.800 (60) | 0.048 | 0.544 | 429 | 0.374 | 0.897 |
| CyAN-ladder (bar) | 0.980 | 0.948 | 0.046 | 0.843 | 0.850 (60) | -0.677 | 0.046 | 429 | 0.367 | 0.929 |
| Track A (fusion, no clim) | 0.983 | 0.957 | 0.044 | 0.844 | 0.878 (60) | -0.486 | 0.166 | 429 | 0.334 | 0.943 |
| Track B (+clim) | 0.980 | 0.953 | 0.045 | 0.846 | 0.873 (60) | -0.356 | 0.275 | 429 | 0.399 | 0.934 |

**Fusion lift over the CyAN ladder is small and CyAN-dominated.** Paired within-lake AUC delta (Track A - ladder), per lake, lake-block bootstrap: median **+0.015** [+0.003, +0.021], positive in 67% of 60 lakes (the headline 0.843->0.891 was difference-of-medians, not paired -- the honest paired lift is ~+0.015).

### Block permutation importance (Track A, mean test drop over 20 shuffles when a block is shuffled; baseline AUC 0.983, baseline onset-MCC 0.334)

| block | AUC drop | onsetMCC drop | onsetMCC std |
| --- | --- | --- | --- |
| CYAN | +0.2756 | +0.2465 | 0.0159 |
| INSITU | +0.0046 | +0.0890 | 0.0286 |
| STATIC | +0.0038 | +0.0702 | 0.0201 |
| WEATHER | +0.0017 | +0.0474 | 0.0154 |
| SEASON | +0.0009 | +0.0048 | 0.0169 |

### Block ablation (Track A minus a block)

| removed | AUC-ROC | AUC_within |
| --- | --- | --- |
| -CYAN | 0.949 | 0.747 |
| -STATIC | 0.981 | 0.881 |
| -SEASON | 0.983 | 0.879 |
| -WEATHER | 0.983 | 0.873 |
| -INSITU | 0.983 | 0.857 |

## Horizon curve h=0..4 (AUC-ROC; flip_MCC)

| h | persist AUC | clim AUC | ladder AUC | fusion AUC | ladder flip_MCC | fusion flip_MCC |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.941 | 0.955 | 0.988 | 0.989 | -0.704 | -0.653 |
| 1 | 0.918 | 0.955 | 0.980 | 0.983 | -0.677 | -0.486 |
| 2 | 0.899 | 0.955 | 0.972 | 0.979 | -0.678 | -0.370 |
| 3 | 0.890 | 0.955 | 0.966 | 0.976 | -0.638 | -0.286 |
| 4 | 0.884 | 0.955 | 0.961 | 0.973 | -0.628 | -0.306 |

## Honest verdict

- **Fusion adds a tiny, real ranking lift** over the CyAN ladder (paired within-lake +0.015 [+0.003, +0.021]), but it is **overwhelmingly CyAN autoregression** (permutation: CYAN dominates; weather/in-situ/static each add ~thousandths of AUC; removing weather or in-situ barely moves pooled AUC).
- **Still anti-predictive on transition weeks** (flip_MCC negative): the model mostly predicts the previous state -- calling offsets positive and onsets negative. **Plain climatology beats the fusion GBM on flips.** Fusion polishes easy next-state ranking; it has NOT solved the scientifically important ONSET/OFFSET problem.
- Same-lake temporal validation only; not a generalization-to-new-lakes claim.
