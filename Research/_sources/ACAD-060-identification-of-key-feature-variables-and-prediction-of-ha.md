---
key: ACAD-060
title: Identification of key feature variables and prediction of harmful algal blooms in a water diversion lake based on interpretable machine learning
authors_or_org: Yundong Wu, Bo Xian, Xiaowei Xiang, Fang Fang, Fuhao Chu, Xingkang Deng, Qing Hu, Xiuqiong Sun, Wei Tang, Shaopan Bao, Genbao Li, Tao Fang
year: 2025
url: https://www.sciencedirect.com/science/article/pii/S001393512500742X
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (Environmental Research, Elsevier), abstract-level access only
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Identification of key feature variables and prediction of harmful algal blooms in a water diversion lake based on interpretable machine learning

**What it is.** A 2025 Environmental Research article that builds an interpretable machine-learning pipeline (CatBoost benchmarked against 9 other ML models, explained with SHAP, plus a PLS-PM path analysis) to identify the key environmental drivers of harmful algal blooms (HABs) in Yilong Lake, a Chinese lake subject to an engineered water-diversion project, and to package the validated model into an operational tool for lake-management staff.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Among ten machine learning models benchmarked for predicting harmful algal blooms (HABs) in Yilong Lake, a CatBoost (gradient-boosted decision tree) model performed best, reaching an AUC of 0.948.
  - *evidence:* Reported as the headline predictive-performance result in the abstract-level text; no comparison metrics for the other nine models were retrievable from the accessible text. (Abstract)
  - *quote:* "The CatBoost model (AUC = 0.948) performed best among 10 machine learning models"
- **[⚠ partial]** Using SHAP-based interpretation/feature selection, the authors reduced an initial pool of 24 candidate environmental variables down to 8 identified as the key predictors of HAB occurrence, including total phosphorus (TP), total nitrogen (TN), and chemical oxygen demand (CODCr).
  - *evidence:* Stated directly as the feature-reduction/interpretability outcome in the abstract. (Abstract)
  - *quote:* "24 features reduced to 8 most important environmental features including TP, TN and CODCr"
  - *reviewer:* Feature reduction (24→8) and key features (TP, TN, CODCr) are confirmed in source. SHAP is confirmed as an interpretation method (global/local). However, the source does not explicitly state SHAP was used for feature selection/reduction itself—the two are mentioned separately. The mechanism linking SHAP to the feature selection process is inferred but not stated in source text.
- **[✓ verified]** SHAP (SHapley Additive exPlanations) was used to interpret the CatBoost model at two levels: a global interpretation summarizing overall feature importance across the model, and a local interpretation explaining individual sample-level predictions.
  - *evidence:* Describes the explainability-method architecture used; directly relevant to this literature review's interest in interpretable ML for HAB prediction. (Abstract)
  - *quote:* "the SHapley Additive explanation (SHAP) method was used to interpret the CatBoost model through global interpretation describing whole model features and local interpretation detailing forecasts for individual samples"
- **[✓ verified]** A Partial Least Squares Path Model (PLS-PM) analysis indicated that the water-diversion project's mitigating effect on HABs operates indirectly, primarily by diluting nutrient concentrations, rather than through some other direct pathway.
  - *evidence:* This is a statistical path/structural-equation association from observational monitoring data, not an experimental manipulation, so it should be read as a correlational pathway finding rather than a proven causal mechanism. (Abstract)
  - *quote:* "water diversion indirectly mitigates HABs mainly through diluting nutrient concentrations"
- **[✓ verified]** The modeling dataset spans 2008-2022: an external-validation dataset from three monitoring sites covering a non-water-diversion period (2008-2013) and a water-diversion period (2014-2020), plus a separate internal-validation dataset from six sampling sites covering 2021-2022.
  - *evidence:* Describes the temporal/spatial validation design distinguishing pre- and post-diversion regimes; this is a genuine out-of-period external validation split rather than a random shuffle, which is methodologically relevant to this review's leakage/validation concerns. (Abstract / Methods (as summarized by fetch))
  - *quote:* "three monitoring sites for 2008-2020 (non-water diversion period 2008-2013 and water diversion period 2014-2020) for external validation and six sampling sites for 2021-2022 for internal validation"
- **[⚠ partial]** The authors frame the core methodological challenge as follows: because water diversion itself alters the receiving lake's hydrodynamics and water environment, it becomes harder to identify which environmental features actually drive HAB occurrence, motivating their interpretable-ML approach.
  - *evidence:* Problem framing/motivation captured verbatim in a search-snippet quotation, apparently drawn from the abstract or introduction. (Abstract/Introduction (as summarized by search))
  - *quote:* "the inevitable changes of hydrodynamic and water environment in the receiving area during water diversion make it more challenging to identify the important environmental features of HABs"
  - *reviewer:* Source confirms the challenge: 'the inevitable changes of hydrodynamic and water environment... make it more challenging to identify the important environmental features of HABs.' Source also reports that interpretable ML (CatBoost + SHAP) was used. However, source text does not explicitly frame this challenge as the stated motivation for the methodological choice. The causal/motivational connection is a reasonable inference but not explicitly stated in source.
- **[✓ verified]** The validated CatBoost + SHAP model was translated into a practical, deployable application intended for use by non-research lake-management staff, specifically personnel of the Bureau of Yilong Lake Administration.
  - *evidence:* Deployment/translation-to-practice claim; loosely corroborated by author-affiliation metadata indicating a co-author (Xiuqiong Sun) is affiliated with the Bureau of Yilong Lake Administration, consistent with a real operational handoff. (Abstract)
  - *quote:* "converted into a convenient application for use by the Bureau of Yilong Lake Administration personnel and researchers"

## Data / numbers
- AUC = 0.948 (CatBoost model; best of 10 ML models compared; unitless metric, range 0-1)
- 24 candidate environmental features reduced to 8 key features (feature count, no units)
- Overall data span: 2008-2022 (15 years)
- External validation: 3 monitoring sites, split into non-water-diversion period 2008-2013 and water-diversion period 2014-2020
- Internal validation: 6 sampling sites, period 2021-2022
- 10 machine learning models compared (count)
- Journal citation: Environmental Research, Volume 276, article no. 121491 (2025); DOI 10.1016/j.envres.2025.121491; PMID 40158870; published online 1 July 2025 (Epub 28 March 2025)

## Methods
Ten machine learning algorithms were benchmarked for predicting HAB occurrence in Yilong Lake using environmental/water-quality monitoring data spanning 2008-2022. Data were split by regime and site count: three monitoring sites for 2008-2020 (subdivided into non-water-diversion 2008-2013 and water-diversion 2014-2020) used for external validation, and six sampling sites for 2021-2022 used for internal validation. CatBoost (a gradient-boosted decision-tree method) was reported as the best performer (AUC = 0.948). SHAP (SHapley Additive exPlanations) was applied to the CatBoost model for both global (whole-model) feature-importance interpretation and local (per-sample) explanation, narrowing 24 candidate environmental features to 8 judged most important (including TP, TN, and CODCr). A Partial Least Squares Path Model (PLS-PM) was additionally used to test indirect pathways, concluding water diversion mitigates HABs mainly by diluting nutrient concentrations. The validated model was packaged into an application for Bureau of Yilong Lake Administration personnel. IMPORTANT GAP: the abstract-level text accessible for this dossier does not name the other 9 benchmarked algorithms or their individual metrics, does not state the operational definition/threshold used to label a "HAB event" (the use of AUC implies a binary classification framing, but the class-definition threshold, e.g. a chlorophyll-a cutoff, was not stated in the retrievable text), and contains no mention of satellite or remote-sensing data — the described "environmental features" appear to be in-situ monitoring-station variables, but this could not be confirmed from the Methods section since it was not accessible.

## Stated limitations
No explicit "limitations" language could be retrieved: only abstract-level text was accessible (ScienceDirect returned HTTP 403 on the primary URL, the DOI-redirect target, and the abstract-only ScienceDirect page across two direct WebFetch attempts plus a follow-up attempt on the linkinghub redirect target), and no PMC, preprint, or other open-access full-text mirror could be located via WebSearch. Consequently, any caveats the authors themselves state in a Discussion/Limitations section (e.g., single-lake generalizability, sensitivity to feature selection, sampling gaps, or model-transfer concerns) are unknown and are NOT asserted here. Separately, no baseline model (e.g., a naive/persistence/climatology comparator) or uncertainty estimate (confidence interval, standard deviation) for the reported AUC = 0.948 was present in any of the accessible text.

## Tensions with other findings
(1) This source's identified key drivers are conventional in-situ nutrient/chemistry variables (TP, TN, CODCr) rather than a fused remote-sensing/satellite signal; as retrieved, there is no mention of satellite, Sentinel, Landsat, or chlorophyll-a remote sensing, which contrasts with this project's mandate to fuse a remote-sensing signal with in-situ data (CLAUDE.md) and with other reviewed sources built around EPA CyAN or similar satellite products. (2) The study is single-lake (Yilong Lake, China) and specific to an engineered inter-basin water-diversion context, which may limit transferability to U.S. lakes without comparable diversion infrastructure (the project's sanctioned sources are U.S.-centric: EPA CyAN, WQP, USGS NWIS). (3) The PLS-PM finding that water diversion mitigates HABs "mainly through diluting nutrient concentrations" is a path/structural-equation association from observational monitoring data, not a controlled experiment, so it should be treated as correlational evidence about a plausible mechanism rather than proven causation. (4) Because the exact HAB-event definition/threshold underlying the AUC=0.948 classification metric was not accessible, this number cannot yet be directly compared against other reviewed sources' skill metrics (which may use different thresholds, e.g., WHO chlorophyll-a bands) without the full Methods text.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Full-text access to the paper was blocked (HTTP 403 on ScienceDirect, DOI redirect, and abstract-only endpoints per source's 'ACCESS FAILURES' note). All claims rest on abstracts and web-aggregated search snippets, not the complete published paper. This access limitation should be flagged when presenting these findings.
- **Reviewer notes:** No claims scored 'no' and no hallucinated numbers were detected, warranting a PASS verdict. Two claims (2 and 6) are marked PARTIAL because they make defensible but not explicitly-stated inferences: Claim 2 attributes the feature reduction to SHAP without explicit source confirmation of that causal link; Claim 6 frames the hydrodynamic challenge as the stated motivation for the ML approach when source only documents that both the challenge and solution exist. All numeric results (AUC, model count, feature counts, dates, site counts) are confirmed in source text. Critical caveat: the full paper is inaccessible due to publisher restrictions; all verification relies on abstracts and search-aggregated snippets, which may omit methodological or interpretive detail present in the full text."

## Provenance
- Canonical URL: https://www.sciencedirect.com/science/article/pii/S001393512500742X
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Fetch protocol actually executed: WebFetch was called on the primary ScienceDirect URL twice with two different comprehensive extraction prompts (per HIGH-relevance instructions), and both calls returned HTTP 403 Forbidden with no body content — ScienceDirect blocks unauthenticated automated fetches. Per Step 2, I then used WebSearch to locate an alternative accessible version, which surfaced a PubMed record (PMID 40158870) with the full structured abstract; I WebFetched that PubMed page directly and obtained a complete abstract plus bibliographic metadata (journal, volume/pages, DOI, epub/print dates, full author list). To reconcile/triangulate (in place of a second successful full-text fetch, since the primary source itself was unreachable), I also: (a) WebFetched the DOI link, which redirected to the Elsevier linkinghub retrieval URL and yielded only an empty 'Redirecting' page; (b) WebFetched the ScienceDirect abstract-only page (also 403); (c) WebFetched the Semantic Scholar Graph API record for this DOI, which independently returned a consistent abstract summary; (d) ran five WebSearch queries, whose snippet aggregations (evidently drawing on the same ScienceDirect abstract/highlights) independently corroborated every key number (AUC 0.948, 24-to-8 features, TP/TN/CODCr, SHAP global+local, PLS-PM dilution pathway, 3 sites/2008-2020 external vs. 6 sites/2021-2022 internal, and the operational-application deployment claim) with no contradictions across sources. I judge this convergence across five independently-sourced retrievals sufficient to trust the abstract content as accurately representing the paper's abstract, even though I never obtained the ScienceDirect-hosted full text itself. No Methods/Results/Discussion body text, no per-model comparison table for the other 9 algorithms, no explicit HAB-classification threshold/definition, and no explicit author-stated Limitations section were ever retrieved — full_text_access is therefore set to 'abstract' and fetch_status to 'partial' (meaningful, corroborated information was obtained, but the comprehensive full-text extraction requested in Step 1 was not achieved). No training-data knowledge of this specific paper was used; every fact above is attributed to a specific tool call recorded in source_extract.
