# 04 — Feature significance assessment (static + in-situ)

Screen every candidate feature for a statistically defensible association with HAB, as the evidence
base for the fusion model. Weather (ERA5) is deferred until its derived features land. **This is a
screen, not the model** — inclusion is permissive (p<0.1) to build a candidate set, with honest
multiple-comparison + within-lake context so nothing is oversold.

## Methodology

- **Linkage (NWIS/WQP → lakes; D-33):** direct = monitoring point in the lake polygon **+250 m**; else
  the median of stations in the **containing BasinATLAS L12** watershed; else null. Lake→L12 by
  **max-overlap** (`join_basinatlas_l12.parquet`, 133/133).
- **Static features** (`assess_static_features.py`): unit = **lake** (n=132/133) to avoid
  pseudoreplication; Spearman(feature, per-lake bloom prevalence); inclusion p<0.1; BH-FDR reported.
- **Temporal features** (`screen_insitu_features.py`): per-(lake,variable) weekly-median series;
  representations = coincident, lag1/2/4, mean/sum(4/12 wk), delta4, anomaly-vs-recent-past (`anomR`),
  anomaly-vs-LOO-climatology (`anomC`). Test = **lake-block bootstrap AUC** (`AUC_pool`) **+ a
  within-lake bootstrap of the median per-lake AUC** (`AUC_within`, the honest temporal test).
  - **CLASS:** `driver` | **`consequence`** (bloom raises turbidity/DO, lowers Secchi; microcystin is
    bloom-produced) | **`circular`** (WQP chl-a = target proxy).
  - **TIMING:** `antecedent` (lag1/2/4, forecast-eligible) vs `same_week` (diagnostic association only).
  - **Read `AUC_within`** (< 0.5 = inverse): it removes the between-lake baseline, exposing
    datum-relative (gage height) / size-scaling (discharge) artifacts that inflate `AUC_pool`.

### Significance tests (this round — precise)

| feature type | statistic | significance | multiplicity |
|---|---|---|---|
| **static** | Spearman ρ (feature vs per-**lake** bloom prevalence, n=132) | correlation p | BH-FDR |
| **temporal** | univariate **AUC = Mann–Whitney U** (feature ranks bloom-week vs non-bloom) | **lake-block bootstrap** (resample whole lakes), two-sided p vs AUC=0.5 — both **pooled** and **within-lake** (median per-lake AUC) | BH-FDR |

So the temporal test is a **cluster-robust (lake-block) Mann–Whitney/AUC test**, which respects the
within-lake autocorrelation; the within-lake variant is the honest temporal read.

**Horizon (h=0–4) handling — as-is, sufficient for this round (per decision 2026-07-03).** Every
temporal feature is tested against bloom in the **same week W**, so the **forecast horizon is encoded in
the feature LAG**: `coincident` ≈ h0, `lag1`/`lag2`/`lag4` ≈ the h1/h2/h4 tests ("feature at W−k vs
bloom(W)" ≡ "feature at issue T vs bloom(T+k)"). *Known scope limits of this round:* **h=3 is not
built** (only lag1/2/4); the **aggregate reps** (`mean/sum/anomR/anomC`) span multiple weeks so are not
single-horizon tests; and the **chl-a lead test** (`chla_leadlag.md`) reports per-horizon AUCs (h1–4)
as **point estimates without a bootstrap p**. An explicit, complete per-horizon significance sweep
(feature as-of the latency-corrected issue week vs bloom at each h=0–4) is **deferred** as unnecessary
for this initial screen; it belongs to the modeling stage.

## Results

### Static — area + BasinATLAS L12 (`feature_significance_static.md`)
**Weak.** 13/33 pass p<0.1 but only **1 survives FDR** (`inu_pc_umn` inundation, ρ=+0.351). **Area**
ρ=+0.226 (p=0.009, included; fails FDR). Directions sensible (anthropogenic/warmth/PET **+**,
forest/moisture **−**) but small — between-lake landscape gradients are **compressed** because all FL
lakes are broadly eutrophic. ⇒ the forecasting signal lives in **within-lake temporal dynamics**.
*Depth omitted (needs HydroLAKES).*

### NWIS hydrology (`feature_significance_nwis.md`) — coverage **25/133 lakes**
Many FL lakes are seepage/closed-basin, ungauged. Within-lake signal:
- **water temperature** — genuine positive (AUC_within ~0.78; only 8 lakes → not within-significant).
- **gage height** — real **inverse** within-lake (~0.30: higher stage → less bloom, dilution/flushing);
  its `AUC_pool` ~0.10 is **datum-inflated** (each gage's own zero) — trust within/anomaly forms.
- **discharge** — weak (~0.39, inverse).

### WQP water quality (`feature_significance_wqp.md`) — coverage **123/133 lakes**
Genuine **driver** signals (consequences chl-a/turbidity/Secchi/DO flagged out):
- **antecedent TP** (`lag4`, **forecast-eligible**, +, within 0.558, 72 lakes, within-sig) — 4-week-
  lagged total phosphorus positively predicts bloom. The key nutrient lead.
- **water-temperature warm anomalies** (`anomR`, +, within 0.690, 28 lakes) — warmer-than-normal weeks.
- **orthophosphate & ammonia** — **inverse** coincident (within ~0.42/0.37): consistent with nutrient
  **drawdown/uptake** during blooms (a same-week diagnostic, not a driver direction to act on).

### chl-a as a leading indicator — the lead-vs-persistence test (`chla_leadlag.md`)
WQP chl-a is a *direct in-situ* measurement, distinct from CyAN's remote cyano-index. Conditioning on
**CyAN-clear at the cutoff** (isolating lead from bloom-state persistence), antecedent chl-a predicts a
CyAN bloom h weeks later at **AUC_within 0.63→0.59 (h=1→4)** — **real, independent lead**. But CyAN's
own sub-threshold CI leads *better* (0.82→0.70). ⇒ **coincident chl-a is redundant** (barred from
driver claims, D-15); **lagged chl-a is a modest, independent early-warning feature** whose value is
catching sub-pixel/nearshore onset the lake-median misses.

### Weather — ERA5-derived (`feature_significance_weather.md`) — coverage **133/133 lakes** (dense)
The **strongest, most complete, and most forecast-eligible** driver layer (gridded → every lake; 102
lakes have both bloom classes for the within-lake test). Physically coherent:
- **Solar radiation + PET + warmth (GDD) → MORE bloom** — `ssrd_trail_14d/30d`, `pet_hargreaves`,
  `gdd`; **within-lake AUC ≈ 0.62–0.66 at lag1/2/4** (forecast-eligible) — the best leading signals.
- **Precipitation / wetness / SPEI → LESS bloom** (inverse, ~0.42–0.46) — flushing/dilution; wetter
  (high SPEI) suppresses.
- **Wind → LESS bloom; calm hours → MORE bloom** (~0.45 / 0.55) — mixing disrupts surface scums,
  stratification favors them.
27 reps pass the within-lake gate. All `driver` class (no consequence/circular issue). *Caveat:*
nearest-cell extraction at 0.25° (~28 km); SPEI reflects the 2026-07-05 recompute.

## Note — location / lake identity as a feature (2026-07-05 audit)
Neither our fitted models nor EPA's use **discrete lake identity** (no COMID dummy / one-hot / per-lake
random intercept / lat-lon). **EPA** represents location with a *generalizing* continuous **SPDE spatial
field** (~88 km range) + static morphology (area, mean depth) — `conus_inla.R:199`. **We** use no
discrete ID either, but the fitted AR-ladder logistic carries a **per-lake per-month climatology**
(`clim`) — a learned per-lake base rate (category-4 identity-by-proxy) that **EPA does not use**.
*Direction (user 2026-07-05, pending finalization):* prefer generalizability → **demote per-lake
climatology to a reported baseline (not a model feature)**, replace its between-lake role with EPA-style
generalizing signals (static morphology incl. depth, general week-of-year seasonality, optional coarse
spatial), and **prove generalization with the blocked-lake (leave-lakes-out) stress test**.

## Candidate feature set for fusion (from this screen)
- **CyAN antecedent ladder** (already the baseline to beat) + **lake area** (D-27) + **inundation**.
- **WQP:** antecedent **TP** (lag), **water-temp anomalies**, **ammonia/orthoP** (drawdown, diagnostic),
  **lagged chl-a** (independent lead, ablation group).
- **NWIS:** **water temperature**, **gage-height anomalies** (inverse), where gauged (25 lakes only).
- **Weather (ERA5) — the main forecast-eligible driver layer, all 133 lakes:** solar radiation
  (`ssrd_trail`), PET, GDD (**+**, lags forecast-eligible ~0.62–0.66); precip/SPEI (**−**, flushing);
  wind (**−**) / calm-hours (**+**).

## Limitations (honest)
1. **WQP not unit/fraction-harmonized** (mixes total/dissolved P, chl-a methods) → nutrient signals
   indicative only; **harmonize before modeling**.
2. **TN & pH grossly undercounted** by characteristic-name misses → need alias/pCode discovery.
3. **NWIS coverage 25/133**; WQP 123/133; static gradients compressed.
4. `same_week` reps are diagnostic, not forecast skill; only `antecedent` (lag) reps are
   forecast-eligible.
5. A few sites fall in >1 lake buffer (kept first, ≤12); direct tier suppresses watershed; WQP chl-a
   ~monthly (sparse).
6. Screen = univariate association; multivariate/incremental value over the CyAN ladder is the modeling
   test — **now shown below** (was: not shown here).

---

## Multivariate importance — the modeling test (Exp 4 / 4b, 2026-07-06, Codex-reviewed)

The univariate screen above is permissive by design. The multivariate test asks: **in the fitted
fusion model, which features actually carry held-out skill?** Method = **correlation-clustered grouped
permutation importance** (`exp_perm_importance.py` → `outputs/exp_perm_importance.md`): cluster the 44
features by |Pearson r| on train (complete linkage, within-cluster |r|≥0.7 → 27 clusters — needed
because 47 pairs are |r|>0.8, so per-feature importance would under-credit redundant twins), refit
fusion_full+clim, then grouped-permute each cluster on held-out test (20 shuffles) and measure the drop
in **onsetMCC** (alert-decision metric, at the fixed val-tuned threshold), **AUC_within**, and **pooled
AUC**. Reported for HistGBM/XGBoost/logistic. *std = shuffle variability only, not full statistical
uncertainty; test-set attribution is descriptive (Codex).*

**Result — one signal dominates.** The CyAN-level cluster (real-time CyAN + `clim`) accounts for
essentially all skill: scrambling it drops HistGBM onsetMCC 0.466→0.002, AUC_within 0.897→0.522, pooled
AUC 0.980→0.514, same for XGBoost/logistic. **No other cluster has large, cross-architecture
importance** — the next tier (`cyan_sd` +0.038, solar/season +0.030, `area_sqkm` +0.018) is small,
onset-specific (≈0 on pooled/within AUC), and inconsistent across architectures (logistic shows several
negatives). Honest wording (Codex): "small/inconsistent," **not** "noise," and "little *incremental
held-out* skill in this full model," **not** "the variables contain no signal" (the univariate screen
did find weather/in-situ associations).

**Decomposition — real-time CyAN vs `clim` (Exp 4b, `exp_perm_c1_decomp.md`).** The dominant cluster
mixes the *generalizable* real-time CyAN observation with `clim` (per-(comid,month) base rate =
identity-by-proxy). Splitting them (HistGBM): `clim` ALONE Δ onsetMCC **+0.351** / pooled **+0.260** vs
ALL-real-time-CyAN-no-clim +0.300 / +0.082 — **a single base-rate feature is leaned on as hard as all
15 CyAN features combined** (robust in both tree models; logistic leans more on real-time CyAN). Yet the
block ablation shows **removing** `clim` costs only onsetMCC 0.466→0.398. Reconciliation: `clim` is
**redundant-but-heavily-exploited** — the signature of a memorization shortcut (large *permutation*
reliance, tiny *drop-column* unique value, because correlated CyAN replaces it on refit). Within
real-time CyAN: current-week obs is the workhorse (+0.214), lags secondary (+0.091), bloom-state/quality
≈0.

**Implications for the model spec:**
- **The deployable model is the clim-free, generalizable real-time-CyAN autoregression.** A clim-free
  model ranks onsets strongly (onsetAUC 0.935, onsetMCC 0.398, AUC_within 0.893) with **no per-lake
  identity** — skill does not require memorization. Including `clim` buys +0.068 onsetMCC at the cost of
  the model routing predictions through per-lake base rate → **empirically vindicates D-35** (keep
  `clim` a baseline, not a feature).
- **Weather / in-situ / morphology fusion adds no incremental held-out skill that survives** — consistent
  with the fusion eval (D-35) and block ablation (D-38d). A clear-eyed negative on fusion value.
- **`area_sqkm` is a whisper, not a headline driver** (Δ onsetMCC ~+0.018, Δ pooled ~0; not cross-arch
  robust; not FDR-significant in the static screen) — **walks back D-27's "headline feature" framing**
  (which was domain-reasoned, not empirically supported). See D-39.
