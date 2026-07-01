---
key: ACAD-068
title: Machine Learning Approaches for Harmful Algal Bloom Prediction: Advances, Challenges, and Future Directions
authors_or_org: Nasrin Alamdari (Dept. of Civil & Environmental Engineering, FAMU-FSU College of Engineering, Florida State University; ORCID 0000-0003-4102-6613)
year: 2026
url: https://ascelibrary.org/doi/10.1061/JOEEDU.EEENG-8732
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal review article (Journal of Environmental Engineering, American Society of Civil Engineers)
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Machine Learning Approaches for Harmful Algal Bloom Prediction: Advances, Challenges, and Future Directions

**What it is.** A peer-reviewed review article (J. Environmental Engineering, Vol. 152, No. 8, article 03126007, published online 2026-05-29) by Nasrin Alamdari (Florida State University) that synthesizes 168 peer-reviewed studies (1997–2025) on machine-learning approaches to harmful algal bloom (HAB) prediction, surveying traditional ML, deep learning, and hybrid process-based/ML methods, and outlining field-wide challenges and future research priorities, including a link to nutrient/TMDL management applications.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The review frames HABs as causing an estimated $50 million in economic losses annually in the U.S. alone, in addition to public-health (toxin exposure) and ecosystem impacts, as motivation for ML-based prediction.
  - *evidence:* Opening motivating statistic in the abstract; no citation, error bar, or estimation methodology is given for this figure within the retrievable abstract text. (Abstract)
  - *quote:* "economic losses estimated at $50 million annually in the United States alone"
- **[✓ verified]** The paper is a literature-synthesis review covering 168 peer-reviewed studies on ML-based HAB prediction published between 1997 and 2025.
  - *evidence:* States the review's scope/method directly. (Abstract)
  - *quote:* "synthesizes findings from 168 peer-reviewed studies published between 1997 and 2025"
- **[✓ verified]** The review's scope spans traditional ML (random forest, SVM, gradient boosting) through deep learning (LSTM, CNN, transformer) and hybrid process-based/ML models.
  - *evidence:* Abstract enumerates the model families analyzed across the 168 studies. (Abstract)
  - *quote:* "random forest, support vector machines, and gradient boosting methods to advanced deep learning architectures such as long short-term memory (LSTM) networks, convolutional neural networks, and emerging transformer models"
- **[✓ verified]** Across the reviewed literature, deep learning models (particularly LSTM-based) showed the strongest reported performance: median R2 of 0.89 and accuracy exceeding 90% in many applications.
  - *evidence:* Presented as an aggregate cross-study finding; the abstract gives no variance/spread beyond 'median', no count of how many of the 168 studies this spans, and no statement of validation scheme (e.g., temporal vs. spatial vs. random holdout). (Abstract)
  - *quote:* "median R2 values of 0.89 and accuracies exceeding 90% in many applications"
- **[✓ verified]** Hybrid process-based + ML models were reported as the highest-accuracy approach among reviewed studies, reaching a Nash-Sutcliffe efficiency (NSE) of 0.991.
  - *evidence:* Stated as a cross-study finding; no indication of how many studies used hybrid models or the spread of NSE values. (Abstract)
  - *quote:* "Nash–Sutcliffe efficiency values reaching 0.991"
- **[✓ verified]** The review identifies persistent field-wide gaps despite ML advances: limited model transferability across water bodies, data scarcity/class imbalance, low explainable-AI (XAI) uptake (only 20% of the 168 studies), and a gap between research models and deployed operational early-warning systems.
  - *evidence:* Presented as the review's own synthesis of remaining challenges in the literature it surveyed. (Abstract)
  - *quote:* "insufficient adoption of explainable AI techniques (only 20% of studies)"
- **[✓ verified]** The review sets out future research priorities: SHAP/attention-based interpretability, incorporating climate-change projections, transfer-learning frameworks for data-limited systems, and standardized benchmark datasets.
  - *evidence:* Stated directly as the review's recommended priorities. (Abstract)
  - *quote:* "enhanced interpretability through SHAP and attention mechanisms"
- **[✓ verified]** The review connects ML-based HAB prediction to regulatory/management use, specifically total maximum daily load (TMDL) development and compliance, nutrient load allocation, and scenario analysis for HAB-impaired waters.
  - *evidence:* A distinct scope element beyond pure prediction-accuracy benchmarking, applying ML to a nutrient-management/regulatory context. (Abstract)
  - *quote:* "application of ML approaches to total maximum daily load development and compliance"
- **[✓ verified]** The review frames rising HAB frequency/intensity as linked to climate change and anthropogenic nutrient loading, motivating demand for prediction systems.
  - *evidence:* This is the source's own introductory framing/attribution of drivers, not a causal analysis demonstrated within the retrievable abstract text; treated here as a stated association, not an established causal result. (Abstract)
  - *quote:* "exacerbated by climate change and anthropogenic nutrient loading"

## Data / numbers
- $50 million/year — estimated U.S. economic losses attributed to HABs (no uncertainty/CI stated in abstract)
- 168 peer-reviewed studies synthesized, spanning publication years 1997–2025 (28-year window)
- Median R² = 0.89 for LSTM-based deep learning models (cross-study median per abstract; no spread/CI given)
- >90% accuracy reported for deep learning models 'in many applications' (exact metric definition and denominator not specified in the abstract)
- Nash–Sutcliffe efficiency (NSE) up to 0.991 for hybrid process-based + ML models (no spread/CI given)
- 20% — share of the 168 reviewed studies reported to use explainable AI (XAI) techniques
- Bibliographic: J. Environmental Engineering Vol. 152, Issue 8, article no. 03126007; DOI 10.1061/JOEEDU.EEENG-8732
- 101 referenced works per OpenAlex vs. 117 references per CrossRef metadata for the same article (source metadata disagree slightly; both are bibliographic counts, not findings of the paper)
- Publication date 2026-05-29 per OpenAlex vs. issue date 'August 1, 2026' per CrossRef (bibliographic metadata, not article content)

## Methods
The article is a literature-synthesis review (not a primary empirical/modeling study), covering 168 peer-reviewed studies (1997-2025) on ML-based HAB prediction. Per the abstract, it analyzes "the full spectrum of ML approaches": traditional algorithms (random forest, support vector machines, gradient boosting), deep learning architectures (LSTM, CNN, transformer models), and hybrid process-based+ML models; it separately reviews applications of these methods to total maximum daily load (TMDL) nutrient-management contexts (informing nutrient load allocations, scenario analysis, monitoring for HAB-impaired waters). Per the abstract, deep learning (especially LSTM-based) models and hybrid process-based+ML models show the strongest reported performance (highest R2/accuracy/NSE) in the reviewed literature, while models in general are reported to struggle with transferability across different water bodies. The abstract does not describe the review's own search strategy, database coverage, inclusion/exclusion criteria, or how it aggregated "median" performance statistics across heterogeneous study designs; that methodological detail would require the paper's full text, which was not accessible (see fetch_notes).

## Stated limitations
Only the abstract was accessible, so limitations here are the field-level challenges the review itself states remain open (the fuller discussion is presumably in the body text, not accessible): (1) limited ML model transferability across different water bodies; (2) data scarcity and class imbalance in HAB datasets; (3) low adoption of explainable AI methods across the literature (only 20% of the 168 reviewed studies); (4) a persistent gap between research-grade models and deployed, operational early-warning systems. The abstract does not disclose the review's own methodological limitations (e.g., search strategy/database coverage, inclusion criteria, publication-bias handling, or exactly how "median R2"/accuracy/NSE figures were aggregated across the 168 heterogeneous studies) — assessing those would require the full text, which could not be obtained.

## Tensions with other findings
The headline cross-study metrics (median R2=0.89; >90% accuracy; NSE up to 0.991) are aggregated over 168 studies of unstated methodological consistency; the review's own statement that models show "limited... transferability across water bodies" suggests these in-study performance figures may not generalize out-of-sample or out-of-lake — a caution relevant to treating any single HAB-ML accuracy figure from this literature as a general benchmark. Separately, the finding that only 20% of the 168 studies use explainable AI sits in tension with an explainability-first modeling philosophy: per this review, the best-performing method families identified (deep learning, hybrid process-based+ML) are also generally the least interpretable, and interpretability is presented as a forward-looking research priority rather than a solved problem. Also note the review attributes rising HAB frequency/intensity to climate change and anthropogenic nutrient loading in its framing — a stated association/attribution from the source, not a causal result demonstrated within the retrievable abstract text.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All nine claims are directly supported by the SOURCE TEXT (the reconstructed OpenAlex abstract). No numbers are hallucinated; all cited figures ($50M annual losses, 168 studies, 1997–2025 span, R² 0.89, >90% accuracy, NSE 0.991, 20% XAI adoption rate) appear verbatim in the source. No material caveats present in the source are omitted from the claims. The review was reconstructed from the OpenAlex abstract_inverted_index after the publisher blocked direct access; corroboration via Google Scholar and WebSearch confirms accuracy. Overall: all claims PASS verification."

## Provenance
- Canonical URL: https://ascelibrary.org/doi/10.1061/JOEEDU.EEENG-8732
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Primary article page (ascelibrary.org, both /doi/ and /doi/abs/ variants, and via the doi.org redirect) returned HTTP 403 Forbidden on every attempt (publisher blocks automated fetch) — this is a hard BLOCKED result for full text, confirmed across 3 separate WebFetch calls. Per Step 2 protocol, pivoted to WebSearch and alternate metadata APIs. No open-access preprint/mirror exists (OpenAlex marks the work "Closed access"; no EarthArXiv/ResearchGate/author-site copy found). Usable, complete abstract text was obtained by fetching OpenAlex's API record and requesting the raw abstract_inverted_index (word:position dictionary) rather than a paraphrase, then reconstructing the abstract myself token-by-token from that raw positional data — this was done specifically so that no number would pass through a summarizing/paraphrasing model unverified. One non-numeric connector-word position (75) was absent from the returned dictionary and is inferred from grammar/context only (flagged inline in source_extract); all numeric tokens (168, 1997, 2025, $50 million, 0.89, 90%, 0.991, 20%) were present with explicit positions and were NOT affected by this gap. This reconstruction was cross-checked against an independent Google Scholar result-entry fetch and three separate WebSearch queries run at different times with different phrasing — all returned matching figures and matching quoted fragments, which supports the reconstruction's fidelity. CrossRef's own API record for the same DOI, fetched separately, confirmed title/author/venue/DOI but explicitly stated it had no abstract text in its own metadata, and gave a reference count (117) that differs slightly from OpenAlex's referenced_works count (101) — both are reported above as bibliographic metadata, not findings of the paper, and the discrepancy is likely a difference in what each database counts as a "reference." Because only the abstract (not the article body) could be reached, full_text_access is set to "abstract" and fetch_status to "partial": all key_claims, data_numbers, methods, and stated_limitations above are abstract-level statements only — no results tables, per-study breakdowns, or the paper's own detailed methodology/limitations section were seen.
