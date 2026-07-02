# cyano-forecasts — preserved primary-source statements + live-probe log

Verbatim quotes and empirical checks behind `../METADATA.md`, with URL + access date, so the audit
trail survives link rot. All accessed **2026-07-02**. Quotes marked **[cached]** are reproduced from a
full-page snapshot preserved in this folder (`habs_hab-forecasts.html`,
`cyanobacterial-hab-forecasting-research.html`) — the exact wording can be re-verified there. Facts
confirmed by our own live probe are marked **[probe]**; those scripts live in `../access/` (and the
one-shot verification scripts in the session scratchpad).

> These are the *load-bearing sentences* behind the metadata. Where EPA's rendered page and our probe
> agree (e.g. the bloom definition), both are recorded.

---

## 1. What the forecast value means — EPA HAB Forecasts page  **[cached]**
URL: https://www.epa.gov/habs/hab-forecasts

- *"The value the forecast generates is a probability (or likelihood) from 0 to 100% that the lake or
  reservoir may experience a cyanobacteria dominated bloom in the next 7 days (where a bloom is defined
  as a lake-wide median surface chlorophyll a ≥12 ug/L over the lake area the satellite can see
  accurately)."*
- *"The EPA has developed the following dashboards for viewing the weekly forecasts for each resolvable
  (what this satellite can see accurately) CyAN lake in the United States. The dashboards also provide
  past forecast information, forecast patterns and downloadable data."*
- *"Note that forecasting data are typically generated from the beginning of April through November as
  the probabilities of harmful algal blooms are generally lower during colder months."*

## 2. Resolvable-area caveat — EPA HAB Forecasts page  **[cached]**
URL: https://www.epa.gov/habs/hab-forecasts

- *"the CyAN satellite generally does not resolve ("accurately see") shallow areas along the edge of the
  lake, small embayments, narrow areas of the lake/reservoir, etc. This means lakes where blooms may be
  isolated or occur in small specific embayments may not register as having a high probability of a
  bloom at the scale of all the resolvable portions of the lake. Similarly, lakes/reservoirs that are
  long and thin may only have resolvable pixels in wider, more open segments where blooms may not occur
  as much."*
- Figure-1 legend (pixel semantics): *"Black pixels were captured by the satellite, but did not pass
  quality control. Gray pixels were captured by the satellite and had no cyanobacterial chlorophyll
  detected. Other colored pixels … had detectable cyanobacterial chlorophyll."*

## 3. Coverage, cadence, over-prediction disclaimer — EPA Forecasting Research page
URL: https://www.epa.gov/water-research/cyanobacterial-harmful-algal-blooms-forecasting-research
(retrieved via WebFetch; exact wording preserved in `cyanobacterial-hab-forecasting-research.html`)

- Experimental model launched **2024**; **7-day** probability predictions for **2,192 lakes** resolvable
  by Sentinel-3; weekly, released **Tuesday or Wednesday**.
- Disclaimer (as retrieved): *"This model should not replace regular sampling or observation methods.
  Currently, the model overpredicts positive events."* … *"The model has low false omission and is
  therefore more conservative in protecting health."*
- Weekly U.S. forecasts *"resumed for 2025"* and are *"now housed on EPA's Harmful Algal Bloom
  Forecasting webpage."*

## 4. Method, predictors, metrics, data-availability — Schaeffer et al. 2024
URL (open access): https://pmc.ncbi.nlm.nih.gov/articles/PMC10842250/ · DOI 10.1016/j.jenvman.2023.119518

- **Data availability (verbatim):** *"All data is publicly available as detailed in the methods and code
  will be made available at the following DOI after acceptance: https://doi.org/10.23719/1529140"*
- **Bloom threshold:** WHO **Alert Level 1** — *">12 μg L−1 chlorophyll-a with cyanobacteria dominance"*
  (binary weekly presence/absence, lake median).
- **Model:** hierarchical Bayesian spatiotemporal via **INLA**; binomial logistic with **AR1** temporal
  term + **SPDE** spatial random field.
- **Predictors:** water surface temperature (RF-modeled from air temp, elevation, lake morphology, day
  of year); precipitation (**PRISM**); mean lake depth; lake surface area.
- **Skill (2021 test year, point estimates, NO CIs reported):** AUC 0.95; accuracy **0.90** (baselines
  SVC/RF/DNN/LSTM/RNN/GRU 0.84–0.85); sensitivity 0.88; specificity 0.91; **precision 0.49**;
  false-omission 0.01; F1 0.63; κ 0.58; Brier 0.04.
- **Base rate:** *"9.1% probability of a cyanoHAB event across time"*; **43,482 / 432,030** lake-weeks
  (10.1%) were blooms.
- **Validation:** 70/30 train/holdout on 2017–2020, **independent 2021 test**; classification cutoff
  0.10; iterative weekly retraining in 2021.
- **Over-prediction (verbatim):** *"the model correctly assigns lower probabilities of positive events
  when they did not exceed the WHO Alert Level 1 threshold"* — with precision 0.49 vs sensitivity 0.88.

## 5. Official code deposit — EPA ScienceHub `INLA_CONUS_forecast`
URL: https://doi.org/10.23719/1529140 → https://catalog.data.gov/dataset/inla_conus_forecast
Resource: https://pasteur.epa.gov/uploads/10.23719/1529140/INLA_CONUS_forecast.zip
License: https://pasteur.epa.gov/license/sciencehub-license.html · Contact: schaeffer.blake@epa.gov

- README (verbatim, preserved at `INLA_CONUS_forecast-README.md`): *"This repository contains all code
  used in the INLA cyanobacteria study. It does not, however, include inpute [sic] files due to file
  size limitations. All input files are publicallly [sic] available for free download."*
- Workflow steps (README): week assignments → lake morphology → CyAN preprocessing/ice-mask/per-lake
  weekly stats → ice tibble (winter "no bloom" relabel) → PRISM download+weekly means → RF water temp
  (`github.com/bschaeff/SW_Model`) → `compile_data.R` → `conus_inla.R` (model + uncertainty outputs).
- Ice-relabel purpose (verbatim): *"replace missing bloom values with 'no bloom,' which creates a more
  balanced dataset for training the INLA model, especially in winter months."*

## 6. EPA public-domain / no-warranty basis
URL: https://www.epa.gov/web-policies-and-procedures/epa-disclaimers — EPA-produced data are public
domain by default (17 U.S.C. §105) with a no-warranty disclaimer (mirrors the `EPA-NARS` §12 basis).

---

## 7. Live probe log (2026-07-02) — our own checks

**Server identity / access model** `[probe]` (curl):
- `awsedap.epa.gov` → `Server: Microsoft-HTTPAPI/2.0`; sets `X-Qlik-Session-public` cookie ⇒ **Qlik
  Sense Enterprise on Windows**, anonymous **`public`** virtual proxy.
- `/` → 301 `/hub/`; `/hub/` → **302 → /internal_forms_authentication/** (auth required);
  `/api/v1/apps` → **302 auth**; `/sense/app/<appid>` → **302 auth**.
- `/public/single/?appid=…&sheet=…` → **200**, 3,428 B bootstrap HTML (anonymous render OK).
- ⇒ **No anonymous REST API; only published public apps render.** Confirms "no official file/API."

**QIX WebSocket extraction** `[probe]` (`qix_probe.py`, `qix_probe2.py`):
- Connect `wss://awsedap.epa.gov/public/app/<appid>?Xrfkey=<16>` + header `X-Qlik-Xrfkey` + session
  cookie + Origin → `OnAuthenticationInformation userId="anonymous…"`, `OnConnected SESSION_CREATED`.
- `OpenDoc` → doc handle; `GetTablesAndKeys` → data model.
- App `c98935c5…`: table `Data` (Date, WeekEndDate, State, Lake_name_for_public,
  Percent_chance_of_cyanoHAB, Lat_centroid, Lon_centroid, COMID) + `Data-1(MaxWeekEndDate)`; opened with
  a **default single-week selection** (summary measures returned 1 distinct week).
- Apps `9727f5d1…` and `c00e1007…`: table **`AllWeeks_CyanForecasts`** (adds `EPA_region`, `Year`);
  `c00e1007…` also has `AllWeeks_CyanForecasts-1(MaxYear)`.

**AllWeeks panel characterization** `[probe]` (app `9727f5d1…`, after `ClearAll`):
- `Count(DISTINCT COMID)` = **2191**; `Count(DISTINCT WeekEndDate)` = **48**; distinct lake-weeks =
  **105168** = 2191 × 48; **zero null probabilities**; distinct lake **names** = 2191 = distinct COMID
  (⇒ 1-lake gap vs advertised 2,192; no null/blank COMIDs).
- `Min/Max(WeekEndDate)` = **2025-04-05 / 2026-06-27**; per-year weeks: 2025 = 35, 2026 = 13; every one
  of the 48 dates is a **Saturday**; each week has all 2191 lakes.
- `Percent_chance_of_cyanoHAB` ∈ [0, 99.98], mean ≈ 10; buckets: =0 →164, (0,10)→81,309,
  [10,50)→15,224, ≥50 →8,471.
- Sample rows (latest, ME): `Pleasant Lake (ME 1)` COMID 759 @46.02266,−68.1624 → 0.02%; etc.

**Deterministic full extraction contract** `[probe]`:
- Straight-table hypercube of all 10 fields → `qSize = {qcx:10, qcy:105168}`; Qlik ~10k-cell page cap ⇒
  1,000 rows/page; paged `GetHyperCubeData` **106 pages → exactly 105,168 rows in ~30 s**, count
  asserted == `qcy`. No null/blank COMID rows across the full read.

**Official artifact** `[probe]` (curl HEAD + download):
- `INLA_CONUS_forecast.zip` → HTTP 200, `Content-Length: 33677`, `Content-Type: application/zip`,
  `Last-Modified: Sat, 11 Nov 2023 01:30:15 GMT`, sha256
  `126f7f3fd9f79bdb36083009f726ecbe2d9047b728b7ac95bb2498545cf84afb`; 12 files (11 `.R` + `README.md`),
  **code only, no input data**.

**Official-feed search** `[probe]`: data.gov CKAN + web search surfaced **no** ArcGIS/ESRI feature
service, WMS/WFS, CSV, or GeoTIFF distribution of the *operational* forecast; the only official deposit
is the code ZIP above. (A "GeoTIFF daily/7-day composite" seen in some summaries is the **CyAN satellite
product**, not this forecast.)
