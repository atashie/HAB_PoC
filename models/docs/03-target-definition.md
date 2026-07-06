# 03 — Target definition & CyAN→lake QA (Prepare)

> The **AL1 bloom label** and the per-lake CyAN aggregation, **pinned from EPA/Schaeffer's deposited
> code** (DOI `10.23719/1529140`, sha256 `126f7f3f…4afb`) so we match the federal benchmark exactly
> rather than invent a threshold. Resolves pre-build pins #1 (AL1 threshold) and #3 (lake-week QA).
> Code lines cited are from the extracted `INLA_CONUS_forecast/` R scripts.

---

## 1. The bloom label (authoritative — `cyan_processing_conus.R:170`)

```r
bloom = ifelse(median >= 130, T, F))   # 97 for 3 ug/L, 130 for 12 ug/L, 151 for 24 ug/L
```

- **Target = per-lake, per-week `bloom` = ( median CyAN DN over the lake's resolvable pixels ≥ 130 ).**
  Binary. `median ≥ 130` **is** WHO Alert Level 1 (12 µg/L chl-a) in their operationalization.
- **Threshold ladder (from the same comment), for sensitivity analysis:**
  | WHO tier | chl-a | **median DN ≥** |
  |---|---|---|
  | (sub-AL1) | 3 µg/L | 97 |
  | **AL1 (primary target)** | **12 µg/L** | **130** |
  | AL2 | 24 µg/L | 151 |
- **DN→CI→chl-a traceability:** `CI = 10^(DN·0.011714 − 4.1870866)` (cyan/METADATA §4). DN 130 →
  CI ≈ 0.00217 → ≈ 217,000 cells/mL (`≈1e8·CI`) ≈ 12 µg/L chl-a. The DN→chl-a step carries scatter
  (CI↔chl-a is approximate); the label is a **satellite AL1 realization**, not a lab measurement —
  stated as a limitation wherever bloom skill is reported.
- **We threshold the MEDIAN**, not the mean. `compile_data.R:32` confirms EPA also uses the median as
  the CyAN predictor ("we're actually using the median, not the mean"), despite the CSV column name.

## 2. Per-lake CyAN aggregation (authoritative — `cyan_processing_conus.R:91,105–108`)

```r
metrics <- function(x) c(mean=mean(x,na.rm=T), median=median(x,na.rm=T), st_dev=sd(x,na.rm=T))
exact_extract(ci_brick, lake)[[1]] %>% filter(coverage_fraction == 1) %>% ... apply(2, metrics)
```

- Per lake × weekly scene, compute **mean / median / SD** of DN over **pixels with
  `coverage_fraction == 1`** — i.e. **only pixels wholly inside the lake polygon** (their mixed/edge
  masking; partial-coverage pixels are dropped). `na.rm=T` excludes masked cells; SD is the **sample**
  SD (`ddof=1`, R `sd()`; NaN for a single-pixel week).
- We **closely approximate** `coverage_fraction == 1` with an **8× subpixel rasterization**
  (`OVERSAMPLE=8`, coverage ≥ 0.999) — *not* `exactextract` (not installed). This is faithful for
  multi-pixel lakes; **exactextract cross-validation on a small/medium/large stratified sample is a
  QA follow-up** (Codex M2). The **median** feeds the label (§1) and is the primary CyAN feature;
  **mean/SD** are additional features.

## 3. Lake-week QA / validity policy (pin #3)

- **DN handling:** upstream masking (Schaeffer `parallel.step1plus2.R`) sets land (254) and
  no-data/cloud (255) to NA; **DN 0 (below-detection) is retained** as a valid low value (a lake of
  mostly DN 0 → median 0 → no bloom). Only pixels inside the lake polygon (`coverage_fraction==1`)
  and non-NA contribute.
- **Insufficient weeks (parity-primary + sensitivity — Codex H3):** the resolvable-lakes set already
  requires ≥ 3 water pixels per lake. A lake-week with **all pixels cloud/no-data → median = NA →
  bloom = NA**. EPA fills NA→`F` **only** under ice (winter balancing); **Florida has no ice, so we do
  NOT fill** — such lake-weeks are **labeled missing, not imputed** (D-26f). **Primary target = Schaeffer
  parity:** the `na.rm` median has *no* min-coverage guard, so a week is valid if it has **≥ 1** clear
  pixel (this is what the code does). We do **not** silently apply a coverage threshold to the primary.
  **Instead** we record **`valid_frac = n_valid / n_inside`** per lake-week and run a **coverage
  sensitivity**: low-coverage weeks (`valid_frac < 0.5`) are ~8–9% of valid rows and carry a *much
  lower* bloom prevalence (~7% vs ~25% for `≥ 0.5`) — a real bias, reported and available as a
  `valid_frac ≥ 0.5` robustness filter, not hidden.
- **QA fields retained per lake-week** (features + stratifiers, D-26f): valid-pixel count, valid
  fraction, no-data fraction. Because cloud gaps are **non-random** (persistent summer convection can
  correlate with bloom conditions), run a **missingness sensitivity** on the exclusion rule.

## 4. Week convention (pin #4, target side)

- Dates parsed from the filename 7-digit `%Y%j` (year + day-of-year) and joined to a **week-assignments
  table** (`generate_week_assignments_tibble.R`): CyAN weeks where **week 1 begins on the first Sunday
  of the year** (README §1). We reproduce this table so our week labels align byte-for-byte with CyAN
  and with the EPA benchmark's weekly cadence. (EPA's dashboard reports `WeekEndDate` = the Saturday
  ending the Sun–Sat window — the same weeks, labeled by end date.)
- Full issue-date / feature-cutoff / antecedent-window definitions live in the **feature-availability
  matrix** (`docs/02`, pin #4 feature side).

## 5. What we deliberately match vs. diverge from EPA

| Element | EPA/Schaeffer | Us | 
|---|---|---|
| Label | median DN ≥ 130 (AL1) | **same** (+ 97/151 sensitivity) |
| CyAN aggregation | mean/median/SD, coverage_fraction==1 | **same** |
| Week convention | CyAN first-Sunday | **same** |
| Ice relabel | NA→F under ice | **skipped** (no FL ice) |
| Weather | PRISM | **ERA5** (diverge — augmented track) |
| Water temp | RF-modeled (`SW_Model`) | WQP in-situ / ERA5-derived (diverge) |
| Extra in-situ | none | NWIS + WQP (augmented track only) |

Matching the label + aggregation + weeks is what makes the **h=1 head-to-head** valid; weather/in-situ
divergences live in the **augmented track** (DESIGN §3), not the parity comparison.

## 6. Realized output (built 2026-07-02)

`prepare/build_cyan_lake_target.py` → `data/derived/cyan_lake_weekly_fl.parquet`:

- **70,623 lake-weeks** = 133 FL lakes × 531 OLCI weeks (2016-04-24 → 2026-06-21).
- **96.6% valid** (a lake-week is missing only if *all* its inside-pixels are cloud/no-data — 3.4%,
  2,390 lake-weeks; lake-wide medians over many pixels are robust to partial cloud).
- **FL bloom prevalence = 23.2%** of valid lake-weeks (15,826 blooms); Apr–Nov 24.3%.
- **Two findings worth carrying forward:**
  1. **FL runs ~2–3× the EPA CONUS base rate (~9–10%).** Expected — FL lakes are warm, shallow,
     eutrophic; the CONUS average is dominated by oligotrophic/ice-covered northern lakes. This is a
     real signal, not a bug, and it means **milder class imbalance** than EPA's (easier precision/
     recall). It also means the EPA head-to-head must be on **shared rows / matched base rate**, not
     raw metric-vs-metric (already required, DESIGN §8).
  2. **Near-flat seasonality** (Jun peak 28.3%, winter trough ~20% — blooms persist through warm FL
     winters). This validates **modeling all weeks** (not EPA's Apr–Nov) and **skipping the ice mask**.
- **Bloomiest lakes are the right ones:** Apopka 99.8%, Hancock 98.1%, Parker 95.8%, Trafford 94.5% —
  all known hypereutrophic central-FL lakes → strong per-lake persistence (the autoregressive ladder,
  DESIGN §8, is essential).
- **AR(1) decomposition (Codex M6, verified):** `corr(cyan_median, lag1)` = **pooled 0.903**, but
  **within-lake (demeaned) 0.734 / median per-lake 0.666**. ~Half the headline pooled autocorrelation
  is *between-lake* structure (which lakes are chronically bloomy) — carried by static lake features —
  not *within-lake* week-to-week persistence (~0.7), which is what a same-lakes temporal forecast must
  actually beat. Reported honestly so persistence skill isn't overstated.
- **Schema:** `comid, start_date, end_date, year, n_inside, n_valid, nodata_frac, cyan_mean,
  cyan_median, cyan_sd, bloom, gnis_name, area_sqkm`.

---

**Provenance:** Schaeffer INLA code, EPA ScienceHub DOI `10.23719/1529140`
(`INLA_CONUS_forecast.zip`, 33,677 B, sha256 `126f7f3fd9f79bdb36083009f726ecbe2d9047b728b7ac95bb2498545cf84afb`),
downloaded + verified 2026-07-02; lines cited from `cyan_processing_conus.R` and `compile_data.R`.
The canonical persistent mirror is `../../data-sources/cyano-forecasts/access/pull_official.py`.
