---
key: FED-023
title: Introduction to the dataRetrieval package (USGS)
authors_or_org: Laura A. DeCicco & Robert M. Hirsch (lead authors); full contributing team per citation: D. Lorenz, J. Read, J. Walker, L. Platt, W.D. Watkins, D.L. Blodgett, M. Johnson, A. Krall, L. Stanish, J. Zemmels, E.D. Hinman, M. Mahoney — U.S. Geological Survey (USGS)
year: 2026
url: https://doi-usgs.github.io/dataRetrieval/articles/dataRetrieval.html
access_date: 2026-07-01
tier: FED
source_type: Software package documentation / online vignette (USGS-authored R package article, hosted on GitHub Pages under the USGS "doi-usgs" organization)
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Introduction to the dataRetrieval package (USGS)

**What it is.** dataRetrieval is a USGS-maintained R package (documented as version 2.7.25) that provides functions to query and download U.S. Geological Survey hydrologic data — streamflow/discharge, gage height, water temperature, groundwater levels, peak flows, rating curves, and site metadata — from the USGS Water Data API and USGS Samples Data service, as well as discrete water-quality data (nutrients, pH, specific conductance, chloride, etc.) from the multi-agency Water Quality Portal (EPA, USDA, USGS), returning results directly as R data frames.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** dataRetrieval is an R package created to simplify loading hydrologic data into the R environment, covering major USGS hydrologic data types available on the web plus discrete water-quality data from the multi-agency Water Quality Portal (WQP).
  - *evidence:* Stated directly in the package's introductory/overview text describing its purpose and scope. (Introduction / Overview section)
  - *quote:* "was created to simplify the process of loading hydrologic data into the R environment"
- **[✓ verified]** WQP, one of the package's two main data backends, currently houses water-quality data contributed by EPA, USDA, and USGS.
  - *evidence:* Overview text names the three contributing federal agencies behind WQP. (Introduction / Overview section)
  - *quote:* "currently houses water quality data from the Environmental Protection Agency (EPA), U.S. Department of Agriculture (USDA), and USGS"
- **[✓ verified]** The package exposes a family of read_waterdata_* functions, each mapped to a specific USGS Water Data API product (daily values, continuous/instantaneous values, rating tables, field measurements, peak flows, monitoring-location/site metadata, parameter-code lookups, period-of-record and date-range statistics), plus separate readWQP*/whatWQP* functions for Water Quality Portal queries and read_waterdata_samples/summarize_waterdata_samples for the USGS Samples Data service.
  - *evidence:* Drawn from 'Table 1: dataRetrieval functions', which both fetches independently rendered as a function-to-data-type-to-source mapping table, corroborating each other. (Table 1: dataRetrieval functions)
  - *quote:* "read_waterdata_daily Daily values USGS Water Data API"
- **[✓ verified]** A worked example retrieves daily discharge (parameter code 00060) for USGS monitoring location 01491000, the Choptank River near Greensboro, MD, over 1980-01-01 to 2010-01-01 using read_waterdata_daily.
  - *evidence:* Basic workflow code example names this exact site, parameter code, and date range. (Basic workflow example (code block))
  - *quote:* "Choptank River near Greensboro, MD"
- **[✓ verified]** Documented USGS parameter codes include 00060 (Discharge, ft3/s), 00065 (Gage height, ft), 00010 (Temperature, C), 00045 (Precipitation, in), 00400 (pH), and 00631 (Nitrate plus nitrite, water, filtered, milligrams per liter as nitrogen).
  - *evidence:* Parameter-code reference table shown alongside the code examples. (Parameter Codes table)
  - *quote:* "00631 | Nitrate plus nitrite, water, filtered, milligrams per liter as nitrogen"
- **[✓ verified]** Documented statistic codes for daily-value aggregation include 00001 (Maximum), 00002 (Minimum), 00003 (Mean), and 00008 (Median).
  - *evidence:* Statistic-code table paired with the temperature/discharge daily-values example. (Statistic Codes table)
  - *quote:* "00003 | Mean"
- **[✓ verified]** USGS's water data APIs impose query rate limits keyed to the requesting IP address per hour, and users are directed to register for a personal API token (stored as an .Renviron variable) to use with the package.
  - *evidence:* API-access subsection describes IP-based hourly rate limiting, gives a signup URL, and shows the exact .Renviron variable syntax plus a note that R must be restarted after setup. (API Access / token section)
  - *quote:* "API_USGS_PAT = "my_super_secret_token""
- **[✓ verified]** Data retrieved by the package is time-stamped in UTC; the documentation illustrates this by noting that a local U.S. Eastern Standard Time midnight appears five hours offset in the returned dateTime column.
  - *evidence:* Explicit worked explanation of the UTC conversion behavior of the returned dateTime column. (Data time zones section)
  - *quote:* "midnight EST will be 5 hours earlier in the dateTime column (the previous day, at 7pm)"
- **[✓ verified]** USGS surface-water monitoring sites are typically identified with 8-digit numbers (e.g., 01491000) while groundwater sites typically use 15-digit numbers (e.g., 434400121275801), both prefixed 'USGS-' in the newer API functions.
  - *evidence:* Demonstrated by contrasting the surface-water code example against the groundwater-levels code example; general rule stated in the key-requirements summary. (Groundwater levels example vs. basic workflow example)
  - *quote:* "USGS-434400121275801"
- **[✓ verified]** Left unspecified, the startDate/endDate arguments default to requesting the maximum available data (full period of record) for a site/parameter.
  - *evidence:* Stated directly as a default-argument behavior note in the function documentation excerpt. (Function defaults note)
  - *quote:* "The arguments startDate and endDate have defaults to request the maximum data."
- **[✓ verified]** The documentation states that legacy water-use data services have been retired, with replacement functionality not yet available at the time of writing.
  - *evidence:* A callout/note under the water-use function description flags this as a known current gap in the package's coverage. (Water-use data section / note)
  - *quote:* "Legacy water use data services have been retired. Check back in for developments on replacement functions."
- **[✓ verified]** USGS attaches a standing disclaimer to this information, describing it as preliminary and subject to revision, provided to meet the need for timely best science, with no liability accepted by USGS or the U.S. Government for damages arising from its use.
  - *evidence:* Standard USGS legal/quality disclaimer reproduced at the foot of the document. (Disclaimer / footer)
  - *quote:* "This information is preliminary and is subject to revision. It is being provided to meet the need for timely best science."
- **[✓ verified]** The documented package version is 2.7.25, citable as a USGS software release (De Cicco, Hirsch, Lorenz, Watkins, Johnson, Blodgett, Hinman, Zemmels, 2026), alongside separate recommended citation templates for the underlying NWIS and WQP data themselves.
  - *evidence:* Citation section gives the package DOI/version plus the two recommended data-citation templates for NWIS (USGS Water Data for the Nation) and WQP (National Water Quality Monitoring Council). (Citation section)
  - *quote:* "v.2.7.25, doi:10.5066/P9X4L3GE"
- **[✓ verified]** Water Quality Portal query examples in the documentation filter by state/county FIPS-style codes and characteristic-name strings, e.g., specific conductance at site WIDNR_WQX-10032762, chloride sites in state code US:34, and pH records in state code US:55 / county code US:55:025.
  - *evidence:* Multiple WQP-oriented code examples (readWQPqw, whatWQPsites, readWQPdata, whatWQPdata) demonstrate the query-filter vocabulary (state code, county code, characteristic name) the package expects for WQP calls. (Water Quality Portal examples (code block))
  - *quote:* "characteristicName = "Chloride""

## Data / numbers
- Documented package version: v.2.7.25 (DOI 10.5066/P9X4L3GE)
- Parameter code 00060 = Discharge [ft3/s]
- Parameter code 00065 = Gage height [ft]
- Parameter code 00010 = Temperature [C]
- Parameter code 00045 = Precipitation [in]
- Parameter code 00400 = pH (unitless)
- Parameter code 00631 = Nitrate plus nitrite, water, filtered [mg/L as nitrogen]
- Statistic code 00001 = Maximum
- Statistic code 00002 = Minimum
- Statistic code 00003 = Mean
- Statistic code 00008 = Median
- Surface-water monitoring-location IDs: 8 digits (example: USGS-01491000)
- Groundwater monitoring-location IDs: 15 digits (example: USGS-434400121275801)
- Example date range in basic workflow: 1980-01-01 to 2010-01-01
- Time-zone conversion example: 'midnight EST will be 5 hours earlier in the dateTime column (the previous day, at 7pm)'
- NWIS data-citation DOI: 10.5066/F7P55KJN
- WQP data-citation DOI: 10.5066/P9QRKUVJ
- Document build/version date given as June 2, 2026; citation year given as 2026

## Methods
The source documents a software tool, not a scientific study: dataRetrieval is an R package whose functions wrap HTTP calls to (a) the USGS Water Data API (read_waterdata* functions: daily values, continuous/instantaneous values, rating tables, field measurements, peak flows, site/monitoring-location metadata, parameter-code lookups, period-of-record and date-range statistics), (b) the USGS Samples Data service (read_waterdata_samples, summarize_waterdata_samples), and (c) the multi-agency Water Quality Portal (readWQPdata, readWQPqw, whatWQPsites, whatWQPdata, whatWQPsamples, whatWQPmetrics, readWQPsummary), returning tidy R data frames. It states this works for USGS-monitored surface-water and groundwater sites nationally (identified by 8- and 15-digit site numbers respectively) and for WQP-aggregated water-quality records contributed by EPA, USDA, and USGS. It documents one area where retrieval currently does not work: legacy water-use data services have been retired with no confirmed replacement function yet available. Access is otherwise rate-limited by requesting IP address per hour, mitigated by registering a free API token used via an .Renviron environment variable.

## Stated limitations
The source itself states: (1) USGS water-data APIs enforce query rate limits by requesting IP address per hour, mitigated only by registering a personal API token; (2) legacy water-use data retrieval services have been retired and no replacement is yet confirmed ("Check back in for developments on replacement functions"); (3) returned timestamps are converted to UTC, which can be non-obvious relative to local U.S. time zones (illustrated with an EST example) and requires the user to handle conversion/awareness themselves; (4) a standing USGS disclaimer that the information is "preliminary and is subject to revision," offered "to meet the need for timely best science," with USGS/U.S. Government accepting no liability for damages from its use. Separately, as an extraction-completeness caveat rather than a limitation of the package itself: this dossier's WebFetch passes could not confirm (and the tool explicitly reported as not found in the rendered excerpt) any discussion of specific legacy function names, related packages (e.g., EGRET, toxEval), a session-info/version footer, a firm sunset date for retired services, or documented behavior for zero-result queries — these should be treated as unverified from this fetch, not as confirmed absent from the live page.

## Tensions with other findings
This is a data-access software tool, not a HAB-analytic or ecological study, so it does not itself make findings that contradict other HAB literature. Two analyst-level (not source-stated) observations relevant to fusing this source with the rest of the HAB dossier: (a) dataRetrieval only reaches in-situ/discrete hydrologic and water-quality time series (e.g., discharge, gage height, temperature, nutrients, pH) and the separate USGS Samples service — it does not provide the remote-sensing/satellite HAB signal (e.g., EPA CyAN cyanobacteria index) itself, so any fused analysis must independently join dataRetrieval-sourced records to a satellite product by site location and date, a step this source does not describe; (b) because WQP aggregates records contributed by multiple agencies (EPA, USDA, USGS) that may use different field/lab protocols, cross-agency method harmonization is a reasonable open question for downstream analysis, but the fetched text does not itself discuss QA/QC harmonization across contributing agencies, so this is flagged here as an unresolved question rather than attributed to the source.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0

## Provenance
- Canonical URL: https://doi-usgs.github.io/dataRetrieval/articles/dataRetrieval.html
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary URL directly with WebFetch three times (two required by protocol plus one supplemental targeted pass to test for specific sections/absences), no redirect occurred, so url_used = resolved_url = the primary URL given. Fetch 1 used a broad "comprehensive extraction" prompt and returned a rich, well-structured summary (function table, code examples, parameter/statistic code tables, API-token/rate-limit info, UTC time-zone note, site-numbering convention, citation block, legal disclaimer). Fetch 2 targeted narrative/workflow/related-package content and returned a much thinner response, confirming the package's stated purpose and the "legacy water use data services retired" note but explicitly stating it could not find, in the rendered excerpt, details on older legacy function names (readNWISdv/readNWISuv/readNWISqw etc.) or related packages (EGRET/toxEval). Fetch 3 directly tested for those gaps (legacy function names, EGRET/toxEval mentions, session-info/version footer, NWIS sunset date, empty-query/no-data behavior, other environment variables) and reported each as not present in the fetched excerpt. Because WebFetch renders via a small summarizing model that can drop content inconsistently between calls, these "not present" results are treated as "not verified from this fetch" rather than a confirmed absence from the live page, and are reported that way in stated_limitations/tensions rather than asserted as fact. All quotes reproduced in key_claims/source_extract are the direct quotations the fetch tool itself presented as verbatim page text; no numbers were paraphrased by the analyst. This is USGS software-package documentation (a vignette/article), not a peer-reviewed study, so it contains no baselines, uncertainty estimates, or HAB-specific findings — data_numbers therefore lists parameter/statistic codes, version, and DOIs rather than a scientific baseline+uncertainty pair. Today's environment date (2026-07-01) is consistent with the document's self-reported "June 2, 2026" build date and "2026" citation year, so this is treated as the source's stated (live, continuously-updated vignette) metadata rather than an error.
