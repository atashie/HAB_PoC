---
key: FED-017
title: Forecasting freshwater cyanobacterial harmful algal blooms for Sentinel-3 satellite resolved U.S. lakes and reservoirs
authors_or_org: Schaeffer BA, Reynolds N, Ferriby H, Salls W, Smith D, Johnston JM, Myer M (U.S. EPA researchers)
year: 2024 (published online 7 Nov 2023; journal issue dated Jan 2024, Vol. 349, Article 119518)
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10842250/
access_date: 2026-07-01
tier: FED
source_type: Peer-reviewed journal article (Journal of Environmental Management, Elsevier), full text hosted on PubMed Central (public-access mirror)
categories: [models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Forecasting freshwater cyanobacterial harmful algal blooms for Sentinel-3 satellite resolved U.S. lakes and reservoirs

**What it is.** A peer-reviewed methods paper (Schaeffer et al., 2024, Journal of Environmental Management) by U.S. EPA researchers that builds and validates a near-term (one-week-ahead) probabilistic forecasting model for cyanobacterial harmful algal blooms across 2,192 Sentinel-3-resolvable U.S. lakes and reservoirs, fusing a weekly satellite-derived cyanobacteria/chlorophyll-a index with gridded environmental predictors (water temperature, precipitation, lake depth, lake area) in a Bayesian hierarchical spatiotemporal (INLA) model, and benchmarking it against six machine-learning/neural-network alternatives.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The paper develops a Bayesian hierarchical spatiotemporal (INLA) model that forecasts, one week ahead, whether a lake will exceed the WHO Recreational Guidance Alert Level 1 cyanoHAB threshold, and evaluates it across 2,192 Sentinel-3 OLCI-resolvable U.S. lakes and reservoirs.
  - *evidence:* Stated as the study's central objective/scope in both fetch passes (abstract and methods content); the 2192-lake CONUS scope and the WHO threshold definition were reported consistently in both independent fetches. (Abstract / Introduction / Methods)
  - *quote:* "2,192 satellite-resolved lakes across contiguous United States (CONUS)"
- **[✓ verified]** On an independent, out-of-sample 2021 test year, the INLA model achieved 90% overall accuracy, 88% sensitivity, 91% specificity, 49% precision, and AUC 0.95.
  - *evidence:* This exact set of headline metrics was returned independently and identically by both fetch passes (once in a structured results list, once in a quoted abstract sentence), which cross-validates it as the paper's central reported result. (Abstract / Results)
  - *quote:* "prediction accuracy of 90% with 88% sensitivity, 91% specificity, and 49% precision"
- **[✓ verified]** The INLA model outperformed six machine-learning/neural-network comparison models (Support Vector Classifier, Random Forest, Dense Neural Network, LSTM, RNN, and a 'Gneural Network'/GRU); the best-performing comparison models (SVC and Random Forest) reached only about 0.84-0.85 accuracy.
  - *evidence:* Reported in the second fetch's performance-metrics section as a direct quoted comparison, and corroborated by the first fetch's list of six named comparison model families and its statement that INLA outperformed all of them on sensitivity/specificity. (Results / Discussion)
  - *quote:* "Machine learning models came closest at 0.84 and 0.85"
- **[✓ verified]** Model performance varied substantially by week across the 2021 forecast year: weekly accuracy ranged 80.1%-98.1%, precision 26.1%-64.0%, sensitivity 59.7%-97.5%, and specificity 75.8%-98.4%.
  - *evidence:* Reported as directly quoted ranges in the second fetch pass; not contradicted by the first fetch, which reported only the annual-aggregate figures. (Results)
  - *quote:* "Accuracy ranged from 80.1% to 98.1%"
- **[✓ verified]** Across the full multi-year study record, 10.1% of lake-weeks (43,482 of 432,030) were classified as bloom weeks (exceeding WHO Alert Level 1), with a median cyanobacterial concentration of 33.1 ug/L during those bloom weeks.
  - *evidence:* The 43,482/10.1% figure and the 432,030 total were reported consistently by both fetch passes; the 33.1 ug/L median was given as a directly quoted sentence in the second fetch. (Results)
  - *quote:* "The median cyanobacterial concentration in lakes classified above the WHO Alert Level 1 was 33.1 μg L⁻¹"
- **[⚠ partial]** The model's four environmental predictors (beyond the satellite signal) - weekly water-surface temperature, weekly precipitation, and static lake mean depth and surface area - were associated with bloom log-odds in the fitted model: warmer water was associated with higher bloom log-odds, while higher precipitation, larger lake area, and greater mean depth were associated with lower bloom log-odds. These are model-fitted statistical associations, not demonstrated causal effects.
  - *evidence:* Coefficient values (posterior mean, SD, 95% credible interval) for each of the four predictors were reported in the first fetch pass's structured extraction of the model's predictor-coefficient table. (Methods/Results (predictor coefficients))
  - *quote:* "Water surface temperature: mean 0.54 (SD: 0.02; 95% CI: 0.49-0.58)"
  - *reviewer:* The predictor coefficients and their directional associations are fully supported by the source (Water surface temperature +0.54, Precipitation −0.10, Lake area −1.03, Mean depth −0.72). However, the explicit caveat ('These are model-fitted statistical associations, not demonstrated causal effects') is not stated in the source text. The claim adds this methodologically appropriate qualifier, which is not contradicted but is not explicitly present.
- **[✓ verified]** The bloom 'ground truth' signal is itself a derived satellite product: the Sentinel-3 OLCI cyanobacteria index (CIcyano) is converted to a chlorophyll-a proxy via a fixed linear equation, and this conversion carries roughly the same magnitude of error as typical in-situ chlorophyll-a measurement.
  - *evidence:* The conversion equation and its stated validation error were reported identically in both fetch passes. (Methods)
  - *quote:* "Chl=6620×CIcyano−3.07"
- **[✓ verified]** A Monte Carlo uncertainty analysis found the forecast was robust to satellite retrieval noise up to a standard deviation of 2.65 ug/L (reclassifying under 0.69% of observations), with acceptable performance maintained up to a standard deviation of 5.30 ug/L (44% of the threshold value), before larger noise levels began to degrade performance.
  - *evidence:* Both the specific SD thresholds and the qualitative robustness/degradation language were reported in both fetch passes, including a directly quoted sentence in the second pass. (Methods/Results (uncertainty analysis))
  - *quote:* "Model was robust to small uncertainty in satellite chlorophyll-a values"
- **[✓ verified]** The authors state that the model currently overpredicts positive (bloom) events, which they connect to its comparatively low precision (49%) given the low true base-rate prevalence of blooms (about 9-10%).
  - *evidence:* The overprediction statement was given as a direct quote in the second fetch pass; the first fetch pass independently supplied the 49% precision and 9.1% prevalence figures used to interpret it. (Discussion)
  - *quote:* "Currently, the INLA model overpredicts positive events"
- **[✓ verified]** The model is explicitly scoped to near-surface (within about 2 m depth) biomass/chlorophyll detection and does not forecast cyanotoxins, and it does not incorporate longer-term climate change, nutrient dynamics, or anthropogenic-scenario effects.
  - *evidence:* These limitation statements were returned as direct quotes in the second fetch pass and corroborated in substance (though paraphrased) by the first fetch's limitations section. (Discussion / Limitations)
  - *quote:* "Model does not include the capability to forecast toxins"
- **[✓ verified]** The comparison machine-learning and neural-network models underperformed the INLA model partly because the dataset was imbalanced (most lake-weeks are 'static' bloom-or-no-bloom states rather than transition weeks) and because those models could not handle missing satellite data without additional preprocessing.
  - *evidence:* The specific imbalance percentages were reported in the first fetch pass; the qualitative explanation (inability to handle missing/unbalanced data) was reported in both passes. (Discussion)
  - *quote:* "static bloom/non-bloom states comprise 59.13% of observations vs. 40.87% state transitions"
- **[✓ verified]** The authors frame the weekly forecast as providing 7 days of advance notice, which they compare favorably to a stated United Nations recommendation of 2-3 days advance notice for this kind of hazard.
  - *evidence:* Reported only in the first fetch pass, not independently corroborated by the second; treated as a qualitative claim only (the accompanying '89% overall accuracy' figure attached to it in that same fetch pass was not corroborated and is not asserted here as a distinct metric). (Discussion)
  - *quote:* "exceeding UN recommendation of 2-3 days"

## Data / numbers
- Primary out-of-sample 2021 test: accuracy 90%, sensitivity 88%, specificity 91%, precision 49%, AUC 0.95, False Omission Rate 0.01, F1 0.63, Kappa 0.58, Brier score 0.04
- Holdout validation set (30% of 2017-2020 data, n=132,688): AUC 0.96, accuracy 90%, sensitivity 91%, specificity 90%, precision 42%, False Omission Rate 0.01
- Training split reported as n=308,204 lake-week observations (2017-2020); cross-check: 308,204 + 132,688 = 440,892, i.e. ~70%/30% train/validation split of the 2017-2020 pool
- 432,030 total lake-week observations reported across the full study record (261 weeks, 2192 lakes, 2017-2021)
- 43,482 lake-weeks (10.1%) classified as exceeding the WHO Alert Level 1 bloom threshold across the full study record
- Median cyanobacterial concentration during bloom weeks: 33.1 μg L⁻¹ (chlorophyll-a proxy)
- 2021 weekly performance range: accuracy 80.1%-98.1%; precision 26.1%-64.0%; sensitivity 59.7%-97.5%; specificity 75.8%-98.4%
- Average annual cyanoHAB prevalence across 2021: 9.1%
- Comparison ML models (SVC, Random Forest) reached ~0.84-0.85 accuracy, below INLA's 0.90
- Bloom threshold definition: >12 μg L⁻¹ chlorophyll-a with cyanobacterial dominance (WHO Alert Level 1)
- Chlorophyll-a conversion from satellite index: Chl = 6620×CIcyano − 3.07; ~60% validation error (vs. 30-60% typical in-situ chl-a measurement error)
- Spatial correlation range: 88.02 km (SD 3.31 km); reported spatial variance 83.05 (units unclear in extracted text - flagged)
- Temporal autocorrelation AR(1) coefficient: 0.96
- Predictor posterior log-odds coefficients: water surface temperature +0.54 (SD 0.02; 95% CI 0.49-0.58); precipitation -0.10 (SD 0.01; 95% CI -0.11 to -0.08); lake surface area -1.03 (SD 0.24; 95% CI -1.51 to -0.56); mean depth -0.72 (SD 0.22; 95% CI -1.15 to -0.30)
- Uncertainty robustness: negligible reclassification (<0.69% of observations) at satellite chl-a noise SD of 2.65 μg L⁻¹; acceptable performance retained up to SD 5.30 μg L⁻¹ (44% of threshold value); tested up to SD 10.59 μg L⁻¹
- Compute: 8 cores / 512 GB RAM; ~10.5 hours total 2021 training+forecasting; ~1 hour initial training; ~10 minutes per weekly retrain
- Dataset imbalance: static bloom/non-bloom states = 59.13% of observations vs. 40.87% state-transition weeks
- Forecast lead time: 7 days ahead, contrasted with a stated UN recommendation of 2-3 days advance notice
- 2021 prediction-dataset size reported as n=113,984 in one fetch pass - this equals exactly 2192 lakes × 52 weeks, and was NOT corroborated by the second fetch or reconcilable with the 432,030/308,204/132,688 figures above; treat as uncertain/possibly an extraction artifact
- Prior validation of the CIcyano satellite index cited from other studies (not this paper's own new result): 84% accuracy (Mishra et al. 2021); 94% agreement with visual observations (Coffer et al. 2021); 73% agreement with state advisories (Whitman et al. 2022)
- Journal citation: Journal of Environmental Management, vol. 349, article 119518 (2024); PubMed ID 37944321

## Methods
Primary model: Integrated Nested Laplace Approximation (INLA) hierarchical Bayesian spatiotemporal model, structured as a binomial logistic regression on a weekly binary bloom/no-bloom response (lake exceeding WHO Alert Level 1, i.e., satellite-derived chlorophyll-a proxy >12 ug/L with cyanobacterial dominance), with a first-order temporal autoregressive process [AR(1)] and spatial covariance handled via INLA's Stochastic Partial Differential Equation (SPDE) approach on a Delaunay triangulation mesh, using weakly informative penalized-complexity priors. Satellite input: Sentinel-3 Ocean and Land Colour Instrument (OLCI) cyanobacteria index (CIcyano, using spectral bands at 620/665/681/709 nm), converted to a chlorophyll-a proxy via Chl = 6620xCIcyano - 3.07. Environmental predictors (selected via stepwise AIC, R stepAIC package): weekly water-surface temperature (itself predicted by an auxiliary random forest trained on EPA National Lakes Assessment 2007/2012/2017 and Water Quality Portal 2016-2022 data, 80/20 train-test split), weekly PRISM-derived precipitation, and static lake mean depth and surface area (computed per Hollister & Stachelek 2017). Training used a 2017-2020 pool split roughly 70% training (n=308,204) / 30% holdout validation (n=132,688), with iterative weekly retraining, then predicted forward onto the independent, out-of-sample 2021 calendar year across all 2192 lakes. Benchmarked against six alternative classifiers - Support Vector Classifier, Random Forest, Dense Neural Network, LSTM, RNN, and a "Gneural Network" (GRU) - implemented in scikit-learn/TensorFlow with 80/20 or 80/10/10 splits and min-max normalization; these underperformed INLA and were reported to struggle with missing data and class imbalance. A separate Monte Carlo uncertainty analysis (1000 resamples per noise level; standard deviations of 0.66-10.59 ug/L) tested forecast robustness to satellite chlorophyll-retrieval error. Computation ran on EPA's "Atmos" high-end computer (8 cores, 512 GB memory).

## Stated limitations
The source states: the model is limited to water-surface predictions within about 2 m depth (a satellite spectral-detection limit), and wind/wave-driven vertical mixing can move cyanobacteria out of the detectable surface layer; extended cloud, snow, and ice cover reduce detection capability for individual lakes/weeks; the CIcyano-to-chlorophyll-a conversion itself carries ~60% validation error, comparable to typical in-situ chlorophyll-a measurement error (30-60%); the model does not forecast cyanotoxins (only a chlorophyll-a/biomass proxy), does not provide within-lake process/movement information, and does not incorporate longer-term climate change, nutrient dynamics, or anthropogenic scenarios; it is scoped only to Sentinel-3 OLCI-resolvable freshwater lakes/reservoirs and excludes brackish/estuarine/coastal systems; the model currently overpredicts positive (bloom) events, which the authors link to its comparatively low precision (49% in the primary test) given a low true bloom prevalence (~9-10%), creating potential management expense from false confirmations; the machine-learning and neural-network comparison models suffered from an inability to handle missing data and from dataset class imbalance (59.13% static states vs 40.87% transition weeks), and the authors say these approaches "warrant additional research" with larger, more complete datasets; and the satellite data training record is described as short, limiting climate-projection capability. The authors flag future work on within-lake/localized bloom prediction and real-time dissemination as open needs.

## Tensions with other findings
The source defines "bloom" via a chlorophyll-a/biomass-based threshold (WHO Alert Level 1, >12 ug/L chlorophyll-a with cyanobacterial dominance) rather than a cyanotoxin-concentration threshold, and it explicitly states it cannot forecast toxins directly - this could complicate comparison with other HAB sources that key their risk/harm definition to measured cyanotoxin (e.g., microcystin) concentrations, since biomass exceedance and toxin presence do not always co-occur. Second, the paper's headline "90% accuracy" coexists with only 49% precision in its primary out-of-sample test (and as low as 26.1% in some weeks), driven by low bloom base-rate prevalence (~9-10%); this is a useful internal caution against citing "accuracy" alone from any HAB nowcasting/forecasting source without also checking precision/recall under class imbalance. Third, both the response variable (satellite CIcyano-derived chlorophyll-a) and several predictors (modeled, not measured, water temperature) are themselves model-derived proxies with their own stated ~60% and unspecified errors respectively, so this source's "environmental predictor" effects (temperature, precipitation, lake morphometry) should be read as statistical associations from a correlational Bayesian model, not as demonstrated causal drivers of bloom risk - relevant caution for any downstream claim that treats these coefficients as causal.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Claim 12: The source text itself contains an internal note flagging that the 7-day/UN recommendation sentence was 'not corroborated by Fetch Pass B,' indicating a cross-validation concern that the claim does not mention. This is a meta-caveat about corroboration rather than a substantive scientific caveat.
- **Reviewer notes:** All claims are supported by the source text or are reasonable methodological inferences from it. Claim 6 receives a 'partial' rating because it appends an explicit statement ('not demonstrated causal effects') that adds appropriate scientific rigor but is not verbatim in the source—the underlying coefficients and their directional associations are fully documented. The source text itself flags Claim 12 with an internal note that the specific 7-day/UN comparison sentence was present in Fetch Pass A but not independently corroborated by Fetch Pass B; however, the claim itself is textually present in the provided source material. No numbers are hallucinated, and no major scientific caveats are omitted from the claims."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10842250/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the PMC full-text page (PMC10842250) twice via WebFetch with two different extraction prompts (general comprehensive summary; targeted methods/metrics/limitations), then took the union. Both passes independently returned the same headline metrics (90% accuracy / 88% sensitivity / 91% specificity / 49% precision / AUC 0.95), the same WHO Alert Level 1 threshold (>12 ug/L chl-a with cyanobacterial dominance), and the same authorship/journal, which cross-validates the core figures. A follow-up WebSearch confirmed full bibliographic metadata (Schaeffer et al. 2024, Journal of Environmental Management 349:119518, PMID 37944321) against PubMed/ScienceDirect/EPA listings, which matched the fetched content.

Two caveats found during reconciliation and NOT silently resolved: (1) dataset-size figures are mutually inconsistent across passes - 308,204 (train) + 132,688 (holdout) = 440,892, not the reported 432,030 study-wide total, and a reported 2021-only n of 113,984 exactly equals 2192 lakes x 52 weeks with no missing-data adjustment, which is suspicious given the paper elsewhere describes cloud/ice/snow-driven data gaps; this smells like an extraction approximation in one fetch pass rather than a verbatim source figure, so it is flagged rather than asserted as fact. (2) A "7-day notice, 89% overall accuracy" figure appeared in only one of the two fetch passes and was not corroborated by the second; it may simply be restating the 88-90% headline metrics with transcription noise, so no additional standalone claim was built on the "89%" figure. Both fetches returned rich, section-specific, seemingly-verbatim quoted text (methods, coefficients, limitations), consistent with genuine full-text (not abstract-only) access via PMC's public-access mirror of this EPA-authored, Elsevier-published article.
