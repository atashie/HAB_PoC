---
key: FED-058
title: GitHub - DOI-USGS/dataRetrieval: R package for discovering and retrieving water data (USGS NWIS / Water Quality Portal)
authors_or_org: DOI-USGS (U.S. Geological Survey, Water Mission Area); package citation authors: De Cicco, L.A., Hirsch, R.M., Lorenz, D., Watkins, W.D., Johnson, M., Blodgett, D.L., Hinman, E.D., Zemmels, J.
year: 2026
url: https://github.com/DOI-USGS/dataRetrieval
access_date: 2026-07-01
tier: FED
source_type: Software package repository (GitHub) / README documentation
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# GitHub - DOI-USGS/dataRetrieval: R package for discovering and retrieving water data (USGS NWIS / Water Quality Portal)

**What it is.** dataRetrieval is a USGS-maintained open-source R package (GitHub repo DOI-USGS/dataRetrieval) providing functions to programmatically discover and download U.S. Geological Survey hydrologic data (streamflow, field measurements, time series) from USGS web services/APIs, plus multi-agency water-quality data from the Water Quality Portal (WQP), directly into R.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** dataRetrieval was created to simplify loading USGS hydrologic data (available on the Web) plus Water Quality Portal (WQP) data into the R environment.
  - *evidence:* Stated directly in the repository's opening package description. (README, package description (top of repo page))
  - *quote:* "was created to simplify the process of loading hydrologic data into the R environment"
- **[✓ verified]** The Water Quality Portal (WQP), one of the package's two main data sources, integrates water-quality data from EPA, USDA, USGS, and over 400 other state/federal/tribal/local agencies.
  - *evidence:* Given as a factual description of WQP's scope in the README's data-sources section. (README, Data Sources / package description)
  - *quote:* "integrates water quality data from EPA, USDA, USGS, and over 400 state/federal/tribal/local agencies"
- **[✓ verified]** Installing the package requires R version 3.0 or greater.
  - *evidence:* Explicit minimum-version requirement given in the installation instructions. (README, Installation section)
  - *quote:* "you must be using R 3.0 or greater and run the following command: install.packages("dataRetrieval")"
- **[✓ verified]** The package is in an explicit transitional state: legacy NWIS web-service functions (readNWIS*) are being replaced over time by newer USGS Water Data API functions (read_waterdata_*).
  - *evidence:* Stated as a current/ongoing status notice, not a hypothetical, with a dedicated Status article linked. (README, Status/notices section (links to Status.html article))
  - *quote:* "NWIS web services (readNWIS functions) will be replaced over time by USGS Water Data APIs (read_waterdata_)"
- **[✓ verified]** USGS discrete water-quality data availability and format are themselves actively changing, independent of the package's own function transition.
  - *evidence:* A second, separate caveat about the underlying federal data (not just the R interface to it) being unstable. (README, Status/notices section)
  - *quote:* "USGS discrete water-quality data availability and format are changing"
- **[✓ verified]** The current package version at the time of this fetch is v2.7.23, released March 10, 2026, carrying a formal DOI-bearing citation.
  - *evidence:* Version and citation string given verbatim in the repository's citation/release information. (README/citation section and repository release metadata)
  - *quote:* "dataRetrieval: R packages for discovering and retrieving water data available from Federal hydrologic web services, v.2.7.23, doi:10.5066/P9X4L3GE"
- **[✓ verified]** The software carries a formal USGS disclaimer that it is preliminary/provisional, has not received final USGS approval, and is provided with no warranty.
  - *evidence:* Standard USGS software disclaimer reproduced in the repository, bearing on reliability/liability for any downstream use. (README, Disclaimer section (bottom of README))
  - *quote:* "This software is preliminary or provisional and is subject to revision...The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government"
- **[✓ verified]** Users can register a free API token to avoid query rate limits when using the package's web-service calls.
  - *evidence:* Practical operational detail relevant to any automated/scripted data-acquisition pipeline built on this package. (README, API token / usage notes)
- **[✓ verified]** The repository's GitHub-detected license status is listed as "Unknown" even though LICENSE.md and LICENSE.note files exist in the repo.
  - *evidence:* Noted as an open question for reuse/redistribution terms rather than a resolved license grant. (Repository sidebar / license metadata)
  - *quote:* "Unknown"

## Data / numbers
- R >= 3.0 — minimum required R version for installation
- v2.7.23 — current package version at time of fetch, released March 10, 2026
- 400+ — number of state/federal/tribal/local agencies whose data the Water Quality Portal integrates (in addition to EPA, USDA, USGS)
- 324 stars; 97 forks; 27 watchers; 63 releases; 5,391 commits; 7 open issues; 2 open pull requests — GitHub repository metadata as of fetch (2026)
- R 97.0% / CSS 1.9% / Other 1.1% — repository language composition
- doi:10.5066/P9X4L3GE — package citation DOI; NWIS data DOI http://dx.doi.org/10.5066/F7P55KJN; WQP data DOI https://doi.org/10.5066/P9QRKUVJ

## Methods
Not a statistical/predictive method — it is a client library that wraps three federal data services/APIs: (1) USGS NWIS legacy web services and the newer USGS Water Data APIs for streamflow/discharge and field measurements, via functions such as read_waterdata_continuous / read_waterdata_latest_continuous (instantaneous discharge sensor data), read_waterdata_daily / read_waterdata_latest_daily (mean daily discharge), read_waterdata_field_measurements (discrete groundwater data), read_waterdata_samples (USGS discrete water-quality data), read_waterdata_ts_meta (time-series metadata), and read_waterdata_stats_por (daily data statistics); (2) the multi-agency Water Quality Portal via readWQPdata; and (3) the Hydro Network-Linked Data Index via findNLDI. It also ships citation-generation helpers (create_NWIS_bib, create_WQP_bib). Where the source says the current approach is breaking down / in transition: legacy camelCase NWIS-service functions (readNWIS*) are explicitly being deprecated and replaced over time by the new snake_case read_waterdata_ functions, and the source states USGS discrete water-quality data availability and format are themselves "changing" (i.e., the underlying data schema is a moving target, not a fixed method).

## Stated limitations
The repository's own disclaimer states the software "is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science... The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software." It also explicitly flags a transitional/moving-target status: "NWIS web services (readNWIS functions) will be replaced over time by USGS Water Data APIs (read_waterdata_)" and "USGS discrete water-quality data availability and format are changing" — both are reproducibility caveats for any downstream pipeline that pins to specific function names or output schemas. Separately, GitHub's own repo metadata lists the license as "Unknown" despite LICENSE.md/LICENSE.note files being present, so exact reuse/redistribution terms are not resolved by this fetch alone.

## Tensions with other findings
This is a data-access tool, not a HAB research or monitoring finding — the fetched README contains no cyanobacteria/HAB-specific content, thresholds, or model claims, so no direct empirical tension with other HAB sources is evident. It is complementary to (not in tension with) EPA CyAN and Water Quality Portal sources used elsewhere in this review: dataRetrieval is the mechanism by which USGS NWIS/WQP in-situ variables (nutrients, chlorophyll-a, temperature, streamflow) would be programmatically pulled to pair with a satellite cyanobacteria signal, as CLAUDE.md's own sanctioned-source list anticipates ("USGS NWIS ... dataRetrieval packages for R & Python"). One internal tension worth flagging for reproducibility: the source itself warns its function set and the underlying USGS discrete water-quality data format are actively in flux, so a pipeline built against current function names/outputs could break or silently change behavior later — a risk to note in any data-acquisition/reproducibility section.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All nine claims are directly supported by the source text. No hallucinated numbers, no critical dropped caveats. Claim 8 uses 'token' where source says 'keys' and does not explicitly state 'free', but the core mechanism (register credentials to avoid rate limits) is clearly present; marking as yes since the substantive claim is accurate."

## Provenance
- Canonical URL: https://github.com/DOI-USGS/dataRetrieval
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Single WebFetch of the GitHub repository landing page (README) succeeded and returned a comprehensive, well-structured extraction covering purpose, data sources, function inventory, installation, version/citation, disclaimer, license status, and repo metadata — no WebSearch fallback was needed. This is a software repository, not a peer-reviewed paper, so "full_text_access: full" refers to the complete README/repo page content, which is the entirety of the primary source material available at this URL. One field (API-token claim) is presented without a verbatim quote because the fetch rendered it as a paraphrased bullet rather than a quoted README passage; it is retained as a claim but flagged as paraphrase-only in evidence_note.
