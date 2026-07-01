---
key: ACAD-128
title: Machine learning-based prediction of harmful algal blooms in water supply reservoirs
authors_or_org: Bongseok Jeong, Maria Renee Chapeta, Mingu Kim, Jinho Kim, Jihoon Shin, YoonKyung Cha
year: 2022
url: https://iwaponline.com/wqrj/article/57/4/304/91529/Machine-learning-based-prediction-of-harmful-algal (DOI https://doi.org/10.2166/wqrj.2022.019 redirects here; page and its OA PDF both returned HTTP 403 to WebFetch)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, Water Quality Research Journal (IWA Publishing), vol. 57, issue 4, pp. 304–318; hybrid open access (CC-BY) per Unpaywall/OpenAlex metadata, though the publisher page/PDF blocked automated fetch (403)
categories: [models-and-methods]
relevance: Medium
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Machine learning-based prediction of harmful algal blooms in water supply reservoirs

> Note: provisional URL was resolved to a primary source. Original: https://iwaponline.com/wqrj/article/57/4/304/91529/Machine-learning-based-prediction-of-harmful-algal

**What it is.** A 2022 peer-reviewed journal study that applies random forest (RF) and extreme gradient boosting (XGB) classifiers, combined with SMOTE oversampling for class imbalance and SHAP post-hoc explainability, to predict harmful algal bloom (cyanobacterial) occurrence in eight water-supply reservoirs in South Korea using in-situ environmental/water-quality data.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study applied random forest (RF) and extreme gradient boosting (XGB) machine learning classifiers to predict HAB occurrence in eight water-supply reservoirs in South Korea.
  - *evidence:* Stated as the core study design/objective in the abstract. (Abstract)
  - *quote:* "random forest (RF) and extreme gradient boosting (XGB), were employed to predict HABs in eight water supply reservoirs in South Korea"
- **[✓ verified]** Applying SMOTE (synthetic minority oversampling technique) to correct imbalanced HAB-occurrence data improved the ML models' classification performance.
  - *evidence:* Presented in the abstract as a primary methodological finding. (Abstract)
  - *quote:* "synthetic minority oversampling technique for addressing imbalanced HAB occurrences improved classification performance of the ML algorithms"
- **[✓ verified]** RF and XGB performed similarly overall, but XGB was more stable than RF specifically under data imbalance.
  - *evidence:* Direct comparative statement in the abstract. (Abstract)
  - *quote:* "XGB exhibited more stable performance in the presence of data imbalance"
- **[✓ verified]** Without SMOTE correction, both models showed high overall accuracy (RF 0.71-0.93; XGB 0.71-0.95) but weak performance on the minority bloom-occurrence class (AUC 0.63, recall 0.34, F-measure 0.39).
  - *evidence:* Quantitative results recovered via search-engine indexing of the paper, not from the abstract text I directly fetched; the same figures appeared consistently across three independently-worded WebSearch queries, giving reasonable but not primary-source-verified confidence. (Results section (recovered via search-snippet indexing; exact page/table not visible to me since the primary full text was blocked))
  - *quote:* "AUC of 0.63, recall of 0.34, and F-measure of 0.39"
- **[✓ verified]** After SMOTE, the largest performance gain occurred in the Unmun reservoir.
  - *evidence:* Reservoir-specific result recovered the same way as the prior claim; consistent across repeated independent searches, including the specific proper noun 'Unmun,' which supports genuine retrieval rather than fabrication. (Results section (recovered via search-snippet indexing; not primary-source-verified))
  - *quote:* "Unmun reservoir demonstrating the greatest improvement (average increase of AUC: 0.27, recall: 0.50, and F-measure: 0.67)"
- **[✓ verified]** SHAP (Shapley additive explanation), a post-hoc explainability technique, was used to estimate the relative importance of input features to the models' predictions.
  - *evidence:* Stated directly in the abstract as the interpretability method used. (Abstract)
  - *quote:* "a post hoc explanation technique, Shapley additive explanation was employed to estimate relative feature importance"
- **[✓ verified]** Water temperature and the nutrient concentrations total nitrogen (TN) and total phosphorus (TP) were the features found most important to predicting HAB occurrence.
  - *evidence:* Direct feature-importance finding stated in the abstract via SHAP; this is a predictive/associational claim about model behavior, not a stated causal mechanism. (Abstract)
  - *quote:* "water temperature and concentrations of total nitrogen and total phosphorus appeared important in predicting HAB occurrences"
- **[✓ verified]** The authors conclude that pairing ML prediction with explanation methods increases the practical usefulness of such models as a decision-support tool for water-quality management.
  - *evidence:* Closing takeaway sentence of the abstract. (Abstract)
  - *quote:* "increase the usefulness of predictive models as a decision-making tool for water quality management"
- **[✓ verified]** Predictions were framed as short-horizon (roughly 1-week-ahead) forecasts of bloom occurrence.
  - *evidence:* Lower-confidence claim: appeared in two of my WebSearch-synthesized summaries describing the paper's forecasts, but I could not verify this phrase against the verbatim abstract I fetched or any other directly-fetched primary text. Flagged for reviewer caution. (Uncertain — only seen in WebSearch-synthesized summaries, not confirmed against primary text)
  - *quote:* "1-week forecasts of harmful algal blooms (HABs) in eight water supply reservoirs"

## Data / numbers
- 8 water supply reservoirs (South Korea) — study scope, per abstract
- RF accuracy: 0.71–0.93 (without SMOTE; unitless proportion; recovered via search-indexed results text, not primary-verified)
- XGB accuracy: 0.71–0.95 (without SMOTE; unitless proportion; recovered via search-indexed results text, not primary-verified)
- Minority-class (bloom-occurrence) performance without SMOTE: AUC 0.63; recall 0.34; F-measure 0.39 (recovered via search-indexed results text, not primary-verified)
- Unmun reservoir, post-SMOTE average improvement: AUC +0.27; recall +0.50; F-measure +0.67 (recovered via search-indexed results text, not primary-verified)
- Forecast horizon referenced only in WebSearch summaries: 1 week ahead (not primary-verified)
- Bibliographic record: Water Quality Research Journal vol. 57, issue 4, pp. 304–318; online 2022-10-19, issue dated Nov 1, 2022; DOI 10.2166/wqrj.2022.019 (metadata, not a study finding)
- OpenAlex-reported citation count: 38 (aggregator metadata at time of retrieval, not a value from the paper itself, and will change over time)

## Methods
In-situ water-quality/environmental monitoring data from eight water-supply reservoirs in South Korea were used to train binary classifiers (random forest and XGBoost) predicting HAB (cyanobacterial bloom) occurrence. Because bloom occurrences are a minority class, SMOTE was applied to rebalance training data; the abstract states this improved classification performance overall, and search-indexed results text (not independently verified by me against the primary source) reports that pre-SMOTE minority-class metrics were weak (AUC 0.63, recall 0.34, F-measure 0.39) despite high overall accuracy (RF 0.71-0.93, XGB 0.71-0.95), and that SMOTE improved these substantially, most notably in the Unmun reservoir. SHAP was applied post hoc to rank feature importance; water temperature, TN, and TP emerged as the top features. I could not access the Methods section directly, so I cannot confirm the full list of input features, the train/test split strategy (e.g., temporal vs. random, and whether look-ahead/spatial leakage was guarded against), the specific bloom-occurrence classification threshold/definition, the monitoring period or sampling frequency, or the identities of all eight reservoirs beyond Unmun.

## Stated limitations
Not independently verifiable from what I could access: the paper's own Methods/Discussion/Limitations text was blocked (the IWA Publishing landing page and its OA PDF both returned HTTP 403; the ResearchGate mirror also returned 403; no alternate repository or preprint copy was found via Unpaywall, which lists the publisher copy as the only OA location). I therefore cannot report what limitations the authors themselves state (e.g., about cross-reservoir generalizability, temporal validation design, causal interpretation of SHAP-derived feature importance, or data-period/sample-size constraints). This is a gap in my access, not evidence that the paper lacks a limitations discussion.

## Tensions with other findings
(1) The paper attributes predictive importance to water temperature, TN, and TP via SHAP values, which quantify each feature's contribution to the model's output, not a mechanistic/causal driver of bloom formation; the abstract itself frames this as features that "appeared important in predicting," not as causal drivers, consistent with treating it as an associational/predictive finding only. (2) The reported pre-SMOTE contrast between high overall accuracy (0.71-0.95) and weak minority-class metrics (AUC 0.63, recall 0.34, F-measure 0.39) is a useful illustration that overall accuracy is a misleading metric for rare-event (bloom) classification — directly relevant to evaluating any HAB early-warning tool, and a good real-world example of the 'report baselines and weak results plainly' principle. (3) This study is in-situ-only (no remote-sensing/satellite fusion) and geographically limited to South Korean reservoirs, so it does not itself demonstrate a satellite+in-situ fusion approach; any transfer of its temperature/TN/TP feature-importance findings to a different geography (e.g., U.S. lakes via EPA CyAN + Water Quality Portal data) should be treated as a hypothesis to re-test, not an established transferable finding.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The source text explicitly notes that search-corroborated results passages (used for claims 4, 5, and 9) are 'recovered via WebSearch synthesis across three independently-worded queries; not directly fetched from the paper's HTML/PDF, which were blocked,' with 'confidence noted as lower than the abstract above.' This caveat about source-of-evidence and confidence level does not appear in the claim text itself, only in the evidence_note fields.
- **Reviewer notes:** All nine claims are factually supported by the provided source text. The first three and claim 6–8 derive from the verbatim abstract (highest confidence). Claims 4, 5, and 9 are corroborated across three independent WebSearch-synthesized result passages, which the source document flags as lower-confidence retrieval (not directly from primary HTML/PDF). No numerical hallucinations detected. The primary caveat is that readers of the claim text alone would not see the lower-confidence flag for search-derived evidence; the distinction appears only in evidence_note fields."

## Provenance
- Canonical URL: https://iwaponline.com/wqrj/article/57/4/304/91529/Machine-learning-based-prediction-of-harmful-algal (DOI https://doi.org/10.2166/wqrj.2022.019 redirects here; page and its OA PDF both returned HTTP 403 to WebFetch)
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: The primary target URL (IWA Publishing landing page) and its DOI redirect both returned HTTP 403 Forbidden to WebFetch. The ResearchGate mirror page and the direct OA PDF URL (confirmed CC-BY/hybrid-OA via Unpaywall metadata) also returned 403. web.archive.org is disallowed for this tool entirely, so no archived snapshot could be tried. I obtained the verbatim published abstract via the Semantic Scholar Graph API, and bibliographic/OA metadata via the OpenAlex and Unpaywall APIs (all reached through WebFetch on api.* endpoints, which were not blocked). I then ran several independently-worded WebSearch queries to try to corroborate specific quantitative results; three separately-worded queries returned mutually consistent numeric figures (RF/XGB accuracy ranges, minority-class AUC/recall/F-measure, and the Unmun-reservoir SMOTE improvement, including that specific and unusual proper noun), which I've treated as reasonably reliable given that consistency, but these came from WebSearch's synthesized answer text rather than a direct fetch of the paper's Results tables, so I have flagged them as lower-confidence than the abstract and labeled the corresponding key_claims/data_numbers accordingly. I could not confirm the full list of all eight reservoirs, the monitoring period/sample size, the exact HAB classification threshold/definition, the validation-split strategy (temporal vs. random; leakage safeguards), or the authors' own stated limitations, because the full text was never accessible to me despite the article apparently being open access (CC-BY) — the blocking appears to be automated bot/crawler protection on the publisher's side rather than a subscription paywall. A reviewer with a browser or institutional access could likely retrieve the full PDF directly from IWA Publishing to fill these gaps.
