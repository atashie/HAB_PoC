---
key: FED-076
title: Water Quality Portal | U.S. Geological Survey
authors_or_org: U.S. Geological Survey (U.S. Department of the Interior)
year: 2019
url: https://www.usgs.gov/tools/water-quality-portal
access_date: 2026-07-01
tier: FED
source_type: Government agency web page — USGS tool overview/landing page
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: landing-only
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Water Quality Portal | U.S. Geological Survey

**What it is.** A short USGS "tool" catalog/landing page (dated March 4, 2019) that describes the Water Quality Portal (WQP) — a unified web search interface integrating publicly available water-quality data from USGS NWIS/BioData, EPA STORET, and USDA-ARS STEWARDS — and points users to the actual portal at waterqualitydata.us; it is a pointer/overview page rather than the data portal or its technical documentation.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The Water Quality Portal integrates and provides access to publicly available water-quality data from multiple federal/state source databases (USGS NWIS and BioData, EPA STORET, USDA-ARS STEWARDS) through one single search interface.
  - *evidence:* This is the page's core descriptive sentence naming the specific source systems that feed the unified portal. (Main content / description paragraph)
  - *quote:* "The Water Quality Portal integrates and provides access to publicly available water-quality data from databases such as USGS NWIS and BioData, EPA STORET, and USDA-ARS STEWARDS through a single search interface."
- **[✓ verified]** Data in the portal is contributed by USGS, EPA, and a large additional set of other agencies, described as over 400 state, federal, tribal, and local agencies.
  - *evidence:* Stated in the image caption/associated descriptive text as the scope of contributing organizations beyond USGS and EPA themselves; given as a lower-bound count ('over 400') with no further breakdown or uncertainty. (Associated image caption)
  - *quote:* "over 400 state, federal, tribal, and local agencies"
- **[✓ verified]** The actual query/download interface for the integrated data lives at a separate site, www.waterqualitydata.us, not on this USGS page itself.
  - *evidence:* The page functions as a pointer: it names the tool and its sponsoring databases but sends users elsewhere for the working interface, meaning this specific page carries no data-access, parameter, or record-count detail of its own. (Primary link)
  - *quote:* "a single search interface"
- **[✓ verified]** This specific overview page is administratively tied to USGS's Water Resources Mission Area and was published March 4, 2019, filed under Web Tools > Data Access Tools, with topical association to the Idaho, New Jersey, New York, and Upper Midwest Water Science Centers.
  - *evidence:* Page metadata / related-topics sidebar; indicates page provenance and internal USGS categorization rather than a scientific finding. (Page metadata / Related Search Topics / footer)
  - *quote:* "Date Published: March 4, 2019"

## Data / numbers
- over 400 (state, federal, tribal, and local agencies contributing data to the portal — approximate/lower-bound count, no uncertainty or exact figure given)
- Page date: March 4, 2019 (page publication/last-noted date, not a data-currency date)

## Methods
Not applicable in the methods-paper sense — this is a descriptive landing page, not a study. Its only 'method' content is naming the four contributing source systems that WQP harmonizes (USGS NWIS, USGS BioData, EPA STORET, USDA-ARS STEWARDS) and directing users to the working query tool at waterqualitydata.us for actual data retrieval; no query mechanics, file formats, parameter taxonomy, or API detail appear on this page.

## Stated limitations
None stated on this page. It contains no caveats about data quality, provisional vs. approved status, latency, spatial/temporal coverage gaps, or QA/QC — a notable absence given this is being cited as an in-situ data source; any such caveats would need to be sourced from waterqualitydata.us or its documentation rather than this overview page.

## Tensions with other findings
None directly, since the page makes no scientific or HAB-related claims. The main tension for our use is methodological/traceability: this page alone cannot support any claim about WQP's data quality, coverage, or limitations (e.g., provisional-data flags, chlorophyll-a/nutrient parameter availability, record counts) — those would require fetching the actual portal or its API docs; citing only this landing page for anything beyond "WQP exists, is run by USGS/EPA/USDA-ARS, and aggregates 400+ agencies" would overstate what this source supports.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All four claims are directly supported by the SOURCE TEXT. No numerical hallucinations detected: both the "over 400 agencies" figure and the "March 4, 2019" publication date are explicitly present in the source. No caveats or qualifications were dropped, as the source text itself notes (in bracketed metadata) that no limitations, caveats, or parameter details are present on the page — meaning there were none to omit. The claims accurately represent the page's descriptive and metadata content."

## Provenance
- Canonical URL: https://www.usgs.gov/tools/water-quality-portal
- Access date: 2026-07-01
- Full-text access: landing-only | Fetch status: ok
- Fetch notes: Fetched https://www.usgs.gov/tools/water-quality-portal directly with WebFetch (twice, with two different extraction prompts, to cross-check completeness); both fetches returned consistent, coherent, on-topic content — not blocked, empty, or garbage — so no WebSearch fallback was needed and url_used = resolved_url = the given primary URL. The page itself is inherently short: a USGS "tool" catalog/landing entry (dated March 4, 2019) that names the source databases (NWIS, BioData, STORET, STEWARDS) and contributing-agency count ('over 400') and then points to the real portal at waterqualitydata.us for actual data access, parameters, and downloads. It contains no data-volume figures (no site/record counts), no parameter taxonomy, no temporal coverage statement, and no stated limitations/QA caveats — these gaps are reported faithfully above rather than filled in from outside knowledge. Categorized as in-situ-and-weather-data (matches provisional) since WQP is the in-situ water chemistry aggregator named in the project's sanctioned source list; kept relevance at Medium (matching provisional) because the page confirms sponsorship/scope usefully for citation purposes but has no technical depth (no API, parameters, or record counts) that would justify High.
