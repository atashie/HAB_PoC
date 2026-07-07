# Part B tool — Florida HAB Risk & State dashboard

A small, self-contained **interactive dashboard** for a non-technical SePRO user (field specialist or
customer). One page, two tabs, reading **precomputed** predictions — no server, no live compute. It draws
directly on the Part A modeling layer (`../models/`). Design doc:
[`../docs/plans/2026-07-06-dashboard-design.md`](../docs/plans/2026-07-06-dashboard-design.md).

**It is a dated demonstration on a fixed real snapshot — not a live operational feed** (labeled as such on
every view). Nothing is live-pulled; nothing is fabricated; every number regenerates from checked-in code.

## Preview it now (no tools needed)

**Double-click `index.html`** — it opens in your browser and works fully offline (geometry and data are
loaded as local JS, not fetched). No install, no server.

## The two tabs

- **Alerts** — map left, ranked list right.
  - *New-bloom risk*: lakes **clear now** ranked by forecast probability of a WHO Alert-Level-1 bloom, with
    a forecast-target-week selector. Each row also shows an **Onset lead** column — the earliest forecast
    horizon (0–4) at which risk first reaches the Warning line, or "–" if none. (It is a *horizon index*, not a
    literal week count: lead `h` targets week `T+(h+1)` and CyAN carries ~2 weeks latency.) Risk tiers
    (Watch/Warning) are **illustrative and tunable**.
  - *Current active blooms*: lakes **blooming now**, ranked by duration (consecutive observed bloom weeks).
- **Deep dive** — pick a lake: forecast risk by target week (our fusion vs the lean CyAN model [median+area] vs climatology vs
  EPA); observed history (CyAN index + WHO AL1 line + real in-situ chl-a samples, both axes pinned to a
  common 0 baseline); where we disagree with climatology / EPA; **collapsible** current feature values by
  family (with staleness); a single **sortable, scrollable fleet table** (all lakes × Δ-vs-clim, Δ-vs-EPA,
  our %) **beside an explorer map** that shades all lakes by any selected forecast or feature; and an
  external link to FL DEP. *(Season features are deliberately excluded from the feature panel —
  `woy_sin/cos` encode the **target week's** calendar position, not a current lake condition.)*

**Both maps** offer a basemap toggle: **Political (light)** — an offline state-outline vector (default, always
works) — or **Satellite (optical)** — Esri World Imagery tiles (needs internet).

## What the numbers are (and are not)

- Forecasts (ours **and** the EPA's) are **probabilities of an AL1 bloom (0–100%)**, *not* a chlorophyll
  concentration. Observed "levels" are the **satellite CyAN index** (0–255, dense) plus **sparse in-situ
  chlorophyll-a** grab samples (real WQP measurements). No invented CyAN→chl-a conversion.
- **AL1 = median CyAN index ≥ 130 ≈ 12 µg/L chl-a** (EPA/Schaeffer operationalization; CyAN index↔chl-a is approximate).
- Disagreements are hypotheses, not proof — **correlation ≠ causation**.

## Rebuild the data — `build_dashboard_data.py`

Deterministic (seed 42), reuses the **exact** estimator code from `../models/model/eval_fusion.py` and
`eval_headtohead_onset.py`. Fits a **separate per-horizon** fusion (HistGradientBoosting, TRACK_A),
lean CyAN model (LogReg on cyan_median+area_sqkm — the optimal 2-feature model per the greedy ablation),
and climatology on labeled history (≤ 2025) — matching `eval_fusion`'s per-horizon
protocol (a pooled all-horizon model gives near-flat, sometimes badly-wrong curves because features at a
fixed cutoff are horizon-invariant). Scores the freshest full forecast (cutoff **2026-05-17**, horizons 0–4);
attaches the EPA `percent_chance`; drops **non-physical** raw in-situ readings; computes disagreement deltas,
current bloom state + duration, current features by family, and observed CyAN/chl-a history. Emits:

| Output | What |
|--------|------|
| `data/dashboard_data.js` | `window.DASH` — meta (snapshot dates, provenance, thresholds, both gates) + per-lake forecast/state/features/history |
| `data/geo.js` | `window.FL_LAKES` / `window.FL_STATES` — lake polygons + state basemap as JS globals (so the page works from `file://`) |

```bash
python dashboard/build_dashboard_data.py
```
Requires `pandas`, `numpy`, `scikit-learn`, `pyarrow`. **Two gates:** *Gate A* (consistency) reproduces the
published fusion 1-week test AUC (**0.983**, matching `../models/outputs/fusion_eval.md`) and refuses to write
if it drifts; *Gate B* (shipped-model validity) scores the **shipped per-horizon** fusion on the genuinely
held-out 2026 period (`oos_partial`) **always beside its baseline**: fusion AUC 0.99→0.98 but **persistence alone
0.95→0.90** — the overall AUC is autocorrelation-dominated and is *not* the result. The honest, fusion-specific
signal is **onset-AUC on new blooms** (fusion 0.96→0.93, where persistence has zero skill by construction). This
matches the project's documented AR-dominance finding; there is no leakage (verified: persistence baseline high,
recipe reproduces the published 2025 curve, 2026 only marginally easier).

**Fidelity caveats baked into the UI** (from Codex accuracy reviews, `CODEX_REVIEW_dashboard.md` /
`CODEX_REVIEW_updates.md`): forecasts are point estimates ("tiers near a threshold are not sharply separable",
in the alert-list ⓘ tooltip); **h0 labelled a diagnostic
nowcast**; the **EPA** comparator is each target week's percent-chance from a *later* snapshot (fair at short
leads, favourable to EPA further out); the observed-history chart marks the **issue cutoff** (post-cutoff data
shaded); in-situ values are flagged **raw/unharmonized**; and lakes missing a horizon are **counted, not silently
dropped**.

## Deploy to Vercel (static, from GitHub)

The repo is already at `github.com/atashie/HAB_PoC`. The dashboard is a **static site** — Vercel just serves
the `dashboard/` folder (no build step, no backend).

1. Commit & push the `dashboard/` folder to GitHub (Claude can do this on request).
2. Go to **vercel.com** → sign in **with the GitHub account that owns the repo** (`atashie`).
3. **Add New… → Project** → import **`atashie/HAB_PoC`**.
4. In the import screen set **Root Directory = `dashboard`**. Framework preset: **Other** (it's static).
   Leave Build Command empty; Output Directory = `.` (or leave default).
5. **Deploy.** Vercel returns a URL like `https://hab-poc-xxxx.vercel.app`. Every future `git push`
   auto-redeploys.

(Alternative, equally free: GitHub Pages. Vercel is chosen here per prior preference.)

## Files

```
dashboard/
  index.html                 # THE TOOL — open in a browser (two tabs)
  build_dashboard_data.py    # deterministic data build (reuses ../models estimator code)
  vendor/                    # Leaflet + Plotly (vendored; no CDN)
  data/
    dashboard_data.js        # generated: window.DASH (forecasts, state, features, history, fleet)
    geo.js                   # generated: window.FL_LAKES / window.FL_STATES
  README.md
```

## Fidelity / provenance

Snapshot dated on every view; forecasts labeled AL1-risk (not chl-a); EPA shown with its current-week-nowcast
caveat; risk tiers labeled illustrative; FL DEP labeled external / not processed by us. The page **footer** carries a
high-level "provisional PoC" description; the **full provenance and both gate results** live in `window.DASH.meta`
(emitted by `build_dashboard_data.py`) and in this README. Every figure traces to
`build_dashboard_data.py` → `../models/data/derived/*` and `../models/outputs/*.md`.
