---
key: FED-001
title: A national harmonized dataset of discrete chlorophyll from lakes and streams (2005-2022)
authors_or_org: Platt, L.R., Spaulding, S.A., Covert, A., Murphy, J.C., and Raynor, N. (U.S. Geological Survey, Ohio-Kentucky-Indiana Water Science Center)
year: 2023 (data release); companion peer-reviewed paper 2024 in Scientific Data
url: https://data.usgs.gov/datacatalog/data/USGS:638f5472d34ed907bf7c8f23
access_date: 2026-07-01
tier: FED
source_type: Government data release (USGS ScienceBase/data catalog) plus companion peer-reviewed data-descriptor paper (Scientific Data, accessed via PMC)
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: flag
---

# A national harmonized dataset of discrete chlorophyll from lakes and streams (2005-2022)

**What it is.** A U.S. Geological Survey public data release (DOI 10.5066/P9J0ZIOF) providing a harmonized, national compilation of discrete (field-collected, lab-analyzed) chlorophyll and pheophytin measurements from inland U.S. waters spanning 2005-2022, compiled by merging the Water Quality Portal (WQP) with USGS National Water Quality Laboratory (NWQL) records specifically to support process-based, machine-learning, and remote-sensing modeling of Harmful Algal Blooms.

## Key claims
*(each tagged with its blind-review verdict)*

- **[⚠ partial]** The dataset spans 2005-2022 (an 18-year span inclusive, described by the authors as a "17-year record") and covers nearly 84,000 unique sites and over 1,374,000 pigment measurements across the U.S. and territories.
  - *evidence:* Stated directly on the USGS data catalog landing page and repeated/detailed in the companion Scientific Data paper, which gives the precise unique-site count. (USGS data catalog abstract/purpose section; PMC companion paper abstract and results)
  - *quote:* "this dataset of nearly 84,000 sites and over 1,374,000 pigment measurements is the largest compilation of harmonized discrete, laboratory-extracted chlorophyll data for the US"
  - *reviewer:* The source explicitly calls it a '17-year record (2005-2022)' — the authors' preferred framing. While 2005-2022 is mathematically 18 calendar years, the authors explicitly chose '17-year record.' The claim's parenthetical attempts to reconcile both but conflates the authors' deliberate labeling with a mathematical recount. Numeric figures (84,000 sites, 1,374,000 measurements) are directly supported.
- **[✓ verified]** The exact unique site count after removing suspected in-situ sensor records is 83,829.
  - *evidence:* Given as a precise figure in the companion paper's methods/results discussion of site counts, distinct from the rounded "nearly 84,000" figure elsewhere. (PMC companion paper, results/discussion on site aggregation)
  - *quote:* "83,829 unique site names"
  - *reviewer:* Directly cited in source: '83,829 unique site names' after filtering.
- **[✓ verified]** Measurement counts differ sharply by pigment type and by phytoplankton vs. periphyton, with corrected chlorophyll a (phytoplankton) the largest single category and essentially no uncorrected chlorophyll a periphyton records.
  - *evidence:* Broken out explicitly by the companion paper as record counts per pigment/habitat combination. (PMC companion paper, data records/technical description)
  - *quote:* "Corrected chlorophyll a (phytoplankton): 651,242 records"
  - *reviewer:* Source provides exact record counts confirming the claim: Corrected chlorophyll a (phytoplankton) 651,242; Uncorrected chlorophyll a (periphyton) 0.
- **[⚠ partial]** The three chlorophyll/pheophytin parameters are not interchangeable: subtracting pheophytin from uncorrected chlorophyll a does not equal corrected chlorophyll a, and the WQP label "corrected chlorophyll a by EPA 445" is ambiguous between two different lab procedures (acidification vs. modified narrow-band-pass fluorometry) that the authors could not distinguish from WQP metadata alone.
  - *evidence:* Authors state this as a specific, methodologically important caveat affecting comparability of a core parameter in their own dataset. (PMC companion paper, discussion of EPA Method 445 and its modified variant)
  - *quote:* "It was not possible to differentiate between these two methods from the WQP metadata"
  - *reviewer:* Source confirms EPA 445 ambiguity and inability to distinguish from metadata. However, the claim that subtracting pheophytin from uncorrected chlorophyll a does not equal corrected chlorophyll a is NOT explicitly stated in the source. The three parameters are defined separately but this arithmetic relationship is not addressed.
- **[⚠ partial]** A depth cutoff of 10 meters was applied and records deeper than that were dropped because deep chlorophyll maxima could mislead remote-sensing and surface-oriented HAB modeling; records with missing depth were kept under the assumption most are near-surface.
  - *evidence:* Stated as an explicit processing decision with its methodological rationale given directly by the authors. (PMC companion paper, methods on depth filtering)
  - *quote:* "potentially misleading for modelling and remote sensing efforts"
  - *reviewer:* Source confirms '10 meters' cutoff and the stated rationale about deep chlorophyll maxima. However, it does NOT explain what was done with records having missing depth values or why. That handling procedure is not documented in the source text.
- **[✓ verified]** Roughly 0.48% of phytoplankton records (about 6,000 records) exceed 2,000 microgram/L chlorophyll, an extreme-value tail the authors could only partially verify against data providers and which they recommend users independently confirm before use.
  - *evidence:* Authors quantify the extreme-value fraction and explicitly caveat that not all such values could be verified. (PMC companion paper, discussion of extreme values)
  - *quote:* "6,000 records (~0.48%) exceeded 2000 µg/L"
  - *reviewer:* Source states directly: '6,000 records (~0.48%) exceeded 2000 µg/L' and 'Authors recommend users confirm extreme values with the data provider.'
- **[✓ verified]** Approximately 40% of the chlorophyll records sourced from USGS NWIS were still "preliminary" (not reviewed by a data steward) at time of release, and these were retained in the dataset rather than excluded.
  - *evidence:* A direct data-quality caveat disclosed by the authors about the QA/QC status of a large minority of the underlying records. (PMC companion paper, data quality/validation discussion)
  - *quote:* "Approximately 40% of chlorophyll data in NWIS characterized as "preliminary" (unchecked by data stewards) were retained"
  - *reviewer:* Source explicitly states: 'Approximately 40% of chlorophyll data in NWIS characterized as preliminary (unchecked by data stewards) were retained.'
- **[⚠ partial]** Co-located monitoring sites (e.g., multiple site numbers on the same lake or river reach) were deliberately not aggregated into a single physical location, which the authors note would otherwise increase apparent sample density at a given place.
  - *evidence:* Authors flag this design choice as something a downstream modeler needs to know about, since it affects apparent spatial sampling density. (PMC companion paper, discussion of site handling)
  - *quote:* "co-located sites were not aggregated, for example, multiple site numbers from an individual lake, a specific river reach, or geographic location were not combined"
  - *reviewer:* Source confirms non-aggregation of co-located sites with examples. However, the stated reason—'would otherwise increase apparent sample density'—is not explicitly given in the source text as the authors' rationale. This is a plausible inference but not stated.
- **[⚠ partial]** Chlorophyll a concentration is explicitly characterized by the authors as only a rough proxy for algal biomass, since cellular chlorophyll content varies with species, nutrients, light, temperature, and cell condition, and high benthic (periphyton) chlorophyll does not necessarily indicate high growth rate.
  - *evidence:* A direct, author-stated interpretive limitation about what the core measured quantity does and does not represent biologically -- relevant to any downstream claim that treats chlorophyll as equivalent to bloom biomass or growth. (PMC companion paper, discussion/limitations)
  - *quote:* "Chlorophyll a concentration is only a rough proxy for algal biomass because cell chlorophyll content is variable across species, nutrient concentration, light regime, temperature, and cell condition"
  - *reviewer:* Source confirms chlorophyll as 'only a rough proxy' with variable cell content across species, nutrients, light, temperature, and condition. However, the claim about periphyton chlorophyll NOT indicating growth rate is not in the source. The source discusses periphyton mixing in high flows but does not make a claim about growth-rate implications.
- **[✓ verified]** The dataset is intended to support HAB-relevant modeling in rivers in particular, an environment the authors describe as historically understudied for HABs relative to lakes, and the largest number of chlorophyll records in the dataset actually comes from rivers/streams rather than lakes.
  - *evidence:* Stated purpose plus a structural fact about the data's composition that matters for anyone assuming this is primarily a lake dataset. (PMC companion paper, background/summary and comparison-to-prior-datasets discussion)
  - *quote:* "While our dataset includes chlorophyll a from phytoplankton in lakes and estuaries, the largest number of records is from rivers"
  - *reviewer:* Source states intended use for 'prediction of harmful algal blooms (HABs), particularly in rivers' described as 'historically understudied,' and notes 'the largest number of records is from rivers.'

## Data / numbers
- Temporal coverage: 2005-01-01 to 2022-12-31 (described by authors as both a "17-year record" and, in the companion paper's abstract phrasing reported via search summary, an "18-year record")
- Unique sites: 83,829 (precise, post-filtering) / "nearly 84,000" (rounded, as stated on the landing page and in the paper's headline claim)
- Total pigment measurements: "over 1,374,000"
- Corrected chlorophyll a, phytoplankton: 651,242 records
- Pheophytin, phytoplankton: 406,056 records
- Uncorrected chlorophyll a, phytoplankton: 315,492 records
- Corrected chlorophyll a, periphyton: 2,236 records
- Pheophytin, periphyton: 1,187 records
- Uncorrected chlorophyll a, periphyton: 0 records
- Extreme values: ~6,000 records (~0.48% of phytoplankton records) exceed 2,000 µg/L chlorophyll
- Depth cutoff applied: samples with depth >10 meters excluded
- Preliminary/unreviewed NWIS records retained: ~40% of NWIS chlorophyll data
- Records explicitly flagged with an algal-bloom hydrologic-event code: 437 records
- Units: plankton (phytoplankton) chlorophyll reported in µg/L (micrograms per liter); periphyton chlorophyll reported in mg/m² (milligrams per square meter)
- File sizes on ScienceBase: site metadata CSV 10.59 MB; corrected chlorophyll a data CSV 106.56 MB; pheophytin data CSV 72.35 MB; uncorrected chlorophyll a data CSV 68.77 MB; FGDC metadata XML 55.23 KB
- No baseline or uncertainty/error bars are reported by the source for any of these counts -- they are inventory/compilation totals, not statistical estimates with confidence intervals

## Methods
Data were pulled from WQP (via the R package dataRetrieval v2.7.12, which itself aggregates EPA WQX, USGS NWIS, and USDA ARS STEWARDS) and merged with NWQL CSV exports. Three pigment parameters were harmonized following EPA Methods 445 and 446: (12.1) uncorrected chlorophyll a (raw optical measurement, includes pheophytin interference), (12.2) corrected chlorophyll a (post-acidification, estimates active chlorophyll), and (12.3) pheophytin (calculated degradation-pigment estimate). Harmonization steps: unit conversion (phytoplankton -> µg/L; periphyton -> mg/m2; records with non-convertible units such as NA, %, IVFU, NTU, RFU omitted); creation of a standardized censored-value code; depth filtering (records with depth >10 m dropped; NA depths retained on the assumption they are near-surface); removal of records with non-chlorophyll analytical method codes; removal of suspected in-situ sensor records (identified by high-frequency same-day timestamps with inconsistent EPA 445 codes); exact-match duplicate removal across site_no/date/date_time/parameter/censored_cd (WQP record kept over NWQL in duplicate pairs, with two exceptions); removal of NWQL records for non-USGS sites (unverifiable location); removal of org_cd "CSKTRIBE" (known conversion error) and one Canadian site; removal of negative values; and, for NWQL specifically, removal of replicate records (SAMP_TYPE=7) and retention only of 14 specified MEDIUM codes. The paper reports the method works well enough to be called "the largest compilation of harmonized discrete, laboratory-extracted chlorophyll data for the US," while explicitly flagging that it could not resolve ambiguity between two different lab procedures both coded as "corrected chlorophyll a," and that co-located sites were deliberately left unaggregated.

## Stated limitations
Authors explicitly disclose: (1) ~40% of NWIS-sourced records remain "preliminary" (not steward-reviewed) yet were retained; (2) ~0.48% (~6,000) of phytoplankton records are extreme values (>2,000 µg/L) that could not all be verified with data providers, and users are told to confirm extreme values independently; (3) the WQP label "corrected chlorophyll a by EPA 445" is methodologically ambiguous between two distinct lab procedures (standard acidification vs. modified narrow-band fluorometry) that cannot be disambiguated from WQP metadata, so these values "may not be comparable in natural waters"; (4) co-located sites were not aggregated, so apparent per-site sampling density is not true physical-location density; (5) site numbering is inconsistent across organizations and years even for the same physical location; (6) a large fraction of records lack sample-depth information, handled by retaining NA-depth records under a near-surface assumption rather than resolving it; (7) suspected in-situ sensor records were removed heuristically and the authors acknowledge some may remain miscoded and undetected elsewhere in WQP; (8) in rivers, periphyton disturbed by high flow can mix with phytoplankton in the water column, making it difficult to determine algal source, and the dataset does not resolve this ambiguity; (9) chlorophyll a is stated by the authors to be "only a rough proxy for algal biomass" due to variability in cellular chlorophyll content across species/nutrients/light/temperature/cell condition, and high periphyton chlorophyll does not necessarily indicate high growth rate; (10) sampling frequency, distribution, and methods vary greatly by state (e.g., Florida dominates phytoplankton records, Indiana dominates periphyton records), producing uneven geographic representation; (11) the authors state there is "no related primary publication associated with this data release" on the original landing page (superseded by the later 2024 Scientific Data companion paper found via search, which itself was not the primary object of the assigned URL).

## Tensions with other findings
This is a measurement-compilation resource, not a HAB-prediction or driver-analysis study, so it does not itself make causal claims -- but it materially complicates any downstream causal or predictive claim built on chlorophyll-a as a HAB proxy: the authors' own statement that chlorophyll a is "only a rough proxy for algal biomass" and that determining whether river chlorophyll comes from phytoplankton or disturbed periphyton "can be difficult" means any model (including remote-sensing chlorophyll retrievals, which is directly relevant to the EPA CyAN satellite signal referenced elsewhere in this project) that treats chlorophyll concentration as a clean stand-in for bloom biomass or cyanobacteria abundance is working with a proxy the source authors themselves flag as noisy and species/condition-dependent. Additionally, the ambiguity between two different "corrected chlorophyll a" lab methods sharing the same parameter code is a concrete, source-documented harmonization/label-conflation risk that any project fusing multiple in-situ chlorophyll sources (e.g., this dataset alongside Water Quality Portal pulls done independently) should account for, since combining them naively could silently mix two non-comparable measurement procedures under one column name.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Only 437 records carry an explicit algal-bloom hydrologic-event code—a critical limitation for bloom-detection use cases not mentioned in claims.
  - River/periphyton mixing during high flows complicates source determination, flagged in source but not reflected in any claim.
- **Reviewer notes:** Four of ten claims rated 'partial' due to incremental additions or sub-claims not found in source. None are entirely unsupported (no 'no' verdicts). The 'partial' ratings reflect overstated framing (17 vs. 18 years), unsubstantiated arithmetic assertions (pheophytin subtraction), undocumented handling procedures (missing depth), and logical inferences stated as author claims (aggregation rationale, periphyton growth rate). The most significant dropped caveat is the 437-record bloom-event code limitation, which materially constrains direct bloom-detection applications of the dataset. Overall: 'flag' due to multiple 'partial' findings indicating the claims add detail beyond what the source supports."

## Provenance
- Canonical URL: https://data.usgs.gov/datacatalog/data/USGS:638f5472d34ed907bf7c8f23
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: The primary URL assigned (USGS data catalog landing page) is a metadata/summary page, not the full technical documentation -- both required WebFetch passes on it converged well but lacked precise record/site counts and detailed QA methodology (it only gave qualitative descriptions of harmonization). Per the task's escalation instruction ("if incomplete... WebSearch for the primary or DOI version and use it"), I searched and found the dataset's open-access, peer-reviewed companion paper ("Chlorophyll a in lakes and streams of the United States (2005-2022)," Scientific Data, published via PMC at PMC11169558) which supplied the exact counts and detailed methods that the landing page omitted; this is the same underlying data release (same DOI/dataset, same authors), not a different source, so it is used here as the fuller technical documentation of the identical FED-001 dataset rather than a substitute source. I additionally fetched the ScienceBase catalog record directly to confirm file names/formats/sizes for the actual data release. The Nature.com URL for the same companion paper hit an institutional-login redirect wall (403-style paywall gate) and was not used; PMC's open-access mirror was used instead and is the authoritative text for all detailed numbers cited here. All four fetches were fully consistent with no contradictions found. No numbers were rounded or altered from what the fetches returned; where the source itself gives both a rounded figure ("nearly 84,000") and a precise figure (83,829) I report both and note the distinction explicitly rather than picking one.
