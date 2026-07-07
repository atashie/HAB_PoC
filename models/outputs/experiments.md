# Experiment suite -- feature-suite x architecture grid (h=1, test = Jul2024-Jun2026)

Split: train <2022-07 / val 2022-07..2024-07 / **test >=2024-07 (2 yr)**; ~60/20/20 temporal. Threshold tuned on val; early stopping (HistGBM/XGBoost). Climatology = BASELINE. `fusion_nocyan` = the anti-persistence model (no antecedent CyAN levels). **`+clim` configs add per-lake climatology as a FEATURE** (reintroduces per-lake identity, D-35 -- trades generalizability for the seasonal onset signal; experiment). **Read AUC_within + flip_MCC** (flips = onsets/offsets, the hard case). Logistic is disadvantaged on sparse in-situ (needs imputation); GBDTs handle NaN natively.

## h=1 grid

| config | AUC-ROC | AUC-PR | Brier | MCC | AUC_within | flip_MCC | flip_AUC | n_flip | onset-MCC | onset-AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | 0.926 | 0.825 | 0.057 | 0.853 | 0.728 | -1.000 | 0.000 | 771 | 0.000 | 0.500 |
| climatology | 0.952 | 0.886 | 0.076 | 0.750 | 0.787 | 0.071 | 0.525 | 771 | 0.363 | 0.886 |
| lean | logistic | 0.970 | 0.937 | 0.047 | 0.853 | 0.881 | -0.916 | 0.009 | 771 | 0.158 | 0.823 |
| lean | histgbm | 0.982 | 0.958 | 0.042 | 0.855 | 0.866 | -0.680 | 0.076 | 771 | 0.314 | 0.916 |
| lean | xgboost | 0.981 | 0.952 | 0.044 | 0.852 | 0.867 | -0.658 | 0.080 | 771 | 0.276 | 0.915 |
| cyan_ladder | logistic | 0.979 | 0.949 | 0.044 | 0.849 | 0.886 | -0.787 | 0.035 | 771 | 0.223 | 0.898 |
| cyan_ladder | histgbm | 0.982 | 0.957 | 0.042 | 0.853 | 0.882 | -0.715 | 0.047 | 771 | 0.331 | 0.918 |
| cyan_ladder | xgboost | 0.982 | 0.957 | 0.042 | 0.852 | 0.888 | -0.771 | 0.043 | 771 | 0.273 | 0.919 |
| fusion_full | logistic | 0.980 | 0.948 | 0.044 | 0.851 | 0.884 | -0.711 | 0.059 | 771 | 0.292 | 0.908 |
| fusion_full | histgbm | 0.985 | 0.963 | 0.040 | 0.863 | 0.893 | -0.506 | 0.152 | 771 | 0.398 | 0.935 |
| fusion_full | xgboost | 0.985 | 0.963 | 0.040 | 0.859 | 0.893 | -0.621 | 0.093 | 771 | 0.280 | 0.933 |
| fusion_nocyan | logistic | 0.866 | 0.726 | 0.129 | 0.556 | 0.562 | -0.063 | 0.462 | 771 | 0.204 | 0.775 |
| fusion_nocyan | histgbm | 0.944 | 0.867 | 0.086 | 0.704 | 0.691 | 0.011 | 0.493 | 771 | 0.312 | 0.878 |
| fusion_nocyan | xgboost | 0.942 | 0.859 | 0.087 | 0.699 | 0.695 | -0.003 | 0.492 | 771 | 0.309 | 0.876 |
| cyan_ladder+clim | logistic | 0.983 | 0.955 | 0.043 | 0.859 | 0.905 | -0.525 | 0.150 | 771 | 0.375 | 0.929 |
| cyan_ladder+clim | histgbm | 0.980 | 0.952 | 0.043 | 0.856 | 0.896 | -0.404 | 0.249 | 771 | 0.409 | 0.927 |
| cyan_ladder+clim | xgboost | 0.984 | 0.960 | 0.043 | 0.856 | 0.898 | -0.489 | 0.211 | 771 | 0.358 | 0.940 |
| fusion_full+clim | logistic | 0.983 | 0.955 | 0.043 | 0.856 | 0.904 | -0.512 | 0.164 | 771 | 0.377 | 0.931 |
| fusion_full+clim | histgbm | 0.980 | 0.953 | 0.043 | 0.861 | 0.897 | -0.303 | 0.291 | 771 | 0.466 | 0.929 |
| fusion_full+clim | xgboost | 0.984 | 0.960 | 0.043 | 0.858 | 0.902 | -0.408 | 0.227 | 771 | 0.437 | 0.940 |
| fusion_nocyan+clim | logistic | 0.955 | 0.891 | 0.081 | 0.751 | 0.751 | 0.036 | 0.513 | 771 | 0.353 | 0.886 |
| fusion_nocyan+clim | histgbm | 0.951 | 0.890 | 0.078 | 0.723 | 0.750 | 0.017 | 0.509 | 771 | 0.339 | 0.890 |
| fusion_nocyan+clim | xgboost | 0.958 | 0.896 | 0.076 | 0.739 | 0.772 | 0.014 | 0.507 | 771 | 0.330 | 0.901 |

## Horizon curve h=0..4 (HistGBM; flip + onset)

| h | config | AUC-ROC | AUC_within | flip_MCC | flip_AUC | onset-MCC | onset-AUC |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | persistence | 0.947 | 0.818 | -1.000 | 0.000 | 0.000 | 0.500 |
| 0 | climatology | 0.952 | 0.787 | 0.029 | 0.506 | 0.286 | 0.876 |
| 0 | lean | 0.989 | 0.938 | -0.688 | 0.057 | 0.255 | 0.925 |
| 0 | cyan_ladder | 0.990 | 0.941 | -0.683 | 0.053 | 0.303 | 0.935 |
| 0 | fusion_full | 0.991 | 0.948 | -0.631 | 0.085 | 0.331 | 0.942 |
| 0 | fusion_nocyan | 0.947 | 0.686 | 0.026 | 0.493 | 0.286 | 0.877 |
| 0 | cyan_ladder+clim | 0.985 | 0.943 | -0.514 | 0.208 | 0.322 | 0.935 |
| 0 | fusion_full+clim | 0.985 | 0.945 | -0.477 | 0.215 | 0.336 | 0.934 |
| 0 | fusion_nocyan+clim | 0.954 | 0.769 | -0.000 | 0.501 | 0.267 | 0.882 |
| 1 | persistence | 0.926 | 0.728 | -1.000 | 0.000 | 0.000 | 0.500 |
| 1 | climatology | 0.952 | 0.787 | 0.071 | 0.525 | 0.363 | 0.886 |
| 1 | lean | 0.982 | 0.866 | -0.680 | 0.076 | 0.314 | 0.916 |
| 1 | cyan_ladder | 0.982 | 0.882 | -0.715 | 0.047 | 0.331 | 0.918 |
| 1 | fusion_full | 0.985 | 0.893 | -0.506 | 0.152 | 0.398 | 0.935 |
| 1 | fusion_nocyan | 0.944 | 0.691 | 0.011 | 0.493 | 0.312 | 0.878 |
| 1 | cyan_ladder+clim | 0.980 | 0.896 | -0.404 | 0.249 | 0.409 | 0.927 |
| 1 | fusion_full+clim | 0.980 | 0.897 | -0.303 | 0.291 | 0.466 | 0.929 |
| 1 | fusion_nocyan+clim | 0.951 | 0.750 | 0.017 | 0.509 | 0.339 | 0.890 |
| 2 | persistence | 0.911 | 0.677 | -1.000 | 0.000 | 0.000 | 0.500 |
| 2 | climatology | 0.952 | 0.787 | 0.090 | 0.539 | 0.401 | 0.894 |
| 2 | lean | 0.976 | 0.837 | -0.607 | 0.099 | 0.307 | 0.907 |
| 2 | cyan_ladder | 0.975 | 0.856 | -0.742 | 0.051 | 0.264 | 0.893 |
| 2 | fusion_full | 0.980 | 0.866 | -0.421 | 0.187 | 0.401 | 0.924 |
| 2 | fusion_nocyan | 0.946 | 0.694 | -0.008 | 0.488 | 0.339 | 0.884 |
| 2 | cyan_ladder+clim | 0.976 | 0.867 | -0.366 | 0.263 | 0.431 | 0.921 |
| 2 | fusion_full+clim | 0.977 | 0.871 | -0.308 | 0.305 | 0.432 | 0.927 |
| 2 | fusion_nocyan+clim | 0.953 | 0.753 | 0.010 | 0.518 | 0.376 | 0.895 |
| 3 | persistence | 0.899 | 0.629 | -1.000 | 0.000 | 0.000 | 0.500 |
| 3 | climatology | 0.952 | 0.787 | 0.116 | 0.554 | 0.450 | 0.904 |
| 3 | lean | 0.973 | 0.801 | -0.531 | 0.133 | 0.335 | 0.911 |
| 3 | cyan_ladder | 0.967 | 0.814 | -0.706 | 0.062 | 0.298 | 0.878 |
| 3 | fusion_full | 0.977 | 0.865 | -0.359 | 0.244 | 0.443 | 0.925 |
| 3 | fusion_nocyan | 0.947 | 0.704 | 0.027 | 0.504 | 0.388 | 0.897 |
| 3 | cyan_ladder+clim | 0.974 | 0.848 | -0.294 | 0.308 | 0.473 | 0.927 |
| 3 | fusion_full+clim | 0.972 | 0.843 | -0.192 | 0.354 | 0.491 | 0.927 |
| 3 | fusion_nocyan+clim | 0.953 | 0.745 | 0.014 | 0.529 | 0.407 | 0.910 |
| 4 | persistence | 0.892 | 0.601 | -1.000 | 0.000 | 0.000 | 0.500 |
| 4 | climatology | 0.952 | 0.787 | 0.150 | 0.574 | 0.476 | 0.909 |
| 4 | lean | 0.970 | 0.744 | -0.481 | 0.158 | 0.346 | 0.910 |
| 4 | cyan_ladder | 0.962 | 0.794 | -0.735 | 0.047 | 0.272 | 0.862 |
| 4 | fusion_full | 0.974 | 0.851 | -0.286 | 0.286 | 0.460 | 0.919 |
| 4 | fusion_nocyan | 0.949 | 0.690 | 0.062 | 0.525 | 0.413 | 0.900 |
| 4 | cyan_ladder+clim | 0.965 | 0.844 | -0.184 | 0.354 | 0.473 | 0.915 |
| 4 | fusion_full+clim | 0.970 | 0.851 | -0.123 | 0.400 | 0.466 | 0.925 |
| 4 | fusion_nocyan+clim | 0.954 | 0.758 | 0.081 | 0.562 | 0.434 | 0.912 |
