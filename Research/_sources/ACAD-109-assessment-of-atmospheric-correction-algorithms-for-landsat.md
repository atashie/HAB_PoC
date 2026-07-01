---
key: ACAD-109
title: Assessment of Atmospheric Correction Algorithms for Landsat-8/9 Operational Land Imager over Inland and Coastal Waters
authors_or_org: Yiqiang Hu, Haigang Zhan, Qingyou He, Weikang Zhan — South China Sea Institute of Oceanology, Chinese Academy of Sciences (affiliation per OpenAlex metadata; not independently confirmed from the paper body since full text was inaccessible)
year: 2025
url: https://www.mdpi.com/2072-4292/17/17/3055
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article — Remote Sensing (MDPI), open access, CC-BY 4.0
categories: [remote-sensing]
relevance: Medium
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Assessment of Atmospheric Correction Algorithms for Landsat-8/9 Operational Land Imager over Inland and Coastal Waters

> Note: provisional URL was resolved to a primary source. Original: https://doi.org/10.3390/rs17173055

**What it is.** A peer-reviewed remote-sensing methods paper (Remote Sensing, MDPI, 2025) that benchmarks six atmospheric correction (AC) algorithms — ACOLITE, C2RCC, iCOR, L2GEN, OC-SMART, and POLYMER — for Landsat-8/9 OLI imagery against 440 in-situ radiometric matchups spanning inland lakes in China and globally distributed coastal waters (GLORIA dataset), to determine which AC algorithm is most accurate under which water-type/turbidity conditions.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study systematically benchmarked six state-of-the-art atmospheric correction (AC) algorithms — ACOLITE, C2RCC, iCOR, L2GEN, OC-SMART, and POLYMER — applied to Landsat-8/9 OLI satellite imagery.
  - *evidence:* Stated directly as the study's core method/design in the abstract. (Abstract (Remote Sensing 17(17), Article 3055))
  - *quote:* "we systematically evaluated six state-of-the-art AC algorithms—ACOLITE, C2RCC, iCOR, L2GEN, OC-SMART, and POLYMER—using Landsat-8/9 OLI data"
- **[✓ verified]** The evaluation benchmark comprised 440 high-quality in-situ radiometric matchups, combining inland-lake data from China's Satellite-Ground Synchronous Campaign with coastal-water data from the globally distributed GLORIA dataset.
  - *evidence:* Abstract states the sample size and the two constituent data sources used as ground truth for validating satellite-derived reflectance. (Abstract)
  - *quote:* "This study leverages 440 high-quality in situ radiometric matchups spanning a wide range of aquatic environments, including inland lakes from China's Satellite-Ground Synchronous Campaign and coastal waters from the globally distributed GLORIA dataset."
- **[✓ verified]** A single, unified Optical Water Type (OWT) classification framework was applied across the combined inland+coastal dataset so that AC performance could be compared consistently across a wide range of environmental/turbidity conditions.
  - *evidence:* Methodological claim about how comparability across heterogeneous water types was ensured. (Abstract)
  - *quote:* "A unified Optical Water Type (OWT) classification framework ensured consistency across environmental conditions."
- **[✓ verified]** AC algorithm performance is not uniform — it varies significantly depending on water type, meaning no single algorithm is universally best.
  - *evidence:* Headline result stated in the abstract; this is the paper's central finding. (Abstract)
  - *quote:* "Results highlight significant variability in algorithm performance based on water type."
- **[✓ verified]** In coastal waters, L2GEN produced the lowest errors in the visible bands, whereas in inland waters OC-SMART achieved the best overall accuracy.
  - *evidence:* Direct comparative result for coastal vs. inland water bodies. (Abstract)
  - *quote:* "In coastal waters, L2GEN demonstrated the lowest errors in visible bands, whereas OC-SMART achieved superior overall accuracy in inland waters."
- **[✓ verified]** ACOLITE specifically outperformed the other five algorithms in the blue spectral region (443 nm and 482 nm bands) for inland waters.
  - *evidence:* Band-specific comparative claim with exact wavelengths named. (Abstract)
  - *quote:* "Notably, ACOLITE exhibited better performance than other algorithms in the blue spectral region (443 and 482 nm) for inland waters."
- **[✓ verified]** Algorithm accuracy also depends on turbidity class (Optical Water Type): OC-SMART stayed robust across the whole turbidity gradient; ACOLITE and iCOR performed best in highly turbid waters (OWT 5-6); L2GEN, C2RCC, and POLYMER performed comparatively better in clearer waters (OWT 3-4).
  - *evidence:* OWT-stratified breakdown of algorithm ranking, the paper's most granular reported result. (Abstract)
  - *quote:* "OWT-specific analysis showed that OC-SMART maintained robust accuracy across the turbidity gradient, while ACOLITE and iCOR excelled in highly turbid waters (OWTs 5–6). In contrast, L2GEN, C2RCC, and POLYMER were more effective in clearer waters (OWTs 3–4)."
- **[⚠ partial]** The paper also discusses each algorithm's practical applicability and offers recommendations for mitigating 'adjacency effects' (AE) — a known contamination source near land-water boundaries — to further improve AC accuracy.
  - *evidence:* States the study's applied/practical contribution beyond the pure benchmarking result. (Abstract)
  - *quote:* "The study further discusses the applicability of each algorithm and offers recommendations for mitigating adjacency effects (AE) to improve AC accuracy."
  - *reviewer:* Source supports discussion of applicability and AE mitigation recommendations; however, it does not define what adjacency effects (AE) are or characterize them as occurring near land-water boundaries. This definition is external domain knowledge not present in the abstract.

## Data / numbers
- 6 atmospheric correction (AC) algorithms benchmarked: ACOLITE, C2RCC, iCOR, L2GEN, OC-SMART, POLYMER
- 440 high-quality in situ radiometric matchups used as validation benchmark (combined inland + coastal)
- Blue-band wavelengths where ACOLITE outperformed other algorithms in inland waters: 443 nm and 482 nm
- Optical Water Types (OWT) 5-6 = 'highly turbid' regime, where ACOLITE and iCOR excelled
- Optical Water Types (OWT) 3-4 = 'clearer waters' regime, where L2GEN, C2RCC, and POLYMER were more effective
- No RMSE, MAPE, R2, bias, uncertainty, or study-date values were retrievable — the abstract states only relative/qualitative rankings ('lowest errors', 'superior accuracy', 'more effective'), not the underlying numeric error statistics that presumably appear in the paper's results tables

## Methods
Six operational atmospheric-correction (AC) algorithms — ACOLITE, C2RCC, iCOR, L2GEN, OC-SMART, and POLYMER — were run on Landsat-8/9 OLI imagery and validated against 440 in-situ radiometric matchups drawn from two complementary datasets: inland lakes from China's Satellite-Ground Synchronous Campaign, and coastal waters from the globally distributed GLORIA dataset. A single unified Optical Water Type (OWT) classification framework was applied to both datasets so AC performance could be compared consistently across a turbidity/optical gradient (the abstract references OWT classes at least 3 through 6, i.e., clearer to highly turbid). Per the abstract's results: L2GEN performs best (lowest visible-band errors) in coastal waters; OC-SMART performs best overall in inland waters and is the most robust across the full turbidity gradient; ACOLITE performs particularly well in the blue bands (443, 482 nm) in inland waters and, together with iCOR, in highly turbid waters (OWT 5-6); L2GEN, C2RCC, and POLYMER perform comparatively better in clearer waters (OWT 3-4). The study also proposes recommendations for mitigating "adjacency effects" (AE), a known error source near land-water boundaries. No further methodological detail (exact matchup/collocation protocol, OWT classification algorithm/reference, statistical error formulas, study period/dates, or site coordinates) was accessible beyond what is stated in the abstract, because the full text could not be retrieved (see fetch_notes).

## Stated limitations
Only the publisher's abstract was accessible (full text blocked across all attempted routes), so the authors' own explicit Limitations/Discussion/Conclusion text could not be retrieved or quoted, and cannot be summarized beyond what follows. The one caveat visible even at abstract level: the authors treat "adjacency effects" (AE) as an unresolved source of AC error significant enough to warrant separate mitigation recommendations ("offers recommendations for mitigating adjacency effects (AE) to improve AC accuracy"), implying AE is not fully solved by any of the six benchmarked algorithms as-is. No sample-size, sensor-transferability, seasonal, or geographic-coverage limitations are stated in the abstract text itself.

## Tensions with other findings
This is a remote-sensing methods/validation paper, not a HAB study — it makes no direct claims about cyanobacteria, chlorophyll-a, or bloom risk, so any link to HAB findings is inferential, not stated by the source. Its finding that AC algorithm choice materially changes retrieved water-leaving reflectance accuracy, and that the best-performing algorithm differs by water type/turbidity (OC-SMART inland vs. L2GEN coastal; ACOLITE/iCOR in turbid OWT 5-6 vs. L2GEN/C2RCC/POLYMER in clearer OWT 3-4), is a caution against treating satellite-derived reflectance or downstream chlorophyll/cyanobacteria indices as uniformly accurate across lakes of differing turbidity. It is also specific to Landsat-8/9 OLI rather than the Sentinel-3 OLCI sensor underlying EPA CyAN's primary cyanobacteria product, so its algorithm-choice recommendations should not be assumed to transfer directly to a CyAN-based pipeline without independent validation on that sensor.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** Seven of eight claims are directly and explicitly supported by the source abstract with exact textual matches or minimal paraphrasing (e.g., 'outperformed' ≈ 'exhibited better performance'). One claim (8) is partial: the source confirms the paper discusses algorithm applicability and offers AE mitigation recommendations, but does not provide the technical definition of adjacency effects that the claim supplies from external knowledge. No hallucinated numbers detected; all figures (440 matchups, 443/482 nm bands, OWT class 5–6 and 3–4) are explicitly in the source. The abstract is complete and detailed enough to support or reject each claim without ambiguity."

## Provenance
- Canonical URL: https://www.mdpi.com/2072-4292/17/17/3055
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Extensive multi-route attempt made to reach full text, all blocked: (1) WebFetch on the DOI (https://doi.org/10.3390/rs17173055) redirected to the MDPI landing page https://www.mdpi.com/2072-4292/17/17/3055, which returned HTTP 403 Forbidden on two separate attempts; (2) the MDPI HTML view (/htm) returned 403; (3) the MDPI PDF endpoint (/pdf) returned 403, including when using the exact Unpaywall-supplied versioned OA link (/pdf?version=1756823328); (4) the r.jina.ai reader-proxy mirror of the MDPI page returned HTTP 401 Unauthorized; (5) DOAJ's article-search API and (6) CORE.ac.uk both returned 403. Successfully retrieved the publisher-supplied abstract verbatim (identical wording across all three) via the Semantic Scholar Graph API (api.semanticscholar.org), the Crossref REST API (api.crossref.org/works/...), and OpenAlex (api.openalex.org) — the latter two also supplied confirmed bibliographic metadata (CC-BY 4.0 license, Vol. 17, Issue 17, article 3055, published online 2025-09-02, 65 references, publisher MDPI AG) and author affiliation. Given full text was unreachable, this dossier is built entirely from the verified abstract; no results-table numbers (RMSE/R2/MAPE/bias), methods details beyond what the abstract states, or the authors' own stated limitations/discussion text could be extracted. full_text_access is therefore set to "abstract" and fetch_status to "partial."
