---
key: ACAD-050
title: Forecasting freshwater cyanobacterial harmful algal blooms for Sentinel-3 satellite resolved U.S. lakes and reservoirs
authors_or_org: Blake A. Schaeffer, Natalie Reynolds, Hannah Ferriby, Wilson Salls, Deron Smith, John M. Johnston, Mark Myer (US EPA; NASA Ocean Biology and Biogeochemistry Program funding)
year: 2023 (published online 7 Nov 2023; journal issue dated Jan 2024 — Journal of Environmental Management, Vol. 349, Art. 119518; DOI 10.1016/j.jenvman.2023.119518)
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10842250/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, open-access author manuscript (PMC full text, NIHMSID NIHMS1943945, PMID 37944321), CC BY-NC-ND license
categories: [models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Forecasting freshwater cyanobacterial harmful algal blooms for Sentinel-3 satellite resolved U.S. lakes and reservoirs

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/pii/S030147972302306X

**What it is.** A peer-reviewed, EPA/NASA-funded study (Schaeffer et al., 2023, Journal of Environmental Management) that builds and validates a national-scale Bayesian spatiotemporal (INLA) model to forecast one-week-ahead exceedance of the WHO recreational cyanobacteria Alert Level 1 threshold for 2,192 Sentinel-3 OLCI-resolved U.S. lakes and reservoirs across nine climate zones, fusing satellite cyanobacteria/chlorophyll-a signal with weather (PRISM temperature/precipitation) and lake-geomorphology predictors, and benchmarking it against machine-learning and neural-network alternatives.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study applies an INLA hierarchical Bayesian spatiotemporal model to forecast WHO recreational Alert Level 1 exceedance (>12 μg/L chlorophyll-a with cyanobacterial dominance) using weekly Sentinel-3 OLCI satellite data, for 2,192 satellite-resolved U.S. lakes across nine climate zones.
  - *evidence:* Stated directly as the core study design in the abstract. (Abstract)
  - *quote:* "An Integrated Nested Laplace Approximation (INLA) hierarchical Bayesian spatiotemporal model was applied to forecast World Health Organization (WHO) recreation Alert Level 1 exceedance >12 μg L−1 chlorophyll-a with cyanobacteria dominance for 2192 satellite resolved lakes in the United States across nine climate zones."
- **[⚠ partial]** Trained on 2017–2020 data and independently tested on the full 2021 calendar year, the INLA model achieved 90% accuracy, 88% sensitivity, 91% specificity, and 49% precision, outperforming compared machine-learning (SVC, random forest ~0.84–0.85 accuracy) and neural-network (DNN, LSTM, RNN, GRU) models on the same task.
  - *evidence:* Headline result stated in the abstract and detailed in the Results performance table (Table 3). (Abstract; Results, Table 3)
  - *quote:* "the INLA model outperformed the machine learning and neural network models with prediction accuracy of 90% with 88% sensitivity, 91% specificity, and 49% precision as demonstrated by training the model with data from 2017 through 2020 and independently assessing predictions with data from the 2021 calendar year."
  - *reviewer:* Performance metrics and model comparison correct; however, source specifies neural network as 'Gneural Network (GNU)', not 'GRU' (Gated Recurrent Unit)
- **[✓ verified]** The model is framed as giving about one week (7-day) advance notice of Alert Level 1 exceedance, maintaining 89% overall accuracy across the full 2021 test year of iteratively updated weekly forecasts.
  - *evidence:* Stated in the Discussion as the operational forecast-lead-time framing and its accuracy. (Discussion)
  - *quote:* "The INLA model provides 7-day advanced notice with 89% overall accuracy across a calendar year."
- **[✓ verified]** The response variable was defined via the Sentinel-3 OLCI CIcyano cyanobacteria index (detection threshold CIcyano>0.0001), converted to a chlorophyll-a estimate (Chl = 6620×CIcyano − 3.07), thresholded at the WHO Alert Level 1 guideline of >12 μg/L chlorophyll-a with cyanobacterial dominance.
  - *evidence:* Direct methodological definition of the outcome variable, including the exact conversion equation and detection threshold. (Methods)
  - *quote:* "The response variable for the INLA model was the satellite binary presence or absence with a lake median concentration of >12 μg L⁻¹... WHO Alert Level 1 serves as a threshold demonstration in this study, defined as > 12 μg L⁻¹ chlorophyll-a with cyanobacteria dominance."
- **[✓ verified]** Across the full study period, bloom weeks (>WHO Alert Level 1) were a minority class: 43,482 of 432,030 total lake-week observations (10.1%), with a median cyanobacteria concentration of 33.1 μg/L in bloom weeks — a substantial class imbalance the model had to handle.
  - *evidence:* Directly reported dataset composition/prevalence statistic in Results; note this total shows an unresolved arithmetic tension with separately reported train/validation/prediction subset sizes (see tensions field). (Results)
  - *quote:* "There were 261 weeks in the study period—including training, validation, and prediction years—and 432,030 total lake-week observations across all 2192 lakes... with 43,482 (10.1 %) lake-weeks classified as 'bloom weeks', above the WHO Alert Level 1 threshold for INLA."
- **[✓ verified]** The strongest fixed-effect predictors (posterior mean log-odds, 95% credible interval) were weekly mean water surface temperature (+0.54 [0.49, 0.58]), precipitation (−0.10 [−0.11, −0.08]), lake area (−1.03 [−1.51, −0.56]), and mean depth (−0.72 [−1.15, −0.30]) — i.e., the fitted model associates warmer, and shallower/smaller, lakes with higher bloom log-odds; this is a statistical association from the regression, not a claim of causal mechanism (the authors explicitly disclaim process-based interpretation elsewhere).
  - *evidence:* Fixed-effects posterior table plus the authors' own interpretive gloss connecting depth/area to light availability. (Results — fixed-effects posterior table; Discussion interpretation)
  - *quote:* "cyanoHABs may be more likely to occur in shallow waters and smaller lakes due to higher light availability"
- **[✓ verified]** Authors state explicit, self-identified limitations: the model only resolves cyanobacteria within about 2 m of the surface; cannot forecast toxins (biomass/chlorophyll proxy only); is degraded by extended cloud/snow/ice cover; and is not intended as a process-based/mechanistic model.
  - *evidence:* Directly stated in the Discussion/limitations section. (Discussion)
  - *quote:* "This model does not include the capability to forecast toxins, as toxins are not directly measured by satellite. ... This study was not intended to provide process-based information of biochemical, physical, or ecological processes. ... The model was limited to water surface predictions that represented a depth within 2 m of the surface, as the red and near-infrared satellite spectral bands were used to measure the cyanobacteria spectral signature."
- **[✓ verified]** Despite ~90% accuracy/specificity, precision was modest (42–49% across train/validation/prediction); the authors attribute this partly to the low true prevalence of bloom weeks and acknowledge the model currently overpredicts positive events.
  - *evidence:* Authors' own stated caveat linking low base-rate prevalence to a precision ceiling, plus their own characterization of overprediction as an operational cost. (Discussion)
  - *quote:* "The 2021 annual cyanoHAB positive prevalence was relatively low, with an average of 9.1%... if the prevalence was low, it would be harder for a model to achieve high precision. ... Currently, the INLA model overpredicts positive events, the potential management expense of which may be time and costs related to additional confirmation practices."
- **[✓ verified]** Validation used a temporally honest, out-of-time holdout design rather than random shuffling: a 70%/30% train/validation split within 2017–2020, plus a fully independent 2021 test year, with the model iteratively retrained each week through 2021 to simulate a real operational forecast.
  - *evidence:* Explicit description of the validation/cross-validation design, appropriate for autocorrelated spatiotemporal data. (Methods)
  - *quote:* "Seventy percent of the satellite data from 2017 to 2020 was randomly selected for training, 30% of the satellite data from 2017 to 2020 was selected for validation, and all satellite data for 2021 was used for prediction... The model was iteratively updated for each week of 2021, retraining with each current week of predictors to simulate an operational forecast for the subsequent week."
- **[✓ verified]** The authors report the INLA approach as robust to missing data and unbalanced/sparse bloom occurrence without requiring extensive data preparation, unlike the compared ML/neural-network models.
  - *evidence:* Authors' own methodological claim contrasting INLA's handling of missing/imbalanced data against the ML/DNN benchmarks. (Abstract; Discussion)
  - *quote:* "The INLA model was robust to missing data and unbalanced sampling between waterbodies. ... [ML/neural network models] could not handle missing data, unbalanced datasets, and data at various spatial and temporal resolutions without significant data preparation... INLA is built specifically to handle missing data, unbalanced datasets, and data at various spatial and temporal scales without any need for data preparation."
- **[✓ verified]** Model performance was strongly seasonal across the 2021 test year: weekly accuracy ranged 80.1%–98.1%, precision 26.1%–64.0%, sensitivity 59.7%–97.5% (highest in the June–September bloom season), and specificity 75.8%–98.4%.
  - *evidence:* Weekly performance ranges reported for the independent 2021 prediction year, reflecting seasonal variation in skill (drawn from the paper's weekly performance results/figure, not a single verbatim sentence). (Results (weekly performance over 2021))
- **[✗ UNVERIFIED]** Full model training plus the entire 2021 forecast run took about 10.5 hours on an 8-core/512GB EPA high-performance-computing node, while a single weekly iterative retraining update took about 10 minutes, indicating the approach is computationally light enough for a weekly operational forecast cycle at national scale.
  - *evidence:* Authors report compute/runtime as an operational-feasibility detail relevant to running the model in production (numeric detail from the paper's computational-requirements description, not a single verbatim sentence). (Methods (computational requirements))
  - *reviewer:* Computational timings (10.5 hours, 10 minutes) and hardware specifications (8-core/512GB) are not present in any section of the provided source text excerpt, which includes abstract, methods, results, and discussion but no computational requirements or runtime details

## Data / numbers
- 2,192 satellite-resolved lakes and reservoirs (CONUS), across 9 climate zones
- 261 weeks in the study period (2017–2021)
- 432,030 total lake-week observations (stated total across the full 2017–2021 study period; see tensions re: arithmetic vs. subset sizes)
- 43,482 lake-weeks (10.1%) classified as 'bloom weeks' (> WHO Alert Level 1) across the full study period
- Median cyanobacteria concentration in bloom weeks = 33.1 μg L⁻¹
- WHO Alert Level 1 threshold: > 12 μg L⁻¹ chlorophyll-a with cyanobacterial dominance
- CIcyano detection threshold: CIcyano > 0.0001
- Chlorophyll-a conversion equation: Chl = 6620 × CIcyano − 3.07 (Seegers et al. 2021 coefficients)
- Training subset (2017–2020, ~70%): 308,204 observations
- Validation/holdout subset (2017–2020, 30%): 132,688 observations
- Prediction/test subset (2021 only): 113,984 observations (52 weeks × 2192 lakes)
- Training metrics: AUC 0.96; Accuracy 0.90; Sensitivity 0.92; Specificity 0.90; Precision 0.43; False Omission Rate 0.01; F1 0.58; Kappa 0.53; Brier Score 0.03
- Validation metrics: AUC 0.96; Accuracy 0.90; Sensitivity 0.91; Specificity 0.90; Precision 0.42; False Omission Rate 0.01; F1 0.58; Kappa 0.53; Brier Score 0.03
- 2021 independent prediction metrics: AUC 0.95; Accuracy 0.90 (90%); Sensitivity 0.88 (88%); Specificity 0.91 (91%); Precision 0.49 (49%); False Omission Rate 0.01; F1 0.63; Kappa 0.58; Brier Score 0.04
- Youden-optimized classification cutoff = 0.10
- 2021 weekly accuracy range: 80.1%–98.1%
- 2021 weekly precision range: 26.1%–64.0%
- 2021 weekly sensitivity range: 59.7%–97.5% (>90% during weeks 24–37, roughly June–September)
- 2021 weekly specificity range: 75.8%–98.4%
- Fixed-effect posterior log-odds (mean [95% credible interval]): water temperature +0.54 [0.49, 0.58]; precipitation −0.10 [−0.11, −0.08]; lake area −1.03 [−1.51, −0.56]; mean depth −0.72 [−1.15, −0.30]
- Temporal AR(1) autocorrelation parameter = 0.96 (SD 0.00, 95% CI [0.95, 0.97])
- Temporal random-effect variance = 0.77 (SD 0.09)
- Spatial random-effect variance (m) = 83.05 (SD 4.60)
- Spatial correlation range ≈ 88.02 km (SD ± 3.31 km)
- Comparison ML models (CONUS scale): best alternative (random forest/SVC) accuracy 0.84–0.85 vs. INLA 0.90
- 7-day forecast lead time; 89% overall accuracy across the 2021 calendar year
- 2021 annual cyanoHAB positive prevalence ≈ 9.1% (vs. 10.1% prevalence over the full multi-year dataset)
- July / August / September: 1.2% / 2.1% / 2.0% of the 2192 lakes had ≥95% mean weekly probability of exceeding Alert Level 1
- Satellite/model uncertainty tolerance: performance maintained with a cyanobacteria-index-based standard deviation up to 2.65 μg L⁻¹ (<0.69% of observations altered); tolerated uncertainty up to ~44% of the threshold value (5.30 μg L⁻¹ SD vs. 12 μg L⁻¹ threshold)
- Compute: ~10.5 hours on an 8-core/512GB EPA 'Atmos' HPC node for full training + 2021 forecast; ~10 minutes per single-week iterative retraining update
- Training data years: 2017–2020; independent test year: 2021 (DOI 10.1016/j.jenvman.2023.119518, published online 7 Nov 2023)

## Methods
Response variable: weekly binary presence/absence of WHO recreational Alert Level 1 exceedance (lake-median chlorophyll-a >12 μg L⁻¹ with cyanobacterial dominance), derived from Sentinel-3 OLCI via the CIcyano spectral-shape index (detection threshold CIcyano>0.0001) converted to chlorophyll-a via Chl = 6620×CIcyano − 3.07 (Seegers et al. 2021 coefficients). Model: INLA hierarchical Bayesian binomial-logistic spatiotemporal model, logit(y_st) = fixed effects (weekly mean water surface temperature, precipitation, lake area, mean depth) + spatial random effect (SPDE/Delaunay triangulation) + temporal random effect (AR(1)); weakly informative penalized-complexity priors; predictor selection cross-checked with stepwise AIC (R stepAIC). Data: Sentinel-3 OLCI (satellite signal), PRISM climate data (air temperature/precipitation), a random-forest-modeled surface water temperature layer, lake morphology (lakemorpho package), and in-situ validation from EPA National Lakes Assessment (2007/2012/2017) and the Water Quality Portal (2016–2022). Validation design: temporally honest holdout — 70%/30% train/validation split within 2017–2020, plus a fully independent, out-of-time 2021 test year, with the model iteratively retrained each week through 2021 to simulate an operational forecast (not a random shuffle/k-fold, appropriate for autocorrelated spatiotemporal data). Benchmarked against SVC, random forest, DNN, LSTM, RNN, and GRU models on the same task; INLA reported as outperforming all of them on accuracy/sensitivity/specificity, while ML/DNN models "could not handle missing data, unbalanced datasets, and data at various spatial and temporal resolutions without significant data preparation." Where it works (per authors): high discrimination (AUC 0.95–0.96), strong accuracy/sensitivity/specificity, especially in the core June–September bloom season; robust to missing data and class imbalance without preprocessing. Where it is weaker (per authors): precision is modest (42–49%) throughout, is lowest outside the bloom season, does not forecast toxins (biomass/chlorophyll proxy only), and is not process-based (statistical association, not mechanism). Reported compute: ~10.5 hours on an 8-core/512GB EPA "Atmos" HPC node for full 2017–2021 training + forecast; ~10 minutes per weekly iterative retraining update. Code stated to be released at https://doi.org/10.23719/1529140 "after acceptance."

## Stated limitations
Authors explicitly state: (1) the satellite/model resolves cyanobacteria only within ~2 m of the surface (red/near-infrared bands), so vertical mixing and cyanobacterial buoyancy regulation can cause the model to miss biomass at other depths; (2) performance is constrained by the satellite algorithm's detection ability and can miss biomass below the detection limit or due to algorithmic error; (3) extended cloud, snow, and ice cover degrade individual-lake performance; (4) the model is restricted to Sentinel-3 OLCI-resolvable lakes (brackish/estuarine and non-resolvable systems excluded); (5) it "does not include the capability to forecast toxins, as toxins are not directly measured by satellite"; (6) it is "not intended to provide process-based information of biochemical, physical, or ecological processes" — reported predictor effects are statistical associations, not mechanistic; (7) it does not incorporate longer-term climate change, nutrient dynamics, or anthropogenic scenarios, constrained by the short satellite data record (2017–2021 training/testing window); (8) precision is limited in part because true bloom prevalence is low (annual 2021 prevalence ~9.1%), which authors note makes high precision statistically difficult regardless of classifier; (9) the model "currently overpredicts positive events," with a stated management cost of additional false-positive confirmation effort; (10) authors state the model "is transferable and could be applied to other countries" — but this is an assertion, not something empirically tested within the study.

## Tensions with other findings
(1) Unresolved internal arithmetic: the source states 432,030 total lake-week observations across the full 2017–2021/261-week study period (43,482 = 10.1% classified as bloom weeks), yet separately reports 308,204 (70% training) + 132,688 (30% validation) ≈ 440,892 observations for 2017–2020 alone, plus 113,984 for 2021 — summing to ≈554,876, well above the stated 432,030 total. The fetched text does not reconcile this (possibly different denominators, e.g., iterative weekly retraining reusing/expanding the training pool vs. a fixed "valid lake-week" count); flagged here rather than silently resolved, since only the PMC full text (not the original tables/PDF) was accessible. (2) High headline accuracy/specificity (~90%) alongside comparatively low precision (42–49%) illustrates a common tension in rare-event/imbalanced bloom forecasting: an "accuracy" figure alone can overstate operational reliability if precision/PPV isn't reported alongside it — worth checking whether other HAB-forecasting sources in this review report precision or only accuracy. (3) This paper models a biomass/chlorophyll-a proxy threshold (WHO Alert Level 1), explicitly not toxin concentration — a distinction the authors are careful to state, which could be in tension with any other reviewed source that treats "bloom forecast" and "toxin risk" as interchangeable. (4) All reported predictor "effects" (temperature, precipitation, lake geomorphology) are posterior associations from a fitted regression; the authors themselves disclaim process-based/mechanistic interpretation, reinforcing that any driver claims here are correlational, not causal.

## Blind adversarial review
- **Overall:** flag
- **Reviewer notes:** Unsupported count: 1. Hallucinated numbers: 10.5 hours, 8-core, 512GB, 10 minutes (all in claim 12). One partial claim (claim 2) contains a neural network model name error (GNU vs GRU), though all performance metrics are correct. Dropped caveats from source text: (1) vertical mixing and cyanobacteria buoyancy regulation can cause model to miss biomass at various depths; (2) general statement 'No forecast is perfect—all forecast models will result in false positives and false negatives'; (3) model's short-term training period cannot account for long-term climatic changes. Major operational limitations are well-represented in claims (2 m surface-only detection, no toxin forecasting, cloud/snow/ice degradation). Core findings—90% accuracy, 88–91% sensitivity/specificity, validation design, fixed-effect estimates with CIs, and interpretive disclaimers—are well-supported by source text."

## Supplemental materials review (added 2026-07-06)

The publisher supplementary files (ScienceDirect PII `S030147972302306X`) were obtained and reviewed
separately — held locally in `../epa-forecast/` with a full review dossier at `../epa-forecast/README.md`.
Two files: `mmc1.docx` (Supplemental Material and Methods + supplemental discussion/figures) and
`mmc2.xlsx` (**Table S1**). Additions/resolutions to the record above:

- **Table S1 gives the Florida-vs-CONUS split for the six comparison models** (previously we had only the
  CONUS "0.84–0.85" figure at line ~89). Verbatim — **CONUS:** SVC acc 0.838 / **prec 0.030**, Random Forest
  0.849 / 0.862, DNN/LSTM/RNN/GRU acc ~0.65–0.66 / prec 0.58–0.65. **Florida:** all six acc ~0.93, **prec
  0.79–0.93** (SVC 0.907, RF 0.931). This confirms our cited "INLA beat SVC/RF at 0.84–0.85 (CONUS)" and
  exposes the **base-rate → precision mechanism**: precision jumps CONUS→FL for every model (SVC 0.03→0.91)
  because FL bloom prevalence is far higher. The CONUS SVC precision of 0.03 corroborates the authors' claim
  that plain ML/NN models can't handle the imbalance without preprocessing.
- **"GRU," not "GNU" — flag resolved.** The claim-2 reviewer flag ("source specifies 'Gneural Network (GNU)'")
  is resolved by Table S1, which labels the sixth model **`GRU`**. Comparison models = SVC, Random Forest,
  DNN, LSTM, RNN, GRU.
- **Classification cutoff = 0.10** (Youden's index on validation; Fig. S2) — the operating point behind the
  0.49 precision. Confirms the "Youden-optimized cutoff = 0.10" data point (line ~79) from the supplement.
- **Lake value = median of CIcyano pixels** on the **weekly-maximum** composite; **CyAN v4.0**, 300 m,
  Jan 2017–Dec 2021; SRTM **60 m** land mask (static w.r.t. waterbody size).
- **Study lineage / Florida seasonality:** expanded from **Myer et al. 2020's 103 FL lakes** (ACAD-092) to 9
  CONUS climate regions (FL is the ~0.5% sub-tropical tail; study is temperate-dominated). The national AR(1)
  seasonal trend peaks Jul–Sep; the authors note FL specifically shows a May rise and a **strong Nov–Dec
  secondary peak** (FL winter blooms confirmed, Coffer 2020) that the national model **dampens** — a concrete
  Florida gap a regionally-tuned model could target.
- **Compute claim still unverified.** The appendix does **not** contain the 10.5 h / 8-core / 512 GB / 10-min
  runtime figures — the claim-12 "hallucinated numbers" flag stands; those remain unsourced from any text we hold.
- **Fidelity for our baseline:** our out-of-sample FL 2025 evaluation of the *deployed* forecast
  (`../../models/outputs/epa_headtohead.md`: AUC-ROC 0.928, precision ≈0.73) brackets between EPA's CONUS INLA
  (0.49) and the in-sample FL comparison models (0.79–0.93), consistent with the base-rate mechanism — i.e.
  we represent the baseline faithfully. Full argument in `../epa-forecast/README.md` §2.

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10842250/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Primary URL (ScienceDirect, https://www.sciencedirect.com/science/article/pii/S030147972302306X) returned HTTP 403 Forbidden on two separate WebFetch attempts with different prompts (paywall/bot-block) — no content was retrieved from it. Per protocol, WebSearch located an open-access full-text mirror: PMC10842250 (author manuscript, NIHMSID NIHMS1943945, PMID 37944321), confirmed via search snippets to be the same article (matching PII, DOI 10.1016/j.jenvman.2023.119518, Journal of Environmental Management, Vol. 349, Art. 119518). Fetched PMC full text twice with different extraction prompts (comprehensive overview + numeric/table-focused) as required for a HIGH-relevance source, then ran one additional targeted third fetch specifically to pin down and cross-check sample-size figures (total vs. train/validation/prediction subset counts) after noticing they did not sum consistently; the discrepancy could not be resolved from the fetched text and is flagged in tensions/source_extract rather than silently corrected. All content in this dossier is drawn from the PMC full-text version (open access, CC BY-NC-ND), not directly from the paywalled ScienceDirect page. No prior/training knowledge of this paper was used — all claims trace to the three WebFetch extractions performed in this session.
