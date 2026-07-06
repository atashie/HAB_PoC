# WEATHER (ERA5-derived) feature significance vs HAB

Coverage: **133/133 lakes** (gridded 0.25deg, nearest cell -> every lake). All features `driver` class. Reps: coincident, lag1/2/4 (antecedent/forecast-eligible), anomC (LOO climatology). Test = lake-block bootstrap AUC (pooled) + **within-lake** median-AUC bootstrap (read `AUC_within`; <0.5 = inverse). `incl_within` = within p<0.1 & |AUC_within-0.5|>=0.05.

| feature | timing | n_lk | n_lw | AUC_pool | AUC_within (n) | within_p | incl_within | incl_assoc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pet_hargreaves_mm__coin` | same_week | 133 | 68233 | 0.536 | 0.662 (102) | 0.000 | Y | Y |
| `ssrd_trail_14d_mj__coin` | same_week | 133 | 68233 | 0.552 | 0.661 (102) | 0.000 | Y | Y |
| `ssrd_trail_30d_mj__coin` | same_week | 133 | 68233 | 0.556 | 0.660 (102) | 0.000 | Y | Y |
| `ssrd_trail_14d_mj__lag1` | antecedent | 133 | 68117 | 0.553 | 0.660 (102) | 0.000 | Y | Y |
| `ssrd_trail_14d_mj__lag2` | antecedent | 133 | 67989 | 0.553 | 0.655 (102) | 0.000 | Y | Y |
| `ssrd_trail_30d_mj__lag1` | antecedent | 133 | 68117 | 0.556 | 0.652 (102) | 0.000 | Y | Y |
| `pet_hargreaves_mm__lag2` | antecedent | 133 | 67989 | 0.536 | 0.648 (102) | 0.000 | Y | Y |
| `pet_hargreaves_mm__lag1` | antecedent | 133 | 68117 | 0.536 | 0.647 (102) | 0.000 | Y | Y |
| `ssrd_trail_30d_mj__lag2` | antecedent | 133 | 67989 | 0.555 | 0.635 (102) | 0.000 | Y | Y |
| `pet_hargreaves_mm__lag4` | antecedent | 133 | 67780 | 0.534 | 0.625 (102) | 0.000 | Y | Y |
| `ssrd_trail_30d_mj__lag4` | antecedent | 133 | 67780 | 0.550 | 0.620 (102) | 0.000 | Y | Y |
| `ssrd_trail_14d_mj__lag4` | antecedent | 133 | 67780 | 0.551 | 0.619 (102) | 0.000 | Y | Y |
| `gdd_daily__coin` | same_week | 133 | 68233 | 0.543 | 0.594 (102) | 0.000 | Y | Y |
| `gdd_daily__lag1` | antecedent | 133 | 68117 | 0.542 | 0.583 (102) | 0.001 | Y | Y |
| `gdd_trail_30d__coin` | same_week | 133 | 68233 | 0.542 | 0.579 (102) | 0.000 | Y | Y |
| `precip_trail_90d_mm__lag4` | antecedent | 133 | 67780 | 0.471 | 0.424 (102) | 0.066 | Y | Y |
| `spei_6__lag2` | antecedent | 133 | 66942 | 0.471 | 0.428 (102) | 0.000 | Y | Y |
| `gdd_daily__lag2` | antecedent | 133 | 67989 | 0.540 | 0.570 (102) | 0.000 | Y | Y |
| `gdd_trail_30d__lag1` | antecedent | 133 | 68117 | 0.538 | 0.563 (102) | 0.000 | Y | Y |
| `spei_6__lag1` | antecedent | 133 | 67069 | 0.471 | 0.440 (102) | 0.000 | Y | Y |
| `precip_trail_90d_mm__lag2` | antecedent | 133 | 67989 | 0.478 | 0.444 (102) | 0.039 | Y | Y |
| `spei_4__anomC` | same_week | 133 | 68233 | 0.475 | 0.446 (102) | 0.006 | Y | Y |
| `spei_6__coin` | same_week | 133 | 67180 | 0.472 | 0.446 (102) | 0.002 | Y | Y |
| `wspd_trail_14d_mean_ms__coin` | same_week | 133 | 68233 | 0.494 | 0.447 (102) | 0.008 | Y |  |
| `calm_hours_trail_7d__coin` | same_week | 133 | 68233 | 0.512 | 0.552 (102) | 0.003 | Y |  |
| `spei_6__anomC` | same_week | 133 | 67180 | 0.469 | 0.448 (102) | 0.000 | Y | Y |
| `spei_6__lag4` | antecedent | 133 | 66688 | 0.473 | 0.449 (102) | 0.000 | Y | Y |
| `spei_4__lag2` | antecedent | 133 | 67989 | 0.476 | 0.452 (102) | 0.000 |  | Y |
| `gdd_trail_90d__lag4` | antecedent | 133 | 67780 | 0.507 | 0.452 (102) | 0.214 |  |  |
| `precip_trail_90d_mm__anomC` | same_week | 133 | 68233 | 0.479 | 0.452 (102) | 0.036 |  | Y |
| `spei_4__coin` | same_week | 133 | 68233 | 0.478 | 0.453 (102) | 0.004 |  | Y |
| `precip_trail_60d_mm__anomC` | same_week | 133 | 68233 | 0.483 | 0.453 (102) | 0.002 |  | Y |
| `wspd_trail_7d_mean_ms__coin` | same_week | 133 | 68233 | 0.494 | 0.453 (102) | 0.000 |  |  |
| `calm_hours_trail_14d__coin` | same_week | 133 | 68233 | 0.511 | 0.546 (102) | 0.031 |  |  |
| `gdd_trail_60d__coin` | same_week | 133 | 68233 | 0.534 | 0.546 (102) | 0.029 |  | Y |
| `spei_2__coin` | same_week | 133 | 68233 | 0.487 | 0.454 (102) | 0.005 |  | Y |
| `pet_hargreaves_mm__anomC` | same_week | 133 | 68233 | 0.512 | 0.545 (102) | 0.000 |  | Y |
| `spei_1__lag1` | antecedent | 133 | 68117 | 0.489 | 0.456 (102) | 0.009 |  | Y |
| `spei_1__anomC` | same_week | 133 | 68233 | 0.492 | 0.456 (102) | 0.009 |  | Y |
| `spei_2__lag1` | antecedent | 133 | 68117 | 0.485 | 0.457 (102) | 0.002 |  | Y |
| `spei_2__anomC` | same_week | 133 | 68233 | 0.485 | 0.457 (102) | 0.005 |  | Y |
| `spei_2__lag2` | antecedent | 133 | 67989 | 0.484 | 0.457 (102) | 0.001 |  | Y |
| `precip_trail_60d_mm__lag4` | antecedent | 133 | 67780 | 0.480 | 0.457 (102) | 0.070 |  | Y |
| `precip_trail_90d_mm__lag1` | antecedent | 133 | 68117 | 0.481 | 0.458 (102) | 0.046 |  | Y |
| `gdd_trail_30d__lag2` | antecedent | 133 | 67989 | 0.534 | 0.541 (102) | 0.024 |  | Y |
| `wspd_trail_7d_mean_ms__lag1` | antecedent | 133 | 68117 | 0.497 | 0.459 (102) | 0.059 |  |  |
| `spei_1__coin` | same_week | 133 | 68233 | 0.493 | 0.460 (102) | 0.003 |  | Y |
| `precip_trail_30d_mm__anomC` | same_week | 133 | 68233 | 0.489 | 0.460 (102) | 0.018 |  | Y |
| `ssrd_trail_30d_mj__anomC` | same_week | 133 | 68233 | 0.516 | 0.539 (102) | 0.000 |  | Y |
| `wspd_trail_14d_mean_ms__lag1` | antecedent | 133 | 68117 | 0.497 | 0.462 (102) | 0.032 |  |  |
| `gdd_daily__lag4` | antecedent | 133 | 67780 | 0.532 | 0.537 (102) | 0.048 |  | Y |
| `spei_4__lag1` | antecedent | 133 | 68117 | 0.477 | 0.463 (102) | 0.020 |  | Y |
| `spei_4__lag4` | antecedent | 133 | 67780 | 0.478 | 0.463 (102) | 0.004 |  | Y |
| `calm_hours_trail_30d__coin` | same_week | 133 | 68233 | 0.509 | 0.535 (102) | 0.290 |  |  |
| `spei_1__lag2` | antecedent | 133 | 67989 | 0.487 | 0.465 (102) | 0.028 |  | Y |
| `calm_hours_trail_7d__lag1` | antecedent | 133 | 68117 | 0.508 | 0.534 (102) | 0.132 |  |  |
| `precip_trail_14d_mm__coin` | same_week | 133 | 68233 | 0.507 | 0.533 (102) | 0.038 |  |  |
| `wspd_trail_30d_mean_ms__coin` | same_week | 133 | 68233 | 0.496 | 0.467 (102) | 0.102 |  |  |
| `calm_hours_trail_14d__lag1` | antecedent | 133 | 68117 | 0.508 | 0.532 (102) | 0.110 |  |  |
| `precip_trail_60d_mm__lag1` | antecedent | 133 | 68117 | 0.489 | 0.468 (102) | 0.187 |  |  |
| `precip_trail_7d_mm__coin` | same_week | 133 | 68233 | 0.510 | 0.530 (102) | 0.021 |  |  |
| `calm_hours_trail_7d__lag2` | antecedent | 133 | 67989 | 0.506 | 0.530 (102) | 0.092 |  |  |
| `ssrd_trail_14d_mj__anomC` | same_week | 133 | 68233 | 0.511 | 0.530 (102) | 0.002 |  | Y |
| `precip_trail_60d_mm__lag2` | antecedent | 133 | 67989 | 0.486 | 0.470 (102) | 0.104 |  |  |
| `wspd_trail_7d_mean_ms__lag2` | antecedent | 133 | 67989 | 0.500 | 0.471 (102) | 0.040 |  |  |
| `precip_trail_30d_mm__lag4` | antecedent | 133 | 67780 | 0.487 | 0.471 (102) | 0.069 |  |  |
| `gdd_trail_90d__lag2` | antecedent | 133 | 67989 | 0.516 | 0.474 (102) | 0.279 |  | Y |
| `precip_trail_14d_mm__anomC` | same_week | 133 | 68233 | 0.494 | 0.475 (102) | 0.052 |  | Y |
| `gdd_trail_60d__lag1` | antecedent | 133 | 68117 | 0.530 | 0.525 (102) | 0.146 |  | Y |
| `precip_trail_90d_mm__coin` | same_week | 133 | 68233 | 0.485 | 0.475 (102) | 0.079 |  |  |
| `wspd_trail_30d_mean_ms__lag2` | antecedent | 133 | 67989 | 0.503 | 0.476 (102) | 0.309 |  |  |
| `precip_trail_7d_mm__lag4` | antecedent | 133 | 67780 | 0.493 | 0.477 (102) | 0.185 |  |  |
| `precip_trail_14d_mm__lag4` | antecedent | 133 | 67780 | 0.491 | 0.478 (102) | 0.126 |  |  |
| `precip_trail_30d_mm__coin` | same_week | 133 | 68233 | 0.502 | 0.522 (102) | 0.492 |  |  |
| `spei_2__lag4` | antecedent | 133 | 67780 | 0.486 | 0.478 (102) | 0.085 |  | Y |
| `calm_hours_trail_30d__lag2` | antecedent | 133 | 67989 | 0.502 | 0.521 (102) | 0.372 |  |  |
| `precip_trail_7d_mm__anomC` | same_week | 133 | 68233 | 0.498 | 0.479 (102) | 0.042 |  |  |
| `precip_trail_7d_mm__lag1` | antecedent | 133 | 68117 | 0.504 | 0.521 (102) | 0.126 |  |  |
| `calm_hours_trail_7d__anomC` | same_week | 133 | 68233 | 0.506 | 0.521 (102) | 0.004 |  | Y |
| `wspd_trail_30d_mean_ms__lag1` | antecedent | 133 | 68117 | 0.500 | 0.480 (102) | 0.112 |  |  |
| `wspd_trail_30d_mean_ms__lag4` | antecedent | 133 | 67780 | 0.510 | 0.520 (102) | 0.597 |  |  |
| `spei_1__lag4` | antecedent | 133 | 67780 | 0.489 | 0.481 (102) | 0.021 |  | Y |
| `wspd_trail_14d_mean_ms__anomC` | same_week | 133 | 68233 | 0.494 | 0.481 (102) | 0.006 |  | Y |
| `gdd_trail_60d__lag4` | antecedent | 133 | 67780 | 0.516 | 0.481 (102) | 0.205 |  | Y |
| `precip_trail_30d_mm__lag2` | antecedent | 133 | 67989 | 0.493 | 0.483 (102) | 0.234 |  |  |
| `calm_hours_trail_30d__lag1` | antecedent | 133 | 68117 | 0.505 | 0.516 (102) | 0.466 |  |  |
| `precip_trail_60d_mm__coin` | same_week | 133 | 68233 | 0.494 | 0.484 (102) | 0.482 |  |  |
| `precip_trail_14d_mm__lag1` | antecedent | 133 | 68117 | 0.502 | 0.515 (102) | 0.134 |  |  |
| `wspd_trail_14d_mean_ms__lag2` | antecedent | 133 | 67989 | 0.501 | 0.486 (102) | 0.168 |  |  |
| `precip_trail_7d_mm__lag2` | antecedent | 133 | 67989 | 0.500 | 0.514 (102) | 0.538 |  |  |
| `wspd_trail_30d_mean_ms__anomC` | same_week | 133 | 68233 | 0.493 | 0.486 (102) | 0.025 |  | Y |
| `wspd_trail_7d_mean_ms__anomC` | same_week | 133 | 68233 | 0.494 | 0.486 (102) | 0.050 |  | Y |
| `calm_hours_trail_30d__anomC` | same_week | 133 | 68233 | 0.505 | 0.514 (102) | 0.151 |  | Y |
| `gdd_trail_30d__lag4` | antecedent | 133 | 67780 | 0.524 | 0.513 (102) | 0.378 |  | Y |
| `calm_hours_trail_14d__lag2` | antecedent | 133 | 67989 | 0.504 | 0.513 (102) | 0.369 |  |  |
| `calm_hours_trail_14d__anomC` | same_week | 133 | 68233 | 0.506 | 0.511 (102) | 0.076 |  | Y |
| `wspd_trail_14d_mean_ms__lag4` | antecedent | 133 | 67780 | 0.507 | 0.489 (102) | 0.537 |  |  |
| `calm_hours_trail_30d__lag4` | antecedent | 133 | 67780 | 0.494 | 0.489 (102) | 0.670 |  |  |
| `gdd_trail_60d__lag2` | antecedent | 133 | 67989 | 0.525 | 0.510 (102) | 0.464 |  | Y |
| `gdd_trail_90d__lag1` | antecedent | 133 | 68117 | 0.521 | 0.491 (102) | 0.795 |  | Y |
| `gdd_trail_60d__anomC` | same_week | 133 | 68233 | 0.505 | 0.508 (102) | 0.365 |  |  |
| `gdd_daily__anomC` | same_week | 133 | 68233 | 0.498 | 0.507 (102) | 0.470 |  |  |
| `gdd_trail_90d__anomC` | same_week | 133 | 68233 | 0.506 | 0.506 (102) | 0.381 |  |  |
| `calm_hours_trail_7d__lag4` | antecedent | 133 | 67780 | 0.498 | 0.505 (102) | 0.791 |  |  |
| `gdd_trail_90d__coin` | same_week | 133 | 68233 | 0.526 | 0.505 (102) | 0.725 |  | Y |
| `gdd_trail_30d__anomC` | same_week | 133 | 68233 | 0.507 | 0.505 (102) | 0.211 |  | Y |
| `precip_trail_30d_mm__lag1` | antecedent | 133 | 68117 | 0.497 | 0.497 (102) | 0.605 |  |  |
| `precip_trail_14d_mm__lag2` | antecedent | 133 | 67989 | 0.498 | 0.502 (102) | 0.912 |  |  |
| `calm_hours_trail_14d__lag4` | antecedent | 133 | 67780 | 0.499 | 0.501 (102) | 0.921 |  |  |
| `wspd_trail_7d_mean_ms__lag4` | antecedent | 133 | 67780 | 0.507 | 0.501 (102) | 0.826 |  |  |

**27 reps pass the within-lake gate.** Per weather variable (best rep by within-lake signal):
- **pet_hargreaves_mm**: within AUC **0.662** + (`coin`, same-week, within-sig)
- **ssrd_trail_14d_mj**: within AUC **0.661** + (`coin`, same-week, within-sig)
- **ssrd_trail_30d_mj**: within AUC **0.660** + (`coin`, same-week, within-sig)
- **gdd_daily**: within AUC **0.594** + (`coin`, same-week, within-sig)
- **gdd_trail_30d**: within AUC **0.579** + (`coin`, same-week, within-sig)
- **precip_trail_90d_mm**: within AUC **0.424** - (inverse) (`lag4`, forecast-eligible, within-sig)
- **spei_6**: within AUC **0.428** - (inverse) (`lag2`, forecast-eligible, within-sig)
- **spei_4**: within AUC **0.446** - (inverse) (`anomC`, same-week, within-sig)
- **wspd_trail_14d_mean_ms**: within AUC **0.447** - (inverse) (`coin`, same-week, within-sig)
- **calm_hours_trail_7d**: within AUC **0.552** + (`coin`, same-week, within-sig)
- **gdd_trail_90d**: within AUC **0.452** - (inverse) (`lag4`, forecast-eligible, n.s. within)
- **precip_trail_60d_mm**: within AUC **0.453** - (inverse) (`anomC`, same-week, n.s. within)
- **wspd_trail_7d_mean_ms**: within AUC **0.453** - (inverse) (`coin`, same-week, n.s. within)
- **calm_hours_trail_14d**: within AUC **0.546** + (`coin`, same-week, n.s. within)
- **gdd_trail_60d**: within AUC **0.546** + (`coin`, same-week, n.s. within)
- **spei_2**: within AUC **0.454** - (inverse) (`coin`, same-week, n.s. within)
- **spei_1**: within AUC **0.456** - (inverse) (`lag1`, forecast-eligible, n.s. within)
- **precip_trail_30d_mm**: within AUC **0.460** - (inverse) (`anomC`, same-week, n.s. within)
- **calm_hours_trail_30d**: within AUC **0.535** + (`coin`, same-week, n.s. within)
- **precip_trail_14d_mm**: within AUC **0.533** + (`coin`, same-week, n.s. within)
- **wspd_trail_30d_mean_ms**: within AUC **0.467** - (inverse) (`coin`, same-week, n.s. within)
- **precip_trail_7d_mm**: within AUC **0.530** + (`coin`, same-week, n.s. within)

**Notes:** weather is a coincident/antecedent DRIVER layer (no consequence/circular issue). SPEI is already a standardized anomaly; trailing sums are levels (anomC removes seasonality). same_week reps are diagnostic; lag reps are forecast-eligible. Nearest-cell extraction (0.25deg ~28km) -- fine for lakes << cell.