# Held-out evaluation - lean 2-feature model vs. baselines

Features: `cyan_median + area_sqkm`  |  target: median CyAN DN >= 130 (WHO AL1)  |  test = target week >= 2024-07-01.
AUC 95% CIs (in brackets) are block-bootstrapped by lake. `onset` = currently-clear lakes only (early-warning skill).

| h | test rows | base rate | lean AUC | persist AUC | clim AUC | lean onset-AUC | clim onset-AUC | lean MCC |
|--:|--:|--:|--|--:|--:|--|--:|--:|
| 0 | 13,471 | 0.267 | 0.980 [0.973, 0.987] | 0.946 | 0.941 | 0.836 [0.781, 0.881] | 0.851 | 0.894 |
| 1 | 13,471 | 0.267 | 0.968 [0.958, 0.977] | 0.926 | 0.941 | 0.804 [0.756, 0.847] | 0.863 | 0.852 |
| 2 | 13,471 | 0.267 | 0.957 [0.943, 0.969] | 0.912 | 0.941 | 0.774 [0.717, 0.821] | 0.866 | 0.825 |
| 3 | 13,471 | 0.267 | 0.949 [0.933, 0.961] | 0.899 | 0.941 | 0.765 [0.712, 0.809] | 0.875 | 0.799 |
| 4 | 13,471 | 0.267 | 0.942 [0.925, 0.957] | 0.892 | 0.941 | 0.752 [0.700, 0.797] | 0.884 | 0.787 |

**Reading it (honestly).** All-sample AUC is high but autocorrelation-dominated - persistence scores nearly as well, so it is *not* the result. The decision-relevant signal is **onset-AUC** (currently-clear lakes), where persistence has no skill by construction. The lean model shows genuine onset skill (well above 0.5), but a per-lake seasonal **climatology - itself only a baseline - is competitive-to-better** on the onset alert. So this 2-feature model's value is *simplicity + explainability while staying competitive*, not beating every baseline; a richer real-time-CyAN ladder is what pushes onset skill higher in the full study. Correlation, not causation.
