# Forecast feature ensemble — operational run-guide

Produces the **same 22 algal-growth weather features** we have for ERA5 history, but for the
**~15-day forecast horizon as a 50-member ECMWF ensemble** — one daily feature series per member,
computed on a stitched *recent-history + forecast* series so the memory features (SPEI, trailing
precip/GDD/solar/wind) are correct at the seam.

**Design & rationale:** [`docs/plans/2026-07-05-forecast-ensemble-features-design.md`](../../../docs/plans/2026-07-05-forecast-ensemble-features-design.md)
(Codex-reviewed, 7 findings folded in). **Feature math** is shared with the history layer
(`../derive/features.py`); this layer only adds the *forecast acquisition + stitch*.

> **⚠️ Status (2026-07-07): PAUSED — not production-viable.** Pipeline is built end-to-end and unit-tested
> (30 tests green: de-accumulation, stitch/seam, feature-refactor regression), and the faithful pull was
> **proven feasible** (a full 2.78 GB global param downloaded clean). **But** the Florida crop stage has a
> **cfgrib per-step memory leak** — RSS climbs ~0.21 GB/step to the full ~17.6 GB cube and thrashes to
> ~53 GB (near-OOM), so **no feature-ensemble product was ever generated**. Read the
> **[Post-mortem](../../../docs/plans/2026-07-05-forecast-ensemble-features-design.md#post-mortem--2026-07-07-why-this-is-paused)**
> before any future work. Stages 3–6 are built + unit-tested but have **never run on real forecast data**.

## Repeat a run with ONE command (no new code)

```bash
# From data-sources/weather/forecast/  (deps: pip install -r ../../requirements.txt)

# Latest 00/12z ENS run, full pipeline (pull → aggregate → stitch → ensemble):
python run_forecast_features.py

# A specific run (reproducible; pin the run you want to demo):
python run_forecast_features.py --ens-date 20260705 --ens-time 12

# Also advance the ERA5 history frontier first (shrinks the gap that must be interpolated):
python run_forecast_features.py --refresh-era5

# Rebuild from already-pulled data (re-aggregate + re-stitch, no re-download):
python run_forecast_features.py --skip-pull
```

Output: `../data/derived/forecast_feature_ensemble_<first-valid-day>.nc`
(dims `member × valid_time × lat × lon`, 22 features + quality/provenance variables).

## Pipeline stages (what the one command chains)

| Stage | Script | Does |
|-------|--------|------|
| 1 (opt) | `../access/pull_hourly_async.py` + `../derive/aggregate_daily.py` | Refresh ERA5T → advance the daily-history frontier to ~now−5. |
| 2 | `pull_ens.py` | Pull the ENS run (`enfo/pf`, **50 members**) + an `oper` gap-fill run; crop to Florida; write `run_manifest.json`. |
| 3 | `aggregate_forecast.py` | Forecast GRIB → daily base fields **on the ERA5 grid** (de-accumulate `tp`/`ssrd`; Tmax/Tmin from `mx2t3`/`mn2t3`; quality flags). |
| 4-6 | `build_feature_ensemble.py` | Build the shared history-to-T0 series (ERA5 → gap-fill → interpolated residual); stitch per member; apply the **frozen** SPEI climatology; store the ensemble. |

## Key facts (probe-verified 2026-07-05/06)

- **50 members, not 51.** Open-data ENS has **no `cf` control** (`type=cf` → "no index entries"); only
  the 50 perturbed `pf` members are served. The deterministic `oper` (HRES) run stands in for a
  control-like series in the gap-fill.
- **All drivers available for the forecast:** `2t, 10u, 10v, tp, ssrd` (+ `mx2t3`/`mn2t3` to +144 h).
  `ssrd` (solar) is present — no climatological-solar fallback needed.
- **Step ladder:** 3-hourly to +144 h, 6-hourly to +360 h (15 days). Only 00/12z ENS runs reach +360 h
  (06/18z reach only +144 h) — the puller auto-selects a long-range cycle.
- **Download is heavy:** one ENS field = ~33.5 MB (50 members × global) and open-data can't server-side
  crop → the faithful pull is ~17 GB of transfer. Intended mitigation: pull one param at a time →
  stream-crop to Florida per step → delete the global GRIB. **⚠️ The per-step crop leaks (~0.21 GB/step,
  see Status/Post-mortem) — this mitigation does not currently work at scale.** Resume reuses complete
  global GRIBs by **step/member count only, not integrity** → a corrupt (interrupted) download can be
  reused and crash eccodes natively; delete a suspect global to force a fresh pull.
- **Grid reconciliation:** the open-data global grid is whole-degree-aligned; our ERA5 grid is offset
  ≤0.2° (CDS `area` registration). Forecast fields are **nearest-neighbour reindexed onto the ERA5
  master grid** (values preserved, no interpolation).
- **Retention:** open-data keeps ~3 days of runs. The gap-fill uses the oldest retained `oper` run;
  refresh ERA5T to keep the interpolated residual small.

## Leakage posture (the graded axis)

- **Frozen climatology.** The SPEI standardization is fit once on ERA5 2016–2025 (`../derive/features.py:
  fit_climatology`, persisted to `../data/derived/spei_climatology_*.nc`) and reused unchanged.
  `apply_features` has **no fitting branch** — it errors without a climatology, so a stitched forecast
  series can never re-fit its own SPEI standardization. Enforced by `tests/test_features_regression.py`.
- **Backward-looking only.** Trailing/rolling features use `min_periods = window`; history precedes
  forecast in every member series — no future value informs a past feature.

## Honest uncertainty & documented limitations (carried IN the output NetCDF)

- **`effective_member_days_in_window`** — how many days in each feature's window are member-specific.
  Near T0 the memory features are history-dominated (day-1 `spei_6` = 1/180), so members near-agree;
  the ensemble spread is **forecast divergence only** (history / gap-fill / model error not included).
- **Per-day quality flags:** `source_class` (era5 | gapfill_forecast | interpolated | member_forecast),
  `temp_extreme_source` (`mx2t3/mn2t3` vs `instant_2t_proxy` past +144 h), `subdaily_step_hours`,
  `calm_proxy`, `aggregation_complete`.
- **Seam bias** — raw stitch, no bias correction (no reforecast in open-data → future work: quantile-map).
- **Gap fill** — residual interpolated: **linear** for temp/solar/wind, **climatological median** for
  precip (never linear-interpolate precip). Seam validation is fail-closed.
- **Tmax/Tmin degrade past day 6**; **`calm_hours` is a 3/6-hourly proxy**; **SPEI provisional**
  (short ~10-yr calibration, inherited from history).

## Directory map

| Path | What | Git? |
|------|------|------|
| `run_forecast_features.py` | One-command orchestrator (stages 1→6) | yes |
| `pull_ens.py` | Stage 2 — ENS + gap-fill pull, FL stream-crop, manifest | yes |
| `aggregate_forecast.py` | Stage 3 — forecast → daily base fields on the ERA5 grid | yes |
| `build_feature_ensemble.py` | Stages 4-6 — stitch + frozen-climatology apply + store | yes |
| `../tests/test_deaccum.py` · `test_stitch_seam.py` · `test_features_regression.py` | Unit tests | yes (green) |
| `../data/raw/forecast_ens/<run>/` · `forecast_gapfill/<run>/` | Cropped FL param NetCDFs + `run_manifest.json` | no (gitignored) |
| `../data/derived/forecast_feature_ensemble_*.nc` | The feature ensemble product | no (gitignored; regenerate) |

## License / attribution

Forecast = **ECMWF open data, CC-BY-4.0** (attribute ECMWF). History = **Copernicus/ERA5, CC-BY-4.0**.
Carry the attribution on every derived artifact.
