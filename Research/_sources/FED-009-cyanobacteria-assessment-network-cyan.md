---
key: FED-009
title: Cyanobacteria Assessment Network (CyAN)
authors_or_org: NASA Ocean Biology Processing Group (OBPG) / Ocean Biology Distributed Active Archive Center (OB.DAAC), in partnership with U.S. EPA, USGS, and NOAA
year: Continuously updated project page (not a dated publication); current data processing "Version 6," release notes dated August 2025
url: https://www.earthdata.nasa.gov/data/projects/cyan
access_date: 2026-07-01
tier: FED
source_type: Government multi-agency project webpage (NASA Ocean Color / NASA Earthdata project page describing a satellite data product)
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Cyanobacteria Assessment Network (CyAN)

> Note: provisional URL was resolved to a primary source. Original: https://oceancolor.gsfc.nasa.gov/projects/cyan/

**What it is.** CyAN is a multi-agency (EPA, USGS, NOAA, hosted by NASA's OB.DAAC) project that produces satellite remote-sensing data products — built on a Cyanobacteria Index (CI) algorithm applied to ESA ocean-color sensor data (MERIS, then Sentinel-3 OLCI) — to detect and quantify cyanobacterial algal blooms in U.S. lakes and estuaries (CONUS and Alaska).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** CyAN is a multi-agency project (EPA, USGS, NOAA, with NASA hosting the data at OB.DAAC) providing satellite-based detection and quantification of cyanobacteria algal blooms in U.S. lakes and estuaries.
  - *evidence:* Stated directly in the page's project-description text; identical wording was returned independently across two separate WebFetch calls of the same page, increasing confidence it is verbatim. (Project description / overview section)
  - *quote:* "a multi-agency project to support the environmental management and public use of U.S. lakes and estuaries by providing a capability of detecting and quantifying cyanobacteria algal blooms."
- **[✓ verified]** The project's core output is a satellite-derived Cyanobacteria Index (CI) product, expressed as CI_cyano, covering lakes across the contiguous U.S. and Alaska (CONUS).
  - *evidence:* Stated in the same project-description passage, corroborated verbatim across two independent fetches. (Project description / overview section)
  - *quote:* "satellite remote sensing products using the cyanobacteria index (CI) algorithm to estimate cyanobacteria concentrations (CI_cyano) in lakes across the contiguous United States and Alaska (CONUS)."
- **[⚠ partial]** CI data derive from three sequential ESA ocean-color sensor records: Envisat MERIS (2002-2012), then Sentinel-3A OLCI (2016-present), then Sentinel-3B OLCI (2018-present); delivered as daily GeoTIFFs and 7-day maximum-value composites.
  - *evidence:* Exact sensor names and year ranges stated directly; reproduced identically in a dedicated verbatim-extraction fetch. (Data Products & Technical Specifications section)
  - *quote:* "The CI data products available are GeoTIFF dailies and a 7-day maximum value composites from different ESA sensors: MERIS (2002-2012) and the Ocean and Land Colour Instrument (OLCI) on Sentinel-3A (2016-present) and OLCI on Sentinel-3B (2018-present)."
  - *reviewer:* The source text names the sensor as 'MERIS' but does not explicitly include the 'Envisat' prefix; without external knowledge, this addition cannot be verified against the source text alone.
- **[✓ verified]** The best temporal coverage is achieved from 2018 onward, once two Sentinel-3 satellites (3A and 3B) were both providing OLCI imagery.
  - *evidence:* Directly stated qualitative claim tying coverage quality to dual-satellite operation. (Data Products & Technical Specifications section)
  - *quote:* "best coverage since 2018, as images utilize sensors on two Sentinel-3 satellites."
- **[✓ verified]** The sensor's native spatial resolution is 300 m; the land mask separating water from land is coarser for the Alaska product (500 m) than for CONUS (50 m).
  - *evidence:* Directly stated in a dedicated verbatim-extraction fetch targeting exact resolution wording. (Data Products & Technical Specifications section)
  - *quote:* "The sensor spatial resolution is 300m. The contiguous US images use a 50m land mask, while the Alaska product uses a less refined 500m land mask."
- **[✓ verified]** Digital Number (DN) pixel values (0-255) are converted to a CI_cyano cell-density estimate via a stated exponential formula, with a reported dynamic range of about 10,000 to 7,000,000 cells/mL.
  - *evidence:* Formula and numeric range given directly and reproduced identically across two independent fetches. (Data Products & Technical Specifications section (DN-to-CI_cyano conversion))
  - *quote:* "CIcyano=10^(DN∗0.011714−4.1870866)... That range is ~10,000 to 7,000,000 cells/ml."
- **[✓ verified]** Within the 0-255 DN scale, 0 flags pixels below the CI detection limit, 1-253 are valid data, 254 marks land, and 255 marks no-data (e.g., cloud-covered) pixels.
  - *evidence:* Directly stated DN legend, reproduced consistently across two independent fetches. (Data Products & Technical Specifications section (DN legend))
  - *quote:* "0 indicates below threshold of CI detection limits (grey color) / 1-253 are data / 254 is land (brown) / 255 are no data (black—e.g., a cloudy pixel)"
- **[✓ verified]** Currently distributed CI data are processed to 'Version 6,' with release notes (dated August 2025, per the linked filename) covering production, interpretation, limitations, and version changes; the merged Sentinel-3A/3B OLCI CI product carries a specific citation and DOI.
  - *evidence:* Version number and full citation string given directly on the page; the August 2025 date is corroborated independently by the release-notes PDF's own filename found via search. (Version & citation information section; release notes filename CyAN_NASA_MERISOLCI_CI_release_notes_V6_Aug_2025.pdf)
  - *quote:* "NASA Ocean Biology Processing Group (OBPG). Cyanobacteria Assessment Network (CyAN), Merged Sentinel-3A and Sentinel-3B OLCI Regional Mapped Cyanobacteria Index (CI) Data, version 6.0, NASA Ocean Biology Distributed Active Archive Center. DOI: 10.5067/MERGED-S3/OLCI/L3M/CYAN/CI/6.0"
- **[✓ verified]** The landing page does not itself list limitations; it directs users to the release notes for interpretation, limitations, and known issues.
  - *evidence:* Directly stated pointer sentence rather than an inline limitations list — an important scope caveat for how much this specific source actually discloses. (Version & citation information section)
  - *quote:* "The release notes provide an overview on CyAN data and imagery production, interpretation, limitations and known issues, in addition to details on version updates."
- **[✓ verified]** A supplementary look at the linked Version 6 release notes found an explicit statement that CI product accuracy is reduced by atmospheric correction uncertainty and adjacency effects near coastlines.
  - *evidence:* Sourced from the release-notes PDF the landing page links to, not the landing page text itself; the fetch tool flagged its own PDF extraction as incomplete ('heavily compressed... may not be fully readable'), so this is lower-confidence supplementary evidence rather than a core landing-page claim. (CyAN_NASA_MERISOLCI_CI_release_notes_V6_Aug_2025.pdf, 'known issues' portion (partially extracted))
  - *quote:* "The MERIS/OLCI Cyanobacteria Index (CI) product is subject to atmospheric correction uncertainties and adjacency effects in coastal waters."
- **[✓ verified]** The project distributes data and tools through a CyAN File Search API, SeaDAS analysis software (with a training presentation), an RS_Tools ArcGIS toolbox (versioned for ArcGIS 10 and ArcGIS Pro) for computing composites and extracting point/polygon time series, and downloadable CONUS/lake shapefiles.
  - *evidence:* Each tool named directly with stated purpose; ArcGIS toolbox version numbers given explicitly. (Data Access Tools / Software & Analysis Tools sections)
  - *quote:* "RSTools allows calculation of all composites and extraction of time series data for points and polygons using ArcGIS."
- **[✓ verified]** EPA separately built a public-facing mobile application (the CyAN app) that consumes this satellite data product, distributed via the Google Play store; this NASA page links out to it rather than describing it technically.
  - *evidence:* Stated as a cross-reference/link on the page rather than a technical description. (Mobile App subsection)
  - *quote:* "Read all about EPA's Cyanobacteria Assessment Network mobile application (CyAN app) and download it from the GooglePlay store"
- **[✓ verified]** The page names EPA, USGS, and NOAA as partner agencies collaborating on CyAN, with NASA hosting the data at its Ocean Biology Distributed Active Archive Center (OB.DAAC).
  - *evidence:* Given as a discrete 'Partners' / 'Data Center' listing on the page rather than a single continuous sentence, so no short verbatim quote is used here to avoid misrepresenting a reconstructed list as a literal quotation. (Partners / Data Center section)

## Data / numbers
- 300 m — native sensor (MERIS/OLCI) spatial resolution
- 50 m — CONUS land-mask resolution used to separate water from land
- 500 m — Alaska land-mask resolution (coarser than CONUS)
- ~10,000 to 7,000,000 cells/mL — reported CI_cyano cell-density range
- CI_cyano = 10^(DN x 0.011714 - 4.1870866) — DN-to-cell-density conversion formula
- DN 0-255 scale: 0 = below CI detection threshold; 1-253 = valid data; 254 = land; 255 = no data/cloud
- 2002-2012 — Envisat MERIS data record (~10 years)
- 2016-present — Sentinel-3A OLCI data record
- 2018-present — Sentinel-3B OLCI data record (dual-satellite 'best' coverage begins)
- Version 6 — current CI data processing version; release notes dated August 2025
- DOI 10.5067/MERGED-S3/OLCI/L3M/CYAN/CI/6.0 — citation identifier for merged Sentinel-3A/3B OLCI CI product v6.0 (as reported on page; DOI not independently resolved)
- RS_Toolbox v2.3.1 (ArcGIS 10) and v3.1.4 (ArcGIS Pro) — named ArcGIS plugin versions

## Methods
Method: the CI algorithm is applied to Level-3 mapped reflectance data from ESA ocean-color sensors (Envisat MERIS 2002-2012; Sentinel-3A OLCI 2016-present; Sentinel-3B OLCI 2018-present) to estimate a near-surface cyanobacterial pigment proxy, CI_cyano, over CONUS and Alaska lakes. Output is delivered as GeoTIFF daily files and 7-day maximum-value composites, tiled by column/row, at 300 m sensor resolution (50 m CONUS land mask / 500 m Alaska land mask). Pixel Digital Numbers (DN, 0-255) are converted to cell-density units via CI_cyano = 10^(DN×0.011714−4.1870866), reported to span ~10,000-7,000,000 cells/mL; DN=0 flags below-detection, DN=254 masks land, DN=255 flags no-data/cloud pixels. The page states coverage is "best" from 2018 onward once both Sentinel-3 satellites were operating simultaneously. Ancillary tools named: a CyAN File Search API, SeaDAS analysis software (with training materials), an RS_Tools ArcGIS toolbox (v2.3.1 for ArcGIS 10, v3.1.4 for ArcGIS Pro) for composites/time-series extraction at points or polygons, and CONUS/lake shapefiles. Where it is reported to fail/degrade: a supplementary, partially-extracted fetch of the linked Version 6 release notes (a PDF, not the landing page itself) states the CI product "is subject to atmospheric correction uncertainties and adjacency effects in coastal waters," with (unquoted, paraphrase-level) mention of reduced data quality in high-suspended-sediment and very shallow waters. No in-situ validation statistics, correlation coefficients, or accuracy/error figures were present in any of the fetched text.

## Stated limitations
The landing page does not itself enumerate limitations inline; it states only that "[t]he release notes provide an overview on CyAN data and imagery production, interpretation, limitations and known issues, in addition to details on version updates" — i.e., it points to the linked Version 6 (August 2025) release-notes PDF rather than listing caveats on the page. A supplementary fetch of that PDF (flagged by the fetch tool itself as an unreliable/incomplete extraction of a "heavily compressed" document) surfaced one direct statement that the CI product "is subject to atmospheric correction uncertainties and adjacency effects in coastal waters," plus an unquoted mention that data quality may be reduced in high-sediment and extremely shallow waters — this should be treated as lower-confidence supplementary evidence, not a fully verified quote from the release notes. Structurally, the page's own DN encoding documents two hard blind spots: cloud-covered pixels are entirely excluded (DN=255, "no data") and near-shore/land-adjacent pixels are masked rather than estimated (DN=254). No explicit accuracy/uncertainty statistic (RMSE, % error, correlation to in-situ chlorophyll-a or cell counts) appears anywhere in the fetched text.

## Tensions with other findings
This NASA/Earthdata page names only EPA, USGS, and NOAA as partners and states no CyAN project start date, no forecasting-model detail, and no Sentinel-2/Landsat-temperature products. A companion EPA program page (https://www.epa.gov/water-research/cyanobacteria-assessment-network-cyan — fetched only as a cross-check, not treated as evidence for this FED-009 entry) states CyAN "officially started October 1, 2015," names a fifth partner (U.S. Army Corps of Engineers, "as of 2023"), and describes a July-2024 experimental weekly cyanoHAB forecasting model for "over 2,000 lakes" plus newer Sentinel-2 MSI (2024) and Landsat surface-temperature products — none of which appear in the fetched NASA/Earthdata text. This is a scope gap between sibling agency pages describing the same program, not a factual contradiction, but it means this single source under-describes the program's current breadth; a full picture needs both pages. Substantively, the source's own admission that the CI signal is degraded by "atmospheric correction uncertainties and adjacency effects in coastal waters" (and, per partial extraction, in high-sediment/shallow water) is a concrete, source-grounded instance of a recurring HAB remote-sensing theme: satellite ocean-color indices are least reliable exactly where many small, shallow, nutrient-impacted inland lakes sit — which is consistent with (though this source does not itself argue for) pairing satellite CI with in-situ monitoring rather than relying on it alone. Note also: detecting a CI_cyano pigment signal is a measurement, not an explanation — this source makes no causal claims about bloom drivers (nutrients, temperature, etc.), so no correlation-vs-causation issue arises directly from it, but "CI_cyano detected" should not be read as itself explaining why a bloom occurred.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The source text explicitly notes that 'Explicit quantitative uncertainty or error ranges (e.g., ±X% accuracy, confidence intervals) are not provided' in the release notes — relevant context omitted from Claims 6 and 10, which report precision figures without acknowledging absence of stated error bounds.
  - Data delivery format detail ('tiles referred to as the column number followed by row number') is mentioned in source but omitted from all claims.
- **Reviewer notes:** One claim (Claim 3) is marked partial for adding 'Envisat' as a prefix to MERIS, which does not appear in the source text—though the core facts (sensor names, year ranges, delivery format) are all directly supported. All 13 claims are factually grounded in the source text with no hallucinated numbers. Two caveats present in the source are not reflected in the claims themselves: the absence of quantitative error bounds in the release notes, and a technical tile-naming detail."

## Provenance
- Canonical URL: https://www.earthdata.nasa.gov/data/projects/cyan
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: The literal primary URL given (https://oceancolor.gsfc.nasa.gov/projects/cyan/) returned "HTTP 444 Unknown Status" (connection closed, no body) on two separate direct WebFetch attempts with different prompts. Per the task's fallback instructions, I used WebSearch, which surfaced a NASA-side alternate path (https://oceancolor.gsfc.nasa.gov/about/projects/cyan/); fetching that returned a 301 redirect to https://www.earthdata.nasa.gov/data/projects/cyan (NASA's site appears to have migrated this project page to the Earthdata domain). I fetched that resolved URL twice with different extraction prompts (satisfying the HIGH-relevance two-fetch/reconcile requirement) and did a third, narrowly-scoped fetch to obtain exact verbatim strings for the numeric/formula claims rather than relying on the first fetch's paraphrases — all three were mutually consistent on every overlapping fact, which is why confidence in the quoted figures is high. I additionally fetched the linked Version 6 release-notes PDF for supplementary limitations detail; the tool itself flagged that PDF extraction as incomplete/unreliable ("heavily compressed... may not be fully readable"), so I have labeled that content as lower-confidence secondary evidence rather than core landing-page fact, and did not build any primary key_claim solely on unquoted portions of it. I also fetched a different, EPA-hosted CyAN page (https://www.epa.gov/water-research/cyanobacteria-assessment-network-cyan) purely as a cross-check; its additional facts (2015 start date, USACE as fifth partner, 2024 forecasting model, Sentinel-2/Landsat additions) are reported only in the "tensions" field, explicitly attributed to that other page, and are not counted as claims of FED-009 itself, since they did not appear in the fetched text of the actual NASA/Earthdata source. One data point (a "site last updated" footer date) was reported inconsistently across two fetches of the identical URL (December 2026 vs. June 30, 2026) and was therefore excluded from data_numbers/key_claims as unreliable. The cited DOI (10.5067/MERGED-S3/OLCI/L3M/CYAN/CI/6.0) is reported as it appeared on the page but was not independently resolved/clicked through.
