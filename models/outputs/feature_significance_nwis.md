# NWIS temporal feature significance vs HAB (Codex-reconciled)

Coverage: **25/133 lakes** (direct in-lake+250m or containing-L12 watershed). Reps: coincident, lag1/2/4, mean/sum(4/12wk), delta4, anomR(vs past), anomC(LOO climatology).

**class**: driver (candidate cause) | **consequence** (bloom raises turbidity/DO, lowers Secchi) | **circular** (WQP chl_a = target proxy). **timing**: antecedent (lag1/2/4, forecast-eligible) | same_week (diagnostic association only). **Read `AUC_within`** (median per-lake AUC; removes datum/size between-lake artifacts; <0.5 = inverse). `incl_within` = within-lake bootstrap p<0.1 & |AUC_within-0.5|>=0.05; `incl_assoc` = pooled p<0.1.

| feature | class | timing | n_lk | n_lw | AUC_pool | AUC_within (n) | within_p | incl_within | incl_assoc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `water_temp__lag1` | driver | antecedent | 12 | 3377 | 0.694 | 0.777 (8) | 0.154 |  | Y |
| `water_temp__coin` | driver | same_week | 12 | 3372 | 0.702 | 0.776 (8) | 0.000 | Y | Y |
| `water_temp__mean4` | driver | same_week | 12 | 3457 | 0.693 | 0.769 (8) | 0.153 |  | Y |
| `water_temp__lag2` | driver | antecedent | 12 | 3373 | 0.683 | 0.744 (8) | 0.154 |  | Y |
| `gage_height__lag1` | driver | antecedent | 24 | 10482 | 0.104 | 0.295 (17) | 0.017 | Y | Y |
| `gage_height__mean12` | driver | same_week | 24 | 10686 | 0.105 | 0.301 (17) | 0.017 | Y | Y |
| `gage_height__lag2` | driver | antecedent | 24 | 10466 | 0.105 | 0.301 (17) | 0.017 | Y | Y |
| `gage_height__mean4` | driver | same_week | 24 | 10606 | 0.104 | 0.308 (17) | 0.017 | Y | Y |
| `gage_height__lag4` | driver | antecedent | 24 | 10438 | 0.104 | 0.309 (17) | 0.017 | Y | Y |
| `water_temp__anomR` | driver | same_week | 12 | 3321 | 0.618 | 0.688 (8) | 0.011 | Y | Y |
| `gage_height__coin` | driver | same_week | 24 | 10496 | 0.105 | 0.315 (17) | 0.017 | Y | Y |
| `water_temp__lag4` | driver | antecedent | 12 | 3366 | 0.651 | 0.678 (8) | 0.154 |  | Y |
| `water_temp__mean12` | driver | same_week | 12 | 3551 | 0.643 | 0.643 (8) | 0.285 |  | Y |
| `water_temp__delta4` | driver | same_week | 12 | 3262 | 0.591 | 0.628 (7) | 0.024 | Y | Y |
| `discharge__mean4` | driver | same_week | 21 | 9801 | 0.357 | 0.388 (15) | 0.051 | Y |  |
| `discharge__sum4` | driver | same_week | 21 | 9801 | 0.355 | 0.391 (15) | 0.051 | Y |  |
| `discharge__lag1` | driver | antecedent | 21 | 9725 | 0.358 | 0.394 (15) | 0.051 | Y |  |
| `discharge__coin` | driver | same_week | 21 | 9744 | 0.358 | 0.412 (15) | 0.051 | Y |  |
| `discharge__mean12` | driver | same_week | 21 | 9850 | 0.350 | 0.414 (15) | 0.009 | Y |  |
| `discharge__lag2` | driver | antecedent | 21 | 9707 | 0.359 | 0.424 (15) | 0.051 | Y |  |
| `water_temp__anomC` | driver | same_week | 12 | 3371 | 0.533 | 0.568 (8) | 0.061 | Y |  |
| `gage_height__anomC` | driver | same_week | 24 | 10495 | 0.439 | 0.444 (17) | 0.206 |  | Y |
| `discharge__lag4` | driver | antecedent | 21 | 9677 | 0.360 | 0.447 (15) | 0.009 | Y |  |
| `discharge__delta4` | driver | same_week | 21 | 9610 | 0.518 | 0.544 (15) | 0.039 |  | Y |
| `discharge__anomC` | driver | same_week | 21 | 9743 | 0.537 | 0.470 (15) | 0.180 |  |  |
| `gage_height__delta4` | driver | same_week | 24 | 10312 | 0.535 | 0.527 (17) | 0.015 |  | Y |
| `discharge__anomR` | driver | same_week | 21 | 9662 | 0.526 | 0.483 (15) | 0.054 |  | Y |
| `gage_height__anomR` | driver | same_week | 24 | 10400 | 0.519 | 0.504 (17) | 0.797 |  |  |

**17 reps pass the within-lake gate.** DRIVER-class variables (best rep by within-lake signal):
- **water_temp**: within AUC **0.777** + (`lag1`, forecast-eligible, 8 lakes; n.s. within)
- **gage_height**: within AUC **0.295** - (inverse) (`lag1`, forecast-eligible, 17 lakes; within-sig)
- **discharge**: within AUC **0.388** - (inverse) (`mean4`, same-week, 15 lakes; within-sig)

**Caveats (Codex):** (1) **chl_a is CIRCULAR** (target proxy) -- coincident excluded from driver claims; lagged chl-a is a real but modest INDEPENDENT lead (`chla_leadlag.md`), weaker than CyAN's own antecedent CI. (2) **turbidity/Secchi/DO are CONSEQUENCES** -- coincident forms are bloom impacts, not causes. (3) **WQP values NOT unit/fraction-harmonized** (mixes total/dissolved P, chl-a methods) -- nutrient signals are indicative only; harmonize before modeling. (4) **TN & pH grossly undercounted** by characteristic-name misses (need alias/pCode discovery). (5) same_week reps are DIAGNOSTIC, not forecast skill; only antecedent (lag) reps are forecast-eligible. (6) coverage/linkage: direct tier suppresses watershed; a few sites fall in >1 lake buffer (kept first) -- minor. (7) WQP chl-a ~monthly (sparse).