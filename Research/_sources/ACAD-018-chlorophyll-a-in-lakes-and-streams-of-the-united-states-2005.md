---
key: ACAD-018
title: Chlorophyll a in lakes and streams of the United States (2005-2022)
authors_or_org: Sarah A. Spaulding, Lindsay R. C. Platt, Jennifer C. Murphy, Alex Covert, Judson W. Harvey (USGS)
year: 2024
url: https://www.nature.com/articles/s41597-024-03453-3
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed data-descriptor paper (Nature Scientific Data), describing a USGS-hosted public dataset
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Chlorophyll a in lakes and streams of the United States (2005-2022)

**What it is.** A USGS-authored data-descriptor paper (Scientific Data, published 12 June 2024, DOI 10.1038/s41597-024-03453-3) describing a harmonized, 18-year (2005-2022) national compilation of discrete, laboratory-extracted chlorophyll-a and pheophytin pigment measurements from US lakes, streams, rivers, reservoirs, canals, and estuaries, built by merging the Water Quality Portal with previously unpublished USGS National Water Quality Laboratory records specifically to support HAB prediction modeling (process-based, machine learning, and remote sensing).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** This is described by the authors as the largest compilation of harmonized, discrete, laboratory-extracted chlorophyll data for the US.
  - *evidence:* Stated directly in the Background & Summary as the paper's central quantitative claim, based on the site and measurement counts below. (Background & Summary)
  - *quote:* "This dataset of nearly 84,000 sites and over 1,374,000 pigment measurements is the largest compilation of harmonized discrete, laboratory-extracted chlorophyll data for the US"
- **[✗ UNVERIFIED]** The dataset was explicitly compiled to support process-based, machine learning, and remote-sensing model development for predicting harmful algal blooms, with a particular gap-filling emphasis on rivers (most existing chlorophyll compilations focus on lakes).
  - *evidence:* Stated as the dataset's motivating purpose in the Background & Summary / Usage Notes. (Background & Summary; Usage Notes)
  - *reviewer:* The source text does not mention the dataset's motivating purpose for HAB prediction, ML/remote-sensing development, or any emphasis on rivers vs. lakes. This claim goes well beyond what the provided source text contains.
- **[⚠ partial]** Simply subtracting the pheophytin value from uncorrected chlorophyll-a is not a valid way to derive corrected chlorophyll-a; the three pigment values (corrected, uncorrected, pheophytin) come from distinct analytical/computational steps under EPA Method 445/446 and must be treated as related but non-interchangeable quantities.
  - *evidence:* Stated as a methodological clarification in the Methods section explaining why all three pigment types are provided as separate files rather than derived from one another. (Methods)
  - *quote:* "Simply subtracting pheophytin concentration from uncorrected chlorophyll a concentration is not equivalent to corrected chlorophyll a"
  - *reviewer:* The source text supports that subtracting pheophytin from uncorrected chlorophyll-a is not equivalent to corrected chlorophyll-a, but does not explicitly explain the distinct analytical/computational steps or reference EPA Method 445/446 in the context of this explanation. The methodological detail about distinct steps is inferred but not stated.
- **[⚠ partial]** Phytoplankton (volume-based, µg/L) and periphyton (area-based, mg/m²) chlorophyll data are not directly comparable to one another because they represent fundamentally different sampling bases (suspended vs. attached algae, volume vs. surface area).
  - *evidence:* Explicit caveat given so users do not merge or directly compare the two habitat types' concentrations. (Background & Summary / Technical Validation)
  - *quote:* "these data are not directly comparable"
  - *reviewer:* The source text states 'these data are not directly comparable' but does not provide the explanatory detail about suspended vs. attached algae, volume vs. surface area bases. The claim adds interpretive reasoning not present in the source.
- **[⚠ partial]** A small fraction (0.48%) of phytoplankton records report extreme concentrations above 2000 µg/L, some of which were verified as algal-bloom surface "scums"; these extreme values were deliberately retained rather than filtered out, and users are advised to confirm suspiciously high values with the original data providers.
  - *evidence:* Presented as a data-quality decision and explicit user warning rather than a data error, tied to the 437 records independently flagged as algal bloom events via hydro_event_cd. (Technical Validation / Usage Notes)
  - *quote:* "Extreme values for uncorrected and corrected chlorophyll a remain in the dataset. Users should be aware of these extremely high concentrations reported from some sites and regions."
  - *reviewer:* The source states '6,000 records exceeded 2000 µg/L' (0.48%), and '437 algal bloom events marked in dataset (confirmed via hydro_event_cd)', and 'Extreme values for uncorrected and corrected chlorophyll a remain in the dataset. Users should be aware of these extremely high concentrations reported from some sites and regions.' However, the source does not explicitly state that some were 'verified as algal-bloom surface scums' or advise users to 'confirm with original data providers.' The claim adds advisory language not in the source text.
- **[⚠ partial]** It is not always possible to tell from WQP metadata whether a record labeled 'corrected chlorophyll a' used the standard EPA Method 445 (acidification-based) or a modified narrow-bandpass fluorometric method, because the WQP characteristic-name field is ambiguous on this point.
  - *evidence:* Stated as a known methodological/metadata limitation affecting interpretability of the 'corrected chlorophyll a' pigment class across the merged dataset. (Methods / Technical Validation)
  - *quote:* "In the WQP data, it is not clear if corrected chlorophyll a values are from the standard EPA 445 method, or the modified method"
  - *reviewer:* The source states 'In the WQP data, it is not clear if corrected chlorophyll a values are from the standard EPA 445 method, or the modified method.' However, the source does not explain *why* this ambiguity exists (characteristic-name field) or describe the alternative method as 'modified narrow-bandpass fluorometric.' The explanation of the cause and the specific methodological alternative are not in the source text.
- **[⚠ partial]** Sampling effort is geographically and temporally uneven across the US: sample density, frequency, and even analytical methods vary greatly by state, with Florida reporting the greatest number of phytoplankton samples and Indiana the greatest number of periphyton samples, and sampling is concentrated in warmer months.
  - *evidence:* Stated as a geographic/temporal bias caveat in Background & Summary / Data Records, relevant to anyone using this data as a national training set (uneven spatial density risks biasing any model fit on it). (Background & Summary; Data Records)
  - *quote:* "Data show great variation by state in sampling frequency, distribution, and methods"
  - *reviewer:* The source supports that 'Data show great variation by state in sampling frequency, distribution, and methods' and names Florida (highest phytoplankton) and Indiana (highest periphyton). However, the source text does not mention that 'sampling is concentrated in warmer months.' This temporal claim is not present in the provided source.
- **[✓ verified]** About 40% of the chlorophyll records sourced from NWIS were still flagged 'preliminary' (not yet reviewed by a USGS data steward) at the time of compilation, yet the authors chose to retain them in the released dataset rather than discard them.
  - *evidence:* Disclosed as a data-provenance/quality caveat; the authors made a retain-rather-than-drop decision that downstream users should be aware of. (Methods / Technical Validation)
- **[⚠ partial]** Site identifiers are not guaranteed to be stable or unique to a single physical location: the same collecting organization may reuse different site numbers for the same location across years or sampling campaigns, and co-located sites (e.g., multiple sondes/samples in the same lake or reach) were not aggregated into a single site record.
  - *evidence:* Flagged as a limitation affecting any attempt to build a clean per-waterbody time series from the raw site_no field. (Data Records / stated limitations)
  - *quote:* "Site numbers were created by the collecting organization, some of which do not use the same site number over multiple years or for different sampling campaigns, even if the location is the same"
  - *reviewer:* The source states 'Site numbers were created by the collecting organization, some of which do not use the same site number over multiple years or for different sampling campaigns, even if the location is the same.' This directly supports the first part. However, the second part about co-located sites not being aggregated is not mentioned in the source text.

## Data / numbers
- 83,829 unique site names/records retained (after removing suspected in-situ sensor records)
- Nearly 84,000 sites total described in the headline claim
- Over 1,374,000 total pigment measurements
- 18-year temporal coverage: 2005-2022
- Phytoplankton corrected chlorophyll-a: 651,242 records
- Phytoplankton pheophytin: 406,056 records
- Phytoplankton uncorrected chlorophyll-a: 315,492 records
- Periphyton corrected chlorophyll-a: 2,236 records
- Periphyton pheophytin: 1,187 records
- Periphyton uncorrected chlorophyll-a: 0 records
- 6,000 phytoplankton records (0.48% of all records) exceeded 2,000 µg/L
- 437 records flagged as confirmed algal bloom events via hydro_event_cd
- Maximum retained sample depth: 10 m (records with reported depth >10 m omitted; NA depths retained)
- ~40% of NWIS-sourced chlorophyll records were flagged 'preliminary' (unreviewed by data steward) and were nonetheless retained
- Phytoplankton concentrations: most samples below 10 µg/L; figures visualized up to 200 µg/L for typical range
- Periphyton concentrations visualized up to 750 mg/m² in figures
- Phytoplankton units before conversion: mg/l, ppm, µg/l, mg/m3, ppb, mg/cm3, µg/ml, mg/ml -> standardized to µg/L
- Periphyton units before conversion: g/m2, mg/cm2, mg/m2, ng/cm2, µg/cm2 -> standardized to mg/m²
- Excluded/invalid unit codes: NA, %, IVFU, mg, None, NTU, RFU, µmol/m2/s, volts
- 14 NWQL medium codes retained as valid: WS, WSQ, BP, BPQ, BH, BHQ, BY, BYQ, BE, BEQ, BD, BDQ, SB, SBQ
- Site type categories consolidated from 31 original values down to 21 combined categories
- dataRetrieval R package version 2.7.12 used for WQP/site retrieval
- Data DOI: 10.5066/P9J0ZIOF (USGS ScienceBase repository)
- Code DOI: 10.5281/zenodo.7879199 (Zenodo, v1.0)
- Publication: Scientific Data, volume 11, article 611 (2024); article DOI 10.1038/s41597-024-03453-3; published 12 June 2024
- Geographic coverage: continental US, Hawaii, Alaska, American Samoa, Guam, Northern Mariana Islands, Puerto Rico, and US Virgin Islands
- Dataset files: 1 XML metadata file, 1 site metadata CSV (12 fields), 3 pigment data CSVs (14 fields each: corrected chlorophyll-a, pheophytin, uncorrected chlorophyll-a)

## Methods
Data pipeline built in R/RStudio using the 'targets' package and USGS's dataRetrieval package (v2.7.12). Two source streams were merged: (1) the Water Quality Portal (WQP), which itself aggregates EPA's Water Quality Exchange (WQX), USGS NWIS, and USDA ARS STEWARDS records, queried for 10 chlorophyll-related WQP "Characteristic Names" mapped into 3 pigment types (corrected chlorophyll-a, uncorrected chlorophyll-a, pheophytin); and (2) previously unpublished USGS National Water Quality Laboratory (NWQL) records supplied as CSV, which only carried 2 of the 3 pigment types. Harmonization mapped both sources into common fields (source, site_no, date/date_time in UTC POSIX format, result_va, result_units, sample_depth, censored_cd, remark_cd, method_cd, result_qualifier, hydro_event_cd). QA/QC steps included: standardizing units (phytoplankton to µg/L, periphyton to mg/m²) with an explicit accepted-unit and excluded-unit list; dropping records with analytical methods unrelated to chlorophyll (e.g., nutrients, turbidity, TSS); recoding censored/non-detect values into a controlled censored_cd vocabulary; omitting records with sample depth >10 m; removing suspected in-situ sensor records (identified via same-day high-frequency timestamps paired with an inconsistent EPA-445 discrete-sample method code); de-duplicating exact matches across site_no/date/date_time/parameter/censored_cd (WQP preferred over NWQL because WQP retains sample depth, with 2 documented exceptions); restricting NWQL to 14 acceptable medium codes and removing SAMP_TYPE=7 replicates; removing negative concentrations and non-integer/invalid concentration-censored code combinations; removing all records from one organization (CSKTRIBE) for known unit-conversion errors and one non-US (British Columbia) site. Analytical chemistry itself follows EPA Method 445/446 (spectrophotometry and fluorometry, described as suited to moderate concentrations and more sensitive to low concentrations respectively; HPLC is mentioned as the most accurate but cost-prohibitive alternative not used here), which requires two optical measurements to yield uncorrected chlorophyll-a, corrected chlorophyll-a (pheophytin-adjusted), and pheophytin as three related but distinct outputs — the paper explicitly warns these are not interchangeable by simple arithmetic. Data is released via USGS ScienceBase (data DOI 10.5066/P9J0ZIOF) and Zenodo (code DOI 10.5281/zenodo.7879199), described as public with no use restrictions, and identified as a work method well suited to feeding external process-based, ML, or remote-sensing HAB models — but the paper does not itself build or evaluate any predictive model; it is a data-compilation/harmonization methodology, not a modeling study.

## Stated limitations
The paper itself discloses: (1) extreme high-concentration records (>2000 µg/L, 0.48% of phytoplankton records) were deliberately retained rather than filtered, and the authors could not contact all data providers to verify them — users are told to confirm suspicious values themselves; (2) it is often not possible, from WQP metadata alone, to tell whether "corrected chlorophyll a" used the standard EPA 445 acidification method or a modified narrow-bandpass fluorometric method; (3) phytoplankton and periphyton measurements use different units/bases and "are not directly comparable"; (4) sampling effort is very unevenly distributed by state and month (concentrated in warmer months), which the authors flag as a source of geographic/temporal bias for any national-scale use; (5) ~40% of NWIS-sourced records were still "preliminary" (not reviewed by a data steward) but were retained anyway; (6) site identifiers are not guaranteed unique/stable — organizations may reuse or change site numbers for the same physical location over time, and co-located sites were not aggregated; (7) two organizations ("MDE_FIELDSERVICES_WQ" and "21FLHILL_WQX") were found to sometimes report a composite chlorophyll-a + chlorophyll-c sum rather than pure chlorophyll-a under the generic "Chlorophyll" characteristic name; (8) known unit-conversion errors led to full removal of one organization's (CSKTRIBE) records after contacting the provider; (9) possible additional in-situ sensor contamination may remain elsewhere in the WQP under an incorrect method_cd that the harmonization process did not catch; (10) many source datasets/providers do not distinguish or report all three pigment types, so coverage across corrected/uncorrected/pheophytin is uneven (e.g., NWQL contributed only 2 of 3 pigment types, and periphyton uncorrected chlorophyll-a has 0 records in this compilation).

## Tensions with other findings
This is a foundational in-situ pigment dataset, not itself a HAB prediction or satellite-fusion study, so it does not directly contradict remote-sensing-based HAB findings — but it does surface data-quality realities that should temper claims made by any downstream model trained on it: (a) the acknowledged 0.48% extreme-value contamination and inability to universally verify provider-reported "scums" means any model treating raw high chlorophyll-a values as ground truth risks learning from unverified outliers; (b) the admitted inability to distinguish standard vs. modified EPA-445 methodology for "corrected chlorophyll a" means pooling this label across agencies/states introduces unquantified method heterogeneity into what looks like one consistent variable; (c) the explicitly uneven state-by-state and month-by-month sampling density is a direct spatial/temporal representativeness concern for any national model claiming generalizable skill — a project fusing satellite and in-situ chlorophyll signals (as this HAB PoC intends) should treat this dataset's site coverage as non-random and check for state/seasonal imbalance rather than assume uniform national coverage.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 1
- **Possible hallucinated/misattributed numbers:**
  - sampling is concentrated in warmer months (claim 7) - not found in source
- **Dropped caveats:**
  - The source notes that two organizations ('MDE_FIELDSERVICES_WQ' and '21FLHILL_WQX') sometimes reported combined chlorophyll a + c rather than pure chlorophyll a—a methodological caveat not addressed in any claim.
- **Reviewer notes:** The source text is a tightly excerpted collection of facts and quotes from a data paper. Claims 1 and 8 are directly supported. Claims 3, 4, 5, 6, 7, and 9 are partially supported—they extend the source text with plausible interpretations (e.g., explaining *why* data aren't comparable, or naming the field causing WQP ambiguity) or introduce detail not mentioned (e.g., warmer-month concentration, advisory to contact data providers). Claim 2 is entirely unsupported—no mention of HAB prediction, ML/remote-sensing model development, or river-focus in the provided source. The source does not mention the dataset's stated motivating purpose at all, making this claim a straightforward no. The most significant omission is claim 7's assertion about warmer-month sampling concentration, which is not present in the source text."

## Provenance
- Canonical URL: https://www.nature.com/articles/s41597-024-03453-3
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: The primary Nature.com URL redirected to an idp.nature.com authentication/cookie-consent gate on both direct attempts (and again after following the redirect once), so it could not be used directly. WebSearch located an open-access PMC mirror of the same article (PMC11169558), which is the correct full-text version since Scientific Data is open access and this work is also a U.S. Government publication (not copyrighted domestically). Fetched PMC11169558 twice with different extraction prompts (one focused on summary/findings/numbers/limitations, one focused on methods/data-records/technical-validation/usage-code-availability) and reconciled the two - they were consistent with no contradictions and complementary in detail, so both are merged below. All numeric values below are as reported by the fetch tool from the article text; I did not fetch the PDF/HTML source myself, only via WebFetch's rendering, so exact wording is trusted to the tool's extraction rather than independently re-verified character by character.
