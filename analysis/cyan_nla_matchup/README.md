# CyAN CI_cyano ↔ NLA 2022 matchup — PROTOTYPE

A thin, honest slice that answers a question from the modeling-utility discussion (scoped by a
Codex review): **how well does the CyAN satellite cyanobacteria index (CI) track NLA's lab
chlorophyll-a and microcystin nationally — and, first, how many usable matches even survive the
resolution / cloud / timing constraints?**

This is **role #2** from the NLA modeling discussion (satellite-signal calibration/validation),
prototyped to *size the opportunity*, not to validate a product.

## Inputs (all already local)
- **NLA 2022** sampled lake-visits: `data-sources/EPA-NARS/data/raw/nla2022/` (siteinfo + waterchem
  `CHLA` + algaltoxins `MICX`) and the lake **polygons** `nla2022_lakes.zip` (EPSG:5070).
- **CyAN** weekly CONUS CI_cyano mosaics: `data-sources/cyan/data/raw/conus_mosaic_weekly/`
  (300 m, EPSG:5070 — same grid, so no reprojection). DN→CI via `cyan/access/cyan_api.py`.

## Method (per lake-visit; unit = `UID`)
1. Temporally match the visit `DATE_COL` to the weekly (7-day) mosaic whose window contains it
   (else nearest within `--tol-days`); record the offset.
2. **Polygon-extract** CI over the lake footprint (user-authorized per-lake reduction; *no*
   cross-lake aggregation): classify in-lake 300 m pixels (land / cloud=nodata / water
   below-detection / valid-CI) and summarize CI (`--stat max|mean`; below-detection water → a CI
   floor so those lakes are kept as left-censored-low, not dropped).
3. Report the **attrition funnel** and, on survivors, CI↔chl-a, CI↔microcystin, and a
   CI-detection × toxin-detection contingency.

## Key findings (run 2026-07-02; `--stat max --tol-days 8`)
- **Usable matches: 334 / 1,219 sampled-with-chl-a (27.4%).** Temporal matching was free (weekly
  mosaics are continuous). The binding constraints are **lake size** (290 lakes are sub-resolvable
  at 300 m) and, dominantly, **cloud** (595 of the 929 resolvable lakes had no cloud-free water
  pixel that week). Usable lakes are biased **large** (median 515 ha, 55 in-lake pixels).
- **CI tracks lab chlorophyll-a moderately:** Spearman ρ = **0.62** (n=334); robust to the CI stat
  (mean → 0.64) and temporal tolerance.
- **CI tracks microcystin more weakly:** ρ = **0.56** (n=184 detections) — and the toxin is a
  *different target* from the spectral index.
- **CI is a poor toxin *screen* in both directions** (contingency, n=334): agreement ~60%, but
  **65** lakes where CI sees cyano yet no microcystin (over-prediction) **and 70** lakes where CI
  sees nothing yet microcystin was detected (**missed toxins**). This reproduces, at the pixel↔lab
  level, the load-bearing HAB caveat that biomass/spectral proxies do not equal toxin risk.

## Honest caveats (this is a prototype, not a validation)
- 300 m CyAN under-resolves small lakes → the usable set is **not representative** of the NLA lake
  population (a resolution-induced exclusion; survey weights can't repair it).
- A weekly composite is **not same-day**; a grab sample and the CI can be days apart, and blooms
  are patchy in space/time.
- **Correlational, cross-sectional** — measures *signal agreement*, not causation; it does not
  validate an operational forecast. chl-a, CI, and microcystin are **distinct targets**.

## Run
```bash
cd analysis/cyan_nla_matchup
python matchup.py                 # default: --stat max --tol-days 8
python matchup.py --stat mean     # conservative CI summary (robustness check)
```
Outputs → `outputs/`: `matchup_report.md`, `matchup_scatter.png`, `cyan_nla_matched.csv`
(the 334-row matched table — the substrate for any follow-on modeling).

## So what (ties back to the modeling-roles discussion)
The satellite↔in-situ bridge is **real but thin and cloud-limited**: usable nationally for
*larger* lakes, moderately good for biomass (chl-a), and **not** a trustworthy toxin detector.
That argues a defensible product should (a) treat CI as a *biomass/screening* signal, not a toxin
claim, (b) carry the resolution/cloud coverage limits explicitly, and (c) use NLA's lab toxins to
*calibrate and bound* the CI→risk translation rather than assume it. Next steps worth considering:
gap-fill cloud with the daily CyAN product (vs the 7-day composite), test `INDEX_*` point-sampling
vs polygon extraction, and repeat across cycles (2017) to grow n before any modeling.
