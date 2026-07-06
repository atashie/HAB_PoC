# Exp 4 - correlation-clustered permutation importance (fusion_full+clim)

Features grouped into **27 clusters** by |Pearson r| on TRAIN (complete linkage, within-cluster |r| >= **0.7**), then each cluster is GROUPED-permuted together in the refit full model on **held-out test (>=2024-07)**, 20 shuffles. **Importance = baseline - permuted** (mean +/- std); higher = the cluster matters more. Clustering handles the heavy collinearity (per-feature importance would under-credit redundant twins). onsetMCC uses the model's val-tuned F1 threshold, held FIXED across permutations. Sorted by **onsetMCC importance** (the alert-decision metric).

## Clusters (from train correlation)

| # | n | block(s) | members |
| --- | --- | --- | --- |
| C1 | 11 | CYAN/clim | `cyan_median`, `cyan_mean`, `cyan_median_lag1`, `cyan_median_lag2`, `cyan_median_lag4`, `cyan_mean_lag1`, (+5 more) |
| C2 | 4 | SEASON/WEATHER | `woy_cos`, `wx_ssrd_trail_14d_mj`, `wx_ssrd_trail_30d_mj`, `wx_pet_hargreaves_mm` |
| C3 | 2 | STATIC | `tmp_dc_syr`, `for_pc_use` |
| C4 | 2 | SEASON/WEATHER | `woy_sin`, `wx_precip_trail_90d_mm` |
| C5 | 2 | INSITU | `wqp_TP_stale`, `wqp_chl_a_stale` |
| C6 | 2 | WEATHER | `wx_wspd_trail_14d_mean_ms`, `wx_calm_hours_trail_7d` |
| C7 | 1 | STATIC | `area_sqkm` |
| C8 | 1 | CYAN | `bloom_roll4_n` |
| C9 | 1 | STATIC | `crp_pc_use` |
| C10 | 1 | CYAN | `cyan_gap_weeks_at_cutoff` |
| C11 | 1 | CYAN | `cyan_sd` |
| C12 | 1 | CYAN | `cyan_sd_lag1` |
| C13 | 1 | STATIC | `hft_ix_u09` |
| C14 | 1 | STATIC | `inu_pc_umn` |
| C15 | 1 | INSITU | `nwis_gage_height_val` |
| C16 | 1 | INSITU | `nwis_water_temp_val` |
| C17 | 1 | STATIC | `pet_mm_syr` |
| C18 | 1 | CYAN | `valid_frac` |
| C19 | 1 | INSITU | `wqp_TP_val` |
| C20 | 1 | INSITU | `wqp_ammonia_val` |
| C21 | 1 | INSITU | `wqp_chl_a_val` |
| C22 | 1 | INSITU | `wqp_orthoP_val` |
| C23 | 1 | INSITU | `wqp_water_temp_val` |
| C24 | 1 | WEATHER | `wx_gdd_trail_30d` |
| C25 | 1 | WEATHER | `wx_precip_trail_30d_mm` |
| C26 | 1 | WEATHER | `wx_spei_1` |
| C27 | 1 | WEATHER | `wx_spei_4` |

## histgbm — baseline: onsetMCC=0.466, AUC_within=0.897, pooledAUC=0.980, onsetAUC=0.929 (thr=0.300)

| cluster | n | block(s) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |
| --- | --- | --- | --- | --- | --- |
| C1 | 11 | CYAN/clim | +0.464 ± 0.007 | +0.375 ± 0.011 | +0.4659 ± 0.0042 |
| C11 | 1 | CYAN | +0.038 ± 0.006 | -0.001 ± 0.002 | +0.0006 ± 0.0001 |
| C2 | 4 | SEASON/WEATHER | +0.030 ± 0.009 | -0.001 ± 0.003 | +0.0001 ± 0.0001 |
| C4 | 2 | SEASON/WEATHER | +0.018 ± 0.006 | +0.001 ± 0.003 | +0.0002 ± 0.0001 |
| C7 | 1 | STATIC | +0.018 ± 0.006 | +0.002 ± 0.002 | +0.0002 ± 0.0001 |
| C5 | 2 | INSITU | +0.017 ± 0.007 | +0.001 ± 0.001 | +0.0002 ± 0.0001 |
| C6 | 2 | WEATHER | +0.016 ± 0.006 | -0.001 ± 0.002 | +0.0000 ± 0.0001 |
| C23 | 1 | INSITU | +0.014 ± 0.005 | -0.002 ± 0.002 | +0.0001 ± 0.0001 |
| C24 | 1 | WEATHER | +0.013 ± 0.007 | -0.001 ± 0.001 | +0.0002 ± 0.0001 |
| C21 | 1 | INSITU | +0.011 ± 0.007 | -0.001 ± 0.002 | +0.0003 ± 0.0001 |
| C26 | 1 | WEATHER | +0.009 ± 0.007 | -0.000 ± 0.003 | -0.0000 ± 0.0001 |
| C17 | 1 | STATIC | +0.009 ± 0.005 | -0.002 ± 0.002 | +0.0001 ± 0.0000 |
| C19 | 1 | INSITU | +0.008 ± 0.005 | -0.002 ± 0.002 | +0.0001 ± 0.0001 |
| C14 | 1 | STATIC | +0.005 ± 0.003 | -0.002 ± 0.002 | -0.0000 ± 0.0000 |
| C27 | 1 | WEATHER | +0.005 ± 0.007 | -0.001 ± 0.002 | +0.0001 ± 0.0000 |
| C15 | 1 | INSITU | +0.004 ± 0.003 | +0.000 ± 0.001 | -0.0001 ± 0.0001 |
| C18 | 1 | CYAN | +0.004 ± 0.003 | -0.000 ± 0.001 | +0.0001 ± 0.0000 |
| C20 | 1 | INSITU | +0.004 ± 0.005 | -0.002 ± 0.002 | +0.0002 ± 0.0001 |
| C25 | 1 | WEATHER | +0.003 ± 0.006 | -0.004 ± 0.002 | -0.0000 ± 0.0001 |
| C22 | 1 | INSITU | +0.002 ± 0.006 | +0.001 ± 0.002 | +0.0001 ± 0.0000 |
| C12 | 1 | CYAN | +0.001 ± 0.004 | -0.001 ± 0.002 | +0.0002 ± 0.0001 |
| C8 | 1 | CYAN | +0.000 ± 0.000 | +0.000 ± 0.000 | -0.0000 ± 0.0000 |
| C10 | 1 | CYAN | +0.000 ± 0.000 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| C9 | 1 | STATIC | -0.000 ± 0.004 | -0.000 ± 0.001 | +0.0001 ± 0.0000 |
| C16 | 1 | INSITU | -0.000 ± 0.001 | -0.000 ± 0.001 | -0.0002 ± 0.0000 |
| C13 | 1 | STATIC | -0.002 ± 0.004 | -0.001 ± 0.001 | +0.0000 ± 0.0000 |
| C3 | 2 | STATIC | -0.002 ± 0.005 | -0.003 ± 0.001 | +0.0000 ± 0.0000 |

## xgboost — baseline: onsetMCC=0.437, AUC_within=0.902, pooledAUC=0.984, onsetAUC=0.940 (thr=0.300)

| cluster | n | block(s) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |
| --- | --- | --- | --- | --- | --- |
| C1 | 11 | CYAN/clim | +0.437 ± 0.007 | +0.392 ± 0.011 | +0.4624 ± 0.0051 |
| C11 | 1 | CYAN | +0.027 ± 0.005 | +0.002 ± 0.002 | +0.0005 ± 0.0001 |
| C7 | 1 | STATIC | +0.018 ± 0.004 | -0.001 ± 0.002 | +0.0002 ± 0.0000 |
| C4 | 2 | SEASON/WEATHER | +0.017 ± 0.005 | -0.000 ± 0.001 | +0.0001 ± 0.0000 |
| C21 | 1 | INSITU | +0.016 ± 0.006 | +0.002 ± 0.001 | +0.0002 ± 0.0001 |
| C2 | 4 | SEASON/WEATHER | +0.007 ± 0.006 | +0.001 ± 0.003 | +0.0002 ± 0.0001 |
| C25 | 1 | WEATHER | +0.007 ± 0.006 | +0.000 ± 0.001 | +0.0001 ± 0.0000 |
| C6 | 2 | WEATHER | +0.006 ± 0.003 | -0.000 ± 0.002 | -0.0000 ± 0.0000 |
| C9 | 1 | STATIC | +0.005 ± 0.003 | +0.000 ± 0.000 | +0.0001 ± 0.0000 |
| C23 | 1 | INSITU | +0.005 ± 0.004 | -0.001 ± 0.001 | -0.0000 ± 0.0000 |
| C12 | 1 | CYAN | +0.004 ± 0.002 | -0.001 ± 0.002 | +0.0001 ± 0.0001 |
| C27 | 1 | WEATHER | +0.003 ± 0.005 | -0.001 ± 0.001 | +0.0000 ± 0.0000 |
| C3 | 2 | STATIC | +0.003 ± 0.003 | -0.001 ± 0.001 | -0.0000 ± 0.0000 |
| C5 | 2 | INSITU | +0.002 ± 0.004 | +0.003 ± 0.003 | +0.0001 ± 0.0000 |
| C16 | 1 | INSITU | +0.002 ± 0.002 | +0.001 ± 0.002 | +0.0001 ± 0.0000 |
| C19 | 1 | INSITU | +0.001 ± 0.004 | +0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C26 | 1 | WEATHER | +0.000 ± 0.003 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| C13 | 1 | STATIC | +0.000 ± 0.000 | +0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C8 | 1 | CYAN | +0.000 ± 0.000 | -0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C10 | 1 | CYAN | +0.000 ± 0.000 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| C22 | 1 | INSITU | -0.000 ± 0.001 | -0.001 ± 0.002 | +0.0000 ± 0.0000 |
| C17 | 1 | STATIC | -0.000 ± 0.001 | +0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C15 | 1 | INSITU | -0.001 ± 0.001 | +0.001 ± 0.001 | +0.0000 ± 0.0000 |
| C20 | 1 | INSITU | -0.001 ± 0.002 | -0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C24 | 1 | WEATHER | -0.001 ± 0.002 | +0.001 ± 0.000 | +0.0000 ± 0.0000 |
| C14 | 1 | STATIC | -0.001 ± 0.001 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| C18 | 1 | CYAN | -0.002 ± 0.004 | +0.002 ± 0.002 | +0.0000 ± 0.0000 |

## logistic — baseline: onsetMCC=0.377, AUC_within=0.904, pooledAUC=0.983, onsetAUC=0.931 (thr=0.300)

| cluster | n | block(s) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |
| --- | --- | --- | --- | --- | --- |
| C1 | 11 | CYAN/clim | +0.372 ± 0.007 | +0.399 ± 0.013 | +0.4464 ± 0.0051 |
| C15 | 1 | INSITU | +0.020 ± 0.006 | +0.012 ± 0.006 | +0.0016 ± 0.0004 |
| C5 | 2 | INSITU | +0.007 ± 0.006 | +0.006 ± 0.003 | +0.0004 ± 0.0002 |
| C19 | 1 | INSITU | +0.006 ± 0.003 | +0.000 ± 0.001 | +0.0001 ± 0.0001 |
| C6 | 2 | WEATHER | +0.006 ± 0.003 | -0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C2 | 4 | SEASON/WEATHER | +0.005 ± 0.005 | +0.002 ± 0.003 | +0.0001 ± 0.0001 |
| C27 | 1 | WEATHER | +0.005 ± 0.004 | +0.001 ± 0.002 | +0.0002 ± 0.0000 |
| C22 | 1 | INSITU | +0.004 ± 0.002 | +0.000 ± 0.001 | -0.0000 ± 0.0000 |
| C14 | 1 | STATIC | +0.003 ± 0.006 | +0.002 ± 0.003 | +0.0003 ± 0.0001 |
| C24 | 1 | WEATHER | +0.002 ± 0.009 | +0.013 ± 0.006 | +0.0009 ± 0.0001 |
| C21 | 1 | INSITU | +0.002 ± 0.004 | -0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C26 | 1 | WEATHER | +0.002 ± 0.002 | -0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C9 | 1 | STATIC | +0.002 ± 0.001 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| C25 | 1 | WEATHER | +0.001 ± 0.007 | +0.002 ± 0.003 | +0.0002 ± 0.0001 |
| C10 | 1 | CYAN | +0.000 ± 0.000 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| C7 | 1 | STATIC | -0.000 ± 0.000 | -0.000 ± 0.000 | -0.0000 ± 0.0000 |
| C18 | 1 | CYAN | -0.000 ± 0.002 | +0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C8 | 1 | CYAN | -0.000 ± 0.002 | +0.001 ± 0.002 | -0.0000 ± 0.0000 |
| C13 | 1 | STATIC | -0.001 ± 0.001 | +0.000 ± 0.000 | +0.0000 ± 0.0000 |
| C12 | 1 | CYAN | -0.001 ± 0.007 | +0.002 ± 0.003 | +0.0004 ± 0.0001 |
| C11 | 1 | CYAN | -0.002 ± 0.009 | +0.006 ± 0.003 | +0.0000 ± 0.0001 |
| C23 | 1 | INSITU | -0.002 ± 0.004 | -0.001 ± 0.002 | -0.0002 ± 0.0000 |
| C16 | 1 | INSITU | -0.002 ± 0.003 | -0.000 ± 0.001 | -0.0000 ± 0.0000 |
| C4 | 2 | SEASON/WEATHER | -0.006 ± 0.007 | +0.005 ± 0.003 | +0.0002 ± 0.0001 |
| C17 | 1 | STATIC | -0.009 ± 0.003 | -0.000 ± 0.001 | +0.0000 ± 0.0000 |
| C20 | 1 | INSITU | -0.010 ± 0.005 | +0.003 ± 0.003 | +0.0003 ± 0.0001 |
| C3 | 2 | STATIC | -0.014 ± 0.005 | +0.003 ± 0.003 | +0.0004 ± 0.0001 |

> Δ is the metric drop when the cluster is scrambled. ~0 or negative = the cluster adds nothing (or noise) to that metric in the full model. A cluster important for onsetMCC but ~0 for pooled_AUC = it helps the ALERT decision but not overall ranking.
