# Code Map — the operational lean model (`ex-operational-poc/`)

> A **simple, self-contained** map of the one workflow that delivers the operational
> forecaster: the **lean 2-feature model** (`cyan_median` + `area_sqkm`) that predicts WHO
> Alert-Level-1 cyanobacteria blooms for Florida lakes, 0–4 weeks ahead. It lives in
> [`ex-operational-poc/`](ex-operational-poc/) and depends on nothing else in the repo at
> runtime except the cached CyAN rasters and the Florida lakes layer.
>
> This is the deliberately-minimal counterpart to the full [`CODE-MAP.md`](CODE-MAP.md): the
> broader study already showed this 2-feature model is the right operational choice, so here
> we build *only* it, and *only* the data it needs. The section that matters most is
> [§4 — avoiding autoregressive leakage](#4-avoiding-autoregressive-leakage-the-essential-part).

---

## 1. The workflow at a glance

Five numbered scripts, run in order. Each does one thing and hands a file to the next.

```mermaid
flowchart LR
    subgraph inputs["Inputs (real, public)"]
        RAS["CyAN weekly OLCI mosaics<br/>(satellite index, EPSG:5070)"]
        LK["FL resolvable lakes<br/>(polygons + area_sqkm)"]
    end
    S1["01_ingest.py<br/>verify / download inputs"]
    S2["02_prepare.py<br/>rasters -> per-lake median + AL1 label"]
    LW["data/lake_week.parquet<br/>comid, week, cyan_median, bloom, area"]
    S3["03_train.py<br/>fit LogReg per horizon, tune threshold on val"]
    MJ["outputs/models.json<br/>readable coefficients"]
    S4["04_evaluate.py<br/>held-out test vs baselines + CIs"]
    S5["05_predict.py<br/>refit on all history, score latest week"]
    EV["outputs/eval_metrics.md"]
    PR["outputs/predictions.csv + summary"]

    RAS --> S1 --> S2
    LK --> S1
    S2 --> LW --> S3 --> MJ
    LW --> S4
    MJ --> S4 --> EV
    LW --> S5
    S5 --> PR
    CORE["common.py<br/>leakage-safe alignment · split · scoring · metrics"]
    CORE -. used by .-> S2
    CORE -. used by .-> S3
    CORE -. used by .-> S4
    CORE -. used by .-> S5
```

Everything routes through **`common.py`**, the small tested core, so the one piece of
logic that must be correct (the leakage-safe alignment) exists in exactly one place.

---

## 2. The five steps

| Step | Script | Reads | Writes | What it does |
|------|--------|-------|--------|--------------|
| 1 · ingest | `01_ingest.py` | CyAN cache, FL lakes | — | Verify both inputs are present and the weekly series is complete (flag any gaps); if the cache is empty, direct you to the repo's cited CyAN pull (`data-sources/cyan`). |
| 2 · prepare | `02_prepare.py` | CyAN rasters, FL lakes | `data/lake_week.parquet` | Rasterize the 133 lakes once over a FL window; per week, take each lake's **median DN** over valid pixels; label **bloom = median ≥ 130**. |
| 3 · train | `03_train.py` | `lake_week.parquet` | `outputs/models.json` | Per horizon: leakage-safe align → temporal split → fit LogReg on **train**, tune threshold on **val**. |
| 4 · evaluate | `04_evaluate.py` | panel + `models.json` | `outputs/eval_metrics.md` | Score the held-out **test** period vs persistence + climatology, with block-bootstrap CIs. |
| 5 · predict | `05_predict.py` | panel + `models.json` | `outputs/predictions.csv` (+ summary) | Refit each horizon on **all** labelled history; score each lake's freshest CyAN → AL1 risk for target week = latest CyAN week + (h+1). |

`config.py` holds every path, threshold (`AL1_THRESHOLD = 130`), split boundary
(`TRAIN_END`, `VAL_END`), and the feature list — one place to change anything.

---

## 3. The model

- **Features (2, that's all):** `cyan_median` (the lake's antecedent median CyAN index) and
  `area_sqkm` (static lake area).
- **Target:** `bloom` = per-lake weekly median CyAN DN ≥ 130 = WHO Alert Level 1 (~12 µg/L
  chlorophyll-a; the EPA/Schaeffer operationalization).
- **Architecture:** standardized **logistic regression**, one model per horizon `h ∈ {0..4}`.
  Fit with scikit-learn, but persisted as plain **coefficients** in `models.json` and scored
  by a 3-line function (`common.logreg_score`) — fully readable, no pickle.
- **Split:** purely temporal — train `< 2022-07`, val `[2022-07, 2024-07)`, test `≥ 2024-07`.
  Never random (lake-weeks are autocorrelated).

---

## 4. Avoiding autoregressive leakage (the essential part)

This model is **autoregressive**: it predicts a threshold on the CyAN median using the CyAN
median from an earlier week. That is legitimate *only* if the feature can never peek at (or
past) the week being forecast. Two rules enforce it.

**The timeline for a horizon-`h` forecast of week `W`:**

```mermaid
flowchart LR
    F["feature week<br/>W - h - 1<br/>cyan_median observed"] -->|"at least h+1 weeks earlier"| I["issue time<br/>forecast made"]
    I -->|"CyAN ~1-week<br/>publication latency"| T["target week W<br/>bloom = median ≥ 130<br/>UNKNOWN at issue"]
```

1. **Antecedent-only + latency.** The feature is taken from week **`W − (h+1)`**, never `W`.
   The `+1` is CyAN's ~1-week publication latency: the freshest composite actually *available*
   when the forecast is issued is one week behind the nominal lead. Using week `W`'s CyAN would
   be circular — "predicting" a threshold on a number from that same number.
2. **Freshest-available, gap-safe.** If week `W − (h+1)` is missing (cloud), we fall back to the
   most recent composite *at or before* that cutoff — the honest "what you'd really have on the
   day" — via a **backward as-of join**. We never reach forward.

**Where it lives (one function):** `common.build_horizon_frame(panel, h)` computes
`cutoff = target_date − (h+1) weeks`, does a `merge_asof(direction="backward")` per lake, and
then **hard-asserts** that every matched feature week is `≤ target − (h+1) weeks`. A leak is a
crash, not a silent bug. The `persistence` baseline is the label carried from that same feature
week, so it is latency-aware by construction.

**Other leakage guards in the same spirit:**

| Guard | Where |
|-------|-------|
| No random shuffling of autocorrelated weeks | `common.temporal_split` (split by date only) |
| Threshold tuned on **validation**, never test | `03_train.py` → `common.best_f1_threshold` |
| Climatology baseline fit on **train+val only** | `04_evaluate.py` → `common.climatology_lookup` |
| CIs bootstrap **whole lakes**, not rows | `common.block_bootstrap_auc_ci` |
| Single sensor (OLCI), so no cross-sensor jump | `01/02` filter to the `L` prefix |

**Tested:** `tests/test_common.py` asserts the feature week is exactly `(h+1)` weeks back on a
clean panel, is never within `(h+1)` weeks of the target, falls back to an *older* week across a
gap (never a newer one), and that persistence equals the feature-week label. 9 tests, all green.

---

## 5. Results (held-out test, real)

Full three-table breakdown (all-sample AUC, onset-AUC, and MCC — each with its baselines) is in
`outputs/eval_metrics.md`, regenerated by `04_evaluate.py`. Base rate ≈ **0.267 on the test window**
(0.233 over the full panel — the target rate drifts up over the record). The decision-relevant
metric is **onset-AUC** (early warning on currently-clear lakes); both the model and the baseline
that beats it carry CIs:

| h | onset base rate | lean onset-AUC [95% CI] | climatology onset-AUC [95% CI] |
|--:|--:|--|--|
| 0 | 0.029 | 0.836 [0.781, 0.881] | 0.851 [0.810, 0.889] |
| 1 | 0.040 | 0.804 [0.756, 0.847] | 0.863 [0.823, 0.901] |
| 2 | 0.048 | 0.774 [0.717, 0.821] | 0.866 [0.825, 0.904] |
| 3 | 0.055 | 0.765 [0.712, 0.809] | 0.875 [0.832, 0.914] |
| 4 | 0.059 | 0.752 [0.700, 0.797] | 0.884 [0.844, 0.919] |

**Reading it honestly.** All-sample AUC (0.98→0.94) is high but **autocorrelation-dominated** —
persistence scores nearly as well, so it is not the result — and at the MCC operating point
**persistence ties the lean model** (0.85 vs 0.85 at h1). On the decision-relevant **onset-AUC**, the
lean model has genuine early-warning skill, but a per-lake seasonal **climatology — itself only a
baseline — is competitive-to-better**: tied at short lead (CIs overlap at h0/h1), clearly ahead from
h2 on (CIs separate). Part of that is **structural** — climatology depends only on the target week's
calendar position, so it is horizon-invariant and pays no lead-time penalty, while the lean model's
real-time feature goes stale. So this 2-feature model's value is **simplicity + explainability while
staying competitive**, not beating every baseline; the richer real-time-CyAN ladder in
[`models/`](models/RESULTS-SUMMARY.md) is what pushes onset skill higher. The label is a satellite
realization, not toxin. Correlation, not causation.

---

## 6. Run it

```bash
cd ex-operational-poc
pip install -r requirements.txt
python 01_ingest.py && python 02_prepare.py && python 03_train.py \
  && python 04_evaluate.py && python 05_predict.py
python -m pytest tests/
```

Deterministic on a fixed environment (seed 42); runs against the CyAN rasters already cached in the
repo. The reported metrics (3 decimals) are stable across platforms; raw LogReg coefficients in
`models.json` can differ in the last decimals across BLAS builds, well below that. See
[`ex-operational-poc/README.md`](ex-operational-poc/README.md) for the file-by-file rundown.

---

*Companion maps: [`ARCHITECTURE.md`](ARCHITECTURE.md) (repo structure) ·
[`CODE-MAP.md`](CODE-MAP.md) (the full codebase) · [`README.md`](README.md) (product overview).*
