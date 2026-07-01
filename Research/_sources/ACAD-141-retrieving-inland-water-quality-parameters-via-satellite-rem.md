---
key: ACAD-141
title: Retrieving Inland Water Quality Parameters via Satellite Remote Sensing: Sensor Evaluation, Atmospheric Correction, and Machine Learning Approaches
authors_or_org: Mohsen Ansari; Anders Knudby (corresponding author); Meisam Amani; Michael Sawada — Department of Geography, Environment and Geomatics, University of Ottawa (Amani additionally affiliated with Canada Centre for Mapping and Earth Observation, Natural Resources Canada)
year: 2025
url: https://www.mdpi.com/2072-4292/17/10/1734
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed, open-access journal article (literature review / evaluation), Remote Sensing (MDPI), CC BY 4.0, 171 references
categories: [remote-sensing]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Retrieving Inland Water Quality Parameters via Satellite Remote Sensing: Sensor Evaluation, Atmospheric Correction, and Machine Learning Approaches

> Note: provisional URL was resolved to a primary source. Original: https://doi.org/10.3390/rs17101734

**What it is.** A 2025 peer-reviewed literature review and qualitative evaluation (not a new empirical retrieval study) examining the three components required to retrieve inland-water quality parameters — chlorophyll-a, colored dissolved organic matter (CDOM), and non-algal particles (NAP) — from optical satellite imagery: satellite sensor suitability (with a proposed sensor-ranking method), atmospheric correction algorithm performance over inland waters, and machine-learning-based bio-optical retrieval approaches, closing with recommended future research directions.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Effective retrieval of water quality parameters from optical satellite imagery requires three components: (1) a sensor sensitive to water-quality-driven optical variation, (2) accurate atmospheric correction to recover water-leaving radiance/reflectance, and (3) a bio-optical model linking the optical signal to the water quality parameter.
  - *evidence:* Stated in the abstract as the organizing framework; the paper's three-part structure directly evaluates each of these components in turn. (Abstract)
  - *quote:* "Effective water quality parameter retrieval via optical satellite remote sensing requires three key components: (1) a sensor whose measurements are sensitive to variations in water quality; (2) accurate atmospheric correction to eliminate the effect of absorption and scattering in the atmosphere and retrieve the water-leaving radiance/reflectance; and (3) a bio-optical model used to estimate water quality from the optical signal."
- **[✓ verified]** The paper reviews decommissioned, active, and upcoming satellite sensors and introduces a ranking method for selecting sensors suited to retrieving chlorophyll-a, CDOM, and non-algal particles specifically in inland (not open-ocean) waters, intended to aid sensor selection for future studies.
  - *evidence:* Presented in the abstract as the first of the paper's three deliverables. (Abstract)
  - *quote:* "a review of decommissioned, active, and upcoming satellite sensors is presented, highlighting their advantages and limitations, and a ranking method is introduced to assess their suitability for retrieving chlorophyll-a, colored dissolved organic matter, and non-algal particles in inland waters. This ranking can aid in selecting appropriate sensors for future studies."
- **[✓ verified]** No single atmospheric correction (AC) algorithm evaluated performs consistently well across all inland-water conditions; algorithm choice should instead be matched to the specific use case based on each algorithm's documented strengths and weaknesses.
  - *evidence:* Presented as the key result of the paper's second component (comparative evaluation of AC algorithms over inland waters). (Abstract)
  - *quote:* "The results show that no atmospheric correction algorithm performed consistently across all conditions. However, understanding their strengths and weaknesses allows users to select the most suitable algorithm for a specific use case."
- **[✓ verified]** Machine-learning-based bio-optical retrieval models for inland water quality have four specific, named limitations — low generalizability, low dimensionality, spatial/temporal autocorrelation, and information leakage — which motivate locally trained models, rigorous cross-validation, and integration of auxiliary data to increase dimensionality as mitigations.
  - *evidence:* Presented as the key result/discussion of the paper's third component (ML use in bio-optical models). (Abstract)
  - *quote:* "Machine learning models have limitations, including low generalizability, low dimensionality, spatial/temporal autocorrelation, and information leakage. These issues highlight the importance of locally trained models, rigorous cross-validation methods, and integrating auxiliary data to enhance dimensionality."
- **[⚠ partial]** The paper concludes with recommendations for promising future research directions spanning the three reviewed components (sensors, atmospheric correction, ML-based bio-optical modeling).
  - *evidence:* Final sentence of the abstract; the specific recommendations themselves are not enumerated in the abstract text and could not be verified since the full text was inaccessible. (Abstract)
  - *quote:* "Finally, recommendations for promising research directions are provided."
  - *reviewer:* Source text confirms that recommendations for research directions are provided, but does not explicitly state whether they span the three reviewed components. The scope of the recommendations is not specified in the abstract.

## Data / numbers
- No quantitative retrieval-accuracy metrics (R2, RMSE, MAE, bias, SNR, etc.) are stated in the abstract; such values, if present, would be in the inaccessible full-text tables/figures (e.g., the described sensor-ranking table and AC-algorithm comparison) and could not be extracted or verified.
- 171 references cited (Crossref 'reference-count' metadata field — bibliometric, not a scientific finding).
- Published online 15 May 2025; Remote Sensing (MDPI), ISSN 2072-4292, Volume 17, Issue 10, Article No. 1734 (Crossref/DOI metadata).
- 13 citing works recorded by Crossref ('is-referenced-by-count') as of the Crossref index snapshot dated 2026-06-20 — a growing bibliometric count, not a fixed statistic.

## Methods
This is a literature review and qualitative evaluation, not a new empirical retrieval experiment. Per the abstract, it has three method components: (1) a structured review of decommissioned, active, and upcoming satellite sensors relevant to inland waters, paired with a novel sensor-ranking method scoring suitability for chlorophyll-a, CDOM, and non-algal-particle (NAP) retrieval; (2) a comparative examination of atmospheric correction algorithms' strengths and weaknesses over inland waters (specific algorithm names, e.g., ACOLITE/C2RCC/POLYMER/l2gen, are not given in the abstract and could not be confirmed without the full text); (3) a discussion of machine-learning-based bio-optical retrieval models, their stated failure modes, and recommended mitigations (local training, rigorous cross-validation, auxiliary-data-driven dimensionality increases). No specific ML algorithm names (e.g., random forest, XGBoost, specific neural-network architectures) are given in the abstract, so none can be reported here without fabrication.

## Stated limitations
Per the abstract (the only source text accessible): every reviewed satellite sensor has "advantages and limitations" for inland-water retrieval (exact trade-offs not detailed in the abstract itself, hence the paper's proposed ranking method to navigate them); atmospheric correction algorithms show no universally consistent performance — "no atmospheric correction algorithm performed consistently across all conditions" over inland waters, so AC choice is inherently context/use-case dependent; and machine-learning bio-optical retrieval models are explicitly limited by "low generalizability, low dimensionality, spatial/temporal autocorrelation, and information leakage," which the authors treat as still-open problems requiring locally trained models, rigorous cross-validation, and auxiliary data rather than as solved issues.

## Tensions with other findings
This review's own abstract flags exactly the validation pitfalls (spatial/temporal autocorrelation and "information leakage" inflating apparent skill, plus low cross-site generalizability) that many single-lake or single-study ML-based chlorophyll-a/CDOM/NAP retrieval papers may not adequately guard against — this source is independent, review-level (171-reference) corroboration that reported retrieval accuracies elsewhere in the HAB remote-sensing literature should be read cautiously unless those studies specifically test spatial/temporal generalization. It also complicates treating any single atmospheric-correction algorithm as universally "best": since "no atmospheric correction algorithm performed consistently across all conditions," AC-algorithm performance claims from other sources should be read as conditional on that study's specific water types/sensors, not as generalizable rankings. (These are the source's own stated cautions about the literature, not this reviewer's independent test of causation — correlation/skill metrics in any single retrieval study should not be assumed to generalize without the safeguards this review recommends.)

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The source uses 'including' when listing the four ML limitations, suggesting they are illustrative examples rather than an exhaustive enumeration; the claim presents them as definitive without this qualifier.
- **Reviewer notes:** Four of five claims are directly supported by verbatim text in the abstract. Claim 5, while plausible given the paper's three-part structure, makes an inference (that recommendations span all three components) that is not explicitly confirmed by the source text. The evidence_note on claim 5 already acknowledges this limitation. One minor caveat: the ML limitations are marked with 'including,' suggesting they are representative rather than exhaustive, but this is not a material misrepresentation by the claim."

## Provenance
- Canonical URL: https://www.mdpi.com/2072-4292/17/10/1734
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: WebFetch on the primary DOI URL (https://doi.org/10.3390/rs17101734) redirected to https://www.mdpi.com/2072-4292/17/10/1734, which returned HTTP 403 Forbidden, as did every other MDPI-domain variant tried (www/no-www, /pdf, /htm, the version-stamped Unpaywall PDF URL, and the sciprofiles.com author-profile mirror) — this appears to be bot/Cloudflare-style access control rather than a paywall, since Unpaywall independently confirms Gold OA / CC-BY status. r.jina.ai proxy returned 401 (needs an API key unavailable in this environment). web.archive.org fetch is explicitly disallowed for this tool. scholar.archive.org had no indexed copy (paper is very recent, May 2025). WebSearch found no PMC/ResearchGate/other full-text mirror. I therefore pivoted to metadata APIs (Crossref, Semantic Scholar, Unpaywall) and recovered the full verbatim publisher abstract plus complete bibliographic metadata (authors, ORCIDs, affiliations, date, volume/issue/page, license, reference count) — this is real, traceable, verbatim source content, just abstract-level rather than full-text. No section/table/figure locations, specific sensor names, specific AC algorithm names, specific ML model names, or any numeric performance metrics could be obtained or verified; per task instructions, only the abstract is summarized, and key_claims/data_numbers explicitly flag this absence rather than inferring or fabricating values. Given the strong topical match to this project's own stated concerns (leakage, spatiotemporal autocorrelation, generalizability in ML validation), a follow-up fetch attempt from a tool/session with different network egress or an authenticated browser is recommended to retrieve the full text, sensor-ranking table, and AC-algorithm comparison for a complete dossier entry.
