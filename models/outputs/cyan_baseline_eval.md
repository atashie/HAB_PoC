# CyAN-only baseline evaluation (FL, temporal split)

Probability models FIT on train (<=2023), threshold tuned on **val (2024)**, refit on train+val, scored on held-out **test 2025**. Persistence = last observed bloom carried to the cutoff week `W-h-1` (latency-aware, D-28). Climatology = per-lake per-month rate. AR ladder = logistic on CyAN-only features + climatology. Metrics: canonical suite (`model/metrics.py`); **MCC is the headline balanced metric**; AUC-ROC of the HARD persistence is capped, so read it with care.

## Full test set

| h | baseline | n_test | base_rate | AUC-ROC | AUC-PR | Brier | MCC | F1 | Prec | Recall | Acc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | persistence | 6808 | 0.266 | 0.941 | 0.858 | 0.046 | 0.883 | 0.914 | 0.915 | 0.913 | 0.954 |
| 0 | climatology | 6808 | 0.266 | 0.955 | 0.887 | 0.076 | 0.75 | 0.815 | 0.83 | 0.802 | 0.903 |
| 0 | ladder | 6808 | 0.266 | 0.986 | 0.965 | 0.035 | 0.88 | 0.912 | 0.922 | 0.902 | 0.954 |
| 1 | persistence | 6808 | 0.266 | 0.918 | 0.809 | 0.063 | 0.838 | 0.881 | 0.885 | 0.877 | 0.937 |
| 1 | climatology | 6808 | 0.266 | 0.955 | 0.887 | 0.076 | 0.75 | 0.815 | 0.83 | 0.802 | 0.903 |
| 1 | ladder | 6808 | 0.266 | 0.982 | 0.949 | 0.046 | 0.845 | 0.887 | 0.867 | 0.908 | 0.939 |
| 2 | persistence | 6808 | 0.266 | 0.899 | 0.771 | 0.077 | 0.803 | 0.855 | 0.861 | 0.849 | 0.923 |
| 2 | climatology | 6808 | 0.266 | 0.955 | 0.887 | 0.076 | 0.75 | 0.815 | 0.83 | 0.802 | 0.903 |
| 2 | ladder | 6808 | 0.266 | 0.976 | 0.937 | 0.052 | 0.822 | 0.87 | 0.837 | 0.905 | 0.928 |
| 3 | persistence | 6808 | 0.266 | 0.89 | 0.754 | 0.083 | 0.786 | 0.842 | 0.852 | 0.833 | 0.917 |
| 3 | climatology | 6808 | 0.266 | 0.955 | 0.887 | 0.076 | 0.75 | 0.815 | 0.83 | 0.802 | 0.903 |
| 3 | ladder | 6808 | 0.266 | 0.974 | 0.931 | 0.056 | 0.812 | 0.862 | 0.864 | 0.86 | 0.927 |
| 4 | persistence | 6808 | 0.266 | 0.884 | 0.743 | 0.087 | 0.776 | 0.834 | 0.846 | 0.823 | 0.913 |
| 4 | climatology | 6808 | 0.266 | 0.955 | 0.887 | 0.076 | 0.75 | 0.815 | 0.83 | 0.802 | 0.903 |
| 4 | ladder | 6808 | 0.266 | 0.973 | 0.927 | 0.06 | 0.799 | 0.853 | 0.846 | 0.859 | 0.921 |

## AUC-ROC by horizon

| h | climatology | ladder | persistence |
| --- | --- | --- | --- |
| 0.0 | 0.955 | 0.986 | 0.941 |
| 1.0 | 0.955 | 0.982 | 0.918 |
| 2.0 | 0.955 | 0.976 | 0.899 |
| 3.0 | 0.955 | 0.974 | 0.89 |
| 4.0 | 0.955 | 0.973 | 0.884 |

## Brier by horizon (lower better)

| h | climatology | ladder | persistence |
| --- | --- | --- | --- |
| 0.0 | 0.076 | 0.035 | 0.046 |
| 1.0 | 0.076 | 0.046 | 0.063 |
| 2.0 | 0.076 | 0.052 | 0.077 |
| 3.0 | 0.076 | 0.056 | 0.083 |
| 4.0 | 0.076 | 0.06 | 0.087 |

## MCC by horizon (headline balanced metric)

| h | climatology | ladder | persistence |
| --- | --- | --- | --- |
| 0.0 | 0.75 | 0.88 | 0.883 |
| 1.0 | 0.75 | 0.845 | 0.838 |
| 2.0 | 0.75 | 0.822 | 0.803 |
| 3.0 | 0.75 | 0.812 | 0.786 |
| 4.0 | 0.75 | 0.799 | 0.776 |

## Pairwise skill deltas -- ALL samples (positive => first beats second)

Climatology as an explicit comparator vs persistence and the ladder. The strongest CyAN-only baseline is **metric-dependent**, so the fused model must beat the best on EACH metric.

**MCC deltas:**

| h | ladder-persist | ladder-clim | clim-persist |
| --- | --- | --- | --- |
| 0.0 | -0.003 | 0.13 | -0.133 |
| 1.0 | 0.007 | 0.095 | -0.088 |
| 2.0 | 0.019 | 0.072 | -0.053 |
| 3.0 | 0.026 | 0.062 | -0.036 |
| 4.0 | 0.023 | 0.049 | -0.026 |

**AUC-ROC deltas:**

| h | ladder-persist | ladder-clim | clim-persist |
| --- | --- | --- | --- |
| 0.0 | 0.045 | 0.031 | 0.014 |
| 1.0 | 0.064 | 0.027 | 0.037 |
| 2.0 | 0.077 | 0.021 | 0.056 |
| 3.0 | 0.084 | 0.019 | 0.065 |
| 4.0 | 0.089 | 0.018 | 0.071 |

**Brier deltas** (lower-is-better; positive => first model has the lower/better Brier):

| h | ladder-persist | ladder-clim | clim-persist |
| --- | --- | --- | --- |
| 0.0 | 0.011 | 0.041 | -0.03 |
| 1.0 | 0.017 | 0.03 | -0.013 |
| 2.0 | 0.025 | 0.024 | 0.001 |
| 3.0 | 0.027 | 0.02 | 0.007 |
| 4.0 | 0.027 | 0.016 | 0.011 |

## Transition weeks only (target != persistence -- the flips)

Where persistence is wrong by construction; this is where a model must earn its keep and where fused features should help most.

| h | baseline | n_flip | flip_rate | AUC-ROC | AUC-PR | Brier | MCC | F1 | Prec | Recall | Acc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | persistence | 311 | 0.046 | 0.0 | 0.508 | 1.0 | -1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 0 | climatology | 311 | 0.046 | 0.511 | 0.515 | 0.342 | -0.007 | 0.46 | 0.504 | 0.424 | 0.495 |
| 0 | ladder | 311 | 0.046 | 0.072 | 0.323 | 0.574 | -0.66 | 0.105 | 0.116 | 0.095 | 0.174 |
| 1 | persistence | 429 | 0.063 | 0.0 | 0.52 | 1.0 | -1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 1 | climatology | 429 | 0.063 | 0.544 | 0.549 | 0.334 | 0.048 | 0.513 | 0.545 | 0.484 | 0.522 |
| 1 | ladder | 429 | 0.063 | 0.144 | 0.346 | 0.526 | -0.548 | 0.317 | 0.296 | 0.341 | 0.235 |
| 2 | persistence | 522 | 0.077 | 0.0 | 0.525 | 1.0 | -1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2 | climatology | 522 | 0.077 | 0.566 | 0.566 | 0.326 | 0.081 | 0.532 | 0.568 | 0.5 | 0.538 |
| 2 | ladder | 522 | 0.077 | 0.2 | 0.367 | 0.493 | -0.482 | 0.371 | 0.34 | 0.409 | 0.274 |
| 3 | persistence | 564 | 0.083 | 0.0 | 0.535 | 1.0 | -1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 3 | climatology | 564 | 0.083 | 0.588 | 0.59 | 0.315 | 0.11 | 0.559 | 0.593 | 0.53 | 0.553 |
| 3 | ladder | 564 | 0.083 | 0.257 | 0.397 | 0.462 | -0.283 | 0.389 | 0.398 | 0.381 | 0.36 |
| 4 | persistence | 591 | 0.087 | 0.0 | 0.543 | 1.0 | -1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 4 | climatology | 591 | 0.087 | 0.611 | 0.613 | 0.303 | 0.145 | 0.587 | 0.616 | 0.561 | 0.572 |
| 4 | ladder | 591 | 0.087 | 0.301 | 0.424 | 0.44 | -0.219 | 0.439 | 0.442 | 0.436 | 0.394 |

## Key findings (auto-generated)

- **Persistence decays with lead** (AUC-ROC 0.941->0.884; Brier 0.046->0.087) -- the freshest published CyAN goes staler.
- **Absolute skill is dominated by per-lake seasonal identity, not just autocorrelation (Codex M3):** climatology alone reaches AUC-ROC 0.955 flat across horizons, and the ladder adds only ~+0.027-+0.018 AUC-ROC over climatology. So the fused model must show **lift over BOTH the ladder AND climatology**, not just over persistence.
- **The ladder is the strongest CyAN-only baseline overall** -- best AUC-ROC/AUC-PR/Brier at every horizon; on MCC it ties persistence at h0 (0.880 vs 0.883) and leads beyond. **Climatology is a strong RANKER but weak CLASSIFIER (a distinct comparator):** it beats persistence on AUC-ROC by a WIDENING margin (+0.014 at h0 -> +0.071 at h4, as persistence decays) yet has the LOWEST MCC (0.750) -- a smooth seasonal prior ranks lake-months well but classifies individual lake-weeks worse than state-aware persistence. It is 2nd on AUC-ROC (ladder leads) and last on MCC, so never the single best baseline, but its ranking strength quantifies how much signal is pure seasonality. The fused model must beat the best baseline on EACH metric.
- **Operating-point metrics tie at short lead (why the wide suite matters):** at h0 persistence MCC 0.883 vs ladder 0.880; the ladder's edge appears at longer leads (h4 MCC 0.776->0.799). AUC-ROC alone overstates the ladder at short lead.
- **The real bar is TRANSITION weeks (target != persistence -- the onsets/offsets).** Persistence is wrong on EVERY flip by construction (AUC-ROC 0, MCC -1). And the CyAN-only **ladder is ANTI-PREDICTIVE on flips at every horizon** (AUC-ROC 0.072->0.301, all < 0.5; MCC -0.660->-0.219, all negative) -- driven by 'current state persists', it predicts the WRONG direction on flips. Climatology (seasonal timing) is the only CyAN-only signal with any positive flip skill, and weak (MCC up to 0.145 at h4). **Flips are where fused weather/nutrient features must earn their keep -- the headline test for fusion.**
