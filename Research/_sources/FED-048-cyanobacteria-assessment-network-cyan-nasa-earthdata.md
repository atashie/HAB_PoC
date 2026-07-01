---
key: FED-048
title: Cyanobacteria Assessment Network (CyAN) | NASA Earthdata
authors_or_org: NASA Earthdata (page); dataset producer credited as NASA Ocean Biology Processing Group (OBPG); multi-agency project partners: EPA, USGS, NOAA
year: 2025 (current data version 6.0; release notes referenced by filename as Aug 2025 — the page does not give an explicit page-publication date or project-founding year)
url: https://www.earthdata.nasa.gov/data/projects/cyan
access_date: 2026-07-01
tier: FED
source_type: Web resource — federal agency data-project documentation page (NASA Earthdata project/dataset landing page with embedded dataset citation, DOI, and technical specifications)
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Cyanobacteria Assessment Network (CyAN) | NASA Earthdata

**What it is.** A NASA Earthdata project/documentation page describing the Cyanobacteria Assessment Network (CyAN) — a multi-agency (EPA, USGS, NOAA) effort that produces the satellite-derived Cyanobacteria Index (CI) data product (from MERIS and Sentinel-3 OLCI ocean-color imagery) to detect and quantify cyanobacteria blooms in U.S. lakes and estuaries, and that documents the product's resolution, DN-to-concentration conversion, current version/DOI, and access tools.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** CyAN is a multi-agency project (EPA, USGS, NOAA) providing satellite-based detection and quantification of cyanobacteria algal blooms in U.S. lakes and estuaries.
  - *evidence:* Stated as the page's opening definitional sentence; the three agencies are separately listed under a 'Partners' heading (as linked items, without an elaborating sentence on individual roles). (Page introduction; 'Partners' section)
  - *quote:* "The Cyanobacteria Assessment Network (CyAN) is a multi-agency project to support the environmental management and public use of U.S. lakes and estuaries by providing a capability of detecting and quantifying cyanobacteria algal blooms."
- **[✓ verified]** The Cyanobacteria Index (CI) data product is built from three sequential/overlapping ESA ocean-color sensor records — MERIS (2002-2012), OLCI on Sentinel-3A (2016-present), and OLCI on Sentinel-3B (2018-present) — and is issued as daily GeoTIFFs plus 7-day maximum-value composites.
  - *evidence:* Direct product/sensor description sentence on the page. (Data products / sensors section)
  - *quote:* "The CI data products available are GeoTIFF dailies and a 7-day maximum value composites from different ESA sensors: MERIS (2002-2012) and the Ocean and Land Colour Instrument (OLCI) on Sentinel-3A (2016-present) and OLCI on Sentinel-3B (2018-present)."
- **[✓ verified]** The CI product has a 300 m sensor spatial resolution, with a 50 m land mask for CONUS versus a coarser 500 m land mask for Alaska.
  - *evidence:* Directly stated resolution figures. (Data products / resolution section)
  - *quote:* "The sensor spatial resolution is 300m. The contiguous US images use a 50m land mask, while the Alaska product uses a less refined 500m land mask."
- **[✓ verified]** MERIS senses across a 390 nm to 1040 nm spectral range.
  - *evidence:* Direct sensor-description sentence. (Sensor description section)
  - *quote:* "MERIS is a medium-spectral resolution imaging spectrometer on board Envisat-1, capable of sensing in the 390 nm to 1040 nm spectral range."
- **[✓ verified]** Raw pixel Digital Numbers (DN) are converted to a cyanobacteria cell-density estimate via a specified log-linear formula, with valid outputs spanning roughly 10,000 to 7,000,000 cells/mL.
  - *evidence:* Explicit conversion formula and output range given on the page for interpreting the CI product. (DN-to-CI conversion / data interpretation section)
  - *quote:* "CIcyano=10^(DN∗0.011714−4.1870866)"
- **[✓ verified]** The DN scale reserves specific values for non-quantitative conditions: 0 = below the CI detection limit, 1-253 = valid data, 254 = land, and 255 = no data (e.g., cloud cover) — i.e., the product cannot quantify cyanobacteria under clouds, over land, or below its detection floor on any given pixel/day.
  - *evidence:* Explicit DN legend/color-code text on the page. (DN legend / data interpretation section)
  - *quote:* "0 indicates below threshold of CI detection limits (grey color)... 1-253 are data... 254 is land (brown)... 255 are no data (black—e.g., a cloudy pixel)"
- **[✓ verified]** The current CyAN CI dataset is processed to Version 6.0, produced by the NASA Ocean Biology Processing Group (OBPG) and citable via a specific DOI.
  - *evidence:* Full formal dataset citation string and DOI given for users to cite the data. (Version / citation section)
  - *quote:* "NASA Ocean Biology Processing Group (OBPG). Cyanobacteria Assessment Network (CyAN), Merged Sentinel-3A and Sentinel-3B OLCI Regional Mapped Cyanobacteria Index (CI) Data, version 6.0; DOI 10.5067/MERGED-S3/OLCI/L3M/CYAN/CI/6.0"
- **[✓ verified]** Data quality/coverage is explicitly tied to satellite availability: 'best coverage' is only available since 2018, once both Sentinel-3A and Sentinel-3B OLCI sensors were operating together.
  - *evidence:* Direct statement linking coverage quality to the two-satellite era. (Temporal resolution / coverage section)
  - *quote:* "The temporal resolution depends on the sensor and date with best coverage since 2018, as images utilize sensors on two Sentinel-3 satellites."
- **[✓ verified]** CONUS CI data are organized into a discrete column/row tile grid rather than one continuous national raster (Alaska has its own separate tile map).
  - *evidence:* Direct statement on spatial data organization; the page includes tile maps for both regions but does not give a total tile count. (Data access / tiling section)
  - *quote:* "Data produced for CONUS is delivered in tiles referred to as the column number followed by row number."
- **[✓ verified]** The page itself provides no inline validation/accuracy statistics and no stated count of monitored lakes or reservoirs; it explicitly defers 'interpretation, limitations and known issues' to a separate Version 6 release-notes document that is linked but not reproduced on this page.
  - *evidence:* Confirmed as an absence across three targeted re-fetches of the page that explicitly searched for a lake count, validation/accuracy language, and an inline limitations list; none were found — only a pointer to the release notes document. (Whole-page scan; 'Documentation'/release-notes reference)
  - *quote:* "provide an overview on CyAN data and imagery production, interpretation, limitations and known issues"
- **[✓ verified]** Multiple software tools support working with CyAN CI data: a CyAN File Search API, an EPA CyAN mobile app (via Google Play), SeaDAS, and RS_Toolbox for ArcGIS, with RS_Toolbox versioned separately for ArcGIS 10 (v2.3.1) and ArcGIS Pro (v3.1.4).
  - *evidence:* Direct tool/version listing under the access-and-tools portion of the page. (Access & Tools section)
  - *quote:* "RS_Toolbox, v2.3.1 ... RS_Toolbox, v3.1.4"

## Data / numbers
- 300 m — sensor spatial resolution of the CyAN Cyanobacteria Index (CI) product
- 50 m — land mask resolution used for CONUS imagery
- 500 m — land mask resolution used for Alaska imagery (page describes it as 'less refined' than the CONUS mask)
- 2002–2012 — MERIS sensor period contributing to the CI record
- 2016–present — OLCI on Sentinel-3A period
- 2018–present — OLCI on Sentinel-3B period; page states 'best coverage since 2018' once both Sentinel-3 satellites were contributing
- 390 nm to 1040 nm — MERIS spectral sensing range stated on the page
- DN 0 = below CI detection threshold (grey); DN 1–253 = valid data; DN 254 = land (brown); DN 255 = no data, e.g. a cloudy pixel (black)
- CI_cyano = 10^(DN × 0.011714 − 4.1870866) — stated DN-to-cyanobacteria-index conversion formula
- ~10,000 to 7,000,000 cells/mL — stated valid output range of CI_cyano
- Version 6.0 — current CyAN CI data processing version; DOI 10.5067/MERGED-S3/OLCI/L3M/CYAN/CI/6.0
- RS_Toolbox v2.3.1 — stated as compatible with ArcGIS 10
- RS_Toolbox v3.1.4 — stated as compatible with ArcGIS Pro

## Methods
The page documents (rather than performs) a remote-sensing data-production pipeline: the Cyanobacteria Index (CI) algorithm is applied to ocean-color reflectance from ESA sensors — MERIS (2002-2012) and OLCI aboard Sentinel-3A (2016-present) and Sentinel-3B (2018-present) — to produce per-pixel Digital Numbers (DN) at 300 m sensor resolution, masked with a 50 m (CONUS) or 500 m (Alaska) land mask, and delivered as daily GeoTIFFs plus 7-day maximum-value composite tiles organized in a column/row grid. DN values are converted to a quantitative cyanobacteria index/cell-density estimate via the stated formula CI_cyano = 10^(DN × 0.011714 − 4.1870866), valid over roughly 10,000-7,000,000 cells/mL for DN 1-253; DN 0, 254, and 255 are reserved flags (below-detection, land, and no-data/cloud respectively) rather than quantitative values. The current release is Version 6.0 (DOI 10.5067/MERGED-S3/OLCI/L3M/CYAN/CI/6.0), distributed through NASA's OB.DAAC with a dedicated CyAN File Search API, and made usable via SeaDAS, RS_Toolbox for ArcGIS (v2.3.1 for ArcGIS 10; v3.1.4 for ArcGIS Pro), and an EPA CyAN mobile app. Where the source itself states the method 'works' or is constrained: it explicitly ties 'best coverage' to the post-2018 dual-Sentinel-3 era, and it explicitly reserves DN 254/255 for pixels where no CI value can be produced (land / cloud or missing data) and DN 0 for concentrations below the algorithm's detection limit — i.e., the method does not produce a quantitative estimate in those cases. The page does not itself report accuracy, validation, or in-situ comparison statistics for the CI algorithm.

## Stated limitations
The fetched page does not contain an inline "Limitations" section; it explicitly delegates "interpretation, limitations and known issues" to a separate Version 6 release-notes document (referenced only by a filename suggesting Aug 2025) that was not itself retrieved, so no further limitations text from that document can be reported without fabrication. Constraints that ARE stated directly on this page: (1) DN=0 pixels are "below threshold of CI detection limits," i.e., the algorithm has a non-zero detection floor below which cyanobacteria cannot be quantified; (2) DN=254 (land) and DN=255 (no data, e.g., cloud) pixels yield no CI value at all, meaning land cover and cloud cover both block retrieval for a given pixel/day; (3) the Alaska land mask (500 m) is explicitly called "less refined" than the CONUS land mask (50 m), implying coarser land/water discrimination and by extension less precise shoreline handling in Alaska; (4) "best coverage" is only available "since 2018," implying weaker/sparser coverage in earlier periods (2002-2012 MERIS-only, and 2016-2018 single-satellite OLCI). The page states no accuracy/validation statistics and no count of lakes or water bodies monitored.

## Tensions with other findings
This page is a data/product specification rather than a peer-reviewed evaluation, so it does not itself argue against other HAB literature. However, its own stated constraints imply a general remote-sensing-vs-in-situ tension relevant to this project's satellite+in-situ fusion approach: a 300 m sensor pixel size, a non-zero CI detection floor (DN=0), and complete signal loss under cloud cover (DN=255) or over land (DN=254) mean the CyAN CI product cannot resolve blooms in water bodies or nearshore areas smaller than its footprint, cannot quantify concentrations below its detection limit, and produces no reading at all on cloudy days for a given tile — whereas in-situ point measurements (e.g., Water Quality Portal chlorophyll-a/nutrient samples) can sample at a single location regardless of cloud cover but lack CyAN's spatial sweep and daily/weekly cadence across many lakes. This complementary-blind-spot relationship (rather than a direct contradiction) is inferred from this page's own stated specs; the source itself does not discuss in-situ comparison.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All 11 claims are directly supported by the source text with no hallucinated numbers, no material dropped caveats, and no unsupported assertions. The claims accurately reflect both explicit statements (e.g., sensor dates, resolution specifications, tool versions, DN legend values) and reasonable inferences from explicit information (e.g., the implication that tiled delivery means non-continuous raster structure). The source text is complete enough to verify all factual content in the claims."

## Provenance
- Canonical URL: https://www.earthdata.nasa.gov/data/projects/cyan
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Primary URL fetched directly and resolved correctly on the first attempt (no redirect, no block, content matched the given title exactly), so no WebSearch fallback was needed. Because WebFetch routes page content through a summarizing model, I made three additional targeted WebFetch passes on the SAME URL specifically asking for exact verbatim quotes (not paraphrases) for every number, threshold, formula, version, and DOI, and separately asked the tool to explicitly confirm or deny (rather than infer) items such as a monitored-lake count, validation/accuracy statistics, an explicit inline limitations list, and whether 'OB.DAAC' is spelled out on the page. Results: this NASA Earthdata project page does NOT state a lake/reservoir count, does NOT state validation or accuracy statistics, and does NOT spell out 'OB.DAAC'; it also does not give an inline limitations/known-issues list, instead pointing to a separate Version-6 release-notes document (referenced by filename as 'Aug 2025') that was not itself fetched. I have not included any of those absent items as findings, and have not substituted outside/training knowledge (e.g., commonly cited '2,000+ lakes' figures elsewhere in the CyAN literature) since it was not present in this specific fetched page.
