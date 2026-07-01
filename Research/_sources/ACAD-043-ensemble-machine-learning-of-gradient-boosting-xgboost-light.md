---
key: ACAD-043
title: Ensemble Machine Learning of Gradient Boosting (XGBoost, LightGBM, CatBoost) and Attention-Based CNN-LSTM for Harmful Algal Blooms Forecasting
authors_or_org: Jung Min Ahn, Jungwook Kim, Kyunghyun Kim
year: 2023
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10611362/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (Toxins, MDPI; open access via PMC)
categories: [models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Ensemble Machine Learning of Gradient Boosting (XGBoost, LightGBM, CatBoost) and Attention-Based CNN-LSTM for Harmful Algal Blooms Forecasting

> Note: provisional URL was resolved to a primary source. Original: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10611362/

**What it is.** A 2023 peer-reviewed methods paper (Toxins, MDPI, open access) that builds, Bayesian-optimization-tunes, and ensembles (bagging + stacking) three gradient-boosting models (XGBoost, LightGBM, CatBoost) and an attention-based CNN-LSTM to forecast weekly cyanobacterial harmful-algal-bloom (HAB) cell counts at a single weir on South Korea's Nakdong River, using only in-situ water-quality and single-station precipitation inputs (trained 2014–2021, tested on 2022).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study built and compared two ML model families — gradient boosting (XGBoost, LightGBM, CatBoost) and an attention-based CNN-LSTM — then combined them via bagging and stacking ensemble techniques to forecast HAB levels.
  - *evidence:* Stated directly in the abstract as the paper's central method and stated purpose. (Abstract)
  - *quote:* "we developed and evaluated two types of machine learning-based models for HABs prediction: Gradient Boosting models (XGBoost, LightGBM, CatBoost) and attention-based CNN-LSTM models... applied bagging and stacking ensemble techniques to obtain the final prediction results."
- **[✓ verified]** On the held-out 2022 weekly test period, LightGBM, the stacking ensemble, and the combined 'Final Ensemble' tied for the best reported fit (R²=0.93, MAE=0.1, RMSE=0.4); CatBoost was the weakest individual model (R²=0.89, MAE=0.2, RMSE=0.5).
  - *evidence:* Read directly from the paper's results table (Table 4, 'Results of different models'); identical values were returned across three independent fetches of the same page, including one explicitly instructed not to round. (Table 4, 'Results of different models')
  - *quote:* "XGBoost 0.92 0.2 0.4 | LightGBM 0.93 0.1 0.4 | CatBoost 0.89 0.2 0.5 | Bagging ensemble 0.92 0.2 0.4 | Stacking ensemble 0.93 0.1 0.4 | Attention-based CNN-LSTM 0.92 0.2 0.4 | Final Ensemble 0.93 0.1 0.4"
- **[⚠ partial]** HAB severity was operationalized as cyanobacteria cell count (cells/mL), ranging 0 to 1,000,000 cells/mL in the raw data, and was log-transformed before modeling because of the large spread in values.
  - *evidence:* Data-preparation/target-definition step described in the data and methods sections. (Data/methods section (variable description, preprocessing))
  - *quote:* "the HABs cell count values ranged from 0 to 1,000,000 cells/mL, they were replaced with log values for the purpose of learning"
  - *reviewer:* The source confirms the range (0–1,000,000 cells/mL) and log-transformation but does not explicitly state the causal reason. Source says the transformation was done 'for the purpose of learning' without explaining why; the 'because of large spread' explanation is inferred from the stated range rather than explicitly stated.
- **[✓ verified]** Model inputs were limited to in-situ water-quality variables (water temperature, pH, dissolved oxygen, total nitrogen, total phosphorus) plus precipitation from one regional weather station; no satellite or remote-sensing variable appears anywhere in the fetched text.
  - *evidence:* Inferred from the complete variable list given identically across both main fetch passes; neither pass surfaced any satellite, spectral, or remote-sensing term despite prompts that explicitly asked for remote-sensing indices. (Data/methods section (input variable list))
  - *quote:* "Water temperature (WT) (°C)... pH... Dissolved oxygen (DO) (mg/L)... Total nitrogen (T-N) (mg/L)... Total phosphorus (T-P) (mg/L)... Precipitation (PCP) (mm) from Daegu General Weather Station"
- **[✓ verified]** A correlation analysis found water temperature had the strongest relationship with (log-transformed) cyanobacteria levels, with month, pH, and total phosphorus also positively correlated.
  - *evidence:* Reported as a correlation-analysis finding (associative, not causal, framing) ahead of model-building. (Results section (correlation analysis, preceding modeling))
  - *quote:* "The data that had the highest correlation with Logcyano were water temperature, and the variables that had positive correlations were the month, pH, and T-P."
- **[✓ verified]** Hyperparameters for every model were tuned via Bayesian optimization (HyperOpt) with 50 evaluations, yielding specific tuned settings per model (e.g., LightGBM: max_depth=12, learning_rate=0.045, n_estimators=574; CatBoost: n_estimators=7600).
  - *evidence:* Reported in the hyperparameter-tuning methods subsection and its results table of tuned values. (Methods, hyperparameter-tuning subsection and hyperparameter table)
  - *quote:* "XGBoost... max_depth=4, learning_rate=0.05, n_estimators=428; LightGBM... max_depth=12, learning_rate=0.045, n_estimators=574; CatBoost... max_depth=3, learning_rate=0.025, n_estimators=7600; CNN-LSTM... hidden_size=4, num_layers=2, dropout_rate=0.1, learning_rate=0.00568939"
- **[✓ verified]** Models were trained/tuned on weekly data from Jan 1, 2014 through Dec 31, 2021, and evaluated on weekly data from Jan 1 through Dec 31, 2022 as a held-out prediction year.
  - *evidence:* Both main extraction passes independently reported this same train/prediction date split; treated as a close paraphrase of the source's stated study period since neither fetch returned a single verbatim sentence stating both dates together. (Methods/data section (study period))
- **[✓ verified]** The bagging ensemble of the three gradient-boosting models produced a smaller overall error deviation across the test year than the stacking ensemble, even though stacking matched the best point-metric scores; CatBoost's errors were particularly high around June.
  - *evidence:* Discussion of ensemble error behavior over time, contextualizing the headline Table 4 metrics. (Results/Discussion, immediately following Table 4)
  - *quote:* "The error size was relatively high for CatBoost around June, and the bagging ensemble technique resulted in a smaller overall error deviation than the stacking ensemble technique."
- **[✓ verified]** The authors attribute cross-model performance differences broadly to several interacting factors rather than one identified cause, and frame ML models as a new complement to prior mechanism-based numerical models (e.g., EFDC) rather than as a directly benchmarked replacement — no head-to-head EFDC comparison numbers are given anywhere in the fetched text.
  - *evidence:* Framing statement in the abstract plus an explicit caveat about CatBoost/model variability in the discussion. (Abstract; Results/Discussion)
  - *quote:* "While mechanism-based numerical modeling, such as the Environmental Fluid Dynamics Code (EFDC), has been widely used in the past, the recent development of machine learning technology... has opened up new possibilities for HABs prediction.' ... 'the accuracy of the prediction results can vary depending on various factors such as time, location, input data composition, and model."
- **[✓ verified]** The paper's closest statement to a limitation is a data-scarcity caveat: despite weekly HAB monitoring since 2014, 'not much data' has accumulated, and it frames better/earlier policy-relevant prediction as contingent on future data accumulation and more advanced algorithms.
  - *evidence:* Forward-looking caveat / future-work statement in the discussion or conclusion; no dedicated 'Limitations' heading was found in either main fetch pass. (Discussion/Conclusion)
  - *quote:* "Not much data have been accumulated for HABs observation even though it has been performed on a weekly basis since 2014.' ... 'If future data are accumulated and advanced algorithms are developed, the basis for predicting HABs in advance and utilizing them for policy purposes will be laid."

## Data / numbers
- R² = 0.92 (XGBoost)
- R² = 0.93 (LightGBM)
- R² = 0.89 (CatBoost) — lowest of the individual models
- R² = 0.92 (Bagging ensemble of XGBoost+LightGBM+CatBoost)
- R² = 0.93 (Stacking ensemble)
- R² = 0.92 (Attention-based CNN-LSTM)
- R² = 0.93 (Final Ensemble combining GB models + CNN-LSTM) — best reported, tied with LightGBM and Stacking ensemble
- MAE = 0.1 (LightGBM, Stacking ensemble, Final Ensemble); MAE = 0.2 (XGBoost, CatBoost, Bagging ensemble, CNN-LSTM) — units not restated alongside the table; target was log10-transformed HAB cell count (cells/mL)
- RMSE = 0.4 (XGBoost, LightGBM, Bagging ensemble, Stacking ensemble, CNN-LSTM, Final Ensemble); RMSE = 0.5 (CatBoost)
- HAB (cyanobacteria) cell counts ranged 0 to 1,000,000 cells/mL in the raw dataset before log-transformation
- Study/training period: weekly data, Jan 1 2014 – Dec 31 2021 (~8 years); held-out prediction period: Jan 1 2022 – Dec 31 2022 (1 year)
- Bayesian hyperparameter optimization via HyperOpt, max_evals = 50
- 5 bootstrap samples (seeds 0–4/0–5) generated per gradient-boosting model for the bagging ensemble
- Tuned XGBoost: max_depth=4, learning_rate=0.05, n_estimators=428
- Tuned LightGBM: max_depth=12, learning_rate=0.045, n_estimators=574
- Tuned CatBoost: max_depth=3, learning_rate=0.025, n_estimators=7600
- Tuned attention CNN-LSTM: hidden_size=4, num_layers=2, dropout_rate=0.1, learning_rate=0.00568939
- DOI 10.3390/toxins15100608; PMID 37888638; PMCID PMC10611362; Toxins 15(10):608 (2023)

## Methods
Two model families were built to forecast weekly HAB (cyanobacteria) cell counts at a single weir on the Nakdong River (Changnyeong-Haman Weir, South Korea), used for drinking-water supply: (1) three gradient-boosting models — XGBoost, LightGBM, CatBoost — and (2) an attention-based CNN-LSTM (1D-CNN feature extraction feeding a Bahdanau-attention LSTM). Inputs were in-situ water-quality variables (water temperature, pH, dissolved oxygen, total nitrogen, total phosphorus) plus precipitation from one regional weather station (Daegu); no remote-sensing/satellite variable is described anywhere in the fetched text. The skewed HAB cell-count target (0–1,000,000 cells/mL) was log-transformed; inputs were MinMax-scaled. Hyperparameters for every model were tuned via Bayesian optimization (HyperOpt, 50 evaluations). Models were trained/tuned on weekly data spanning 2014–2021 and evaluated on held-out weekly data from 2022. The three gradient-boosting models were combined via bagging (5 bootstrap variants per model, different seeds) and via stacking (meta-learner); a 'Final Ensemble' then combined the gradient-boosting outputs with the attention CNN-LSTM. Where it "works": LightGBM, the stacking ensemble, and the Final Ensemble all reach the paper's best reported fit (R²=0.93) on this one river/weir/year. Where it "fails" or is weaker: CatBoost underperforms the other models (R²=0.89) with the authors noting particularly high error around June, and they attribute cross-model differences broadly to "time, location, input data composition, and model" rather than a single diagnosed cause. No naive/persistence/climatology baseline and no remote-sensing predictor appear anywhere in the fetched text.

## Stated limitations
The fetched text does not contain a section formally headed "Limitations" (confirmed independently by both main extraction passes). The closest the authors come is a data-availability caveat: "Not much data have been accumulated for HABs observation even though it has been performed on a weekly basis since 2014" — i.e., despite weekly cadence, the observational record (2014–2022, one 2022 test year) is short. On individual-model reliability, they acknowledge CatBoost gave "relatively poor prediction results" relative to the other models, with error "relatively high... around June," and attribute cross-model accuracy differences broadly to "various factors such as time, location, input data composition, and model" without isolating a specific cause. As forward-looking framing, they state that better, earlier, policy-usable HAB prediction depends on more data being accumulated and more advanced algorithms being developed, implying the authors themselves see current data volume as a constraint on real-world/policy readiness.

## Tensions with other findings
This source reports strong fit (R²=0.89–0.93) using ONLY in-situ weekly water-quality variables (water temperature, pH, dissolved oxygen, total nitrogen, total phosphorus) plus single-station precipitation — no satellite or remote-sensing input is described anywhere in the fetched text. That sits in tension with a remote-sensing-fusion framing such as this project's own approach: it could mean dense in-situ river monitoring alone yields high apparent skill without any spectral/satellite signal, but it is equally possible the reported skill is optimistic because (a) evaluation used a single held-out year rather than multiple independent test periods or repeated folds, (b) no naive/persistence or seasonal-climatology baseline is reported against which R²=0.89–0.93 could be judged, and (c) the top correlates identified (water temperature, calendar month) are themselves seasonal/climatological proxies, so part of the apparent skill may reflect the model learning an annual cycle rather than a specific chemical or bloom-formation driver. None of these caveats are raised by the authors in the fetched text (no dedicated limitations section was found), so they are flagged here as an external methodological read, not an in-source finding — consistent with treating water-temperature/month correlation as associative, not causal.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All claims verified against source text. One partial claim (Claim 3) where the causal explanation 'because of large spread in values' is a reasonable inference from the stated data range but is not explicitly stated in the source, which only says the transformation was done 'for the purpose of learning.' All numeric values (R², MAE, RMSE, hyperparameters, dates, cell counts, evaluations count) verified exact to the source table and methods sections. No evidence of data hallucination or dropped major caveats."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10611362/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Original URL (ncbi.nlm.nih.gov) 301-redirected to pmc.ncbi.nlm.nih.gov; followed the redirect per instructions. Per the HIGH-relevance protocol, fetched the resolved PMC URL twice with different extraction prompts (one broad: title/abstract/data/metrics/limitations; one targeted: study area/features/tables/sample size/limitations verbatim). Both passes returned the same model list, same Table 4 metric values (R²/MAE/RMSE to 2/1 decimal places), same hyperparameters, and the same absence of a formal limitations section, giving high confidence in consistency. Because the R²/MAE/RMSE values looked suspiciously rounded, ran a third confirmatory WebFetch on the same PMC page targeted specifically at Table 4, explicitly instructing not to round — it returned the identical values, indicating the rounding is native to the paper's own table, not an extraction artifact. Attempted a fourth check against the publisher page (mdpi.com/2072-6651/15/10/608) to cross-validate; that request returned HTTP 403 Forbidden, so it was abandoned and PMC (open-access full text, PMCID PMC10611362) was relied on as the authoritative full-text source. No PDF/file download or filesystem access was used — all content came from WebFetch of the PMC HTML page.
