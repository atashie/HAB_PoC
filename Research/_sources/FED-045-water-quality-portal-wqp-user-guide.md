---
key: FED-045
title: Water Quality Portal (WQP) User Guide
authors_or_org: National Water Quality Monitoring Council, in partnership with the U.S. Geological Survey (USGS) and the U.S. Environmental Protection Agency (EPA)
year: 2021 (per the guide's own citation format); page content includes notices referencing updates as recent as March 2024
url: https://www.waterqualitydata.us/portal_userguide/
access_date: 2026-07-01
tier: FED
source_type: Government/interagency web documentation (data-portal user guide), not a peer-reviewed study
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Water Quality Portal (WQP) User Guide

**What it is.** The Water Quality Portal (WQP) is a joint USGS/EPA/National Water Quality Monitoring Council web portal and set of web services that provides unified public access to water-quality monitoring data by merging the USGS NWIS database and the EPA WQX database (formerly STORET). This page is its User Guide, documenting the search interface, query parameters, data-retrieval profiles, download formats, and data-quality caveats.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The WQP unifies data from two underlying systems: NWIS (USGS) and WQX (EPA), the latter formerly called STORET.
  - *evidence:* Stated directly in the guide's description of the 'Data Source' search parameter, which lists NWIS and WQX as the two selectable source databases and explains WQX's lineage from STORET. (Section: 'Explanation of portal search parameters' (Data Source parameter))
  - *quote:* "Formerly the STORET database, this is a data warehouse for water quality, biological, and physical data used by state environmental agencies, the EPA, other federal agencies, universities, private citizens, and others."
- **[✓ verified]** NWIS (USGS) covers roughly 1.5 million monitoring sites across the US and territories and is refreshed every 24 hours.
  - *evidence:* Direct descriptive text for the NWIS data-source option in the search-parameter documentation. (Section: 'Explanation of portal search parameters' (Data Source parameter, NWIS description))
  - *quote:* "Water-resources data collected from approximately 1.5 million sites in all 50 states, the District of Columbia, Puerto Rico, the Virgin Islands, Guam, American Samoa, and the Commonwealth of the Northern Mariana Islands. NWIS (USGS) is updated every 24 hours."
- **[✓ verified]** WQX (EPA) data is refreshed on a weekly cadence, Thursday evenings.
  - *evidence:* Direct descriptive text for the WQX data-source option, immediately following the NWIS description. (Section: 'Explanation of portal search parameters' (Data Source parameter, WQX description))
  - *quote:* "WQX (EPA) is updated weekly on Thursday evening."
- **[✓ verified]** USGS-sourced records in WQP may not yet have received Director's approval, are labeled provisional/subject to revision, and USGS/the federal government disclaim liability for their use.
  - *evidence:* Stated as a formal data-quality/liability disclaimer specific to USGS-origin records. (Section: 'Interpreting USGS data retrieved from the Water Quality Portal')
  - *quote:* "The USGS sourced data available on the Water Quality Portal may include data that have not received Director's approval and as such are provisional and subject to revision. The data are released on the condition that neither the USGS nor the United States Government may be held liable for any damages resulting from its authorized or unauthorized use."
- **[✓ verified]** Individual USGS results move through a status workflow from 'provisional' to 'accepted' after hydrologist review, but even 'accepted' status does not guarantee the value will never be revised later.
  - *evidence:* Explains the per-result QA/QC status field and explicitly warns that 'accepted' is not a permanent guarantee. (Section: 'Interpreting USGS data retrieved from the Water Quality Portal')
  - *quote:* "Results are initially coded with a result status of provisional. After review by a project hydrologist, the result status is usually changed to accepted... an accepted status does not guarantee that results will never be updated."
- **[✓ verified]** The standard/default WQP interface only serves WQX2.2-format profiles, which do not include USGS data added after March 11, 2024; that newer USGS data is only reachable through a separate beta WQX3.0 interface.
  - *evidence:* A dated, explicit data-completeness notice/banner on the guide page describing a coverage gap in the default interface. (Guide page notice/banner (data-availability caveat))
  - *quote:* "This user interface only serves WQX2.2 profiles, which do NOT contain USGS data added after March 11, 2024."
- **[✓ verified]** Downloaded result sets that exceed Excel's row limit will be silently truncated when opened, with only the first 1,048,576 rows displayed.
  - *evidence:* Explicit numeric caveat about the MS Excel (.xlsx) download format option. (Section: 'Explanation of data retrievals' (download format / Excel option))
  - *quote:* "Excel 2007 and later have a limit of 1,048,576 rows. If your download file exceeds this limit, only the first 1,048,576 rows will open."
- **[✓ verified]** Many monitoring stations outside the continental US lack latitude/longitude referenced to the NAD83 datum, so they cannot be located via the portal's point-location/radial-distance search.
  - *evidence:* Direct caveat attached to the point-location (lat/long, NAD83, radial distance) search parameter. (Section: 'Explanation of portal search parameters' (Point Location parameter))
  - *quote:* "Many stations outside the continental US do not have latitude and longitude referenced to NAD83 and cannot be found using these parameters."
- **[✓ verified]** The portal specifies an official citation format, including a DOI, for anyone using WQP-derived data or query results.
  - *evidence:* Given as the recommended citation text in the guide's dedicated citation section. (Section: 'Cite the Water Quality Portal')
  - *quote:* "Water Quality Portal. Washington (DC): National Water Quality Monitoring Council, United States Geological Survey (USGS), Environmental Protection Agency (EPA); 2021. https://doi.org/10.5066/P9QRKUVJ."

## Data / numbers
- ~1.5 million NWIS/USGS monitoring sites nationwide (50 states, DC, Puerto Rico, Virgin Islands, Guam, American Samoa, CNMI)
- NWIS (USGS) refresh interval: every 24 hours
- WQX (EPA) refresh interval: weekly, Thursday evenings
- Excel (.xlsx) download row limit: 1,048,576 rows (Excel 2007+); rows beyond this limit do not open
- Default minimum sampling activities per site (search filter default): 1
- Default minimum results per site (search filter default): 1
- Organization ID / Site ID type-ahead search threshold: at least 2 characters
- USGS data-completeness cutoff for the default (WQX2.2) interface: excludes USGS data added after March 11, 2024
- Citation year given in the official WQP citation: 2021; DOI 10.5066/P9QRKUVJ
- Public contact center phone number: 1-800-424-9067 (email WQX@epa.gov)

## Methods
Not an empirical study; this is portal documentation describing a data-integration and delivery system. WQP harmonizes two independently-operated monitoring databases (USGS NWIS and EPA WQX/STORET) behind a single search UI (Basic and Advanced query forms) and equivalent REST web services, using shared query parameters (country/state/county FIPS codes, HUC, point-location with NAD83 lat/long + radial distance, bounding box, organization/site/project ID, date range, sample media, characteristic group/characteristic, parameter code, minimum activities/results per site). Output is delivered as one of several 'data profiles' at different granularities (organization, site-only, project metadata vs. sample results — physical/chemical, biological, or narrow —, sampling activity, sampling activity metrics, biological habitat metrics, project monitoring-location weighting, and detection/quantitation-limit data), downloadable as comma-separated, tab-separated, or MS Excel files. The guide states this approach works for harmonized, multi-agency retrieval of in-situ monitoring records by location/parameter/date, but explicitly states it does not currently expose the newest USGS data through the default interface (see limitations) and does not resolve non-CONUS station coordinates in the standard geographic search.

## Stated limitations
(1) The default, non-beta WQP interface serves only WQX2.2 profiles and explicitly does NOT contain USGS data added after March 11, 2024 — current/newer USGS records require the separate beta WQX3.0 profiles. (2) USGS-origin data may lack Director's approval and are labeled provisional/subject to revision, with USGS/US Government disclaiming liability for use. (3) Even results marked 'accepted' after hydrologist review are not guaranteed to remain unchanged ('an accepted status does not guarantee that results will never be updated'). (4) Data recently added to either source system (NWIS or WQX) 'may not be immediately accessible through the WQP' — i.e., a lag exists between source-system update and portal availability. (5) Many non-continental-US stations lack NAD83-referenced coordinates and cannot be found via the point-location/radial-distance search. (6) MS Excel downloads silently truncate at 1,048,576 rows. (7) The second fetch pass found no explicit statement in the guide of a maximum-records-per-query, request timeout, or file-size cap — such limits, if they exist, are not documented on this page.

## Tensions with other findings
This is infrastructure documentation, not a HAB-outcome study, so it does not itself make competing scientific claims; the practical tensions are for downstream use: (a) The March 11, 2024 USGS-data cutoff on the standard interface is a material risk for any current-cycle (2024-2026) HAB analysis that pulls 'live' USGS nutrient/temperature/discharge records through the default WQP UI or web services — recent USGS in-situ data could be silently absent unless the WQX3.0 beta endpoint is used, which could understate very recent driver signals when fusing with satellite (e.g., CyAN) observations. (b) The provisional-to-accepted status workflow, and the explicit statement that 'accepted' does not guarantee finality, is in tension with treating any single WQP snapshot as a fixed ground truth for model training/validation — a reproducible pipeline must record the pull date, because re-querying WQP later for the 'same' historical period can return revised values (this is a portal-level version of look-ahead/data-drift risk relevant to CLAUDE.md's fidelity and reproducibility requirements for this project).

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All nine claims are directly supported by explicit statements in the source text. No numeric values were hallucinated; all figures (1.5 million sites, 1,048,576 rows, March 11 2024, 24-hour and Thursday-evening refresh schedules) appear verbatim in the source. No material caveats present in the source were omitted from the claims. The extraction is faithful and complete."

## Provenance
- Canonical URL: https://www.waterqualitydata.us/portal_userguide/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: WebFetch succeeded on both calls at the primary URL (no redirect, no WebSearch fallback needed) — full_text_access is treated as 'full' since the guide's actual content (not a landing/abstract page) was retrieved twice. Fetch 1 used a general/overview extraction prompt; Fetch 2 used a technical/parameter-and-citation-focused prompt; outputs were reconciled by union — they agree on all overlapping facts (NWIS ~1.5M sites/24-hr updates, WQX weekly Thursday updates, provisional/accepted status language, March 11 2024 USGS cutoff on the WQX2.2 interface, Excel 1,048,576-row limit, 2021 citation with DOI 10.5066/P9QRKUVJ, contact info) with no direct contradictions. Two small internal inconsistencies surfaced within Fetch 1's own summarization (a 'small model' rendering artifact, as flagged in the task instructions) and were NOT promoted to data_numbers: (1) site types described as '15+' but only 14 discrete terms enumerated; (2) sample media described as 'eight categories' but nine terms enumerated. These are noted here and in source_extract rather than asserted as verified figures. Both fetches independently confirm no explicit statement of a maximum-records-per-query, timeout, or file-size cap exists on this page, which is itself treated as a stated (negative) finding under 'stated_limitations' rather than an omission on my part.
