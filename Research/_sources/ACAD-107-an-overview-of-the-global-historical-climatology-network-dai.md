---
key: ACAD-107
title: An Overview of the Global Historical Climatology Network-Daily Database
authors_or_org: Menne, M. J.; Durre, I.; Vose, R. S.; Gleason, B. E.; Houston, T. G. (all NOAA National Climatic Data Center, Asheville, NC)
year: 2012
url: https://doi.org/10.1175/JTECH-D-11-00103.1 (redirects to http://journals.ametsoc.org/doi/10.1175/JTECH-D-11-00103.1)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (data-infrastructure / dataset-overview paper), Journal of Atmospheric and Oceanic Technology, vol. 29, pp. 897-910, doi:10.1175/JTECH-D-11-00103.1
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# An Overview of the Global Historical Climatology Network-Daily Database

> Note: provisional URL was resolved to a primary source. Original: https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml

**What it is.** The peer-reviewed reference/methods paper (Menne et al. 2012, J. Atmos. Oceanic Technol.) that formally describes GHCN-Daily, NOAA/NCDC's global compilation of daily in-situ land-station weather observations (temperature, precipitation, snow) assembled from dozens of source networks, quality-screened, and distributed as the official U.S. daily climate data archive. It is an infrastructure/data-description paper, not a study of harmful algal blooms.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** GHCN-Daily was purpose-built to meet the need for daily-resolution climate data over global land areas, to support applications such as analyzing heavy-rainfall frequency and heat-wave duration.
  - *evidence:* Stated as the paper's own rationale in the opening sentence(s) of the abstract. (Abstract)
  - *quote:* "designed to fulfill the need for daily climate data over global land areas"
- **[✓ verified]** As of the 2012 publication, GHCN-Daily contained records from over 80,000 stations in 180 countries and territories, and its processing system produced the official archive of U.S. daily station data.
  - *evidence:* Directly stated scale/coverage figures in the abstract; describes the dataset's status at time of writing (2012), not necessarily current size. (Abstract)
  - *quote:* "over 80,000 stations in 180 countries and territories"
- **[✓ verified]** Commonly reported variables are maximum/minimum temperature, total daily precipitation, snowfall, and snow depth, but roughly two-thirds of all stations report precipitation only (i.e., no temperature).
  - *evidence:* Stated directly in the abstract; implies large heterogeneity in per-station variable completeness across the network. (Abstract)
  - *quote:* "about two-thirds of the stations report precipitation only"
- **[✓ verified]** Quality-assurance checks are applied to the entire dataset, but GHCN-Daily is explicitly NOT homogenized -- station-level artifacts from different reporting eras (i.e., changes in systematic bias over time) are left uncorrected.
  - *evidence:* An explicit, self-stated limitation in the abstract; important caveat for anyone using GHCN-Daily series for trend/change analysis rather than raw daily values. (Abstract)
  - *quote:* "not homogenized to account for artifacts associated with the various eras in reporting practice at any particular station"
- **[✓ verified]** GHCN-Daily is compiled from 20+ constituent source datasets and is fully reconstructed on roughly a weekly cadence so that it stays synchronized with its growing list of sources; each update/reprocessing is assigned a unique version number, the latest version is freely published, and every version is archived in perpetuity at NOAA's National Climatic Data Center.
  - *evidence:* Describes update cadence, source-count, versioning, and archival/reproducibility policy -- recovered consistently (near-identical wording) across multiple independent search-engine snippet retrievals of the abstract, though not confirmed via a single quotation-marked excerpt the way the other claims were, so treat this one claim as high-confidence-but-not-fully-verified verbatim. (Abstract (recovered via aggregated search snippets rather than a directly quoted excerpt))
  - *quote:* "reconstructed, usually once per week, from its 20+ data source components"

## Data / numbers
- >80,000 stations (dataset scale as stated in the 2012 abstract; no uncertainty/error bar given -- it is a descriptive inventory count, not a modeled estimate)
- 180 countries and territories (spatial coverage as of 2012)
- ~two-thirds of stations report precipitation only (i.e., roughly one-third report temperature and/or other elements; no confidence interval stated)
- 20+ constituent source datasets feeding the compiled product (2012); dataset fully reconstructed approximately once per week
- No period-of-record start year, exact per-element station counts, or QC-flag pass/fail statistics could be confirmed from the text actually retrieved (see fetch_notes / stated_limitations)

## Methods
Per the recovered abstract text: GHCN-Daily merges station records from 20+ (as of 2012) independent source datasets/networks into one product, which is fully rebuilt roughly weekly so it stays synchronized with its growing list of constituent sources; each incremental and each fully-reprocessed version receives a unique version number, with the latest version freely published and every version archived in perpetuity at NOAA/NCDC. Dataset-wide quality-assurance checks are applied, but no homogenization is performed. The paper's own Methods/Data-Integration/QC sections, tables, and figures (e.g., the specific list of source networks, exact QC test names, and flag-level statistics) could NOT be retrieved despite repeated attempts (see fetch_notes) and are therefore NOT claimed here. For background context only -- and explicitly NOT verified as text of this article -- NOAA's companion, non-journal GHCN-Daily documentation (the dataset's public README and its NCEI/ISO metadata record for the same product, fetched separately) describes: (a) a three-step data-integration process of "screening the source data for stations whose identity is unknown or questionable," "classifying each station...as one that is already represented...or as a new site," and merging/"mingling the data from the different sources"; and (b) a per-record flag scheme (MFLAG/QFLAG/SFLAG) with named checks such as duplicate, gap, internal-consistency, streak/frequent-value, climatological-outlier, spatial-consistency, and temporal-consistency checks, plus source-network codes for contributors such as U.S. Cooperative Summary of the Day, ASOS, CoCoRaHS, SNOTEL, RAWS, and the European Climate Assessment & Dataset, among ~20-30 others. These NOAA-documentation details are included only as background color since the journal article's own text was inaccessible, and are not to be treated as quotes from Menne et al. (2012) itself.

## Stated limitations
Self-stated in the abstract: the dataset is not homogenized, so station-level artifacts tied to different eras of reporting practice (instrument changes, station moves, etc. -- i.e., shifts in systematic bias) remain in the data and are left for users to address "in the context of specific applications." Separately, and as an honest disclosure of THIS fetch's own limitations rather than a claim by the paper: the article's Introduction, full Methods, Results, discussion of specific QC tests, source-dataset table, and Conclusions could not be retrieved (see fetch_notes), so this dossier entry is built only from the abstract; period-of-record start date, the complete list of named source networks, and quantitative QC-flag statistics are therefore not available here and should not be assumed. The scale figures given (>80,000 stations, 180 countries, 20+ sources) are also explicitly a 2012 snapshot -- NOAA's own current dataset-description pages (a separate, non-journal source consulted only for cross-reference) describe a substantially larger current network (on the order of 90,000-100,000+ stations and roughly 30 source datasets), so the 2012 paper's figures should not be quoted as current coverage without checking a more recent source.

## Tensions with other findings
This is a data-infrastructure paper with no findings about algal blooms, nutrients, or water quality; its relevance to the HAB PoC is solely as a candidate authoritative source of in-situ daily temperature/precipitation covariates to pair with a satellite HAB signal (consistent with the CLAUDE.md-sanctioned NOAA/NCEI weather-data category), not as evidence about bloom dynamics itself -- any driver/covariate relationship built from GHCN-Daily data to a HAB outcome would be a separate correlational analysis and must not be read as validated by this paper. The paper's own explicit "not homogenized" caveat is itself a tension for that downstream use: station-level discontinuities in temperature/precipitation series (unrelated to real climate or bloom-relevant signal) could inject noise or spurious trend into any derived weather covariate, so any HAB analysis using GHCN-Daily series should treat raw trends cautiously rather than assuming homogeneity. No direct contradiction with other HAB-specific sources is evident from the abstract alone.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All five claims are directly supported by the article passages in the source text. No hallucinated figures; no material caveats from the source have been omitted from the claims. The supplementary NOAA metadata mentions 'approximately 30 different data sources' versus the article's '20+', but the claim correctly cites the article's figure. Source text is well-formed and claims are traceable to specific passages."

## Provenance
- Canonical URL: https://doi.org/10.1175/JTECH-D-11-00103.1 (redirects to http://journals.ametsoc.org/doi/10.1175/JTECH-D-11-00103.1)
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: WebFetch was attempted directly on the primary URL (journals.ametsoc.org/view/...), the AMS "/abstract/..." URL variant, the AMS "/downloadpdf/..." URL, the DOI (which redirected to journals.ametsoc.org/doi/...), and the ResearchGate and Semantic Scholar pages for this paper -- every one of these returned HTTP 403 Forbidden or an empty page. Two independent NOAA/NCEI-hosted PDF mirrors of the same 4.4MB/14-page article (ncei.noaa.gov/pub/data/ushcn/papers/menne-etal2012.pdf and .../pub/data/ghcn/daily/papers/menne-etal2012.pdf) were fetched twice each; in every case the PDF's FlateDecode content streams could not be decoded into readable text (only PDF structural metadata -- fonts, page count, object count -- was recoverable), indicating a genuine, reproducible text-extraction failure for this specific (older, custom-font-encoded) AMS-typeset PDF rather than a transient error. The Semantic Scholar API confirmed the publisher has deliberately elided the abstract field from its record. Unpaywall confirmed the article is "bronze" OA with its sole open-access location being the same blocked ametsoc.org PDF URL (no independent repository copy exists). Given these blocks, I used targeted WebSearch queries (including a Google Scholar scholar_lookup citation search) to recover the article's own abstract in verbatim/near-verbatim fragments, which together read as a complete, internally consistent abstract paragraph; this is reported here as full_text_access="abstract" and fetch_status="partial" since no part of the article's Introduction, Methods, Results, tables, or Conclusions could be retrieved. Background-only supplementary detail was drawn from NOAA's own (non-journal) GHCN-Daily README and ISO metadata pages for the same dataset and is clearly flagged wherever used so it is not mistaken for the journal article's text.
