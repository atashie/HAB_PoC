# Dashboard — internal decisions & known issues

Internal working notes for the Part B dashboard. Not shipped to the user-facing page. Complements the
Codex review reconciliations (`CODEX_REVIEW_dashboard.md`, `CODEX_REVIEW_updates.md`).

## Open issue — "primary model" naming: shipped is Track A (fusion), *not* fusion + explicit clim (Track B)

**Status: documented, not changed (2026-07-07). May switch models later.**

The user has referred to the primary forecaster as the **"fusion + clim" model**. What the dashboard
actually ships as the primary forecaster is **Track A**:

- **Track A (shipped as `fusion`)** = HistGradientBoosting on `TRACK_A` = CYAN + STATIC + SEASON + WEATHER +
  INSITU features. It does **not** include an explicit `clim` (per-lake-month climatology) input feature.
- **Climatology is a separate comparator line** in the UI (`clim`), a per-lake-month mean of `target_bloom`
  fit on labeled history — shown *beside* the fusion forecast, not folded into it.
- **Track B (not shipped)** would add the per-lake-month `clim` value as an extra input feature to the
  fusion model. The build code already supports a `clim` feature slot (`Xof(...)` injects it if `"clim"` is
  in the feature list), so switching would be a one-line feature-list change plus a rebuild.

**Why this matters for the claim gate:** the on-page label and README call the primary model "fusion" (Track
A), which is accurate to what runs. There is no *shipped* mislabel — the discrepancy is only between the
user's shorthand ("fusion + clim") and the shipped Track A. But if we later say "fusion + clim" anywhere
user-facing, that must trace to a model that actually ingests `clim`.

**Decision (user, 2026-07-07):** keep Track A as the shipped primary for now; document only. Revisit whether
to promote Track B (+clim feature) later. Switching would re-touch the Gate A / Gate B numbers (they are
computed on the shipped estimator), so it is a deliberate, re-benchmarked change — not a silent swap.

**If we do switch to Track B later, the checklist is:**
1. Add `"clim"` to the `TRACK_A` feature list (or define a `TRACK_B`) in `build_dashboard_data.py`.
2. Re-run the build; confirm Gate A still reproduces the published test AUC within band (or update the
   published reference in `../models/outputs/` first — coordinate with the models layer).
3. Re-report Gate B (fusion vs persistence vs onset) on 2026 with the new estimator.
4. Update README + on-page labels to "fusion + clim" only after the shipped model actually ingests `clim`.

## Resolved — "Weeks to Bloom" column renamed to "Onset lead" (2026-07-07)

Per Codex finding F2 (`CODEX_REVIEW_updates.md#2`): the column displayed the **onset horizon index (0–4)**,
not a literal calendar-week count, so "Weeks to Bloom" over-promised precise timing. Renamed the column and
its tooltips to **"Onset lead"** and clarified in the ⓘ tooltip and README that it is a *horizon index*
(lead `h` targets week `T+(h+1)`; CyAN carries ~2 weeks latency), not literal weeks. No values changed.
