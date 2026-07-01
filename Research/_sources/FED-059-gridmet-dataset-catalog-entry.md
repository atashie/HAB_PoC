---
key: FED-059
title: gridMET dataset catalog entry
authors_or_org: Data producer: Climatology Lab, listed on the catalog page as "Academic Institution(s)"; primary methodological citation author: J.T. Abatzoglou. Catalog record itself is hosted/maintained within the USGS Water Mission Area integrated data catalog.
year: 2013 (year of the cited Abatzoglou methodological paper); the gridMET dataset itself is described as continuously updated, covering 1979 to present
url: https://water.usgs.gov/catalog/datasets/ef98187e-8703-4ec6-afc1-4dbc72c9d6d8/
access_date: 2026-07-01
tier: FED
source_type: Government agency dataset/data-catalog metadata record (USGS Water Mission Area integrated data catalog entry describing a third-party academic gridded climate dataset)
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# gridMET dataset catalog entry

**What it is.** gridMET (aka METDATA) is a daily, ~4-km (1/24th degree) resolution gridded surface meteorological dataset covering the contiguous United States from 1979 to the present, produced by an academic group (Climatology Lab) by blending PRISM's spatial detail with NLDAS-2's temporal detail; this specific source is the USGS Water Mission Area's integrated data-catalog metadata record describing that dataset, its variables, and its links to other USGS resources.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** gridMET is a daily, ~4-km (1/24th degree) resolution surface meteorological dataset covering the contiguous US from 1979 to the present, produced by blending PRISM's spatial attributes with NLDAS-2's temporal attributes, and is updated daily.
  - *evidence:* Stated directly in the catalog entry's description paragraph and corroborated by the separate Spatial Details, Temporal Details, and Update Information fields on the same page. (Catalog entry description paragraph; Spatial Details / Temporal Details / Update Information fields)
  - *quote:* "daily high-spatial resolution (~4-km, 1/24th degree) surface meteorological data covering the contiguous US from 1979-yesterday"
- **[✓ verified]** The dataset's defining method is a blend of PRISM (spatial climatology) with NLDAS-2 (temporal/reanalysis-informed) data.
  - *evidence:* This sentence is the core methodological description given on the catalog page and was returned consistently and identically across two independent fetch passes. (Description section)
  - *quote:* "These data blend the high quality spatial attributes of PRISM with the temporal attributes and additional data from NLDAS-2"
- **[✓ verified]** gridMET is also known/cited under the alternate name METDATA.
  - *evidence:* Given as an aside in the description text returned by the fetch. (Description section)
  - *quote:* "also known as cited as METDATA"
- **[✓ verified]** The dataset includes at least 15 explicitly named meteorological, drought, and fire-danger variables (including fuel-model-specific fire indices and a named drought index), plus roughly 10 further variables that are not enumerated on the page itself.
  - *evidence:* The Variables field lists 15 items by name; a follow-up fetch targeted specifically at this field confirmed a 'See 10 More Variables...' expansion control exists but its contents were not retrievable from the static page text. (Variables field)
  - *quote:* "Energy Release Component (fuel model G (conifer forest)); Burning Index (fuel model G (conifer forest)); 100-hour and 1000-hour dead fuel moisture ... 10-day Palmer Drought Severity Index"
- **[✓ verified]** The dataset's foundational methodological citation is Abatzoglou (2013), published in the International Journal of Climatology, volume 33, pages 121-131, DOI 10.1002/joc.3413.
  - *evidence:* Given verbatim in the Citation field of the catalog entry; independently cross-checked via WebSearch against Wiley/ADS/ScIRP bibliographic listings, which match volume, pages, and DOI. (Citation field)
  - *quote:* "Abatzoglou, J.T., 2013, Development of gridded surface meteorological data for ecological applications and modelling. Int. J. Climatol., 33: 121-131. https://doi.org/10.1002/joc.3413"
- **[✓ verified]** The catalog record designates gridMET as the source dataset for three downstream USGS resources that tie the climate grid to hydrography: the Water Mission Area STAC Catalog, a workflow regridding gridMET to NHD HUC12 polygons, and a workflow aggregating gridMET to NHD flowlines and sample points.
  - *evidence:* Listed under the page's 'Linked Use Cases' / 'IsSourceOf' relationships. (Linked Use Cases section)
  - *quote:* "IsSourceOf Regridding gridded climate data to NHD HUC12 polygons; IsSourceOf Aggregate gridMET data to NHD Flowlines and sample points"
- **[✓ verified]** The catalog entry classifies the data source type as 'Academic Institution(s)' with an update type of 'Dynamic' and update detail of 'append,' while the update-frequency field itself is populated as unknown.
  - *evidence:* Directly transcribed from the Source and Update Information fields of the catalog record. (Source / Update Information fields)
  - *quote:* "Update Type: Dynamic; Update Frequency: unknown; Update Detail: append"
- **[✓ verified]** The catalog entry does not provide a point of contact, a license or use-constraints statement, bounding-box coordinates, or a record-level metadata/publication date, and does not enumerate its full variable list on the static page.
  - *evidence:* Confirmed by a targeted follow-up fetch that explicitly asked whether each of these fields was present; the fetch reported each one as 'not present on the page' or not retrievable from the rendered text. (Whole page (absence checked across all sections))

## Data / numbers
- Spatial resolution: ~4 km (1/24th degree)
- Spatial extent: CONUS (contiguous United States); description also states coverage extends to southern British Columbia
- Temporal coverage: 1979 to present ("1979-yesterday"), i.e., 47 years and counting as of 2026
- Update frequency: daily ("updated daily"); catalog's own 'Update Frequency' field is listed as 'unknown' with Update Type 'Dynamic' and Update Detail 'append'
- Named variables on the catalog page: 15 explicitly listed, plus a 'See 10 More Variables' control indicating additional unenumerated variables (~25 total implied, not confirmed)
- Citation record: International Journal of Climatology, volume 33, pages 121-131 (2013), DOI 10.1002/joc.3413
- No accuracy/validation statistics (e.g., bias, RMSE, correlation vs. station data) are given anywhere on the catalog page; no baseline or uncertainty values are stated for any variable

## Methods
The catalog entry attributes gridMET's production method to a blend of "the high quality spatial attributes of PRISM" with "the temporal attributes and additional data from NLDAS-2" (North American Land Data Assimilation System phase 2), citing Abatzoglou (2013, Int. J. Climatol. 33:121-131, doi:10.1002/joc.3413) as the methodological reference. The catalog page does not itself reproduce the interpolation/blending algorithm, any validation procedure, or any statement of where the method performs well or poorly (e.g., by region, season, or variable) — that level of detail would reside in the cited journal article, which was not fetched as part of this dossier (only its citation string was captured and independently bibliography-checked via WebSearch). No modeling, statistical, or machine-learning methodology beyond this data-blending description is present in the source.

## Stated limitations
The catalog entry contains no explicit "limitations" section and states no accuracy or validation statistics (e.g., no bias, RMSE, or correlation figures versus station observations) for any variable. It provides no license or use-constraints statement, no point-of-contact/contact-organization field, no bounding-box coordinates, and no record-level metadata or publication date — all of these were specifically checked for and confirmed absent by a targeted fetch pass. The variable list is also incomplete on the page itself: 15 variables are named, with a "See 10 More Variables" control whose contents could not be retrieved from the static fetched text, so this dossier cannot confirm the full ~25-variable roster. Because this is a catalog/metadata record rather than the underlying scientific paper, no discussion of the method's known failure modes, regions of degraded skill, or comparison to alternative products (e.g., PRISM or NLDAS-2 alone) is present in the fetched text.

## Tensions with other findings
This source describes a gridded weather/land-surface meteorological and fire/drought-index product (temperature, precipitation, humidity, wind, evapotranspiration, drought and fire-danger indices) rather than an aquatic, remote-sensing, or water-quality product, and the catalog entry contains no claims, statistics, or discussion regarding harmful algal blooms, cyanobacteria, chlorophyll-a, or nutrient loading. Its relevance to a HAB literature review is therefore only as a candidate exogenous covariate/driver layer (e.g., temperature and precipitation forcing to pair with a satellite cyanobacteria signal such as EPA CyAN or with in-situ Water Quality Portal data), not as direct evidence about bloom dynamics. It neither corroborates nor contradicts other HAB-specific sources; it simply makes no HAB-related claims, so it cannot be used to support any driver/causal statement about blooms without additional, separate analysis linking gridMET variables to bloom outcomes.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Source text (pass 2 synthesis) notes that data extend to southern British Columbia, expanding coverage beyond the stated CONUS spatial extent, though this is not contradicted by the claims—only left implicit.
- **Reviewer notes:** All eight claims are directly supported by the source text. No hallucinated numbers were detected; every numerical detail traces to the fetched catalog page. The claims accurately capture the core metadata: temporal and spatial resolution, method (PRISM+NLDAS-2 fusion), citation (Abatzoglou 2013), variable enumeration (15 explicit + ~10 hidden), update schedule (daily, dynamic, unknown frequency), source classification (Academic Institution), and the specific absences confirmed by pass 3 targeted checks. One minor dropped caveat: the geographic extent slightly exceeds CONUS (extends to southern British Columbia per the description synthesis), but this is neither contradicted nor critical to the core claims. This is a solid, well-traced extraction with no material discrepancies."

## Provenance
- Canonical URL: https://water.usgs.gov/catalog/datasets/ef98187e-8703-4ec6-afc1-4dbc72c9d6d8/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Primary URL fetched directly (no redirect); page loaded successfully and was clearly the correct source (USGS Water Mission Area catalog record for gridMET). Performed three WebFetch passes against the same URL: (1) a general comprehensive-extraction prompt, (2) a request to reproduce the raw text section-by-section verbatim, and (3) a targeted follow-up specifically probing for point-of-contact, license/use-constraints, bounding-box coordinates, a record-level DOI/persistent identifier, metadata dates, and the full variable roster. The third pass confirmed those fields are NOT present in the fetched page content (either genuinely absent from this catalog record or hidden behind a client-side "10 More Variables" expansion not captured by the fetch tool). Per instructions, no substitute/alternate source was needed since the fetch was neither blocked nor the wrong page. One supplementary WebSearch was run solely to verify the bibliographic accuracy of the cited Abatzoglou (2013) paper (volume/pages/DOI) against independent listings (Wiley, ADS, ScIRP) — this was used only to corroborate the citation string already present on the catalog page, not to source any additional claims about gridMET's content, methods, or numbers. All key_claims and data_numbers below derive only from the fetched catalog-page text itself.
