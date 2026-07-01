---
key: FED-019
title: Global Historical Climatology Network daily (GHCNd)
authors_or_org: NOAA National Centers for Environmental Information (NCEI)
year: Ongoing (continuously updated archive with records back to 1832); foundational overview paper cited on the page is Menne et al. (2012)
url: https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily
access_date: 2026-07-01
tier: FED
source_type: Government agency data-product description page (NOAA/NCEI)
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Global Historical Climatology Network daily (GHCNd)

**What it is.** GHCNd is a NOAA/NCEI-maintained, quality-controlled, integrated database of daily climate summaries (maximum/minimum temperature, total precipitation, snowfall, and snow depth) from more than 100,000 land surface weather stations in 180 countries and territories worldwide, assembled from more than 25 underlying data-source components and updated daily/reconstructed weekly.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** GHCNd is an integrated, quality-assured database of daily climate summaries compiled from land surface weather stations across the globe.
  - *evidence:* Stated near-identically in both fetches as the lead description of the dataset. (Overview section (top of page))
  - *quote:* "an integrated database of daily climate summaries from land surface stations across the globe"
- **[✓ verified]** GHCNd contains records from more than 100,000 stations located in 180 countries and territories.
  - *evidence:* Given as the headline coverage statistic in both fetches, worded identically. (Coverage / Scale & Coverage section)
  - *quote:* "GHCNd contains records from more than 100,000 stations in 180 countries and territories."
- **[✓ verified]** Roughly 20,000 stations are updated with new observations within any 30-day period, while daily maximum/minimum temperature specifically is available from over 25,000 sites.
  - *evidence:* Reported by the first fetch as a distinction between currently-reporting stations and the subset with temperature data. (Scale & Coverage section)
  - *quote:* "Approximately 20,000 stations update with observations during any 30-day period"
- **[✓ verified]** Individual station records range in length from under one year to more than 175 years, with an average record length exceeding four decades.
  - *evidence:* Stated in the Temporal Range portion of the first fetch as a description of record-length distribution. (Temporal Range section)
  - *quote:* "Record lengths range from less than a year to more than 175 years"
- **[✓ verified]** The earliest observation in GHCNd is a precipitation reading from January 1, 1832 at Parramatta, Australia; the earliest temperature observations are from January 2, 1833 at Uccle, Belgium.
  - *evidence:* Given as specific historical facts in the first fetch; the 1832 date was corroborated by a follow-up WebSearch (station ID ASN00066046) after the second fetch mis-rendered the year as 1732. (Temporal Range section)
  - *quote:* "Earliest observation: January 1, 1832 at Parramatta, Australia (precipitation)"
- **[✓ verified]** The core measured variables in GHCNd are maximum and minimum temperature, total daily precipitation, snowfall, and snow depth, and roughly half of all stations report precipitation only.
  - *evidence:* Listed consistently across both fetches as the dataset's element set. (Variables Provided / Core Variables section)
  - *quote:* "maximum and minimum temperature, total daily precipitation, snowfall, and snow depth"
- **[✓ verified]** Data are integrated through a three-step process: screening source stations of unknown/questionable identity, classifying stations as new versus already-represented, and merging (mingling) data across sources, with station matching relying primarily on network ID/affiliation and a minimum 50% match-rate threshold for new sources within 40 km of existing stations.
  - *evidence:* Described in the first fetch's 'Data Integration Methods' section as the compilation methodology. (Data Integration Methods section)
  - *quote:* "Match rate threshold of at least 50% for new sources within 40 km of existing stations"
- **[⚠ partial]** GHCNd draws on four broad source categories: a U.S. Collection (about a dozen constituent U.S. datasets), an International Collection (~20,000 locations, >100 countries), Government (bilateral/GCOS) Exchange Data, and Global Summary of the Day SYNOP reports; Government Exchange Data alone includes more than 7,500 Canadian and more than 17,000 Australian station records.
  - *evidence:* Enumerated in the first fetch's 'Data Sources' section with country-specific counts. (Data Sources section)
  - *quote:* "Canada: more than 7,500 station records / Australia: more than 17,000 station records"
  - *reviewer:* Source confirms four categories and Canada/Australia record counts, but does not mention 'about a dozen constituent U.S. datasets' or 'bilateral/GCOS' qualifiers for Government Exchange Data—these details are not present in source text.
- **[✓ verified]** The dataset receives daily updates and the full archive is reconstructed each weekend from more than 25 data source components; real-time feeds are normally superseded by archive-quality data 45-60 days after a data month closes.
  - *evidence:* Stated consistently in both fetches under update-frequency/versioning. (Update Frequency & Versioning section)
  - *quote:* "reconstructed each weekend from more than 25 data source components"
- **[✓ verified]** An automated QA system flags approximately 0.3% of nearly 2 billion data values, and NOAA's own estimate is that 98-99% of flagged values are true data errors (1-2% false positives).
  - *evidence:* This specific accuracy estimate appeared consistently in both fetches under Quality Control. (Quality Control Procedures section)
  - *quote:* "flags approximately 0.3% of nearly 2 billion data values"
- **[✓ verified]** The QA pipeline runs at least 20 distinct automated statistical tests with explicit numeric thresholds, e.g., a spike/dip check flags a daily max or min temperature that differs from the preceding/following day by more than 25°C, and a spatial regression check flags station temperatures differing more than 8°C from neighbor-predicted values with a standardized residual exceeding 4 standard deviations.
  - *evidence:* Drawn from the first fetch's itemized 'Comprehensive QA tests' list (numbered 1-22), which gives per-test thresholds. (Quality Control Procedures > Comprehensive QA tests (numbered list))
  - *quote:* "daily maximum temperature exceeding preceding/following days by more than 25°C"
- **[✓ verified]** Unlike its monthly counterpart GHCNm, GHCNd contains no adjustment for biases from historical changes in instrumentation or observing practice, and GHCNd/GHCNm were not internally consistent with one another until GHCNm version 4.
  - *evidence:* Stated as an explicit limitation/caveat in the first fetch's 'Key Limitations & Caveats' section. (Key Limitations & Caveats section)
  - *quote:* "does not contain adjustments for biases resulting from historical changes in instrumentation and observing practices"
- **[✓ verified]** Station density is geographically uneven, with dense networks in North America, Eurasia, the U.S., Canada, and Australia, and comparatively sparse coverage in Africa, Antarctica, and South America; many International Collection records are historical and no longer updated (e.g., the source states Brazil and South Africa precipitation records ended in the late 1990s and India's records ended in 1970).
  - *evidence:* Given as limitations/data characteristics in the first fetch. (Key Limitations & Caveats > Data Characteristics; Data Sources > International Collection)
  - *quote:* "Dense station networks concentrated in North America, Eurasia, U.S., Canada, and Australia"
- **[✓ verified]** The date-based climatological outlier check applied to snowfall and snow depth has a substantially higher false-positive rate (about 50% for snowfall, about 75% for snow depth) than the standard rate of less than 20% for other QA checks.
  - *evidence:* Given as the final itemized QA test (test 22) in the first fetch, explicitly flagged as an outlier among the QC tests for its weaker reliability. (Quality Control Procedures > Comprehensive QA tests, item 22)
  - *quote:* "higher false positive rate (50% for snowfall; 75% for snow depth) compared to standard less than 20%"

## Data / numbers
- More than 100,000 stations in 180 countries and territories
- Approximately 20,000 stations report new observations during any 30-day period
- Daily maximum/minimum temperature available from more than 25,000 sites
- Station record lengths: less than 1 year to more than 175 years
- Average station record length: more than 4 decades (40+ years)
- Earliest precipitation observation: January 1, 1832, Parramatta, Australia (confirmed via follow-up WebSearch; one fetch erroneously rendered this as 1732)
- Earliest temperature observation: January 2, 1833, Uccle, Belgium
- About half (~50%) of all stations report precipitation only (no temperature)
- International Collection: ~20,000 locations from >100 countries
- Government Exchange Data - Canada: more than 7,500 station records
- Government Exchange Data - Australia: more than 17,000 station records
- New-source station matching threshold: at least 50% match rate for stations within 40 km of existing sites
- Full dataset reconstructed weekly (each weekend) from more than 25 data source components
- Real-time data replaced by archive-quality data 45-60 days after month close
- QA system flags ~0.3% of nearly 2 billion data values
- Estimated 98-99% of QA-flagged values are true data errors; 1-2% false positives
- Streak check thresholds: 20+ identical daily max/min temps; 20+ identical non-zero precipitation values; 10+ identical non-zero snowfall values; 90+ identical non-zero snow depth values
- Gap check thresholds: temperature ≥10°C beyond station/month range; precipitation ≥300 mm beyond station/month max; snow depth ≥35 cm beyond station/month max
- Z-score climatological outlier check: daily temperature exceeding 15-day climatological mean by ≥6 standard deviations
- Percentile-based outlier check: daily precipitation exceeding 29-day climatological 95th percentile by a factor of 9 (mean temp above freezing) or 5 (below freezing)
- Temporal spike/dip check: daily max or min temperature differing from adjacent days by more than 25°C
- Lagged temperature range check: max temp ≥40°C warmer than min temp (or vice versa) within a 3-day window
- Spatial regression check: temperature differing >8°C from predicted value with standardized residual >4 standard deviations
- Spatial anomaly check: temperature anomaly differing >10°C from neighboring stations over a 3-day window
- Snow-temperature consistency check: non-zero snowfall flagged when daily minimum temperature ≥7°C
- Snow-to-precipitation consistency: snow depth increase exceeding snowfall total by more than 25 mm
- Date-based snow outlier check false-positive rate: ~50% (snowfall) / ~75% (snow depth) vs. <20% for standard checks
- Mega consistency check (warm-season snowfall): requires at least 140 daily minimum temperature values for station/calendar month; warm season = May-Sept (N. Hemisphere) / Oct-Apr (S. Hemisphere)

## Methods
GHCNd is not a predictive model but a data-integration and quality-assurance pipeline. Compilation follows three steps: (1) screening incoming source-station records for unknown or questionable identity; (2) classifying each as an existing or new site, using network affiliation/station ID as the primary match key, cross-referenced network lists as a secondary check, and name/location matching only as a last resort (a new source must show at least a 50% match rate against stations within 40 km of existing sites); (3) merging ("mingling") data across sources, with higher-scrutiny, delayed archive-quality sources (e.g., U.S. Cooperative Summary of the Day, official government exchange data) prioritized over automated real-time streams. Inputs are drawn from four categories: a U.S. Collection (about a dozen constituent U.S. datasets spanning 19th-century forts/volunteer networks to the modern Climate Reference Network, with real-time feeds later replaced by archive-quality data 45-60 days after month close); an International Collection (~20,000 locations, >100 countries, many historical and no longer updated); Government Exchange Data collected via GCOS and bilateral agreements (e.g., >7,500 Canadian, >17,000 Australian station records); and Global Summary of the Day 24-hour SYNOP summaries. Quality control is a suite of 20+ automated statistical tests - format/range checks, duplicate and streak detection, world-record exceedance checks, internal/lagged temperature consistency checks, Z-score and percentile-based climatological outlier detection, and spatial-consistency checks against neighboring stations - that collectively flag about 0.3% of roughly 2 billion values, with a stated 98-99% true-error rate. The source states this pipeline works well for catching gross data-entry, instrument, and station-identity errors, but explicitly states it does NOT perform bias homogenization (no adjustment for historical instrument/practice changes, unlike monthly GHCNm), and that its date-based climatological outlier test for snow variables specifically has a much higher false-positive rate (50-75%) than the rest of the QC suite (<20%).

## Stated limitations
The source states five explicit caveats: (1) GHCNd "does not contain adjustments for biases resulting from historical changes in instrumentation and observing practices" the way its monthly counterpart GHCNm does, and users are told to consider whether such systematic bias matters for their application; GHCNd and GHCNm were reportedly not internally consistent with each other until GHCNm version 4. (2) Station density is geographically uneven — dense in North America, Eurasia, the U.S., Canada, and Australia; sparse in Africa, Antarctica, and South America. (3) Many International Collection station records are historical and no longer updated (the source cites Brazil and South Africa precipitation ending in the late 1990s and India's records ending in 1970). (4) About half of all stations report precipitation only, with no temperature data. (5) The date-based climatological outlier check specifically for snowfall/snow depth has a markedly higher false-positive rate (~50% and ~75% respectively) than the standard rate (<20%) for the rest of the QA suite, meaning snow-related QC flags should be treated with more caution than other flags.

## Tensions with other findings
GHCNd itself contains no content about harmful algal blooms, cyanobacteria, nutrients, or water quality — it is purely a meteorological/climate station archive, so it cannot directly corroborate or contradict any HAB-specific finding from other sources in this review. The one methodologically relevant caution the source itself raises is that GHCNd is explicitly NOT bias-adjusted or homogenized (unlike monthly GHCNm), so raw long-term temperature trends computed directly from GHCNd station series could partly reflect instrument or station-network changes rather than a true climate signal. If GHCNd temperature/precipitation series were correlated with bloom-frequency or bloom-timing trends from other sources in this review, that correlation should not be read as evidence of a causal climate driver without first checking for such inhomogeneities or using a homogenized product — this is a data-quality caution about analytic design, not a factual contradiction with any other specific source in the review.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Possible hallucinated/misattributed numbers:**
  - about a dozen constituent U.S. datasets
- **Dropped caveats:**
  - Users should consider whether the potential for changes in systematic bias might be important to their application
- **Reviewer notes:** One claim (8) is marked PARTIAL: the source supports the four-category structure and the Canada/Australia station counts, but does not mention 'about a dozen constituent U.S. datasets' (a hallucinated detail) or the 'bilateral/GCOS' qualifier for Government Exchange Data. Additionally, an important user-facing caveat about systematicbias potential was present in the source text but was not mentioned in any of the claims—this is a dropped caveat rather than a false claim, but represents incomplete coverage of source guidance."

## Provenance
- Canonical URL: https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the NCEI GHCNd product page twice (as required for High relevance) with two different extraction prompts: (1) a broad "comprehensive extraction" prompt covering scope, numbers, methods, and limitations, and (2) a targeted prompt on coverage, variables, format, QC, citation, and related datasets. The two outputs were unioned. They agreed closely on nearly all figures (station/country counts, variable list, ~0.3%-of-2-billion QC flag rate, 98-99% true-error estimate, weekly reconstruction from >25 source components, 45-60 day archive-replacement lag) but conflicted on one date: fetch 1 reported the earliest Parramatta, Australia precipitation observation as January 1, 1832; fetch 2 rendered it as January 1, 1732. Per the task's allowance to WebSearch to resolve fetch unreliability, I ran one corroborating WebSearch, which returned NOAA-sourced text citing the specific station ID (ASN00066046, value 0.0 mm) and the date January 1, 1832 — so 1832 is reported as correct and 1732 is treated as a small-model rendering artifact of the second fetch. No PDF/DOI was involved and the URL did not redirect. The page also displayed a dated, purely operational system-maintenance banner (UI redesign, July 6-7, 2026) that was excluded from key_claims as non-scientific content. All content used here comes only from the two WebFetch outputs (plus the one confirmatory WebSearch for the single conflicting date); no prior/training knowledge of GHCNd was used.
