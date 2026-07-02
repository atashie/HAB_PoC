# PROGRESS — modeling layer

Living tracker across the DS arc (define → acquire → prepare → explore → model → evaluate →
communicate). Update the status column and check items as work lands. `[ ]` todo · `[~]` in progress
· `[x]` done · `[!]` blocked. Newest status note at the top of the log.

**Current front line:** DEFINE complete; **ACQUIRE next** (fresh Florida pulls + compute-gate
estimate).

---

## Phase status

| Phase | Status | Key output |
|-------|--------|-----------|
| 0 · Define & design | `[x]` done | `DESIGN.md`, `DECISIONS-LOG.md`, this scaffold |
| 1 · Acquire (Florida) | `[~]` in progress | domain + compute-gate done (`docs/01`); fresh pulls next |
| 2 · Prepare | `[ ]` todo | fused pixel-week table + `docs/02/03/04` |
| 3 · Explore / feature assessment (Task A) | `[ ]` todo | coincident inclusion tests + feature catalog results |
| 4 · Model (Task B) | `[ ]` todo | logistic GLM/SVC/XGBoost/logistic GAM classifiers, multi-horizon + `model-cards/` |
| 5 · Evaluate | `[ ]` todo | skill-vs-lead-time vs baselines, event-based skill, leakage gap |
| 6 · Communicate | `[ ]` todo | figures/tables feeding the tool + slides |

---

## Phase 0 — Define & design `[x]`

- [x] Clarify target/unit/split/models with user (4-question round, 2026-07-02)
- [x] Pull commonly-used features + validation practice from `../Research/` (cited)
- [x] Write `DESIGN.md` (framing, unit, features, split, models, baselines, metrics, leakage guards)
- [x] Write `DECISIONS-LOG.md` (D-01…D-09, W-01, assumptions)
- [x] Write `README.md`, `PROGRESS.md`, `OPEN-QUESTIONS.md`
- [x] Codex adversarial review of the plan → sound fixes folded into `DESIGN.md` v2 (D-11…D-19)
- [x] Resolve blocking `OPEN-QUESTIONS.md` — Q-1/Q-2/Q-6/Q-7 done (Q-3/Q-4/Q-5 are phase-deferred)

## Phase 1 — Acquire (Florida) `[~]`

- [x] Define Florida domain: extent (Census FL polygon, EPSG:5070), POR (OLCI 531 wks), CyAN coverage
      in FL (≈128,628 water px ≈11,577 km²) → `docs/01-domain-and-data.md`
- [x] **Compute-gate estimate** (`acquire/compute_gate_estimate.py`): ≈68.3 M rows; dense monolith
      unsafe → partitioned columnar; **native-pixel viable, no lake fallback** (D-22)
- [ ] Obtain CyAN **resolvable-lakes** shapefile → FL lake mask (COMID); confirm FL lake count
- [ ] Per-lake weekly CyAN **mean/median/SD** (OLCI) + **WHO AL1** target construction
- [ ] ERA5 FL subset (coincident + antecedent windows)
- [ ] NWIS FL gages (discharge/stage)
- [ ] WQP FL stations (nutrients, temp, chl-a, turbidity, EC, DO, pH, Secchi)
- [ ] BasinATLAS L12 attributes for FL sub-basins (from `bchars_intersected12.csv` / gdb on `D:`)
- [ ] Write `docs/01-domain-and-data.md` (extents, params, join keys, cost estimate, gate outcome)

## Phase 2 — Prepare `[ ]`

**PRE-BUILD PINS (resolve before writing pipeline code — Codex v3 review, D-26):**
- [ ] **AL1 threshold** from Schaeffer's deposited code (`compile_data.R`/`cyan_processing_conus.R`);
      else label "Schaeffer-compatible AL1 proxy" + sensitivity → `docs/03`
- [ ] **Freeze FL lake list** from the CyAN resolvable-lakes shapefile (COMID; reconcile 2,191 vs 2,192)
- [ ] **Lake-week QA policy** (min valid pixels/fraction, mixed/edge mask, missing-not-imputed)
- [ ] **Feature-availability matrix / temporal protocol** (week convention CyAN first-Sunday / EPA
      Saturday, issue date, target window, cutoffs, lags, staleness, oracle-only cols) → `docs/02`

- [ ] Target construction: per-lake mean/median/SD (OLCI), AL1 label, QA/masking → `docs/03`
- [ ] Feature assembly (value + staleness); **two tracks** (EPA-parity vs augmented); CyAN antecedent-only
- [ ] COMID identity joins (WQP/NARS/NWIS/LakeCat) → NLDI/HUC/nearest fallback + distance windows
- [ ] Temporal held-out-year split (+ **secondary blocked-lake** stress test); z-score fit on train only
- [ ] Leakage checklist run (temporal/circularity/normalization/feature-selection/version)

## Phase 3 — Feature assessment / Task A `[ ]`

- [ ] Coincident non-random-distribution test per non-literature candidate (with correction)
- [ ] Finalize included feature set (literature-precedent + passed-test), log outcomes (no cherry-pick)

## Phase 4 — Model / Task B `[ ]`

- [ ] Baselines: **CyAN autoregressive ladder** + persistence + climatology + **EPA forecast (shared FL
      COMID-weeks, h=1)**, per horizon
- [ ] Classifiers: logistic GLM · SVC · XGBoost · logistic GAM — one per horizon (or h-as-feature; log choice)
- [ ] Explainability: **incremental lift over the ladder** first; then coefficients / SHAP / PDP vs literature
- [ ] Write `docs/05-modeling-plan.md` + `model-cards/`

## Phase 5 — Evaluate `[ ]`

- [ ] Skill-vs-lead-time curve, all models vs baselines, with clustered CIs
- [ ] Classification skill per horizon: AUC + **PR-AUC / precision@recall / calibration / event counts**
- [ ] EPA head-to-head on shared FL COMID-weeks; secondary blocked-lake stress test reported
- [ ] Honest limitations write-up (oracle-weather, circularity/ladder lift, known-lake-only, AL1 proxy)

## Phase 6 — Communicate `[ ]`

- [ ] Figures/tables that feed Part B (tool) and Part A (slides)

---

## Status log (newest first)

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
