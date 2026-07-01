---
key: FED-018
title: GitHub - DOI-USGS/dataretrieval-python: Python package for retrieving water data from USGS or the multi-agency Water Quality Portal
authors_or_org: DOI-USGS (U.S. Geological Survey); suggested-citation authors: Hodson, T.O., Hariharan, J.A., Black, S., and Horsburgh, J.S.
year: 2023 (suggested-citation software release); repository actively maintained through latest release v1.2.0 (Jun 24, 2026)
url: https://github.com/DOI-USGS/dataretrieval-python
access_date: 2026-07-01
tier: FED
source_type: Software repository (GitHub) / USGS software release, not a peer-reviewed paper
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# GitHub - DOI-USGS/dataretrieval-python: Python package for retrieving water data from USGS or the multi-agency Water Quality Portal

**What it is.** dataretrieval-python is a USGS-maintained (DOI-USGS) open-source Python package, the Python counterpart to USGS's R `dataRetrieval` package, that provides a programmatic interface for discovering and retrieving major U.S. hydrologic and water-quality data types from federal web services: the modern USGS Water Data API, the National Ground-Water Monitoring Network (NGWMN), the multi-agency Water Quality Portal (WQP, aggregating USGS/EPA/other agencies), the Network Linked Data Index (NLDI), a modeled water-use dataset, and a deprecated legacy NWIS interface.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The package's stated purpose is to simplify loading hydrologic data into Python by retrieving major USGS hydrology data types plus data from the Water Quality Portal (WQP), the National Ground-Water Monitoring Network (NGWMN), and the Network Linked Data Index (NLDI).
  - *evidence:* Stated directly in the repository README's package-overview description, and reflected in the module structure (waterdata, ngwmn, nwis, wqp, nldi, wateruse) both fetches independently returned. (README, package overview section)
  - *quote:* "The dataretrieval package simplifies loading hydrologic data into Python, retrieving major U.S. Geological Survey (USGS) hydrology data types available on the Web, as well as data from the Water Quality Portal (WQP), the National Ground-Water Monitoring Network (NGWMN), and the Network Linked Data Index (NLDI)."
- **[✓ verified]** The Water Quality Portal module (dataretrieval.wqp) retrieves analytical results, monitoring locations, organizations, and project details, and the WQP itself aggregates contributions from USGS, EPA, and other agencies.
  - *evidence:* Given in the module-by-module breakdown of the WQP functions (get_results, what_sites, what_organizations, what_projects) and the description of what the WQP aggregates. (README, Water Quality Portal module section)
  - *quote:* "USGS, EPA, and other agencies"
- **[✓ verified]** The legacy `dataretrieval.nwis` module (functions get_dv, get_iv, get_info, get_stats, get_discharge_peaks) is explicitly marked deprecated in favor of the newer `dataretrieval.waterdata` module.
  - *evidence:* The README lists the nwis module with an explicit 'Deprecated' label, distinct from the actively promoted waterdata module that supersedes it (get_daily, get_continuous, get_field_measurements, etc.). (README, Legacy NWIS module section)
  - *quote:* "Legacy NWIS (`dataretrieval.nwis`) — Deprecated"
- **[✓ verified]** Users are advised to obtain a USGS API key for higher rate limits and to break continuous (high-frequency) data requests into smaller time windows to avoid timeouts.
  - *evidence:* Given as explicit operational guidance/warnings in the README aimed at users making large or repeated queries. (README, usage notes / important warnings section)
  - *quote:* "Users are strongly encouraged to obtain an API key for higher rate limits. ... We _strongly advise_ breaking continuous data requests into smaller time windows to avoid timeouts and other issues."
- **[✓ verified]** The software carries the standard USGS provisional-software disclaimer: it is preliminary/provisional, has not received final USGS approval, and neither USGS nor the U.S. Government accepts liability for its use.
  - *evidence:* Standard USGS open-source software disclaimer text present verbatim in the repository, returned identically in substance by both fetches. (README, disclaimer section)
  - *quote:* "This software is preliminary or provisional and is subject to revision... The software has not received final approval by the U.S. Geological Survey (USGS)... The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from its authorized or unauthorized use."
- **[✓ verified]** Development of the package was partially funded by a National Science Foundation award.
  - *evidence:* Stated as a funding acknowledgment line in the README. (README, acknowledgments)
  - *quote:* "This material is partially based upon work supported by the National Science Foundation (NSF) under award 1931297."
- **[✓ verified]** The official suggested citation is Hodson, Hariharan, Black, and Horsburgh (2023), published as a USGS software release with DOI 10.5066/P94I5TX3.
  - *evidence:* Given verbatim as the README's suggested citation; corroborated independently via WebSearch, which surfaced the same DOI, authorship, and description ('a Python package for discovering and retrieving water data available from U.S. federal hydrologic web services') on the GitHub README, PyPI, and USGS Water Mission Area tool-catalog listings. (README, citation section)
  - *quote:* "Hodson, T.O., Hariharan, J.A., Black, S., and Horsburgh, J.S., 2023, dataretrieval (Python): a Python package for discovering and retrieving water data available from U.S. federal hydrologic web services: U.S. Geological Survey software release, https://doi.org/10.5066/P94I5TX3."
- **[✓ verified]** As of the fetch date, the repository listed 252 stars, 59 forks, 11 watchers, 7 open issues, 8 open pull requests, 23 releases (latest v1.2.0, dated Jun 24, 2026), 421 total commits, and a language composition of 100% Python.
  - *evidence:* Read directly from the GitHub repository page's stats/sidebar at fetch time by both extraction passes (values matched across both fetches). These are dynamic repository metrics that will change as the project evolves, not a fixed property of the software. (GitHub repo page, sidebar/stats (as rendered at fetch time, 2026-07-01))
- **[✓ verified]** dataretrieval-python is presented as the Python counterpart to / mirror of USGS's original R package `dataRetrieval`.
  - *evidence:* Noted as a related-package reference in the README; corroborated by WebSearch results describing the Python package as adapted from the R `dataRetrieval` package created by Timothy Hodson at USGS. (README, related packages note)
- **[✓ verified]** Query functions return a two-item result of a pandas DataFrame plus a metadata object, e.g., `df, metadata = waterdata.get_daily(monitoring_location_id='USGS-01646500', parameter_code='00060', time='2024-10-01/2025-09-30')`.
  - *evidence:* Demonstrated directly in the README's usage-example code blocks for waterdata, ngwmn, wqp, nldi, and wateruse modules. (README, usage examples)
  - *quote:* "df, metadata = waterdata.get_daily(monitoring_location_id='USGS-01646500', parameter_code='00060', time='2024-10-01/2025-09-30')"

## Data / numbers
- 252 GitHub stars (as of fetch, 2026-07-01)
- 59 forks
- 11 watchers
- 7 open issues
- 8 open pull requests
- 23 total releases; latest release v1.2.0 dated Jun 24, 2026
- 421 total commits
- 100% Python language composition
- NSF award number 1931297 (funding acknowledgment; not a monetary figure)
- DOI 10.5066/P94I5TX3 (USGS software-release identifier, corroborated via independent WebSearch)
- Example USGS parameter codes shown in usage examples: '00060' (discharge, daily-data example) and '00065' (gage height, continuous-data example) — illustrative, not thresholds

## Methods
Not a scientific model but a data-access software library: a modular Python API (submodules `waterdata`, `ngwmn`, `nwis` [deprecated], `wqp`, `nldi`, `wateruse`) that wraps REST calls to USGS's modern Water Data API, the National Ground-Water Monitoring Network, the multi-agency Water Quality Portal, the Network Linked Data Index, and a HUC12-gridded water-use model. Installable via `pip install dataretrieval`, `conda install -c conda-forge dataretrieval`, or directly from GitHub. Each function call returns a `(DataFrame, metadata)` tuple. The README states it is intended to be used with an API key registered at api.waterdata.usgs.gov for higher rate limits, and recommends chunking continuous/high-frequency data requests into smaller time windows, implying the service is prone to timeouts on large unchunked continuous-data pulls. The legacy `nwis` interface still functions but is deprecated in favor of `waterdata`.

## Stated limitations
The source itself states: (1) the software is "preliminary or provisional" and "has not received final approval" by USGS, with USGS/the U.S. Government disclaiming liability for its use; (2) the legacy `dataretrieval.nwis` module is deprecated in favor of the newer `waterdata` module, implying reduced future support; (3) continuous/high-frequency data requests over long time spans risk timeouts unless deliberately chunked into smaller windows, per the README's explicit advisory; (4) unauthenticated use is rate-limited, with an API key "strongly encouraged" to avoid throttling. Neither fetch pass surfaced a specific stated license type (only that a LICENSE.md file exists in the repo), so no license type is asserted here.

## Tensions with other findings
This is an infrastructure/tooling source, not a scientific or HAB-specific finding, so it does not itself make claims about cyanobacteria dynamics, drivers, or prediction — any HAB-relevant conclusions must come from data actually pulled through this tool (e.g., WQP chlorophyll-a, nutrients, temperature; NWIS streamflow/gage data), not from the repository's own text. One practical tension for reproducibility: the package's own legacy `nwis` module is deprecated in favor of a new `waterdata` API, so code samples, tutorials, or prior analyses elsewhere that reference `dataretrieval.nwis.get_dv()`-style calls may not match the current recommended interface — a versioning/reproducibility consideration if this package is checked in as the acquisition layer for the HAB PoC's in-situ data.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All 10 claims are directly supported by the source text. Verification approach: (1) Exact-string matching for major claims (claims 1–7, 10); (2) Cross-reference of repository statistics against Fetch 1 values (claim 8); (3) Validation of functional module descriptions against detailed module listings (claims 2–3); (4) Confirmation of advisory language via direct quote matching (claim 4); (5) Corroboration of R-package relationship via secondary WebSearch results (claim 9). No numbers outside source text, no material caveats omitted, and no unsupported assertions detected."

## Provenance
- Canonical URL: https://github.com/DOI-USGS/dataretrieval-python
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the single primary GitHub URL twice with two different extraction prompts as required for a High-relevance source: (1) a general comprehensive-extraction prompt covering description, functions, install, citation, examples, limitations, stats; (2) a prompt focused on README content, data services/APIs, disclaimers, license, and repo stats. Both fetches returned mutually consistent content (identical citation text, DOI, disclaimer wording, and repo stats: 252 stars / 59 forks / 11 watchers / 7 open issues / 23 releases), so they were reconciled by union rather than needing to adjudicate a conflict. Ran one additional independent WebSearch to cross-check the suggested-citation DOI (10.5066/P94I5TX3) and authorship, since these are precise identifiers a fetch-summarizing model could in principle mis-render; the search independently surfaced the same DOI, authors, and package description across PyPI, the USGS Water Mission Area tools catalog, and the raw GitHub README, corroborating the fetched text. No wrong-page or blocked-content issue occurred; the given URL was the correct repository page and both fetches returned substantive, overlapping content, so full_text_access is rated 'full' rather than 'landing-only.' Caveats on my own extraction: (a) the specific OSS license type (e.g., exact license name) was not clearly surfaced by either fetch — only that a LICENSE.md file exists — so it is deliberately left unstated rather than guessed; (b) GitHub repository social/activity statistics (stars, forks, watchers, issues, releases, commits) are dynamic and reflect the state at fetch time (2026-07-01 per system date), not a fixed characteristic of the software, and are reported here only as contextual metadata, not as a scientific finding. This source is a software tool, not a study; its 'findings' are its capabilities, module structure, and operational caveats rather than empirical HAB results, and I did not draw on any prior/training knowledge of this repository beyond what the two fetches and the corroborating search returned.
