# Held-out evaluation - lean 2-feature model vs. baselines

Features: `cyan_median + area_sqkm`  |  target: median CyAN DN >= 130 (WHO AL1)  |  test = target week >= 2024-07-01.
AUC 95% CIs (brackets) are block-bootstrapped by lake.

### A. Ranking - all-sample AUC-ROC

| h | test base rate | lean AUC [95% CI] | persistence | climatology |
|--:|--:|--|--:|--:|
| 0 | 0.267 | 0.980 [0.973, 0.987] | 0.946 | 0.941 |
| 1 | 0.267 | 0.968 [0.958, 0.977] | 0.926 | 0.941 |
| 2 | 0.267 | 0.957 [0.943, 0.969] | 0.912 | 0.941 |
| 3 | 0.267 | 0.949 [0.933, 0.961] | 0.899 | 0.941 |
| 4 | 0.267 | 0.942 [0.925, 0.957] | 0.892 | 0.941 |

### B. Early warning - onset-AUC (currently-clear lakes only)

| h | onset base rate | lean onset-AUC [95% CI] | climatology onset-AUC [95% CI] |
|--:|--:|--|--|
| 0 | 0.029 | 0.836 [0.781, 0.881] | 0.851 [0.810, 0.889] |
| 1 | 0.040 | 0.804 [0.756, 0.847] | 0.863 [0.823, 0.901] |
| 2 | 0.048 | 0.774 [0.717, 0.821] | 0.866 [0.825, 0.904] |
| 3 | 0.055 | 0.765 [0.712, 0.809] | 0.875 [0.832, 0.914] |
| 4 | 0.059 | 0.752 [0.700, 0.797] | 0.884 [0.844, 0.919] |

### C. Operating point - MCC at the val-tuned threshold

| h | lean MCC | persistence MCC | climatology MCC |
|--:|--:|--:|--:|
| 0 | 0.894 | 0.893 | 0.731 |
| 1 | 0.851 | 0.853 | 0.731 |
| 2 | 0.825 | 0.825 | 0.732 |
| 3 | 0.797 | 0.800 | 0.731 |
| 4 | 0.787 | 0.786 | 0.730 |

**Reading it (honestly).**
- **All-sample AUC (A) is autocorrelation-dominated** - persistence scores nearly as well, so it is *not* the result.
- **onset-AUC (B) is the decision-relevant metric** (persistence has no skill on currently-clear lakes by construction). The lean model has genuine onset skill, but a per-lake seasonal **climatology - itself only a baseline - is competitive-to-better** (tied at short lead, ahead at longer lead). Note this is partly *structural*: climatology depends only on the target week's calendar position, so it is **horizon-invariant and pays no lead-time penalty**, while the lean model's real-time feature goes stale with lead. The onset subset is also small and imbalanced (base rate ~3-6%, rising with h), so each row scores a slightly different task.
- **At the operating point (C), persistence matches the lean model** on MCC - the 2-feature model earns no unique thresholded edge. Thresholds are tuned on validation (by F1), never on test.
- The target **base rate drifts up** over the record (train ~0.22 -> test ~0.27); reported as a limitation, not corrected for.

This 2-feature model's value is **simplicity + explainability while staying competitive**, not beating every baseline; the richer real-time-CyAN ladder in `../models/` is what pushes onset skill higher. The label is a satellite realization, not toxin. Correlation, not causation.
