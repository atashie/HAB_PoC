# Weather features — QA & methodology

**Product:** `data/derived/weather_features_2016-01-01_2026-06-27.nc` (gitignored; regenerates from
`derive/features.py`). **Scope:** State of Florida, native **0.25°** (27×32 cells), **daily**,
**2016-01-01 → 2026-06-27** (3,831 days). **Compiled:** 2026-07-03. License: CC-BY-4.0 (Copernicus/ERA5).
**Reviewed by Codex (GPT-5), 2026-07-03 — 4 findings, all fixed (below).**

## Lineage (every feature traces to bytes + code)
Hourly ERA5 single-levels (CDS, `access/pull_hourly_async.py`, 11 yearly GRIBs, sha256-manifested)
→ daily base fields (`derive/aggregate_daily.py`: Tmax/Tmin/Tmean, precip-sum, solar-sum, wind
mean/max/min, calm-hours; ERA5 accumulation `time×step` flattened via `valid_time`; **incomplete days
dropped**) → features (`derive/features.py`). Unit tests: `tests/test_features.py` (8) + `tests/test_era5_daily.py` (4).

## Feature inventory (22)
| Family | Features | Definition |
|---|---|---|
| Drought | `spei_1,2,4,6` | **Daily-cadence** SPEI: standardized trailing **30/60/120/180-day** water balance D = P − PET; per-calendar-month Pearson III (method-of-moments); a distinct value every day |
| PET | `pet_hargreaves_mm`, `gdd_daily` | Hargreaves daily PET (FAO-56, true DOY); daily GDD (base 10 °C) |
| Antecedent moisture | `precip_trail_{7,14,30,60,90}d_mm` | trailing rainfall sum |
| Thermal | `gdd_trail_{30,60,90}d` | trailing Growing Degree-Days (base 10 °C) |
| Light | `ssrd_trail_{14,30}d_mj` | trailing downward solar |
| Air-stillness | `calm_hours_trail_{7,14,30}d`, `wspd_trail_{7,14,30}d_mean_ms` | trailing calm-hours; trailing mean wind |

## Codex review — findings & resolutions (2026-07-03)
1. **[High] SPEI within-month look-ahead** — monthly SPEI was broadcast to *every* day in that month
   (a June-1 join saw the full June water balance). **Fixed → then upgraded to daily cadence (user direction):**
   SPEI is now computed **per day** as the standardized trailing k×30-day water balance (spei_1→30 d … spei_6→180 d),
   so each day has its own value from its own backward-looking window — no broadcast. Verified: 30 distinct daily
   values across a sample month; ≈ N(0,1); valid from day 30 (spei_1) … day 180 (spei_6). (`features.py add_spei`)
2. **[High] Hargreaves PET day-of-year drift** — `climate_indices.eto_hargreaves` reshapes to (years, 366) and
   assumes 366-day years, so a continuous multi-year series drifts DOY (hence Ra) after each non-leap year.
   **Fixed:** replaced with a **vectorized FAO-56 Hargreaves using the true calendar DOY**; cross-checked to
   match the library on a single aligned leap year (`tests/test_features.py`). Verified no drift: PET peak month =
   July in both 2016–18 and 2023–26.
3. **[Med] Incomplete final day** — the ERA5T tail ended 2026-06-28 with only 3 h, biasing that day.
   **Fixed:** `aggregate_daily.py` now **drops any day without 24 hourly steps** (2026 → 178 days, ends 06-27).
4. **[Med] Incomplete final month in SPEI** — the partial current month formed a monthly total.
   **Fixed:** months lacking all calendar days are **masked** (NaN) before the SPEI transform.
5. **[Low, accepted] SPEI Pearson III + ~10-yr calibration is statistically fragile** — see caveats.
Codex also confirmed correct: unit conversions (K→C, m→mm, J→MJ), accumulation `valid_time` flattening/dedupe,
calibration excludes partial years, trailing windows backward-looking (`min_periods=window`).

## QA results (post-fix, validated 2026-07-03)
- **SPEI ≈ N(0,1):** spei_1/2/4/6 mean −0.03…−0.07, std 1.02…1.04, range ±3.09. Valid 99/98/97/95%
  (each scale needs its window of history: 30/60/120/180 days before the first valid value).
- **Physical ranges (all sensible):** PET 0.1–7.7 mm/day (monthly-mean seasonal, Jul peak); GDD-90d ~237–1770;
  precip-30d 0–784 mm; precip-90d 17–1085 mm; ssrd-30d 224–815 MJ/m²; calm-hours-30d 0–628 of 720; wind 1–13 m/s.
- **Cross-year consistency** (daily aggregates): annual precip 1,155–1,348 mm/yr; Tmax 37–40 °C; Tmin −3 to −8 °C;
  leap years 366 d. Real events visible (2017 Irma winds; panhandle winter freezes).

## Deferred issues (documented for future work — user-approved to defer 2026-07-05)
1. **⚠ SPEI calibration record is SHORT (~10 complete years, 2016–2025).** Standardization is correct but the
   fitted tails are under-constrained → **SPEI values are provisional**. **Fix (future):** pull a longer ERA5
   baseline (e.g. 1991–2020) for the SPEI climatology *only*, keeping the served series at 2016→present.
2. **GDD base = 10 °C is a placeholder.** **Fix (future):** calibrate against a cyanobacteria-relevant thermal
   threshold from the literature (`../../Research/`).

## Design decisions (settled 2026-07-05)
3. **SPEI = daily cadence, Pearson III (method-of-moments, per calendar month).** User-directed daily cadence
   (not the traditional monthly index). Pearson III kept (the original log-logistic isn't in `climate_indices`;
   our standardization is hand-rolled with scipy `pearson3`). Settled — good as-is.
4. **PET = Hargreaves** (temperature-only). Settled for now; Penman-Monteith upgrade possible later using
   `ssrd` + humidity.
5. **`ssrd_trail_*` is DOWNWARD solar** (not net) — a light-availability proxy, labeled as such.

## Leakage posture (leakage is the graded axis)
- **Trailing features** — strictly backward-looking (rolling with `min_periods = window`, NaN until enough
  history) → as-of safe.
- **SPEI** — the trailing k×30-day water-balance accumulation is backward-looking (`min_periods = window`); the
  per-calendar-month Pearson III standardization uses a **fixed 2016–2025 climatology**, reused unchanged at serve
  time (never re-fit including the target window) → as-of safe.
- **Aggregation** — temporal → daily is explicit (user-requested). **No spatial aggregation** (native per-cell).

## Reproducibility
Deterministic; scripted; cached + sha256-manifested (`weather_features_manifest.jsonl`).
Regenerate: `python derive/aggregate_daily.py` (all years) → `python derive/features.py`.
