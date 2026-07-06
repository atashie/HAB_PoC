# Exp 4b - C1 decomposition: real-time CyAN vs `clim` (per-lake base rate)

Grouped permutation (same protocol as `exp_perm_importance.py`) of SEMANTIC sub-groups inside the dominant CyAN+clim cluster, in the fitted **fusion_full+clim** model on held-out test, 20 shuffles. **Δ = baseline − permuted** (mean ± std). The honesty question: is the model's skill from the GENERALIZABLE real-time CyAN signal, or from PER-LAKE MEMORIZATION via `clim`?

> **Read the GROUP TOTALS** — `ALL CyAN NO clim` vs `clim ONLY`. Sub-groups inside a correlated cluster under-credit each other (redundancy), so the finer splits (current / lags / state) are **lower bounds**, not additive shares. std = shuffle variability only (not lake/bootstrap uncertainty).

## histgbm — baseline onsetMCC=0.466, AUC_within=0.897, pooledAUC=0.980 (thr=0.300)

| sub-group (within CyAN+clim) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |
| --- | --- | --- | --- |
| clim ONLY (per-lake base rate) | +0.351 ± 0.016 | +0.240 ± 0.013 | +0.2595 ± 0.0045 |
| CyAN current-week obs (median/mean/sd) | +0.214 ± 0.011 | +0.127 ± 0.010 | +0.0290 ± 0.0007 |
| CyAN antecedent lags | +0.091 ± 0.011 | +0.019 ± 0.008 | +0.0048 ± 0.0002 |
| CyAN bloom-state flags | +0.006 ± 0.004 | +0.000 ± 0.002 | +0.0001 ± 0.0000 |
| CyAN data-quality (gap/valid_frac) | +0.004 ± 0.004 | -0.000 ± 0.001 | +0.0001 ± 0.0000 |
| ALL CyAN, NO clim (15 feat) | +0.300 ± 0.011 | +0.240 ± 0.014 | +0.0822 ± 0.0012 |
| ALL CyAN + clim (reference = C1-ish) | +0.466 ± 0.007 | +0.374 ± 0.013 | +0.4678 ± 0.0042 |

## xgboost — baseline onsetMCC=0.437, AUC_within=0.902, pooledAUC=0.984 (thr=0.300)

| sub-group (within CyAN+clim) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |
| --- | --- | --- | --- |
| clim ONLY (per-lake base rate) | +0.321 ± 0.011 | +0.189 ± 0.012 | +0.1119 ± 0.0019 |
| CyAN current-week obs (median/mean/sd) | +0.203 ± 0.014 | +0.147 ± 0.012 | +0.0323 ± 0.0008 |
| CyAN antecedent lags | +0.043 ± 0.010 | +0.008 ± 0.006 | +0.0037 ± 0.0002 |
| CyAN bloom-state flags | +0.002 ± 0.009 | +0.006 ± 0.004 | +0.0017 ± 0.0001 |
| CyAN data-quality (gap/valid_frac) | -0.002 ± 0.002 | +0.002 ± 0.002 | +0.0000 ± 0.0000 |
| ALL CyAN, NO clim (15 feat) | +0.274 ± 0.011 | +0.274 ± 0.017 | +0.1402 ± 0.0024 |
| ALL CyAN + clim (reference = C1-ish) | +0.438 ± 0.007 | +0.384 ± 0.014 | +0.4529 ± 0.0045 |

## logistic — baseline onsetMCC=0.377, AUC_within=0.904, pooledAUC=0.983 (thr=0.300)

| sub-group (within CyAN+clim) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |
| --- | --- | --- | --- |
| clim ONLY (per-lake base rate) | +0.213 ± 0.015 | +0.091 ± 0.009 | +0.0204 ± 0.0005 |
| CyAN current-week obs (median/mean/sd) | +0.137 ± 0.011 | +0.195 ± 0.014 | +0.0487 ± 0.0012 |
| CyAN antecedent lags | +0.017 ± 0.010 | +0.026 ± 0.006 | +0.0022 ± 0.0002 |
| CyAN bloom-state flags | -0.008 ± 0.011 | +0.038 ± 0.008 | +0.0043 ± 0.0004 |
| CyAN data-quality (gap/valid_frac) | -0.001 ± 0.002 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| ALL CyAN, NO clim (15 feat) | +0.339 ± 0.008 | +0.323 ± 0.015 | +0.2335 ± 0.0035 |
| ALL CyAN + clim (reference = C1-ish) | +0.374 ± 0.007 | +0.393 ± 0.011 | +0.4379 ± 0.0053 |

> **Interpretation key:** if `ALL CyAN NO clim` ≈ the full C1 drop while `clim ONLY` is small, the model is a **generalizable real-time-CyAN** model and clim is NOT load-bearing (cross-check: block ablation `-clim` barely moves onsetMCC). If `clim ONLY` is large, the model leans on per-lake base-rate memorization.
