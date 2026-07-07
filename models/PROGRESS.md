# PROGRESS — modeling layer

Living tracker across the DS arc (define → acquire → prepare → explore → model → evaluate →
communicate). Update the status column and check items as work lands. `[ ]` todo · `[~]` in progress
· `[x]` done · `[!]` blocked. Newest status note at the top of the log.

**Current front line:** **WRAP-UP — all DS-arc phases complete.** Deployed choice = the **lean 2-feature
CyAN model (`cyan_median` + `area_sqkm`) + the EPA CyanoHAB forecast** ("go simple", D-41); full 44-feature
fusion+clim is a **tantalizing-but-unproven** onset avenue, not shipped. The **deck** (`presentation/story.html`)
and the **Part-B dashboard** (`dashboard/`, deployed at https://harmful-algal-bloomspoc.vercel.app/) are shipped.
Open items are deferred cleanup only: the **D-42** climatology-baseline code fix and the **D-43** Codex-workflow-review
items (both deferred to the next, OOM-sensitive rerun; neither overturns the shipped conclusions).

---

## Phase status

| Phase | Status | Key output |
|-------|--------|-----------|
| 0 · Define & design | `[x]` done | `DESIGN.md`, `DECISIONS-LOG.md`, this scaffold |
| 1 · Acquire (Florida) | `[x]` done | CyAN + weather + NWIS + WQP + BasinATLAS pulls landed (`docs/01`) |
| 2 · Prepare | `[x]` done | fused lake-week table (`modeling_table_fusion_fl.parquet`) + `docs/02/03/04` |
| 3 · Explore / feature assessment (Task A) | `[x]` done | significance screens + block **and** feature-level ablation (greedy → lean 2-feature); clustered permutation importance |
| 4 · Model (Task B) | `[x]` done | logistic/HistGBM/XGBoost classifiers, multi-horizon; experiment suites via `experiment_lib.py`; shipped = lean CyAN + EPA |
| 5 · Evaluate | `[x]` done | EPA head-to-head (both thresholds), onset/offset skill, overfit gaps, ablations, onset-by-lead |
| 6 · Communicate | `[x]` done | `presentation/story.html` deck + `dashboard/` Part-B tool (deployed) |

---

## Phase 0 — Define & design `[x]`

- [x] Clarify target/unit/split/models with user (4-question round, 2026-07-02)
- [x] Pull commonly-used features + validation practice from `../Research/` (cited)
- [x] Write `DESIGN.md` (framing, unit, features, split, models, baselines, metrics, leakage guards)
- [x] Write `DECISIONS-LOG.md` (D-01…D-09, W-01, assumptions)
- [x] Write `README.md`, `PROGRESS.md`, `OPEN-QUESTIONS.md`
- [x] Codex adversarial review of the plan → sound fixes folded into `DESIGN.md` v2 (D-11…D-19)
- [x] Resolve blocking `OPEN-QUESTIONS.md` — Q-1/Q-2/Q-6/Q-7 done (Q-3/Q-4/Q-5 are phase-deferred)

## Phase 1 — Acquire (Florida) `[x]`

- [x] Define Florida domain: extent (Census FL polygon, EPSG:5070), POR (OLCI 531 wks), CyAN coverage
      in FL (≈128,628 water px ≈11,577 km²) → `docs/01-domain-and-data.md`
- [x] **Compute-gate estimate** (`acquire/compute_gate_estimate.py`): ≈68.3 M rows; dense monolith
      unsafe → partitioned columnar; **native-pixel viable, no lake fallback** (D-22)
- [x] Obtain CyAN **resolvable-lakes** shapefile → FL lake mask (COMID); **133 FL lakes** confirmed
- [x] Per-lake weekly CyAN **mean/median/SD** (OLCI) + **WHO AL1** target construction (70,623 lake-weeks)
- [x] ERA5 FL subset (coincident + antecedent windows) — 133/133 lakes
- [x] NWIS FL gages (discharge/stage) — 25/133 lakes
- [x] WQP FL stations (nutrients, temp, chl-a, turbidity, EC, DO, pH, Secchi) — 123/133 lakes
- [x] BasinATLAS L12 attributes for FL sub-basins — 133/133 (max-overlap L12 join)
- [x] Write `docs/01-domain-and-data.md` (extents, params, join keys, cost estimate, gate outcome)

## Phase 2 — Prepare `[x]`

**PRE-BUILD PINS (resolve before writing pipeline code — Codex v3 review, D-26):**
- [x] **AL1 threshold** — PINNED: per-lake weekly **median CyAN DN ≥ 130** (≡12 µg/L chl-a) from
      Schaeffer `cyan_processing_conus.R:170` → `docs/03` (sensitivity DN 97/151)
- [x] **Freeze FL lake list** — **133 FL lakes** from CyAN `updatedValidLakes.shp` (2,321 CONUS) →
      `data/derived/fl_resolvable_lakes.gpkg` (`build_fl_lake_mask.py`); reconcile vs forecast `State=FL`
- [x] **Lake-week QA policy** — PINNED (matches Schaeffer): median over `coverage_fraction==1` pixels,
      DN 0 retained, land/nodata NA, all-cloud week → missing (no ice-fill in FL) → `docs/03` §3
- [x] **Feature-availability matrix / temporal protocol** → `docs/02` (issue time, h=0 nowcast vs
      h≥1 forecast, antecedent-only CyAN, oracle-weather + ablation, (value+staleness), two tracks)

- [x] Target construction DONE: per-lake mean/median/SD (OLCI), AL1 label, QA/masking → `docs/03`
      (`prepare/build_cyan_lake_target.py` → `data/derived/cyan_lake_weekly_fl.parquet`).
      **70,623 lake-weeks (133×531), 96.6% valid, FL bloom prevalence 23.2%** (Apopka ~100%✓)
- [x] Feature assembly (value + staleness); **two tracks**; CyAN antecedent-only:
      - [x] **CyAN antecedent block + autoregressive ladder** → `data/derived/cyan_features_fl.parquet`
            (`build_cyan_features.py`; AR(1) corr=0.903 ✓ matches ACAD-092; climatology deferred to split)
      - [x] lake **area** (headline, D-27, later walked back to a whisper in D-39) rides along; depth join skipped (needs HydroLAKES)
      - [x] **ERA5 join** → fusion table (133/133 lakes); weather features screened (`feature_significance_weather.md`)
      - [x] NWIS / WQP / BasinATLAS L12 joins → `modeling_table_fusion_fl.parquet` (339,400×58)
- [x] COMID identity joins (WQP/NARS/NWIS/LakeCat) → NLDI/HUC/nearest fallback + distance windows
- [x] **Assembler** → `data/derived/modeling_table_cyan_fl.parquet` (`assemble_modeling_table.py`):
      339,400 rows, horizons 0–4, latency-guard `feature=target−7·(h+1)` **PASSED**; split train≤2023 /
      val 2024 / test 2025 / oos 2026 (prevalence rising 22%→27%→29%)
- [x] Temporal held-out-year split done (above); z-score fit on train only (in model pipe)
- [!] **Secondary blocked-lake (unseen-lake) stress test — NOT run (known limitation).** Same-lake temporal
      validation only; unseen-lake transfer is untested (see D-43 #10; deck says "less tied to per-lake identity", not "generalizes").
- [x] Leakage checklist run (temporal/circularity/normalization/feature-selection/version) — clean on the core
      CyAN pairing/CRS/metrics (D-43 #13–15); surfaced two claim-gate deviations logged as known limitations
      (feature-selection screens ran over all years; non-CyAN joins one week stale — D-43 #1/#2)

## Phase 3 — Feature assessment / Task A `[x]`

- [x] Coincident non-random-distribution test per non-literature candidate (with correction) — static/in-situ/weather
      screens (`feature_significance_*.md`). **Known limitation (D-43 #1): screens ran over all years, not train-only.**
- [x] Finalize included feature set (literature-precedent + passed-test), log outcomes (no cherry-pick) — greedy backward
      ablation → **lean `cyan_median` + `area_sqkm`**; clustered permutation importance (one CyAN cluster ≈100% of skill)

## Phase 4 — Model / Task B `[x]`

- [x] Baselines: persistence + climatology + **CyAN ladder** + **EPA head-to-head** DONE per horizon
      (`model/eval_cyan_baselines.py` → `outputs/cyan_baseline_eval.md`; `model/eval_epa_headtohead.py`
      → `outputs/epa_headtohead.md`). Test-2025 ladder AUC 0.987→0.973; high absolute AUC = circularity
      → fused bar = **lift over ladder+climatology + transition-week skill**. **EPA:** on shared FL 2025
      (4,527 lake-wk), EPA AUC 0.928 does NOT clearly beat persistence (ΔAUC CI incl. 0) vs our AL1 —
      but structural advantage to us (all else AL1-derived) + seasonal + definition caveats; **no
      "beat EPA" claim.**
- [x] Classifiers: **logistic GLM · HistGBM · XGBoost** — one model per horizon (h=0–4). *(SVC / logistic GAM were in
      the DESIGN plan but not built — D-36b: architecture barely mattered, so the three above sufficed.)*
- [x] Explainability: **incremental lift over the ladder** first (block + feature-level ablation, clustered permutation
      importance) → fusion adds no robust incremental held-out skill; deployable = lean CyAN autoregression + EPA
- [~] `docs/05-modeling-plan.md` + `model-cards/` folded into `RESULTS-SUMMARY.md` + `DECISIONS-LOG.md` (no separate files)

## Phase 5 — Evaluate `[x]`

- [x] Skill-vs-lead-time curve, all models vs baselines (`experiments.md`, `headtohead_onset.md`); onset-MCC-by-lead
- [x] Classification skill per horizon: AUC + **PR-AUC / MCC / Brier / onset-AUC / onset-MCC / event counts**
- [x] EPA head-to-head on shared FL COMID-weeks (both operating points; week-block bootstrap CIs); **blocked-lake
      stress test NOT run** (known limitation, D-43 #10)
- [x] Honest limitations write-up (oracle-weather ablation, circularity/ladder lift, known-lake-only, AL1 proxy) →
      `RESULTS-SUMMARY.md` + deck Defensibility (appendix); Codex-workflow-review limitations logged (D-43)

## Phase 6 — Communicate `[x]`

- [x] Figures/tables that feed Part B (tool) and Part A (slides) — all deck charts built from `data/*.json` (none
      hardcoded); **deck `presentation/story.html`** + **Part-B dashboard `dashboard/`** (deployed to Vercel)

---

## Status log (newest first)

- **2026-07-07** — **WRAP-UP.** All DS-arc phases complete. Shipped: the **deck** (`presentation/story.html`) and the
  **Part-B dashboard** (`dashboard/`, deployed at https://harmful-algal-bloomspoc.vercel.app/, live-embedded in the deck).
  Deployed forecaster = **lean 2-feature CyAN (`cyan_median` + `area_sqkm`) + EPA** ("go simple", D-41). Two deferred
  cleanup items (next OOM-safe rerun), neither overturning the shipped conclusions.
- **2026-07-07** — **CODEX WORKFLOW REVIEW LOGGED (D-43).** The untracked `models/CODEX_REVIEW_workflow.md` (15-point
  acquire→evaluate technical audit) was reconciled into the audit trail. **CONFIRMED-clean negatives:** core CyAN
  horizon pairing, `metrics.py` formulas, CRS/geospatial handling. **Known limitations (documented, deferred; do NOT
  overturn the shipped lean-model or the fusion-negative):** (#1) feature-selection screens ran over all years, not
  train-only; (#2) non-CyAN joins one week too stale for h≥1 (conservative — makes fusion look *weaker*); (#5) in-situ
  ffill without a max-age / staleness companion; (#3/#4) some operating-point thresholds tuned on test/embed val labels
  in `clim`; (#7) onset metrics lack CIs; (#8/#9) generated-output wording lags the code; (#10) "generalizable" exceeds
  the same-lake-only design (deck already softened to "less tied to per-lake identity"). See D-43.
- **2026-07-07** — **CLIMATOLOGY-BASELINE FIT INCONSISTENCY (D-42) + full-deck value audit.** Climatology baseline is
  fit train+val in `eval_experiments.py` (0.952/0.886/0.363) vs train-only in `experiment_lib.py` (0.936/0.851/0.323);
  train+val is the fair fit. Deck slide 17 patched to the train+val values (interim); code fix + regeneration deferred.
  A 4-agent value audit + an independent Codex review (verdict **GO**) found no other same-window numeric conflict.
- **2026-07-06** — **ONSET-MCC BY HORIZON; full fusion reframed "tantalizing but unproven" (D-41).** Added onset-MCC/
  onset-AUC across leads to `eval_experiments.py` (+ a `lean` 2-feature suite). Full fusion+clim leads onset-MCC at every
  lead on the 2-yr test (0.466 vs lean 0.314 at h1) but it is **not significance-tested** (onset-AUC CI includes 0) and
  **climatology also beats lean at every lead** — so much is seasonality. **Decision: ship the lean CyAN model + EPA
  ("go simple"); full fusion+clim = an unproven avenue to validate next.** Deck slides 14–18 reworked; Defensibility → appendix.
- **2026-07-06** — **EVAL THRESHOLD-TUNING FIX (D-40, Codex-flagged).** A follow-up Codex leakage
  re-review confirmed the antecedent-CyAN "no temporal overlap" claim **survives**, but found a *separate*
  eval leak: the onset head-to-head script (`eval_headtohead_onset.py`) tuned the operating thresholds for
  climatology / CyAN-ladder / fusion on the **test** labels. Fixed to tune on **validation** (thr-models
  fit on train, F1 threshold picked on val); EPA stays at fixed 0.10/0.50; persistence 0.5. Re-ran →
  `headtohead_onset.md` regenerated. **Effect (h1):** fusion onset-MCC **0.474→0.349** — it no longer
  "leads" the thresholded alert; CyAN-ladder (0.375) ≈ climatology (0.371) ≈ fusion (0.349) tie, so
  **fusion adds nothing over the CyAN-only ladder on the alert** (strengthens the fusion-negative). onset-
  AUC (threshold-free) unchanged: fusion 0.944 ≈ ladder 0.943 > clim 0.896 > EPA 0.818. No other eval
  affected (the shared `experiment_lib` harness already tuned on val; EPA cutoffs are fixed). Propagated
  to `RESULTS-SUMMARY.md` §3/§4 + `presentation/story.html`.
- **2026-07-06** — **FEATURE-LEVEL ABLATION + CLUSTERED PERMUTATION IMPORTANCE, Codex-reviewed (D-39).**
  (1) Greedy backward ablation (pooled & onset-AUC criteria) strips to `cyan_median`+`area_sqkm` on any
  AUC metric but loses operating-point skill (onsetMCC 0.466→0.314) — greedy-on-AUC is blind to the alert
  decision. (2) Clustered permutation importance (`exp_perm_importance.py`): **one cluster (CyAN-level)
  ≈100% of skill** (scramble → onsetMCC 0.466→0.002); nothing else has large cross-arch importance.
  (3) Decomposition (`exp_perm_c1_decomp.py`, Codex's #1 follow-up): **`clim` is redundant-but-exploited**
  (permutation reliance ≥ all real-time CyAN; drop-column cost only 0.068) → memorization shortcut, stays
  a BASELINE (**vindicates D-35**). **Real-time CyAN alone is sufficient + generalizable** → deployable
  model = clim-free CyAN autoregression. (4) **Walked back D-27**: `area_sqkm` is a whisper, not a
  headline driver. Codex: no method/leakage bug; corrected "noise"→"small/inconsistent", "no skill"→"no
  incremental held-out skill". Docs: `docs/04` §Multivariate importance, D-39.
- **2026-07-06** — **EPA-FAIRNESS AUDIT + PART-2 ABLATION Codex-reconciled + PART-3 launched (D-38).**
  (1) Audit confirmed our label **IS** EPA's own event (median CyAN DN≥130 = WHO AL1, pinned verbatim
  from Schaeffer's code) → apples-to-apples, not an in-house target. (2) Fixed EPA misrepresentation:
  harness now reports EPA at **both @0.50 (acc-opt) and @0.10 (EPA's deployed cutoff)** — at 0.10
  overall MCC 0.636→0.672, flipMCC_h1 +0.026→**−0.059** (EPA is anti-predictive on flips, agreeing with
  `epa_headtohead.md`). (3) Reporting contract extended: always show **AUC-ROC, AUC_within (+n), MCC**.
  (4) Part-2 block ablation: **CyAN dominant survives**; "weather net-negative" **downgraded to
  neutral/no-detectable-benefit** (Codex); clim trades ranking for onset-calibration. (5) **Part-3
  feature-level greedy backward ablation running** (`exp_feature_ablation.py`) + regen of block/change
  tables through the fixed harness (sequential — concurrent runs OOM'd).
- **2026-07-05** — **ONSET-METRIC CORRECTION (D-37, Codex-reconciled).** Codex Exp-1 review → my flip
  metric conflated onset/offset (hid ranking skill) + change features were redundant. Fixed harness
  (`experiment_lib.py`): non-redundant CHANGE (non-overlap trends + train-clim anomalies), onset/offset
  split, EPA fixed-threshold, standard train+val refit. **CORRECTED: onsets ARE rankable** — onsetAUC h1
  fusion_full **0.935** / fusion+clim 0.93–0.94 / nocyan+clim ~0.89 / climatology 0.851 / EPA 0.831 /
  persistence 0.50. **Fusion beats climatology AND EPA on early-warning** (onsetMCC 0.47 vs 0.32 vs 0.23)
  [⚠️ SUPERSEDED 2026-07-06 / D-40: the 0.47 was a test-threshold-tuning artifact; with val-tuned
  thresholds fusion onset-MCC is **0.349** and does NOT beat the CyAN-ladder (0.375) or climatology
  (0.371) on the alert — the onset-AUC *ranking* result is unaffected];
  CyAN sub-threshold value helps rank onsets. Weather CHANGE still adds ~nothing (negative holds).
  nocyan overfits more (~0.04). → **NEXT: Part 2 feature ablation, then Codex.**
- **2026-07-05** — **EXPERIMENT SUITE (D-36): split 60/20/20 2yr-test, arch grid logistic/HistGBM/
  XGBoost, anti-persistence track.** `eval_experiments.py` → `outputs/experiments.md`. **Findings (h=1,
  771 flips):** (1) **architecture barely matters** — logistic≈HistGBM≈XGBoost on CyAN/fusion; GBDTs
  better on sparse fusion (native NaN); XGBoost≈HistGBM confirmed. (2) **Anti-persistence confirmed:**
  fusion_nocyan drops aggregate (0.985→0.944 AUC) but takes **flips from anti-predictive to neutral**
  (flip_MCC −0.51→+0.01). (3) **Sobering:** the drivers don't ACTIVELY predict onsets — fusion_nocyan
  ~random on flips (0.49), and **climatology (seasonal) is the BEST flip predictor** (+0.07→+0.15,
  grows with horizon). **+clim configs added (user):** climatology-as-feature helps CyAN models' flips
  (fusion_full+clim best CyAN flip_MCC −0.30) + nocyan aggregate (0.944→0.951), but **NO config beats
  plain climatology on flips** — fusion_nocyan+clim (+0.017) is even *worse* than climatology alone
  (+0.071). **CLEAR-EYED CONCLUSION: seasonal climatology is the CEILING for onset prediction; drivers
  carry ~no onset signal beyond seasonality → bloom ONSETS not predictable at useful skill from these
  public features.** (Change-features worth a quick try; expectations tempered.)
- **2026-07-05** — **FUSION MODEL EVAL Codex-reconciled & FINALIZED (D-35).** `eval_fusion.py` →
  `outputs/fusion_eval.md` (val-threshold+early-stop, paired within-CI, block ablation+permutation,
  h=0–4). **Honest verdict:** fusion beats the ladder by a **tiny real** margin (paired within-lake
  **+0.015 [+0.003,+0.021]**) but is **CyAN-dominated** (perm: CYAN +0.27 vs drivers ~0.002–0.005) and
  **anti-predictive on flips** (only climatology positive) — flip anti-predictivity shrinks with horizon
  (−0.65 h0 → −0.29 h3/4). **NEXT: anti-persistence model series** (drop antecedent CyAN levels to free
  the model for onsets; user idea) + onset/change features + transition-primary metric.
- **2026-07-05** — **WEATHER (ERA5) screened + fusion table assembled + location audit.** Weather screen
  (`screen_weather_features.py`, on the rerun-SPEI file) → `feature_significance_weather.md`: **all 133
  lakes**, strongest **forecast-eligible** drivers — solar/PET/GDD **+** (lag AUC ~0.62–0.66),
  precip/SPEI/wind **−**, calm-hours **+**. **Fusion table** built (`assemble_fusion_table.py` →
  `modeling_table_fusion_fl.parquet`, CyAN+static+WQP+NWIS as-of-cutoff + staleness; weather block to
  add next). **Location audit (2 subagents):** neither we nor EPA use discrete lake ID; EPA =
  generalizing SPDE + morphology; OUR only identity-like feature = per-lake climatology (`clim`) in the
  ladder logistic → **decision pending:** demote climatology to baseline-only, add generalizing
  morphology/seasonality, run blocked-lake stress test. `docs/04` updated.
- **2026-07-03** — **IN-SITU FEATURE SCREEN COMPLETE + Codex-reconciled (D-34)** →
  `docs/04-feature-assessment.md` (consolidated). WQP screened (123/133 lakes). Engine reconciled:
  variable CLASS (driver/consequence/circular), TIMING (antecedent/same_week), **within-lake bootstrap
  significance gate**, anomR past-only, anomC LOO, flux-only sums. **chl-a lead test** (`chla_leadlag.md`):
  lagged chl-a = real independent lead (AUC ~0.6) but weaker than CyAN's own antecedent — coincident
  barred, lagged kept. **Genuine drivers:** antecedent **TP** (lag4, forecast-eligible), **water-temp
  anomalies**; orthoP/ammonia inverse (drawdown). Static weak (area/inundation only). Limits: WQP not
  unit-harmonized, TN/pH undercounted, NWIS 25/133. **Weather (ERA5) deferred.**
- **2026-07-02** — **NWIS in-situ temporal features screened** (`pull_link_nwis_fl.py` +
  `screen_insitu_features.py` → `outputs/feature_significance_nwis.md`). Pulled 812 sites/554k daily
  values; linked (in-lake+250m→L12-median). **Coverage 25/133 lakes** (many FL lakes are seepage, no
  gages). Reps: coincident/lag1,2,4/mean·sum4,12/delta/anomR/anomC. Test = lake-block bootstrap AUC +
  **within-lake AUC** (key: exposes datum/size between-lake artifacts). **Findings:** water-temp = real
  within-lake signal (AUC_within ~0.78; warmer-than-normal anomalies ~0.65); gage-height real inverse
  within-lake (~0.30, pooled datum-inflated); discharge weak. → **NEXT: WQP (same engine).**
- **2026-07-02** — **FEATURE SCREENING started (D-33).** Lake→L12 join built
  (`join_basinatlas_l12.py`, 132/133). **Static assessment** (area + 32 BasinATLAS L12; per-lake n=132,
  Spearman, **p<0.1 inclusion screen** + FDR honesty) → `outputs/feature_significance_static.md`:
  **13/33 pass p<0.1, 1 survives FDR** (inundation; area included p=0.009/q=0.068). Honest weak
  result → signal is in within-lake temporal dynamics. **Codex-reviewed & reconciled** (max-overlap L12
  join, 133/133; extent/QA/wording fixes). Depth skipped (needs HydroLAKES). → **NEXT: FL NWIS + WQP
  pull → link (in-lake+250m → L12-median → null) → coincident/aggregated/lagged temporal features →
  significance screen (lake-aware).**
- **2026-07-02** — **EPA head-to-head Codex-reconciled + FLIPS added.** Provenance (snapshot, not
  as-issued), corrected caveat framing (same AL1 concept; Brier gap descriptive), timing, exact-key
  seasonal, dead-code removed. **Flips finding (pivotal):** ordering INVERTS on transition weeks —
  climatology AUC 0.551 > EPA 0.455 > our CyAN-only ladder 0.118 (anti-predictive) > persistence 0.000.
  CyAN-only aggregate dominance = artifact of easy weeks; **fusion features must beat climatology on
  flips.** `DESIGN §8`, D-32 updated. → **NEXT: generate + assess fusion features (ERA5/NWIS/WQP/BasinATLAS).**
- **2026-07-02** — **EPA head-to-head built** (`eval_epa_headtohead.py` → `outputs/epa_headtohead.md`).
  Shared FL 2025 (4,527 lake-wk, 132 lakes × 35 wk; exact COMID+week join, 132/132 overlap). Scored vs
  **our AL1**: EPA AUC-ROC 0.928 / Brier 0.101 — **does NOT clearly beat persistence** (week-block
  bootstrap ΔAUC +0.010, 95% CI [−0.000, +0.022]). **Honest framing (3 caveats):** structural advantage
  to us (all else AL1-derived; EPA predicts its own threshold); **seasonal** — EPA Apr–Nov only, 35/52
  wk, base rate 28.8% vs 26.6% (modest effect, FL near-aseasonal — AUC ≈ unchanged); threshold-free
  first. **No "beat EPA" claim.** Fair EPA eval needs EPA's own bloom definition (follow-up).
- **2026-07-02** — **Climatology made an explicit comparator (all samples) vs persistence + ladder**
  (pairwise MCC/AUC-ROC/Brier deltas + MCC-by-horizon table → `outputs/cyan_baseline_eval.md`).
  **Codex round-3 caught an overclaim (corrected):** the **ladder** is the strongest CyAN-only baseline
  overall (best AUC-ROC/AUC-PR/Brier; ties persistence on h0 MCC). Climatology is a strong *ranker*
  (beats persistence on AUC-ROC, widening) but weak *classifier* (lowest MCC 0.75) — **never** the
  single best baseline (I had wrongly said "best AUC-ROC"). Fused model must beat the best on EACH
  metric. Deltas/arithmetic verified by Codex. → EPA head-to-head next.
- **2026-07-02** — **Codex round-2 (metrics+assembler+baselines) incorporated (D-30a–h); Codex
  reconfirmed the numbers from the parquet.** Wide suite (`model/metrics.py`: AUC-ROC, AUC-PR, Brier,
  **MCC**, F1, Prec, Recall, Acc); persistence = last-valid carry-forward (not fill-0); threshold tuned
  on val; **transition-week eval added**. **Headline (corrected):** on flips the CyAN-only ladder is
  **anti-predictive** (AUC-ROC<0.5, MCC negative all h) — it predicts the WRONG direction on onsets;
  climatology is the only weakly-positive CyAN flip signal (MCC≤0.15). Absolute skill dominated by
  per-lake seasonal identity (climatology AUC 0.955). **Fusion bar = transition-week skill + lift over
  ladder AND climatology.** Ready for **EPA head-to-head** next.
- **2026-07-02** — **ASSEMBLER + CyAN-only BASELINES BUILT (first real skill numbers).** Assembler:
  339,400 rows, latency leakage-guard PASSED. Baselines on held-out **test year 2025** (base rate
  26.6%): persistence AUC 0.941→0.884 (h0→h4, decays as CyAN staleness grows); **CyAN ladder** AUC
  0.987→0.973, **beats persistence at every lead, gap widening +0.05→+0.09**; climatology flat 0.955.
  **Honest headline: absolute AUC is very high because the target is autocorrelated CyAN (the D-26a
  circularity) → the fused model's bar is INCREMENTAL LIFT over the ladder (Brier/PR-AUC/calibration +
  transition weeks), not headline AUC.** `outputs/cyan_baseline_eval.md`.
- **2026-07-02** — **Codex review (baseline+features) incorporated (D-29a–i, no BLOCKING).** Code:
  `cyan_sd`→sample SD (ddof=1), added `valid_frac` + coverage sensitivity, renamed
  `staleness_weeks`→`cyan_gap_weeks_at_cutoff`, added `bloom_roll4_n`, kept `n_inside`, within-lake AR
  diagnostic. Docs: explicit issue-time/publish cutoff + EPA info-set W−1/W−2 sensitivity, coverage
  sensitivity (parity primary), 8×-approx honesty, h=0=diagnostic-only, area-claim softened, assembler
  leakage tests required. **VERIFIED after rebuild+re-run:** coverage sensitivity 6.76% (`<0.5`) vs
  24.75% (`≥0.5`); **AR(1) pooled 0.903 → within-lake 0.734 / median-per-lake 0.666** (honest temporal
  number). Both artifacts regenerated with fixes.
- **2026-07-02** — **Baseline updated (D-28): latency-aware persistence is the primary reference**;
  both our model AND EPA scored as skill over `Persistence(W,h)=bloom(W−h−1)` (CyAN ~1-week composite
  latency, cyan/METADATA §13). Feature-availability matrix corrected so CyAN features use the same
  `W−h−1` freshest week (no fresher-than-baseline). `DESIGN.md` §8 + `docs/02` updated. → Codex review.
- **2026-07-02** — **Feature build started.** Pin #4 done: feature-availability matrix / temporal
  protocol → `docs/02` (h=0 coincident nowcast vs h≥1 forecast; antecedent-only CyAN; oracle-weather +
  ablation). **CyAN antecedent feature block + autoregressive ladder built** →
  `cyan_features_fl.parquet` (70,623×20). **AR(1) corr(median,lag1)=0.903** — empirically matches
  ACAD-092, confirming persistence is the baseline to beat. ERA5 join **held** pending upstream SPEI
  derived features; NWIS/WQP/BasinATLAS/depth next.
- **2026-07-02** — **TARGET DATASET COMPLETE.** `cyan_lake_weekly_fl.parquet`: 70,623 lake-weeks
  (133×531, 2016-04-24→2026-06-21), **96.6% valid**, **FL bloom prevalence 23.2%** (~2–3× EPA CONUS →
  milder imbalance; near-flat seasonality → all-weeks modeling justified; Apopka ~100%). Findings +
  schema in `docs/03` §6. Also: lake **area elevated to headline feature** (D-27, sub-resolvable-
  waterbody expansion hook). **Next:** feature layers — pin #4 (feature-availability matrix) + ERA5
  (FL daily 2016→present ready) / NWIS / WQP / BasinATLAS joins by COMID.
- **2026-07-02** — **Build proceeding.** Pins #1–3 resolved from Schaeffer's actual code (AL1 = median
  DN≥130; `coverage_fraction==1` aggregation) → `docs/03`. FL mask built: **133 lakes** from CyAN
  `updatedValidLakes.shp` (`build_fl_lake_mask.py`). Target aggregation validated on 4 weeks (Apopka
  bloom✓, Okeechobee low✓); **full 531-week run in progress**. Only pin #4 (feature-availability
  matrix) remains, and it gates *features*, not the target.
- **2026-07-02** — **Codex v3 review incorporated** (D-26a–f): circularity control (CyAN
  autoregressive-ladder baseline + antecedent-only CyAN features), AL1 threshold to be pinned from
  Schaeffer code, two feature tracks (parity vs augmented), benchmark on shared FL COMID-weeks,
  secondary blocked-lake stress test, concrete lake-week QA + per-horizon PR-AUC/calibration. Stale
  spatial-split tasks removed from Phase 2/5. **4 pre-build pins** logged (Phase 2). **Proceeding to
  build** — starting with pin #1 (AL1 threshold from Schaeffer's code) + pin #2 (freeze FL lake list).
- **2026-07-02** — **PIVOT to match the EPA/Schaeffer forecast** (D-23/24/25): unit = **resolvable
  lake** (per-lake CyAN mean/median/SD), split = **temporal held-out-year**, target = **WHO AL1
  binary** (median chl-a ≥12 µg/L). Models become classifiers, all full-scale (N ≈ FL lakes × weeks →
  no subsampling). `DESIGN.md` → **v3**; `docs/01`, `OPEN-QUESTIONS`, `DECISIONS-LOG` synced. Pixel
  compute-gate retained as context (choice made on comparability, not compute). Next: resolvable-lakes
  FL mask + per-lake aggregation + AL1 target.
- **2026-07-02** — **Acquire started.** Compute gate measured & resolved (D-22): FL inland-water CyAN
  footprint ≈128,628 px ≈11,577 km² (matches FL's ~12,000 km² surface water — clip validated) →
  ≈68.3 M pixel-week rows over 531 OLCI weeks; dense monolith unsafe → **partitioned columnar; native
  300 m pixel viable, no lake fallback**. Q-5 closed. `acquire/compute_gate_estimate.py` +
  `docs/01-domain-and-data.md` written. Next: CyAN→FL clip + target construction.
- **2026-07-02** — Codex review complete; `DESIGN.md` bumped to **v2** incorporating the sound fixes
  (D-11…D-19: oracle-weather labeling, persistence redefinition + issue-time, train-only feature
  selection, clustered uncertainty, chl-a ablation, fusion-stage compute gate, target QA policy, new
  required artifacts). **Blocked on user call for Q-6 (temporal split) + Q-7 (OLCI-only)** before
  Acquire.
- **2026-07-02** — Phase 0 scaffold stood up (README, DESIGN, DECISIONS-LOG, PROGRESS,
  OPEN-QUESTIONS). Design reflects the 4-question round + a cited research extract from `../Research/`.
