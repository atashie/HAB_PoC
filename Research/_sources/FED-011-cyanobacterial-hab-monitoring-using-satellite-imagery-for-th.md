---
key: FED-011
title: Cyanobacterial HAB Monitoring using Satellite Imagery for the United States Great Lakes region created by the NOAA Harmful Algal Bloom Forecasting Branch (HAB-F) from 2000 to 2024 (NCEI Accession 0312614)
authors_or_org: Mishra, Sachidananda; Meredith, Andrew; Wynne, Timothy; Hounshell, Alexandria G.; Stumpf, Richard P. — NOAA National Centers for Coastal Ocean Science (NCCOS), Harmful Algal Bloom Forecasting Branch (HAB-F); archived at NOAA NCEI
year: 2026
url: https://coastalscience.noaa.gov/data_reports/cyanobacterial-hab-monitoring-using-satellite-imagery-for-the-united-states-great-lakes-region-created-by-the-noaa-harmful-algal-bloom-forecasting-branch-hab-f-from-2000-to-2024-ncei-accession-0312/ (no redirect; page links to NCEI ISO metadata record at https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:0312614, fetched as a supplementary same-dataset page; DOI 10.25921/wzk1-r208)
access_date: 2026-07-01
tier: FED
source_type: Federal agency data report + NCEI data-archive accession (dataset landing page + ISO metadata record), not a peer-reviewed journal article
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Cyanobacterial HAB Monitoring using Satellite Imagery for the United States Great Lakes region created by the NOAA Harmful Algal Bloom Forecasting Branch (HAB-F) from 2000 to 2024 (NCEI Accession 0312614)

> Note: provisional URL was resolved to a primary source. Original: https://coastalscience.noaa.gov/data_reports/cyanobacterial-hab-monitoring-using-satellite-imagery-for-the-united-states-great-lakes-region-created-by-the-noaa-harmful-algal-bloom-forecasting-branch-hab-f-from-2000-to-2024-ncei-accession-0312/

**What it is.** An NOAA NCCOS/HAB-F data report and NCEI archive accession (0312614; DOI 10.25921/wzk1-r208) presenting a 25-year (2000–2024), continuous, cross-sensor-harmonized satellite time series of the Cyanobacteria Index (CIcyano) for priority U.S. Great Lakes waterbodies — Lake Erie, Sandusky Bay, Saginaw Bay (Lake Huron), Green Bay (Lake Michigan), and Lake Winnebago — built by fusing Envisat-MERIS, Sentinel-3A/B OLCI, and MODIS-Terra ocean-color imagery, with the MERIS-to-OLCI sensor gap bridged using a deep-learning framework called CyanNet.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The dataset provides a 25-year, continuous, cross-sensor-consistent satellite-based time series (2000–2024) of cyanobacterial HAB observations for the U.S. Great Lakes region.
  - *evidence:* Stated directly as the core description of the data product on the report landing page. (Data report page, opening description/abstract)
  - *quote:* "A 25-year, continuous, and cross-sensor-consistent satellite-based time series (2000–2024) of cyanobacterial harmful algal bloom observations is presented for the United States Great Lakes region."
- **[✓ verified]** The monitoring effort specifically targets Lake Erie, Sandusky Bay, Saginaw Bay (Lake Huron), Green Bay (Lake Michigan), and Lake Winnebago as the priority CyanoHAB-affected waterbodies.
  - *evidence:* These waterbodies are named explicitly as the areas of concern motivating the product. (Data report page, opening description/abstract)
  - *quote:* "especially in Lake Erie, Sandusky Bay, Saginaw Bay in Lake Huron, Green Bay in Lake Michigan, and Lake Winnebago"
- **[✓ verified]** The time series was built by fusing three satellite ocean-color sensor missions: Envisat-MERIS, Sentinel-3A/B OLCI, and MODIS-Terra.
  - *evidence:* Named as the source instruments feeding the harmonized record. (Data report page, description/abstract)
  - *quote:* "This time series was created using data from multiple satellite ocean color sensors, specifically Envisat-MERIS, Sentinel-3A/B OLCI, and MODIS-Terra."
- **[⚠ partial]** To bridge the observational gap between the MERIS and OLCI sensor eras, the Cyanobacteria Index (CIcyano) was derived from MODIS-Terra using a purpose-built deep-learning framework called CyanNet.
  - *evidence:* Describes the specific harmonization method used to make the sensor-to-sensor transition continuous rather than leaving a data gap. (Data report page, description/abstract)
  - *quote:* "To bridge the observational gap between the MERIS and Ocean and Land Color Instrument (OLCI) sensors…the Cyanobacteria Index (CIcyano) was derived from MODIS-Terra using CyanNet, a science-informed deep learning framework."
  - *reviewer:* Claim states 'purpose-built' but source states 'science-informed deep learning framework' — these characterizations differ; 'science-informed' does not assert the framework was built specifically for this task as 'purpose-built' does.
- **[✓ verified]** The stated purpose of the long time series is to characterize bloom phenology, assess trends in phenological changes, and understand the key drivers that cause and exacerbate blooms.
  - *evidence:* Direct statement of the product's intended analytical use, framed as the reason a multi-decadal record was assembled. (Data report page, opening description/abstract)
  - *quote:* "Long-term time series data are required to characterize bloom phenology, assess trends in phenological changes, and understand the key drivers that cause and exacerbate blooms."
- **[✓ verified]** CyanoHABs are framed by the source as an ongoing threat to water quality, ecosystems, economies, and public health in the Great Lakes region (motivational framing, not a new empirical finding).
  - *evidence:* Opening motivational sentence establishing why the monitoring product matters. (Data report page, opening sentence)
  - *quote:* "Cyanobacterial Harmful Algal Blooms (CyanoHABs) are an ongoing threat to water quality, ecosystems, economies, and public health in the Great Lakes region."
- **[✓ verified]** The dataset is formally archived with DOI 10.25921/wzk1-r208, spatial bounding box roughly 40.941°N–49.141°N by -92.4° to -74.528° longitude, temporal extent 2000-06-01 to 2024-11-15, distributed as CSV and GeoTIFF files via HTTPS/FTP under a CC0 1.0 public-domain license.
  - *evidence:* Structured metadata fields returned from the linked NCEI ISO metadata record for this same accession; these are field values as rendered by the fetch tool from a structured metadata page, not a single verbatim prose quote, so treat the exact numeric boundaries with slightly lower confidence than the prose quotes above. (NCEI ISO metadata landing page (linked from report page as "Access Data/Report"), structured metadata fields)
  - *quote:* "DOI 10.25921/wzk1-r208; bounding box West -92.4°, East -74.528°, South 40.941°, North 49.141°; temporal extent Start 2000-06-01, End 2024-11-15; formats "CSV and GeoTIFF""
- **[✓ verified]** NOAA/NCEI applies a standard no-warranty use constraint to the dataset, disclaiming responsibility for data suitability.
  - *evidence:* Boilerplate use-constraint/limitation language attached to the archived data, not specific to this dataset's science. (NCEI ISO metadata landing page, Use Constraints field)
  - *quote:* "NOAA and NCEI make no warranty, expressed or implied, regarding these data"
- **[✓ verified]** The report page carries a general website accessibility disclaimer stating that some linked scientific publications may not conform to Section 508 accessibility standards.
  - *evidence:* Site-level legal/accessibility caveat, distinct from any data-quality or scientific limitation. (Data report page, footer/disclaimer)
  - *quote:* "Some scientific publications linked from this website may not conform to Section 508 accessibility standards."

## Data / numbers
- 25-year time series, coverage years 2000–2024 (as stated on report page)
- Temporal extent per NCEI ISO metadata: 2000-06-01 to 2024-11-15
- Spatial bounding box per NCEI ISO metadata: South 40.941°, North 49.141°, West -92.4°, East -74.528°
- NCEI Accession number: 0312614
- Dataset DOI: 10.25921/wzk1-r208
- Distribution formats: CSV and GeoTIFF, via HTTPS and FTP
- License: Creative Commons CC0 1.0 (public domain)
- Report/creation date returned as 'April 1, 2026' by two independent fetch prompts (see fetch_notes — moderate confidence only)
- No spatial resolution (m), temporal revisit frequency, file/record counts, or accuracy/validation statistics (e.g. RMSE, R², hit rate) were present anywhere in the fetched text — these are absent from the source content retrieved, not merely omitted by us

## Methods
Multi-mission satellite ocean-color remote sensing: Envisat-MERIS (Medium Resolution Imaging Spectrometer), Sentinel-3A/B OLCI (Ocean and Land Colour Instrument), and MODIS-Terra (Moderate Resolution Imaging Spectroradiometer) are fused into one Cyanobacteria Index (CIcyano) time series. The source states the MERIS-to-OLCI observational gap is bridged by deriving CIcyano from MODIS-Terra imagery using "CyanNet, a science-informed deep learning framework," producing a single cross-sensor-consistent record for 2000-2024. The fetched text does not describe the algorithm's internal architecture, training data, or report any accuracy/validation metrics (no RMSE, correlation, skill score, or comparison to in-situ cyanobacteria/chlorophyll measurements appears in the retrieved content) — it states that harmonization was done, not how well it performs.

## Stated limitations
The fetched text's only explicit limitation-type language concerns (1) the observational gap between the MERIS and OLCI sensor eras, which the source presents as addressed/bridged via MODIS-Terra + CyanNet rather than as a remaining open gap; (2) a standard NOAA/NCEI use-constraint disclaiming warranty ("NOAA and NCEI make no warranty, expressed or implied, regarding these data") and requiring users to determine data suitability themselves; and (3) a general website accessibility disclaimer about Section 508 conformance of linked publications, which is a site-legal caveat rather than a scientific one. Beyond these, the retrieved content contains no discussion of algorithm validation/accuracy, cloud-cover or atmospheric-correction handling, false-positive/negative behavior, or spatial/temporal resolution trade-offs — these are simply not present in the fetched text, so their absence is reported here as a gap in what could be retrieved, not asserted as a limitation the source itself claims.

## Tensions with other findings
A WebSearch cross-check surfaced what appears to be a related peer-reviewed article, "Two decades of cyanobacterial bloom dynamics in the Great Lakes: insights from multi-mission ocean color sensors" (IOPscience, DOI 10.1088/2752-664X/ae4631), which likely contains the fuller scientific analysis, validation, and trend results underlying this NCEI accession. That article was not fetched and none of its content is used in this dossier entry — it is flagged only so a reviewer knows the deeper methodological/validation detail probably lives there rather than on this data-report landing page. Separately, within this project's own source list, this NOAA HAB-F/NCCOS Great Lakes product is a distinct effort from EPA's CyAN program (the project's designated primary satellite-signal source): CyAN centers on an OLCI-derived cyanobacteria index across many U.S. lakes from roughly 2016 forward, while this dataset extends the record back to 2000 via MERIS and bridges to MODIS-Terra with a custom deep-learning harmonization (CyanNet). If both were ever combined for overlapping Great Lakes sites/dates, differing processing chains could plausibly yield non-identical CIcyano values, so cross-calibration would be a consideration — this is an analytical note for future integration work, not a contradiction stated by either source, and should not be read as a claim from the fetched text.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** One claim (Claim 4) uses a more definitive characterization ('purpose-built') than the source supports ('science-informed'), but this is a partial issue, not a refutation. All nine claims are either fully supported or appropriately marked partial with the specific discrepancy noted. No hallucinated numbers and no material dropped caveats about dataset quality or limitations. The source text is clear and internally consistent across the primary report page and linked NCEI metadata landing page."

## Provenance
- Canonical URL: https://coastalscience.noaa.gov/data_reports/cyanobacterial-hab-monitoring-using-satellite-imagery-for-the-united-states-great-lakes-region-created-by-the-noaa-harmful-algal-bloom-forecasting-branch-hab-f-from-2000-to-2024-ncei-accession-0312/ (no redirect; page links to NCEI ISO metadata record at https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:0312614, fetched as a supplementary same-dataset page; DOI 10.25921/wzk1-r208)
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary URL twice with different extraction prompts (comprehensive what/where/how/numbers extraction; then abstract/metadata-focused extraction with DOI/keywords/lineage focus) and reconciled them — both returned mutually consistent content (same title, accession, authors, sensors, coverage lakes), so no conflicts to resolve. The primary page turned out to be a short data-report landing page rather than a long technical report, so no PDF or additional full-text document exists beyond it and its linked NCEI ISO metadata record; a dedicated link-inventory fetch confirmed only one outbound link ("Access Data/Report" to the NCEI ISO page) and no PDF/FTP/reference links on the primary page. I additionally fetched that linked NCEI ISO metadata page (same dataset/accession, not a different source) to recover fields the shorter landing page omitted: DOI, bounding box, temporal extent, formats, distribution method, license, and use constraints. Two more targeted fetches of the primary URL were used purely to get closer-to-verbatim quotes for source_extract, since the WebFetch tool truncates any quoted segment over roughly 125 characters in one mode; a follow-up prompt requesting ≤20-word segments successfully reconstructed the full abstract paragraph in order. One WebSearch was run to check for a DOI/companion reference; it confirmed the DOI already found and surfaced a related peer-reviewed journal article (IOPscience) that was not fetched and is not used as source content here (flagged only in tensions). Two independent fetch prompts on the primary URL both returned "Publication Date: April 1, 2026" for this field, which is reported in data_numbers/source_extract, but flagged as only moderate-confidence: WebFetch renders pages through a small intermediary model, and an exact publication date is the kind of field such a model can occasionally mis-render even when it is consistent across calls, so this specific date should be independently verified before being used as a citable fact. No spatial resolution, temporal (revisit) frequency, file/record counts, or accuracy/validation statistics (e.g., RMSE, R², comparison against in-situ chlorophyll/cyanobacteria measurements) appeared in any fetch of either page; these are reported as absent from the retrieved content rather than inferred or invented.
