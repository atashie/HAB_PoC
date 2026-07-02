# CyAN CI_cyano <-> NLA 2022 matchup - PROTOTYPE

CI summary stat per lake: **max** over in-lake valid pixels; temporal tolerance **8 d**; below-detection water -> CI floor (-4.187 log10).

> Per-lake spatial extraction (user-authorized); no cross-lake aggregation. Cross-sectional & correlational - measures *signal agreement*, not causation, and does not validate an operational forecast.

## 1. Attrition funnel (the headline)
- A. Sampled lake-visits with lab chl-a: **1219**  (100.0% of A)
- B. + matched to a lake polygon: **1219**  (100.0% of A)
- C. + temporally matched to a weekly mosaic (<= 8d): **1219**  (100.0% of A)
- D. + lake resolvable at 300m (>=1 in-lake pixel): **929**  (76.2% of A)
- E. + >=1 cloud-free water pixel (USABLE match): **334**  (27.4% of A)

Of lakes resolvable at 300m, **595** lost the week to cloud (no cloud-free water pixel). Temporal matching was cheap (weekly mosaics are continuous); the binding constraints are **lake size (300m)** and **cloud**.

## 2. What the usable lakes look like
- Usable lakes have a median of **55** in-lake 300m pixels (area median **515 ha**).
- Median cloud-free water pixels/lake: **32**; median in-lake cloud pixels: **3**.

## 3. Does CI track the in-situ measurements?
- **CI vs lab chlorophyll-a** (log-log Spearman): rho = **0.619** (n = 334). [biomass proxy vs spectral index]
- **CI vs microcystin** (detections only, log-log Spearman): rho = **0.561** (n = 184). [toxin - a different target]

### CI-detection vs microcystin-detection (usable lakes)
```
tox_pos  False  True 
ci_pos               
False       85     70
True        65    114
```
Rows = CI detected (satellite sees cyano); Cols = microcystin detected (lab). Off-diagonal = disagreement; recall chl-a/CI proxies over-predict toxin risk.

## 4. Honest caveats
- 300m CyAN under-resolves small lakes; the usable set is biased toward LARGER lakes -> not representative of the NLA lake population (survey weights would not fix a resolution-induced exclusion).
- A weekly composite is not same-day; CI and the grab sample can be days apart and a bloom is patchy in space and time.
- `max` CI is sensitive to a single bright/edge pixel; `--stat mean` is the conservative alternative (re-run to compare).
- chl-a, CI, microcystin are distinct targets; agreement on one does not transfer.
- Correlational only. This prototype sizes the opportunity; it is not a validation.
