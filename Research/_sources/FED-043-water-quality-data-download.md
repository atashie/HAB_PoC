---
key: FED-043
title: Water Quality Data Download
authors_or_org: U.S. Environmental Protection Agency (EPA), Office of Water / Water Data and Tools; the featured Water Quality Portal is co-sponsored by USGS, EPA, and the National Water Quality Monitoring Council
year: 2026 (page "last updated" May 22, 2026; this is a continuously-maintained EPA web page, not a dated publication)
url: https://www.epa.gov/waterdata/water-quality-data-download
access_date: 2026-07-01
tier: FED
source_type: Government agency web page — data-access hub / landing page (not a peer-reviewed study)
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Water Quality Data Download

**What it is.** EPA's "Water Quality Data Download" page is the agency's central web hub explaining how to obtain in-situ water quality data (physical, chemical, biological, habitat, and metrics/indexes data) contributed by over 1,500 federal, state, and tribal agencies and other organizations — chiefly via the Water Quality Portal (WQP) — and it links out to the Water Quality eXchange (WQX) data format, the Legacy Data Center (pre-1999 archive), and several downstream analysis/visualization tools.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** EPA's Water Quality Data Download page states that water quality data submitted from over 1,500 federal, state and tribal agencies, watershed organizations, and other groups are available to support water quality analyses, spanning physical, chemical, biological, habitat, and metrics/indexes data.
  - *evidence:* Directly stated as the page's opening description of data scope and data types available for download. (Main page heading / introductory paragraph)
  - *quote:* "Water quality data submitted from over 1,500 federal, state and tribal agencies, watershed organizations and other groups are available to support your water quality analyses."
- **[✓ verified]** The Water Quality Portal (WQP) is a cooperative service sponsored by USGS, EPA, and the National Water Quality Monitoring Council, and it serves over 430 million water result records.
  - *evidence:* Stated directly, naming the three co-sponsoring bodies and giving the cumulative record count. ("Water Quality Portal" section)
  - *quote:* "a cooperative service sponsored by the United States Geological Survey, the Environmental Protection Agency and the National Water Quality Monitoring Council ... over 430 million water result records"
- **[✓ verified]** The WQP aggregates data from multiple underlying source systems, including EPA's Water Quality eXchange (WQX) and the USGS National Water Information System (NWIS), plus other government agencies.
  - *evidence:* Describes the source systems that feed into the Portal's aggregated record count. ("Water Quality Portal" section)
  - *quote:* "from multiple sources including EPA's Water Quality eXchange (WQX), USGS National Water Information System, and government agencies"
- **[✓ verified]** Water Quality eXchange (WQX) is defined on this page as a universal format for sharing water quality data.
  - *evidence:* Direct definitional statement of what WQX is/does. (WQX description)
  - *quote:* "a universal format for sharing water quality data"
- **[✓ verified]** The Legacy Data Center (LDC) contains historical water quality data dating back to the early 20th century through the end of 1998, is no longer being added to, but remains publicly accessible (including via FTP).
  - *evidence:* States the temporal coverage of the legacy STORET-derived archive and its current (frozen but accessible) status. ("Legacy Data" section)
  - *quote:* "historical water quality data dating back to the early part of the 20th century and collected up to the end of 1998"
- **[✓ verified]** The page enumerates downstream tools built on WQP/WQX data, including How's My Waterway (which integrates over 30 separate data sources), TADA, the WQI screening tool, EDM, CyAN, and Freshwater Explorer (covering all 50 U.S. states, Puerto Rico, and the U.S. Virgin Islands), plus a Harmful Algal Toxins StoryMap.
  - *evidence:* Lists agency tools that consume WQP data, including HAB-specific tools (CyAN, the algal toxins StoryMap), directly relevant to this project's data-source landscape. ("Agency Tools Using WQP" section)
  - *quote:* "data and information from over 30 separate data sources ... all 50 U.S. states, Puerto Rico, and the U.S. Virgin Islands"
- **[✓ verified]** The page itself contains no explicit data-quality warnings, uncertainty statements, or interpretation caveats.
  - *evidence:* One extraction pass explicitly checked for and reported the absence of such disclaimers on this page. (General page review (absence noted across both extraction passes))
  - *quote:* "No Warnings or Data Quality Disclaimers Present"

## Data / numbers
- over 1,500 federal, state, and tribal agencies, watershed organizations, and other groups contributing data (per this EPA page; a related WQP-description page instead states "more than 1,000 programs, organizations, Tribes, and agencies" — see tensions)
- over 430 million water result records in the Water Quality Portal (cumulative count, no stated uncertainty; independently corroborated via WebSearch)
- over 30 separate data sources integrated into the How's My Waterway tool
- geographic coverage: all 50 U.S. states, Puerto Rico, and the U.S. Virgin Islands (Freshwater Explorer tool)
- Legacy Data Center temporal range: data collected from "the early part of the 20th century" through "the end of 1998" (no records/count given, only date bounds)
- page last updated: May 22, 2026

## Methods
This is not a research study but a data-infrastructure description page. Water Quality Portal (WQP) = a cooperative aggregation service sponsored by USGS, EPA, and the National Water Quality Monitoring Council, pulling from EPA's Water Quality eXchange (WQX), the USGS National Water Information System (NWIS), and other contributing agencies. WQX = a submission format/schema ("a universal format for sharing water quality data"); WQXWeb = a web platform for building custom data imports into WQX. Legacy Data Center (LDC) = a static historical archive (data collected "up to the end of 1998," dating back to "the early part of the 20th century"), accessible via FTP (gaftp.epa.gov/storet/exports/), no longer being added to. Downstream tools named (but not methodologically detailed) on this page: Tools for Automated Data Analysis (TADA, R-based), the dataRetrieval R package, How's My Waterway, the Water Quality Indicators (WQI) screening tool, EPA's Estuary Data Mapper (EDM), CyAN (Cyanobacteria Assessment Network), and Freshwater Explorer.

## Stated limitations
Neither extraction pass found any explicit data-quality caveats, uncertainty statements, or methodological limitations on the page itself; one pass explicitly confirmed "No Warnings or Data Quality Disclaimers Present." As a navigation/access hub rather than an analysis, the page does not discuss comparability of sampling/QA methods across its 1,500+ contributing agencies, record-level data quality, or interpretation guidance — it only notes that the Legacy Data Center is static/no-longer-updated and points users to a separate "Quick Reference Guide" and training materials (a video and a WQX 101 course module) for usage detail not captured in this fetch.

## Tensions with other findings
No direct contradiction of other HAB findings appears in the fetched text — this is a data-infrastructure reference, not an analytical claim. Two points worth flagging for the broader review: (1) An independent, related EPA/WQP page (found via a corroborating WebSearch, not fetched in full for this dossier) describes the WQP as built from "more than 1,000 programs, organizations, Tribes, and agencies," versus "over 1,500" federal/state/tribal agencies stated on this specific page — a minor inconsistency across EPA's own materials, likely reflecting different snapshot dates or counting units (programs vs. agencies) rather than a substantive conflict; the "430 million" record figure, however, was independently corroborated. (2) The page lists CyAN (a satellite/remote-sensing cyanobacteria detection tool) alongside WQP-derived in-situ tools as parallel "agency tools using WQP," which is useful corroboration that EPA itself treats satellite HAB detection and in-situ chemistry monitoring as complementary-but-structurally-separate data pipelines — supportive of, not contradictory to, this project's remote-sensing + in-situ fusion framing.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All seven claims are directly supported by the source text (both FETCH 1 and FETCH 2 extraction passes, with corroborating websearch). No numbers are hallucinated; all figures (1,500 agencies, 430 million records, 30+ data sources, 50 states/territories coverage) appear verbatim in the source. No material caveats or qualifications are dropped. The claim about 'no data-quality warnings' is explicitly confirmed in FETCH 2 as an absence statement. The characterization of tools as 'downstream tools built on WQP/WQX data' is a reasonable interpretation of the source's 'Agency Tools Using WQP' section header."

## Provenance
- Canonical URL: https://www.epa.gov/waterdata/water-quality-data-download
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary URL twice with different extraction prompts per instructions (one focused on datasets/tools/numbers, one focused on a structured content inventory of headings/links/agencies); the two passes converged closely and were reconciled by union with no material conflicts between them. Ran one corroborating WebSearch ("EPA Water Quality Data Download waterdata.epa.gov 430 million 1,500 water quality portal") which independently confirmed the Water Quality Portal's "430 million" water result records figure and its USGS/EPA/National Water Quality Monitoring Council sponsorship via a related WQP description page and Data.gov catalog entry, giving confidence the fetched content is genuine (not a fetch-model confabulation) and that this is the correct page. That same search surfaced a related WQP-description page citing "more than 1,000 programs, organizations...and agencies" rather than "1,500," which I flag under tensions as a minor cross-page inconsistency rather than resolving it, since I did not fetch that second page in full. No PDF/binary issues; the page rendered cleanly as HTML/text in both fetches. Given this is a live, continuously-updated agency web page rather than a dated publication, I report "year" as the stated page-last-updated date rather than a true publication year.
