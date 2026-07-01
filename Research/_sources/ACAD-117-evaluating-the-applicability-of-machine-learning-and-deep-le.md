---
key: ACAD-117
title: Evaluating the applicability of machine learning and deep learning models for predicting cyanobacterial alert levels in a drinking water reservoir
authors_or_org: Seohyun Byeon (Korea Environment Institute, Sejong); Hankyu Lee (Konkuk University, Seoul) [one metadata source renders this name "Han-Saeng Lee" — discrepancy unresolved]; Jae-Ki Shin (Konkuk University & Hannam University); Sang-Soo Baek (Yeungnam University, Gyeongsan); Soon-Jin Hwang (Konkuk University, Seoul); Jin Hwi Kim (corresponding author, Korea University, Seoul); Yongeun Park (corresponding author, Konkuk University, Seoul)
year: 2025
url: https://www.sciencedirect.com/science/article/abs/pii/S2214714425007573 (confirmed identical target via DOI 10.1016/j.jwpe.2025.107685 → https://linkinghub.elsevier.com/retrieve/pii/S2214714425007573)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (paywalled), Journal of Water Process Engineering, Vol. 73, article 107685
categories: [models-and-methods]
relevance: Medium
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Evaluating the applicability of machine learning and deep learning models for predicting cyanobacterial alert levels in a drinking water reservoir

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/abs/pii/S2214714425007573

**What it is.** A 2025 Journal of Water Process Engineering paper (Byeon, Lee, Shin, Baek, Hwang, Kim &amp; Park) that builds and compares three predictive model families — 1D-CNN, ANN, and an ensemble (random forest + boosting) — to make short-term/early predictions of cyanobacterial ("algal") alert levels in a South Korean drinking-water reservoir, using meteorological, hydrodynamic, and water-quality data as inputs on a "small-scale" (approx. nine-year) dataset.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study constructs and compares three model types — 1D-CNN, ANN, and an ensemble of random forest + boosting — to predict short-term cyanobacterial alert levels in a drinking-water reservoir from a small-scale dataset of meteorological, hydrodynamic, and water-quality variables.
  - *evidence:* This description recurred, in closely matching wording, across multiple independent WebSearch retrievals of the article's highlights/abstract content, which is the only content I could access (direct fetch of the ScienceDirect page returned HTTP 403 three times). (Highlights/Abstract (exact section unconfirmed — full text not accessible))
  - *quote:* "An ANN (Artificial Neural Network), ensemble models, and 1D-CNN (one-dimensional Convolutional Neural Network) were constructed using small-scale datasets."
- **[✓ verified]** The ensemble model (random forest + boosting) achieved the highest accuracy of the three approaches: 84.7% (training) and 78.7% (testing), versus 72.6%/77.0% for 1D-CNN and 79.0%/73.8% for ANN.
  - *evidence:* This exact six-number sentence recurred nearly verbatim across independent search retrievals not all of which I had seeded with the full set of numbers, and the ensemble figures (84.7%/78.7%) were independently corroborated by a separate WebFetch of a Google Scholar summary of the same paper. (Abstract/results summary (exact section/page unconfirmed — full text not accessible))
  - *quote:* "The optimal accuracies of prediction performance in the 1D-CNN, ANN, and ensemble models were 72.6%, 79.0%, and 84.7%, respectively, in the training step and 77.0%, 73.8%, and 78.7% in the testing step."
- **[✓ verified]** The ensemble model outperformed both deep-learning models (1D-CNN, ANN) overall and was selected by the authors as the optimal model for predicting algal alert levels.
  - *evidence:* Stated directly in a WebSearch synthesis of the paper's reported conclusion, consistent with the accuracy figures in the prior claim. (Abstract/Conclusion (as indexed; exact section unconfirmed))
  - *quote:* "The ensemble model outperformed 1D-CNN and ANN in terms of overall accuracy and was selected as the optimal model for the prediction of algal alert levels."
- **[✓ verified]** Water temperature was identified as the most influential predictor of algal alert level in the model(s), with nitrogen-related water-quality variables also ranking as relatively important contributors (an association/importance finding from model explainability analysis, not a claim of causation).
  - *evidence:* The temperature+nitrogen finding recurred in nearly every independent search retrieval of this paper; the specific attribution to a SHAP analysis appeared in one retrieval only and could not be independently re-confirmed. (Highlights/Results (as indexed; exact section unconfirmed))
  - *quote:* "Temperature was found to be the most influential factor through SHAP model analysis, and water quality variables related to nitrogen exhibited relatively high contributions."
- **[✓ verified]** The models were trained on roughly nine years of meteorological, hydrodynamic, and water-quality monitoring data from the studied reservoir (a 'small-scale' dataset by the authors' own framing).
  - *evidence:* "Nine years" recurred in two independent, otherwise-clean search retrievals; one later retrieval said "10 years" but appeared in a passage that also mixed in content (resampling vs. feature-selection comparison) that looks like it bled over from a related 2023 companion paper by overlapping authors, so I treat 'nine years' as more likely correct but not fully certain. (Methods/data description (as indexed; exact section unconfirmed))
  - *quote:* "using nine years of water quality, hydrological, and meteorological data from a reservoir"
- **[✓ verified]** The authors frame their central research question as whether ML/DL models remain feasible and useful predictive tools when the available input data are limited in scope, rather than assuming an ideal, large dataset.
  - *evidence:* This framing recurred across several independent retrievals in closely similar wording, suggesting it reflects the paper's own stated rationale/objective. (Abstract (objective statement, as indexed; exact section unconfirmed))
  - *quote:* "the feasibility of machine learning and deep learning models in utilizing limited input datasets and managing model complexities for predicting early warnings of harmful cyanobacterial blooms"
- **[✓ verified]** The authors propose that the resulting model can be used operationally within a cyanobacterial early-warning system for the reservoir.
  - *evidence:* Recurred as a closing highlight-style statement across multiple independent retrievals. (Highlights (concluding bullet, as indexed; exact section unconfirmed))
  - *quote:* "The model developed in this study can be utilized in cyanobacterial early warning systems."

## Data / numbers
- 72.6% — 1D-CNN training-step alert-level prediction accuracy
- 79.0% — ANN training-step alert-level prediction accuracy
- 84.7% — ensemble (random forest + boosting) training-step alert-level prediction accuracy (best of the three)
- 77.0% — 1D-CNN testing-step alert-level prediction accuracy
- 73.8% — ANN testing-step alert-level prediction accuracy
- 78.7% — ensemble model testing-step alert-level prediction accuracy (best of the three)
- ~9 years — length of meteorological/hydrodynamic/water-quality dataset used (one lower-confidence retrieval said 10 years; unresolved discrepancy)
- Journal of Water Process Engineering, Volume 73, Article 107685 (2025); DOI 10.1016/j.jwpe.2025.107685
- No stated baseline model or uncertainty interval (e.g., CI) found for any of the above accuracies in the retrieved material

## Methods
Three model families were built and compared on the same small-scale, multi-year dataset: a one-dimensional convolutional neural network (1D-CNN), an artificial neural network (ANN), and an ensemble approach combining random forest and boosting. Inputs were meteorological, hydrodynamic, and water-quality variables; the target was the reservoir's short-term cyanobacterial/algal alert-level classification. Per the reconstructed abstract-level text, the ensemble model gave the best overall accuracy (84.7% train / 78.7% test) and was selected as the optimal model, beating both deep-learning architectures (1D-CNN: 72.6% train / 77.0% test; ANN: 79.0% train / 73.8% test). One retrieval attributes the identification of temperature and nitrogen-related variables as the top predictors to a SHAP-based explainability analysis. No remote-sensing/satellite input is mentioned anywhere in the retrieved material — the fusion here is meteorological + hydrodynamic + in-situ water quality only.

## Stated limitations
Full-text limitations/discussion sections could not be retrieved (paywalled; direct fetch blocked). The paper's own recurring framing of its goal — "evaluating the feasibility of machine learning and deep learning models in utilizing limited input datasets and managing model complexities" — signals that the authors treat working from a "small-scale" dataset (roughly nine, possibly ten, years of data from what appears to be a single, unnamed reservoir) as the central constraint/challenge of the study, which by construction limits generalizability beyond that site; this is my inference from the recurring framing language, not a verbatim "Limitations" section quote. No baseline model (e.g., majority-class or persistence baseline) or uncertainty interval around the reported accuracies appears in any of the retrieved text.

## Tensions with other findings
(1) The finding that a simpler ensemble of random forest + boosting matched or beat both deep-learning architectures (1D-CNN, ANN) on a small real-world ecological dataset is a concrete external data point supporting the "explainability/simplicity over sophistication" stance in this project's own operating principles. (2) Anomaly I noticed in the reconstructed numbers (not addressed in any retrieved source text): the 1D-CNN's reported test accuracy (77.0%) is higher than its training accuracy (72.6%), which is unusual for a well-behaved supervised classifier and would need verification against the primary text (possible causes could include a small/imbalanced test split, but this is speculation on my part, not sourced). (3) This source fuses meteorological + hydrodynamic + in-situ water-quality data only — it does NOT appear to include a remote-sensing/satellite signal, so it is relevant to this project chiefly as a modeling/framing precedent (DL-vs-ensemble comparison, alert-level classification target, temperature/nitrogen as top explanatory variables) rather than as a directly reusable remote-sensing+in-situ fusion pipeline. (4) During research I found and had to discard a set of much higher-performing metrics (R²=0.982 etc., attributed to a "FLAML" framework) and an incorrect journal name ("Environmental Research") that appeared in some search-engine syntheses but contradicted confirmed CrossRef/DOI metadata and are almost certainly conflated with a different paper on a similar topic — flagged here so a reviewer knows this contamination was identified and excluded, not overlooked.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All seven claims are directly supported by the source text as provided. The analyst's retrieval strategy was sound: when the primary ScienceDirect URL returned HTTP 403, they pivoted to multiple independent WebSearch and WebFetch queries, corroborated numbers across retrievals, and explicitly flagged and excluded unreliable conflations with a related 2023 companion paper. The six accuracy figures in Claim 2 are verbatim from Passage B. The analyst appropriately added a causation caveat to Claim 4 even though not strictly required. The only point of residual uncertainty is whether the dataset spans nine or ten years (the analyst notes one later retrieval said ten years but appeared conflated with a different paper); however, both consistent independent retrievals in the source text say nine years, and the claim uses the qualifier 'roughly,' which is appropriate. No hallucinated numbers, no dropped caveats from the paper content itself, and all claims align with the source passages."

## Provenance
- Canonical URL: https://www.sciencedirect.com/science/article/abs/pii/S2214714425007573 (confirmed identical target via DOI 10.1016/j.jwpe.2025.107685 → https://linkinghub.elsevier.com/retrieve/pii/S2214714425007573)
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Access was effectively paywalled: WebFetch to the primary ScienceDirect URL, its non-"/abs/" variant, and the DOI-redirect linkinghub URL all returned HTTP 403 Forbidden; web.archive.org was unreachable to this tool; Semantic Scholar and OpenAlex both confirm the correct paper via DOI/title match but both return a null abstract (Elsevier blocks abstract redistribution to most indexers, and no open-access PDF is registered — Semantic Scholar's openAccessPdf status is "CLOSED"). I therefore reconstructed abstract/highlights-level content via a large number of targeted WebSearch queries and cross-checked for internal consistency, keeping only claims/numbers that recurred consistently across independent, differently-worded queries, and explicitly discarding a cluster of specific-sounding but non-recurring/contradictory content (a "FLAML" result set with different R²/RMSE/MAPE figures, an incorrect journal name, and content that appears to belong to a related 2023 companion paper by overlapping authors) that I judged to be search-engine hallucination or cross-paper conflation rather than genuine content of ACAD-117. Because of this, I was not able to obtain: the reservoir's name/location, the exact number and thresholds of "alert level" classes used as the classification target, an explicit author-stated Limitations/Discussion section, or a fully certain figure for the length of the data record (nine vs. ten years, inconsistent across retrievals). Everything reported above should be treated as abstract/highlights-level confidence, reconstructed rather than directly read, and re-verified against the primary PDF/HTML if this source is to support any product claim.
