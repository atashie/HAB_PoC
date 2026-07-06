# WQP temporal feature significance vs HAB (Codex-reconciled)

Coverage: **123/133 lakes** (direct in-lake+250m or containing-L12 watershed). Reps: coincident, lag1/2/4, mean/sum(4/12wk), delta4, anomR(vs past), anomC(LOO climatology).

**class**: driver (candidate cause) | **consequence** (bloom raises turbidity/DO, lowers Secchi) | **circular** (WQP chl_a = target proxy). **timing**: antecedent (lag1/2/4, forecast-eligible) | same_week (diagnostic association only). **Read `AUC_within`** (median per-lake AUC; removes datum/size between-lake artifacts; <0.5 = inverse). `incl_within` = within-lake bootstrap p<0.1 & |AUC_within-0.5|>=0.05; `incl_assoc` = pooled p<0.1.

| feature | class | timing | n_lk | n_lw | AUC_pool | AUC_within (n) | within_p | incl_within | incl_assoc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `chl_a__coin` | circular | same_week | 116 | 7938 | 0.882 | 0.877 (69) | 0.000 | Y | Y |
| `turbidity__lag1` | consequence | antecedent | 116 | 7041 | 0.807 | 0.860 (65) | 0.000 | Y | Y |
| `turbidity__coin` | consequence | same_week | 117 | 7053 | 0.810 | 0.848 (67) | 0.000 | Y | Y |
| `chl_a__lag1` | circular | antecedent | 116 | 7924 | 0.879 | 0.840 (67) | 0.000 | Y | Y |
| `turbidity__lag2` | consequence | antecedent | 118 | 7047 | 0.803 | 0.821 (67) | 0.000 | Y | Y |
| `chl_a__mean4` | circular | same_week | 116 | 24365 | 0.907 | 0.817 (78) | 0.000 | Y | Y |
| `turbidity__mean4` | consequence | same_week | 118 | 22261 | 0.847 | 0.806 (77) | 0.000 | Y | Y |
| `chl_a__lag2` | circular | antecedent | 116 | 7935 | 0.873 | 0.786 (72) | 0.000 | Y | Y |
| `chl_a__mean12` | circular | same_week | 112 | 22634 | 0.904 | 0.783 (74) | 0.000 | Y | Y |
| `turbidity__mean12` | consequence | same_week | 106 | 18780 | 0.834 | 0.781 (69) | 0.000 | Y | Y |
| `turbidity__lag4` | consequence | antecedent | 118 | 7036 | 0.794 | 0.780 (67) | 0.000 | Y | Y |
| `chl_a__lag4` | circular | antecedent | 116 | 7907 | 0.861 | 0.757 (69) | 0.000 | Y | Y |
| `chl_a__anomC` | circular | same_week | 112 | 7803 | 0.581 | 0.749 (67) | 0.000 | Y | Y |
| `turbidity__anomC` | consequence | same_week | 107 | 6894 | 0.591 | 0.743 (65) | 0.000 | Y | Y |
| `water_temp__anomR` | driver | same_week | 72 | 4761 | 0.587 | 0.690 (28) | 0.000 | Y | Y |
| `secchi__coin` | consequence | same_week | 119 | 9055 | 0.324 | 0.318 (72) | 0.000 | Y | Y |
| `secchi__mean12` | consequence | same_week | 114 | 26057 | 0.316 | 0.324 (77) | 0.000 | Y | Y |
| `secchi__lag1` | consequence | antecedent | 118 | 9054 | 0.326 | 0.330 (69) | 0.000 | Y | Y |
| `secchi__lag4` | consequence | antecedent | 119 | 9036 | 0.335 | 0.337 (73) | 0.000 | Y | Y |
| `secchi__lag2` | consequence | antecedent | 119 | 9051 | 0.329 | 0.340 (74) | 0.000 | Y | Y |
| `secchi__mean4` | consequence | same_week | 119 | 27345 | 0.295 | 0.347 (82) | 0.000 | Y | Y |
| `turbidity__anomR` | consequence | same_week | 54 | 3105 | 0.572 | 0.642 (21) | 0.000 | Y | Y |
| `ammonia__mean12` | driver | same_week | 103 | 16642 | 0.410 | 0.373 (69) | 0.010 | Y | Y |
| `water_temp__coin` | driver | same_week | 121 | 8751 | 0.572 | 0.621 (72) | 0.000 | Y | Y |
| `chl_a__delta4` | circular | same_week | 101 | 2767 | 0.549 | 0.619 (25) | 0.000 | Y | Y |
| `secchi__anomC` | consequence | same_week | 114 | 8942 | 0.478 | 0.381 (71) | 0.000 | Y | Y |
| `chl_a__anomR` | circular | same_week | 84 | 3959 | 0.551 | 0.607 (30) | 0.000 | Y | Y |
| `turbidity__delta4` | consequence | same_week | 74 | 2394 | 0.528 | 0.604 (20) | 0.007 | Y | Y |
| `water_temp__mean4` | driver | same_week | 121 | 25204 | 0.553 | 0.597 (82) | 0.005 | Y | Y |
| `secchi__anomR` | consequence | same_week | 85 | 4860 | 0.450 | 0.409 (34) | 0.001 | Y | Y |
| `water_temp__lag2` | driver | antecedent | 121 | 8753 | 0.557 | 0.585 (73) | 0.002 | Y | Y |
| `orthoP__coin` | driver | same_week | 113 | 7507 | 0.413 | 0.417 (63) | 0.017 | Y | Y |
| `orthoP__lag1` | driver | antecedent | 112 | 7494 | 0.413 | 0.420 (61) | 0.014 | Y | Y |
| `orthoP__mean12` | driver | same_week | 105 | 18785 | 0.410 | 0.424 (67) | 0.265 |  | Y |
| `secchi__delta4` | consequence | same_week | 102 | 3327 | 0.482 | 0.424 (28) | 0.000 | Y | Y |
| `orthoP__lag2` | driver | antecedent | 113 | 7502 | 0.413 | 0.425 (65) | 0.034 | Y | Y |
| `water_temp__lag1` | driver | antecedent | 119 | 8740 | 0.567 | 0.573 (70) | 0.048 | Y | Y |
| `water_temp__delta4` | driver | same_week | 90 | 3575 | 0.544 | 0.570 (27) | 0.026 | Y | Y |
| `water_temp__lag4` | driver | antecedent | 121 | 8739 | 0.543 | 0.568 (72) | 0.053 | Y | Y |
| `DO__mean12` | consequence | same_week | 109 | 21608 | 0.639 | 0.568 (75) | 0.003 | Y | Y |
| `orthoP__mean4` | driver | same_week | 113 | 22136 | 0.433 | 0.438 (76) | 0.002 | Y |  |
| `DO__lag4` | consequence | antecedent | 119 | 8270 | 0.609 | 0.561 (69) | 0.002 | Y | Y |
| `ammonia__lag2` | driver | antecedent | 117 | 6403 | 0.399 | 0.439 (62) | 0.247 |  | Y |
| `ammonia__lag1` | driver | antecedent | 115 | 6395 | 0.397 | 0.441 (62) | 0.189 |  | Y |
| `TP__lag4` | driver | antecedent | 117 | 10111 | 0.503 | 0.558 (72) | 0.055 | Y |  |
| `TP__coin` | driver | same_week | 119 | 10143 | 0.510 | 0.555 (73) | 0.135 |  |  |
| `ammonia__coin` | driver | same_week | 118 | 6408 | 0.404 | 0.445 (63) | 0.159 |  | Y |
| `TP__lag2` | driver | antecedent | 119 | 10142 | 0.510 | 0.553 (73) | 0.275 |  |  |
| `DO__anomC` | consequence | same_week | 110 | 8119 | 0.526 | 0.552 (68) | 0.006 | Y | Y |
| `TP__mean4` | driver | same_week | 119 | 27268 | 0.505 | 0.551 (81) | 0.322 |  |  |
| `water_temp__mean12` | driver | same_week | 111 | 22685 | 0.529 | 0.551 (78) | 0.028 | Y | Y |
| `ammonia__mean4` | driver | same_week | 118 | 19053 | 0.414 | 0.449 (75) | 0.093 | Y | Y |
| `DO__coin` | consequence | same_week | 119 | 8280 | 0.593 | 0.549 (69) | 0.174 |  | Y |
| `DO__mean4` | consequence | same_week | 119 | 24005 | 0.613 | 0.543 (79) | 0.141 |  | Y |
| `DO__anomR` | consequence | same_week | 70 | 4413 | 0.475 | 0.459 (25) | 0.060 |  |  |
| `ammonia__lag4` | driver | antecedent | 116 | 6390 | 0.400 | 0.462 (64) | 0.276 |  | Y |
| `TP__mean12` | driver | same_week | 111 | 26336 | 0.500 | 0.533 (77) | 0.551 |  |  |
| `orthoP__lag4` | driver | antecedent | 113 | 7497 | 0.414 | 0.467 (61) | 0.168 |  |  |
| `TP__lag1` | driver | antecedent | 117 | 10149 | 0.508 | 0.530 (70) | 0.393 |  |  |
| `TP__anomR` | driver | same_week | 84 | 6420 | 0.476 | 0.529 (33) | 0.124 |  |  |
| `DO__lag2` | consequence | antecedent | 119 | 8280 | 0.603 | 0.527 (70) | 0.105 |  | Y |
| `ammonia__delta4` | driver | same_week | 76 | 2606 | 0.510 | 0.526 (25) | 0.312 |  |  |
| `TP__delta4` | driver | same_week | 97 | 4649 | 0.525 | 0.525 (30) | 0.375 |  | Y |
| `DO__lag1` | consequence | antecedent | 117 | 8265 | 0.601 | 0.522 (67) | 0.267 |  | Y |
| `orthoP__anomC` | driver | same_week | 103 | 7354 | 0.482 | 0.482 (62) | 0.418 |  |  |
| `DO__delta4` | consequence | same_week | 90 | 3360 | 0.483 | 0.483 (27) | 0.567 |  |  |
| `TP__anomC` | driver | same_week | 111 | 10009 | 0.470 | 0.514 (71) | 0.884 |  |  |
| `water_temp__anomC` | driver | same_week | 113 | 8599 | 0.504 | 0.506 (71) | 0.729 |  |  |
| `ammonia__anomC` | driver | same_week | 102 | 6217 | 0.482 | 0.495 (63) | 0.908 |  |  |
| `orthoP__anomR` | driver | same_week | 64 | 3878 | 0.512 | 0.496 (22) | 0.902 |  |  |
| `orthoP__delta4` | driver | same_week | 82 | 3082 | 0.515 | 0.499 (25) | 0.822 |  | Y |
| `ammonia__anomR` | driver | same_week | 61 | 3182 | 0.527 | 0.499 (21) | 0.839 |  |  |

**45 reps pass the within-lake gate.** DRIVER-class variables (best rep by within-lake signal):
- **water_temp**: within AUC **0.690** + (`anomR`, same-week, 28 lakes; within-sig)
- **ammonia**: within AUC **0.373** - (inverse) (`mean12`, same-week, 69 lakes; within-sig)
- **orthoP**: within AUC **0.417** - (inverse) (`coin`, same-week, 63 lakes; within-sig)
- **TP**: within AUC **0.558** + (`lag4`, forecast-eligible, 72 lakes; within-sig)

**Caveats (Codex):** (1) **chl_a is CIRCULAR** (target proxy) -- coincident excluded from driver claims; lagged chl-a is a real but modest INDEPENDENT lead (`chla_leadlag.md`), weaker than CyAN's own antecedent CI. (2) **turbidity/Secchi/DO are CONSEQUENCES** -- coincident forms are bloom impacts, not causes. (3) **WQP values NOT unit/fraction-harmonized** (mixes total/dissolved P, chl-a methods) -- nutrient signals are indicative only; harmonize before modeling. (4) **TN & pH grossly undercounted** by characteristic-name misses (need alias/pCode discovery). (5) same_week reps are DIAGNOSTIC, not forecast skill; only antecedent (lag) reps are forecast-eligible. (6) coverage/linkage: direct tier suppresses watershed; a few sites fall in >1 lake buffer (kept first) -- minor. (7) WQP chl-a ~monthly (sparse).