# Does WQP chl-a LEAD CyAN? (isolating lead from shared persistence)

Test: restrict to weeks where **CyAN is NOT blooming at the cutoff** (`bloom(W-h)=0`), then measure whether antecedent in-situ chl-a (freshest on/before W-h, staleness<=8wk) predicts a CyAN bloom h weeks later. AUC>0.5 there = genuine lead (chl-a saw it before CyAN). Within-lake median AUC. Compared to CyAN's own sub-threshold median at W-h.

| h (wk) | n lake-wks | n lakes | chl-a AUC_within | CyAN-median AUC_within | onset rate |
| --- | --- | --- | --- | --- | --- |
| 1 | 26,024 | 75 | 0.634 | 0.816 | 0.030 |
| 2 | 26,024 | 75 | 0.626 | 0.777 | 0.040 |
| 3 | 26,024 | 74 | 0.617 | 0.733 | 0.047 |
| 4 | 26,024 | 74 | 0.589 | 0.697 | 0.054 |

**Reading:** if chl-a AUC_within > 0.5 (and > CyAN-median's), in-situ chl-a carries early-warning signal the satellite's own sub-threshold value does not -- quantifying the lead. If ~0.5 or <= CyAN, the apparent lag skill was shared persistence, not independent lead. Caveat: WQP chl-a ~monthly (staleness up to 8wk), so lead resolution is coarse; coincident chl-a remains redundant with the CyAN-defined target (D-15).