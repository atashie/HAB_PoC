# WQP — preserved primary-source statements

Verbatim quotes we rely on, with URL + access date, so the audit trail survives link rot. All accessed
**2026-07-01**. Where a fact was also confirmed by our own live REST probe it is marked **[probe]** and the probe
lives (or will live) in `../access/`.

> Preservation note: these are the *load-bearing sentences* behind `../METADATA.md`. Full-page HTML/PDF snapshots
> can be archived here later if a stronger audit copy is needed; the quotes below are what our claims cite.

---

## 1. Restrictions, disclaimer, citation — WQP User Guide
URL: https://www.waterqualitydata.us/portal_userguide/

- Disclaimer: *"The data are released on the condition that neither the USGS nor the United States Government may
  be held liable for any damages resulting from its authorized or unauthorized use."*
- Provisional: *"The USGS sourced data available on the Water Quality Portal may include data that have not
  received Director's approval and as such are provisional and subject to revision."*
- Provisional→accepted: *"Results are initially coded with a result status of provisional. After review by a
  project hydrologist, the result status is usually changed to accepted."* … *"accepted status does not guarantee
  that results will never be updated."*
- Recommended citation: *"National Water Quality Monitoring Council, YYYY, Water Quality Portal, accessed mm, dd,
  yyyy, hyperlink_for_query, https://doi.org/10.5066/P9QRKUVJ."*
- Delivery format: *"The data are delivered in a format and nomenclature defined by the WQX-Outbound Schema."*

## 2. Update cadence — WQP User Guide
URL: https://www.waterqualitydata.us/portal_userguide/
- *"NWIS (USGS) is updated every 24 hours."*
- *"WQX (EPA) is updated weekly on Thursday evening."*

## 3. Detection/Quantitation limits (censoring) — WQP User Guide
URL: https://www.waterqualitydata.us/portal_userguide/
- *"There can be multiple Result Detection Quantitation limits per result, and they can be linked to results
  retrieved using the 'narrow' result profile using ResultIdentifier."*

## 4. Characteristic naming differences — WQP User Guide
URL: https://www.waterqualitydata.us/portal_userguide/
- *"The nomenclature for WQX (EPA) and USGS characteristics are not identical."*
- DO example: *"The WQX (EPA) lists each dissolved oxygen characteristic, while the USGS classifies dissolved
  oxygen under 'oxygen'"* → to get DO from both, select *"dissolved oxygen"* (WQX) **and** *"oxygen"* (USGS list).

## 5. The 2024-03-11 USGS split — USGS "WQX3.0 Data Now Available" blog
URL: https://waterdata.usgs.gov/blog/wqx3/
- *"USGS data that was collected or analyzed after March 11, 2024, as well as any modification to existing data
  made after this date will not appear in the WQX2.2 profiles."*
- *"we have set up a temporary user interface (https://www.waterqualitydata.us/beta/) to serve these data."*
- *"After the beta user interface has been tested, WQX3.0 data will become the default output."*
- *"WQX2.2 data profiles and web services will remain available for a period of time, then they will be deprecated."*
- Backward compatibility: *"WQX 3.0 is backwards-compatible with prior versions of the WQX standard, meaning that
  data submitted with an earlier version of the standard will still be served to users."*  ← basis for the
  dual-schema **double-count** risk.

## 6. Home-page notice — WQP home
URL: https://www.waterqualitydata.us/
- *"New WQX 3.0 profiles are available at waterqualitydata.us/beta/. These profiles will contain recent USGS data
  added since March 11, 2024, which marks the beginning of limited accessibility for USGS data."*
- *"This user interface only serves WQX2.2 profiles, which do NOT contain USGS data added after March 11, 2024."*

## 7. Source systems / scale — WQP Description
URL: https://www.waterqualitydata.us/wqp_description/
- NWIS: *"current and historical water data from more than 1.5 million sites across the nation."*
- WQX: submissions from *"states, tribes, watershed groups, other federal agencies, volunteer groups, and
  universities."*

## 8. Bulk / throughput guidance — Web-services documentation
URL: https://www.waterqualitydata.us/webservices_documentation/
- Compression: `zip=yes` — *"compression often greatly increases throughput."*
- Sorting: *"For large downloads (over 5 million rows) sorting is disabled by default"*; `sorted=yes` *"increases
  response time significantly, sometimes by orders of magnitude."*
- Long queries: use **HTTP POST** with a JSON payload when GET length limits are hit.
- OGC limit: *"The service supports calls up to 250,000 sites."*

## 9. dataRetrieval status — USGS
URL: https://water.code-pages.usgs.gov/dataretrieval/articles/Status.html
- *"readNWISqw"* retired (superseded by `readWQPqw()`); WQP functions default to legacy, WQX3 options available;
  NWIS discrete water-quality services frozen (March 2024). Use `dataretrieval` only for cross-checks here.

## 10. Live probe log (2026-07-01) — our own checks
- `/data/Station/search?countycode=US:39:095&characteristicName=Chlorophyll a` → **200**, header
  `Total-Site-Count: 20`.
- `/wqx3/Station/search?...` → **200**, 56 columns, all renamed vs legacy (`MonitoringLocationIdentifier` →
  `Location_Identifier`), adds `Location_HUCTwelveDigitCode`, standardized lat/lon, `AlternateLocation_Identifier`.
- `/data/Result/search?...&characteristicName=Microcystin` → **200**, 63-col `resultPhysChem`; rows from org
  `NARS_WQX` (site `NARS_WQX-NGL_OH-10001`), `ResultMeasureValue` seen as `"NA"` with empty
  `ResultDetectionConditionText`.
- `/data/summary/monitoringLocation/search?...&dataProfile=periodOfRecord` → **200**, 19 cols, 1,903 rows for
  Lucas County OH (per site×year×characteristic counts + `LastResultSubmittedDate` + lat/lon + HUC8).
- `/wqx3/summary/monitoringLocation/search?...` → **404** (no Summary service in WQX3).
- `/wqx3/Result/search?...&dataProfile={fullPhysChem,basicPhysChem,narrow}` → **200** for all three.
- **Date format:** `startDateLo=2024-03-12` (ISO) → **400**; `startDateLo=03-12-2024` (MM-DD-YYYY) → **200**.
- **Invalid characteristicName:** `characteristicName=TotallyMadeUpXYZ` → **400**; `Microcystins, total` → **400**
  (not a domain value); `Microcystin` → **200**. One bad name 400s the whole query.
- **Count headers:** legacy Result returns `Total-Site/Activity/Result-Count`; **WQX3 returns none**.
- **Split proof:** post-`03-12-2024` USGS (`providers=NWIS`) Results, Lucas County OH — legacy **0**,
  WQX3 **7,528** (via `discover_wqp.py`, 2026-07-01).
- **WQX3 Result carries detection limits INLINE** (`DetectionLimit_TypeA/MeasureA/…B`) + coords + HUC8/12;
  legacy Result carries none of these (DQL is a separate endpoint; coords/HUC live on Station).
