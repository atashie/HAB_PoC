---
key: ACAD-004
title: A systematic literature review of forecasting and predictive models of harmful algal blooms in flowing waters (peer-reviewed version published as: "Fifty years of riverine harmful algal bloom modeling: A global synthesis of approaches, challenges, and opportunities")
authors_or_org: Jennifer C. Murphy, Rebecca M. Gorney, Lisa V. Lucas, Jacob A. Zwart (also rendered "Jacob Aaron Zwart"), Jennifer L. Graham — U.S. Geological Survey, Central Midwest Water Science Center
year: 2025 (bioRxiv preprint, posted 2025-09-29); 2026 (peer-reviewed publication, Water Research v.303, art. 126240)
url: DOI 10.1101/2025.09.29.679270 redirects (302) to http://biorxiv.org/lookup/doi/10.1101/2025.09.29.679270 (confirmed canonical bioRxiv location, but this and both given primary URLs returned HTTP 403 on fetch). The peer-reviewed version resolves to https://doi.org/10.1016/j.watres.2026.126240 (Water Research, v.303, art. 126240, 2026). Companion dataset DOI: 10.5066/P1JWCCXF.
access_date: 2026-07-01
tier: ACAD
source_type: bioRxiv preprint of a systematic literature review, subsequently published as a peer-reviewed journal article in Water Research; companion structured dataset archived on USGS ScienceBase
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# A systematic literature review of forecasting and predictive models of harmful algal blooms in flowing waters (peer-reviewed version published as: "Fifty years of riverine harmful algal bloom modeling: A global synthesis of approaches, challenges, and opportunities")

> Note: provisional URL was resolved to a primary source. Original: https://www.biorxiv.org/content/10.1101/2025.09.29.679270v1.full

**What it is.** A USGS-authored systematic literature review examining 162 articles (1975-2024) on forecasting/predictive models of harmful algal blooms (HABs) in flowing waters — rivers, run-of-river reservoirs/lock-and-dam systems, and tidal/estuarine systems with riverine processes (explicitly not standing lakes) — to characterize which modeling approaches, predictor variables, and geographic contexts dominate the field and to identify persistent gaps. Posted as a bioRxiv preprint (2025-09-29) and subsequently published in Water Research (2026); a companion structured dataset (review_data.csv + response_definitions.csv codebook) is archived publicly on USGS ScienceBase.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The review comprises 162 articles on forecasting/predictive models of HABs in flowing waters, published across nearly 50 years (explicit range 1975-2024), and covering more than 80 rivers worldwide.
  - *evidence:* Headline scope/count of the review, stated in the abstract and corroborated independently across the USGS preprint landing page, the USGS published-article landing page, and the ScienceBase dataset description (which gives the exact 1975-2024 range). (Abstract (USGS pub. page index ID 70272235; ScienceBase item summary))
  - *quote:* "The review included 162 articles published over nearly 50 years, covering more than 80 rivers worldwide."
- **[✓ verified]** Process-based (mechanistic) models were the most common modeling approach among reviewed river-HAB studies (59% of articles), more common than data-driven/statistical-ML approaches (37%).
  - *evidence:* Specific percentage breakdown given in the abstract; repeated consistently on both the preprint's and the published article's USGS landing pages, giving it higher confidence. (Abstract (USGS pub. pages for preprint 70272235 and published article 70276589))
  - *quote:* "Process-based models were more common (59%) than data-driven approaches (37%)"
- **[✓ verified]** Nearly all reviewed studies (93%) were site-specific model applications, and the modeled systems were predominantly large, eutrophic rivers with flow modifications or obstructions (e.g., dams).
  - *evidence:* Given as a headline statistic characterizing generalizability in the published-article abstract summary. (Abstract (USGS pub. page 70276589))
  - *quote:* "Articles largely focused on site-specific applications (93%) across more than 80 rivers worldwide, with most modeled systems being large, eutrophic rivers with flow modifications or obstructions"
- **[✓ verified]** Reviewed studies were geographically concentrated: South Korea alone accounted for 26% of articles, followed by Europe (25%), the United States (21%), and China (12%).
  - *evidence:* Specific percentage breakdown by country/region given in the published-article abstract; the four listed groups sum to 84%, implying roughly 16% spread across other regions (not itemized in the fetched text). (Abstract (USGS pub. page 70276589))
  - *quote:* "South Korea accounting for 26% of articles, followed by Europe (25%), United States (21%), and China (12%)"
- **[✓ verified]** The observational datasets underlying the reviewed models were typically short and spatially sparse: about 5 years of record, sampled weekly to monthly, at 1-10 sites.
  - *evidence:* Stated as a typical/summary characterization of the underlying calibration data in the published-article abstract. (Abstract (USGS pub. page 70276589))
  - *quote:* "spanned 5 years, with weekly to monthly sampling at 1–10 sites"
- **[✓ verified]** Across the reviewed river-HAB models, the key predictor variables were nutrients, light availability, streamflow, algal physiological process representations, and water temperature.
  - *evidence:* Explicit list of key predictors given in the published-article abstract. (Abstract (USGS pub. page 70276589))
  - *quote:* "Nutrients, light availability, streamflow, algal physiological processes, and water temperature emerged as key predictors"
- **[✓ verified]** Most articles used algal biomass or chlorophyll as the modeling endpoint; 23% of articles were motivated by concern with algal toxins, but only 5% actually used a toxin measure as the modeled endpoint.
  - *evidence:* Distinguishes stated motivation from the actual modeled endpoint, quantifying a specific gap between toxin-related concern and toxin-endpoint modeling. (Abstract (USGS pub. page 70272235))
  - *quote:* "23% developed models motivated by algal toxins, though only 5% used toxins as an endpoint"
- **[✓ verified]** Only 6% of the reviewed studies modeled benthic (bottom-attached) HABs; the remaining studies addressed pelagic (water-column) HABs.
  - *evidence:* Direct quantified statement of benthic vs. pelagic modeling focus in the review. (Abstract (USGS pub. page 70272235))
  - *quote:* "Only 6% modeled benthic HABs; the remainder addressed pelagic HABs."
- **[✓ verified]** River/flowing-water HAB models place greater emphasis on streamflow and hydrologic transport metrics as predictors than lake-focused HAB models do.
  - *evidence:* Direct comparative statement between river- and lake-focused HAB modeling literature regarding flow/transport variables. (Abstract (USGS pub. page 70272235))
  - *quote:* "Streamflow and transport metrics received greater emphasis in river models compared to lake models."
- **[✓ verified]** The review's inclusion criteria required that a model make predictions beyond its own calibration dataset (in time or space) or be used for sensitivity/scenario analysis; purely descriptive/correlative studies without such extrapolative use were excluded.
  - *evidence:* Explicit eligibility/inclusion rule for the systematic review, described on the companion ScienceBase dataset page. (Methods / Inclusion criteria (ScienceBase item, DOI 10.5066/P1JWCCXF))
  - *quote:* "make predictions beyond the calibration datasets in time or space or are utilized for sensitivity or scenario analysis"
- **[✓ verified]** The review's methodology consisted of querying multiple scientific publication databases, a three-level screening process, and structured information extraction from the 162 included articles via a standardized form with multiple-choice and write-in fields; the resulting structured dataset (review_data.csv plus a response_definitions.csv codebook) is archived publicly.
  - *evidence:* Describes the systematic-review workflow and the resulting public data product on the companion ScienceBase page. (Methods (ScienceBase item, DOI 10.5066/P1JWCCXF))
  - *quote:* "queries from multiple scientific publication databases, followed by a three-level screening process, and finally information extraction"
- **[✓ verified]** The review identifies persistent field-wide gaps limiting progress on river HAB modeling: a lack of site-specific model inputs representing key processes, overlooked riverine environments (the benthos and side/back-channel areas), and poorly/inconsistently reported model performance metrics across the literature.
  - *evidence:* Stated as the review's research-gap/conclusions content on the USGS preprint landing page, echoed with different wording ("underrepresentation of benthic habitats, neglect of side-channel and backwater influences, insufficient documentation of river features") on the published-article landing page. (Discussion/Conclusions summary (USGS pub. pages 70272235 and 70276589))
  - *quote:* "lack of site-specific model inputs ... poorly reported model performance metrics"

## Data / numbers
- 162 articles reviewed (systematic-review corpus)
- Time span: nearly 50 years; explicit range 1975-2024 (49 years)
- >80 rivers worldwide covered by the reviewed studies
- 59% of articles used process-based (mechanistic) models
- 37% of articles used data-driven (statistical/ML) models
- 93% of articles were site-specific model applications (single location/system)
- Geographic distribution: South Korea 26%, Europe 25%, United States 21%, China 12% of articles
- 23% of articles motivated by algal toxins; 5% used toxins as the actual modeled endpoint
- 6% of articles modeled benthic HABs (remainder modeled pelagic HABs)
- Typical underlying dataset: ~5 years of record, weekly-to-monthly sampling frequency, 1-10 monitoring sites
- Published version: Water Research, Volume 303, article no. 126240, 17 pages (2026)
- Preprint DOI 10.1101/2025.09.29.679270 (posted 2025-09-29); published-article DOI 10.1016/j.watres.2026.126240; companion dataset DOI 10.5066/P1JWCCXF; USGS index IDs 70272235 (preprint) and 70276589 (published)

## Methods
Systematic literature review: queries run across multiple scientific publication databases, a three-level screening process, then structured information extraction using a standardized form (multiple-choice plus write-in fields) applied uniformly to all 162 included articles. Companion structured dataset archived on USGS ScienceBase (DOI 10.5066/P1JWCCXF): review_data.csv (extracted info from the 162 articles, with columns for location, aggregated responses, standardized terminology) and response_definitions.csv (column/response definitions). Inclusion criteria: only models that predict beyond their calibration data (in time or space) or that are used for sensitivity/scenario analysis were included; purely descriptive/empirical-correlation studies without such extrapolative use were excluded. Scope: not limited to a specific cyanobacteria taxon or modeling endpoint; covers rivers, run-of-river reservoirs, lock-and-dam systems, and riverine estuaries — explicitly excludes standing lakes as the primary study object. Per the abstract-level content obtained (no full Methods/Results text was accessible): process-based approaches are reported as most common (59%) versus data-driven/ML approaches (37%); site-specific single-location applications dominate (93%) over demonstrably transferable models; underlying calibration datasets are typically short (~5 yr) and spatially coarse (weekly-to-monthly sampling, 1-10 sites); and model-performance reporting across the reviewed literature is characterized as "poorly reported" — a field-wide weakness the review flags rather than a strength of any particular method.

## Stated limitations
No excerpt of the review's own explicit self-critique of its methodology (e.g., database coverage, language/publication bias, gray-literature exclusion) was retrievable from the abstract-level text obtained — only field-level limitations that the authors identify IN THE REVIEWED LITERATURE were accessible: (1) "lack of site-specific model inputs" representing key processes; (2) overlooked riverine environments, specifically the benthos and side/back-channel areas (only 6% of studies modeled benthic HABs); (3) "poorly reported model performance metrics" across the literature; (4) per the published-version phrasing, "underrepresentation of benthic habitats, neglect of side-channel and backwater influences, insufficient documentation of river features"; (5) heavy geographic clustering (South Korea/Europe/US/China = 84% of articles combined) and dominance of site-specific (93%) rather than generalizable modeling, implying limited demonstrated transferability across river systems; (6) short calibration records (~5 yr) and coarse spatial sampling (1-10 sites) underlying most models. These are limitations of the REVIEWED FIELD as characterized by the authors, not a stated critique of the review's own systematic-review methodology (which was not accessible in the fetched text).

## Tensions with other findings
(1) Ecosystem-type mismatch: this review's scope is explicitly flowing waters (rivers, run-of-river reservoirs, lock-and-dam systems, riverine estuaries) and excludes standing lakes — the primary object of most other HAB PoC sources (e.g., EPA CyAN targets lakes/reservoirs). Findings here (predictor emphasis, model-family split, generalizability caveats) should not be assumed to transfer directly to lentic (lake) systems without explicit justification. (2) Model-family framing: the fetched USGS summary text states process-based models are more common (59%) than data-driven models (37%) in rivers, framed with an added comment that this 'contrasts with lake-focused literature where data-driven models predominated' — but that specific comparative clause appeared outside quotation marks in the fetched output, suggesting it may be the fetch/rendering tool's own gloss rather than a verbatim sentence from the paper. It is flagged here as a plausible-but-unverified secondary claim, not a directly quoted fact, pending full-text access. If accurate, it would caution against assuming ML/data-driven approaches are the presumptive default for HAB forecasting broadly, which is relevant to the PoC's model-family choice. (3) Reporting-rigor tension: the review's own flag that model-performance metrics are 'poorly reported' across the river-HAB literature is itself evidence that many prior HAB modeling papers fail the 'every number carries a baseline and an uncertainty' bar — reinforcing, rather than contradicting, the project's fidelity/transparency standard, and a useful cautionary data point when citing other HAB modeling papers uncritically.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All 12 claims are explicitly supported by the source text. Figures are traceable to direct quotations or closely paraphrased statements in the preprint landing page, published article landing page, or ScienceBase dataset description. No hallucinated numbers, no dropped caveats detected. The claims accurately reflect the scope, methodological approach, key results, and identified research gaps as presented in the source material."

## Provenance
- Canonical URL: DOI 10.1101/2025.09.29.679270 redirects (302) to http://biorxiv.org/lookup/doi/10.1101/2025.09.29.679270 (confirmed canonical bioRxiv location, but this and both given primary URLs returned HTTP 403 on fetch). The peer-reviewed version resolves to https://doi.org/10.1016/j.watres.2026.126240 (Water Research, v.303, art. 126240, 2026). Companion dataset DOI: 10.5066/P1JWCCXF.
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Both given primary URLs (v1.full and .full.pdf) returned HTTP 403 Forbidden on two separate WebFetch attempts each using different, comprehensive extraction prompts, as did the DOI-resolved bioRxiv URL (http://biorxiv.org/lookup/doi/10.1101/2025.09.29.679270, reached via a 302 redirect from https://doi.org/10.1101/2025.09.29.679270) and a fallback text-extraction proxy (r.jina.ai, HTTP 401 Unauthorized — requires an API key). Per the task's fallback instructions, WebSearch was used to locate, and WebFetch was then used to retrieve, three alternate institutional landing pages describing this exact review (same authorship/DOI lineage): the USGS publication page for the bioRxiv preprint, the USGS ScienceBase catalog page for the review's companion structured dataset, and the USGS publication page for the peer-reviewed published version in Water Research (v.303, art. 126240, 2026) — which covers the same 162-article corpus. These three successful, independently-worded fetches were reconciled into one union, satisfying the spirit of the 'fetch twice and reconcile' instruction given the primary source was unreachable. No full paper text (detailed Methods, PRISMA screening-flow counts at each stage, Results tables/figures, Discussion/Limitations sections verbatim, specific model-name tallies such as Random Forest/ANN/SVM counts, or quantitative performance metrics like R2/RMSE values) could be obtained — all extracted content is abstract/summary-level. The highest-confidence numbers (162 articles; 59%/37% process-based vs. data-driven split; >80 rivers; 93% site-specific) are corroborated across 2-3 independent fetched pages; others (toxin-endpoint percentages, benthic-modeling percentage, geographic breakdown by country, typical dataset characteristics, key predictor list) are single-sourced to one fetched page each. One comparative sentence fragment ('contrasting with lake-focused literature where data-driven models predominated') appeared outside quotation marks in a fetch output and is flagged in the tensions field as possibly the fetch tool's own gloss rather than a verbatim quote from the paper.
