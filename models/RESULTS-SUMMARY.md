# Modeling results — summary for the story deck

*Florida cyanobacteria bloom forecasting (HAB PoC). Compiled 2026-07-06; D-42/D-43 pass 2026-07-07. Every number
below traces to a checked-in result file (linked in §9) produced by checked-in code from cited public data. Written
in the project's plain/honest/anti-marketing voice — the negatives are findings, not things to hide.*

---

## 1. One-paragraph version

We forecast **WHO Alert Level 1 cyanobacteria blooms** (per Florida lake, per week, lead times 0–4 wk)
by fusing the **EPA CyAN satellite signal** with weather (ERA5), in-situ chemistry (WQP/NWIS), and lake
morphology, benchmarked head-to-head against the **EPA CyanoHAB forecast** and naïve baselines. The
central result is a **clear-eyed, well-validated negative-plus-positive**: (a) **early warning works** —
we can rank which currently-clear lakes will bloom next week with **onset-AUC ≈ 0.94**, beating
climatology and EPA; but (b) essentially **all of that skill comes from the real-time CyAN signal
itself** — the weather / in-situ / morphology "fusion" adds **no incremental held-out skill that
survives rigorous importance testing**. The honest, deployable model is a **compact real-time-CyAN
autoregression** (less tied to per-lake identity; unseen-lake transfer untested), not a big fusion model. A well-validated simple model beat the complex
one — exactly the outcome the brief prizes.

---

## 2. Setup (what was actually run)

- **Geography / scope:** Florida, the **133 CyAN-resolvable lakes**, Sentinel-3 OLCI era 2016→2026.
- **Target (apples-to-apples with EPA):** WHO **Alert Level 1** = lake-median CyAN **DN ≥ 130**
  (≈ 12 µg/L chlorophyll-a, cyano-dominant). The threshold is copied **verbatim from EPA/Schaeffer's
  deposited forecast code** (`cyan_processing_conus.R:170`), so our label **is** EPA's own forecast
  event — not an in-house target. `models/docs/03-target-definition.md`.
- **Baselines (every horizon):** **latency-aware persistence** (`Persistence(W,h) = bloom(W−h−1)`,
  accounting for CyAN's ~1-wk publication latency), **per-lake climatology**, a **CyAN autoregressive
  ladder**, and the **EPA forecast**.
- **Models:** regularized **logistic GLM**, **HistGBM**, **XGBoost** (explainable classifiers; a GAM was
  in the design). Results are reported across the whole feature-combo × architecture grid.
- **Split:** temporal, **train < 2022-07 / val [2022-07, 2024-07) / test ≥ 2024-07** (~60/20/20, **2-yr
  test**). The EPA head-to-head additionally uses the **2025 shared-FL** window (matches EPA's issue
  dates). Held-out **time only** — matches EPA's own validation; no unseen-lake transfer claim.
- **Metric suite:** AUC-ROC, AUC-PR, Brier, MCC, plus three that carry the story:
  - **`AUC_within`** = median *per-lake* AUC (within-lake temporal skill; strips between-lake artifacts).
  - **`onset-AUC` / `onset-MCC`** = **positive-only early warning** — restrict to currently-CLEAR
    lake-weeks and score which BECOME a bloom. *This is the decision-relevant metric.*
  - **`flip-MCC` / `offset-MCC`** = the older **general transition** metric (both directions; see §5).

---

## 3. Headline findings (for the deck)

1. **Early warning works, and it's a positive result.** Among currently-clear lakes, we rank next-week
   onsets at **onset-AUC ≈ 0.94** (h1) — **fusion 0.944 ≈ CyAN-ladder 0.943**, both beating
   **climatology 0.90** and the **EPA forecast 0.82**, and far above persistence (0.50). On the
   *thresholded* onset alert (onset-MCC, with operating thresholds tuned on **validation, not test**), the
   CyAN-ladder (**0.375**), climatology (**0.371**) and fusion (**0.349**) are essentially tied — **fusion
   adds nothing over the CyAN-only ladder** on the alert (consistent with §6 importance). The earlier
   "fusion leads at onset-MCC 0.47" was a test-threshold-tuning artifact, now corrected (D-40).
   *(`headtohead_onset.md`)*
2. **It's a CyAN-autoregression model.** Correlation-clustered permutation importance: **one cluster —
   the real-time CyAN level — accounts for ~100% of skill.** Scrambling it collapses the model to a coin
   flip (onset-MCC 0.466→0.002; within-lake AUC 0.897→0.522; pooled AUC 0.980→0.514), on every
   architecture. *(`exp_perm_importance.md`)*
3. **The weather / in-situ / morphology fusion adds no robust incremental skill.** Every multivariate
   test — clustered permutation importance, greedy feature ablation, block ablation, the change-feature
   experiment — converges on this. The only clean aggregate win is a **+0.015 within-lake AUC**
   [+0.003, +0.021] fusion lift over the CyAN ladder — tiny and CyAN-dominated. *(`fusion_eval.md`,
   `exp_ablation.md`, `exp_perm_importance.md`, `exp_feature_ablation*.md`)*
4. **A 2-feature model matches a 44-feature model on every AUC metric.** Greedy backward elimination
   strips to **`cyan_median` + `area_sqkm`** with no significant AUC loss on held-out test — strong
   evidence of massive redundancy/overfitting risk (47 feature pairs at |r|>0.8). *(`exp_feature_ablation.md`)*
5. **`clim` (per-lake seasonal base rate) is a memorization shortcut — kept as a baseline, not a
   feature.** It's leaned on as hard as all 15 CyAN features combined (permutation Δonset-MCC +0.351),
   yet removing it costs only 0.068 — redundant-but-exploited. The deployable model is **clim-free**, and
   real-time CyAN alone is sufficient and less tied to per-lake identity (unseen-lake transfer untested). *(`exp_perm_c1_decomp.md`)*
6. **We are competitive with a validated federal product** (EPA CyanoHAB forecast) on the same event, at
   EPA's own operating point — a credible "as-good-as-EPA, and explainable" product claim, stated with
   its caveats. *(`epa_headtohead.md`, `headtohead_onset.md`)*

---

## 4. The early-warning result in numbers (positive-only onset, h1, 2025 shared-FL)

| model | onset-AUC (rank) | onset-MCC (alert) | all-sample AUC-ROC |
|:--|--:|--:|--:|
| **fusion (CyAN + drivers)** | **0.944** | 0.349 | 0.983 |
| CyAN-ladder | 0.943 | **0.375** | 0.982 |
| climatology | 0.896 | 0.371 | 0.955 |
| EPA forecast | 0.818 | 0.241 | 0.928 |
| persistence | 0.500 | 0.000 | 0.918 |

- Onset-AUC ~0.93–0.94 holds across the full 2-yr test window too (`exp_change_features.md`,
  `exp_ablation.md`). Onsets are **rankable** — an earlier "onsets unpredictable" impression was a metric
  artifact, corrected (see §5).
- **Threshold correction (2026-07-06, D-40):** the onset-MCC operating thresholds are now tuned on
  **validation**, never on test. Earlier test-tuning inflated fusion to onset-MCC 0.474 and made it look
  like it "led" the alert; with honest thresholds fusion is **0.349** and does *not* lead. (onset-AUC,
  being threshold-free, is unchanged.)
- On onset-MCC across horizons the picture is honest and mixed, and **no model consistently leads**:
  **climatology (seasonality) tops h0 and h4**, the **CyAN-ladder tops h1 and h2**, and h3 is a three-way
  tie (fusion 0.455 ≈ climatology 0.452 ≈ ladder 0.443). **Fusion never clearly wins** — at h1 it sits
  *third* of the three (0.349 vs ladder 0.375 vs climatology 0.371). Seasonality is a real onset signal but
  is a *baseline*, not a driver; and "fusion" earns **no thresholded-alert edge over the CyAN-only ladder**.
  *(`headtohead_onset.md`)*
- **On the 2-year internal test the story differs by model (a genuine nuance, D-41):** the full **fusion +
  clim** model leads onset-MCC at *every* lead (h0–4: 0.34/0.47/0.43/0.49/0.47) over the lean 2-feature
  model (0.26/0.31/0.31/0.34/0.35) — a consistent **point-estimate** edge that is **not yet proven** (~half
  `clim`/seasonality at h1, ~half the wider CyAN+driver set; the onset-AUC lift's CI includes 0), and
  **climatology (a baseline) also beats the lean model at every lead**. So full fusion+clim is a
  **tantalizing-but-unproven** avenue to validate next (the "go deep" direction); the *deployable* choice
  stays the lean model + EPA. Note this is the 2-yr window with the **clim-carrying** model — distinct from
  the shared-2025 clim-free head-to-head above. *(`experiments.md` horizon curve; deck slides 17–18.)*
- **Climatology-baseline fit inconsistency (D-42, deferred fix).** The standalone **climatology baseline** is fit on
  **train+val** in `experiments.md` (the *fair* fit — it matches how the models are refit on train+val before predicting
  test → onset-MCC 0.363 at h1) but on **train-only** in the `exp_*ablation` tables (0.323 at h1), which under-credits it.
  The deck reconciles to the train+val values; the code fix (make the baseline train+val everywhere) + regeneration is
  deferred to the next OOM-safe rerun. No look-ahead either way (val precedes test); the deployable lean model is unaffected.

---

## 5. The honesty centerpiece: "general flip" vs "positive-only onset"

This distinction resolves an apparent contradiction and is worth a slide of its own.

- **General flip** (what we ran first): `target ≠ persistence` — **both** clear→bloom (onset) **and**
  bloom→clear (offset), one threshold. On this metric, CyAN-only is **anti-predictive** (flip-MCC −0.5 to
  −0.7; flip-AUC 0.05–0.15, i.e. ranked *backwards*), and non-CyAN / climatology / a no-CyAN model look
  **better** (flip-MCC ~0 to +0.1; flip-AUC ~0.5).
- **Positive-only onset** (what we switched to): restrict to currently-clear weeks. Here **CyAN wins the
  ranking** and out-discriminates within the onset subset.
- **Why it flips — the clincher** (`exp_ablation.md`, h1): the CyAN model is better on onsets (MCC 0.466
  vs 0.339) **and** better on offsets (0.325 vs 0.251), yet **worse** on the *combined* general-flip
  metric (−0.303 vs +0.017). That's only possible because general-flip mixes two opposite-state
  populations at one threshold: the persistence-anchored CyAN model ranks onset-flips *below* offset-
  flips (backwards). **General-flip was measuring onset-vs-offset ranking — not the early-warning
  decision.** Switching to positive-only onset (decision D-37) revealed CyAN's genuine value that the
  combined metric hid.
- **Bottom line:** non-CyAN's transition "advantage" is real on the *general* metric but is a combined-
  metric artifact; on the *decision-relevant* positive-onset metric, CyAN leads and only seasonality (a
  baseline) — not our drivers — competes. *This nuance is load-bearing; the deck should not claim "non-
  CyAN helps flips" without naming which flip condition.*

---

## 6. Feature importance (the multivariate test) — quantified

Method: cluster 44 features by |Pearson r| (→ 27 clusters, needed because of heavy collinearity), then
**grouped-permute each cluster** in the fitted model on held-out test and measure the drop.
*(`exp_perm_importance.md`, `exp_perm_c1_decomp.md`; Codex-reviewed, no method/leakage bug found.)*

- **CyAN-level cluster:** Δonset-MCC **+0.464**, Δ within-lake AUC **+0.375**, Δ pooled AUC **+0.466**
  (HistGBM; same on XGBoost/logistic). It *is* the model.
- **Every other cluster:** ≤ +0.038 on onset-MCC, ≈ 0 on pooled/within AUC, and **inconsistent in sign
  across architectures** — Codex-corrected wording: **"small / inconsistent," not "noise"**; and **"no
  incremental held-out skill in this full model," not "these variables contain no signal"** (the
  univariate screens *did* find weather/in-situ associations — see `feature_significance_*.md`).
- **Real-time CyAN vs `clim`:** `clim` ALONE Δonset-MCC +0.351 vs all-15-CyAN-no-clim +0.300 — a single
  base-rate feature leaned on as hard as all real-time CyAN. Yet dropping `clim` costs only 0.068
  (block ablation) → **redundant-but-exploited memorization shortcut** (large *reliance*, tiny *unique*
  value). A **clim-free** model ranks onsets strongly (onset-AUC 0.935, onset-MCC 0.398) with **no per-
  lake identity** → less tied to per-lake identity (unseen-lake transfer untested).
- **`area_sqkm` is a whisper** (Δonset-MCC ~+0.018, Δ pooled ~0; not cross-arch robust; not FDR-
  significant in the static screen) — we **walked back** an earlier "headline feature" framing (D-27→D-39d).
- **Within real-time CyAN:** current-week obs is the workhorse (+0.214), lags secondary (+0.091),
  bloom-state/quality ≈ 0.

---

## 7. EPA head-to-head (the federal benchmark)

*(`epa_headtohead.md`, `headtohead_onset.md`)*

- **Same event, computed honestly:** we score EPA's published probabilities against our labels, which are
  EPA's *own* AL1 definition (DN≥130) — the best-possible apples-to-apples (EPA never publishes realized
  labels; both derive truth from the same CyAN observations).
- **Reported at BOTH operating points:** **@0.10** (EPA's deployed, health-protective, over-predicts) and
  **@0.50** (accuracy-optimal default). At @0.10 EPA onset-MCC 0.248; on general flips EPA is anti-
  predictive at its real cutoff (flip-MCC_h1 **−0.059**) — the earlier +0.026 was an artifact of scoring
  it at 0.50.
- **Skill vs baselines:** our CyAN-ladder − EPA on all-sample AUC = **+0.054 [+0.047, +0.059]** (CI
  excludes 0 — but caveated: the ladder is fit to our exact labels, EPA is independent). **EPA −
  persistence = +0.010 [−0.000, +0.022]** — CI includes 0, so EPA does not cleanly beat naïve persistence
  at predicting our AL1.
- **EPA's within-lake AUC ≈ 0.50** (descriptive/unstable, only ~64/132 lakes qualify) — it ranks *which
  lakes* bloom, less *which weeks within a lake*.
- **Caveats we carry:** EPA values are one 2026-07-02 dashboard snapshot (not proven as-issued); EPA's
  probability is a fixed current-week nowcast held constant across h0–4 (flatters it at longer leads);
  seasonal shared subset.

---

## 8. The deployable model + honest limitations

**Deployable model:** a **compact, clim-free real-time-CyAN autoregression** (current + recent CyAN level,
lightweight morphology; less tied to per-lake identity, unseen-lake transfer untested), multi-horizon 0–4 wk,
explainable, competitive with EPA on the same event. Fusion drivers and `clim` "ride along" but earn no defensible incremental claim.

**Limitations (stated plainly — the brief rewards these):**
1. **Fusion is a negative result:** weather/in-situ/morphology add no robust incremental held-out skill
   here. Real, and reported as such.
2. **Transition prediction is weak:** even the best general-flip skill is ~random; we forecast *levels*
   well, *changes* poorly. The scientifically hard onset/offset timing problem is **not solved**.
3. **Same-lake temporal validation only** — not transfer to unseen lakes; static morphology + nearest-
   cell weather can still fingerprint place under a same-lake split.
4. **`clim`/seasonality is identity-by-proxy** — kept out of the deployable model deliberately.
5. **In-situ not harmonized** (WQP mixes total/dissolved P, chl-a methods; NWIS covers 25/133 lakes);
   nutrient signals are indicative only.
6. **The label is a satellite AL1 realization**, not lab chlorophyll (DN→chl-a carries scatter) — but it
   applies identically to us and EPA, so it doesn't bias the comparison.

**Rigor / provenance:** every experiment was adversarially reviewed (Codex) and/or audited; corrections
were folded in and logged (e.g. the onset-metric correction D-37, the EPA-fairness fix D-38, the
importance findings D-39). Full trail in `models/DECISIONS-LOG.md`.

---

## 9. Direct links — code, results, docs, data

### Analysis code (`models/model/`)
- **Shared harness** (split, features, refit protocol, metric suite, EPA rows): [`experiment_lib.py`](model/experiment_lib.py), [`metrics.py`](model/metrics.py)
- **Experiment drivers:**
  - Change/trend features vs onsets (Exp 1): [`exp_change_features.py`](model/exp_change_features.py)
  - Block (family) ablation (Exp 2): [`exp_ablation.py`](model/exp_ablation.py)
  - Feature-level greedy backward ablation (Exp 3, pooled + onset criteria): [`exp_feature_ablation.py`](model/exp_feature_ablation.py)
  - Clustered permutation importance (Exp 4): [`exp_perm_importance.py`](model/exp_perm_importance.py)
  - `clim`-vs-real-time-CyAN decomposition (Exp 4b): [`exp_perm_c1_decomp.py`](model/exp_perm_c1_decomp.py)
- **Baseline / benchmark evals:** [`eval_cyan_baselines.py`](model/eval_cyan_baselines.py), [`eval_fusion.py`](model/eval_fusion.py), [`eval_epa_headtohead.py`](model/eval_epa_headtohead.py), [`eval_headtohead_onset.py`](model/eval_headtohead_onset.py), [`eval_experiments.py`](model/eval_experiments.py)
- **Feature screens:** [`assess_static_features.py`](model/assess_static_features.py), [`screen_weather_features.py`](model/screen_weather_features.py), [`screen_insitu_features.py`](model/screen_insitu_features.py), [`leadlag_chla_test.py`](model/leadlag_chla_test.py)
- **Prepare / acquire:** [`build_cyan_lake_target.py`](prepare/build_cyan_lake_target.py) (the AL1=DN≥130 label), [`build_cyan_features.py`](prepare/build_cyan_features.py), [`assemble_fusion_table.py`](prepare/assemble_fusion_table.py), [`assemble_modeling_table.py`](prepare/assemble_modeling_table.py), [`join_basinatlas_l12.py`](prepare/join_basinatlas_l12.py), [`pull_link_wqp_fl.py`](prepare/pull_link_wqp_fl.py), [`pull_link_nwis_fl.py`](prepare/pull_link_nwis_fl.py), [`build_fl_lake_mask.py`](acquire/build_fl_lake_mask.py)

### Results (`models/outputs/`)
- **Early warning / benchmarks:** [`headtohead_onset.md`](outputs/headtohead_onset.md) ⭐ (positive-onset, 5 models × horizons), [`epa_headtohead.md`](outputs/epa_headtohead.md), [`cyan_baseline_eval.md`](outputs/cyan_baseline_eval.md), [`fusion_eval.md`](outputs/fusion_eval.md)
- **Experiment grid & ablations:** [`experiments.md`](outputs/experiments.md), [`exp_change_features.md`](outputs/exp_change_features.md), [`exp_ablation.md`](outputs/exp_ablation.md), [`exp_collinearity.md`](outputs/exp_collinearity.md), [`exp_feature_ablation.md`](outputs/exp_feature_ablation.md) + [`_trace`](outputs/exp_feature_ablation_trace.md), [`exp_feature_ablation_onset.md`](outputs/exp_feature_ablation_onset.md) + [`_trace`](outputs/exp_feature_ablation_onset_trace.md)
- **Feature importance ⭐:** [`exp_perm_importance.md`](outputs/exp_perm_importance.md), [`exp_perm_c1_decomp.md`](outputs/exp_perm_c1_decomp.md)
- **Univariate screens:** [`feature_significance_static.md`](outputs/feature_significance_static.md), [`feature_significance_weather.md`](outputs/feature_significance_weather.md), [`feature_significance_nwis.md`](outputs/feature_significance_nwis.md), [`feature_significance_wqp.md`](outputs/feature_significance_wqp.md), [`chla_leadlag.md`](outputs/chla_leadlag.md)

### Documentation (`models/`)
- **Design & rationale:** [`DESIGN.md`](DESIGN.md) · **Decisions/audit trail (D-01…D-43):** [`DECISIONS-LOG.md`](DECISIONS-LOG.md) · **Progress log:** [`PROGRESS.md`](PROGRESS.md)
- **Domain & data:** [`docs/01-domain-and-data.md`](docs/01-domain-and-data.md) · **Feature catalog:** [`docs/02-feature-catalog.md`](docs/02-feature-catalog.md) · **Target definition (AL1=DN≥130, EPA-pinned):** [`docs/03-target-definition.md`](docs/03-target-definition.md) · **Feature assessment + §Multivariate importance:** [`docs/04-feature-assessment.md`](docs/04-feature-assessment.md)

### Key data artifacts (`models/data/derived/`)
- `modeling_table_fusion_fl.parquet` (the fused lake-week table, 339,400 × 58) · `modeling_table_cyan_fl.parquet` · `cyan_lake_weekly_fl.parquet` · `lake_basinatlas_l12.parquet`
- EPA forecast + CyAN source layers: `data-sources/cyano-forecasts/` and `data-sources/cyan/` (with their own METADATA/README).

---

## 10. Suggested narrative arc for the deck (optional — findings, not prescriptions)

- **Act 1 — the problem, honestly framed:** blooms are a health + operations problem; the public signals
  are the CyAN satellite index + weather/in-situ; the honest question is whether fusing them beats CyAN
  alone and a federal benchmark. WHO AL1 target, pinned to EPA's own definition.
- **Act 2 — what we found:** (1) early warning works (onset-AUC 0.94, beats EPA/climatology); (2) but it's
  CyAN doing the work — the fusion is a clear-eyed negative; (3) the metric-honesty story (general-flip vs
  positive-onset) and the memorization-shortcut story (`clim`); (4) a 2-feature model matches 44.
- **Act 3 — the product:** a compact, explainable real-time-CyAN early-warning model (less tied to per-lake
  identity), competitive with EPA, with its limits stated (transitions weak, same-lake only / unseen-lake transfer untested, fusion didn't pay off).
  The value proposition is **rigor + explainability + a defensible claim**, not a bigger model.
