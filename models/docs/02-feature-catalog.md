# 02 — Feature catalog & feature-availability matrix (Prepare, pin #4)

> The **temporal protocol** (issue time, horizons, no-look-ahead), the **feature-availability matrix**
> that enforces it, and the candidate feature catalog. This is the single source of truth that
> prevents leakage in feature construction (DESIGN §3, §6; D-26a/D-26f).

---

## 1. Temporal protocol

- **Target** = `bloom(lake, week W)` — WHO AL1, per `docs/03` (median DN ≥ 130).
- **Horizons** `h ∈ {0,1,2,3,4}` weeks. EPA's product is `h=1`.
- **CyAN is ANTECEDENT-ONLY, and latency-corrected** (D-26a, D-28). A feature may never use the target
  week's CyAN (the label is CyAN-derived → circular). Moreover CyAN weekly composites carry a **~1-week
  publication latency** (post ~COB the Monday after the window closes; `../../data-sources/cyan/
  METADATA.md` §13), so the freshest CyAN *actually available* at issue time is week **`W − h − 1`**
  (the nominal lead **+ 1 week latency**) — the model and the persistence baseline (§3, DESIGN §8) use
  the **same** freshest week, so the model never sees fresher CyAN than the baseline it must beat.
  (Daily products would cut latency to ~2 days — tunable.)
- **Issue-time convention — implementation honesty (Codex H1, round 2).** The **current assembler uses
  the weekly ALGEBRAIC form** `feature_date = target_date − 7·(h+1) days` (verified: holds for every
  row). Under the fixed **~1-week weekly-composite latency** this *equals* the publish-time cutoff
  `max(week k : publish(k) ≤ issue)` with `publish(k) ≈ COB Monday after week k's window` and issue set
  at **h full weeks before week W begins**. The algebra is exact *for the weekly product*; a general
  `publish_datetime ≤ issue_datetime` join is only needed when **mixing the daily product** or matching
  **EPA's Tue/Wed release** — deferred to the EPA head-to-head (where we run `W−1`/`W−2` sensitivity).
  The resolved cutoff week (`feature_date`) is persisted per row for audit.
- **EPA head-to-head fairness (Codex H2).** Scoring the **EPA forecast** against persistence must use
  **EPA's** information set — the CyAN composite published **≤ EPA's release** (EPA releases Tue/Wed).
  Release timestamps aren't in the panel, so this comparison is labeled **approximate** and reported
  under **both `W−1` and `W−2`** cutoffs (sensitivity), not assumed to equal ours.
- **`h=0` = coincident nowcast / diagnostic ONLY (Codex M5).** Features may use **week-W weather +
  in-situ** (observed by the end of week W) but **CyAN only ≤ W-1**. This is a **retrospective
  diagnostic** ("given this week's conditions, is it blooming?"), **not an operational issue-time
  forecast** — using week-W in-situ/weather would leak within-week info if issued before W ends. h=0 is
  **excluded from operational forecast claims**; only h≥1 are forecasts.
- **`h≥1` = forecast.** All features frozen at issue: **CyAN ≤ `W−h−1`** (latency, above), in-situ
  ≤ `W−h`; **weather = oracle week-W** (the coincident-ERA5 idealization, D-11) — reported as a
  potential-predictability upper bound, with an **antecedent-weather-only ablation** (weather ≤ `W-h`)
  to expose the operational gap.
- **(value + staleness)** for every temporal feature: `value` = last observation at/before the cutoff;
  `staleness` = time (weeks for CyAN, days for in-situ) between that observation and week W. Handles
  irregular sampling **without interpolation** (D-02).
- **Why h=0 ≠ h=1:** under antecedent-only CyAN + oracle weather they'd otherwise be identical; h=0 is
  distinguished by seeing **coincident in-situ**, h≥1 freezes in-situ at issue time.

## 2. Feature-availability matrix

For target week `W`, horizon `h`. "Freshest allowed" = the most recent week a series may be drawn from.

| Feature group | Static/temporal | Freshest allowed (h=0) | Freshest allowed (h≥1) | Staleness unit | Oracle-only | Track |
|---|---|---|---|---|---|---|
| CyAN median/mean/SD (+lag1/2/4) | temporal | `W-1` | `W−h−1` † | weeks | no | parity |
| Prior bloom state / recent-bloom frac | temporal | `W-1` | `W−h−1` † | weeks | no | parity |
| Per-lake climatology (calendar-**month** bloom rate) | derived (**train-years only**) | n/a | n/a | — | no | parity |
| Lake **surface area** (D-27), mean/max depth | static | always | always | — | no | parity |
| BasinATLAS L12 attributes | static | always | always | — | no | augmented |
| ERA5 temp / precip / solar / wind / evap / **SPEI** | temporal | `W` (coincident) | `W` (**oracle**) / `W-h` (ablation) | — | **yes** (h≥1) | parity (temp, precip) + augmented |
| NWIS discharge / stage | temporal | `W` | `W-h` | days | no | augmented |
| WQP analytes (temp, TP, TN, NH₃, **chl-a**, turb, EC, DO, pH, Secchi) | temporal | `W` | `W-h` | days | no | augmented (chl-a = ablation, D-15) |

† **CyAN latency (D-28):** freshest CyAN available at issue = week `W−h−1` (nominal lead + ~1-week
weekly-composite publication latency; `../../data-sources/cyan/METADATA.md` §13). This also cleanly
separates h=0 (freshest `W−1`) from h=1 (freshest `W−2`). The **persistence baseline uses the identical
week** (§3) so the model never sees fresher CyAN than the baseline.

**Leakage guards baked in:** climatology is **train-years-only** (target-derived → else leaks); CyAN
never uses week ≥ `W` for any horizon; oracle-weather columns are **flagged** so the ablation can drop
them; normalization μ/σ fit on train only (DESIGN §5).

## 3. The autoregressive-ladder baseline block (D-26a)

**Persistence** `= bloom(W − h − 1)` is the **primary reference baseline** (DESIGN §8, D-28): carry the
freshest *published* CyAN bloom state (latency-corrected, above) forward to the target. It is the
simplest rung of the ladder; **both our models and the EPA forecast are scored as skill over it.** The
full **leakage-control ladder** every fusion feature must beat on *incremental lift* is CyAN-only,
computed at the issue week and paired to the target by horizon:

- `cyan_median` (freshest), `cyan_mean`, `cyan_sd`
- `cyan_median_lag1 / lag2 / lag4` (+ `cyan_mean_lag1`, `cyan_sd_lag1`)
- `bloom_state` (bloom at the freshest week), `bloom_roll4` (mean bloom over the prior *valid* weeks)
  + `bloom_roll4_n` (how many of the 4 prior weeks were valid — exposes the denominator; Codex M4)
- `cyan_gap_weeks_at_cutoff` (weeks since the last valid CyAN median at the cutoff — cloud gaps). **NOT
  target-relative** (Codex M3): target-relative staleness = this **+ 7·(h+1) days**, added by the
  horizon assembler.
- `n_inside`, `n_valid`, `valid_frac`, `nodata_frac` (QA quality of the freshest CyAN read; `valid_frac`
  drives the coverage sensitivity, `docs/03` §3)
- **climatology** (per-lake **calendar-month** bloom rate; month chosen over week-of-year for
  stability — ~12 cells/lake vs 52, Codex M4) — **added at split time on train years only**

**Assembler leakage tests — REQUIRED (Codex H4).** The latency guard currently lives only in this doc;
the horizon assembler (Phase 2, not yet built) must enforce it in code. Mandatory unit tests: for every
horizon `h`, assert the paired CyAN-feature/persistence cutoff week satisfies
`feature_start_date == target_start_date − 7·(h+1) days`; and **persist the resolved cutoff week per
modeling row** so any prediction's information set is auditable.

## 4. Two feature tracks (D-26c)

- **EPA-parity set** (head-to-head only): CyAN (median/mean/SD + lags) + **precipitation** + **water-
  surface-temperature** + **lake depth** + **surface area**.
- **Augmented SePRO set** (extension): parity **+** full ERA5 (SPEI, wind, solar, evap) + NWIS + WQP +
  BasinATLAS L12.

## 5. Build status

- ✅ **CyAN antecedent feature block** (`prepare/build_cyan_features.py` → `data/derived/
  cyan_features_fl.parquet`) — the §3 ladder, from `cyan_lake_weekly_fl.parquet`. Antecedent-only;
  climatology deferred to split time.
- ✅ **Lake area / static morphology** — `area_sqkm` rides along; depth join pending source (LakeCat/NHD).
- ✅ **ERA5 join** — weather features computed + joined; **133/133 lakes** (`feature_significance_weather.md`).
- ✅ **NWIS / WQP** — COMID/NLDI joins + (value, staleness) done; **NWIS 25/133, WQP 123/133** lakes.
- ✅ **BasinATLAS L12** — max-overlap L12 join, **133/133** lakes. All four folded into `modeling_table_fusion_fl.parquet`
  (339,400×58). *(Known limitation, D-43 #2/#5: for h≥1 the non-CyAN blocks join one week stale, and in-situ values are
  forward-filled without a staleness cap — deferred to next rerun.)*
