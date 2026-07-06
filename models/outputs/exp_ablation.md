# Exp 2 - feature ablation (drop-one block) + overfitting focus (HistGBM)

Split train<2022-07 / val[2022-07,2024-07) / **test>=2024-07** (~60/20/20, 2yr); fit train, threshold+early-stop on val, **refit train+val**, predict test. `valAUC-testAUC` = in-sample(val, from the refit) minus held-out(test) -- an optimism gap, NOT a clean val->test generalization gap. `AUC_within` = median per-lake AUC (within-lake temporal skill); `AUC_within_n` = # qualifying lakes (small n => unstable). `flipMCC_h0..4` = all transitions per lead. **onsetAUC/onsetMCC_h1 = the EARLY-WARNING skill** (among currently-CLEAR lake-weeks, predict bloom next); offsetMCC = pers=1->clear. **EPA rows: shared FL test weeks, at BOTH @0.50 (acc-opt default) and @0.10 (EPA's published health-protective cutoff); threshold-free cols identical across the two; indicative** vs full-test rows (n_shared) -- strict head-to-head in `epa_headtohead.md`. Our target IS EPA's own event (median CyAN DN>=130 == WHO AL1, pinned from Schaeffer's deposited code) -> apples-to-apples. EPA prob is a fixed current-week nowcast held constant across h0..4 (flatters EPA at longer leads).

| config | AUC-ROC | AUC-PR | Brier | MCC | AUC_within | AUC_within_n | valAUC-testAUC | flipMCC_h0 | flipMCC_h1 | flipMCC_h2 | flipMCC_h3 | flipMCC_h4 | onsetAUC_h1 | onsetMCC_h1 | offsetMCC_h1 | n_shared |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | 0.926 | 0.825 | 0.057 | 0.853 | 0.728 | 71 |  | -1.000 | -1.000 | -1.000 | -1.000 | -1.000 | 0.500 | 0.000 | 0.000 |  |
| climatology | 0.936 | 0.859 | 0.085 | 0.719 | 0.763 | 71 |  | 0.013 | 0.044 | 0.055 | 0.064 | 0.091 | 0.851 | 0.323 | 0.282 |  |
| fusion_full (all) | histgbm | 0.985 | 0.963 | 0.040 | 0.863 | 0.893 | 71 | 0.009 | -0.631 | -0.506 | -0.421 | -0.359 | -0.286 | 0.935 | 0.398 | 0.293 |  |
| fusion_full -CYAN | histgbm | 0.944 | 0.867 | 0.086 | 0.704 | 0.691 | 71 | 0.047 | 0.026 | 0.011 | -0.008 | 0.027 | 0.062 | 0.878 | 0.312 | 0.248 |  |
| fusion_full -STATIC | histgbm | 0.983 | 0.959 | 0.042 | 0.857 | 0.890 | 71 | 0.009 | -0.654 | -0.611 | -0.497 | -0.464 | -0.421 | 0.926 | 0.310 | 0.272 |  |
| fusion_full -SEASON | histgbm | 0.985 | 0.962 | 0.040 | 0.860 | 0.898 | 71 | 0.010 | -0.663 | -0.507 | -0.413 | -0.350 | -0.293 | 0.934 | 0.355 | 0.322 |  |
| fusion_full -WEATHER | histgbm | 0.985 | 0.963 | 0.040 | 0.861 | 0.902 | 71 | 0.009 | -0.632 | -0.486 | -0.402 | -0.337 | -0.267 | 0.934 | 0.416 | 0.268 |  |
| fusion_full -INSITU | histgbm | 0.985 | 0.964 | 0.039 | 0.863 | 0.892 | 71 | 0.008 | -0.649 | -0.543 | -0.419 | -0.348 | -0.309 | 0.936 | 0.371 | 0.298 |  |
| fusion_full+clim (all) | histgbm | 0.980 | 0.953 | 0.043 | 0.861 | 0.897 | 71 | 0.016 | -0.477 | -0.303 | -0.308 | -0.192 | -0.123 | 0.929 | 0.466 | 0.325 |  |
| fusion_full+clim -CYAN | histgbm | 0.951 | 0.890 | 0.078 | 0.723 | 0.750 | 71 | 0.043 | -0.000 | 0.017 | 0.010 | 0.014 | 0.081 | 0.890 | 0.339 | 0.251 |  |
| fusion_full+clim -STATIC | histgbm | 0.980 | 0.953 | 0.043 | 0.859 | 0.893 | 71 | 0.014 | -0.433 | -0.349 | -0.268 | -0.243 | -0.139 | 0.929 | 0.430 | 0.329 |  |
| fusion_full+clim -SEASON | histgbm | 0.980 | 0.953 | 0.043 | 0.852 | 0.894 | 71 | 0.017 | -0.491 | -0.319 | -0.271 | -0.205 | -0.151 | 0.930 | 0.464 | 0.260 |  |
| fusion_full+clim -WEATHER | histgbm | 0.981 | 0.954 | 0.043 | 0.858 | 0.897 | 71 | 0.012 | -0.430 | -0.344 | -0.310 | -0.195 | -0.112 | 0.933 | 0.449 | 0.300 |  |
| fusion_full+clim -INSITU | histgbm | 0.980 | 0.953 | 0.043 | 0.859 | 0.902 | 71 | 0.016 | -0.454 | -0.302 | -0.316 | -0.173 | -0.118 | 0.931 | 0.444 | 0.338 |  |
| fusion_full+clim -clim | histgbm | 0.985 | 0.963 | 0.040 | 0.863 | 0.893 | 71 | 0.009 | -0.631 | -0.506 | -0.421 | -0.359 | -0.286 | 0.935 | 0.398 | 0.293 |  |
| fusion_nocyan+clim (all) | histgbm | 0.951 | 0.890 | 0.078 | 0.723 | 0.750 | 71 | 0.043 | -0.000 | 0.017 | 0.010 | 0.014 | 0.081 | 0.890 | 0.339 | 0.251 |  |
| fusion_nocyan+clim -STATIC | histgbm | 0.954 | 0.892 | 0.077 | 0.734 | 0.764 | 71 | 0.040 | 0.003 | 0.024 | 0.028 | 0.042 | 0.064 | 0.893 | 0.347 | 0.267 |  |
| fusion_nocyan+clim -SEASON | histgbm | 0.952 | 0.891 | 0.077 | 0.728 | 0.765 | 71 | 0.042 | 0.015 | 0.021 | 0.012 | 0.039 | 0.062 | 0.891 | 0.348 | 0.253 |  |
| fusion_nocyan+clim -WEATHER | histgbm | 0.956 | 0.893 | 0.075 | 0.746 | 0.777 | 71 | 0.035 | -0.004 | 0.027 | 0.042 | 0.013 | 0.049 | 0.895 | 0.358 | 0.284 |  |
| fusion_nocyan+clim -INSITU | histgbm | 0.952 | 0.890 | 0.076 | 0.743 | 0.790 | 71 | 0.037 | 0.020 | 0.044 | 0.027 | 0.057 | 0.104 | 0.889 | 0.342 | 0.306 |  |
| fusion_nocyan+clim -clim | histgbm | 0.944 | 0.867 | 0.086 | 0.704 | 0.691 | 71 | 0.047 | 0.026 | 0.011 | -0.008 | 0.027 | 0.062 | 0.878 | 0.312 | 0.248 |  |
| EPA_forecast @0.50 (acc-opt) | 0.931 | 0.854 | 0.105 | 0.636 | 0.498 | 64 |  | 0.026 | 0.026 | 0.008 | 0.004 | -0.005 | 0.831 | 0.233 | 0.256 | 6204.000 |
| EPA_forecast @0.10 (deployed) | 0.931 | 0.854 | 0.105 | 0.672 | 0.498 | 64 |  | -0.032 | -0.059 | -0.078 | -0.104 | -0.138 | 0.831 | 0.248 | 0.261 | 6204.000 |
