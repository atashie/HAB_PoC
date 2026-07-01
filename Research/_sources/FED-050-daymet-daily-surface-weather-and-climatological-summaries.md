---
key: FED-050
title: Daymet: Daily Surface Weather and Climatological Summaries
authors_or_org: NCAR/UCAR Climate Data Guide entry, authored/edited by Peter E. Thornton & National Center for Atmospheric Research Staff (Eds.); underlying dataset produced by Oak Ridge National Laboratory (ORNL), Principal Investigators Michele Thornton and Peter Thornton; core methods paper by Thornton, P.E., R. Shrestha, M. Thornton, S.-C. Kao, Y. Wei, and B. E. Wilson.
year: 2021 (Thornton et al. methods paper in Scientific Data); Climate Data Guide entry stated as "Last modified 2025-12-11"
url: https://climatedataguide.ucar.edu/climate-data/daymet-daily-surface-weather-and-climatological-summaries
access_date: 2026-07-01
tier: FED
source_type: Dataset description / expert-reviewed reference entry (NCAR/UCAR "Climate Data Guide"), describing a gridded daily weather/climatology data product
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Daymet: Daily Surface Weather and Climatological Summaries

**What it is.** Daymet is a gridded daily surface-weather and climatology dataset produced by Oak Ridge National Laboratory that statistically interpolates/extrapolates ground-based weather-station observations onto a continuous 1 km x 1 km grid over continental North America, Hawaii, and Puerto Rico. This source itself is not a HAB study but an NCAR "Climate Data Guide" reference page describing the dataset's coverage, methodology, strengths, limitations, and access/citation information.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Daymet provides long-term, continuous, gridded daily weather and climatology estimates by interpolating and extrapolating ground-based station observations through statistical modeling.
  - *evidence:* Stated in the page's introductory overview description of what Daymet is. (Overview/description section (top of page))
  - *quote:* "long-term, continuous, gridded estimates of daily weather and climatology variables by interpolating and extrapolating ground-based observations through statistical modeling techniques"
- **[✓ verified]** The dataset's spatial resolution is a 1 km x 1 km grid.
  - *evidence:* Stated in the overview text and confirmed independently in the page's metadata table under "Spatial Resolution: 1 km × 1 km." (Overview section; Metadata table field "Spatial Resolution")
  - *quote:* "1 km x 1 km gridded surface"
- **[✓ verified]** Coverage spans continental North America and Hawaii from 1980 onward and Puerto Rico from 1950, with the guide describing data as current through July 2023.
  - *evidence:* The overview states the start years by region and gives this as the extent of complete-calendar-year coverage as of the page's description; the metadata table separately lists Start Date "1980-01 (North America/Hawaii); 1950 (Puerto Rico)" and End Date "2023-07." (Overview section; Metadata table fields "Start Date"/"End Date")
  - *quote:* "data current through July 2023"
- **[✓ verified]** Daymet outputs seven primary variables: daily minimum and maximum temperature, precipitation, vapor pressure, shortwave radiation, snow water equivalent, and day length.
  - *evidence:* The seven-variable list is given in the page's variables description and echoed in the metadata table's "Main Variables" field (day length is listed separately in the variables description, derived from date/location rather than the atmosphere/cryosphere table). (Variables section; Metadata table field "Main Variables")
  - *quote:* "Atmosphere (Maximum Air Temperature, Minimum Air Temperature, Precipitation, Radiation, Water Vapor); Cryosphere (Snow Water Equivalent)"
- **[✓ verified]** The Daymet V4 algorithm uses three-dimensional spatial regressions with objective weighting to capture vertical and horizontal climate gradients, and sizes its station search radius to capture the average number of input stations based on pre-calculated station-distance arrays.
  - *evidence:* Given in the page's methodology/algorithm discussion of the Daymet V4 approach. (Methodology section (algorithm description))
  - *quote:* "three-dimensional spatial regressions with objective weighting functions to estimate vertical and horizontal gradients in temperature and precipitation... defines a search radius for each estimation location which is sized to capture exactly the average number of input stations, based on pre-calculated arrays of station distances"
- **[✓ verified]** Daymet's ground-station input data is NCEI's Global Historical Climatology Network-daily (GHCNd) dataset.
  - *evidence:* Named explicitly as the source of input station observations. (Methodology/input-data section)
  - *quote:* "the NCEI Global Historical Climate Network daily (GHCNd) data"
- **[✓ verified]** Shortwave radiation, vapor pressure, and snow water equivalent are not independently observed but are derived from the primary temperature and precipitation fields via theoretical and empirical relationships; day length is computed from location and time of year.
  - *evidence:* Explains that only temperature and precipitation are primary/directly modeled variables, with the rest being secondary/derived. (Methodology/derived-variables section)
  - *quote:* "derived from the primary temperature and precipitation variables on the basis of theory and empirical relationships"
- **[✓ verified]** The published Daymet datasets include, as a standard component, detailed and rigorous cross-validation-based error reporting for temperature and precipitation.
  - *evidence:* Listed as a "Key Strength" of the dataset. ("Key Strengths" section)
  - *quote:* "detailed and rigorous reporting of estimation error for temperature and precipitation based on cross-validation analysis, as a standard component of the published datasets"
- **[✓ verified]** A stated key strength is that the combination of high (1 km) spatial resolution, seven variables, and continuous updates since 1980 is an unusual/unique combination of attributes among gridded weather products.
  - *evidence:* First bullet under the page's "Key Strengths" heading. ("Key Strengths" section, bullet 1)
  - *quote:* "High spatial resolution, wide selection of variables, regular updates over 1980-present are a unique set of attributes"
- **[✓ verified]** A stated key limitation is that Daymet's empirical humidity-estimation relationships produce climate-zone-related biases in arid environments.
  - *evidence:* First bullet under the page's "Key Limitations" heading. ("Key Limitations" section, bullet 1)
  - *quote:* "Empirical relationships for humidity estimation in arid environments produce biases related to climate zone"
- **[✓ verified]** A stated key limitation is that station network density cannot resolve patchy daily precipitation patterns at high latitudes.
  - *evidence:* Second bullet under the page's "Key Limitations" heading. ("Key Limitations" section, bullet 2)
  - *quote:* "Network density can't resolve patchy daily precipitation patterns at high latitudes"
- **[✓ verified]** A stated key limitation is that Daymet does not include all variables needed to drive full land-surface models, with the page pointing to NLDAS as a comparison product for that purpose.
  - *evidence:* Third bullet under "Key Limitations," framed as a product-scope caveat relative to a named alternative dataset (NLDAS). ("Key Limitations" section, bullet 3)
  - *quote:* "Does not include all variables needed to drive full land surface models (see NLDAS for comparison)"
- **[✓ verified]** Cross-validation error is regionally uneven: it is lowest in the densely-instrumented eastern US, and the central-US Rocky Mountains show relatively low error compared with the more sparsely-instrumented mountain regions of Canada and Alaska.
  - *evidence:* Given in a regional-performance discussion tying cross-validation error magnitude to station network density. (Performance/cross-validation discussion section)
  - *quote:* "Cross-validation errors are lowest over the densely-instrumented regions in the eastern US... relatively low cross-validation errors, when compared to remote and sparsely-instrumented mountain regions in Canada and Alaska"
- **[✓ verified]** The dataset's algorithm and uncertainty-quantification approach are documented in a 2021 peer-reviewed paper by Thornton et al. in Scientific Data, volume 8.
  - *evidence:* Given as the key underlying methods citation for the Daymet V4 product line, with DOI 10.1038/s41597-021-00973-0. (Citation / key-publication section)
  - *quote:* "Gridded daily weather data for North America with comprehensive uncertainty quantification... Scientific Data 8"
- **[✓ verified]** Daymet Version 4 R1 data are distributed as multiple separately-DOI'd products: daily surface weather data, annual climate summaries, monthly climate summaries, station-level inputs and cross-validation data, and a monthly-latency daily product.
  - *evidence:* Listed in the page's data-access section as the citable dataset products with their respective DOIs. (Data Access section / dataset DOI list)
  - *quote:* "Daymet: Daily Surface Weather Data on a 1-km Grid for North America, Version 4 R1... Daymet: Station-Level Inputs and Cross-Validation for North America, Version 4 R1... Daymet Version 4 Monthly Latency: Daily Surface Weather Data"

## Data / numbers
- Spatial resolution: 1 km × 1 km grid cell
- Temporal coverage: 1980–present for continental North America and Hawaii; 1950–present for Puerto Rico
- Data stated as current through 2023-07 (July 2023) per the guide page's metadata ("End Date")
- 7 primary weather/climate variables provided (min. temperature, max. temperature, precipitation, vapor pressure, shortwave radiation, snow water equivalent, day length)
- Dataset version: Daymet Version 4, Revision 1 (V4 R1)
- 5 distinct DOI-registered V4 R1/related data products cited: 10.3334/ORNLDAAC/2129 (daily), 10.3334/ORNLDAAC/2130 (annual), 10.3334/ORNLDAAC/2131 (monthly), 10.3334/ORNLDAAC/2132 (station-level inputs & cross-validation), 10.3334/ORNLDAAC/1904 (monthly-latency daily)
- Core methods/uncertainty paper: Thornton et al. 2021, Scientific Data, volume 8, DOI 10.1038/s41597-021-00973-0
- Climate Data Guide entry citation block states "Last modified 2025-12-11"
- No numeric cross-validation error values (e.g., RMSE/bias in °C or mm) are stated on this page — regional error is described only qualitatively (lowest in eastern US; higher in arid/high-latitude/sparse-network regions)

## Methods
Daymet (Version 4 / V4 R1) generates its gridded fields using "three-dimensional spatial regressions with objective weighting functions to estimate vertical and horizontal gradients in temperature and precipitation." The V4 algorithm "defines a search radius for each estimation location which is sized to capture exactly the average number of input stations, based on pre-calculated arrays of station distances." Input ground observations come from "the NCEI Global Historical Climate Network daily (GHCNd) data." Three of the seven output variables (shortwave radiation, vapor pressure, snow water equivalent) are not directly observed but "derived from the primary temperature and precipitation variables on the basis of theory and empirical relationships"; day length is computed astronomically from location and date. Quality control includes "identification and correction of network data biases, including biases related to sensor replacement, and biases related to different time of day for 24-hour reporting among networks and stations." The published V4/V4R1 products include, "as a standard component," cross-validation-based estimation error for temperature and precipitation. The page states this approach works best (lowest cross-validation error) in densely-instrumented regions (the eastern US) and is comparatively weaker for humidity/vapor-pressure estimation in arid climate zones and for resolving patchy daily precipitation in high-latitude, sparsely-instrumented regions (e.g., Canada, Alaska). No specific quantitative error values (e.g., RMSE, bias in mm or °C) are given on this page itself — only qualitative regional comparisons; the page points to the cited 2021 Scientific Data paper for "comprehensive uncertainty quantification."

## Stated limitations
The page's "Key Limitations" bullets state: (1) "Empirical relationships for humidity estimation in arid environments produce biases related to climate zone (hot or cold arid zones, differences in seasonal precipitation maxima)"; (2) "Network density can't resolve patchy daily precipitation patterns at high latitudes"; (3) the dataset "does not include all variables needed to drive full land surface models (see NLDAS for comparison)." The extracted page narrative additionally notes that the daily precipitation product does not utilize radar network data, that there is temporal variability in network-station data availability (particularly for Mexican stations), and that station networks are sparse in sparsely populated regions generally.

## Tensions with other findings
The source makes no claims about HABs, cyanobacteria, or water quality — it is purely a weather-data description, so it does not directly corroborate or contradict any HAB finding. However, its self-stated limitations matter if Daymet's gridded temperature/precipitation were used as a weather covariate in a HAB risk model (e.g., temperature as a cyanobacteria-growth proxy, precipitation as a nutrient-runoff/loading proxy per this project's remote-sensing + in-situ + weather fusion approach): the page states accuracy is uneven by region, with lowest cross-validation error in the densely-instrumented eastern US and comparatively higher uncertainty in arid zones (humidity/vapor pressure), high-latitude/sparsely-instrumented mountain regions (Canada, Alaska), and areas with sparse or temporally inconsistent station coverage (e.g., Mexico). This implies any HAB analysis pooling lakes across regions of very different station density should expect non-uniform weather-covariate error rather than assuming equal precision everywhere — a caveat I am inferring from the source's stated limitations, not one the source itself frames in terms of HABs.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Quality assurance bias-correction procedures (sensor replacement, time-of-day reporting differences across networks)
  - Daily precipitation product does not utilize radar network data
  - Temporal variability in network data availability (Mexican stations noted)
  - Data-driven spatial gradient analysis and objective joint precipitation occurrence/intensity estimation as strengths
  - Sparse networks in sparsely populated regions as limitation
- **Reviewer notes:** All 15 claims are directly supported by corresponding passages in the source text. No numerical claims are hallucinated or absent from the source. The source text fully corroborates the dataset metadata (coverage dates, spatial resolution, variable count and types), methodology (algorithm design, input data), institutional affiliation (ORNL, Thornton et al.), and stated strengths and limitations. Quotes provided match source language precisely or are faithful paraphrases. The claims are selective (not capturing every detail in the source, such as quality-assurance procedures or radar-data exclusions) but make no false or unsupported assertions."

## Provenance
- Canonical URL: https://climatedataguide.ucar.edu/climate-data/daymet-daily-surface-weather-and-climatological-summaries
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched directly at the given primary URL with no redirect. Two WebFetch calls returned substantively consistent, comprehensive content covering the overview, variables, methodology, "Key Strengths," "Key Limitations," regional cross-validation performance, data-access/DOI list, institutional/citation information, and a metadata table — treated as full coverage of this reference-page source (not a journal article, so no separate "abstract vs. full text" distinction applies). A third WebFetch call asking for exact section-by-section verbatim reproduction of the entire page was refused by the tool's underlying model on copyright grounds, so exact original HTML wording beyond the quoted fragments already obtained could not be independently re-verified; no raw HTML/DOM access was available to this analyst (WebFetch and WebSearch only, no Read/browser tool). No WebSearch was needed since the primary URL fetched correctly to the intended page on the first attempt. This source page contains no HAB-, cyanobacteria-, or water-quality-specific content; all HAB-relevance framing in this dossier (see "tensions") is this analyst's inference connecting the source's stated weather-data limitations to potential downstream use as a covariate source, not a claim made by the source itself. One apparent internal tension in the source's own metadata is left unresolved here rather than explained away: the citation block states the guide entry was "Last modified 2025-12-11," yet the page's own coverage/metadata describes data as current only "through July 2023" — this analyst did not attempt to reconcile that gap, since doing so would require information not present in the fetched text.
