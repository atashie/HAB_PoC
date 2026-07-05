# Forecast-ensemble weather features (Florida HAB PoC) — design

**Date:** 2026-07-05 · **Status:** design, Codex-reviewed (7 findings folded in), ready to implement.
**Owner layer:** `../../data-sources/weather/` · registry rows `era5` + `ecmwf_fc` ·
decisions log 2026-07-05 (session 14). **Sister workstream** handles the CyAN fusion — **not here**.

## Goal (one line)

Produce the **same 22 algal-growth weather features** we already have for ERA5 history, but for the
**forecast horizon (~15 days) as a 51-member ECMWF ensemble** — one daily feature series per member,
computed on a stitched *history + forecast* series so the **memory features (SPEI-1/2/4/6, trailing
precip/GDD/solar/wind) are correct** at the seam.

## Why this is non-trivial

Several features have memory: SPEI-6 needs a 180-day trailing water balance; trailing windows span
7–90 days. So a member's forecast features cannot be computed from the forecast alone — each member's
series must be **`recent ERA5 history + that member's forecast`**, run through the **identical** feature
code, then sliced to the forecast days. Two products meet at the seam (ERA5 reanalysis vs IFS forecast),
and ERA5 is stale (~5 d) while open-data forecasts are retained only ~2 d — so there is also a **gap** to
bridge between the history frontier and the forecast's T0.

## Confirmed scope & decisions (user-approved — settled, not reopened)

1. **Thin PoC demo.** One latest ENS run, **all 51 members**, full pipeline end-to-end.
   **Parameterized + documented** so a new run = re-run one command (no new code per run).
2. **Gap handling.** Refresh ERA5T to advance the frontier to ~now−5 → fill the recent ~2 days with the
   **oldest still-retained forecast run's** short leads → interpolate the residual ~3-day sub-gap:
   **linear for temp/solar/wind; climatological median (per cell, per day-of-year) for precip — never
   linear-interpolate precip.**
3. **Seam bias.** **Raw stitch, no bias correction.** ERA5 and IFS share the 0.25° grid but are
   different products; a seam discontinuity is expected and **documented as a bounded limitation**
   (proper fix = quantile-mapping against reforecasts, which open-data lacks → future work).

## Core principle — reuse the exact feature code with a FROZEN climatology

The forecast features must be computed **identically** to the historical features or they aren't
comparable. Refactor `derive/features.py` into two hard-separated callables:

- **`fit_climatology(era5_daily) -> params`** — the per-calendar-month Pearson-III SPEI parameters
  (`{scale, month, lat, lon, mean, std, skew, cal_years, input_hash}`), fit **once on ERA5 2016–2025**
  and **serialized/frozen**.
- **`apply_features(daily_series, params) -> 22 features`** — trailing windows, Hargreaves PET, GDD, and
  the **frozen** SPEI standardization, applied to any daily series (history or stitched forecast).
  **`apply_features` has NO fitting branch** — it *errors* if `params` is missing. This is what makes the
  frozen-climatology leakage-safety *enforceable*, not merely intended: the forecast path physically
  cannot re-fit SPEI on stitched data that contains forecast days.

GDD base (10 °C), trailing windows, calm threshold are fixed constants already — no fitting.

## Build order — Phase 0 is a hard gate

### Phase 0 — Refactor + golden regression gate (NO forecast code until this passes)

*Codex #3, #5.* Refactoring `features.py` risks silently changing our already-validated historical
product (leap-day grouping, NaN handling, skew, clipping, dtype, calendar selection). Gate:

- Golden test: run **old `build_features()`** and **new `apply_features(load_daily(), fit_climatology(load_daily()))`**
  on the same ERA5 input; **assert equality on all 22 variables** (tight numeric tolerance; data values,
  not attrs). Store climatology params with a hash; assert historical `spei_*` reproduces the current
  NetCDF within tolerance.
- Leakage-enforcement test: appending absurd values to the tail of a series changes forecast SPEI **only
  through the trailing accumulation**, never through the fitted mean/std/skew.

Only when both are green does forecast work begin.

### Stages 1–6 (the forecast pipeline; one parameterized runner, `run=latest` or a date)

1. **Refresh ERA5(T)** — re-pull Florida hourly ERA5 to the current ERA5T frontier (~now−5), aggregate
   to daily (reuses `access/pull_hourly_async.py` + `derive/aggregate_daily.py`). Frontier = last day with
   24 complete hours. → shared history spine.
2. **Pull forecasts** —
   - Latest ENS run (`enfo`, **51 members**), Florida crop (download global → crop), out to 15 days, with
     the sub-daily steps needed: `mx2t3`/`mn2t3` (3-hourly max/min temp, **only to +144 h**), sub-daily
     `2t`/`10u`/`10v`, and `tp`/`ssrd` accumulation boundaries.
   - The **oldest still-retained run** as a single deterministic gap-fill series (ensemble mean of that
     run, or `oper`/HRES — decided empirically; `enfo` control `type=cf` did not index in a probe).
3. **Forecast → daily** — aggregate each member (and the gap-filler) to the **same** daily base fields as
   `aggregate_daily.py`. **De-accumulation (Codex #2):** forecast `tp`/`ssrd` accumulate from step 0 — a
   *different data contract* than ERA5's hourly increments. Algorithm: sort by `(member, valid_time, step)`;
   difference consecutive lead steps within each member to get per-interval increments; validate cumulative
   **monotonic-nonnegative** (except step 0); resample increments to UTC days. **Tests** crossing the
   3h→6h transition at +144 h and crossing 00Z.
4. **Build the shared history-to-T0 series** (one series, shared by all 51 members):
   ERA5 spine `[frontier−180d .. frontier]` → gap-filler forecast (recent ~2 d) → residual sub-gap (linear
   temp/solar/wind; **climatological-median precip**). 180 d because SPEI-6 needs a 180-d window (the
   standardization is already frozen, so only the trailing accumulation needs history depth).
5. **Stitch + compute per member** — for each member m (1..51):
   `member_series = shared_history[.. T0] + member_forecast_daily[T0 .. T0+15]`; **seam-validate**
   (below); run `apply_features(member_series, frozen_climatology)`; slice out `[T0+1 .. T0+15]`.
6. **Store the feature ensemble** — NetCDF, dims `(member, valid_time, lat, lon)` × 22 features, forecast
   horizon only; + manifest + provenance (run datetime, ERA5 frontier, gap-fill run id, config/climatology
   hash, sha256 of inputs) + the honesty/quality variables below.

## Honesty & guards baked into stages 3–6 (Codex findings)

- **Ensemble-spread labeling — not inflation (Codex #1).** A day-1 `spei_6` is 179 shared history days +
  1 member day, so members near-agree at T0. This collapse is **physically correct** (members genuinely
  share history) — the risk is **misinterpretation**. We **reject** filling the pre-T0 tail with old-run
  members (member IDs don't correspond across runs). Instead we **emit `effective_member_days_in_window`**
  per feature/valid-day (day-1 spei_6 = 1/180; day-15 = 15/180) and document that the ensemble spread is
  **forecast divergence only** — history, gap-fill, and model error are **not** in it.
- **Seam validation, fail-closed (Codex #4).** Before `apply_features`: continuous daily date index; no
  duplicate/missing dates; all required base variables present; **no NaN in `[T0−179, T0+15]`** for
  SPEI-used variables; per-day source labels. **Fail closed** — never silently emit a mostly-NaN feature
  file; mark it failed instead.
- **Quality flags travel IN the NetCDF, not just the README (Codex #6, #7).** Per valid-day:
  `temp_extreme_source` (`mx2t3`/`mn2t3` | `instant_2t_proxy`), `subdaily_step_hours` (3|6), `calm_proxy`
  (bool), `aggregation_complete` (bool), and **`source_class`** (`era5` | `gapfill_forecast` |
  `interpolated` | `member_forecast`). Store member coords **exactly as ECMWF provides**; **assert exactly
  51 members before writing**.

## New code layout (`data-sources/weather/forecast/`)

| File | Role |
|------|------|
| `pull_ens.py` | Pull ENS run + gap-fill run, Florida crop, cache + manifest |
| `aggregate_forecast.py` | Forecast GRIB → daily per member (mirrors `aggregate_daily.py`; de-accumulation algorithm) |
| `build_feature_ensemble.py` | Seam-validate → stitch → `apply_features` → store ensemble + quality vars |
| `run_forecast_features.py` | Top-level orchestrator (stages 1–6), parameterized (`--run`, `--area`) |
| `README.md` | Runbook — generate a new run with **no new code** |
| `tests/test_deaccum.py`, `tests/test_stitch_seam.py`, `tests/test_features_regression.py` | De-accumulation, seam-guard, and Phase-0 golden-regression tests |

Feature math stays in the refactored `derive/features.py` (shared with history).

## Daily-aggregation details (forecast resolution mismatch vs hourly ERA5)

- **Tmax/Tmin:** from `mx2t3`/`mn2t3` (3-hourly max/min), **only to +144 h (day 6)**. Beyond day 6 only
  6-hourly instantaneous `2t` exists → Tmax/Tmin **degrade** days 7–15 (flagged via `temp_extreme_source`).
- **Tmean:** from sub-daily `2t` (3-hourly to 144 h, 6-hourly after).
- **precip / ssrd daily sum:** de-accumulation algorithm above.
- **wind mean/max/min:** from sub-daily `10u`/`10v`.
- **calm_hours:** ERA5 counts hours below a wind threshold from 24 hourly steps; the forecast is 3/6-hourly
  → a **scaled proxy** (fraction of sub-daily steps below threshold × 24), flagged via `calm_proxy`.

## Storage & repeatability

- Output: `data/derived/forecast_features/<run>/feature_ensemble.nc` (dims `member × valid_time × lat × lon`,
  22 features + quality vars) + manifest + provenance. Modest size (51 × 15 × ~27×32).
- **Repeatable:** `python forecast/run_forecast_features.py --run latest --area <FL>` regenerates
  everything; a new forecast = same command, new date. That's the runbook — **no new code per run**.
- Deterministic, cached, sha256-manifested — same discipline as the history layer.

## Documented limitations (carried in output + runbook)

1. **Seam bias** — raw stitch, no bias correction (no reforecast in open-data → future work: quantile-map).
2. **Gap fill** — residual ~3-day interpolation; precip via climatological median.
3. **Tmax/Tmin degrade past day 6** — no 3-hourly max/min beyond +144 h.
4. **calm_hours proxy** — 3/6-hourly forecast vs hourly ERA5 resolution mismatch.
5. **SPEI provisional** — short ~10-yr calibration, inherited from the historical features.
6. **Ensemble spread ≠ calibrated probability** — it is forecast divergence only; near-T0 memory features
   are history-dominated (see `effective_member_days_in_window`).

## Leakage posture (the graded axis)

- **Frozen climatology** — SPEI standardization is fit once on ERA5 2016–2025 and reused unchanged;
  `apply_features` cannot re-fit (no fitting branch) → forecast SPEI is on the same scale as history and
  cannot leak forecast values into its own standardization.
- **Trailing/rolling features** — strictly backward-looking (`min_periods = window`) → as-of safe.
- **Stitch direction** — history precedes forecast in every member series; no future value informs a past
  feature. Correlation ≠ causation for any driver implication downstream.

## Open items resolved during implementation (not gating)

- Which deterministic series backs the gap-fill (ens-mean of the old run vs `oper`/HRES) — decided
  empirically in stage 2; recorded in provenance.
