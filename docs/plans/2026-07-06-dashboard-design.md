# Part B tool — two-tab HAB dashboard (design)

**Date:** 2026-07-06 · **Status:** approved, building · **Owner:** Arik + Claude
**Deploy target:** Vercel (personal account, arik.tash@gmail.com), static site from `github.com/atashie/HAB_PoC`, Root Directory = `dashboard/`.

## What this is

The Part B deliverable: a small, working, interactive tool for a **non-technical SePRO user**
(field/technical specialist or customer). One page, two tabs, reading **precomputed** predictions —
no server, no live compute. It draws directly on the Part A modeling layer (`models/`).

It is a **dated demonstration on a fixed real snapshot**, not a live operational feed — labeled as such
everywhere (claim gate). Nothing is live-pulled; nothing is fabricated.

## The two forks we resolved with the user

1. **"Levels" = risk %, not chl-a.** Our model and the EPA forecast both output a **probability of a WHO
   Alert-Level-1 bloom**, not a chlorophyll concentration. So forecasts are shown as **risk 0–100%**;
   observed history is shown as the **CyAN index** (dense) + **sparse in-situ chl-a** (real WQP samples).
   No invented CyAN→chl-a conversion.
2. **Fixed, dated snapshot** — not live.
3. **FL DEP** (floridadep.gov/AlgalBloom) = **external link**, clearly labeled "not processed by us."

## Data snapshot (grounded in the real pipeline)

Source: `models/data/derived/modeling_table_fusion_fl.parquet` (133 lakes, horizons 0–4, through
2026-06-21) + `cyan_lake_weekly_fl.parquet` (observed weekly) + EPA snapshot
`data-sources/cyano-forecasts/.../allweeks_20260702T000000Z.csv` + `presentation/data/fl_lakes.geojson`.

- **Horizon semantics:** at feature cutoff `T`, horizon `h` targets week `T + (h+1) weeks`.
- **Forecast anchor = cutoff 2026-05-17** — the latest cutoff carrying a full h0–h4 forecast (targets
  2026-05-24 → 2026-06-21). At h=1: 84 lakes clear, 41 blooming.
- **Current-blooms anchor = freshest observed week per lake** (through ~2026-06-21).
- Each view is dated for exactly what it shows.

## Data build — `dashboard/build_dashboard_data.py`

Deterministic, seeded (42), reuses the **exact** model code from `models/model/eval_fusion.py` and
`eval_headtohead_onset.py` (same features, same estimators). Steps:

1. Fit **fusion** (HistGradientBoosting, TRACK_A features), **CyAN-ladder** (LogReg pipeline, CYAN+clim),
   **climatology** LUT — on labeled history (splits train+val+test, target ≤ 2025-12-28).
2. Score the **forecast-anchor** rows (oos_partial @ cutoff 2026-05-17, h0–4): fusion prob, ladder prob,
   climatology prob per lake × horizon. No leakage (scored rows held out of fit).
3. Attach **EPA** `percent_chance` matched by comid × target-week (current-week nowcast, held across h).
4. **Disagreement** deltas per lake × horizon: fusion − climatology, fusion − EPA.
5. **Current bloom state + duration** per lake from the observed weekly table (consecutive bloom weeks).
6. **Current features by family** (CyAN / catchment / weather / in-situ) at the anchor, with staleness.
7. **Observed history** per lake: weekly CyAN index (dense) + in-situ chl-a samples (sparse).
8. Emit `dashboard/data/dashboard_data.js` (`window.DASH = {...}`) + provenance/data-dictionary.
9. **Verification gate:** separately reproduce the eval protocol (fit train+val → predict test) and assert
   fusion h=1 test AUC matches `fusion_eval.md` (~0.98); print PASS/FAIL. Consistency with published numbers.

Risk tiers (illustrative, tunable, exposed as constants): **Watch ≥ 0.20**, **Warning ≥ 0.40**
(base rate ≈ 0.23). Labeled as illustrative, not an operational cutoff.

## Frontend — `dashboard/index.html` (standalone, vendored Leaflet + Plotly)

**Tab 1 — Alerts (simple).** Map left / list right. Sub-toggle `New-bloom risk` ⇄ `Current active blooms`;
horizon selector 1–4 (default 1) on the risk view.
- *New-bloom risk:* only currently-clear lakes eligible; map colored by risk tier; list ranked by forecast
  probability. Currently-blooming lakes greyed (can't have a *new* bloom).
- *Current active blooms:* lakes blooming now, ranked by duration (weeks).
- Click a lake → highlight + risk-by-horizon readout.

**Tab 2 — Deep dive (all raw data).** Lake selector, then panels:
- Forecast risk % by horizon — ours vs EPA vs climatology.
- Observed history — CyAN index line + in-situ chl-a dots + AL1 threshold.
- Current features by family — with staleness flags.
- Disagreement — ours − climatology and ours − EPA by horizon; plus a fleet view of the biggest
  disagreements.
- Ancillary — labeled external link to FL DEP.

## Fidelity rails

Snapshot/date banners on every view; forecasts labeled AL1-risk not chl-a; EPA shown with current-week
caveat; drivers correlational (correlation ≠ causation); risk tiers labeled illustrative; FL DEP external;
every number regenerates from `build_dashboard_data.py`, which reproduces the eval numbers as a gate.

## Deploy (Vercel, static)

Repo already at `github.com/atashie/HAB_PoC`. Import into Vercel (personal account) → Root Directory
`dashboard` → no build step (static) → auto-redeploys on push. Alternative: GitHub Pages. A 6-line
click-by-click ships with Phase 4.

## Phases

1. `build_dashboard_data.py` + verification gate.
2. Static shell + Tab 1 (Alerts).
3. Tab 2 (Deep dive).
4. Fidelity polish + `dashboard/README.md` + Vercel steps; branch/commit when the user approves.
