---
key: ACAD-012
title: Anthropogenic and climatic factors regulate algal bloom intensity and timing in global lakes under climate change
authors_or_org: Kun Xue, Ronghua Ma, Minqi Hu, Yao Li
year: 2026
url: https://www.nature.com/articles/s43247-026-03446-7
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (open access), Communications Earth & Environment (Nature Portfolio), Vol. 7, Article 458, published 01 April 2026
categories: [basic-science]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Anthropogenic and climatic factors regulate algal bloom intensity and timing in global lakes under climate change

**What it is.** A global satellite remote-sensing study that analyzes two decades (2003-2022) of MODIS Aqua imagery across 4,085 lakes (>20 km^2) worldwide to quantify trends in surface algal-bloom intensity (fractional floating algal cover, FAC) and phenology (bloom start/end dates), then uses principal component regression and three SSP climate-scenario projections (to 2081-2100) to attribute these trends to anthropogenic (population density, cropland, GDP, fertilizer use) versus climatic (temperature, wind, precipitation) drivers.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Bloom intensity and bloom timing change largely independently of each other at the global scale, and are governed by different classes of drivers: anthropogenic factors mainly explain rising intensity, while temperature and wind better explain timing shifts, especially in cold regions.
  - *evidence:* This is the paper's headline finding, stated in the abstract, and is what the whole driver-attribution (PCR) analysis is built to support. (Abstract)
  - *quote:* "We find that intensity and timing often change independently: about 71% of lakes show increasing intensity, mainly associated with higher population density and agricultural pressure, whereas temperature and wind better explain shifts in bloom timing, especially in cold regions."
- **[✓ verified]** Under a medium-emission climate scenario, tropical lakes are projected to intensify rapidly with only modest phenology shifts, whereas cold-region lakes show regionally contrasting (not uniform) timing changes.
  - *evidence:* Stated as a top-line projection result in the abstract, based on the SSP2-4.5 scenario applied to the same PCR driver model. (Abstract / Future projections section)
  - *quote:* "Under a medium-emission scenario, tropical lakes show rapid intensification with modest timing shifts, while cold-region lakes exhibit regionally contrasting timing changes."
- **[✓ verified]** Across 2003-2022, most lakes (2,905 of 4,085, 71.11%) showed an increasing trend in fractional algal cover (FAC), averaging +0.032% per year, while 1,180 lakes (28.89%) showed a decreasing trend averaging -0.018% per year.
  - *evidence:* Reported as the primary intensity-trend result from the 20-year MODIS FAC time series across all screened lakes. (Results - Bloom intensity trends (2003-2022))
- **[✓ verified]** A subset of 1,877 lakes had statistically significant FAC increases (averaging +0.046% per year), concentrated in cold (n=1,193) and temperate (n=377) climate zones, while 529 lakes had significant declines (averaging -0.028% per year), also mostly in cold zones (n=309); 841 lakes increased by more than 10% between the first and second decade of the record.
  - *evidence:* These are the statistically-significant-only subsets of the overall trend results, broken out by climate zone. (Results - Bloom intensity trends (2003-2022))
- **[✓ verified]** Bloom timing shows a near-even split globally: 2,134 lakes (55.73%) show delayed start-of-bloom-season (SOD) (+0.041 day/year on average) while 1,695 lakes (44.27%) show earlier onset (-0.046 day/year); end-of-season (EOD) is similarly split, with 1,893 lakes (51.13%) delayed (+0.085 day/year) and 1,809 lakes (48.87%) earlier (-0.084 day/year).
  - *evidence:* Phenology trend results derived from Fourier-smoothed daily FAC curves using a yearly-median+5% threshold definition of bloom season, reported separately for SOD and EOD across the full lake set. (Results - Bloom timing (start/end of season))
- **[✓ verified]** The relative importance of drivers of FAC (intensity), quantified via principal component regression, is dominated by anthropogenic variables: population density contributes 27.63% and GDP 21.37%, versus a combined 30.23% for temperature+wind+precipitation together; 3,123 lakes are classified as primarily anthropogenic-driven versus 607 primarily climate-driven.
  - *evidence:* This is the core attribution result underpinning the 'anthropogenic factors regulate intensity' half of the paper's title/thesis; based on PCA-decorrelated drivers and PCR relative-importance weights reported at p<0.05. (Results - Driver analysis (Principal Component Regression))
- **[✓ verified]** For bloom timing (SOD/EOD), natural (climatic) factors carry more relative importance than for intensity - about 32.47% (SOD) and 32.22% (EOD) - with temperature (11.65%), wind speed (10.54%) and precipitation (10.29%) as the largest individual contributors for SOD; cold-climate lakes account for 90.38% of all lakes with statistically significant timing changes, and natural-factor importance rises to 34.14%-36.51% within the cold zone (roughly 10 percentage points higher than other zones).
  - *evidence:* Supports the 'climatic factors regulate timing, especially in cold regions' half of the thesis. (Results - Driver analysis (Principal Component Regression))
- **[✓ verified]** Regional warming and bloom-timing trends can move in opposite directions across continents: in Europe, summer temperature rose 0.42 degrees C per decade (about double the average rate) while SOD advanced 2.4 days per decade (p<0.05); in North America, warming was weaker and not statistically significant (+0.1 degrees C per decade, p=0.21) yet SOD was significantly delayed by 3.4 days per decade (p<0.01) - i.e. an opposite-signed, statistically significant phenology trend despite non-significant local warming.
  - *evidence:* Regional case comparison used by the authors to illustrate that timing responses to warming are not globally uniform; the North America case in particular shows a significant phenology trend not obviously matched by a significant local temperature trend, illustrating a driver-attribution gap the authors do not fully resolve. (Results/Discussion - Regional temperature-phenology relationships)
  - *quote:* "North American lakes displayed opposing trends with SOD delays (δSOD = 6.67 days)"
- **[✓ verified]** Algal FAC responds non-linearly to temperature: in tropical lakes FAC declines sharply above 28-32 degrees C, while in temperate lakes the decline threshold is lower, above 18-22 degrees C.
  - *evidence:* Derived from Generalized Additive Models (GAM) fitting temperature-FAC relationships separately by climate zone; presented as a threshold/optimum-type response rather than a simple linear one. (Results - Temperature threshold effects (GAM analysis))
- **[✓ verified]** Fertilizer application is correlated with bloom intensity at a majority, not the entirety, of lakes: 61.7% of lakes show a positive correlation between FAC and nitrogen fertilizer use, and 58.7% show a positive correlation with phosphorus fertilizer use.
  - *evidence:* Pearson correlation result linking gridded fertilizer-use data to FAC trends; stated as majority-but-not-universal, implying substantial spatial heterogeneity even in a well-established nutrient-bloom relationship. (Results - Driver analysis (fertilizer correlations))
- **[✓ verified]** Under three future SSP scenarios (SSP1-2.6, SSP2-4.5, SSP4-6.0), the number of lakes projected to show further FAC increases by 2081-2100 (relative to 2003-2022) rises with emissions: 1,134 lakes under SSP1-2.6, 1,495 under SSP2-4.5, and 1,526 under SSP4-6.0; tropical lakes under SSP2-4.5 show a projected intensification of +4.18 percentage points in FAC with comparatively small phenology shifts.
  - *evidence:* Future-projection results obtained by applying the same fitted PCR driver model to projected climate (ISIMIP3b/MRI-ESM2-0) and socioeconomic drivers under each SSP. (Results - Future projections (2081-2100 vs 2003-2022))
- **[✓ verified]** The satellite FAC metric is derived from a Floating Algae Index (FAI) computed from red/NIR/SWIR MODIS bands, converted to a percentage cover via a logistic function calibrated against 1,281 concurrent Landsat 8 OLI-MODIS Aqua image pairs (acquired within 3 hours of each other), with fitted parameters m=4.2 and n=42.7.
  - *evidence:* This is the core remote-sensing method definition and its empirical calibration/validation basis; the paper reports the fitted logistic-regression parameters explicitly. (Methods - Satellite-derived metrics (FAC retrieval))
  - *quote:* "FAC = 100%/(1 + e^(m−n×FAI))"
- **[✓ verified]** The FAC method is explicitly stated to be better suited to detecting dense, surface-accumulating (buoyant) blooms than subsurface blooms or non-buoyant taxa such as diatoms, and the study excludes small lakes (<20 km^2) because MODIS resolution (250-500 m) is too coarse for them.
  - *evidence:* Authors' own stated methodological limitation on what the satellite signal can and cannot detect, and on the lake-size scope of the analysis. (Discussion/Limitations)
  - *quote:* "less sensitive to subsurface blooms or blooms dominated by non-buoyant phytoplankton groups (e.g., diatoms)"
- **[✓ verified]** The authors state that a lack of long-term, global-scale nutrient (nitrogen/phosphorus concentration) datasets prevented nutrients from being used as an independent predictor variable in the driver model, and that this is a data-availability limitation rather than a claim that nutrients are unimportant.
  - *evidence:* Explicit stated limitation about missing covariate data; fertilizer-use data (a proxy, not an in-lake nutrient measurement) were used instead and only covered a restricted period. (Discussion/Limitations)
  - *quote:* "Limitations in the availability of long-term nutrient datasets at the global scale prevented us from incorporating them as independent predictors."
- **[✓ verified]** The authors frame the intensity/timing decoupling as ecologically consequential and call for region-specific rather than one-size-fits-all management, and note that persistent FAC increases could push some lake ecosystems toward a tipping point, that cyanobacteria-dominated blooms offer lower food-web nutritional quality than spring diatom blooms, and that delayed bloom termination could increase short-term organic carbon export and methane (CH4) production.
  - *evidence:* Stated as the paper's ecological-implications/management framing in the discussion and conclusion; these are interpretive claims linked to, but going beyond, the directly measured FAC/phenology trends. (Discussion/Conclusion)
  - *quote:* "This decoupling may alter lake food webs and carbon cycling, underscoring the need for region-specific management strategies under climate change."

## Data / numbers
- 4,085 lakes analyzed (area > 20 km^2), screened from an initial 8,194 lakes
- Total study lake area 1,100,559.01 km^2 (from an initial 1,659,452.98 km^2 before screening)
- Study period 2003-2022 (20 years); future projection window 2081-2100
- 71.11% of lakes (n=2,905) with increasing FAC trend, average +0.032% year^-1
- 28.89% of lakes (n=1,180) with decreasing FAC trend, average -0.018% year^-1
- 1,877 lakes with statistically significant FAC increase, average +0.046% year^-1 (cold zone n=1,193; temperate n=377)
- 529 lakes with statistically significant FAC decline, average -0.028% year^-1 (mostly cold zone, n=309)
- 841 lakes with >10% relative FAC increase between first and second decade (average relative change 8.07%)
- Global mean FAC 1.69% +/- 1.08% (mean +/- SD)
- Oceania mean FAC 2.57% +/- 2.40% (n=24, highest of continents)
- Asia mean FAC 1.48% +/- 1.02% (n=501, lowest of continents)
- 134 lakes with mean FAC > 5%; 89 of these (66.5%) are North American lakes < 100 km^2
- Northern Hemisphere FAC peak ~day 199 of year: 2.82% +/- 2.49%
- Southern Hemisphere FAC peak ~day 355 of year: 3.43% +/- 4.26%
- SOD (start of bloom season) delayed in 55.73% of lakes (n=2,134), average +0.041 day year^-1
- SOD advanced (earlier) in 44.27% of lakes (n=1,695), average -0.046 day year^-1
- 565 lakes with significant SOD delay, average +0.72 day year^-1; 326 lakes with significant SOD advance, average -0.71 day year^-1
- Continental SOD (day-of-year): Africa earliest at 71.89 days; North America latest at 132.47 days
- EOD (end of bloom season) delayed in 51.13% of lakes (n=1,893), average +0.085 day year^-1
- EOD advanced in 48.87% of lakes (n=1,809), average -0.084 day year^-1
- 711 lakes with significant EOD delay, average +0.78 day year^-1; 646 lakes with significant EOD advance, average -0.77 day year^-1
- Continental EOD (day-of-year): South America earliest at 182.13 days; Oceania 194.67 days; Europe 258.19 days; North America latest at 269.42 days
- Tropical and arid-zone blooms occur on average 28.74 days earlier than cold-zone blooms
- PCR driver importance for FAC: population density 27.63%; GDP 21.37%; combined temperature+wind+precipitation 30.23%; cold-zone natural-factor importance 34.14% (~10 percentage points above other zones)
- 3,123 lakes classified as primarily anthropogenically-driven for FAC; 607 lakes primarily climate-driven
- 61.7% of lakes positively correlated (Pearson) between FAC and nitrogen fertilizer use; 58.7% positively correlated with phosphorus fertilizer use
- PCR driver importance for timing: natural factors 32.47% (SOD) and 32.22% (EOD); temperature 11.65%, wind speed 10.54%, precipitation 10.29% (all for SOD)
- Cold-climate lakes = 90.38% of all lakes with statistically significant timing changes; natural-factor contribution within cold zone 36.51%
- Temperature threshold for FAC decline: tropical lakes above 28-32 degrees C; temperate lakes above 18-22 degrees C
- Europe: summer mean temperature +0.42 degrees C decade^-1 (about double the average rate); SOD advanced 2.4 days decade^-1 (p<0.05); EOD delayed 1.1 days decade^-1 (p>0.05, not significant)
- North America: warming +0.1 degrees C decade^-1 (p=0.21, not significant); SOD delayed 3.4 days decade^-1 (p<0.01); EOD advanced 0.8 days decade^-1 (p=0.12, not significant)
- Future lakes with FAC increase by 2081-2100: 1,134 under SSP1-2.6; 1,495 under SSP2-4.5; 1,526 under SSP4-6.0
- Tropical zone projected FAC intensification under SSP2-4.5: delta-FAC = +4.18 percentage points
- Europe (cold zone) under SSP2-4.5: delta-SOD = -1.30 days; delta-EOD = +6.13 days
- North America (cold zone) under SSP2-4.5: delta-SOD = +6.67 days; delta-EOD = -2.23 days
- SSP4-6.0: SOD increases in 1,746 lakes (mean +16.76 days), decreases in 1,372 lakes (mean 15.17 days); EOD increases in 1,488 lakes (mean +16.68 days), decreases in 1,553 lakes (mean 17.54 days)
- SSP1-2.6: tropical zone +0.19% decade^-1 and arid zone +0.16% decade^-1 FAC increase
- FAC retrieval calibration: 1,281 concurrent Landsat 8 OLI / MODIS Aqua image pairs (<3 hour overpass difference); logistic parameters m=4.2, n=42.7
- Lake depth classification (HydroLAKES): shallow <= 3 m mean depth; deep > 3 m mean depth
- Ice-cover exclusion criterion: summer mean temperature < 20 degrees C
- Global Surface Water Occurrence (GSWO) water-frequency threshold: 95%; boundary erosion criterion >30% pixel retention after 1-pixel erosion; daily validity threshold >20% effective pixels
- MODIS Aqua products used: MYD09GA.061 (500 m, 7 bands) and MYD09GQ.061 (250 m, 2 bands), 2003-2022
- Approximate 2100 radiative forcing by scenario: SSP1-2.6 ~2.6 W/m^2, SSP2-4.5 ~4.5 W/m^2, SSP4-6.0 ~6.0 W/m^2
- Fertilizer gridded data available 2003-2019 (one part of the text states fertilizer analyses were restricted to 2003-2013); GDP gridded data (v5) covers 2005-2100 at 0.25 degree resolution
- Data availability: processed lake-level datasets at Figshare https://doi.org/10.6084/m9.figshare.31449865; example analysis scripts at https://doi.org/10.6084/m9.figshare.31489222

## Methods
Satellite remote sensing: MODIS Aqua surface reflectance (MYD09GA.061 at 500 m/7 bands and MYD09GQ.061 at 250 m/2 bands), 2003-2022, used to compute a Floating Algae Index (FAI = rho(NIR) - rho(RED) - [rho(SWIR) - rho(RED)] x (lambda_NIR - lambda_RED)/(lambda_SWIR - lambda_RED)) from red (645 nm), NIR (859 nm) and SWIR (1240 nm) bands, then converted to a Fractional floating Algae Cover (FAC) percentage via a logistic regression (FAC = 100%/(1+e^(m-n*FAI)), m=4.2, n=42.7) calibrated against 1,281 concurrent Landsat 8 OLI/MODIS Aqua image pairs (<3h apart). Lake masks built from Global Surface Water Occurrence (GSWO, 30 m, 95% water-frequency threshold) with a 1-pixel erosion/>30%-retention rule; only lakes >20 km^2 with summer mean temperature <20 degrees C (to exclude persistent ice) and >20% valid daily pixels were retained (4,085 of 8,194 candidate lakes). Daily FAC series were Fourier-smoothed and start/end-of-bloom-season (SOD/EOD) dates derived using a yearly-median-FAC+5% threshold, requiring >=2 consecutive weeks below threshold. Climate forcing (temperature, wind speed, precipitation, 0.5 degree resolution, historical 1850-2014 and projected 2015-2100) came from ISIMIP3b driven by the MRI-ESM2-0 GCM; socioeconomic drivers included population density (ISIMIP2b), gridded GDP (0.25 degree, v5, 2005-2100), cropland fraction (LUH2, 0.25 degree) and gridded N/P fertilizer use (0.5 degree, 2003-2019). Statistical analysis used Pearson correlation (run separately for shallow <=3 m and deep >3 m lakes per HydroLAKES), Principal Component Analysis to decorrelate the six driver variables, Principal Component Regression (PCR) to quantify each driver's relative importance for FAC and for SOD/EOD (relative-importance results reported at p<0.05), and Generalized Additive Models (GAM) to characterize non-linear temperature-FAC relationships by climate zone. Future change was projected by re-applying the fitted PCR model to projected 2081-2100 climate/socioeconomic drivers under three CMIP6 SSP scenarios (SSP1-2.6, SSP2-4.5, SSP4-6.0) and comparing to the 2003-2022 baseline. The method is stated to work well for large (>20 km^2), non-ice-covered lakes with dense, buoyant, surface-accumulating bloom signals, and is explicitly stated to work less well (be less sensitive) for subsurface blooms, non-buoyant taxa such as diatoms, small lakes below MODIS's effective resolution, and extremely turbid waters where NIR reflectance can confound the algal signal.

## Stated limitations
The FAC remote-sensing metric is "particularly sensitive to dense, surface-accumulating blooms" but "less sensitive to subsurface blooms or blooms dominated by non-buoyant phytoplankton groups (e.g., diatoms)", so the reported trends likely under-represent non-buoyant/subsurface bloom dynamics. Small lakes (<20 km^2) were excluded entirely because MODIS's ~250-500 m resolution is too coarse for them; the authors say future work should integrate higher-resolution sensors (Landsat 8/9 OLI, Sentinel-2 MSI) to extend the analysis to smaller lakes. Uncertainty is stated to increase in extremely turbid waters where elevated near-infrared reflectance can partially confound the algal signal, and the authors note no universally applicable global chlorophyll-a product currently exists because lake optical properties vary too strongly. Long-term, global-scale in-situ nutrient (N/P concentration) datasets were unavailable, so nutrients were not used as an independent predictor in the driver model (a fertilizer-use proxy was used instead, covering a restricted period, roughly 2003-2019/2003-2013 per different parts of the text). Other plausible controls on bloom dynamics - water residence time, lake morphology, artificial dams - are not parameterized, again citing global data limitations; seasonal shifts in phytoplankton community composition (e.g., warming-driven species turnover) were also excluded from the study. The future-projection component is explicitly flagged as carrying "large uncertainties" because it rests on a PCR model applied to a "limited number of lakes for which future driver simulations were performed", because the six driver datasets "originate from various sources, leading to complex variability", and because the authors acknowledge "challenges remain in separating climate-driven changes...from those due to other anthropogenic forces."

## Tensions with other findings
The paper states its intensification finding is "consistent with previous global assessments based on Landsat and MODIS observations" (e.g., prior Landsat/MODIS-based global lake-bloom studies), so on the headline "blooms are increasing" point it corroborates rather than contradicts the broader literature. However, it complicates a simple, uniform "warming causes earlier/longer bloom seasons" narrative that is common in HAB literature: within this paper's own regional comparison, Europe shows warming with earlier SOD in the expected direction (SOD advanced 2.4 days/decade, p<0.05, alongside a statistically significant 0.42 degrees C/decade warming trend), but North America shows a statistically significant phenology shift in the opposite direction (SOD delayed 3.4 days/decade, p<0.01) even though local warming there is comparatively weak and NOT statistically significant (p=0.21) - i.e., a significant timing trend without a correspondingly significant local temperature trend to obviously explain it. This is a nuance/internal tension worth flagging when citing "warming drives earlier blooms" claims elsewhere, since this source's own data show the relationship is regionally reversible and not fully mechanistically resolved by temperature alone. The paper also attributes bloom INTENSITY increases predominantly to anthropogenic factors (population density 27.63% + GDP 21.37% > combined climate 30.23%), which sits alongside, but is somewhat distinct from, other narratives that emphasize climate warming as the primary driver of rising bloom intensity/eutrophication - here climate is assigned the larger relative role for TIMING but a smaller one for INTENSITY. All of these driver-attribution results come from correlational methods (Pearson correlation, PCA/PCR), so the source's own "drivers" language should be read as statistical association/relative importance, not demonstrated causation; the source itself does not claim experimental causal proof for any individual driver.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Uncertainties may increase in extremely turbid waters
  - Seasonal shifts in phytoplankton community composition were not considered in this study
  - The PCR model-based approach carries inherent large uncertainties
  - Limited number of lakes for which future driver simulations were performed
  - Challenges remain in separating climate-driven changes from those due to other anthropogenic forces
- **Reviewer notes:** All 15 claims are directly supported by the source text with no fabricated numbers. Dropped caveats are methodological limitations and model uncertainties present in the source's Discussion/Limitations section but not explicitly captured in the claims under review. These do not contradict the claims themselves—they qualify the broader interpretation and scope of findings. Claims 13-14 do capture the most directly relevant limitations to their respective analyses (satellite method constraints, nutrient data gaps)."

## Provenance
- Canonical URL: https://www.nature.com/articles/s43247-026-03446-7
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: WebFetch was called twice on the primary URL (https://www.nature.com/articles/s43247-026-03446-7) as required for a HIGH-relevance source. Both calls initially hit a cookie-consent redirect chain (idp.nature.com/authorize -> idp.nature.com/transit -> back to the nature.com article URL with a one-time auth code query string); each redirect was followed as instructed by the tool's own redirect messages, landing on the live, open-access article page both times. Fetch 1 used a broad "extract everything comprehensively" prompt and returned detailed Results/Methods/Limitations content organized by the paper's own subheadings. Fetch 2 used a targeted prompt for Abstract/Discussion/bibliographic metadata/limitations wording and returned the verbatim abstract, author list, journal/volume/article-number/date, discussion comparisons to prior literature, and data-availability statements. The two extractions were reconciled (duplicates merged, no contradictions found) into the fields above. A WebSearch was also run to confirm the article's identity and was consistent with the two WebFetch results (same title, volume 7, article 458, 2026, Communications Earth & Environment); the search also surfaced several distinct, unrelated lake-bloom papers (e.g., a different Nature Communications paper "s41467-026-69529-3" on climate extremes and lake eutrophication, and a Nature Geoscience paper on global bloom mapping) which were NOT used as sources for this dossier - only the two WebFetch calls on the ACAD-012 URL and its redirect chain were used for claims/quotes. One numeric item that appeared in the first fetch output ("Projected U.S. lake cyanobacteria bloom days: current 7 days to 18-39 days by 2090, cited from Chapra et al. 2017 models") is flagged as lower-confidence: it reads as this paper's own in-text citation of a different prior study (Chapra et al.) rather than this paper's own result, and the attribution label was supplied by the extraction step rather than independently re-verified verbatim, so it was deliberately excluded from key_claims/data_numbers to avoid overstating confidence, though it is noted here for transparency. A funding/acknowledgements statement was not captured in either fetch (fetch 2 explicitly reported it as "not explicitly provided in the visible sections"), so full_text_access is called "full" on the strength of the abstract+results+methods+discussion+limitations+data-availability content obtained, while acknowledging the funding section specifically was not retrieved.
