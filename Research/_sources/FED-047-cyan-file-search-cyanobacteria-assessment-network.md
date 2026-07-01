---
key: FED-047
title: CyAN File Search / Cyanobacteria Assessment Network
authors_or_org: NASA Ocean Biology Distributed Active Archive Center (OB.DAAC), Earth Science Data Systems (ESDS) Program; tool supports the multi-agency CyAN partnership of NASA, NOAA, USGS, and EPA
year: Not stated on page
url: https://www.earthdata.nasa.gov/data/tools/cyan-file-search
access_date: 2026-07-01
tier: FED
source_type: NASA Earthdata tool-directory/catalog page, plus its linked operational data-search web application (not a peer-reviewed publication or dataset paper)
categories: [remote-sensing]
relevance: Medium
full_text_access: landing-only
fetch_status: ok
review_severity: notes
review_overall: pass
---

# CyAN File Search / Cyanobacteria Assessment Network

**What it is.** CyAN File Search is a NASA Earthdata-catalogued web tool, co-developed by NASA's Ocean Biology DAAC (OB.DAAC), that provides search, discovery, analysis, and visualization access to the multi-agency (NASA/NOAA/USGS/EPA) Cyanobacteria Assessment Network's satellite-derived cyanobacteria-index (CI_cyano) bloom data products for lakes in the contiguous U.S. and Alaska. The Earthdata page itself is a brief catalog/landing entry that links out to the actual working application at oceandata.sci.gsfc.nasa.gov, where the real search parameters (region, date range, cadence, resolution, download method) are documented.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** CyAN is a multi-agency initiative among NASA, NOAA, USGS, and EPA to support environmental management and public use of U.S. lakes and estuaries by detecting and quantifying cyanobacteria algal blooms.
  - *evidence:* Stated directly as the overview/purpose of the CyAN program that this File Search tool provides access to. (Overview section, earthdata.nasa.gov/data/tools/cyan-file-search)
  - *quote:* "a multi-agency project among NASA, NOAA, USGS, and the U.S. Environmental Protection Agency (EPA)"
- **[✓ verified]** The CyAN project generates satellite remote-sensing products using a 'cyanobacteria index (CI)' algorithm to estimate cyanobacteria concentration (CI_cyano) in lakes across the contiguous United States and Alaska.
  - *evidence:* Given as the core method/output of the project underlying the tool's data. (Key Purpose & Function section)
  - *quote:* "satellite remote sensing products using the cyanobacteria index algorithm to evaluate cyanobacteria concentrations across the contiguous United States and Alaska"
- **[✓ verified]** The CyAN File Search tool itself was co-developed by NASA's Ocean Biology Distributed Active Archive Center (OB.DAAC).
  - *evidence:* Stated as the tool's origin/co-developer in the page's 'Development' section. (Development section)
  - *quote:* "NASA's Ocean Biology Distributed Active Archive Center partnered in creating the CyAN File Search tool"
- **[✓ verified]** NASA Earthdata classifies the tool under three functional types: Analysis, Search and Discovery, and Visualization.
  - *evidence:* Listed as the page's 'Data Tool Type' metadata tags. (Tool Capabilities / Data Tool Type metadata)
  - *quote:* "Analysis; Search and Discovery; Visualization"
- **[⚠ partial]** Reading the tool's description page requires no account, but downloading the underlying satellite data and using full tool functionality requires an Earthdata Login.
  - *evidence:* Stated as an access requirement/caveat on the landing page. (Access section)
  - *quote:* "an Earthdata Login is required for downloading data and utilizing certain full-functionality features"
  - *reviewer:* The source explicitly requires login for 'downloading data and full tool functionality,' but does not explicitly state that reading the description page requires no account. This is implied by the availability of overview and capability descriptions without mention of a login gate, but the explicit absence-of-requirement is not stated in the source text.
- **[✓ verified]** NASA Earthdata lists an ARSET training, 'Monitoring Water Quality of Inland Lakes using Remote Sensing,' as a learning resource for this tool, held July 18-25, 2023.
  - *evidence:* Given as a titled, dated training resource under 'Learning Resources.' (Learning Resources section)
  - *quote:* "Monitoring Water Quality of Inland Lakes using Remote Sensing ... (July 18-25, 2023)"
- **[✓ verified]** NASA Earthdata also lists an ARSET training, 'Introduction to Remote Sensing of Harmful Algal Blooms,' held Sept. 5-26, 2017.
  - *evidence:* Given as a second titled, dated training resource under 'Learning Resources.' (Learning Resources section)
  - *quote:* "Introduction to Remote Sensing of Harmful Algal Blooms ... (Sept. 5-26, 2017)"
- **[✓ verified]** The tool's actual search interface lets users query by region (Alaska or CONUS), by date range, and by weekly-vs-daily cadence, returning Cyanobacteria Index (weekly or daily) or True Color (daily only) products as GeoTIFF files at 300 m or 1.2 km resolution.
  - *evidence:* Directly described in the fetched content of the tool's own search-parameter page, which the Earthdata landing page links to as the actual application. (Search Parameters & Fields / Product Type / Data Format sections, oceandata.sci.gsfc.nasa.gov/api/cyan_file_search/)
  - *quote:* "valid options: 1 (Weekly); 2 (Daily)" ... "GeoTIFF files at 300m (CyAN) or 1.2km resolution"
- **[✓ verified]** Historical data through the tool is available from 2002 to the present, retrievable via wget, cURL, or Python scripts, with the page noting reported command errors specifically on Windows machines.
  - *evidence:* Stated in the Time Period and Access Methods portions of the tool's own page. (Time Period / Access Methods sections, oceandata.sci.gsfc.nasa.gov/api/cyan_file_search/)
  - *quote:* "reported errors with running these commands on Windows machines"

## Data / numbers
- 300 m — GeoTIFF spatial resolution of the CyAN Cyanobacteria Index product (tool page)
- 1.2 km — alternate GeoTIFF resolution option offered by the tool (the product/sensor distinction between this and the 300 m option is not explained in the fetched text)
- 2002–present — stated historical data availability range (tool page)
- Weekly = time-period option code 1; Daily = option code 2 (tool page selector values)
- Alaska = region code 0; CONUS = region code 1 (tool page selector values)
- July 18-25, 2023 — dates of the 'Monitoring Water Quality of Inland Lakes using Remote Sensing' ARSET training (Earthdata page)
- Sept. 5-26, 2017 — dates of the 'Introduction to Remote Sensing of Harmful Algal Blooms' ARSET training (Earthdata page)

## Methods
The source documents a data-delivery mechanism rather than a scientific method it validates: NOAA/NASA's "cyanobacteria index (CI)" algorithm is applied (upstream, not described in this source) to satellite imagery to produce a per-pixel cyanobacteria-concentration estimate ("CI_cyano"), delivered through this tool as GeoTIFF rasters at 300 m (or an alternate 1.2 km) resolution, at weekly or daily cadence, for CONUS or Alaska, over a stated 2002-present record. Access is via a searchable web interface with region/tile/date-range selection, with bulk retrieval by wget, cURL, or Python scripting, plus optional text-file listings, URL-prefix output, and checksum files. The source does not describe how the CI algorithm is derived, calibrated, or validated, nor its accuracy against in-situ measurements — it documents access mechanics only. It states one concrete practical failure mode: reported command-line errors when using the documented wget/cURL/Python download commands on Windows machines (no workaround given). Related visualization tools are cross-referenced (SeaDAS, Giovanni, Worldview) but not described in detail.

## Stated limitations
The source states only access-related caveats, not scientific ones: (1) "an Earthdata Login is required for downloading data and utilizing certain full-functionality features," meaning the descriptive page is open but the underlying satellite data cannot be bulk-downloaded anonymously; (2) the documented wget/cURL/Python download commands have "reported errors...on Windows machines," implying non-Windows environments are the better-supported path for scripted access. The source states no limitations regarding the accuracy, validation, spatial/temporal gaps, cloud-cover interference, or false-positive/negative behavior of the underlying CI / CI_cyano cyanobacteria-index products themselves — these scientific caveats are simply absent from this source's text.

## Tensions with other findings
None evident. This is a tool/data-access description, not a scientific or validation study, so it makes no empirical or predictive claims that could be checked against, or that could complicate, other HAB findings. Its main value in a HAB literature review is infrastructural — it documents how the CI_cyano satellite product (which underlies many other CyAN-based studies) is actually queried and retrieved (region, date range, cadence, resolution options), which can help interpret other reviewed sources' methods sections. As a gap rather than a contradiction: the source offers no accuracy or uncertainty figures for CI_cyano itself, so it cannot corroborate or dispute performance statistics reported elsewhere in the HAB literature, and any correlation implied between CI_cyano readings and actual bloom/toxin conditions in other sources should not be read as validated by this source.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The source notes that Earthdata Login is required for 'certain full-functionality features' without explicitly defining what those features are beyond data download; this qualifier about the scope of 'full functionality' is not addressed in the claims.
- **Reviewer notes:** Eight of nine claims are directly and explicitly supported by the source extracts. Claim 5 is marked partial because while the login requirement for downloading and full functionality is explicit, the claim's first premise—that reading the description page requires no account—is not explicitly stated in the source, only implied by the presentation of descriptive content without login-gate language. All dates (2002-present, July 18-25/2023, Sept. 5-26/2017), tool names, agency partners, product types, file formats, and access methods are verified verbatim in the source text. No hallucinated numbers detected."

## Provenance
- Canonical URL: https://www.earthdata.nasa.gov/data/tools/cyan-file-search
- Access date: 2026-07-01
- Full-text access: landing-only | Fetch status: ok
- Fetch notes: The assigned primary URL was fetched twice with different extraction prompts (a "comprehensive extraction" prompt and a "reproduce all text verbatim" prompt); both returned mutually consistent but brief content typical of a NASA Earthdata tool-catalog directory entry, with no quantitative technical specs (resolution, sensor, date range) despite explicit prompting for numbers. Because that landing page exists specifically to point users to the tool's actual launch point, I additionally fetched the linked operational application at https://oceandata.sci.gsfc.nasa.gov/api/cyan_file_search/ to capture the search-parameter and format details needed to describe "what the tool is/does"; this is presented as supplementary detail about the same tool, with its distinct URL cited in each relevant claim's location field, and full_text_access is marked "landing-only" to flag that the assigned primary URL is inherently a thin catalog page rather than a technical document. One WebSearch (query: '"CyAN File Search" earthdata.nasa.gov cyanobacteria index OB.DAAC') was run to cross-check the page's content; it corroborated the Earthdata page's description but also surfaced sensor/era detail (MERIS 2002-2012; OLCI on Sentinel-3A from 2016; OLCI on Sentinel-3B from 2018) that appears to live on a separate NASA Earthdata project page ("Cyanobacteria Assessment Network | NASA Earthdata," https://www.earthdata.nasa.gov/data/projects/cyan) which was not directly fetched for this task. That sensor/era detail is deliberately NOT included in this dossier's key_claims or data_numbers, to avoid attributing content from an unfetched, distinct URL to FED-047. No paywall or login was encountered reading either descriptive page; Earthdata Login is only required to actually download the underlying satellite data files.
