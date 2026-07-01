---
key: ACAD-110
title: Comment on "Early warning of harmful cyanobacteria blooms based on high frequency in situ monitoring and intelligible machine learning modelling: The case study of Lake Müggelsee (Germany)" by Recknagel et al. (Water Research 287 2025 124,514)
authors_or_org: Feilong Shen; Zhongbing Chen (Czech University of Life Sciences Prague, per Europe PMC affiliation record)
year: 2026
url: https://linkinghub.elsevier.com/retrieve/pii/S0043135426000886
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal Comment (short critique/correspondence), Water Research
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Comment on "Early warning of harmful cyanobacteria blooms based on high frequency in situ monitoring and intelligible machine learning modelling: The case study of Lake Müggelsee (Germany)" by Recknagel et al. (Water Research 287 2025 124,514)

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/abs/pii/S0043135426000886

**What it is.** A short peer-reviewed "Comment" (Water Research, Vol. 293, article 125406, epub 15 Jan 2026) by Feilong Shen and Zhongbing Chen that critiques the methodology of Recknagel et al. (2025, Water Research 287, article 124514), a study forecasting cyanobacterial blooms in Lake Müggelsee (Germany) 5 days ahead using high-frequency in-situ monitoring and three machine-learning algorithms. It raises four specific validation concerns and recommends fixes, without disputing the original paper's overall value as a demonstration.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The commenters characterize the paper under comment as using high-frequency in-situ data and three fundamentally different machine learning algorithms to forecast cyanobacterial blooms in Lake Müggelsee at a 5-day horizon.
  - *evidence:* Opening framing sentence of the abstract, setting up the critique that follows. (Abstract, opening sentence)
  - *quote:* "leveraging high-frequency in-situ data and three fundamentally different machine learning algorithms to forecast cyanobacterial blooms in Lake Müggelsee at a 5-day horizon"
- **[✓ verified]** The commenters argue that cross-year preprocessing and interpolation of weekly biovolume measurements up to hourly/daily resolution can introduce temporal (look-ahead-style) leakage and can artificially smooth the bloom dynamics the model is meant to predict.
  - *evidence:* First of four numbered methodological concerns listed in the abstract. (Abstract, point (i))
  - *quote:* "cross-year preprocessing and interpolation of weekly biovolume to hourly/daily resolution, which can introduce temporal leakage and smooth bloom dynamics"
- **[✓ verified]** The commenters argue the original study's evaluation emphasized R2/RMSE rather than threshold-exceedance skill and lead-time distributions at the operationally relevant 4 mm3/L biovolume hazard level, and communicated uncertainty only in a limited way.
  - *evidence:* Second of four numbered concerns; directly questions whether reported accuracy metrics translate into actionable early-warning skill at the decision-relevant hazard threshold. (Abstract, point (ii))
  - *quote:* "evaluation emphasizing R2/RMSE rather than threshold-exceedance skill and lead-time distributions at the 4 mm3/L hazard level, with limited uncertainty communication"
- **[✓ verified]** The commenters argue that the original model's strong reliance on the phycocyanin (PHYCO) sensor variable, while operationally reasonable, needs PHYCO-persistence baselines and no-PHYCO ablation tests to quantify how much of the forecasting skill is incremental value from the model versus simple persistence/dependence on that one sensor.
  - *evidence:* Third of four numbered concerns, about input/sensor dependency and the need for ablation-based attribution of skill. (Abstract, point (iii))
  - *quote:* "strong reliance on phycocyanin (PHYCO), which is operationally reasonable but warrants PHYCO-persistence baselines and no-PHYCO ablations to quantify incremental forecasting value and sensor dependence"
- **[✓ verified]** The commenters argue that mixed data-aggregation choices, in which single-station driver (predictor) variables were paired with multi-station or depth-integrated target variables, can bias the relationships the model learns.
  - *evidence:* Fourth of four numbered concerns, about a spatial/aggregation mismatch between predictors and targets. (Abstract, point (iv))
  - *quote:* "mixed aggregation choices and single-station drivers paired with multi-station/depth-integrated targets, which can bias learned relationships"
- **[✓ verified]** The commenters conclude that adopting leakage-robust validation practices, sensitivity analyses, event-based metrics, uncertainty reporting, and strong baselines would further strengthen the original study's operational credibility, while explicitly stating this would not change its overall contribution as a pragmatic demonstration.
  - *evidence:* Closing recommendation sentence of the abstract; frames the critique as constructive refinement rather than rejection of the original work. (Abstract, closing sentence)
  - *quote:* "A practical set of leakage-robust validation practices, sensitivity analyses, event-based metrics, uncertainty reporting, and strong baselines could further strengthen the study's operational credibility without changing its overall contribution as a pragmatic demonstration."

## Data / numbers
- 5-day forecast horizon — lead time of the original Recknagel et al. (2025) early-warning models, as characterized by the commenters
- 4 mm3/L — cyanobacteria biovolume 'hazard level' the commenters say should anchor threshold-exceedance skill/lead-time evaluation, instead of relying only on R2/RMSE
- three (3) — number of 'fundamentally different' machine learning algorithms used in the original study, per the commenters' description
- Water Research, vol. 287 (2025), article no. 124,514 — citation of the original Recknagel et al. paper under comment
- Water Research, vol. 293 (2026), article no. 125406; DOI 10.1016/j.watres.2026.125406; PMID 41619426; Epub 15 Jan 2026, print/issue date 1 Apr 2026 — bibliographic identifiers for this comment itself

## Methods
This is a peer-reviewed journal 'Comment' (critique/correspondence), not a primary empirical study. From the retrieved abstract, there is no indication the commenters ran their own new empirical re-analysis of the Müggelsee dataset; rather, they critique the methodology of the original study (high-frequency in-situ monitoring + 3 ML algorithms forecasting cyanobacterial biovolume 5 days ahead) and prescribe specific validation methods the original authors should apply: leakage-robust cross-validation/splitting, PHYCO-persistence and no-PHYCO-ablation baselines, threshold-exceedance and event/lead-time-based skill metrics evaluated at the 4 mm3/L hazard level, explicit uncertainty reporting, and sensitivity analyses around data-aggregation choices. Whether the comment's full body (beyond the abstract) contains the commenters' own recomputed numbers could not be verified, since only the abstract was retrievable (ScienceDirect and the Elsevier full-text host both blocked programmatic access).

## Stated limitations
The comment bounds its own critique rather than claiming the original findings are wrong: it states the recommended checks would 'further strengthen the study's operational credibility without changing its overall contribution as a pragmatic demonstration' — i.e., the four points are framed as robustness/validation gaps, not refutations. No further self-stated limitations of the comment itself are visible in the retrieved text, because only the abstract could be accessed; the full body (which may contain additional caveats) was not retrievable.

## Tensions with other findings
This source is itself a direct, peer-reviewed methodological rebuttal of Recknagel et al. (2025)'s Water Research paper on ML-based early warning of cyanobacteria blooms in Lake Müggelsee: it argues the original paper's reported forecasting skill may be inflated by (i) temporal leakage from interpolating weekly biovolume to hourly/daily resolution, (ii) reliance on R2/RMSE instead of threshold/event-based metrics at the operational hazard level, (iii) unquantified dependence on a single sensor variable (phycocyanin) absent a persistence baseline or ablation test, and (iv) mismatched spatial aggregation between single-station predictors and multi-station/depth-integrated targets. This closely parallels — and provides independent, current (2026) peer-reviewed support for — the HAB_PoC project's own non-negotiable operating principles (hunt leakage, always report a baseline and uncertainty, prefer event/threshold-based skill metrics for actionable HAB decisions over raw R2/RMSE, and quantify how much apparent skill is attributable to a single input via ablation). It is a useful illustration that reviewers in this exact sub-field treat strong R2/RMSE results on ML cyanobacteria forecasts as insufficient without these specific robustness checks — a caution directly applicable to any HAB model this project builds.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The abstract's opening caveat that these methodological choices 'may overstate actionable early-warning skill if not accompanied by robustness checks' is implicit in the conditional language of the individual claims but not made explicit as an umbrella premise.
- **Reviewer notes:** All six claims are directly supported by verbatim or near-verbatim passages from the published abstract. No numerical hallucinations detected. The extracted claims faithfully represent the structure and substance of the Comment paper's four-point critique and concluding recommendations. The only minor caveat: the abstract frames these concerns as conditional (four choices that 'may overstate' skill), but this conditional framing is reasonably conveyed through the use of modal verbs ('can introduce,' 'can bias') in the individual claim points."

## Provenance
- Canonical URL: https://linkinghub.elsevier.com/retrieve/pii/S0043135426000886
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: WebFetch on the given primary URL (ScienceDirect abs page) failed with HTTP 403 Forbidden. WebSearch located the DOI (10.1016/j.watres.2026.125406) and confirmed the paper identity/PII match. Following the DOI redirect led to an Elsevier linkinghub page that only rendered a client-side 'Redirecting' stub (no extractable content) — so the ScienceDirect/Elsevier full text could not be read at all, and full_text_access is capped at 'abstract'. I obtained the complete, verbatim published abstract via the Semantic Scholar Graph API (paper lookup by DOI, requesting the raw 'abstract' field), and independently corroborated the same distinctive wording via PubMed (PMID 41619426) and the Europe PMC REST API for the same PMID — three independent tools returning matching distinctive phrases, which gives confidence this is the genuine abstract and not a hallucination. No freely available full-text copy (preprint, ResearchGate, institutional repository) of the comment body was found via WebSearch, so anything beyond the abstract (e.g., any additional numbers, tables, or extended argument in the comment's body) is NOT reflected in this dossier entry. fetch_status is set to 'partial' to reflect that: bibliographic metadata and full abstract are solid and cross-validated, but the full text of this short comment was not accessible.
