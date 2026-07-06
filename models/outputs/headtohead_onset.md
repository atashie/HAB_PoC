# Positive-flip (ONSET) head-to-head -- shared FL 2025 EPA COMID-weeks, horizons 0-4

Shared test set (h=1): **4,527 lake-weeks** (132 lakes x 35 weeks); base rate 28.8%; **3,239 currently-clear** weeks carry the onset test.

**ONSET / positive-flip** = restrict to currently-CLEAR weeks (persistence==0); score flagging the ones that BECOME a bloom. Distinct from the both-direction transition/flip metric (target != persistence) in `epa_headtohead.md`. Threshold-free cols reproduce the epa_headtohead W-2/h1 values (consistency check). Operating: in-sample F1 thresholds (models) / fixed 0.10 & 0.50 (EPA). EPA prob is a fixed current-week nowcast held constant across h (flatters EPA at longer leads).

## Baselines @ h=1 (the bar to clear) -- all-sample + ONSET

| predictor | AUC-ROC | AUC-PR | Brier | MCC | Acc | onset-AUC | onset-MCC | onset-Recall | n_onset |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | 0.918 | 0.818 | 0.066 | 0.838 | 0.934 | 0.5 | 0.0 | 0.0 | 158 |
| climatology | 0.955 | 0.895 | 0.081 | 0.752 | 0.896 | 0.896 | 0.388 | 0.601 | 158 |
| CyAN-ladder | 0.982 | 0.951 | 0.049 | 0.847 | 0.937 | 0.943 | 0.351 | 0.222 | 158 |
| EPA @0.10 | 0.928 | 0.851 | 0.101 | 0.647 | 0.834 | 0.818 | 0.241 | 0.595 | 158 |
| EPA @0.50 | 0.928 | 0.851 | 0.101 | 0.644 | 0.86 | 0.818 | 0.248 | 0.329 | 158 |

## Horizon curve h=0..4 -- AUC-ROC (all weeks) + ONSET-MCC (positive flips), 5 model classes

| h | model | AUC-ROC | onset-MCC | onset-AUC | n_onset |
| --- | --- | --- | --- | --- | --- |
| 0 | persistence | 0.937 | 0.0 | 0.5 | 120 |
| 0 | climatology | 0.955 | 0.324 | 0.893 | 120 |
| 0 | CyAN-ladder | 0.986 | 0.263 | 0.928 | 120 |
| 0 | fusion | 0.989 | 0.226 | 0.942 | 120 |
| 0 | EPA | 0.928 | 0.214 | 0.823 | 120 |
| 1 | persistence | 0.918 | 0.0 | 0.5 | 158 |
| 1 | climatology | 0.955 | 0.388 | 0.896 | 158 |
| 1 | CyAN-ladder | 0.982 | 0.351 | 0.943 | 158 |
| 1 | fusion | 0.983 | 0.474 | 0.944 | 158 |
| 1 | EPA | 0.928 | 0.241 | 0.818 | 158 |
| 2 | persistence | 0.897 | 0.0 | 0.5 | 199 |
| 2 | climatology | 0.955 | 0.44 | 0.904 | 199 |
| 2 | CyAN-ladder | 0.976 | 0.421 | 0.936 | 199 |
| 2 | fusion | 0.977 | 0.405 | 0.936 | 199 |
| 2 | EPA | 0.928 | 0.261 | 0.822 | 199 |
| 3 | persistence | 0.886 | 0.0 | 0.5 | 221 |
| 3 | climatology | 0.955 | 0.485 | 0.917 | 221 |
| 3 | CyAN-ladder | 0.973 | 0.461 | 0.938 | 221 |
| 3 | fusion | 0.972 | 0.461 | 0.925 | 221 |
| 3 | EPA | 0.928 | 0.294 | 0.838 | 221 |
| 4 | persistence | 0.879 | 0.0 | 0.5 | 236 |
| 4 | climatology | 0.955 | 0.516 | 0.922 | 236 |
| 4 | CyAN-ladder | 0.972 | 0.509 | 0.943 | 236 |
| 4 | fusion | 0.97 | 0.403 | 0.927 | 236 |
| 4 | EPA | 0.928 | 0.307 | 0.842 | 236 |
