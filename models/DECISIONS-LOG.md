# DECISIONS LOG — modeling layer

Append-only. Newest entries at top. Each entry: date, decision, rationale, and (where relevant) what
it supersedes. This is the audit trail for *why* the model is built the way it is.

---

## 2026-07-02 — Codex v3 (pivot) review incorporated

Codex reviewed the pivoted v3 design; sound fixes folded into `DESIGN.md`. The headline concern was
**circularity** (the target is a threshold on the same CyAN product fed as features).

- **D-26a — CyAN autoregressive-ladder baseline + CyAN features antecedent-only.** Build a CyAN-only
  ladder (prior bloom state, lag-1/2/4 median CI, climatology); report every fusion feature as
  **incremental lift over the ladder** before any importance claim. CyAN features never include the
  target week (kills the tautology, esp. at h=0).
- **D-26b — AL1 threshold pinned from Schaeffer's deposited code before building labels.** If no
  authoritative CyAN CI→chl-a cutoff exists, label the outcome a **"Schaeffer-compatible satellite AL1
  proxy"** + threshold sensitivity; do not claim true WHO-AL1.
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

**Pre-build pins (must resolve before writing pipeline code):** (1) AL1 threshold from Schaeffer code;
(2) freeze the FL resolvable-lake list (shapefile, COMID, reconcile 2,191 vs 2,192); (3) lake-week QA
policy; (4) feature-availability matrix / temporal protocol (week convention, issue date, target
window, cutoffs, lags, staleness, oracle-only columns).

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
