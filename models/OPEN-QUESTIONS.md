# OPEN QUESTIONS — modeling layer

Decisions still needing resolution or user input. Each has a recommendation so work isn't blocked;
resolved items move to `DECISIONS-LOG.md`. Nothing here blocks the Acquire phase except where noted.

---

### Q-1 — Target type ✅ RESOLVED 2026-07-02 → **SUPERSEDED by D-25**
Originally continuous CI regression (D-10). **Superseded by the EPA-matching pivot (D-25):** target is
the **WHO Alert Level 1 binary bloom** (lake median chl-a ≥ 12 µg/L, cyano-dominant); models predict
P(bloom). Continuous per-lake median CI may be kept as a secondary/diagnostic regression target.

### Q-2 — 4th model: GAM or Random Forest? ✅ RESOLVED 2026-07-02 → **SUPERSEDED in practice by D-36b**
**Confirmed at the time (D-05):** the 4th model would be a **GAM**. *In practice (D-36b) the as-built
architecture grid was **logistic GLM · HistGBM · XGBoost**; SVC and GAM were not built — architecture barely
moved skill, so the three sufficed.*

### Q-3 — Bloom threshold ✅ RESOLVED 2026-07-02 (D-25)
**WHO Alert Level 1 — lake-wide median chl-a ≥ 12 µg/L with cyanobacteria dominance** (matching
EPA/Schaeffer). Exact CI↔chl-a mapping + classification cutoff pinned in `docs/03`; report sensitivity
to the mapping. (The earlier >100,000 cells/mL candidate is dropped in favor of benchmark parity.)

### Q-4 — Horizon handling: one model per horizon, or horizon-as-feature? ✅ RESOLVED
**One model per h ∈ {0,1,2,3,4}** — per-lead skill is reported cleanly across horizons in
`outputs/experiments.md` + `outputs/headtohead_onset.md` (`eval_experiments.py`).

---

**Status (2026-07-07): all Q-1…Q-7 resolved.** The bigger questions that arose mid-build are tracked in
`DECISIONS-LOG.md`, not here: fusion-vs-lean at onset → **D-41**; do the drivers help at onset → **D-39**
(no robust incremental skill; one CyAN cluster ≈ 100% of skill); climatology handling → **D-35** then
**D-42**; the Codex workflow-review limitations → **D-43**.

### Q-5 — Compute gate (pixel vs lake) ✅ RESOLVED 2026-07-02 → **SUPERSEDED by D-23**
D-22 (native pixel, feasible via columnar) is **superseded**: the EPA-matching pivot (D-23) aggregates
to **lake-level** for comparability, not compute. N drops to ≈ FL lakes × weeks (tens of thousands) —
compute is now a non-issue and all four models run at full scale. The pixel measurement in
[`docs/01`](docs/01-domain-and-data.md) remains useful context (FL water footprint ≈ 11,577 km²).

### Q-6 — Split: spatial vs temporal ✅ RESOLVED 2026-07-02 → **REVISED to temporal (D-24)**
D-20 (spatial-only) is **superseded** by the EPA-matching pivot: the split is now **temporal
(held-out-year)**, matching Schaeffer (train earlier years, independent recent test year). Same lakes
appear across years (per-lake structure carried by static features + lagged CI); cross-lake spatial
transfer is not tested here (future work).

### Q-7 — Sensor scope: OLCI-only, or include MERIS? ✅ RESOLVED 2026-07-02
**Decided (D-21): OLCI only, MERIS dropped.** Model OLCI (2016-04-24→present, ~531 weekly composites)
only; MERIS (2008–2012) excluded entirely.
