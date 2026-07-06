# Feature collinearity (train, h=1) -- |Pearson r| > 0.8

47 highly-collinear pairs among 43 fusion features -- excess covariance inflates overfitting risk (motivates the ablation).

| feat A | feat B | |r| |
| --- | --- | --- |
| `bloom_state` | `bloom_state_ffill` | 1.000 |
| `cyan_median` | `cyan_mean` | 0.985 |
| `cyan_median_lag1` | `cyan_mean_lag1` | 0.985 |
| `wx_ssrd_trail_14d_mj` | `wx_ssrd_trail_30d_mj` | 0.952 |
| `bloom_lag1` | `bloom_roll4` | 0.933 |
| `cyan_mean` | `cyan_mean_lag1` | 0.923 |
| `woy_cos` | `wx_ssrd_trail_30d_mj` | 0.920 |
| `cyan_median` | `cyan_mean_lag1` | 0.907 |
| `cyan_median_lag2` | `cyan_mean_lag1` | 0.907 |
| `cyan_mean` | `cyan_median_lag1` | 0.906 |
| `cyan_median_lag1` | `cyan_median_lag2` | 0.899 |
| `cyan_median` | `cyan_median_lag1` | 0.898 |
| `woy_cos` | `wx_ssrd_trail_14d_mj` | 0.884 |
| `wqp_TP_stale` | `wqp_chl_a_stale` | 0.884 |
| `cyan_mean` | `cyan_median_lag2` | 0.877 |
| `cyan_median_lag2` | `bloom_roll4` | 0.873 |
| `cyan_mean_lag1` | `bloom_roll4` | 0.873 |
| `bloom_state` | `bloom_roll4` | 0.872 |
| `bloom_state_ffill` | `bloom_roll4` | 0.872 |
| `bloom_state_ffill` | `bloom_lag1` | 0.871 |
| `cyan_mean` | `bloom_state` | 0.869 |
| `cyan_mean` | `bloom_state_ffill` | 0.869 |
| `cyan_median_lag2` | `cyan_median_lag4` | 0.869 |
| `cyan_mean_lag1` | `bloom_lag1` | 0.869 |
| `bloom_state` | `bloom_lag1` | 0.869 |
| `cyan_median` | `cyan_median_lag2` | 0.867 |
| `cyan_median_lag4` | `bloom_roll4` | 0.863 |
| `cyan_median_lag1` | `bloom_roll4` | 0.861 |
| `cyan_median` | `bloom_state` | 0.859 |
| `cyan_median` | `bloom_state_ffill` | 0.859 |
| `cyan_median_lag1` | `bloom_lag1` | 0.859 |
| `cyan_median_lag4` | `cyan_mean_lag1` | 0.855 |
| `woy_cos` | `wx_pet_hargreaves_mm` | 0.851 |
| `woy_sin` | `wx_precip_trail_90d_mm` | 0.849 |
| `cyan_mean` | `bloom_roll4` | 0.845 |
| `cyan_median_lag1` | `cyan_median_lag4` | 0.844 |
| `cyan_mean` | `cyan_median_lag4` | 0.834 |
| `cyan_median` | `bloom_roll4` | 0.831 |
| `cyan_mean_lag1` | `bloom_state` | 0.831 |
| `cyan_mean_lag1` | `bloom_state_ffill` | 0.831 |
