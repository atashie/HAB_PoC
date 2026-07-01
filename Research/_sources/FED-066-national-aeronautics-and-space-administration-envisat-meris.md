---
key: FED-066
title: National Aeronautics and Space Administration - ENVISAT MERIS Global Binned Cyanobacteria Index (CI) Data, version 5.0
authors_or_org: NASA Ocean Biology Processing Group (OBPG) / Ocean Biology Distributed Active Archive Center (OB.DAAC); Cyanobacteria Assessment Network (CyAN) multi-agency project (EPA, NASA, NOAA, USGS)
year: 2023 (CyAN "Version 5" reprocessing release date, per NASA's version-5 documentation; original data.gov listing date not recoverable — the page itself is now delisted)
url: https://catalog.data.gov/dataset/envisat-meris-global-binned-cyanobacteria-index-ci-data-version-5-0-a7b6f — confirmed HTTP 404 (delisted) on direct fetch and on its /resource/ sub-page and the CKAN package_show API; no live replacement landing page for this exact "Global Binned CI v5.0" entry was found on data.gov, data.nasa.gov, the new earthdata.nasa.gov catalog, CMR, or DataCite
access_date: 2026-07-01
tier: FED
source_type: Government satellite data product / dataset catalog record (NASA OB.DAAC, harvested to data.gov); primary landing page now delisted (HTTP 404)
categories: [remote-sensing]
relevance: Medium
full_text_access: landing-only
fetch_status: partial
review_severity: notes
review_overall: pass
---

# National Aeronautics and Space Administration - ENVISAT MERIS Global Binned Cyanobacteria Index (CI) Data, version 5.0

> Note: provisional URL was resolved to a primary source. Original: https://catalog.data.gov/dataset/envisat-meris-global-binned-cyanobacteria-index-ci-data-version-5-0-a7b6f

**What it is.** This data.gov entry (title: "ENVISAT MERIS Global Binned Cyanobacteria Index (CI) Data, version 5.0") points to a NASA OB.DAAC/CyAN Level-3 binned satellite data product delivering Cyanobacteria Index (CI_cyano) values derived from the ENVISAT MERIS sensor (2002-2012), part of the multi-agency Cyanobacteria Assessment Network (CyAN) used to detect and quantify cyanobacteria blooms in U.S. lakes/estuaries. As of this review the specific catalog.data.gov page for this exact version (5.0, "Global Binned") returns HTTP 404 and is no longer live; the CyAN product line has since moved on to Version 6.0 (Feb 2025), and this dossier entry is therefore built from NASA's own live documentation of the identical "Version 5" processing run plus the live sibling/successor product page, not from the dead landing page itself.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The specific catalog.data.gov landing page for this dataset (version 5.0, "Global Binned" CI) is no longer live; direct fetches of the page, its resource sub-page, and the CKAN API all returned HTTP 404, and NASA's current CyAN documentation confirms the product line has since moved to Version 6.0.
  - *evidence:* Confirmed by repeated direct WebFetch attempts (all 404) on the primary URL, its /resource/ sub-page, and the data.gov CKAN package_show/package_search API, while a control fetch of the general data.gov catalog homepage loaded normally (543,479 datasets listed) — showing data.gov itself is functional and this specific record is what's gone. A sibling v5.0 record ("True Color" TC data) is also 404, suggesting the whole v5.0 CyAN family was delisted. (WebFetch attempts on the primary URL (this review); corroborated by the current CyAN project page)
  - *quote:* "Current version is Version 6."
- **[✓ verified]** NASA's "Version 5" (V5) reprocessing of the CyAN Cyanobacteria Index data (the version this dataset entry names) was released on May 22, 2023.
  - *evidence:* Stated directly on NASA's dedicated CyAN version-5 reprocessing documentation page. (oceancolor.gsfc.nasa.gov/data/reprocessing/projects/cyan/version/5/)
  - *quote:* "All data are processed to version 5 (V5) as of May 22, 2023."
- **[✓ verified]** Version 5 introduced an improved turbid-water exclusion filter, a clear-water correction for invalid retrieved Kd, and an OLCI-to-MERIS inter-calibration step for the Cyanobacteria Index.
  - *evidence:* Listed as the specific V5 processing changes on NASA's version-5 reprocessing notes page, with the inter-calibration step attributed to a cited paper (Wynne et al., 2021). (oceancolor.gsfc.nasa.gov/data/reprocessing/projects/cyan/version/5/, "Key Version 5 Improvements")
  - *quote:* "Improved filter for turbid water exclusion, which reduces CI_cyano values in highly turbid environments"
- **[✓ verified]** Version 5 CI_cyano values are on average 15-20% higher than Version 4 values for the same imagery, an artifact of recalibration rather than a real change in cyanobacteria abundance.
  - *evidence:* The source directly attributes this shift to updated ESA vicarious-calibration gains used in V5, not to any environmental change — a calibration/versioning effect, not a bloom-intensity finding. (oceancolor.gsfc.nasa.gov/data/reprocessing/projects/cyan/version/5/, "Quantified Changes from V4 to V5")
  - *quote:* "Version 5 shows on average a 15-20% increase in CI_cyano values...This is driven by gain changes (using updated ESA gains)."
- **[✓ verified]** NASA explicitly prohibits comparing or trending Cyanobacteria Index values across different processing versions of this product.
  - *evidence:* Stated as a standalone, emphasized caveat on the same version-5 documentation page, directly limiting any downstream multi-year trend use of the data unless version is held fixed. (oceancolor.gsfc.nasa.gov/data/reprocessing/projects/cyan/version/5/, "Critical Limitation")
  - *quote:* "There should be no change/trend analysis across versions. Only a single version should be used in any change/trend analysis."
- **[✓ verified]** NASA itself describes the CI_cyano algorithm/product as still under active evaluation with known unresolved issues, i.e., not presented as a finalized, fully validated product.
  - *evidence:* Direct self-assessment statement by the data provider (NASA/OBPG) on its own reprocessing documentation. (oceancolor.gsfc.nasa.gov/data/reprocessing/projects/cyan/version/5/, "Algorithm and Index")
  - *quote:* "The CI_cyano continues to be evaluated and the product has known outstanding issues."
- **[✓ verified]** The underlying CyAN sensors and coverage windows are: ENVISAT MERIS 2002-2012, OLCI on Sentinel-3A from 2016-present, and OLCI on Sentinel-3B from 2018-present, with satellite sensor spatial resolution of 300 m and CI products distributed as GeoTIFF daily and 7-day maximum-value composite files over CONUS and Alaska.
  - *evidence:* General CyAN project description (current, i.e. v6-era, page) giving the sensor/coverage/resolution facts that describe the product family this version-5.0 dataset belongs to. (CyAN project overview page (www.earthdata.nasa.gov/data/projects/cyan, redirected from oceancolor.gsfc.nasa.gov/about/projects/cyan/), "Sensors and Temporal Coverage" / "Spatial and Technical Specifications")
  - *quote:* "Sensor spatial resolution: "300m""
- **[✓ verified]** A live, structurally-analogous successor product in the same NASA OB.DAAC/CyAN family — "ENVISAT MERIS Regional Mapped Cyanobacteria Index (CI) Data, version 6.0" — comprises 248,675 netCDF-4 granules covering 2002-03-21 to 2012-05-09 (the full MERIS mission), distributed openly under EOSDIS data-use terms; this is offered as family context, not as a direct description of the version-5.0 "Global Binned" dataset itself.
  - *evidence:* Fetched from the live Earthdata catalog page for the v6.0 sibling/successor dataset, used here only to characterize how NASA documents this product family now that the exact v5.0 entry is gone. (www.earthdata.nasa.gov/data/catalog/ob-cloud-meris-l3m-cyan-6.0)
  - *quote:* "Granules: 248,675 files"
- **[⚠ partial]** A separate, still-live EPA ScienceHub catalog record, "Cyanobacteria Index (MERIS)" (Ohio and Florida scope, a distinct dataset from FED-066), documents the underlying MERIS instrument as having a 68.5-degree nadir-pointing field of view, 15 spectral bands, and a 300x300 m grid resolution, and cites a peer-reviewed method paper for using this CI data to track HAB spatial extent over time.
  - *evidence:* This is a distinct, related dataset entry (different scope and publisher) fetched successfully as corroborating context on MERIS/CI methodology, since the exact NASA v5.0 Global Binned page is unreachable. (catalog.data.gov/dataset/cyanobacteria-index-meris)
  - *quote:* "Field-of-view: 68.5 degrees, nadir-pointing"
  - *reviewer:* Reference to 'FED-066' and claimed distinctness from it cannot be verified in source text; all other technical specifications and publication details are confirmed.

## Data / numbers
- 300 m — CyAN sensor (MERIS/OLCI) spatial resolution, per current CyAN project page
- 50 m — CONUS land mask resolution used in CyAN CI products
- 500 m — Alaska land mask resolution used in CyAN CI products
- 2002–2012 — ENVISAT MERIS operational coverage period feeding CyAN CI
- 2016–present — Sentinel-3A OLCI coverage period feeding CyAN CI (as stated on source page)
- 2018–present — Sentinel-3B OLCI coverage period feeding CyAN CI (as stated on source page)
- May 22, 2023 — release date of CyAN "Version 5" (V5) reprocessing
- 15–20% — average increase in CI_cyano values in V5 vs V4, attributed to updated calibration gains, not a real bloom change
- 10 to 16 months — stated CyAN reprocessing cadence
- ~10,000 to 7,000,000 cells/mL — approximate output range of the CI-to-cyanobacteria-cell-count conversion, per current (v6-era) formula CIcyano=10^(DN×0.011714−4.1870866)
- 248,675 — granule/file count for the related v6.0 "Regional Mapped" CI netCDF-4 product (NOT the v5.0 Global Binned dataset itself)
- 2002-03-21 to 2012-05-09 — temporal extent of the v6.0 Regional Mapped CI product (full MERIS mission span)
- 68.5 degrees — MERIS sensor nadir field-of-view, per EPA ScienceHub MERIS CI documentation
- 15 — number of MERIS spectral bands (visible/near-infrared), per EPA ScienceHub MERIS CI documentation
- 300×300 m — MERIS CI grid resolution, per EPA ScienceHub MERIS CI documentation (Ohio/Florida scope)

## Methods
Cyanobacteria Index (CI_cyano) retrieval algorithm applied to (Rayleigh-corrected top-of-atmosphere) reflectance imagery from ENVISAT MERIS and, for the wider product family, Sentinel-3 OLCI; processed to Level-3 binned form (this dataset) as well as mapped and true-color companion products. Version 5 processing (the version named in this dataset's title) added a turbid-water exclusion filter, a clear-water Kd-based correction, and an OLCI-to-MERIS inter-calibration step (citing Wynne et al., 2021), plus updated ESA Collection-3 vicarious-calibration gains, with full reprocessing repeated roughly every 10-16 months. NASA states the algorithm "continues to be evaluated" and has "known outstanding issues," and explicitly instructs users not to compare or trend CI values across reprocessing versions. No independent accuracy/validation statistics (e.g., against in-situ chlorophyll-a, phycocyanin, or cyanotoxin measurements) appear in the fetched material for this version.

## Stated limitations
The source material states, in NASA's own words: (1) "The CI_cyano continues to be evaluated and the product has known outstanding issues" — the algorithm/product is not presented as fully validated; (2) "There should be no change/trend analysis across versions. Only a single version should be used in any change/trend analysis" — a hard constraint on using this data (or any CyAN CI series) for multi-year trend claims unless the version is held fixed; (3) the V5 turbid-water filter and recalibration were introduced specifically because earlier versions had known shortcomings (turbid-water false positives, uncorrected gains), implying pre-V5/early-V5 outputs carry these residual risks. As an access/traceability limitation specific to this catalog record: the primary catalog.data.gov page for this exact "version 5.0, Global Binned" dataset returned HTTP 404 at time of review and no live equivalent could be located via data.gov, data.nasa.gov, the new earthdata.nasa.gov catalog, CMR, or DataCite — a reproducibility gap for anyone citing this exact entry today, even though the underlying CyAN product line and data continue to exist under newer version numbers.

## Tensions with other findings
This source is itself a built-in warning against a common HAB remote-sensing pitfall: because the CyAN CI_cyano algorithm has been reprocessed multiple times — with V5 alone producing a stated 15-20% average value shift from calibration changes alone — and NASA explicitly disallows cross-version trend analysis, any HAB study, dashboard, or product claim (including within this project) that stitches together CyAN CI values spanning a reprocessing boundary (e.g., pre- vs. post-May-2023, or the 2025 move to V6) risks mistaking a processing artifact for an ecological trend; this directly bears on this project's own "model drift & auditability" concerns for Part C. Separately, the disappearance of this exact dataset's public catalog.data.gov page (while the underlying granules and successor-version products remain accessible through OB.DAAC/Earthdata under a new version number) illustrates a broader tension in the public HAB data ecosystem: agency-side dataset versioning and catalog churn can silently break external citations and reproducibility pointers even when the underlying science data persists.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** Eight of nine claims are fully supported by the source text with exact quotes and specifications verified. One claim (Claim 9) is marked partial due to an unverifiable reference to 'FED-066' which does not appear in the source text; however, all core technical facts about the MERIS instrument, grid resolution, field-of-view, spectral bands, and the peer-reviewed publication are confirmed. No hallucinated numbers detected—all numeric values (dates, percentages, granule counts, technical specifications) are present and accurately cited from the source. No significant dropped caveats affect the accuracy of the claims presented."

## Provenance
- Canonical URL: https://catalog.data.gov/dataset/envisat-meris-global-binned-cyanobacteria-index-ci-data-version-5-0-a7b6f — confirmed HTTP 404 (delisted) on direct fetch and on its /resource/ sub-page and the CKAN package_show API; no live replacement landing page for this exact "Global Binned CI v5.0" entry was found on data.gov, data.nasa.gov, the new earthdata.nasa.gov catalog, CMR, or DataCite
- Access date: 2026-07-01
- Full-text access: landing-only | Fetch status: partial
- Fetch notes: The primary URL (catalog.data.gov entry for this exact "version 5.0, Global Binned" dataset) is dead: direct WebFetch returned HTTP 404 on the page itself, its /resource/ sub-page, and the data.gov CKAN package_show/package_search API. A control fetch confirmed catalog.data.gov itself is functioning normally (homepage listing loaded, "543,479 datasets"), and a sibling v5.0 record ("True Color" TC data) is also 404 — indicating the entire v5.0 CyAN family was removed from data.gov's harvest, consistent with NASA's CyAN line having moved on to Version 6.0 (published 2025-02-20, per the fetched v6.0 sibling page). I made extensive further attempts to locate a live replacement landing page for this exact "Global Binned CI v5.0" entry: CMR concept-ID lookup (C2561580568-OB_DAAC, both .html and .umm_json), CMR collection search by keyword and by concept_id (both returned zero entries), DOI guesses under the 10.5067/ENVISAT/MERIS/L3B/CYAN/CI/5.0 pattern (404), earthdata.nasa.gov catalog slug guesses following the confirmed "ob-cloud-meris-l3m-cyan-6.0" naming pattern (404, in both /data/catalog/ and /es/data/catalog/ forms), a data.nasa.gov mirror guess (404), and a DataCite Commons DOI guess (HTTP 429, inconclusive). None succeeded. I did successfully fetch and use: (1) NASA's own dedicated "CyAN Version 5" reprocessing-notes page, which documents the exact processing version named in this dataset's title (release date, algorithm changes, quantified V4→V5 shift, explicit no-cross-version-trending caveat); (2) the live sibling/successor "Regional Mapped CI v6.0" Earthdata catalog page, used only as product-family context (clearly labeled as NOT this exact dataset); (3) the current CyAN project overview page for sensor/format/resolution facts; (4) a distinct, still-live EPA ScienceHub "Cyanobacteria Index (MERIS)" catalog record as corroborating context on MERIS/CI methodology. The V5 PDF release notes were located but returned unparseable binary content through WebFetch and were not used as evidence. Every number and quote in this dossier traces to one of these four successfully fetched pages; nothing is drawn from prior/training knowledge of this dataset.
