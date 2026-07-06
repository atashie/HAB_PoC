# Exp 3 - feature-level greedy backward ablation, selection metric = ONSET (lean=2 of 44 feats; TOL=0.005)

Split train<2022-07 / val[2022-07,2024-07) / **test>=2024-07** (~60/20/20, 2yr); fit train, threshold+early-stop on val, **refit train+val**, predict test. `valAUC-testAUC` = in-sample(val, from the refit) minus held-out(test) -- an optimism gap, NOT a clean val->test generalization gap. `AUC_within` = median per-lake AUC (within-lake temporal skill); `AUC_within_n` = # qualifying lakes (small n => unstable). `flipMCC_h0..4` = all transitions per lead. **onsetAUC/onsetMCC_h1 = the EARLY-WARNING skill** (among currently-CLEAR lake-weeks, predict bloom next); offsetMCC = pers=1->clear. **EPA rows: shared FL test weeks, at BOTH @0.50 (acc-opt default) and @0.10 (EPA's published health-protective cutoff); threshold-free cols identical across the two; indicative** vs full-test rows (n_shared) -- strict head-to-head in `epa_headtohead.md`. Our target IS EPA's own event (median CyAN DN>=130 == WHO AL1, pinned from Schaeffer's deposited code) -> apples-to-apples. EPA prob is a fixed current-week nowcast held constant across h0..4 (flatters EPA at longer leads).

| config | AUC-ROC | AUC-PR | Brier | MCC | AUC_within | AUC_within_n | valAUC-testAUC | flipMCC_h0 | flipMCC_h1 | flipMCC_h2 | flipMCC_h3 | flipMCC_h4 | onsetAUC_h1 | onsetMCC_h1 | offsetMCC_h1 | n_shared |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | 0.926 | 0.825 | 0.057 | 0.853 | 0.728 | 71 |  | -1.000 | -1.000 | -1.000 | -1.000 | -1.000 | 0.500 | 0.000 | 0.000 |  |
| climatology | 0.936 | 0.859 | 0.085 | 0.719 | 0.763 | 71 |  | 0.013 | 0.044 | 0.055 | 0.064 | 0.091 | 0.851 | 0.323 | 0.282 |  |
| fusion_full+clim (full) | histgbm | 0.980 | 0.953 | 0.043 | 0.861 | 0.897 | 71 | 0.016 | -0.477 | -0.303 | -0.308 | -0.192 | -0.123 | 0.929 | 0.466 | 0.325 |  |
| fusion_full+clim (full) | xgboost | 0.984 | 0.960 | 0.043 | 0.858 | 0.902 | 71 | 0.005 | -0.572 | -0.408 | -0.363 | -0.270 | -0.192 | 0.940 | 0.437 | 0.273 |  |
| fusion_full+clim (full) | logistic | 0.983 | 0.955 | 0.043 | 0.856 | 0.904 | 71 | -0.001 | -0.612 | -0.512 | -0.381 | -0.325 | -0.257 | 0.931 | 0.377 | 0.266 |  |
| greedy_lean | histgbm | 0.982 | 0.958 | 0.042 | 0.855 | 0.866 | 71 | -0.000 | -0.688 | -0.680 | -0.607 | -0.531 | -0.481 | 0.916 | 0.314 | 0.197 |  |
| greedy_lean | xgboost | 0.981 | 0.952 | 0.044 | 0.852 | 0.867 | 71 | -0.003 | -0.703 | -0.658 | -0.634 | -0.588 | -0.567 | 0.915 | 0.276 | 0.238 |  |
| greedy_lean | logistic | 0.970 | 0.937 | 0.047 | 0.853 | 0.881 | 71 | -0.006 | -0.877 | -0.916 | -0.947 | -0.820 | -0.836 | 0.823 | 0.158 | 0.099 |  |
| EPA_forecast @0.50 (acc-opt) | 0.931 | 0.854 | 0.105 | 0.636 | 0.498 | 64 |  | 0.026 | 0.026 | 0.008 | 0.004 | -0.005 | 0.831 | 0.233 | 0.256 | 6204.000 |
| EPA_forecast @0.10 (deployed) | 0.931 | 0.854 | 0.105 | 0.672 | 0.498 | 64 |  | -0.032 | -0.059 | -0.078 | -0.104 | -0.138 | 0.831 | 0.248 | 0.261 | 6204.000 |
