# EPA forecast head-to-head vs our CyAN-only baselines (shared FL 2025 COMID-weeks)

Shared test set: **4,527 FL lake-weeks** (132 lakes x 35 weeks). Ground truth = our AL1 bloom (pinned to the same Schaeffer/WHO AL1 concept EPA forecasts).

> **EPA values = 2026-07-02 dashboard snapshot (NOT proven as-issued).** The dashboard is a live, revisable view and we hold ONE snapshot, so 2025 values may have been revised since issuance -- treat as dashboard-observed, not strictly as-issued.

### Four material caveats
1. **Provenance:** snapshot, not proven as-issued (above).
2. **Structural advantage to us (subtle):** SAME AL1 concept, but persistence/climatology/ladder are fit to / derived from our EXACT realized labels; EPA's model is independent. A gap is not a clean skill test.
3. **Timing:** EPA releases Tue/Wed, valid the current week through Sat (not 7-days-ahead). Our W-1/W-2 is OUR CyAN-latency sensitivity, not EPA's info set.
4. **Seasonal:** EPA ~Apr-Nov -> 35/52 weeks, peak season, base rate 28.8% vs 26.6% full-year. Metrics seasonal-only.

## Threshold-free -- ALL samples (primary)

| EPA freshest | predictor | AUC-ROC | AUC-PR | Brier |
| --- | --- | --- | --- | --- |
| W-1 | EPA_forecast | 0.928 | 0.851 | 0.101 |
| W-1 | our_ladder | 0.986 | 0.967 | 0.038 |
| W-1 | persistence | 0.937 | 0.859 | 0.05 |
| W-1 | climatology | 0.955 | 0.895 | 0.081 |
| W-2 | EPA_forecast | 0.928 | 0.851 | 0.101 |
| W-2 | our_ladder | 0.982 | 0.951 | 0.049 |
| W-2 | persistence | 0.918 | 0.818 | 0.066 |
| W-2 | climatology | 0.955 | 0.895 | 0.081 |

## Transition weeks only (target != persistence -- the flips)

The fairest cut: persistence is wrong on every flip by construction, so this shows whether EPA's fusion model (CyAN+weather+morphology) anticipates ONSETS better than our CyAN-only baselines. Threshold-free + MCC/Recall at the same operating threshold.

| EPA freshest | predictor | n_flip | AUC-ROC | AUC-PR | Brier | MCC | Recall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W-1 | EPA_forecast | 227 | 0.469 | 0.518 | 0.401 | -0.021 | 0.483 |
| W-1 | our_ladder | 227 | 0.068 | 0.339 | 0.571 | -0.647 | 0.175 |
| W-1 | persistence | 227 | 0.0 | 0.529 | 1.0 | -1.0 | 0.0 |
| W-1 | climatology | 227 | 0.537 | 0.566 | 0.335 | 0.061 | 0.575 |
| W-2 | EPA_forecast | 299 | 0.455 | 0.508 | 0.407 | -0.062 | 0.456 |
| W-2 | our_ladder | 299 | 0.118 | 0.348 | 0.535 | -0.585 | 0.215 |
| W-2 | persistence | 299 | 0.0 | 0.528 | 1.0 | -1.0 | 0.0 |
| W-2 | climatology | 299 | 0.551 | 0.567 | 0.333 | 0.105 | 0.608 |

## Week-block bootstrap 95% CIs for AUC-ROC (W-2 / h1; resamples the 35 weeks)

| predictor | AUC-ROC 2.5% | median | 97.5% |
| --- | --- | --- | --- |
| EPA_forecast | 0.92 | 0.928 | 0.936 |
| our_ladder | 0.978 | 0.982 | 0.985 |
| persistence | 0.904 | 0.918 | 0.93 |
| climatology | 0.95 | 0.955 | 0.96 |

**AUC-ROC differences (95% CI):** our_ladder - EPA: +0.054 [+0.047, +0.059]; EPA - persistence: +0.010 [-0.000, +0.022]

## Seasonal-window shift -- OUR baselines, full-year 2025 vs exact shared COMID-weeks (h1)

| predictor | full-yr AUC | shared AUC | full-yr base | shared base |
| --- | --- | --- | --- | --- |
| persistence | 0.918 | 0.918 | 0.266 | 0.288 |
| climatology | 0.955 | 0.955 | 0.266 | 0.288 |
| our_ladder | 0.982 | 0.982 | 0.266 | 0.288 |

## Operating-point -- ALL samples (in-sample thresholds; optimistic, even-handed)

| EPA freshest | predictor | MCC | F1 | Prec | Recall | Acc |
| --- | --- | --- | --- | --- | --- | --- |
| W-1 | EPA_forecast | 0.677 | 0.774 | 0.731 | 0.821 | 0.861 |
| W-1 | our_ladder | 0.879 | 0.914 | 0.913 | 0.915 | 0.95 |
| W-1 | persistence | 0.877 | 0.913 | 0.917 | 0.908 | 0.95 |
| W-1 | climatology | 0.751 | 0.825 | 0.794 | 0.858 | 0.895 |
| W-2 | EPA_forecast | 0.677 | 0.774 | 0.731 | 0.821 | 0.861 |
| W-2 | our_ladder | 0.846 | 0.89 | 0.895 | 0.885 | 0.937 |
| W-2 | persistence | 0.838 | 0.885 | 0.891 | 0.879 | 0.934 |
| W-2 | climatology | 0.751 | 0.825 | 0.794 | 0.858 | 0.895 |

## Key findings (auto-generated)

- **EPA vs persistence (against our AL1):** AUC-ROC gap +0.010 [-0.000, +0.022] -- CI INCLUDES 0, so EPA does NOT clearly beat naive persistence at predicting our AL1 (marginal at best). EPA Brier 0.101 vs persistence 0.066; EPA mean prob 0.246 vs shared base 0.288 -- descriptive calibration gap, not a proven definition mismatch.
- **Our ladder vs EPA:** +0.054 AUC-ROC [+0.047, +0.059] -- but see caveat 2: the ladder is fit to our EXACT labels, EPA is not, so NOT a clean skill win.
- **On FLIPS (h1):** EPA AUC-ROC 0.455 / MCC -0.062 / Recall 0.456 vs our ladder AUC-ROC 0.118 / MCC -0.585 vs climatology AUC-ROC 0.551. See table for the full onset comparison.
- **FUSION MOTIVATION (the headline for feature work):** the ordering FLIPS on flips -- climatology (0.551) > EPA fusion (0.455) > our CyAN-only ladder (0.118, anti-predictive) > persistence (0.000). Our ladder's all-samples dominance is an ARTIFACT of persistence-easy weeks; on the onsets that matter, CyAN-only is useless-to-harmful, and EPA's weather/morphology fusion helps. **Our fusion features must beat CLIMATOLOGY on flips to earn their place.**
