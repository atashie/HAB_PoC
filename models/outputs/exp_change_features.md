# Exp 1 - weather change/trend features vs onsets (flips)

Split train<2022-07 / val[2022-07,2024-07) / **test>=2024-07** (~60/20/20, 2yr); fit train, threshold+early-stop on val, **refit train+val**, predict test. `valAUC-testAUC` = in-sample(val, from the refit) minus held-out(test) -- an optimism gap, NOT a clean val->test generalization gap. `AUC_within` = median per-lake AUC (within-lake temporal skill); `AUC_within_n` = # qualifying lakes (small n => unstable). `flipMCC_h0..4` = all transitions per lead. **onsetAUC/onsetMCC_h1 = the EARLY-WARNING skill** (among currently-CLEAR lake-weeks, predict bloom next); offsetMCC = pers=1->clear. **EPA rows: shared FL test weeks, at BOTH @0.50 (acc-opt default) and @0.10 (EPA's published health-protective cutoff); threshold-free cols identical across the two; indicative** vs full-test rows (n_shared) -- strict head-to-head in `epa_headtohead.md`. Our target IS EPA's own event (median CyAN DN>=130 == WHO AL1, pinned from Schaeffer's deposited code) -> apples-to-apples. EPA prob is a fixed current-week nowcast held constant across h0..4 (flatters EPA at longer leads).

| config | AUC-ROC | AUC-PR | Brier | MCC | AUC_within | AUC_within_n | valAUC-testAUC | flipMCC_h0 | flipMCC_h1 | flipMCC_h2 | flipMCC_h3 | flipMCC_h4 | onsetAUC_h1 | onsetMCC_h1 | offsetMCC_h1 | n_shared |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | 0.926 | 0.825 | 0.057 | 0.853 | 0.728 | 71 |  | -1.000 | -1.000 | -1.000 | -1.000 | -1.000 | 0.500 | 0.000 | 0.000 |  |
| climatology | 0.936 | 0.859 | 0.085 | 0.719 | 0.763 | 71 |  | 0.013 | 0.044 | 0.055 | 0.064 | 0.091 | 0.851 | 0.323 | 0.282 |  |
| fusion_full | histgbm | 0.985 | 0.963 | 0.040 | 0.863 | 0.893 | 71 | 0.009 | -0.631 | -0.506 | -0.421 | -0.359 | -0.286 | 0.935 | 0.398 | 0.293 |  |
| fusion_full | xgboost | 0.985 | 0.963 | 0.040 | 0.859 | 0.893 | 71 | 0.005 | -0.696 | -0.621 | -0.502 | -0.460 | -0.405 | 0.933 | 0.280 | 0.314 |  |
| fusion_full | logistic | 0.980 | 0.948 | 0.044 | 0.851 | 0.884 | 71 | -0.004 | -0.779 | -0.711 | -0.711 | -0.646 | -0.711 | 0.908 | 0.292 | 0.169 |  |
| fusion_full+clim | histgbm | 0.980 | 0.953 | 0.043 | 0.861 | 0.897 | 71 | 0.016 | -0.477 | -0.303 | -0.308 | -0.192 | -0.123 | 0.929 | 0.466 | 0.325 |  |
| fusion_full+clim | xgboost | 0.984 | 0.960 | 0.043 | 0.858 | 0.902 | 71 | 0.005 | -0.572 | -0.408 | -0.363 | -0.270 | -0.192 | 0.940 | 0.437 | 0.273 |  |
| fusion_full+clim | logistic | 0.983 | 0.955 | 0.043 | 0.856 | 0.904 | 71 | -0.001 | -0.612 | -0.512 | -0.381 | -0.325 | -0.257 | 0.931 | 0.377 | 0.266 |  |
| fusion_full+clim+chg | histgbm | 0.980 | 0.953 | 0.043 | 0.860 | 0.906 | 71 | 0.016 | -0.477 | -0.346 | -0.316 | -0.228 | -0.151 | 0.931 | 0.443 | 0.322 |  |
| fusion_full+clim+chg | xgboost | 0.983 | 0.959 | 0.043 | 0.857 | 0.898 | 71 | 0.006 | -0.561 | -0.415 | -0.293 | -0.317 | -0.178 | 0.936 | 0.434 | 0.263 |  |
| fusion_full+clim+chg | logistic | 0.983 | 0.955 | 0.043 | 0.856 | 0.904 | 71 | -0.001 | -0.605 | -0.516 | -0.399 | -0.322 | -0.252 | 0.931 | 0.369 | 0.274 |  |
| fusion_nocyan+clim | histgbm | 0.951 | 0.890 | 0.078 | 0.723 | 0.750 | 71 | 0.043 | -0.000 | 0.017 | 0.010 | 0.014 | 0.081 | 0.890 | 0.339 | 0.251 |  |
| fusion_nocyan+clim | xgboost | 0.958 | 0.896 | 0.076 | 0.739 | 0.772 | 71 | 0.022 | 0.003 | 0.014 | 0.026 | 0.052 | 0.078 | 0.901 | 0.330 | 0.295 |  |
| fusion_nocyan+clim | logistic | 0.955 | 0.891 | 0.081 | 0.751 | 0.751 | 71 | 0.011 | 0.008 | 0.036 | 0.058 | 0.064 | 0.088 | 0.886 | 0.353 | 0.304 |  |
| fusion_nocyan+clim+chg | histgbm | 0.956 | 0.894 | 0.076 | 0.733 | 0.780 | 71 | 0.039 | -0.000 | 0.032 | 0.006 | 0.063 | 0.054 | 0.900 | 0.347 | 0.270 |  |
| fusion_nocyan+clim+chg | xgboost | 0.958 | 0.895 | 0.077 | 0.738 | 0.758 | 71 | 0.022 | -0.008 | 0.009 | 0.041 | 0.058 | 0.086 | 0.902 | 0.329 | 0.291 |  |
| fusion_nocyan+clim+chg | logistic | 0.954 | 0.891 | 0.081 | 0.750 | 0.758 | 71 | 0.012 | -0.006 | 0.031 | 0.052 | 0.066 | 0.079 | 0.886 | 0.347 | 0.307 |  |
| EPA_forecast @0.50 (acc-opt) | 0.931 | 0.854 | 0.105 | 0.636 | 0.498 | 64 |  | 0.026 | 0.026 | 0.008 | 0.004 | -0.005 | 0.831 | 0.233 | 0.256 | 6204.000 |
| EPA_forecast @0.10 (deployed) | 0.931 | 0.854 | 0.105 | 0.672 | 0.498 | 64 |  | -0.032 | -0.059 | -0.078 | -0.104 | -0.138 | 0.831 | 0.248 | 0.261 | 6204.000 |
