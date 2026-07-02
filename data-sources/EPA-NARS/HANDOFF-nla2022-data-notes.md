# Handoff notes on the NLA 2022 samples (from a viz session)

> Context drop for the session that pulled the NARS data. Written 2026-07-01 by a sister
> session while building a NC-statewide layered viz on `data/raw/nla2022/`. **FYI only** —
> nothing here requires action; it's so our METADATA/QA stay consistent and you know a viz
> was added. Delete this file once absorbed.

## Survey design (verified in siteinfo)
- File = **3,880 rows / 3,784 distinct SITE_IDs**, but only **981 are the core probability
  sample** (`WGT_TP_CORE_NLA > 0`). The rest: oversample panels (`PANEL_USE` 22Over/17Over,
  ~2,760), NES legacy sites (`WGT_TP_NES > 0`, 153), and **1,691 NonTarget** (`TNT_CAT`) drawn
  but dry/not-a-lake/inaccessible. Only weighted core rows support national/regional estimates.
  Core weights sum to ~**268,018** (target population represented).
- Strata: ecoregion (10 L1), state (`STRATUM`), lake size class (`PROB_CAT`: 1-4/4-10/10-50/>50 ha).

## Sampled vs evaluated (matters for coords + QA)
- **`INDEX_LAT_DD`/`INDEX_LON_DD` (actual sampled point) exist only for physically-sampled
  lakes.** Non-sampled frame sites have only `LAT_DD83`/`LON_DD83` (design coord). Example (NC):
  22 lakes → 17 site-visits with INDEX coords = **15 distinct sampled lakes** (2 revisited) +
  **7 evaluated-not-sampled**. Recommend distinguishing these in any per-lake product (never
  silently drop the not-sampled ones).

## Per-lake sample structure
- One index site per lake (near-deepest/center), single grab / photic-integrated sample.
  Sampled **once** in the summer index period; ~10% revisited ~2-4 wks later (`VISIT_NO=2`) for
  repeatability — **revisits carry WGT=0** (no double-count). So per lake = 1-2 time points in one
  summer; **not a time series**. Cross-year signal only via 5-yr cycles (2007/2012/2017/2022),
  in aggregate.

## Measurement bundles + flags
- Water chem (`waterchem_wide`): ~20 analytes as `<ANALYTE>_RESULT` with matching
  `_UNITS/_MDL/_RL/_NARS_FLAG/_QA_FLAG` (TP=`PTL`, TN=`NTL`, chl-a=`CHLA`, + dissolved fractions,
  ions, `PH`, `COND`, `ANC`, `DOC`, `TURB`, `COLOR`, `SILICA`). **Quirk: `CHLA` has NO `_UNITS`
  column** (µg/L by convention) — don't assume every analyte has `_UNITS`.
- Toxins (`algaltoxins`, LONG format): ANALYTE codes **`MICX`** (microcystin), **`CYLSPER`**
  (cylindrospermopsin); `RESULT` + `MDL/RL` + `NARS_FLAG`. `NARS_FLAG=ND` = **left-censored
  non-detect** (RESULT blank) — keep distinct from 0/NaN. NC: microcystin 7 detects (all <0.5 µg/L,
  well under EPA rec. 8) / 8 ND; cylindrospermopsin 3 detects / 12 ND.
- Secchi (`secchi`): `DISAPPEARS`/`REAPPEARS` (mean = depth) + `INDEX_SITE_DEPTH`.
- You pulled 4 modules (siteinfo, waterchem_wide, algaltoxins, secchi). Full 2022 also publishes
  phyto/zoo/benthos/sediment/physical-habitat/atrazine/enterococci at the same URLs (not needed
  for HAB fusion).

## Geographic sparseness (fidelity)
- ~981-lake national probability sample → most counties have 0-1 lakes. Orange County, NC = **0**
  (confirmed via FIPS 37135). Expected, not a gap. County/local asks should redirect (statewide,
  or WQP for true local coverage).

## Viz added (avoid duplicate work)
- Added `make_layered_state_map()` + a `--state` flag to `viz/viz_nars.py`:
  `python viz_nars.py --state NC` → `outputs/nla2022_<state>_layered_map.html`. One marker per
  sampled lake; togglable FeatureGroup per variable (chl-a/TP/TN/microcystin/cylindrospermopsin/
  Secchi/turbidity/pH/conductivity); radio toggle; full per-lake popup (all values, all visits);
  ND = hollow grey; "evaluated, not sampled" layer; standard UNWEIGHTED/not-an-estimate labels.
  Values cross-checked exact vs source. **Uncommitted** as of this note — flag if it collides with
  in-progress edits to that file.
