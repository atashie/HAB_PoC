# DECISIONS LOG — modeling layer

Append-only. Newest entries at top. Each entry: date, decision, rationale, and (where relevant) what
it supersedes. This is the audit trail for *why* the model is built the way it is.

---

## 2026-07-07 — Climatology baseline fit inconsistency; full-deck value audit (D-42)

- **D-42 — the climatology BASELINE is fit two different ways across the modeling scripts, which surfaced as
  a cross-slide numeric conflict in the deck.** `eval_experiments.py` (→ `experiments.md` → deck slides
  15 & 18) fits the per-lake-per-month base-rate table on **train+val** for the test prediction
  (`add_clim(fit, te)`, `fit = concat[tr, va]`), mirroring how the models are refit on train+val before
  predicting test. `experiment_lib.py::run_experiment` (→ `exp_feature_ablation.md` → deck slide 17) fits the
  same baseline on **train-only** (`add_clim(trh, teh)`). Persistence and the fusion models are byte-identical
  across both files (same test rows), so this is purely the baseline's fit source — and because onset-**AUC**
  (threshold-free) differs too (0.886 vs 0.851), it is the climatology *probabilities* that differ, not a
  threshold effect. Values: train+val **0.952 / 0.886 / 0.363** (pooledAUC / onsetAUC / onsetMCC) vs
  train-only **0.936 / 0.851 / 0.323**.
- **Which is correct:** train+val is the *fair* baseline — the deployed models get train+val, so the baseline
  should too; train-only handicaps it (no leakage either way: train+val all precede the ≥2024-07 test). The
  train-only version under-credits climatology.
- **Decision (user, 2026-07-07): patch the deck now, defer the code fix to the next rerun** (avoids re-running
  the OOM-sensitive modeling layer today). Deck slide 17's climatology row was changed 0.936/0.851/0.323 →
  **0.952/0.886/0.363** (the train+val values from `experiments.md`) so slides 15/17/18 are internally
  consistent; slide 17's source note now attributes the climatology row to `experiments.md` (train+val). A
  precise `# TODO (D-42)` was added at the fix site in `experiment_lib.py` (predict on train+val, keep the
  threshold train-only). **On next rerun:** apply that fix, regenerate `exp_feature_ablation.md` /
  `exp_ablation.md`, and re-source slide 17's climatology from `exp_feature_ablation.md` (it will then equal
  `experiments.md`). Consequence to keep in mind: with 0.363, climatology (a baseline) clearly beats the lean
  model on onset-MCC at h=1 too — already the story on slide 18; the lean model's case rests on cost,
  generalization, and overall/level skill (AUC 0.982), not on beating climatology at onset.
- **Full-deck value audit (4 parallel review agents, per user request).** Every numeric claim across all 28
  slides + `results.json` / `story_data.js` was traced to `models/outputs/*.md`. **The climatology baseline
  above was the only genuine cross-source data conflict.** Three secondary fixes applied: (a) slide 18's
  "fusion leads at **every** lead" / "fusion > climatology > lean > EPA" was **false at h4** (climatology
  0.476 > fusion 0.466) — reworded to "leads the *lean* model at every lead; climatology edges fusion by h4;
  ordering holds through h3"; (b) slide 18's "h=1 numbers = slide 17" claim narrowed to exclude the EPA
  marker (0.241 shared-2025 vs 0.248 2-yr); (c) slide 16's "each costs 0.05–0.09" softened to "roughly
  0.05–0.09" (weather block is 0.047). **Verified clean:** all scope/counts (133 universe vs 132 evaluable,
  4,527 weeks, 28.8% / 26.6% base rates, 261 sources, N=12 tools, 44→2 features, costs), the 2.8%→5.8% onset
  base rate (no stale "3.7%→7.2%" remains), and all other metric values trace correctly. Cross-window
  differences (e.g. climatology onset-MCC 0.371 shared-2025 vs 0.363 2-yr) are legitimate, not conflicts.

## 2026-07-06 — Onset-MCC by horizon; full-fusion framed "tantalizing but unproven" (D-41)

- **D-41 — the full fusion + clim model's onset-MCC edge is presented as a "tantalizing but not-yet-proven"
  avenue (deck slide 17/18), NOT a validated claim; we ship the lean 2-feature CyAN model + EPA.** Prompted
  by the user's (fair) push that onset-MCC **0.466** (full+clim) / **0.398** (clim-free) are substantially
  above lean **0.314** on the **2-year** held-out test — the *more-robust* window (≈2× the data of the
  shared-2025 subset). Added onset-MCC across horizons to `eval_experiments.py` (plus a `lean` 2-feature
  suite); `experiments.md` horizon curve now carries onset-MCC/onset-AUC.
- **Finding:** full fusion+clim leads onset-MCC at **every** lead (h0–4: 0.34/0.47/0.43/0.49/0.47) vs lean
  (0.26/0.31/0.31/0.34/0.35). The full-vs-lean gap at h1 is ~half `clim` (+0.068) and ~half the wider
  CyAN+driver set (+0.084). **But** it is not significance-tested, the onset-AUC lift's bootstrap CI
  includes 0, and **climatology (a baseline) also beats lean at every lead** and nearly ties fusion by h4 —
  so much of the "edge" is **seasonality**, which the full model carries via `clim`.
- **Corrections to my earlier wording (logged for honesty):** (a) "the onset edge is *mostly* clim" was
  wrong — it's ~half clim, ~half the broader feature set; (b) leaning on the shorter shared-2025 window
  (fusion 0.349 "ties" the ladder) to dismiss it conflated a *smaller seasonal subset* **and** a
  *clim-free-vs-clim* comparator — the 2-yr window is the more robust estimate.
- **Deck changes:** slide 17 reframed (full fusion "tantalizing, unproven"; lean "shipped for PoC"); slide
  18 gains the onset-MCC-by-horizon figure (2-yr window; EPA as its 2025 point); slide 16's two ablation
  charts merged into one shared-axis figure; **"Go home" → "Go simple" = lean-CyAN + EPA**; production
  table + recommendation realigned. The **aggregate / ranking** fusion-negative (D-35/D-39) is unchanged;
  this nuance is specific to the thresholded **onset-MCC** decision metric.
- **onset-MCC *rises* with lead time = an artifact, not improving skill (verified for slide 18).** The onset
  base rate **~doubles over h0→h4 (2.8%→5.8%** on the 2-yr test; a lake clear h+1 wk ago is likelier to have
  bloomed by the target week), and long-lead onsets are more *seasonal* — so the thresholded onset-MCC climbs
  even though every **ranking** metric falls with lead (all-weeks AUC 0.985→0.970; onset-AUC 0.934→0.925
  fusion, 0.925→0.910 lean; climatology's onset-AUC *rises* 0.876→0.909 because long-lead onsets are seasonal).
  Slide 18 states this and must be read **model-vs-model at each fixed lead**, not as a trend. Corrects a stray
  "3.7%→7.2%" (that was the shared-2025 window, not the 2-yr window slide 18 plots).

## 2026-07-06 — Onset head-to-head operating thresholds moved from test → validation (D-40, Codex-flagged)

- **D-40 — Evaluation-leakage fix in `eval_headtohead_onset.py`: onset-MCC thresholds were tuned on TEST,
  now tuned on VALIDATION.** A follow-up Codex leakage re-review (of the "no temporal overlap in
  `cyan_median`" claim — which **survived** recomputation) found a *separate* evaluation leak: the onset
  head-to-head script fit its models on train+val but then picked the F1 operating threshold for
  climatology / CyAN-ladder / fusion on the **test** labels (`best_f1_threshold(y_test, …)`), which
  inflates every thresholded onset-MCC. **Fix:** fit threshold-models on **train**, pick the F1 threshold
  on **validation** predictions, then score on test; EPA keeps its fixed **0.10 / 0.50** cutoffs;
  persistence = 0.5. Re-ran → `headtohead_onset.md` regenerated.
- **Effect (h1, shared-FL 2025):** fusion onset-MCC **0.474 → 0.349**. The earlier "fusion leads the
  thresholded onset alert" was a **test-threshold-tuning artifact**. With honest thresholds the alert is a
  near three-way tie — **CyAN-ladder 0.375 ≈ climatology 0.371 ≈ fusion 0.349** — i.e. **fusion adds no
  thresholded-alert skill over the CyAN-only ladder**, consistent with the permutation-importance finding
  (D-39b) that one CyAN cluster carries ~all the skill. This **strengthens** the clear-eyed fusion-negative
  result; it weakens no positive claim. onset-**AUC** (threshold-free, the ranking metric) is
  **unaffected**: fusion 0.944 ≈ ladder 0.943 > climatology 0.896 > EPA 0.818 > persistence 0.500.
- **Scope — what was NOT affected.** Only `eval_headtohead_onset.py` carried this bug. The shared
  experiment harness (`experiment_lib.py`) already tuned thresholds on val (Codex confirmed no val/test
  target leak), so the permutation-importance / ablation / decomposition numbers (D-39, the `exp_*`
  outputs, `docs/04`) stand unchanged. EPA's onset-MCC is computed at fixed cutoffs and is unchanged
  everywhere (incl. `epa_headtohead.md`). Propagated to `RESULTS-SUMMARY.md` (§3 headline #1, §4
  table+prose), `PROGRESS.md` (status log + a superseded-marker on the D-37 entry), and
  `presentation/story.html` (baselines & final@1wk slides).
- **D-40b — deck onset-metric charts (traceability).** For the story deck's *model-families* (slide 14)
  and *feature-importance* (slide 16) charts, onset-AUC/onset-MCC columns were added to
  `eval_experiments.py` (per-family, val-tuned threshold) and a **20-shuffle per-block onset-MCC
  permutation** to `eval_fusion.py`; both outputs (`experiments.md`, `fusion_eval.md`) were regenerated
  and parsed into `results.json`. The pooled AUC/MCC family numbers are unchanged (deterministic). The
  block onset-MCC permutation shows **CyAN dominating the alert (Δ −0.247 ± 0.016 of a 0.334 baseline)**
  while non-CyAN blocks show *modest* permutation **reliance** (in-situ −0.089, static −0.070, weather
  −0.047) that is **not unique value** — block *ablation* barely moves skill and the 27-cluster test
  (D-39b) caps any single non-CyAN cluster <0.04 (the redundant-but-exploited signature, like `clim`).
  So the fusion-negative holds on the decision metric too; no conclusion changed.

## 2026-07-06 — Feature-level ablation + clustered permutation importance (D-39, Codex-reviewed)

- **D-39a — Feature-level greedy backward ablation: the model is AUC-saturated at ~2 features.** Both a
  pooled-AUC criterion and an onset-ranking-AUC criterion (`exp_feature_ablation.py`, two TOLs) strip
  fusion_full+clim to **`cyan_median` + `area_sqkm`** with no significant loss *on any AUC metric*
  (held-out bootstrap CIs include 0). BUT the lean set loses operating-point skill (onsetMCC 0.466→0.314,
  flipMCC_h1 −0.303→−0.680) — i.e. **greedy-on-AUC is the wrong tool for a thresholded alert**: pooled/
  onset *ranking* is saturated by the current-CyAN level, so AUC-selection is blind to the operating-
  point value the fuller set provides. Reported honestly (not a "ship 2 features" recommendation).
- **D-39b — Clustered permutation importance quantifies feature importance (`exp_perm_importance.py`).**
  Because of heavy collinearity (47 pairs |r|>0.8), per-feature importance is unreliable; we cluster by
  |r| (complete linkage, |r|≥0.7 → 27 clusters) and grouped-permute each cluster in the fitted model on
  held-out test, on onsetMCC / AUC_within / pooled AUC, across HistGBM/XGBoost/logistic. **One cluster
  (CyAN-level) accounts for ~100% of skill** (scramble → onsetMCC 0.466→0.002); no other cluster has
  large cross-arch importance. Codex-corrected wording: non-CyAN effects are **"small/inconsistent," not
  "noise"**; the fusion claim is **"little incremental *held-out* skill in this full model," not "no
  signal"** (univariate screens did find weather/in-situ associations). Codex found **no method/leakage
  bug** (grouped permutation correct; clim train-only for test).
- **D-39c — `clim` is a redundant-but-exploited memorization shortcut → stays a BASELINE (vindicates
  D-35).** Decomposition (`exp_perm_c1_decomp.py`, Codex's #1 follow-up): `clim` ALONE has permutation
  importance ≥ all 15 real-time CyAN features combined (HistGBM Δ onsetMCC +0.351 vs +0.300; pooled +0.260
  vs +0.082), YET removing it costs only onsetMCC 0.466→0.398 (drop-column). Large *reliance*, tiny
  *unique value* = the model routes predictions through per-lake base rate when offered it, though it
  doesn't need to. **Real-time CyAN alone is sufficient + generalizable** (clim-free: onsetAUC 0.935,
  onsetMCC 0.398, AUC_within 0.893, no per-lake identity). → Deployable model = **clim-free generalizable
  real-time-CyAN autoregression**; within it, current-week obs is the workhorse, lags secondary,
  bloom-state/quality ≈0.
- **D-39d — WALK BACK D-27 (lake area as a "headline feature").** Permutation importance shows `area_sqkm`
  is a *whisper* (Δ onsetMCC ~+0.018, Δ pooled ~0; not cross-arch robust; not FDR-significant in the
  static screen). D-27's "first-class, prominently-reported feature" framing was domain-reasoned
  (sub-300m waterbodies) but is **not empirically supported**; report area as a minor/context feature, not
  a driver. (Greedy keeps it only as the best *second* feature once CyAN is stripped to one column — a
  conditional artifact, not marginal importance.)

## 2026-07-06 — EPA-forecast representation audited & fixed; Part-2 ablation Codex-reconciled (D-38)

- **D-38a — Our target IS EPA's own event (audit-verified apples-to-apples).** A dedicated fairness
  audit traced `target_bloom` = `median CyAN DN ≥ 130` (`prepare/build_cyan_lake_target.py:43`),
  copied **verbatim** from Schaeffer's deposited code (`cyan_processing_conus.R:170` = "130 for
  12 ug/L") → WHO AL1. EPA's forecast predicts the **same** event; EPA never publishes realized labels,
  and both sides derive truth from the *same* CyAN observations, so scoring EPA's `percent_chance`
  against our labels is the **best-possible head-to-head, not an in-house-target bias**. The FL
  in-season base rate (29.8% vs EPA's national ~9–10%) is geography+season computed *at EPA's own 130
  cutoff* — not a threshold mismatch. Resolves the user's "are we judging EPA on our target?" concern.
- **D-38b — EPA now scored at BOTH operating points (was a fixed 0.5).** The harness scored EPA's
  threshold metrics (MCC/onset/offset/flip) at 0.5, which **misrepresented** EPA: at 0.5 it looked
  mildly skillful on flips (flipMCC_h1 +0.026) while at every real operating point it is anti-predictive
  (−0.06 to −0.14) — silently contradicting `epa_headtohead.md`. Fix (user 2026-07-06): report EPA at
  **@0.50** (symmetric-loss / accuracy-optimal default for calibrated probs) **AND @0.10** (EPA's
  PUBLISHED health-protective cutoff, Schaeffer 2024; over-predicts positives). Neither is test-tuned;
  0.10 is EPA's own choice. Threshold-free cols (AUC-ROC/PR/Brier/AUC_within/onsetAUC) are identical
  across the two. Verified re-score (n=6204 shared FL wks): overall MCC 0.636→0.672, onsetMCC
  0.233→0.248, **flipMCC_h1 +0.026→−0.059** at 0.10. Also labeled: EPA prob is a fixed current-week
  nowcast held constant across h0..4 (flatters EPA at longer leads).
- **D-38c — Reporting contract extended (user).** Every config table now shows **AUC-ROC, AUC_within
  (+ `AUC_within_n` = # qualifying lakes), and MCC** alongside the onset/overfit columns. EPA's
  AUC_within=0.498 is flagged **descriptive/unstable** (only 64/132 lakes qualify; per-lake AUCs 0–1),
  not a hard contradiction of its 0.931 pooled AUC (Codex).
- **D-38d — Part-2 block ablation, Codex-reconciled.** CyAN is the dominant block (drop → AUC_within
  0.89→0.69, overfit gap ~5×) — **survives**. "Weather net-negative" **downgraded** to "neutral / no
  detectable benefit" (tiny single-arch/seed deltas; Codex). clim trades ranking for onset-calibration
  — survives. `valAUC-testAUC` relabeled an **in-sample-val optimism gap** (val is in-sample for the
  train+val refit), *not* a clean generalization gap. This motivated the **Part-3 feature-level (greedy
  backward) ablation** (`exp_feature_ablation.py`) — drop individual features while val-AUC stays within
  0.001 of the full model, then confirm the lean set on held-out test across archs with a lake-block
  bootstrap. (Running.)

## 2026-07-05 — Change-feature exp + onset-metric CORRECTION (D-37, Codex-reconciled)

- **D-37 — The "onsets are unpredictable" conclusion was a METRIC ARTIFACT; corrected.** Codex's Exp-1
  review flagged: (a) my weather "change" features were **redundant** (linear combos of columns already
  in DRIVERS), so they couldn't test the hypothesis; (b) **flip_MCC conflates onsets & offsets** and
  MCC-at-threshold hides ranking skill. Reconciled in `experiment_lib.py`:
  - **Non-redundant CHANGE features** — non-overlapping recent-vs-prior weather trends + **anomalies vs
    train seasonal climatology** (genuinely new info, train-only/leakage-safe).
  - **Onset/offset decomposition** — `onsetAUC/onsetMCC` on the currently-CLEAR subset (pers=0 → bloom
    next = the EARLY-WARNING skill); offset on pers=1. Plus combined flipMCC per horizon.
  - EPA row: **fixed 0.5 threshold** (not test-tuned); harness reverted to the standard **train+val
    refit** (D-35b/user); dead code removed.
  - **CORRECTED RESULT (`exp_change_features.md`):** onsets ARE rankable — **onsetAUC h1: fusion_full
    0.935, fusion_full+clim 0.93–0.94, fusion_nocyan+clim ~0.89, climatology 0.851, EPA 0.831,
    persistence 0.50.** **Fusion beats climatology AND EPA on early-warning** (onsetMCC: fusion_full+clim
    0.466 vs climatology 0.323 vs EPA 0.233). **CyAN sub-threshold value helps rank onsets**
    (fusion_full 0.935 > nocyan 0.90). **Weather CHANGE features still add ~nothing** even non-redundant
    (onsetAUC flat ±0.005 with/without) — that negative now holds. nocyan overfits more (valAUC-testAUC
    ~0.04 vs ~0.01) → motivates the Part-2 ablation.

## 2026-07-05 — Experiment-suite framework: split, architectures, standard tracks (D-36)

- **D-36a — Split widened to ~60/20/20, 2-YEAR test** (user; 1-yr test too few): date-based **train
  <2022-07-01 / val [2022-07, 2024-07) / test >=2024-07** (2 yr, covers EPA's 2025–2026 window).
  Replaces the year-based train≤2023/val2024/test2025.
- **D-36b — Architecture suite = regularized logistic + HistGBM + XGBoost** (user added XGBoost; v3.3.0
  installed). Logistic = the genuinely-different linear/explainable comparator (impute+scale+missingness
  indicator → *disadvantaged on sparse in-situ*, reported honestly); HistGBM & XGBoost = GBDTs w/ native
  NaN (XGBoost ~ robustness check on HistGBM, same family). Protocol: fit train (early stop where avail),
  threshold on VAL, refit train+val, score TEST.
- **D-36c — Standard experiment suites (always report the feature-combo × architecture GRID):**
  baselines (persistence, climatology) + **cyan_ladder** + **fusion_full** (CyAN+static+season+weather+
  in-situ) + **fusion_nocyan** (static+season+weather+in-situ = the **anti-persistence model**, drops
  antecedent CyAN levels to free the model for onsets — user idea, D-35 follow-on). Run this suite for
  every experiment unless one explicitly trials a new feature set. `eval_experiments.py` →
  `outputs/experiments.md`. Grid pre-specified (no result-shopping); large grid run in background,
  output kept digestible (suite×arch matrix + horizon curve).

## 2026-07-05 — Climatology demoted to baseline; validate on held-out TIME only (D-35)

- **D-35a — Per-lake climatology is DEMOTED to a BASELINE, not a model feature** (user). Rationale
  (2-subagent audit): neither we nor EPA use *discrete* lake identity, but our fitted ladder carried a
  per-lake per-month climatology (`clim`) = a learned per-lake base rate (identity-by-proxy) that **EPA
  does not use** (EPA = generalizing SPDE spatial field + morphology). Dropping it from the model both
  matches EPA's feature philosophy and honors the generalizability preference (avoids memorizing lakes
  with short per-lake records). Fusion **Track A** = generalizable (CyAN ladder + static morphology +
  general week-of-year seasonality + weather + in-situ; NO clim, NO lake ID/lat-lon); **Track B** = +clim
  (contrast only). Climatology + persistence + CyAN-ladder are the baselines.
- **D-35b — Validation = held-out TIME only (match EPA), leave-lakes-out DROPPED** (user correction).
  EPA (Schaeffer) validated on a held-out YEAR with all lakes in training (SPDE covers all locations);
  no held-out lakes. So for an apples-to-apples head-to-head we use the temporal split (test 2025) only.
  *Noted tradeoff:* without a blocked-lake test we cannot *empirically* show the generalization benefit
  of dropping climatology — so demoting it is a **principled, EPA-aligned choice**, not empirically
  forced. Leave-lakes-out kept as a deferred *secondary* diagnostic (not part of the EPA comparison).
- **Fusion eval (`eval_fusion.py` → `outputs/fusion_eval.md`, HistGBM, test 2025) — Codex-reconciled &
  FINALIZED.** Fixes folded in: val-threshold + early stopping, **paired within-lake delta + lake-block
  CI** (not difference-of-medians), **block ablation + permutation importance**, h=0–4 curve, honest
  language (same-lake temporal only; not unseen-lake generalization). **Honest verdict:** fusion beats
  the CyAN ladder by a **tiny, real** margin (paired within-lake **+0.015 [+0.003, +0.021]**, 67% of
  lakes) but is **overwhelmingly CyAN autoregression** (perm importance: CYAN +0.27 vs weather/in-situ/
  static ~0.002–0.005 each; removing weather/in-situ barely moves AUC). **Still anti-predictive on
  flips** (flip_MCC h1 −0.49; ladder −0.68; **only climatology is positive, +0.05**) — though fusion's
  flip anti-predictivity **shrinks with horizon** (−0.65 h0 → −0.29 h3/4 as CyAN goes stale). Fusion
  polishes easy next-state ranking; has NOT solved onset/offset. → motivates the anti-persistence series.

## 2026-07-03 — In-situ screen: Codex-reconciled + chl-a lead-vs-persistence test (D-34)

- **D-34 — In-situ temporal screen reconciled (Codex + user).** Codex reviewed the NWIS/WQP screen
  engine (no blocker beyond chl-a; user's insight refined it). Fixes folded into
  `screen_insitu_features.py`:
  - **Variable CLASS** — `driver` vs **`consequence`** (turbidity/Secchi/DO/microcystin: bloom raises
    turbidity/DO, lowers Secchi — impacts, not causes) vs **`circular`** (WQP `chl_a`: our AL1 target
    is chl-a-defined). Consequence/circular flagged; excluded from driver/forecast claims.
  - **chl-a lead test (user's question) — `chla_leadlag.md`:** conditioning on **CyAN-clear at the
    cutoff**, antecedent WQP chl-a predicts a CyAN bloom h weeks later at **AUC_within ≈ 0.63→0.59
    (h=1→4)** — **real independent LEAD, not circularity** (the user was right). BUT CyAN's own
    sub-threshold median leads *better* (0.82→0.70). So lagged chl-a is a genuine but **modest**
    in-situ early-warning signal whose value is *independence* (catches sub-pixel/nearshore onset),
    not raw lead; coincident chl-a stays redundant.
  - **TIMING** — antecedent (`lag1/2/4`, forecast-eligible) vs `same_week` (coincident + through-W
    aggregates: DIAGNOSTIC association only, not forecast skill).
  - **Two significance gates** — pooled lake-block bootstrap AUC (`incl_assoc`) **AND a within-lake
    bootstrap of the median per-lake AUC** (`incl_within`): the honest temporal test. Catches
    within-only signals the pooled test misses (Codex: TP `lag4` within-p≈0.06) and demotes
    datum/size between-lake artifacts (NWIS gage height).
  - **Fixes:** `anomR` baseline PAST-only (excludes W); `anomC` leave-one-out per-lake-month
    climatology; `sum4` only for FLUX vars (discharge) — a concentration rolling-sum is a
    sampling-frequency artifact.
  - **Significance tests documented (`docs/04` §Significance tests):** static = Spearman ρ + p +
    BH-FDR (per-lake); temporal = **cluster-robust (lake-block bootstrap) Mann–Whitney/AUC** test,
    pooled + within-lake, two-sided vs 0.5 + BH-FDR. **Horizon h=0–4 encoded via feature lags**
    (coin≈h0, lag1/2/4≈h1/2/4; h3 not built; aggregates are multi-week) — **accepted as sufficient for
    this initial round (user, 2026-07-03)**; an explicit per-horizon sweep is deferred to modeling.
  - **Documented limitations (not fully fixed — screen-stage):** WQP values **not unit/fraction-
    harmonized** (mixes total/dissolved P, chl-a methods) → nutrient signals indicative only; **TN/pH
    grossly undercounted** (characteristic-name misses → need alias/pCode discovery); a few sites in
    >1 lake buffer (kept first, ≤12); direct tier suppresses watershed; WQP chl-a ~monthly (sparse).

## 2026-07-02 — Feature significance screening: methodology + static layer (D-33)

- **D-33 — Feature-vs-HAB significance screening.** Goal: find features with a statistically defensible
  association with bloom, as candidates for the fusion model.
  - **Linkage hierarchy (NWIS/WQP → lakes; user):** (1) DIRECT = monitoring point in the lake polygon
    **+250 m buffer**; else (2) WATERSHED = median of stations in the **containing BasinATLAS L12**
    only; else (3) NULL. Prereq built: `join_basinatlas_l12.py` → `lake_basinatlas_l12.parquet`
    (**max-overlap** L12 assignment per Codex — handles split-basin/coastal lakes; **133/133** matched,
    94 sub-basins, 46 lakes span >1 L12).
  - **STATIC test (area + 32 L12 attrs):** unit = **LAKE** (n=132), not lake-week (avoids
    pseudoreplication); Spearman(feature, per-lake bloom prevalence). **Inclusion screen = raw p<0.1**
    (user; permissive — pick candidates, narrow to top-N later), with **BH-FDR q reported** for honesty
    (`*` = survives q<0.05). `assess_static_features.py` → `outputs/feature_significance_static.md`.
  - **Result (honest, weak; Codex-reconciled):** **13/33 pass p<0.1**, but only **1 survives FDR**
    (`inu_pc_umn` inundation, ρ=+0.351). **Area** ρ=+0.226, p=0.009 (included), q=0.068 (fails FDR).
    (Codex fix: max-overlap join dropped 2 marginal features, 15→13.) Directions all
    sensible (anthropogenic/warmth/PET +, forest/moisture −) but effect sizes small — between-lake
    landscape gradients are compressed (all FL lakes ~eutrophic); the forecasting signal is in
    **within-lake temporal dynamics**, motivating the NWIS/WQP/weather temporal features.
  - **Depth: skipped** (no per-lake source on disk; HydroLAKES needed — deferred by user).
  - **TEMPORAL in-situ test (NWIS/WQP):** representations per variable = coincident, lag1/2/4, recent
    mean+sum (4/12wk), delta(W−W4), anomaly-vs-recent (`anomR`), anomaly-vs-climatology (`anomC`).
    Test = **lake-block bootstrap univariate AUC** (`AUC_pool`, resample lakes) **+ within-lake median
    AUC** (`AUC_within`). **Critical:** `AUC_pool` conflates between/within-lake; datum-relative (gage
    height) & size-scaling (discharge) absolute values are not cross-lake comparable, so a strong
    `AUC_pool` can be a between-lake artifact (tell: every rep gives ~same AUC) — **`AUC_within` is the
    honest temporal test**. `screen_insitu_features.py` (source-agnostic).
  - **NWIS result:** coverage **25/133** lakes (many FL lakes are seepage/closed-basin, ungauged).
    **Water-temperature** = genuine within-lake signal (`AUC_within` ~0.78; warmer-than-normal
    anomalies ~0.65). **Gage-height** real inverse within-lake (~0.30; pooled datum-inflated to ~0.10).
    **Discharge weak** (~0.41, fails robust bootstrap). → `outputs/feature_significance_nwis.md`.
  - **WQP pull:** station-first (statecode US:12 `Station` list → spatial filter → results by siteid
    chunk; bBox 500s, statewide result queries time out). Same screen engine.

## 2026-07-02 — EPA forecast head-to-head + seasonal documentation (D-32)

- **D-32 — EPA head-to-head, honestly framed; no "beat EPA" claim.** `eval_epa_headtohead.py` scores
  EPA's 7-day cyanoHAB forecast, our ladder, persistence, climatology as predictors of **our AL1** on
  shared FL 2025 COMID-weeks (exact join: EPA `WeekEndDate`=our `end_date`, COMID identical, 132/132).
  Result: EPA AUC-ROC 0.928 / Brier 0.101 **does not clearly beat persistence** (week-block bootstrap
  ΔAUC +0.010, 95% CI [−0.000, +0.022]). **Three material caveats documented in-output:**
  1. **Structural advantage to us** — persistence/climatology/ladder are all our-AL1-derived; EPA
     predicts its own chl-a/dominance threshold (cutoff unstated) scored on ours → gap is partly
     definition mismatch. A fair EPA eval needs EPA's own definition (follow-up).
  2. **Seasonal window (user-requested)** — EPA is ~Apr–Nov only → shared set = **35/52 weeks**,
     peak-bloom, base rate **28.8% vs 26.6% full-year**; all metrics seasonal-only, NOT comparable to
     `cyan_baseline_eval.md`. Quantified: our baselines' AUC ≈ unchanged seasonal-vs-full (FL is
     near-aseasonal), the shift is mainly base-rate → affects threshold-dependent metrics.
  3. **Threshold-free first** — EPA has no held-out year to tune a threshold; operating-point uses
     in-sample thresholds (optimistic, even-handed).
  - Rigor added: **week-block bootstrap 95% CIs** (resample the 35 weeks) to prevent the limited,
    autocorrelated record from masquerading as precision. Reflected in `DESIGN.md` §8.
  - **Codex-reconciled (round 2):** (a) **provenance** — labeled EPA values a *2026-07-02 dashboard
    snapshot, not proven as-issued* (revisable view, one snapshot); (b) **corrected the caveat-1
    framing** — our AL1 is the SAME Schaeffer/WHO concept EPA forecasts (not a different threshold); the
    advantage is that our models are fit to our *exact realized labels*; Brier gap is *descriptive*
    (mean prob 0.246 vs base 0.288), not a proven definition mismatch; (c) **timing** — EPA is a
    current-week forecast (Tue/Wed release), W−1/W−2 is our CyAN-latency sensitivity; (d) seasonal
    comparison now uses **exact shared COMID-weeks**; (e) removed dead val-tuned threshold code.
  - **Flips comparison added (user request):** on transition weeks (target≠persistence) the ordering
    **inverts** — climatology AUC 0.551 > EPA 0.455 > our CyAN-only ladder 0.118 (anti-predictive) >
    persistence 0.000. **The fusion mandate:** CyAN-only dominates aggregate only via persistence-easy
    weeks; on onsets it is useless-to-harmful, EPA's weather/morphology fusion helps, and **our fusion
    features must beat climatology on flips** to earn their place.

## 2026-07-02 — Climatology as explicit comparator + overclaim correction (D-31)

- **D-31 — Climatology reported as a first-class comparator in the all-samples case** (pairwise
  MCC/AUC-ROC/Brier deltas: ladder−persistence, ladder−climatology, climatology−persistence; +
  MCC-by-horizon table). Codex round-3 **verified the deltas/arithmetic and caught an interpretation
  overclaim** (no code bug): I had written climatology is the "best AUC-ROC baseline" and framed the
  best baseline as "climatology on AUC-ROC, ladder on MCC/Brier." **False** — the **ladder** has the
  best AUC-ROC at every horizon (h0 0.986 > climatology 0.955 > persistence 0.941). Corrected: the
  ladder is the strongest CyAN-only baseline on nearly every metric (ties persistence on h0 MCC);
  climatology is a strong *ranker* (beats persistence on AUC-ROC, widening as persistence decays) but a
  weak *classifier* (lowest MCC ≈ 0.75) — never the single best baseline. Also added **Brier deltas**
  (lower-better sign convention). Corrected in `eval_cyan_baselines.py`, `outputs/cyan_baseline_eval.md`,
  DESIGN §8, PROGRESS. Fidelity note: reported-as-they-are, own error surfaced.

## 2026-07-02 — Codex review of assembler + baselines incorporated (D-30)

Codex independently **recomputed the numbers from the parquet and confirmed them** (339,400 rows, base
rate 26.57%, ladder AUC 0.987→0.973, latency guard holds); no BLOCKING. Fixes:

- **D-30a — Wide metric suite** for ALL experiments (`model/metrics.py`): AUC-ROC, AUC-PR, Brier, MCC,
  F1, Prec, Recall, Acc. **MCC** is the headline balanced metric; AUC-ROC read with the hard-vs-soft
  caveat (a hard 0/1 has capped AUC). DESIGN §8.
- **D-30b — Persistence = last-valid carry-forward (H2/M2), not fill-0.** `bloom_state_ffill` added to
  the feature block; cloudy freshest weeks carry the last OBSERVED bloom (10,368 rows flagged
  `persistence_from_cloudy_cutoff`); only ~75 record-start rows remain null (dropped in eval).
- **D-30c — Threshold tuned on VALIDATION, not in-sample (M1).** Prob models fit on train, threshold
  tuned on val (2024), refit on train+val, scored on test (2025) with the frozen threshold.
- **D-30d — Transition-week evaluation added (M3/L5)** — the honest headline: on flips the CyAN-only
  ladder is **anti-predictive** (AUC-ROC < 0.5, MCC negative all horizons); climatology is the only
  weakly-positive CyAN flip signal. **Fusion's real bar = transition-week skill + lift over ladder AND
  climatology**, not aggregate AUC.
- **D-30e — Interpretation corrected (M3):** absolute skill is dominated by **per-lake seasonal
  identity** (climatology 0.955), not autocorrelation alone.
- **D-30f — Issue-time doc honesty (H1):** assembler uses the **weekly algebraic** `target−7·(h+1)`
  form (= publish-time cutoff under fixed 1-wk latency); general publish-time join deferred to EPA/daily.
- **D-30g — Climatology = per-lake calendar-MONTH** (docs said week-of-year; month is more stable, M4).
  Also computed from **unique (comid, target_date)** rows (L4).
- **D-30h — Robustness:** eval re-asserts the latency guard at load (L2); `assert`→`raise` (L3);
  metrics NaN guard (L1); output md is plain ASCII (M5).

## 2026-07-02 — Codex review of baseline/feature updates incorporated (D-29)

Codex reviewed the D-27/D-28 updates + built artifacts (no BLOCKING). Fixes folded in:

- **D-29a — Coverage sensitivity, not a silent threshold (H3).** Primary target keeps **Schaeffer
  parity** (valid = ≥1 clear pixel, all-cloud → missing); added **`valid_frac`** column + a **coverage
  sensitivity** (low-coverage weeks `valid_frac<0.5` are ~8–9% of rows and bias prevalence low, ~7% vs
  ~25%). Docs that implied a hard ≥50% threshold corrected (`docs/03` §3, DESIGN §4).
- **D-29b — Parity SD (M1):** `cyan_sd` → **sample SD (`ddof=1`)**, NaN for single-pixel weeks (matches
  R `sd()`). Target rebuilt.
- **D-29c — Explicit issue-time / publish-time cutoff (H1)** and **EPA info-set fairness (H2):**
  persistence via `max(week k: publish(k) ≤ issue)`, not bare algebra; EPA scored on **its own** cutoff
  (publish ≤ Tue/Wed release) with **W−1/W−2 sensitivity**. `docs/02` §1, DESIGN §8.
- **D-29d — Feature-column honesty:** `staleness_weeks` → **`cyan_gap_weeks_at_cutoff`** (cutoff-, not
  target-relative; M3); **`bloom_roll4_n`** exposes the roll denominator (M4); retained
  **`n_inside`/`valid_frac`** (L2).
- **D-29e — AR(1) reported pooled AND within-lake (M6):** pooled 0.903 is inflated by between-lake
  baseline spread; report demeaned within-lake + median per-lake AR too.
- **D-29f — `coverage_fraction==1` = close 8× approximation, not exactextract (M2):** docs corrected;
  exactextract cross-validation = QA follow-up.
- **D-29g — h=0 is retrospective diagnostic ONLY, excluded from operational forecast claims (M5).**
- **D-29h — Lake-area claim softened to hypothesis-generating (M7):** confound + no-extrapolation-
  below-support caveats (D-27 amended in DESIGN §3).
- **D-29i — Assembler leakage tests REQUIRED (H4):** enforce `feature_week == target − 7·(h+1)` per
  horizon + persist the resolved cutoff week (`docs/02` §3).

## 2026-07-02 — Latency-aware persistence is the primary baseline (D-28)

- **D-28 — Persistence is THE primary reference baseline, and it is latency-aware; both our model AND
  the EPA forecast are scored as skill relative to it.** Persistence carries forward the AL1 bloom state
  of the **freshest CyAN composite actually published by issue time**. CyAN weekly composites post
  ~COB the Monday after the 7-day window closes → **~1-week publication latency** (verified,
  cyan/METADATA §13). So the freshest *available* composite for a horizon-`h` forecast of week `W` is
  week **`W − h − 1`** (nominal lead **+ 1 week latency**), NOT the idealized `W−h`:
  **`Persistence(W,h) = bloom(W − h − 1)`**. *Rationale (user):* persist from the *oldest-freshest
  actually-possible* CyAN — never over-credit availability. **Consequences:** (1) the model's CyAN
  features use the **same** `W−h−1` freshest week (docs/02 matrix updated) so it never sees fresher
  CyAN than the baseline; (2) latency cleanly separates h=0 (freshest `W−1`) from h=1 (`W−2`); (3) the
  common yardstick for **our model and EPA** is "who beats latency-aware persistence by more, and at
  what lead." Daily products would cut latency to ~2 days (tunable). Reflected in `DESIGN.md` §8 +
  `docs/02` §1–3. No feature-parquet rebuild needed (lags already present; horizon→lag mapping applies
  the +1 at assembly time).

## 2026-07-02 — Lake area elevated to a headline feature (D-27)

- **D-27 — Lake surface area is a first-class, prominently-reported feature + strategic diagnostic.**
  Area (`AREASQKM`, static, already in the FL mask + target table) stays in the EPA-parity set, but we
  **report its importance + partial-dependence in every model** (not buried in a morphology bundle) and
  test it **non-linearly** (small- vs large-lake regimes). *Rationale (user):* area's utility is itself
  a finding — a strong area effect **quantifies the value of resolving smaller waterbodies**, and since
  CyAN only resolves lakes ≥ ~900 m, that is the evidence base for a **future-work extension of this
  same workflow to sub-300 m / sub-resolvable waterbodies** (SePRO's core customers; cyan/METADATA §5).
  Reflected in `DESIGN.md` §1 (future-work), §3 (feature), §8 (headline diagnostic).
- **⚠️ WALKED BACK 2026-07-06 (see D-39d):** clustered permutation importance shows `area_sqkm` is a
  *whisper* (Δ onsetMCC ~+0.018, Δ pooled ~0; not cross-arch robust; not FDR-significant). The
  "headline/first-class feature" framing was domain-reasoned, not empirically supported — report area as
  a minor/context feature. The *future-work* rationale (resolving sub-300 m waterbodies is valuable to
  SePRO) still stands as motivation; what changes is that area is **not** an empirically strong driver
  in *this* model, so we don't headline it as one.

## 2026-07-02 — Codex v3 (pivot) review incorporated

Codex reviewed the pivoted v3 design; sound fixes folded into `DESIGN.md`. The headline concern was
**circularity** (the target is a threshold on the same CyAN product fed as features).

- **D-26a — CyAN autoregressive-ladder baseline + CyAN features antecedent-only.** Build a CyAN-only
  ladder (prior bloom state, lag-1/2/4 median CI, climatology); report every fusion feature as
  **incremental lift over the ladder** before any importance claim. CyAN features never include the
  target week (kills the tautology, esp. at h=0).
- **D-26b — AL1 threshold PINNED (resolved 2026-07-02): per-lake weekly median CyAN DN ≥ 130** (≡ 12
  µg/L chl-a, WHO AL1) — authoritative from Schaeffer `cyan_processing_conus.R:170` (sensitivity DN
  97/151). We claim WHO-AL1-equivalent, noting CI↔chl-a scatter. Aggregation = mean/median/SD over
  pixels fully inside the lake polygon (`coverage_fraction==1`). See `docs/03-target-definition.md`.
- **D-26c — Two feature tracks:** *EPA-parity* (only track for head-to-head claims) vs *augmented
  SePRO* (extension).
- **D-26d — Benchmark fairness:** compare EPA head-to-head on **shared FL COMID-weeks where both
  exist** (recent-window overlap), not their paper's CONUS 2017–2021 numbers (context only).
- **D-26e — Secondary blocked-lake stress test** for per-lake memorization; primary claim narrowed to
  **"known-lake forecasting"** (no transfer-to-new-lakes wording); **antecedent-weather-only ablation**
  alongside oracle runs.
- **D-26f — Concrete lake-week QA policy:** min valid pixels/fraction, mixed/edge mask, missing (not
  imputed) below threshold, QA fields + missingness sensitivity; per-horizon **PR-AUC / precision@recall
  / calibration / event-count CIs**; pin the **week convention** (CyAN first-Sunday / EPA Saturday) in
  the feature-availability matrix before coding.

**Pre-build pins:** (1) ✅ AL1 threshold = median DN ≥ 130 (D-26b, `docs/03`); (2) ✅ FL lake list =
**133 lakes** from CyAN `updatedValidLakes.shp` → `data/derived/fl_resolvable_lakes.gpkg`
(`build_fl_lake_mask.py`); (3) ✅ lake-week QA policy (`docs/03` §3); (4) ⏳ feature-availability matrix
/ temporal protocol (`docs/02`) — needed before *feature* assembly, not before target aggregation.

## 2026-07-02 — PIVOT: match the EPA/Schaeffer forecast (lake-level, temporal split, WHO AL1)

After reviewing the EPA experimental CyanoHAB forecast (`../data-sources/cyano-forecasts/`,
Schaeffer et al. 2024 INLA) — the closest federal benchmark to our task — the user directed us to
**fully match their methods where possible**. This supersedes several earlier decisions.

- **D-23 — Lake-level analysis unit (matches EPA); supersedes D-22 (native pixel).** Aggregate CyAN to
  **per-lake weekly mean / median / SD** over the CyAN **resolvable-lakes** footprints (Schaeffer's
  `cyan_processing_conus.R` recipe; mixed pixels masked). Mask = the CyAN resolvable-lakes set filtered
  to Florida (COMID-keyed). Keep raw pixels for QA/diagnostics only. **This is the explicit aggregation
  sign-off** the standing no-aggregation rule requires. *Rationale (user):* comparability to the
  federal baseline + identity joins to WQP/NARS/NWIS/LakeCat via COMID. NOT a compute decision (pixel
  was feasible; lake is *better* for the product claim).
- **D-24 — Temporal (held-out-year) split; supersedes D-20 / Q-6 (spatial-only).** Match Schaeffer:
  train on earlier OLCI years, evaluate on an **independent held-out recent year** (their scheme:
  70/30 within 2017–2020 + independent 2021 test; classification cutoff 0.10). Forward-chaining
  option. Leakage guard shifts to **temporal look-ahead primary**; cross-lake spatial autocorrelation
  is carried by per-lake static features + lagged per-lake CI (as EPA carries it via SPDE/AR1), not by
  spatial blocking.
- **D-25 — Target = WHO Alert Level 1 (binary); supersedes D-10 (continuous CI) and resolves Q-3.**
  Bloom = **lake-wide weekly median surface chlorophyll-a ≥ 12 µg/L with cyanobacteria dominance**
  (WHO AL1), binary presence/absence, evaluated over the resolvable area. Models predict **P(bloom)**;
  base rate ~9–10% (imbalanced). The exact CI↔chl-a/AL1 mapping (CyAN CI → 12 µg/L chl-a-equivalent)
  is pinned in `docs/03` from the CyAN docs + Schaeffer code — a documented approximation with scatter,
  stated as a limitation. Continuous per-lake median CI may be kept as a *secondary/diagnostic*
  regression target.

**Consequences:** models become **classifiers** (logistic GLM · SVC · XGBoost · logistic GAM), all now
feasible at full scale (N ≈ FL lakes × weeks ≈ tens of thousands → **no subsampling** needed). Metrics
become classification-first (AUC, precision/recall/F1/specificity/Brier — matching their reported
table) so we can benchmark head-to-head at h=1 (their 7-day horizon). We still use **ERA5** (not
PRISM) and add **WQP/NWIS in-situ** as a superset of their predictors; **OLCI-only** (D-21) still
holds; the **oracle-weather** idealization (D-11) still holds. **Ice-mask step is skipped** (no ice in
Florida). See `DESIGN.md` v3.

## 2026-07-02 — Compute gate measured & resolved (Q-5)

- **D-22 — Native 300 m pixel-week is viable; no lake-aggregation fallback.** Measured the FL
  inland-water CyAN footprint from the local OLCI mosaics
  ([`acquire/compute_gate_estimate.py`](acquire/compute_gate_estimate.py), see
  [`docs/01-domain-and-data.md`](docs/01-domain-and-data.md)): **≈128,628 water pixels ≈11,577 km²**
  (matches FL's real ~12,000 km² surface water — clip validated), **≈68.3 M pixel-week rows** over 531
  OLCI weeks. Dense monolith ≈27.3 GB = **unsafe** on 16–32 GB (and the sampled union undercounts), so
  **partitioned columnar storage (Parquet/DuckDB/Polars)** is mandated; native-pixel then fits. GLM &
  XGBoost scale; **RBF-SVM & GAM run on a documented stratified subsample**. Resolves Q-5; the
  lake-aggregation fallback (D-03) is **not** triggered. *A raw lat/lon box (no FL clip) reads ~1.46 M
  "valid" px by sweeping in shallow marine water CyAN also processes — hence the FL-polygon clip is
  mandatory (marine is not our freshwater-HAB target).*

## 2026-07-02 — Validation & sensor scope resolved (Q-6, Q-7)

- **D-20 — Spatial-only split (Q-6).** Split on **space only** (blocked); no temporal holdout, per
  user. *Consequence (documented as a limitation):* Task-B measures **spatial transfer to unseen water
  bodies**, not forecasting into unseen future time — reported skill is an upper bound on operational
  forecast skill. Temporal/forward-chaining holdout = future work.
- **D-21 — OLCI only, MERIS dropped (Q-7).** Model **OLCI (2016-04-24→present) only**; exclude MERIS
  (2008–2012) entirely. *Rationale:* CI not comparable across the sensor/version boundary [`FED-066`];
  removes cross-sensor bookkeeping and the version-straddle leakage risk by construction. Drops the
  sensor-era stratification from diagnostics; supersedes D-09's "restrict-or-indicate" framing.

## 2026-07-02 — Codex methodological review incorporated (DESIGN v2)

Codex reviewed the plan (adversarial pass over `models/` + `CLAUDE.md` + data metadata). Sound fixes
folded into `DESIGN.md` v2; two items that touch prior user decisions were escalated to
`OPEN-QUESTIONS.md` (Q-6, Q-7) rather than applied unilaterally. Accepted decisions:

- **D-11 — Task B is an oracle-weather / potential-predictability experiment, labeled as such.** The
  perfect-weather idealization (user's choice) is kept, but results are reported as an
  **oracle-weather upper bound**, never as operational "two-weeks-early" skill. Operational
  (issue-time-only weather) protocol = future work. *Rationale:* coincident ERA5 is unavailable at
  real issue time; mislabeling would breach the claim gate.
- **D-12 — Persistence baseline = most recent CyAN composite available at the issue date** (carried to
  t+h), for all horizons incl. h=0. *Rationale:* "CI(t)=target" is tautological at h=0 and hides
  leakage. Forces an explicit **issue-time / feature-cutoff** definition (features must end before the
  7-day target composite window begins).
- **D-13 — Outcome-driven feature-selection tests run on TRAIN folds only; feature set frozen before
  held-out evaluation.** Literature-precedent inclusion is outcome-blind and exempt. *Rationale:*
  prevents test-label leakage into the feature set.
- **D-14 — Uncertainty via clustered (spatial-block) bootstrap / fold-level CIs; never row-level
  bootstrap or ordinary CV spread.** *Rationale:* pixel-weeks are autocorrelated; row resampling
  understates uncertainty. Hyperparameter tuning is **nested** (inner CV on train; one final pass on
  frozen test).
- **D-15 — chl-a is an ablation group** (skill reported with/without; barred from early-warning claims
  absent proven pre-target availability). *Rationale:* chl-a is a biomass proxy → near-circular skill.
- **D-16 — Language + reporting discipline:** call CyAN the **reference/satellite-derived target**, not
  "ground truth" (Stage-2 preliminary product); **blocked results first** in every table; random split
  **watermarked "leakage diagnostic."**
- **D-17 — Compute gate evaluated at the FUSION stage** (not download; CyAN already local) with explicit
  thresholds (rows/RAM/disk/wall-time/per-model limits); columnar partitioned storage
  (Parquet/DuckDB/Polars); **RBF-SVM & GAM run on documented subsamples at pixel scale** (they don't
  scale). Lake-aggregation fallback still gated on explicit sign-off + a new design section.
- **D-18 — Predeclared target QA/masking policy** (DESIGN §4): DN 0 = censored non-detect, mask
  254/255, exclude/stratify <~900 m + shoreline pixels, single processing version, **threshold =
  CI-exceedance not toxin risk**.
- **D-19 — New required artifacts:** per-horizon **feature-availability matrix**, **derived-row
  provenance** columns/manifests, **in-situ join hierarchy** (same-waterbody → NLDI topology → HUC12 →
  distance fallback + sensitivity), **WQP reconciliation** (WQX2/3 dedup, units, censoring, drop
  NARS-in-WQP), **calibrated prediction intervals** + coverage eval, and **stratified skill
  diagnostics** (era/season/size/staleness/cloud/join-distance).

## 2026-07-02 — Scope, target, unit, split, and models fixed (from user Q&A)

Five load-bearing decisions, set by the user after a clarifying-questions round.

**D-01 — Two-mode target framing.**
- *Feature assessment (Task A):* evaluate feature relationships **coincidentally (nowcast, zero
  lag)** — does a candidate feature relate to *same-week* `CI_cyano`?
- *ML models (Task B):* **multi-horizon forecast** at h ∈ {0, 1, 2, 3, 4} weeks, under a
  **perfect-weather idealization** — always use *coincident* ERA5 weather for the target week; defer
  the uncertainty from real ECMWF forecasts to future work.
- *Rationale:* isolates predictive structure (water state + weather + basin → bloom) from
  weather-forecast quality; supports the brief's "two weeks early" thesis and a skill-vs-lead-time
  curve. Literature does not expect skill beyond ~2 wk [`ACAD-092`] — reporting the decay is honest.

**D-02 — Every temporal feature carries (value + staleness).**
- For streamflow, each water-quality analyte, and the lagged CI target, the model sees both the last
  observed **value** and its **staleness** (days old).
- *Rationale:* lets the model weight stale inputs appropriately and handles irregular/sparse in-situ
  sampling **without interpolation** (which would fabricate observations and risk look-ahead).

**D-03 — Analysis unit = native 300 m CyAN pixel × week (primary); resolvable-lake aggregation is a
gated fallback.**
- Try 300 m pixels first. If compute is infeasible on local hardware, fall back to per-lake
  aggregation — but only with **explicit user sign-off**, since aggregating CyAN pixels is exactly
  the kind of aggregation the standing rule forbids by default.
- *Rationale:* honors no-aggregation default and preserves target resolution; keeps a documented,
  reversible escape hatch for compute.

**D-04 — Spatially-blocked split is PRIMARY; random split is a reported optimistic reference.**
- **Supersedes** the originally-specified "random 60/20/20 on space."
- Assign whole spatial blocks (buffered) to train/val/test ~60/20/20; also run the random split and
  report the random-vs-blocked skill **gap** as a leakage measurement.
- *Rationale:* nearby pixels are spatially autocorrelated; a random split leaks and inflates skill
  [`ACAD-141`, `ACAD-048`]. Blocked split = genuine spatial-generalization test.

**D-05 — Drop the CNN; use four tabular models: GLM, SVM, XGBoost, + GAM.**
- 4th model = **GAM** (**confirmed by user 2026-07-02**) — a distinct, highly interpretable additive
  family (smooth partial-dependence curves) complementing linear GLM, kernel SVM, and boosted
  XGBoost. Random Forest was the faster alternative; not chosen (overlaps XGBoost as a tree ensemble).
- *Rationale:* all-tabular keeps one shared data representation and maximizes explainability (brief
  favors well-validated simple models over opaque complex ones). CNN's spatial-patch pipeline was a
  large lift for uncertain gain given the tabular fusion.

## 2026-07-02 — Domain fixed: State of Florida

**D-06 — Physical domain = State of Florida; requires a fresh, FL-clipped download of all sources.**
- *Rationale:* user-selected. Florida has strong CyAN relevance (Lake Okeechobee + many resolvable
  lakes) and a published Bayesian analog to benchmark framing against [`ACAD-092`]. Regional (not
  global) model is an explicit scope bound.

## 2026-07-02 — Mandatory reporting standards adopted from the research pack

**D-07 — Persistence baseline is mandatory at every horizon.**
- Week-to-week CI autocorrelation is ~0.90 [`ACAD-092`]; leading fusion studies omitted a persistence
  baseline [`ACAD-092`, `ACAD-050`]. We report skill relative to persistence **and** climatology,
  always with uncertainty. A model that doesn't beat persistence is a reported (negative) result.

**D-08 — Report event-based (threshold-exceedance) skill, not just RMSE/R².**
- *Rationale:* R²/RMSE alone can mask poor operational-hazard skill [`ACAD-110`]. We report
  precision/recall/AUC/CSI at a documented bloom threshold per horizon.

**D-09 — Verify CyAN processing-version homogeneity before modeling.**
- *Rationale:* NASA prohibits trending CI across processing versions (V4→V5 shifted 15–20%
  [`FED-066`]); our POR straddles MERIS/OLCI eras. Restrict to a consistent era or add a sensor/era
  indicator; document the check.

## 2026-07-02 — Target type confirmed

**D-10 — Model continuous `CI_cyano` (regression, log scale); derive the bloom-exceedance evaluation
from it at a documented threshold.** **Confirmed by user 2026-07-02** (was working decision W-01).
Gives both a rich continuous signal and event-based (threshold) skill, rather than committing to a
pure binary classifier up front.

---

### Assumptions register (revisit if invalidated)

- **A-1:** CyAN resolves enough Florida lakes across the POR to yield a usable pixel sample. *(Verify
  in Acquire phase — `docs/01-domain-and-data.md`.)*
- **A-2:** Nearest-station/gage joins are a defensible spatial association for sparse in-situ data at
  300 m; distance windows will be tuned + documented. *(Prepare phase.)*
- **A-3:** Perfect-weather idealization (coincident ERA5) is acceptable for the PoC; real-forecast
  degradation is future work. *(Stated as a limitation everywhere skill is reported.)*
