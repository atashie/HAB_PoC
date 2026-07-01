---
key: ACAD-126
title: Integrated explainable deep learning prediction of harmful algal blooms
authors_or_org: Donghyun Lee, Mingyu Kim, Beomhui Lee, Sangwon Chae, Sungjun Kwon, Sungwon Kang
year: 2022
url: https://doi.org/10.1016/j.techfore.2022.122046
access_date: 2026-07-01
tier: ACAD
source_type: peer-reviewed journal article
categories: [models-and-methods]
relevance: Medium
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Integrated explainable deep learning prediction of harmful algal blooms

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/abs/pii/S0040162522005674

**What it is.** A 2022 peer-reviewed journal article (Technological Forecasting and Social Change, Elsevier, vol. 185, article 122046) presenting an "integrated" convolutional neural network (CNN) model that predicts chlorophyll-a concentration (used as the harmful-algal-bloom proxy) across four major Korean rivers from water-quality and weather variables, with Deep SHAP applied for explainability and performance benchmarked against an LSTM baseline.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study built an integrated convolutional neural network (CNN) model, using eight water-quality variables and four weather variables as inputs, to predict chlorophyll-a concentration across four major Korean rivers with a single model (rather than one model per site).
  - *evidence:* Stated directly as the core method description in the abstract; 'integrated' and 'simultaneously predicting HABs at all monitoring stations' (see claim 4) indicate one model serves all stations/rivers at once, contrasted implicitly with a per-station LSTM baseline. (Abstract)
  - *quote:* "we developed a convolutional neural network model using eight water quality variables and four weather variables to predict the concentration of chlorophyll-a in four major Korean rivers"
- **[✓ verified]** Deep SHAP (a Shapley-value-based explainability method adapted for deep networks) was applied to the CNN to identify which input variables drive the chlorophyll-a predictions, explicitly framed as support for policy/decision-making.
  - *evidence:* Stated as an explicit methodological step in the abstract, directly tying the explainability method to a decision-support purpose rather than pure model diagnostics. (Abstract)
  - *quote:* "Deep SHAP was applied to aid in policy decision-making and identify the influence on variables affecting chlorophyll-a"
- **[✓ verified]** The integrated CNN model reduced RMSE by 38.01% and improved R² by 36.16% relative to an LSTM (long short-term memory) baseline model.
  - *evidence:* Reported as the paper's headline comparative accuracy result against a named baseline; no uncertainty interval, standard deviation, or significance test is given alongside these percentages in the abstract text. (Abstract)
  - *quote:* "This integrated prediction model showed a 38.01 % reduction in root mean square error and 36.16 % improvement in R-squared compared to the long short-term memory (LSTM) model."
- **[⚠ partial]** The integrated model trained 394 times faster than LSTM-based models, even though it simultaneously predicts at all monitoring stations (whereas the comparison implies LSTM models were trained per station).
  - *evidence:* Efficiency claim stated as a direct quantitative comparison in the abstract; no baseline hardware/compute specification or variance is given. (Abstract)
  - *quote:* "despite simultaneously predicting HABs at all monitoring stations and training 394 times faster than LSTM-based models, the proposed method exhibited a significant improvement in efficiency and elucidated variable influences that existing models failed to explain"
  - *reviewer:* The quantitative facts (394× faster training, simultaneous prediction) are in the source. However, the parenthetical inference '(whereas the comparison implies LSTM models were trained per station)' is not explicitly supported. The abstract reports efficiency gains and simultaneous prediction but does not state that LSTM models were trained per-station or explain their architecture.
- **[✓ verified]** The authors frame the model's practical value as decision-support: forecasting HAB spread, surfacing variable influence for decision-makers, and enabling preemptive management responses to reduce economic loss and protect aquatic ecosystems.
  - *evidence:* This is the paper's own closing summary/value statement in the abstract; it is a stated intent/framing by the authors, not an independently validated outcome (e.g., no field deployment or economic-loss measurement is described in the abstract). (Abstract)
  - *quote:* "The proposed integrated prediction model can predict HAB spread, identify variable influences to aid decision-makers, and effectively implement preemptive responses, thus reducing economic losses and preserving aquatic ecosystems."

## Data / numbers
- 38.01% reduction in RMSE (root mean square error) for the integrated CNN model vs. the LSTM baseline (no confidence interval or variance given in the abstract)
- 36.16% improvement in R² (coefficient of determination) for the integrated CNN model vs. the LSTM baseline (no confidence interval given)
- 394x (394 times) faster training time for the integrated CNN model vs. LSTM-based models
- 8 water-quality variables + 4 weather variables used as model inputs (12 predictors total)
- 4 (four) major Korean rivers covered by the single integrated model
- Not from the article itself, but noted for context: OpenAlex records 50 citing works for this paper (94th percentile citation performance) as of this search — bibliometric metadata, not a finding of the paper

## Methods
Convolutional neural network (CNN) taking 8 water-quality variables and 4 weather variables as inputs, trained to forecast chlorophyll-a concentration (used as the HAB proxy) simultaneously across four major Korean rivers with one integrated model. Explainability is provided via Deep SHAP (a SHAP variant for deep networks) to quantify each input variable's influence on predictions. Performance and training efficiency are benchmarked against a long short-term memory (LSTM) recurrent neural network baseline, measured by RMSE, R², and training time. The abstract does not specify: the exact data source/agency, years or temporal range of data used, the specific list of the 8+4 variable names, number of monitoring stations, train/validation/test split methodology, or hyperparameters — none of this was retrievable because only the abstract was accessible (full text sits behind an Elsevier paywall; no legal open-access copy was located via Unpaywall, OpenAlex, or Semantic Scholar).

## Stated limitations
Not stated in the retrieved text. Only the abstract was accessible (the full text is paywalled by Elsevier with no legal open-access copy found via Unpaywall, OpenAlex, or Semantic Scholar), and this type of short abstract does not itself enumerate limitations, caveats, generalizability boundaries, or failure cases. This absence reflects a gap in what could be verified from available text, not a claim that the source states it has no limitations.

## Tensions with other findings
Nothing can be responsibly identified as a stated tension from the abstract alone — the source text does not compare itself against other specific HAB studies beyond its own internal LSTM baseline. One contextual note for the reviewer (my own framing for this literature review, NOT a claim made by the source): this paper predicts chlorophyll-a concentration, a bulk-phytoplankton pigment proxy, rather than cyanobacteria-specific cell counts, cyanotoxin concentration, or a satellite-derived cyanobacteria index (e.g., the EPA CyAN product used elsewhere in this review). Readers should not conflate 'HAB prediction' here with confirmed toxin risk or cyanobacteria-specific detection — the abstract itself uses 'HAB' and 'chlorophyll-a' interchangeably without addressing that distinction. Also note the geography (Korean rivers) and data modality (in-situ water-quality + weather only, no remote-sensing/satellite input mentioned) differ from remote-sensing-fusion approaches (e.g., EPA CyAN + Water Quality Portal) that are central to this project's own Part A design.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All core factual claims are supported by the source abstract. No numbers are hallucinated. One claim contains an unsupported inference (about LSTM per-station training) in a parenthetical, but the main claim's quantitative assertions are correct. The abstract does not state explicit caveats—it reports findings only."

## Provenance
- Canonical URL: https://doi.org/10.1016/j.techfore.2022.122046
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Primary URL (ScienceDirect, both the /abs/ path and the plain /pii/ path) returned HTTP 403 Forbidden on every WebFetch attempt — the fetch tool is blocked by ScienceDirect's bot protection, not merely paywalled-with-content. ResearchGate's page for this paper, SciSpace/typeset.io, growkudos, scilit, and dimensions.ai were also unreachable (403/404/empty) via WebFetch. Confirmed via Unpaywall (api.unpaywall.org) that the DOI is_oa=false, oa_status='closed', with an empty oa_locations array — there is no legal open-access copy of the full text anywhere. OpenAlex and Semantic Scholar APIs both confirm closed access and store no abstract text of their own (abstract fields null). The complete, verbatim abstract was ultimately obtained from IDEAS/RePEc (ideas.repec.org), a bibliographic-metadata mirror that reproduces publisher abstracts verbatim; I fetched that page twice with different prompts and got byte-for-byte-consistent text both times, and the article identifier on that page (v185y2022ics0040162522005674) matches the exact PII given in the task, confirming it is the correct article. Full text (methods detail beyond the abstract, exact data provenance/dates, results tables, discussion, and any stated limitations section) could NOT be retrieved by any means available to me — this dossier is abstract-only. IMPORTANT caveat discovered during research: WebSearch's synthesized answers repeatedly blended in details (a 'Transformer model', 'Lake Erie', 'particulate organic carbon/nitrogen and total phosphorus as SHAP drivers', and an unverified '29 monitoring stations' figure) that, on independent verification, belong to two DIFFERENT unrelated papers — an EarthArxiv preprint by Demiray, Mermer, Baydaroğlu & Demir ('Predicting Harmful Algal Blooms Using Explainable Deep Learning Models: A Comparative Study', about Lake Erie) and a separate ScienceDirect/PMC paper ('Explainable deep learning identifies patterns and drivers of freshwater harmful algal blooms'). I verified this contamination by fetching the EarthArxiv preprint's own title/author/abstract directly, confirmed it was a different study, and excluded all such details from this dossier. Only facts confirmed from a single-source, directly-attributable fetch of the actual paper's own abstract (via ideas.repec.org and cross-checked fragments) are reported below.
