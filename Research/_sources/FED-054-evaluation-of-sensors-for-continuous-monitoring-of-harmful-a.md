---
key: FED-054
title: Evaluation of sensors for continuous monitoring of harmful algal blooms in the Finger Lakes region, New York, 2019 and 2020
authors_or_org: U.S. Geological Survey (New York Water Science Center), conducted in cooperation with the New York State Department of Environmental Conservation. Individual human authors were not identified in the extracted text; report is issued under USGS Scientific Investigations Report series with contact given as "Director, New York Water Science Center."
year: 2024
url: https://pubs.usgs.gov/publication/sir20245010/full (no redirect occurred; report DOI: https://doi.org/10.3133/sir20245010; PDF also available at https://pubs.usgs.gov/sir/2024/5010/sir20245010.pdf)
access_date: 2026-07-01
tier: FED
source_type: federal scientific investigations report
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Evaluation of sensors for continuous monitoring of harmful algal blooms in the Finger Lakes region, New York, 2019 and 2020

> Note: provisional URL was resolved to a primary source. Original: https://pubs.usgs.gov/publication/sir20245010/full

**What it is.** A USGS Scientific Investigations Report (SIR 2024-5010, posted March 26, 2024), produced in cooperation with the New York State Department of Environmental Conservation, documenting a pilot deployment of high-frequency in-situ sensor platforms (multiparameter sondes, nutrient optical sensors, fluorometers, weather/light instruments) on three New York Finger Lakes (Seneca, Owasco, Skaneateles) in 2019-2020, and a statistical evaluation of how well those continuous sensor readings agreed with discrete laboratory reference samples (chlorophyll-a, nutrients, dissolved organic carbon, phytoplankton/cyanobacteria biovolume), intended to inform future continuous cyanobacterial harmful algal bloom (cyanoHAB) monitoring strategies.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The continuous monitoring sensors, deployed on open-water platforms at three Finger Lakes, performed reasonably well overall in 2019-2020 despite operational challenges (power issues, biofouling), but statistical agreement with laboratory reference samples varied substantially by lake and by parameter.
  - *evidence:* Stated as the report's own overall/conclusions-level assessment, then substantiated by the parameter-specific correlation results (chlorophyll, phycocyanin, fDOM, nitrate, orthophosphate) that follow in the results section. (Conclusions section ("Overall Assessment"); Results section overview)
  - *quote:* "Despite challenges like power issues and sensor fouling, the sensors performed well overall."
- **[✓ verified]** Multivariate (stepwise) regression models built from multiple sensor parameters did not explain more variance in chlorophyll-a or biovolume than simple univariate fluorescence-based models.
  - *evidence:* Directly stated as the outcome of the stepwise regression analysis (66 of 147 possible observations, alpha = 0.05, forward/backward stepwise), reported as a negative/null result for the value-add of multivariate sensor fusion over single-sensor fluorescence. (Results section, "Regression Modeling" subsection)
  - *quote:* "Multivariate models did not outperform simple fluorescence-based models."
- **[✓ verified]** Sensor-measured chlorophyll fluorescence showed only moderate correlation with laboratory-measured chlorophyll-a, with correlation strength differing by lake (strongest at Seneca, weaker at Owasco and Skaneateles), and was weaker still against total phytoplankton biovolume.
  - *evidence:* Per-lake Pearson and Spearman coefficients are given for chlorophyll fluorescence vs. lab chlorophyll-a; the source separately states that relations with total phytoplankton biovolume were weaker than with chlorophyll-a. (Results section, "Chlorophyll Fluorescence" subsection)
  - *quote:* "relations with total phytoplankton biovolume were weaker"
- **[✓ verified]** Phycocyanin fluorescence from the dual-channel sonde fluorometers was not significantly related to cyanobacterial biovolume, and turbidity was a more significant indicator of cyanobacterial biovolume variability than phycocyanin.
  - *evidence:* Both statements are given as direct results-section findings; the turbidity-over-phycocyanin finding is flagged by the report itself as notable, since phycocyanin is the conventional in-situ cyanobacteria proxy. (Results section, "Phycocyanin" and "Turbidity" subsections; also repeated in the Limitations section)
  - *quote:* "Relations between phycocyanin concentration measurements from the dual-channel fluorometers and cyanobacterial biovolume were not significant."
- **[✓ verified]** The fluorescent dissolved organic matter (fDOM) sensor had a weak (and in several cases negative-direction) relationship with laboratory-measured dissolved organic carbon (DOC) at all three study lakes.
  - *evidence:* Explicit qualitative statement plus lake-specific Pearson/Spearman coefficients, several of which are negative, supporting the 'weak' characterization. (Results section, "Fluorescent Dissolved Organic Matter (fDOM)" subsection; Limitations section)
  - *quote:* "The relation between the fluorescent dissolved organic matter sensor and laboratory-measured dissolved organic carbon was weak at all study lakes."
- **[✓ verified]** Nitrate sensors showed a strong overall monotonic/linear relationship with laboratory nitrate values across lakes combined, but the Seneca Lake sensor underestimated concentrations relative to lab samples (lower R^2, narrower sensor range than the lab range), while the Owasco Lake sensor showed better agreement.
  - *evidence:* Overall pooled correlation/R^2 given, followed by per-lake sample size, R^2, and sensor-vs-lab concentration range comparison showing the Seneca sensor's narrower/underestimating range. (Results section, "Nitrate" subsection)
  - *quote:* "Spearman's ρ = 0.87, p < 0.05, n = 24; Pearson's r = 0.88, R² = 0.78"
- **[✓ verified]** Orthophosphate sensor performance could not be meaningfully evaluated in this study because the overwhelming majority of discrete laboratory samples fell below the analytical detection or reporting limits, leaving almost no paired data for comparison.
  - *evidence:* Quantifies the non-detect rate (5 of 147 samples above detection limit; only 1 above reporting limit) that the report gives as the reason evaluation was not possible. (Results section, "Orthophosphate" subsection)
  - *quote:* "Only 1 sample (0.7%) was above reporting limit, measuring 0.012 mg/L as P from Owasco Lake near-bottom on June 27, 2019."
- **[✓ verified]** Among all sensor-measured parameters, water temperature was one of the strongest correlates of chlorophyll-a, total phytoplankton biovolume, and cyanobacterial biovolume.
  - *evidence:* Direct comparative statement ranking temperature's correlative strength against the other measured parameters in the study. (Results section, "Water Temperature" subsection)
  - *quote:* "Of all collected parameters, water temperature was among the strongest correlated with chlorophyll-a, total phytoplankton biovolume, and cyanobacterial biovolume."
- **[✓ verified]** The report attributes the limited explanatory power of its chlorophyll-a/biovolume models partly to the absence of cyanoHAB events at the specific open-water monitoring locations during the study, and separately cautions that Finger Lakes cyanoHABs are often spatially isolated, ephemeral, or heterogeneous, such that fixed-point sensor platforms and discrete grab sampling may not reliably capture elevated bloom concentrations occurring elsewhere in a lake.
  - *evidence:* Two linked caveats stated by the report itself about the generalizability/representativeness of its fixed open-water monitoring design relative to the true spatial distribution of blooms. (Discussion/Limitations section)
  - *quote:* "CyanoHABs in the Finger Lakes are commonly isolated, ephemeral, or spatially heterogeneous, so monitoring and quantifying risk to public health through traditional discrete grab sampling may not reliably capture elevated concentrations."
- **[✓ verified]** The stepwise multivariate regression analysis was constrained by substantial missing sensor data, using only 66 of 147 possible paired observations, illustrating how incomplete concurrent sensor records limit model-building even when many instruments are deployed.
  - *evidence:* States the sample-size shortfall directly attributable to missing sensor data across the multi-instrument platform, and is echoed by the report's own concluding remark on the importance of maintaining all sensors continuously. (Methods section, "Regression Modeling" subsection (Statistical Methods); Limitations, "Dataset Completeness" subsection)
  - *quote:* "analysis limited to 66 of 147 possible observations due to missing sensor data"
- **[✓ verified]** Laboratory replicate quality-control samples for chlorophyll-a showed a median relative percent difference (RPD) of 7.9% (within the study's 20% acceptance threshold), but 3 of 13 replicate pairs exceeded 20% RPD (23.7-29.5%), indicating the lab 'ground truth' itself carries measurable sampling/analytical noise against which sensors were judged.
  - *evidence:* Specific QC statistic (median RPD, exceedance count and range, and absolute concentration differences) reported for chlorophyll-a discrete-sample replicates. (Methods section, Quality Assurance/Quality Control subsection)
  - *quote:* "Chlorophyll-a: median RPD = 7.9%, n = 13 pairs (3 pairs exceeded 20%, ranging 23.7–29.5%, with differences 0.14–1.24 µg/L)"
- **[✓ verified]** Data loss was substantial in 2019 due to daisy-chained wiring among multiparameter sondes, a problem the study resolved in 2020 by giving each sonde independent cabling; extended 2019 deployment intervals (4-8 weeks between visits) also caused heavy biofouling (dreissenid mussels) that was reduced in 2020 by increasing site-visit frequency to every two weeks.
  - *evidence:* Operational/data-quality limitation explicitly attributed to platform wiring design and visit frequency, contrasted between the two study years. (Limitations section, "Data Loss Issues" subsection)
  - *quote:* "substantial loss of real-time sensor data"
- **[⚠ partial]** The report recommends that future CyanoHAB monitoring integrate machine learning to exploit the large multi-sensor datasets these platforms generate, but states that broader data collection capturing more actual cyanoHAB events is needed before such models can be adequately refined.
  - *evidence:* Forward-looking recommendation stated in the conclusions, conditioned on the acknowledged shortage of bloom-event data in the current dataset. (Conclusions section, "Machine Learning Potential" and "Need for Additional Data" subsections)
  - *quote:* "Broader data collection, including more CyanoHAB events, is necessary to refine these models."
  - *reviewer:* Framing of 'recommends' overstates source's cautious conditional language. Source says machine learning 'could leverage' datasets (exploratory), not a direct recommendation/prescription. The broader-data caveat is clearly present and well-supported.

## Data / numbers
- Chlorophyll fluorescence vs. lab chlorophyll-a: Seneca Lake Pearson's r = 0.774, Spearman's rho = 0.738 (sample size not specified in extracted text)
- Chlorophyll fluorescence vs. lab chlorophyll-a: Owasco Lake Pearson's r = 0.578, Spearman's rho = 0.717
- Chlorophyll fluorescence vs. lab chlorophyll-a: Skaneateles Lake Pearson's r = 0.619, Spearman's rho = 0.772
- fDOM sensor vs. lab DOC: Seneca Lake Pearson's r = -0.159, Spearman's rho = -0.308
- fDOM sensor vs. lab DOC: Owasco Lake Pearson's r = -0.275, Spearman's rho = -0.598
- fDOM sensor vs. lab DOC: Skaneateles Lake Pearson's r = -0.072, Spearman's rho = -0.270
- Nitrate sensor vs. lab (all lakes combined): Spearman's rho = 0.87 (p < 0.05, n = 24); Pearson's r = 0.88, R^2 = 0.78 (78% of variance explained)
- Nitrate sensor, Seneca Lake: n = 13, R^2 = 0.64 (sensor underestimated lab values); sensor range 0.24-0.50 mg/L as N vs. lab range 0.05-1.19 mg/L as N
- Nitrate sensor, Owasco Lake: n = 11, R^2 = 0.88; sensor range 0.58-1.19 mg/L as N vs. lab range 0.58-1.21 mg/L as N
- Orthophosphate: only 5 of 147 discrete samples (3.4%) above minimum detection limit of 0.004 mg/L as P
- Orthophosphate: only 1 sample (0.7%) above reporting limit, value = 0.012 mg/L as P (Owasco Lake, near-bottom, June 27, 2019)
- Stepwise regression dataset: 66 of 147 possible paired observations usable (missing sensor data excluded remainder)
- Chlorophyll-a lab replicate QC: median relative percent difference (RPD) = 7.9%, n = 13 pairs; 3 pairs exceeded the 20% RPD acceptance criterion, ranging 23.7-29.5% RPD (absolute differences 0.14-1.24 ug/L)
- Nitrate lab replicate QC: median RPD = 1.8%, n = 15 pairs
- DOC lab replicate QC: median RPD = 1.8%, n = 14 pairs
- Phytoplankton replicate QC (Absolute Value Logarithmic Difference, AVLD < 1 acceptance): total biovolume range 0.14-0.86, median AVLD = 0.25, n = 15 pairs; cyanobacterial biovolume range 0.11-0.61, median AVLD = 0.26, n = 15 pairs
- Sample replication: 15 replicate pairs collected, ~10% of 147 total environmental discrete samples
- YSI EXO2 multiparameter sonde specs: temperature accuracy +/-0.2 degC (range -5 to 50 degC); turbidity accuracy +/-0.3 FNU (range 0-4,000 FNU); chlorophyll fluorescence range 0-400 ug/L; phycocyanin fluorescence range 0-100 ug/L; fDOM range 0-300 ug/L as QSE; recording interval 15 minutes
- s::can nitro::lyser II nitrate sensor: accuracy +/-2% + 0.07 mg/L as N, range 0-100 mg/L, resolution 0.005 mg/L
- Hach Nitratax plus sc nitrate sensor: accuracy +/-3% + 0.5 mg/L as N, detection limit 0.1 mg/L, range 0.1-100 mg/L
- Sea-Bird HydroCycle PO4 orthophosphate sensor: accuracy +/-0.0015 mg/L as P, detection limit 0.002 mg/L as P, reporting limit 0.008 mg/L as P, range 0-0.3 mg/L as P
- USGS National Water Quality Laboratory nitrate+nitrite: detection limit 0.04 mg/L as N, reporting limit 0.08 mg/L as N, precision 20% RPD, bias 70-130% recovery
- USGS lab DOC method: detection limit 0.23 mg/L, reporting limit 0.46 mg/L
- Study platforms: ~40 separate instruments per platform generating >200 time series and >10,000 data points/day
- Study period: June-November 2019 at all three lakes (Seneca, Owasco, Skaneateles); June-October 2020 at Seneca and Owasco only
- Lake morphometry: Seneca surface area ~175 km^2, max depth ~200 m, volume ~15,500 million m^3; Owasco surface area ~30 km^2, max depth ~50 m, volume ~780 million m^3; Skaneateles surface area ~40 km^2, max depth ~90 m, volume ~1,600 million m^3
- Regional context: Finger Lakes region drainage basin ~23,310 km^2, ~35% of New York State; in 2017 all 11 Finger Lakes experienced open-water, shoreline, or both types of CyanoHABs

## Methods
Three open-water monitoring platforms (aluminum barges) were deployed on Seneca, Owasco, and Skaneateles Lakes (Seneca and Owasco in both 2019 and 2020; Skaneateles in 2019 only), each instrumented with: three YSI EXO2 multiparameter sondes (near-surface, mid-depth, near-bottom) measuring temperature, specific conductance, dissolved oxygen, pH, turbidity, chlorophyll fluorescence, phycocyanin fluorescence, and fDOM (15-min interval); a nitrate optical sensor (s::can nitro::lyser II in 2019, Hach Nitratax plus sc in 2020); a Sea-Bird Scientific HydroCycle PO4 orthophosphate sensor; a Turner Designs PhytoFind multichannel fluorometer (chlorophyll, phycocyanin, phycoerythrin, algal-group pigments, fDOM); HOBO UA-002-64 temperature/light loggers at 1-m depth intervals; a LI-COR LI-190R PAR sensor; and a Vaisala WTX536 weather station. Roughly every two weeks, discrete water samples were collected with a Van Dorn sampler at the same depths and analyzed at the USGS National Water Quality Laboratory (nitrate+nitrite, orthophosphate, dissolved organic carbon, chlorophyll-a) and by PhycoTech, Inc. (phytoplankton taxonomic/biovolume microscopy). Sensor-vs-laboratory agreement was assessed with Pearson's r (linear association), Spearman's rho (monotonic association), and R^2 (variance explained), and multivariate stepwise regression (alpha = 0.05, Real Statistics Resource Pack for Excel) was used to test whether combining sensor parameters improved prediction of chlorophyll-a, total phytoplankton biovolume, and cyanobacterial biovolume beyond univariate fluorescence models. Where methods 'worked': nitrate sensors showed strong pooled agreement with lab values (best at Owasco); chlorophyll fluorescence showed moderate agreement; water temperature was among the strongest correlates of the biological response variables. Where methods 'failed' or were inconclusive: the orthophosphate sensor could not be evaluated (near-universal non-detects in lab reference samples); the fDOM sensor correlated weakly (often negatively) with lab DOC at every lake; phycocyanin fluorescence was not significantly related to cyanobacterial biovolume; and multivariate stepwise regression did not outperform simple fluorescence-based univariate models.

## Stated limitations
The report itself flags: (1) limited explanatory power of chlorophyll-a/biovolume models, possibly because no cyanoHAB events occurred at the specific open-water monitoring locations during the study; (2) a general caveat that Finger Lakes cyanoHABs are often isolated, ephemeral, or spatially heterogeneous, so fixed-point sensors and discrete grab sampling "may not reliably capture elevated concentrations" occurring elsewhere in a lake; (3) the orthophosphate sensor's performance "could not be evaluated" because nearly all lab reference samples were non-detects, and the sensor itself is described as "complex and prone to data loss"; (4) the fDOM sensor's relationship to lab DOC was weak at every lake; (5) nitrate sensors are described as sensitive to ambient temperature with a substantial power requirement; (6) the multichannel fluorometer (PhytoFind) is "complex to operate," required unique DOM-compensation procedures, showed systematic fDOM outliers in ~2% of data, and its full 2019 dataset was excluded entirely for not meeting the study's data-quality goals; (7) substantial data loss occurred in 2019 from daisy-chained sonde wiring (fixed in 2020 with independent cabling) and from biofouling during longer (4-8 week) 2019 deployment intervals (improved in 2020 with 2-week visits); (8) the stepwise multivariate regression was limited to 66 of 147 possible paired observations because of missing sensor data, and PhytoFind/nitrate sensors plus Skaneateles Lake had to be excluded from that analysis for insufficient observations; (9) three of thirteen chlorophyll-a laboratory replicate pairs exceeded the study's 20% RPD acceptance criterion; and (10) the USGS explicitly disclaims that the report ranks, certifies, or guarantees the performance of any technology evaluated.

## Tensions with other findings
The finding that phycocyanin fluorescence from dual-channel sondes was NOT significantly related to cyanobacterial biovolume - and that turbidity was a better indicator of cyanobacterial biovolume than phycocyanin - complicates the common treatment of phycocyanin as a straightforward, reliable in-situ proxy for cyanobacteria abundance elsewhere in HAB literature and monitoring practice; the report frames this as lake/period-specific rather than a universal indictment of phycocyanin sensing, and itself notes the likely confound that the monitored locations may not have experienced actual cyanoHAB conditions during the study window, so the null result may reflect a restricted-range/low-bloom-incidence sample rather than a general failure of phycocyanin sensing. Separately, the source's explicit statement that fixed-point sensor platforms and discrete grab sampling "may not reliably capture elevated concentrations" of spatially heterogeneous cyanoHABs is not a contradiction so much as a direct, citable reinforcement of the rationale for pairing satellite/remote-sensing spatial coverage with in-situ point sensors (e.g., an EPA CyAN-style approach) - it argues against relying on in-situ monitoring alone, which is directly relevant to any project's decision to fuse the two signal types rather than use either in isolation. Finally, the report's conclusion that multivariate sensor-fusion regression did not outperform a simple univariate fluorescence model is a useful clear-eyed counterpoint to any assumption that adding more sensor channels automatically improves predictive power.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - USGS neutrality disclaimer stating the agency does not rank/compare technologies, determine compliance, certify performance or provide guarantees
  - Nitrate sensor technical limitations (temperature sensitivity, substantial power requirements)
  - Phycocyanin performance detail omitted: source also notes multichannel fluorometer's chlorophyll contribution from cyanobacteria showed moderately strong correlation with cyanobacterial biovolume (contrast to dual-channel failure)
  - fDOM relationship detail understated: all three lakes showed negative correlations, not 'several cases'
  - Orthophosphate sensor complexity issues (prone to data loss, inherently difficult to evaluate)
- **Reviewer notes:** The claims demonstrate high fidelity to the source text with no numerical hallucinations and strong traceability to reported results. One claim (Claim 13) uses slightly stronger prescriptive language ('recommends') than the source supports (conditional 'could leverage'), but this is a minor framing issue. Several meaningful technical caveats and details were omitted (USGS neutrality statement, sensor-specific limitations, performance nuances), but these are contextual/supplementary rather than negating the core factual claims. All 12 primary result claims are well-supported with exact correlation coefficients, sample sizes, and directional findings matching source data precisely."

## Provenance
- Canonical URL: https://pubs.usgs.gov/publication/sir20245010/full (no redirect occurred; report DOI: https://doi.org/10.3133/sir20245010; PDF also available at https://pubs.usgs.gov/sir/2024/5010/sir20245010.pdf)
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Single WebFetch on the given URL (https://pubs.usgs.gov/publication/sir20245010/full) returned an extensive, well-organized extraction spanning report identity, key findings, sensor specifications, laboratory/reference methods, statistical methods, platform infrastructure, limitations, lake characteristics, conclusions, and data-availability links (DOI 10.3133/sir20245010; USGS data releases at 10.5066/P9046YOS and 10.5066/P9TP9T1D). No redirect was reported, so url_used and resolved_url are the same. As a corroborating check (not a re-fetch of the report itself), a WebSearch for the report identifier confirmed the report is real and independently indexed with matching title, DOI, lakes (Seneca, Owasco, Skaneateles), study years, and USGS/NYSDEC authorship framing, giving confidence the WebFetch extraction reflects genuine report content rather than a fabrication. I could not independently line-verify every granular sensor-spec figure (e.g., individual accuracy/range values) against the raw PDF/HTML myself, since I have no filesystem or PDF-rendering access in this task; these are reported as extracted rather than independently re-checked digit-by-digit, though their internal consistency (standard manufacturer datasheet conventions, consistent units, cross-referencing between sections) is a good sign of fidelity.
