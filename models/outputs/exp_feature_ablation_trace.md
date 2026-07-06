# Exp 3 - feature-level greedy backward ablation (selection trace)

Start = fusion_full+clim (44 features). Greedy backward: at each step drop the single feature whose removal least hurts **validation** AUC at h=1, keep it dropped iff the reduced model stays within **TOL=0.001** of the full-model val AUC (`0.97073`). Val (not test) drives selection; clim/anom pseudo-features are train-only (leakage-safe). Final lean set evaluated unbiased on test below.

**Result: dropped 42 of 44 features with <0.001 val-AUC cost; 2 kept.**

## Elimination order

| step | dropped feature | block | val AUC | delta vs full | n kept |
| --- | --- | --- | --- | --- | --- |
| 0 | `(full model)` |  | 0.97073 | +0.00000 | 44 |
| 1 | `clim` | clim | 0.98009 | +0.00937 | 43 |
| 2 | `wx_ssrd_trail_30d_mj` | WEATHER | 0.98072 | +0.00999 | 42 |
| 3 | `bloom_state` | CYAN | 0.98072 | +0.00999 | 41 |
| 4 | `wqp_water_temp_val` | INSITU | 0.98063 | +0.00991 | 40 |
| 5 | `inu_pc_umn` | STATIC | 0.98069 | +0.00996 | 39 |
| 6 | `cyan_mean` | CYAN | 0.98064 | +0.00991 | 38 |
| 7 | `nwis_water_temp_val` | INSITU | 0.98079 | +0.01006 | 37 |
| 8 | `wx_gdd_trail_30d` | WEATHER | 0.98082 | +0.01009 | 36 |
| 9 | `wx_spei_4` | WEATHER | 0.98097 | +0.01025 | 35 |
| 10 | `wqp_chl_a_stale` | INSITU | 0.98104 | +0.01032 | 34 |
| 11 | `bloom_lag1` | CYAN | 0.98122 | +0.01050 | 33 |
| 12 | `cyan_gap_weeks_at_cutoff` | CYAN | 0.98122 | +0.01049 | 32 |
| 13 | `wx_precip_trail_90d_mm` | WEATHER | 0.98120 | +0.01047 | 31 |
| 14 | `bloom_roll4_n` | CYAN | 0.98131 | +0.01058 | 30 |
| 15 | `wx_calm_hours_trail_7d` | WEATHER | 0.98110 | +0.01038 | 29 |
| 16 | `tmp_dc_syr` | STATIC | 0.98114 | +0.01041 | 28 |
| 17 | `wx_wspd_trail_14d_mean_ms` | WEATHER | 0.98120 | +0.01048 | 27 |
| 18 | `for_pc_use` | STATIC | 0.98128 | +0.01056 | 26 |
| 19 | `wqp_chl_a_val` | INSITU | 0.98123 | +0.01051 | 25 |
| 20 | `wqp_ammonia_val` | INSITU | 0.98132 | +0.01060 | 24 |
| 21 | `bloom_state_ffill` | CYAN | 0.98134 | +0.01062 | 23 |
| 22 | `nwis_gage_height_val` | INSITU | 0.98123 | +0.01051 | 22 |
| 23 | `wqp_orthoP_val` | INSITU | 0.98124 | +0.01051 | 21 |
| 24 | `cyan_sd_lag1` | CYAN | 0.98109 | +0.01037 | 20 |
| 25 | `wqp_TP_stale` | INSITU | 0.98126 | +0.01054 | 19 |
| 26 | `cyan_median_lag4` | CYAN | 0.98112 | +0.01040 | 18 |
| 27 | `wx_ssrd_trail_14d_mj` | WEATHER | 0.98116 | +0.01043 | 17 |
| 28 | `crp_pc_use` | STATIC | 0.98099 | +0.01027 | 16 |
| 29 | `woy_sin` | SEASON | 0.98107 | +0.01034 | 15 |
| 30 | `hft_ix_u09` | STATIC | 0.98094 | +0.01021 | 14 |
| 31 | `wx_spei_1` | WEATHER | 0.98077 | +0.01004 | 13 |
| 32 | `wx_precip_trail_30d_mm` | WEATHER | 0.98054 | +0.00982 | 12 |
| 33 | `wx_pet_hargreaves_mm` | WEATHER | 0.98047 | +0.00974 | 11 |
| 34 | `cyan_median_lag1` | CYAN | 0.98020 | +0.00948 | 10 |
| 35 | `wqp_TP_val` | INSITU | 0.98020 | +0.00947 | 9 |
| 36 | `cyan_median_lag2` | CYAN | 0.98012 | +0.00940 | 8 |
| 37 | `woy_cos` | SEASON | 0.97969 | +0.00897 | 7 |
| 38 | `bloom_roll4` | CYAN | 0.97941 | +0.00868 | 6 |
| 39 | `valid_frac` | CYAN | 0.97930 | +0.00857 | 5 |
| 40 | `cyan_mean_lag1` | CYAN | 0.97809 | +0.00736 | 4 |
| 41 | `pet_mm_syr` | STATIC | 0.97687 | +0.00614 | 3 |
| 42 | `cyan_sd` | CYAN | 0.97559 | +0.00487 | 2 |

## Kept vs dropped, by block

| block | kept | dropped |
| --- | --- | --- |
| CYAN | 1: `cyan_median` | 14: `bloom_state`, `cyan_mean`, `bloom_lag1`, `cyan_gap_weeks_at_cutoff`, `bloom_roll4_n`, `bloom_state_ffill`, `cyan_sd_lag1`, `cyan_median_lag4`, `cyan_median_lag1`, `cyan_median_lag2`, `bloom_roll4`, `valid_frac`, `cyan_mean_lag1`, `cyan_sd` |
| STATIC | 1: `area_sqkm` | 6: `inu_pc_umn`, `tmp_dc_syr`, `for_pc_use`, `crp_pc_use`, `hft_ix_u09`, `pet_mm_syr` |
| SEASON | 0: -- | 2: `woy_sin`, `woy_cos` |
| WEATHER | 0: -- | 10: `wx_ssrd_trail_30d_mj`, `wx_gdd_trail_30d`, `wx_spei_4`, `wx_precip_trail_90d_mm`, `wx_calm_hours_trail_7d`, `wx_wspd_trail_14d_mean_ms`, `wx_ssrd_trail_14d_mj`, `wx_spei_1`, `wx_precip_trail_30d_mm`, `wx_pet_hargreaves_mm` |
| INSITU | 0: -- | 9: `wqp_water_temp_val`, `nwis_water_temp_val`, `wqp_chl_a_stale`, `wqp_chl_a_val`, `wqp_ammonia_val`, `nwis_gage_height_val`, `wqp_orthoP_val`, `wqp_TP_stale`, `wqp_TP_val` |
| clim | 0: -- | 1: `clim` |

## Full vs lean on HELD-OUT TEST (h=1), lake-block bootstrap of the AUC gap

- Full (44 feat) test AUC = **0.9801**; Lean (2 feat) test AUC = **0.9823**.
- Full - Lean test-AUC gap (resampling 133 lakes): median **-0.0020**, 95% CI [-0.0078, +0.0015].
- **CI includes 0 -> the lean model is NOT significantly worse on held-out test.**
