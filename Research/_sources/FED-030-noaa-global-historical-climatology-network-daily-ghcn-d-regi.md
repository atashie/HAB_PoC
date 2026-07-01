---
key: FED-030
title: NOAA Global Historical Climatology Network Daily (GHCN-D) — Registry of Open Data on AWS
authors_or_org: NOAA (National Oceanic and Atmospheric Administration) / NOAA Open Data Dissemination (NODD) Program (data steward); listing hosted on the AWS Open Data Sponsorship Program's "Registry of Open Data on AWS"
year: 
url: https://registry.opendata.aws/noaa-ghcn/
access_date: 2026-07-01
tier: FED
source_type: Public dataset registry / catalog listing (web page), not a journal article
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# NOAA Global Historical Climatology Network Daily (GHCN-D) — Registry of Open Data on AWS

**What it is.** An AWS "Registry of Open Data" catalog entry describing NOAA's Global Historical Climatology Network Daily (GHCN-D) dataset — daily land-station weather/climate observations (temperature, precipitation, snow) distributed as public CSV files in an Amazon S3 bucket under NOAA's Open Data Dissemination (NODD) program. It is a data-access/metadata listing, not a scientific study.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** GHCN-D contains daily observations over global land areas from land-based station measurements, and about two-thirds of those stations are precipitation-only stations.
  - *evidence:* Stated as the dataset's core description on the registry page; independently confirmed verbatim via a WebSearch snippet quoting the same registry.opendata.aws page, and matches the underlying YAML source that generates the page. (Registry page, main Description/summary block)
  - *quote:* "a dataset from NOAA that contains daily observations over global land areas ... station-based measurements from land-based stations worldwide, about two thirds of which are for precipitation measurement only"
- **[✓ verified]** The dataset is a composite of climate records merged from numerous source networks and subjected to a common suite of quality-assurance reviews (specific QA methodology/metrics are not detailed on this page).
  - *evidence:* Stated directly in the description; no further methodological detail (e.g., which tests, error rates) is given on this page. (Registry page, Description block)
  - *quote:* "a composite of climate records from numerous sources that were merged together and subjected to a common suite of quality assurance reviews"
- **[✓ verified]** Beyond precipitation, the other meteorological elements the dataset records include daily maximum and minimum temperature, temperature at time of observation, snowfall, and snow depth.
  - *evidence:* Listed explicitly as the 'other meteorological elements' in the description. (Registry page, Description block)
  - *quote:* "Other meteorological elements include, but are not limited to, daily maximum and minimum temperature, temperature at the time of observation, snowfall and snow depth"
- **[✓ verified]** Some station records extend more than 175 years, and the dataset is organized into one CSV file per calendar year covering 1763 through the present.
  - *evidence:* Stated directly on the page as both an age claim and a file-organization/coverage claim; independently confirmed via WebSearch snippet quoting the same page ('Each file corresponds to a year from 1763 to present and is named as such'). (Registry page, Description block)
  - *quote:* "Some data are more than 175 years old ... Each file corresponds to a year from 1763 to present and is named as such."
- **[✓ verified]** The dataset's listed Update Frequency is Daily.
  - *evidence:* Given as a discrete metadata field on the registry page sidebar, consistent across both fetches. (Registry page, 'Update Frequency' metadata field)
  - *quote:* "Daily"
- **[✓ verified]** The data are released under the Creative Commons CC0-1.0 Public Domain Dedication, with no stated restrictions on use, though NOAA requests attribution be retained on unaltered data and that modified/adapted data not be represented as official NOAA content or imply NOAA endorsement.
  - *evidence:* Given in the page's 'License' field/section; corroborated by the underlying YAML license text and by an independent WebSearch snippet. (Registry page, 'License' section)
  - *quote:* "Creative Commons 1.0 Universal Public Domain Dedication (CC0-1.0) ... There are no restrictions on the use of the data."
- **[✓ verified]** The dataset's cloud resource is the public S3 bucket 'noaa-ghcn-pds' (ARN arn:aws:s3:::noaa-ghcn-pds) in AWS region us-east-1, paired with an SNS notification topic (ARN arn:aws:sns:us-east-1:123901341784:NewGHCNObject), and is accessible without AWS credentials.
  - *evidence:* Listed as structured 'Resources' metadata (ARNs, region, resource type) on the registry page; the anonymous-access CLI example ('--no-sign-request') was also surfaced by one fetch, consistent with a public bucket. (Registry page, 'Resources' / ARN metadata section)
  - *quote:* "arn:aws:s3:::noaa-ghcn-pds ... arn:aws:sns:us-east-1:123901341784:NewGHCNObject"
- **[✓ verified]** The listing is managed by NOAA, tagged with the keywords agriculture, climate, meteorological, weather (plus an internal 'aws-pds' program tag in the underlying source file), and points to a separate GitHub technical-documentation repository rather than embedding technical schema docs on the landing page itself.
  - *evidence:* Tags and 'Managed By'/'Documentation' link fields are given directly on the page; the 'aws-pds' tag was found only in the underlying YAML source used to generate the page, not confirmed as a visible chip in either rendered-page fetch. (Registry page sidebar fields ('Tags', 'Managed By', 'Documentation'); tag list also cross-checked against the underlying open-data-registry YAML source file)
  - *quote:* "Tags: aws-pds, agriculture, climate, meteorological, weather"
- **[✓ verified]** The page lists example downstream uses: AWS tutorials on calculating agricultural growing degree days and on visualizing 200+ years of global temperature (via Amazon Athena/QuickSight and via Apache Spark/BigQuery), plus a cited peer-reviewed publication relating natural/socioeconomic conditions to tick-borne encephalitis case patterns in Russia.
  - *evidence:* Listed under the page's 'Usage examples' / 'Data at work' section as titled links, not as data findings by NOAA/AWS themselves. (Registry page, 'Usage examples' section)
  - *quote:* "Calculating growing degree days using AWS Registry of Open Data"
- **[✓ verified]** (From the page's own linked 'Documentation,' not the registry landing page itself) The yearly CSV files encode each observation as one station-day row with five core elements — PRCP (precipitation, in tenths of mm), SNOW (snowfall, in mm), SNWD (snow depth, in mm), TMAX (max temperature, in tenths of °C), and TMIN (min temperature, in tenths of °C) — alongside station ID, date, element code, data value, and M-/Q-/S-flag quality-control columns.
  - *evidence:* This schema/units detail appeared only when the linked GitHub 'open-data-docs' documentation page (reached via the registry page's 'Documentation' link) was fetched separately; it is not stated on the registry.opendata.aws landing page text itself, so it is reported here as supplementary and separately sourced. (Linked documentation (github.com/awslabs/open-data-docs, noaa/noaa-ghcn path) — one hop from the registry landing page, not the landing page text)
  - *quote:* "The fields are comma delimited and each row represents one station-day."

## Data / numbers
- About two-thirds (~2/3) of GHCN-D stations are precipitation-only stations (fraction, unitless; no numerator/denominator station count given on this page)
- More than 175 years of historical record depth stated (years)
- Per-year CSV files span 1763 to present (calendar-year coverage, no end date given since it's described as ongoing/daily-updated)
- Update Frequency: Daily
- S3 Bucket ARN: arn:aws:s3:::noaa-ghcn-pds, Region us-east-1
- SNS Topic ARN: arn:aws:sns:us-east-1:123901341784:NewGHCNObject
- License: CC0-1.0 (Creative Commons Public Domain Dedication), 'no restrictions on the use of the data' as stated on the page
- Tags listed: agriculture, climate, meteorological, weather (plus 'aws-pds' in the underlying YAML source)
- (From linked documentation, not the landing page) Element units: PRCP in tenths of mm; SNOW in mm; SNWD in mm; TMAX in tenths of degrees C; TMIN in tenths of degrees C
- No baseline, error bar, accuracy percentage, or uncertainty estimate for any measurement is given anywhere in the fetched text — this is a data-access listing, not a validation/accuracy study

## Methods
This is a dataset registry/catalog page, not a methods paper, so it describes data provenance and access mechanics rather than an analytical method. Per the fetched text: GHCN-D data are produced by merging station reports from numerous underlying source networks into one composite record set and passing them through "a common suite of quality assurance reviews" — but the page does not specify which QA tests are applied, what error/flagging rates result, or how conflicts between sources are resolved. Distribution is via a public, unauthenticated Amazon S3 bucket (noaa-ghcn-pds, us-east-1), one CSV file per year, updated daily, with an SNS topic that can notify subscribers when new objects land in the bucket; one fetch surfaced an anonymous-access CLI example ("aws s3 ls --no-sign-request s3://noaa-ghcn-pds/"), consistent with no-login public access. The separately-fetched linked documentation (GitHub open-data-docs page) adds that each yearly file is row-per-station-day, comma-delimited, with ID/date/element/value plus M-flag/Q-flag/S-flag quality-control columns and an observation-time field — implying the "quality assurance reviews" manifest partly as these per-record QC flags, though the landing page itself never explains what the flags mean. No model, statistical method, or validation procedure is described anywhere in the fetched text; the source only claims the data are accessible, license-clear, and QA-reviewed, not that they meet any particular accuracy standard.

## Stated limitations
The source states no quantified limitations (no error bars, missing-data rates, station-siting/instrument-homogeneity caveats, or accuracy figures appear anywhere in the fetched text) — for a foundational dataset entry this absence is itself notable and should be recorded as a gap rather than assumed away. The only limitation-like language present is on data reuse, not data quality: the CC0-1.0 license section notes that although there are "no restrictions on the use of the data," NOAA requests that attribution be kept on unaltered data and that adapted/modified versions not be represented as official NOAA data or imply NOAA endorsement. The page also does not state how "quality assurance reviews" are performed, what fraction of raw reports are flagged/rejected, or how spatial/temporal coverage gaps (e.g., station dropout, the ~2/3 precipitation-only subset lacking temperature) affect any downstream use — none of that is addressed in the fetched text.

## Tensions with other findings
This source supplies weather/climate ground-station variables (air temperature, precipitation, snow), not aquatic chemistry or a satellite HAB signal — it is a candidate driver/predictor dataset, not a bloom-indicator dataset, and the page itself makes no claim about any relationship to algal blooms, water temperature, or nutrient loading; any use of GHCN-D air-temperature or precipitation as a proxy for water-body thermal conditions or nutrient runoff (as the HAB_PoC brief's fusion approach would require) is an assumption to be justified and tested separately, not something this source establishes — correlation between a nearby weather station's readings and a specific lake's bloom risk would still need to be demonstrated, not assumed. Two internal-consistency notes worth flagging for downstream spatial-matching work: (1) stations are land-based meteorological sites (not on-water/limnological sensors), so proximity to a given lake does not guarantee representativeness of that lake's surface conditions; (2) because roughly two-thirds of stations are precipitation-only, the effective network density for temperature-linked hypotheses is sparser than the raw station count would suggest, which matters for choosing "nearest station" pairings in any lake-level fusion pipeline.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All ten claims are directly supported by the source text fetches and cross-checks. No hallucinated numbers were detected; all figures (175 years, two-thirds stations, 1763 start date, ARNs, region identifiers, update frequency) appear verbatim in the provided source. No material caveats were omitted from claims; notably, the claims appropriately flag where methodological details are absent and where schema information is sourced from linked documentation rather than the landing page itself. The extraction demonstrates good practice by deliberately excluding internally inconsistent station-count figures from claims."

## Provenance
- Canonical URL: https://registry.opendata.aws/noaa-ghcn/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Primary URL fetched twice with different extraction prompts (comprehensive metadata extraction; then link/tag/license-detail extraction) as required for a High-relevance source, and reconciled — both returned consistent content with no contradictions on the core description, license, update frequency, or AWS resource identifiers. Because the fetch tool renders via a small model, I additionally (a) ran two WebSearch queries that independently surfaced verbatim snippets quoting the same registry.opendata.aws/noaa-ghcn/ page (confirming the 'about two thirds,' '175 years,' and '1763 to present' figures were not fetch-model paraphrase), and (b) fetched the underlying GitHub YAML source file that programmatically generates this AWS registry page, to check numbers against as close to raw source text as possible. I also fetched the page's own linked 'Documentation' (a GitHub open-data-docs page one hop from the landing page) to capture element units/schema not present on the landing page itself; that material is clearly labeled as separately sourced in key_claims/source_extract, not attributed to the registry landing page. One inconsistency surfaced only in that supplementary documentation fetch (two different station-count figures, ~160,000 vs. ~106,200, in the same fetch output) could not be reconciled or corroborated elsewhere, so per the no-fabrication rule I excluded any station-count figure from key_claims/data_numbers rather than assert an uncertain number; this is disclosed in source_extract. No paywall, login, or access barrier was encountered — the registry page and its linked resources are fully public. No explicit page-publication/last-updated date was found anywhere in the fetched text, so the 'year' field is omitted rather than guessed.
