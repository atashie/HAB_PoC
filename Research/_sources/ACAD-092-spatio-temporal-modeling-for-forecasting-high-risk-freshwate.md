---
key: ACAD-092
title: Spatio-Temporal Modeling for Forecasting High-Risk Freshwater Cyanobacterial Harmful Algal Blooms in Florida
authors_or_org: Mark H. Myer, Erin Urquhart, Blake A. Schaeffer, John M. Johnston (all US EPA — ORISE fellows and EPA Center for Exposure Measurement and Modeling, Athens GA / Research Triangle Park NC)
year: 2020
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC7751622/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (open access, PubMed Central)
categories: [models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Spatio-Temporal Modeling for Forecasting High-Risk Freshwater Cyanobacterial Harmful Algal Blooms in Florida

> Note: provisional URL was resolved to a primary source. Original: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7751622/

**What it is.** A peer-reviewed EPA study (Myer, Urquhart, Schaeffer & Johnston, 2020, Frontiers in Environmental Science) that builds and validates a hierarchical Bayesian spatio-temporal model (R-INLA, with an SPDE spatial random effect and an AR1 temporal random effect) to forecast weekly high-risk cyanobacterial bloom occurrence in 103 Florida lakes, fusing Sentinel-3 OLCI satellite-derived cyanobacteria abundance with Landsat surface-water-temperature and PRISM climate covariates over May 2016-June 2019.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study builds a hierarchical Bayesian spatio-temporal model (R-INLA, SPDE spatial random effect + AR1 temporal random effect, binomial logistic response) to forecast weekly high-risk cyanobacterial bloom occurrence across 103 Florida lakes, fusing a satellite cyanobacteria signal (Sentinel-3 OLCI) with in-situ-style environmental covariates (Landsat surface water temperature, PRISM air temperature and precipitation, static lake morphometry) over May 2016-June 2019.
  - *evidence:* Stated directly in the abstract/methods description of study design, model structure, study area and data period. (Abstract; Materials and Methods (Study Area, Data))
  - *quote:* "103 lakes in the state of Florida, United States"
- **[✓ verified]** High-risk bloom status was defined using a WHO-based cyanobacteria cell-count threshold of >100,000 cells/mL, and 22.5% of bloom weeks in the dataset met this high-risk definition.
  - *evidence:* Explicit response-variable definition and prevalence statistic reported in Methods/Results. (Methods (Response Variable); Results)
  - *quote:* "The response variable was the presence or absence of a high-risk cyanobacteria bloom, defined as a waterbody-wide average cell count above 100,000 cells/mL"
- **[✓ verified]** Among lake-weeks classified high-risk, the average cyanobacteria concentration was 376,504 cells/mL, over three times the WHO threshold, indicating high-risk events were not just marginally over the line.
  - *evidence:* Directly stated descriptive result in Results section. (Results)
  - *quote:* "Average waterbody-wide cyanobacterial concentration in lakes classified as high-risk was 376,504 cells/mL, more than three times the WHO 'high' threshold."
- **[✓ verified]** A nested-model comparison via Deviance Information Criterion (DIC) showed that adding spatial structure produced by far the largest improvement in fit (DIC dropped from ~21,300 for non-spatial models to ~7,700-7,600 once a spatial random effect was included), with the combined spatial+temporal model fitting best overall.
  - *evidence:* Reported as a 4-model DIC comparison table (M1 non-hierarchical, M2 temporal-only, M3 spatial-only, M4 spatial+temporal), consistently reported across both extraction passes. (Results, model-comparison table)
  - *quote:* "M1 (non-hierarchical): DIC = 21,381; M2 (temporal only): DIC = 21,294; M3 (spatial only): DIC = 7,758; M4 (spatial + temporal): DIC = 7,601"
- **[✓ verified]** On a 20% holdout validation set the model reached AUC 0.95 with sensitivity and specificity both 0.88 (88% accuracy), but on a genuine future/out-of-sample week the performance was lower: AUC 0.89, sensitivity and specificity both 0.82 (82% accuracy).
  - *evidence:* Two distinct performance evaluations reported: an in-sample-period holdout split and a true prospective one-week-ahead forecast test, giving a more honest sense of real forecasting skill versus fitted skill. (Results (Model Validation))
  - *quote:* "Validation dataset AUC: 0.95 ... accuracy: 0.88 ... Prediction dataset AUC: 0.89 ... accuracy: 0.82"
- **[✓ verified]** The classification cutoff (0.365 predicted probability) used to call a lake-week 'high-risk' was chosen by maximizing Youden's J statistic (sensitivity + specificity - 1) on the validation data, rather than using a default 0.5 threshold.
  - *evidence:* Explicit statement of threshold-selection method and resulting cutoff value. (Methods/Results)
  - *quote:* "Youden optimization attempts to find the cutoff at which sensitivity and specificity are balanced and at a maximum."
- **[✓ verified]** Surface water temperature had a statistically significant positive association with high-risk bloom odds: a one-standard-deviation increase (6.23 degC) corresponded to a log-odds increase of 0.17, i.e. about 1.18 times greater odds.
  - *evidence:* Confirmed by a targeted third fetch that resolved an initial extraction inconsistency; this is the correct multiplicative figure for water temperature (not 14.88x, which belongs to lake depth). (Results / Table 3 (covariate effects))
  - *quote:* "For a one standard deviation increase in surface water temperature (6.23°C), the expected change in high-risk bloom log odds is 0.17 (or 1.18 times greater odds)."
- **[✓ verified]** Mean lake depth had a strong, statistically significant positive association with high-risk bloom odds -- counterintuitive because deeper, more stratified lakes are often assumed lower-risk -- with a one-SD increase (0.75 m) corresponding to a log-odds increase of 2.70, i.e. about 14.88 times greater odds; the authors interpret depth as likely acting as a proxy for water residence time in these shallow, largely polymictic Florida lakes rather than a direct causal mechanism.
  - *evidence:* Explicit coefficient with credible interval, plus authors' own causal caution/reinterpretation of an unexpected sign/magnitude. (Results / Discussion)
  - *quote:* "an increase in one standard deviation (0.75 m) leading to an expected increase in log odds of 2.70 (or 14.88 times greater odds)"
- **[✓ verified]** Ambient air temperature was negatively associated with high-risk bloom odds (1 SD = 4.79 degC -> log-odds -0.23, about 0.79x/lower odds), while precipitation and lake area showed no statistically significant effect (95% credible intervals spanned zero).
  - *evidence:* Reported covariate effect sizes/credible intervals for all five final predictors; two of five were non-significant. (Results / Table 3)
  - *quote:* "a one standard deviation increase in ambient air temperature (4.79°C) resulting in change in high-risk bloom log odds of −0.23 (or 0.79 times lower odds)"
- **[✓ verified]** Bloom risk showed spatial clustering: a fitted spatial correlation range of about 16.8 km (posterior mean rho=16.76 km, 95% CI 10.72-24.14 km) indicates lakes within roughly that distance of one another tend to show correlated high-risk status, and week-to-week bloom state showed strong temporal persistence (AR1 alpha=0.90, 95% CI 0.68-0.99).
  - *evidence:* Both parameters reported as posterior estimates with 95% credible intervals from the fitted hierarchical model's random-effect structure. (Results (spatial and temporal random-effect parameters))
- **[✓ verified]** The authors explicitly caution that their model is not expected to stay accurate more than about two weeks into the future, because the wide-area meteorological covariates it depends on become unreliable beyond that horizon -- directly bounding the model's usable forecast/action window.
  - *evidence:* Stated as an explicit forward-looking limitation on forecast horizon, not merely implied by the data. (Discussion / Limitations)
  - *quote:* "This model is not expected to remain accurate for more than 2 weeks into the future, because wide spatial coverage meteorological estimates become less reliable beyond that time scale."
- **[✓ verified]** The authors flag that, given the strong week-to-week temporal autocorrelation, a substantial share of apparent near-term predictive accuracy could reflect simple persistence of current conditions rather than genuinely new information from the covariates -- an important caveat for interpreting the model's skill.
  - *evidence:* Authors' own interpretive caution about what the strong AR1 term implies for how much of the forecast skill is 'real' versus persistence-driven; text as returned by the fetch tool (not independently re-verified word-for-word in the confirmation pass). (Discussion)
- **[⚠ partial]** Stated limitations include: coarse 300 m satellite pixel resolution, cloud cover, and waterbody misclassification limiting predictive skill in smaller inland lakes; elongated/narrow lakes likely underrepresented in the satellite signal; and land use/nutrient data could not be included as weekly covariates because such data are not available at weekly resolution nationally, leaving a large unexplained spatial variance component.
  - *evidence:* Multiple explicit caveats stated by the authors regarding sensor resolution, lake geometry bias, and omitted-variable (nutrient) limitations. (Discussion / Limitations)
  - *quote:* "the relatively coarse 300 m sensor resolution, presence of cloud cover, and occasional missing data due to waterbody misclassification, limits our predictive ability in smaller inland waterbodies"
  - *reviewer:* The source text lists sensor resolution, cloud cover, waterbody misclassification, and elongated-lake limitations explicitly, and clearly states that nutrients and land-use data are unavailable at weekly resolution. However, the source does not explicitly connect the nutrient/land-use omission to a 'large unexplained spatial variance component'—this causal link is an inference from the reported spatial variance value (38.51) rather than an author statement.
- **[✓ verified]** The authors also caution that satellite red-band penetration depth is very shallow (on the order of centimeters at the cyanoHAB threshold used), so optically shallow water or benthic cyanobacteria could introduce artifacts into the satellite-derived cell-count signal underlying the whole model.
  - *evidence:* Explicit sensor-physics caveat about what the satellite signal can and cannot reliably detect. (Discussion / Limitations)
  - *quote:* "Satellite penetration in the red spectrum is 2 m or less in oligotrophic waters. Given the focus of our model on cyanoHABs at the >100,000 cells/ml threshold, the penetration depth is likely only a few centimeters."
- **[✓ verified]** The authors note the approach is geographically bounded to Florida Coastal Plain lakes and propose future work applying the same spatio-temporal framework at sub-lake resolution (e.g., Lake Okeechobee) and with higher-resolution sensors such as Sentinel-2, implying current results should not be assumed to generalize beyond this study region without further testing.
  - *evidence:* Stated as explicit future-work / scope-boundary language. (Discussion / Conclusion)
  - *quote:* "Future work will apply the spatial-temporal modeling approach at the sub-lake level, particularly in large systems with greater geographic bloom variability such as Lake Okeechobee in South Florida"

## Data / numbers
- Study area: 103 lakes/reservoirs in Florida (St. Johns River, Southwest Florida, South Florida Water Management Districts), NLA Coastal Plain ecoregion
- Study period: May 2016-June 2019 = 217 weeks of Sentinel-3 OLCI satellite observations
- High-risk bloom threshold: waterbody-wide average >100,000 cells/mL cyanobacteria (WHO recreational-exposure guideline)
- 22.5% of total bloom weeks classified high-risk (n=3,149 of 13,980 total weeks studied)
- Mean cyanobacteria concentration in high-risk lake-weeks: 376,504 cells/mL (>3x the WHO threshold)
- Total modeled observations: n=11,096 waterbody-week records; Training 80% / Validation (holdout) 20% = n=2,775; final forecast test week n=103 (May 27-June 2, 2019)
- Holdout validation performance: AUC=0.95, sensitivity=0.88, specificity=0.88, accuracy=0.88
- One-week-ahead true forecast performance: AUC=0.89, sensitivity=0.82, specificity=0.82, accuracy=0.82
- Youden's-index-optimized classification cutoff: 0.365
- Model comparison by Deviance Information Criterion (DIC): M1 non-hierarchical=21,381 (~7s compute); M2 temporal-only=21,294 (~10s); M3 spatial-only=7,758 (~45s); M4 spatial+temporal=7,601 (~53s, best-fitting)
- Surface water temperature (WTEMP) effect: 1 SD=6.23degC -> log-odds +0.17 (95% CrI 0.08-0.26), i.e. 1.18x greater odds
- Ambient air temperature (ATEMP) effect: 1 SD=4.79degC -> log-odds -0.23 (95% CrI -0.37 to -0.08), i.e. 0.79x (lower) odds
- Mean lake depth (DMEAN) effect: 1 SD=0.75 m -> log-odds +2.70 (95% CrI 1.68-3.72), i.e. 14.88x greater odds
- Precipitation (PRECIP) and lake area (AREA): not statistically significant (95% credible intervals span zero)
- Spatial correlation range rho=16.76 km (95% CI 10.72-24.14 km); spatial variance=38.51 (95% CI 25.63-56.35); temporal variance=0.19 (95% CI 0.05-0.62)
- Temporal AR1 autocorrelation parameter alpha=0.90 (95% CI 0.68-0.99)
- Sentinel-3 OLCI: 300 m x 300 m pixel resolution, 2-3 day repeat cycle; minimum 3 water pixels per waterbody (EPA 2012 NLA criteria)
- Landsat ARD surface water temperature: 30 m native resolution, upscaled to 300 m, 8- and 16-day products
- PRISM air temperature: 4 km resolution daily (downscaled to 300 m); PRISM precipitation: 13.8 km resolution hourly (downscaled to 300 m)
- Citation: Frontiers in Environmental Science, 2020 Nov 2; 8:581091, doi:10.3389/fenvs.2020.581091

## Methods
Hierarchical Bayesian spatio-temporal binomial logistic regression fit with R-INLA (Integrated Nested Laplace Approximation), using a Stochastic Partial Differential Equation (SPDE) spatial random effect and a first-order autoregressive (AR1) temporal random effect on top of fixed-effect covariates (formula: logit(y_st) = beta*X + u_s [spatial] + mu_t [temporal AR1]); weakly informative penalized-complexity priors used throughout. Predictor variables (surface water temperature, air temperature, precipitation, lake area, mean lake depth) were first screened via non-spatial GLMs (R glmulti package) and AIC-based stepwise selection (stepAIC), then standardized to Z-scores. Model utility of spatial/temporal terms was tested by comparing four nested model variants (non-hierarchical, temporal-only, spatial-only, spatial+temporal) via Deviance Information Criterion (DIC). Validation used an 80/20 train/holdout split plus a genuine prospective one-week-ahead forecast test, with performance measured via AUC, sensitivity, specificity and accuracy, and a Youden's-J-optimized probability cutoff (0.365) for binary classification. Data: cyanobacteria abundance (response) from Sentinel-3 OLCI Level-1B imagery (NASA Ocean Biology Processing Group), converted from a spectral cyanobacteria index to cells/mL via the Wynne et al. curvature method (updated by Lunetta et al. 2015 and Coffer et al. 2020), weekly-maximum composited; surface water temperature from Landsat Analysis Ready Data (upscaled to 300 m); air temperature and precipitation from PRISM Climate Group (downscaled to 300 m); static lake morphometry (area, depth) via the lakeMorpho R package; waterbodies delineated via USGS/EPA NHDPlus v2 using EPA 2012 National Lakes Assessment site-selection criteria. Per the source, the approach works well within the 103-lake Florida Coastal Plain study domain (strong within-region fit and one-week-ahead skill) but the authors state it is expected to degrade for forecasts beyond ~2 weeks, in smaller/irregularly-shaped inland waterbodies, and in any setting where the underlying 300 m satellite signal or weekly meteorological inputs are degraded (cloud cover, misclassification, coarse resolution).

## Stated limitations
The authors state the model is "not expected to remain accurate for more than 2 weeks into the future" because wide-area meteorological inputs become unreliable beyond that horizon; that its strong week-to-week persistence (AR1 alpha=0.90) means much of its apparent short-term skill could reflect simple continuation of current conditions rather than novel predictive information; that coarse 300 m satellite resolution, cloud cover, and waterbody misclassification limit predictive skill in smaller inland lakes; that elongated/narrow-shaped lakes may be spatially underrepresented in the satellite signal, potentially missing localized blooms; that nutrient and land-use covariates -- widely considered important eutrophication drivers -- could not be included because they are not available at weekly national resolution, leaving a substantial unexplained spatial variance term; that shallow satellite light penetration (a few centimeters at the cyanoHAB threshold used) could introduce bottom-reflectance or benthic-cyanobacteria artifacts; and that weekly temporal averaging, done to manage cloud cover and satellite repeat cycles, causes some loss of information and may miss short-lived blooms. The authors also flag the counterintuitive positive lake-depth association as likely a residence-time proxy rather than a direct mechanistic effect, and note results are specific to Florida's Coastal Plain lakes, with future work proposed at sub-lake resolution (e.g., Lake Okeechobee) and with higher-resolution sensors (Sentinel-2) before broader generalization.

## Tensions with other findings
This is one of the closest published methodological analogs to the HAB_PoC project itself: it fuses a satellite cyanobacteria signal (Sentinel-3 OLCI, same detection lineage/Wynne-method family as EPA CyAN) with in-situ-style environmental covariates (temperature, precipitation) in an explainable, coefficient-based hierarchical Bayesian model, explicitly validated against nested simpler baselines (DIC comparison) and a genuine prospective forecast test rather than only in-sample fit -- directly supporting the brief's emphasis on explainability, defensible baselines, and honest reporting. It also independently corroborates the brief's framing that a ~2-week action window is the realistic ceiling for this kind of forecast: the authors state their own model degrades beyond ~2 weeks due to meteorological input limits. At the same time, it is a useful cautionary example for HAB_PoC's own baseline discipline: the source itself flags that strong temporal autocorrelation (AR1 alpha=0.90) means a persistence/climatology-style baseline could explain much of the apparent short-term accuracy, so any HAB_PoC model claim must be benchmarked against such a baseline, not just an internal train/test split. Its counterintuitive positive lake-depth/bloom-risk association, which the authors explicitly refuse to interpret causally (reframing it as a residence-time proxy), is a clean illustration of the "correlation is not causation" principle HAB_PoC must apply to its own driver claims. No direct contradiction with other HAB sources was evident in the fetched text.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Information loss from 1-week temporal averaging (may cause short-term blooms to be missed)
  - Model robustness to missing data and unbalanced sampling between waterbodies mentioned as a strength but not reflected in any claim
- **Reviewer notes:** Strong extraction overall. One partial claim (13) where the connection between nutrient omission and spatial variance is inferred but not explicitly drawn by the authors. All numeric values are accurate and traceable to the source. The source text is substantial enough (abstract through discussion) to fairly assess all claims. No hallucinated numbers or unsupported claims detected."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7751622/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Primary URL (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7751622/) 301-redirected to https://pmc.ncbi.nlm.nih.gov/articles/PMC7751622/; both WebFetch calls auto-followed and returned substantial full open-access text (methods, results tables, discussion, stated limitations). Per HIGH-relevance protocol, ran two initial fetches with different extraction prompts, then reconciled. Both agreed closely on nearly all figures (DIC values, AUC/sensitivity/specificity, thresholds, spatial/temporal variance terms), giving good cross-fetch confidence. One discrepancy was caught and corrected: both initial fetches stated a "14.88x greater odds" figure for BOTH surface water temperature and mean lake depth, which is numerically inconsistent (exp(0.17)=1.18, not 14.88; exp(2.70)=14.88 matches only depth). A third, narrowly-targeted verification WebFetch confirmed the correct wording: WTEMP is "1.18 times greater odds" and DMEAN is "14.88 times greater odds." This is reflected in the corrected data_numbers/key_claims below; treat the surface-water-temperature effect size as 1.18x, not 14.88x. One minor unreconciled ambiguity remains: the fetches report slightly different denominators for the dataset (n=11,096 "total observations" vs. n=13,980 "total weeks studied" used as the denominator for the 22.5% high-risk figure vs. n=2,775 as ~20% of ~13,875); this likely reflects different accounting (e.g., all lake-weeks with any detected bloom vs. all modeled records vs. validation subset) but could not be fully disambiguated without the original tables, so all three counts are reported as stated rather than forced into agreement.
