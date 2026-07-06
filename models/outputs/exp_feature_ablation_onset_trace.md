# Exp 3 - feature-level greedy backward ablation (selection metric = **ONSET**)

Selection criterion = **val ONSET AUC (currently-clear weeks)** at h=1. Start = fusion_full+clim (44 features). Greedy backward: at each step drop the single feature whose removal least hurts that metric, keep it dropped iff the reduced model stays within **TOL=0.005** of the full-model score (`0.89602`). Val (not test) drives selection; clim/anom pseudo-features are train-only (leakage-safe). Final lean set evaluated unbiased on test below.

**Result: dropped 42 of 44 features with <0.005 cost on the selection metric; 2 kept.**

## Elimination order (score = val ONSET AUC (currently-clear weeks))

| step | dropped feature | block | sel score | delta vs full | n kept |
| --- | --- | --- | --- | --- | --- |
| 0 | `(full model)` |  | 0.89602 | +0.00000 | 44 |
| 1 | `clim` | clim | 0.92735 | +0.03133 | 43 |
| 2 | `wx_ssrd_trail_30d_mj` | WEATHER | 0.93083 | +0.03481 | 42 |
| 3 | `bloom_state` | CYAN | 0.93083 | +0.03481 | 41 |
| 4 | `bloom_roll4_n` | CYAN | 0.93024 | +0.03422 | 40 |
| 5 | `wx_wspd_trail_14d_mean_ms` | WEATHER | 0.93128 | +0.03526 | 39 |
| 6 | `crp_pc_use` | STATIC | 0.93165 | +0.03563 | 38 |
| 7 | `wx_gdd_trail_30d` | WEATHER | 0.93150 | +0.03547 | 37 |
| 8 | `cyan_mean` | CYAN | 0.93121 | +0.03519 | 36 |
| 9 | `bloom_state_ffill` | CYAN | 0.93183 | +0.03581 | 35 |
| 10 | `cyan_gap_weeks_at_cutoff` | CYAN | 0.93183 | +0.03581 | 34 |
| 11 | `wx_spei_4` | WEATHER | 0.93123 | +0.03521 | 33 |
| 12 | `cyan_sd_lag1` | CYAN | 0.93223 | +0.03621 | 32 |
| 13 | `woy_sin` | SEASON | 0.93209 | +0.03607 | 31 |
| 14 | `tmp_dc_syr` | STATIC | 0.93195 | +0.03593 | 30 |
| 15 | `wx_calm_hours_trail_7d` | WEATHER | 0.93241 | +0.03639 | 29 |
| 16 | `inu_pc_umn` | STATIC | 0.93382 | +0.03780 | 28 |
| 17 | `wqp_orthoP_val` | INSITU | 0.93409 | +0.03807 | 27 |
| 18 | `bloom_roll4` | CYAN | 0.93356 | +0.03754 | 26 |
| 19 | `hft_ix_u09` | STATIC | 0.93392 | +0.03790 | 25 |
| 20 | `wx_spei_1` | WEATHER | 0.93294 | +0.03692 | 24 |
| 21 | `nwis_water_temp_val` | INSITU | 0.93357 | +0.03755 | 23 |
| 22 | `nwis_gage_height_val` | INSITU | 0.93320 | +0.03718 | 22 |
| 23 | `wx_precip_trail_90d_mm` | WEATHER | 0.93340 | +0.03738 | 21 |
| 24 | `wqp_water_temp_val` | INSITU | 0.93287 | +0.03685 | 20 |
| 25 | `bloom_lag1` | CYAN | 0.93254 | +0.03652 | 19 |
| 26 | `for_pc_use` | STATIC | 0.93286 | +0.03684 | 18 |
| 27 | `cyan_median_lag1` | CYAN | 0.93368 | +0.03766 | 17 |
| 28 | `wqp_chl_a_stale` | INSITU | 0.93381 | +0.03779 | 16 |
| 29 | `wqp_TP_stale` | INSITU | 0.93395 | +0.03793 | 15 |
| 30 | `wqp_chl_a_val` | INSITU | 0.93419 | +0.03817 | 14 |
| 31 | `woy_cos` | SEASON | 0.93212 | +0.03609 | 13 |
| 32 | `wx_ssrd_trail_14d_mj` | WEATHER | 0.93363 | +0.03761 | 12 |
| 33 | `wx_precip_trail_30d_mm` | WEATHER | 0.93164 | +0.03561 | 11 |
| 34 | `wqp_ammonia_val` | INSITU | 0.93158 | +0.03556 | 10 |
| 35 | `cyan_median_lag4` | CYAN | 0.93045 | +0.03443 | 9 |
| 36 | `valid_frac` | CYAN | 0.92884 | +0.03282 | 8 |
| 37 | `wx_pet_hargreaves_mm` | WEATHER | 0.92762 | +0.03160 | 7 |
| 38 | `cyan_median_lag2` | CYAN | 0.92505 | +0.02903 | 6 |
| 39 | `wqp_TP_val` | INSITU | 0.92494 | +0.02891 | 5 |
| 40 | `pet_mm_syr` | STATIC | 0.91883 | +0.02281 | 4 |
| 41 | `cyan_sd` | CYAN | 0.91052 | +0.01450 | 3 |
| 42 | `cyan_mean_lag1` | CYAN | 0.90087 | +0.00485 | 2 |

## Kept vs dropped, by block

| block | kept | dropped |
| --- | --- | --- |
| CYAN | 1: `cyan_median` | 14: `bloom_state`, `bloom_roll4_n`, `cyan_mean`, `bloom_state_ffill`, `cyan_gap_weeks_at_cutoff`, `cyan_sd_lag1`, `bloom_roll4`, `bloom_lag1`, `cyan_median_lag1`, `cyan_median_lag4`, `valid_frac`, `cyan_median_lag2`, `cyan_sd`, `cyan_mean_lag1` |
| STATIC | 1: `area_sqkm` | 6: `crp_pc_use`, `tmp_dc_syr`, `inu_pc_umn`, `hft_ix_u09`, `for_pc_use`, `pet_mm_syr` |
| SEASON | 0: -- | 2: `woy_sin`, `woy_cos` |
| WEATHER | 0: -- | 10: `wx_ssrd_trail_30d_mj`, `wx_wspd_trail_14d_mean_ms`, `wx_gdd_trail_30d`, `wx_spei_4`, `wx_calm_hours_trail_7d`, `wx_spei_1`, `wx_precip_trail_90d_mm`, `wx_ssrd_trail_14d_mj`, `wx_precip_trail_30d_mm`, `wx_pet_hargreaves_mm` |
| INSITU | 0: -- | 9: `wqp_orthoP_val`, `nwis_water_temp_val`, `nwis_gage_height_val`, `wqp_water_temp_val`, `wqp_chl_a_stale`, `wqp_TP_stale`, `wqp_chl_a_val`, `wqp_ammonia_val`, `wqp_TP_val` |
| clim | 0: -- | 1: `clim` |

## Full vs lean on HELD-OUT TEST (h=1), lake-block bootstrap of the onset-AUC (currently-clear weeks) gap

- Full (44 feat) test onset-AUC (currently-clear weeks) = **0.9292**; Lean (2 feat) = **0.9164**.
- Full - Lean gap (resampling lakes): median **+0.0124**, 95% CI [-0.0045, +0.0297].
- **CI includes 0 -> the lean model is NOT significantly worse on held-out test onset-AUC (currently-clear weeks).**

> NOTE: this bootstrap tests only the selection metric. Read the full-vs-lean grid below for the OTHER metrics (onsetMCC, AUC_within, flipMCC) -- a lean set that ties on the selection metric can still lose skill on the others.
