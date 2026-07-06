# DESIGN — Florida CyAN multi-horizon bloom forecasting

> Authoritative modeling design spec. **v3, 2026-07-02** — pivoted to **match the EPA/Schaeffer
> forecast** (lake-level unit, temporal split, WHO Alert Level 1 target). Supersedes v2. Decisions +
> rationale in [`DECISIONS-LOG.md`](DECISIONS-LOG.md) (D-23/24/25 pivot; earlier D-01…D-22 amended
> where noted); unresolved choices in [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md). Literature cited by
> source ID (e.g. `ACAD-048`), traceable via [`../Research/REFERENCES.md`](../Research/REFERENCES.md).
> The federal benchmark we mirror is documented in
> [`../data-sources/cyano-forecasts/METADATA.md`](../data-sources/cyano-forecasts/METADATA.md).

> ⚠️ **RESULTS UPDATE (2026-07-06) — read [`RESULTS-SUMMARY.md`](RESULTS-SUMMARY.md) for the concluded
> findings.** This spec is the *plan*; several of its bets resolved as clear-eyed **negatives** once the
> experiments ran (all logged D-37…D-39):
> - **Fusion is a negative result** — weather/in-situ/morphology add **no robust incremental held-out
>   skill** over CyAN; the model is a **real-time-CyAN autoregression** (clustered permutation importance:
>   the CyAN-level cluster ≈ 100% of skill).
> - **`clim` stays a BASELINE, not a feature** — it's a redundant-but-exploited per-lake memorization
>   shortcut; the deployable model is **clim-free** (D-35, empirically vindicated D-39c).
> - **Lake area (§1/§3 below) was WALKED BACK** — permutation importance shows it is a *whisper*, not a
>   headline driver (D-27 → **D-39d**); the future-work motivation stands, the "first-class feature"
>   framing does not.
> - **Early warning works** — onset-AUC ≈ 0.94 (positive-only onset), beating climatology and EPA.

---

## 1. Problem framing & scope

**Goal.** Forecast **cyanobacteria-bloom presence** in **Florida lakes**, fusing a remote-sensing
target (EPA/NASA **CyAN**) with in-situ and static predictors — deliberately **matching the design of
the EPA experimental CyanoHAB forecast** (Schaeffer et al. 2024, INLA) so our model is a
**like-for-like, benchmarkable** counterpart to the strongest published federal product for this task.

**Target = WHO Alert Level 1 (AL1), binary, per lake-week.** A bloom is **lake-wide weekly median
surface chlorophyll-a ≥ 12 µg/L with cyanobacteria dominance**, evaluated over the satellite-resolvable
area — exactly EPA's definition. We operationalize it on the CyAN signal (per-lake **median** CI_cyano
exceeding the AL1-equivalent threshold; CI↔chl-a mapping pinned in `docs/03`). Models predict
**P(bloom)**. This is a **satellite-derived label**, not ground truth or a toxin measure (correlation
≠ causation; CI→chl-a conversion has scatter — stated as a limitation).

**Two tasks:**

- **Task A — Feature assessment (coincident / nowcast).** Include a candidate feature if (a) it (or a
  proxy) is *commonly used* in the HAB literature, or (b) it passes a statistical test that the target
  is distributed **non-randomly** with respect to it, at **zero lag**, **run on the training years
  only** (frozen before the held-out test).
- **Task B — Multi-horizon forecasting.** Predict P(AL1 bloom) at lead times **h ∈ {0,1,2,3,4}
  weeks**. EPA's product is the **h = 1 (7-day)** case, so **our h = 1 is the direct head-to-head**;
  the other horizons extend the skill-vs-lead-time curve. Under the **oracle-weather idealization**
  (coincident ERA5 always available) — a potential-predictability upper bound, *not* an operational
  forecast (real forecast weather deferred). Reported as such, never as operational "two-weeks-early"
  skill.

**Issue time & feature cutoff.** Each lake-week has an **issue date**; all features must be available
at/before it. The lagged target and antecedent weather draw only from before the target week (the one
documented exception is coincident ERA5 under the oracle idealization). Enforced via the
feature-availability matrix (§3).

**Explicitly deferred to future work** (unchanged): CyAN→cell/toxin linkage; local grab-sample fusion;
live optical/SAR retrievals; basin-scale hydrologic modeling; a global/transferable model;
weather-forecast uncertainty (oracle-weather for now); and **sub-resolvable (< ~900 m) waterbodies** —
CyAN can't see them but they're SePRO's core customers, so this is the **priority extension**, and the
**lake-area feature's importance (§3) is the evidence for prioritizing it** (finer sensors / in-situ).

**Standing caveat.** Every driver/importance statement is **correlational and model-relative**, not
causal [`ACAD-048`].

---

## 2. Analysis unit, aggregation & data fusion

**Unit = the resolvable lake × week** (matches EPA). One row = one lake for one weekly period.

**CyAN → lake aggregation (Schaeffer recipe, `cyan_processing_conus.R`).** For each resolvable lake ×
week, compute the **mean, median, and SD** of CyAN CI over the lake's resolvable pixels (mixed/edge
pixels masked, §4). The **median** defines the AL1 target (§1); mean/median/SD become CyAN features
(§3). This is a deliberate, **user-authorized aggregation** (D-23) — the standing no-aggregation rule's
explicit per-case sign-off — with a documented recipe; raw pixels are retained for QA only.

**Lake universe / Florida mask.** The **CyAN resolvable-lakes set** (COMID-keyed, the same backbone as
`cyan`/`EPA-NARS`), filtered to Florida. This doubles as the EPA benchmark's lake list, so our lakes
line up with theirs. Exact FL lake count to be pulled in Acquire (§ per-source plan) — order of a few
hundred at most, so N ≈ FL lakes × 531 weeks ≈ **tens of thousands of rows** (compute is a non-issue;
the pixel-level gate of v2 is now moot — see `docs/01`).

**Fusion by identity, then proximity.** COMID gives **identity joins** to WQP, NARS, NWIS, and LakeCat
(the reason for going lake-level). Where identity is unavailable, fall back to NLDI topology / HUC12 /
nearest-station within a max radius (join hierarchy in `docs/01`). Weather joins to the overlying ERA5
cell(s) covering the lake.

| Source | Native support | Join to a lake-week |
|--------|----------------|----------------------|
| CyAN CI (target + feature) | 300 m raster | per-lake mean/median/SD over resolvable pixels |
| ERA5 weather | 0.25° grid | overlying cell(s); coincident + antecedent (oracle) |
| NWIS hydrology | point gages | COMID/NLDI/HUC/nearest + **staleness** |
| WQP water quality | point stations | COMID/NLDI/HUC/nearest + **staleness** per analyte |
| BasinATLAS L12 + lake morphology | polygons | containing L12 sub-basin + lake depth/area |

---

## 3. Feature representation (tabular)

Per-lake-week columns. Full catalog + citations in `docs/02-feature-catalog.md`. We use a **superset**
of EPA's predictors (they use water-temp, precip, depth, area):

- **CyAN (per-lake)** — **antecedent-only** weekly **mean / median / SD** of CI (lag-1/2/4), **never
  the target week's CyAN** (the label is CyAN-derived, so a coincident CyAN feature is circular). Per-
  lake CI is strongly autocorrelated (AR1 α≈0.90 [`ACAD-092`]) → these define the **autoregressive-
  ladder baseline** (§8) that fusion features must beat to earn any importance claim.
- **Lake surface area — ⚠️ WALKED BACK (D-39d, 2026-07-06): a *whisper*, not a headline driver.**
  Permutation importance found area's marginal contribution tiny (Δonset-MCC ~+0.018, Δ pooled ~0; not
  cross-arch robust; not FDR-significant in the static screen). Report it as a minor/context feature; the
  future-work motivation (resolving sub-300 m waterbodies matters to SePRO) still stands. *Original plan
  (superseded framing):* "first-class, prominently-reported feature (and a strategic diagnostic)."
  Area is already a Schaeffer/EPA-parity predictor (static; `AREASQKM` from the resolvable-lakes
  shapefile, carried in the FL mask + target table), but we **elevate it deliberately and report its
  importance + partial-dependence in every model**, never buried in a morphology bundle. Rationale:
  **area's utility is itself a finding — but hypothesis-generating, not proof (Codex M7).** A strong
  area effect *prioritizes* investigating smaller waterbodies (CyAN only resolves lakes ≥ ~900 m across,
  ≥ 3×3 px, **excluding the sub-300 m waterbodies that are SePRO's likely customers**,
  `../data-sources/cyan/METADATA.md` §5). **Caveats up front:** area is confounded with depth, trophic
  state, region, and the CyAN measurement process; and importance *within* 133 resolvable lakes does
  **not** extrapolate below CyAN's support — it *motivates* a finer-sensor/in-situ extension (§1), it
  does not validate one. We test area **non-linearly** (small- vs large-lake regimes) with **area-binned
  calibration + blocked lake-size-band validation**, and use *no-extrapolation-below-support* language.
- **Other static — depth + BasinATLAS L12** — mean/max depth (EPA morphology predictor), plus L12
  sub-basin attributes (land use, climate normals, anthropogenic). Static lake identity/morphology also
  carries the cross-lake structure EPA models with an SPDE spatial field.
- **Weather — ERA5** (we use ERA5, **not** EPA's PRISM): air temperature (proxy for water temp, r>0.93
  [`ACAD-048`]), precipitation (antecedent/cumulative [`ACAD-049`]), solar, wind, evaporation,
  pressure — coincident + antecedent windows.
- **In-situ hydrology — NWIS** (beyond EPA): discharge / gage height — proxy for loading + flushing
  [`FED-024`]. **(value + staleness).**
- **In-situ water quality — WQP** (beyond EPA): water temp, TP, TN, NH₃-N, chl-a, turbidity, EC, DO,
  pH, Secchi — direct measurements, after WQX2/3 reconciliation (dedup/units/censoring; drop
  NARS-in-WQP). **(value + staleness).**

**Two feature tracks (for honest benchmarking).** *EPA-parity set* = CyAN + precipitation +
water-surface-temperature + lake depth + surface area (Schaeffer's predictors / our proxies) — the
**only** track that supports a head-to-head EPA claim. *Augmented SePRO set* = parity **+** NWIS + WQP
+ BasinATLAS L12 + extra ERA5 — reported as an **extension**, not a like-for-like comparison.

**(value + staleness) rule (D-02).** Every temporal feature = last observed **value** + **staleness**
(days before issue date). Handles irregular in-situ sampling **without interpolation**.

**chl-a circularity — ablation (D-15, refined by the D-34 lead test).** WQP chl-a is a biomass proxy
and the AL1 target is chl-a-defined → **coincident** chl-a is redundant with the target (circular).
BUT WQP is a *direct in-situ* measurement, distinct from CyAN's remote cyano-index — and the lead test
(`outputs/chla_leadlag.md`) shows **lagged chl-a carries genuine independent lead**: conditioned on
CyAN-clear, antecedent chl-a predicts a bloom h weeks out at AUC_within ≈ 0.59–0.63 (weaker than CyAN's
own sub-threshold CI, ~0.70–0.82). So: **coincident chl-a barred** from driver/early-warning claims;
**lagged chl-a kept as an independent (modest) in-situ early-warning feature** (its value is catching
sub-pixel/nearshore onset CyAN's lake-median misses). Remains an **ablation group** (skill with/without).

**Required artifacts:** per-horizon **feature-availability matrix** (allowed-at-issue / latency /
staleness / oracle-only); **derived-row provenance** (COMID, source IDs, timestamps, join method +
distance, staleness, QA flags).

---

## 4. Target definition & QA/masking policy (predeclared)

- **AL1 label — PINNED (`docs/03`): per-lake weekly median CyAN DN ≥ 130** (≡ 12 µg/L chl-a, WHO AL1;
  from Schaeffer `cyan_processing_conus.R:170`). Binary. Sensitivity tiers: DN 97 (3 µg/L) / 151
  (24 µg/L). Aggregate mean/median/SD over pixels **fully inside the lake polygon**
  (`coverage_fraction==1`, `na.rm`); the **median** drives the label and is the primary CyAN feature.
  CI↔chl-a scatter → the label is a satellite AL1 realization, not a lab measure (stated limitation).
- **Pixel QA + lake-week validity — PIN before aggregation.** DN 0 = below-detection (valid, low
  signal); DN 254 (land) / 255 (no-data/cloud) masked; **mixed/edge pixels masked** (Schaeffer step
  1/2). **Primary = Schaeffer parity:** a week is valid with **≥ 1** clear pixel (his `na.rm` median has
  no coverage guard); **all-cloud → missing, not imputed**. We record **`valid_frac`** and run a
  **coverage sensitivity** (low-coverage weeks bias prevalence low — ~7% vs ~25%; `docs/03` §3), rather
  than silently thresholding. Retain per-lake-week **QA fields** (valid-pixel count, valid fraction,
  no-data fraction) as features + stratifiers.
- **Resolvable-area caveat.** The label reflects only pixels the sensor resolves (edges/embayments/
  narrow arms under-seen) — a representativeness limit, not an error.
- **Sensor/version.** **OLCI only** (D-21), single processing version — no cross-sensor CI trend by
  construction.
- **Ice mask: N/A for Florida** (EPA's winter no-bloom relabel is class-balancing for cold lakes; FL
  has none — skipped, noted).

---

## 5. Normalization

**Z-score per feature, fit on the TRAINING-YEARS split only** (§6), applied to the held-out test,
denormalized on inference. Persisted μ/σ are checked-in artifacts. Target log-scale not needed for the
binary AL1 label; per-lake median CI (secondary regression target, if used) is log-transformed.

---

## 6. Split, validation & leakage guards

**Temporal (held-out-year) split — PRIMARY (matches EPA; supersedes the v2 spatial split).** Train on
earlier OLCI years, evaluate on an **independent held-out recent year** (Schaeffer: 70/30 within
2017–2020 + independent 2021 test). With OLCI 2016→2026 we hold out the most recent full season(s) as
the test year and use a **forward-chaining** inner scheme for tuning. Classification cutoff tuned on
validation (their analog: 0.10).

**Why temporal, and the honest limitation.** This tests **forecasting into unseen future time** (the
real Task-B claim) and matches the benchmark's evaluation. Because the **same lakes appear in train and
test** (different years), the model can learn per-lake baselines — this is EPA's design too (per-lake
SPDE/AR1); we carry it via per-lake static features + lagged per-lake CI. Spatial holdout is **not the
primary**, but a **secondary, clearly-labeled blocked-lake stress test** (leave-one-region /
lake-size-band) is run to expose per-lake **memorization** — static morphology + BasinATLAS + lagged CI
can encode lake identity, so this is where implicit "identity leakage" would show. The **primary claim
is "known-lake forecasting into future weeks"**; wording implying transfer to *new/unseen* lakes is
**forbidden** unless the blocked-lake test supports it. An **antecedent-weather-only ablation** (no
coincident ERA5) accompanies the oracle runs so the operational gap is visible.

**Leakage checklist** (`docs/04-validation-protocol.md`): **temporal** (feature cutoff before target
week; lagged CI from pre-issue weeks; oracle-ERA5 flagged) — now primary; **normalization** train-only
(§5); **feature-selection** train-years only (§1); **target-version** single OLCI version (§4);
**circularity** chl-a ablation (§3). Hyperparameter tuning is **nested** (forward-chaining CV within
train years; one final pass on the held-out year).

**Uncertainty — clustered.** Lake-weeks are autocorrelated; report **block bootstrap / fold-level CIs**
(by lake and/or year), never row-level bootstrap.

---

## 7. Models

Four **tabular classifiers** predicting P(AL1 bloom), spanning a family spread, all explainable — and
all **feasible at full scale** now (tens of thousands of rows → **no subsampling**):

| Model | Family | Why | Explainability |
|-------|--------|-----|----------------|
| **GLM** — logistic (elastic-net) | Linear | Transparent baseline; coefficients as log-odds | Signed coefficients |
| **SVM** — SVC (RBF) | Kernel | Nonlinear reference [`ACAD-001`] | Permutation importance / PDP |
| **XGBoost** — classifier | Boosted trees | Dominant in single-site HAB studies [`ACAD-117`, `ACAD-060`] | SHAP + PDP |
| **GAM** — logistic | Additive | Distinct, highly interpretable (smooth partial effects) | Partial-dependence curves |

EPA's own **INLA** is the external benchmark, not one of our four (its Bayesian spatiotemporal machinery
is out of scope; we approximate its spatial/temporal structure with features). One classifier per
horizon (or h-as-feature — logged at modeling; `OPEN-QUESTIONS.md` Q-4).

**Explainability caveat.** SHAP/importance is associational, inflatable by autocorrelation [`ACAD-048`];
compare across models and vs literature drivers (temp, nutrients, prior CI) — never as causal.

---

## 8. Baselines, metrics & benchmark

**Baselines every model must beat, every horizon:**

- **CyAN autoregressive ladder (the leakage-control baseline).** Because the target is a threshold on
  the same CyAN product we feed as features, much near-term skill is *autocorrelation*. Build a
  CyAN-only ladder — prior bloom state, prior median CI, **lag-1/2/4 median CI**, per-lake
  climatology — and report **every fusion feature's value as its incremental lift OVER this ladder**,
  *before* any importance claim. This is the active leakage-hunt the claim gate demands.
- **Persistence — THE primary reference baseline and the common yardstick (D-28).** Carry forward the
  AL1 bloom state of the **freshest CyAN composite _actually published_ by issue time**. CyAN weekly
  composites post ~COB the Monday after the 7-day window closes → **~1-week publication latency**
  (`../data-sources/cyan/METADATA.md` §13). So for a horizon-`h` forecast of week `W` the freshest
  *available* composite is week **`W − h − 1`** — the nominal lead **plus one week of latency**, NOT
  the idealized just-closed week `W−h`. **`Persistence(W,h) = bloom(W − h − 1)`.** (This latency-aware
  form is also what separates h=0 (freshest `W−1`) from h=1 (freshest `W−2`). Daily products would cut
  latency to ~2 days — documented, tunable.) Persistence is a *strong* baseline the leading studies omitted [`ACAD-092`, `ACAD-050`] — CyAN
  autocorrelation is high, though the **honest temporal number is the within-lake AR(1) ≈ 0.66–0.73**
  (pooled 0.903 is inflated by between-lake baseline spread; `docs/03` §6). The between-lake half
  ("which lakes bloom") is carried by static lake features; the within-lake half ("when") is what a
  temporal forecast must actually predict. **Both our models AND
  the EPA forecast are reported as skill _relative to this same persistence baseline_** — the like-for-
  like question is *"who beats latency-aware persistence by more, and at what lead?"*
- **CyAN autoregressive ladder** — persistence's richer extension (lag-1/2/4 median CI + recent-bloom
  fraction + train-only climatology); fusion features must show **incremental lift over the ladder**.
- **Climatology** — per-lake week-of-year bloom rate (train-years only).
- **EPA/Schaeffer forecast** — the **federal benchmark** at **h = 1**, compared **head-to-head on the
  same Florida COMID-weeks where both exist** (the dashboard retains only ~2 recent seasons → that
  overlap is the actual bar, **not** their paper's CONUS 2017–2021 point estimates — context only) and,
  like our model, **scored as skill over the same latency-aware persistence baseline** — but using
  **EPA's own information set** (persistence cutoff = CyAN published ≤ EPA's Tue/Wed release), reported
  under **`W−1`/`W−2` sensitivity** since release timestamps aren't in the panel (Codex H2, `docs/02`
  §1). *Leakage guard:* compare **against** it and may use its lake **geometry** as the mask, but
  **never** its
  probability values as a label/feature (CyAN-derived → circular).

**Empirical baseline result (built 2026-07-02 → `outputs/cyan_baseline_eval.md`) — this reframes the
fusion bar.** On held-out test 2025 (base rate 27%): (1) absolute skill is **high but dominated by
per-lake seasonal identity, not just autocorrelation** — climatology alone hits AUC-ROC 0.955 flat,
and the CyAN ladder adds only ~+0.02–0.03 AUC-ROC over it. Across metrics the **ladder is the
strongest CyAN-only baseline** (best AUC-ROC/AUC-PR/Brier at every horizon; on MCC it ties persistence
at h0 and leads beyond). **Climatology is a strong *ranker* but weak *classifier*** — it beats
persistence on AUC-ROC by a widening margin as persistence decays, yet has the lowest MCC (≈ 0.75); it
is never the single best baseline, but its ranking strength quantifies how much of the signal is pure
seasonality. All three (persistence, climatology, ladder) are reported as explicit comparators (all
samples + transitions), and the fused model must **beat the best baseline on each metric**. (2) At short
lead the ladder **ties persistence** on operating-point metrics (h0 MCC 0.88≈0.88). (3) **On transition weeks (the flips) the
CyAN-only ladder is _anti-predictive_** (AUC-ROC 0.07→0.30 < 0.5, MCC negative at every horizon) —
being persistence-driven, it predicts the wrong direction on onsets; climatology is the only weakly
positive CyAN-only flip signal (MCC ≤ 0.15). **⇒ The fused model must show lift over BOTH the ladder
AND climatology, and the headline test is transition-week skill — not aggregate AUC** (which is
near-saturated by the circularity, D-26a).

**EPA head-to-head (built 2026-07-02, Codex-reviewed → `outputs/epa_headtohead.md`) — read with FOUR
caveats.** On shared FL 2025 COMID-weeks (4,527 lake-weeks, 132 lakes × 35 weeks; exact COMID+week
join), scoring EPA's forecast, our ladder, persistence, and climatology as predictors of **our AL1**:
EPA AUC-ROC **0.928** vs persistence 0.918, climatology 0.955, ladder 0.982. **EPA does *not* clearly
beat naive persistence** (week-block bootstrap ΔAUC +0.010, 95% CI **[−0.000, +0.022]** — includes 0);
Brier 0.101 (worst). *Caveats:* (1) **provenance** — EPA values are the **2026-07-02 dashboard
snapshot, not proven as-issued** (the view is revisable; one snapshot held); (2) **structural advantage
to us (subtle)** — our AL1 is the *same* Schaeffer/WHO AL1 concept EPA forecasts (not a different
threshold), but persistence/climatology/ladder are fit to / derived from our **exact realized labels**
while EPA's model is independent → not a clean skill test; EPA's Brier gap is *descriptive* (mean prob
0.246 vs base 0.288), not a proven definition mismatch; (3) **timing** — EPA is a current-week forecast
(released Tue/Wed, valid through Sat), and W−1/W−2 is *our* CyAN-latency sensitivity, not EPA's info
set; (4) **seasonal** — Apr–Nov only, peak-season subset (base 28.8% vs 26.6%), modest effect (FL
near-aseasonal; our baselines' AUC ≈ unchanged). **We do NOT claim to beat EPA.**

**The flips reverse the story (the fusion motivation).** On transition weeks (target ≠ persistence),
the all-samples ordering *inverts*: climatology AUC-ROC **0.551** > EPA **0.455** > our CyAN-only ladder
**0.118** (anti-predictive) > persistence 0.000. Our ladder's aggregate dominance is an **artifact of
persistence-easy weeks**; on the onsets that matter, CyAN-only is useless-to-harmful and **EPA's
weather/morphology fusion helps**. This is the empirical mandate for the fusion features: **they must
beat climatology on flips to earn their place** (§3).

**Canonical metric suite — EVERY experiment reports all of it** (enforced by
`model/metrics.py::classification_metrics`, one source of truth): **AUC-ROC, AUC-PR, Brier, MCC, F1,
Precision, Recall, Accuracy** — per horizon, vs baselines, with clustered CIs. Threshold-free (AUC-ROC/
AUC-PR/Brier) *and* operating-point (MCC/F1/Prec/Recall/Acc at a train-tuned threshold). **MCC is the
headline balanced metric** (robust to the ~23% imbalance and fair to hard classifiers like
persistence); **AUC-ROC is read with care** — a hard 0/1 baseline has a capped AUC, so it flatters soft
models (verified: at h0 persistence MCC 0.882 ties the ladder's 0.879 while AUC-ROC 0.941 vs 0.987
overstates the gap). Because the **measured FL base rate is ~23%** (built 2026-07-02, `docs/03` §6 —
~2–3× EPA's ~9–10% CONUS rate, i.e. *milder* imbalance) and lagged-CI skill decays with horizon, also
report
**PR-AUC and precision at a fixed recall** (AUC is optimistic under imbalance), **calibration /
reliability curves**, and **absolute event counts + CIs per horizon** (not just rates — h=4 is
rare-event-dominated). Prefer threshold tuning over resampling; report any SMOTE cost [`ACAD-128`]. The
tool shows a **calibrated probability with uncertainty**, not a bare class.

**Mandatory stratified diagnostics:** by season, lake size, staleness bin, cloud/no-data fraction,
in-situ join distance.

**Lake area is a headline output (D-27).** Report area's model importance + partial-dependence
**explicitly in every model** (not just as a stratifier), and interpret it: a strong/monotone area
effect is the quantified case for extending the workflow to **sub-resolvable waterbodies** (§1) — the
smaller waterbodies CyAN can't see but SePRO's customers manage. Stated as association, not causation.

---

## 9. Reproducibility & auditability

Scripted/deterministic (fixed seeds; FL pulls scripted); artifacts persisted/manifested (norm μ/σ,
split assignments, feature-availability matrix, trained models, per-run **model cards**, per-row
provenance); decisions/assumptions logged; **negative results reported plainly** (a model that doesn't
beat persistence *or* the EPA benchmark is the finding).

---

## 10. Planned documentation set

Core docs live now. Phase docs written as reached (tracked in `PROGRESS.md`):

| Doc | Phase | Contents |
|-----|-------|----------|
| `docs/01-domain-and-data.md` | Acquire | FL domain; resolvable-lakes mask + FL lake count; per-source COMID-identity pull plan; (pixel compute-gate now context). |
| `docs/02-feature-catalog.md` | Prepare | Per-lake feature catalog (CyAN mean/median/SD, morphology, ERA5, NWIS, WQP), citations, lags, (value+staleness) rules, feature-availability matrix, Task-A tests (train-years). |
| `docs/03-target-definition.md` | Prepare | AL1 label construction: per-lake median CI, **CI↔chl-a/AL1 threshold**, pixel QA/mixed-pixel mask, min-valid-pixel rule, CyAN week convention. |
| `docs/04-validation-protocol.md` | Prepare | Temporal held-out-year split, forward-chaining tuning, leakage checklist, baselines incl. EPA benchmark, metric defs, clustered CIs. |
| `docs/05-modeling-plan.md` | Model | Per-classifier config, nested tuning, calibration, explainability, model-card template. |
| `model-cards/*.md` | Model→Evaluate | Per model: config, metrics-vs-baseline+benchmark (CIs), importances, stratified diagnostics, limits. |

---

## 11. Design at a glance

```
Target:   WHO Alert Level 1 bloom (lake median chl-a >=12 ug/L, cyano-dominant), BINARY per lake-week   [OLCI only]
Unit:     resolvable LAKE x week (CyAN pixels -> per-lake mean/median/SD; authorized aggregation, D-23)
Mask:     CyAN resolvable-lakes set, filtered to Florida (COMID) = EPA benchmark's lake list
Task A:   feature inclusion via coincident (nowcast) test on TRAIN YEARS only  OR  literature precedent
Task B:   forecast P(bloom) at h=0,1,2,3,4 wk  |  ORACLE weather (coincident ERA5)  |  h=1 == EPA head-to-head
Features: CyAN mean/median/SD (+lag) + lake morphology + BasinATLAS L12 + ERA5 + NWIS + WQP
          every temporal feature = (value, staleness); chl-a is an ablation group
Norm:     z-score fit on TRAIN YEARS only; denorm on inference
Split:    TEMPORAL held-out-year (matches EPA); same lakes across years; forward-chaining tuning; cutoff ~0.10
          + secondary blocked-lake stress test (per-lake memorization); claim = "known-lake forecasting"
Features: TWO tracks — EPA-parity (CyAN+precip+watertemp+depth+area) for head-to-head; augmented (+NWIS/WQP/L12) = extension
          CyAN features are ANTECEDENT-ONLY (never target week) to avoid circularity with the CyAN-derived label
Models:   logistic GLM · SVC · XGBoost · logistic GAM  (classifiers, full-scale, no subsample)
Baselines: CyAN autoregressive ladder (lag-1/2/4 + climatology) + persistence + EPA forecast (shared FL COMID-weeks, h=1)
          -> report every fusion feature as INCREMENTAL LIFT over the ladder   [beat all, every horizon]
Metrics:  AUC/precision/recall/specificity/F1/Brier/FOR/kappa + PR curves + calibration — vs baselines, clustered CIs
Diagnostics: stratify by season/lake-size/staleness/cloud-fraction/join-distance
```
