---
key: ACAD-066
title: Limnological data derived from high frequency monitoring buoys are asynchronous in a large lake
authors_or_org: Stevens C, Frost PC, Pearce NJT, Kelley JD, Zastepa A, Xenopoulos MA
year: 2025
url: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314582 (cross-checked against PMC mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC11884689/)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, open access (PLOS ONE, Vol. 20, Issue 3, Article e0314582, published March 6, 2025; DOI 10.1371/journal.pone.0314582)
categories: [in-situ-and-weather-data, treatment-and-management]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Limnological data derived from high frequency monitoring buoys are asynchronous in a large lake

> Note: provisional URL was resolved to a primary source. Original: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314582

**What it is.** An open-access PLOS ONE study (Stevens et al., 2025) that used two warm seasons (May–October 2021 and 2022) of hourly sensor data from 10 static high-frequency monitoring buoys in the western basin of Lake Erie to quantify spatial synchrony/asynchrony of water temperature, dissolved oxygen, turbidity, chlorophyll-a and phycocyanin between buoy pairs, and to translate those synchrony patterns into practical buoy-spacing guidance for monitoring-network design.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Water temperature was highly synchronous across the buoy network, whereas dissolved oxygen, turbidity, chlorophyll-a and phycocyanin were asynchronous.
  - *evidence:* Stated directly in the abstract and confirmed in Results, where temperature's pairwise Pearson r values (0.89–0.99 in 2021; 0.63–0.99 in 2022) are far higher and tighter than the other four variables, which ranged widely and included negative correlations between some buoy pairs. (Abstract; Results)
  - *quote:* "water temperature was highly synchronous whereas dissolved oxygen, turbidity, chlorophyll and phycocyanin were asynchronous"
- **[✓ verified]** The degree of asynchrony increased with increasing spatial distance between buoy pairs, significantly so for dissolved oxygen (both years), turbidity and chlorophyll (2022), and temperature (2022).
  - *evidence:* Non-parametric Siegel repeated-medians regressions of pairwise Pearson r on inter-buoy distance were statistically significant with negative slopes for these variable-year combinations. (Abstract; Results/Table 2)
  - *quote:* "The extent of this asynchrony was higher with increasing spatial distance between buoys."
- **[✓ verified]** Using r=0.5 ('moderately strong') as the synchrony threshold, the predicted buoy separation needed to reach that correlation was far larger for temperature (~108 km) than for the bio-optical/chemical variables (~18–46 km).
  - *evidence:* Derived from the fitted distance-correlation regression models per variable, solved for the distance at which predicted r=0.5. (Methods (threshold definition); Table 2)
  - *quote:* "a coefficient of 0.5 is generally accepted as being a moderately strong correlation"
- **[✓ verified]** Extrapolating the dissolved-oxygen distance-correlation model to the entire surface of Lake Erie (not just the western basin), the authors calculate at least 1,239 buoys would be needed to fully resolve its spatial complexity.
  - *evidence:* Stated as the authors' own back-of-envelope calculation built on the Table 2 dissolved-oxygen spacing estimate. (Discussion)
  - *quote:* "at least 1,239 buoys are needed across Lake Erie"
- **[✓ verified]** Moran's Index values were close to zero for every variable studied, including temperature, indicating no classic spatial autocorrelation even where the distance-correlation regressions were statistically significant.
  - *evidence:* Reported as a distinct spatial-statistics result alongside the correlation and DTW analyses; the two analyses (Moran's I vs. distance-regression) appear to disagree on 'spatial structure,' which the authors relate to non-continuous, patchy movement of water masses rather than smooth gradients. (Results)
  - *quote:* "all had MI values very close to zero, indicating no spatial autocorrelation"
- **[✓ verified]** The ten-buoy network did not capture the full spatial complexity of the western basin, and data from an individual buoy should not be extrapolated to conditions (including cyanobacterial blooms) outside the area it monitors.
  - *evidence:* Stated as the study's central practical conclusion for monitoring-network users. (Discussion)
  - *quote:* "should not be used to draw conclusions about cHABs outside of the area which the buoys monitors"
- **[✓ verified]** Synchrony was generally higher near the start (May) and end (October) of the sampling season, with turbidity, chlorophyll and phycocyanin least synchronous during August-September.
  - *evidence:* Time-resolved correlation analysis showed a within-season pattern coinciding with the peak cyanobacterial bloom period in western Lake Erie. (Results/Discussion)
  - *quote:* "Turbidity, chlorophyll, and phycocyanin were typically the least synchronous during August and September"
- **[✓ verified]** The authors interpret the observed asynchrony as reflecting basin hydrodynamics (Detroit and Maumee River inflows, wind-driven mixing, weak/variable stratification, hypoxic backflow from the central basin) combined with spatially patchy biological processes such as localized cyanobacterial blooms -- an interpretation of plausible mechanism, not a causally demonstrated effect.
  - *evidence:* Presented in the Discussion as the authors' explanatory narrative for the quantitative synchrony patterns; the study itself is correlational (distance vs. correlation coefficient) and does not test these mechanisms directly. (Discussion)
  - *quote:* "a windspeed of only 6 m s⁻¹ is needed to vertically mix the western basin"
- **[✓ verified]** The authors recommend that buoy placement be tailored to specific monitoring objectives and that anchored high-frequency buoys be supplemented with other data-collection methods, since no monitoring program can feasibly deploy enough buoys to fully resolve spatial complexity in a large lake.
  - *evidence:* Stated as a practical recommendation following directly from the quantified buoy-spacing requirements. (Discussion/Conclusion)
  - *quote:* "it is unreasonable to assume in the case of large lakes, one would have the resources to deploy enough buoys to capture the full complexity of the system"
- **[✓ verified]** The buoy-spacing guidance is derived from a single region of a single lake over one warm season repeated across two years, and the authors caution against generalizing without testing on other large lakes.
  - *evidence:* Explicit generalizability caveat given by the authors themselves. (Discussion/Limitations)
  - *quote:* "the findings of Table 2 do only represent one region of a single lake"
- **[✓ verified]** The study used only surface-water sensor data, which the authors acknowledge limits its ability to investigate vertical (depth-related) processes.
  - *evidence:* Directly stated limitation. (Limitations)
  - *quote:* "this study only uses data collected at the surface, and in that regard it is difficult to investigate vertical processes"
- **[✓ verified]** Western Lake Erie is a major drinking-water source (about 11 million people) that experiences recurrent nuisance and harmful cyanobacterial blooms, which motivates the high-frequency monitoring network this study analyzes.
  - *evidence:* Background/motivation given in the introduction to justify the monitoring context; not itself a novel finding. (Introduction)
  - *quote:* "a source of drinking water for 11 million people"

## Data / numbers
- Western basin of Lake Erie surface area = 3,282 km²
- Western basin average depth = 7.4 m
- Western basin wind fetch ≈ 388 km (as extracted; background limnology context)
- 10 static monitoring buoys (abstract phrasing: '10 pairs of static buoys'), deployed 2021 and/or 2022 via the Seagull-GLOS platform
- Study period: May–October in each of 2021 and 2022
- Temperature Pearson r: 0.89–0.99 (2021); 0.63–0.99 (2022)
- Temperature vs. distance: 2022 p=0.01, r=-0.39; predicted buoy spacing for r=0.5: 108.10 km (SD=39.44)
- Brunt-Väisälä frequency (stratification) Pearson r: 0.28–0.85 (2021); 0.48–0.85 (2022); derived from n=4 profiling buoys
- Example stratification heterogeneity: 6.96×10⁻⁵ at one buoy vs. 2.55×10⁻³ at a buoy 18.6 km away, same time
- Dissolved oxygen: average r=0.39 (2021), 0.46 (2022); vs. distance: 2021 p=0.004, r=-0.52; 2022 p=1.2×10⁻⁴, r=-0.59; predicted spacing for r=0.5: 20.88 km (SD=0.23); 2022 DTW=0.23 (highest of all variables)
- Turbidity: average r=0.18 (2021), 0.09 (2022); 2022 range r=-0.30 to 0.70; vs. distance (2022): p=4.5×10⁻⁶, r=-0.62; predicted spacing for r=0.5: 24.34 km (SD=16.73)
- Chlorophyll-a: DTW=0.30 (2021), 0.19 (2022); 2021 r range -0.33 to 0.80; vs. distance 2022: p=1.4×10⁻⁶, r=-0.77 (2021 not significant, p=0.20); predicted spacing for r=0.5: 17.61 km (SD=34.19); DTW vs. distance 2022: p=3.52×10⁻², r=0.39
- Phycocyanin: DTW=0.23 (2021), 0.19 (2022); 2021 r range -0.62 to 0.76; predicted spacing for r=0.5 (2021): 46.43 km; model weak fit (2022 p=0.11; 2021 p=0.05)
- Correlation threshold used to define 'moderately strong' synchrony for all spacing predictions: r=0.5
- Estimated buoys needed to fully resolve dissolved-oxygen spatial complexity across all of Lake Erie (not just western basin): ≥ 1,239
- Wind speed sufficient to vertically mix the western basin: 6 m/s; basin stratified roughly 60% of the time
- Lake Erie supplies drinking water to approximately 11 million people
- ~99.994% of world's lakes reported as <10 km² surface area in one extraction pass; a second pass reported most global lakes sized '0.001 to 0.01 km²' (both attributed to the source, not word-for-word reconciled)
- Publication record: PLOS ONE, Volume 20, Issue 3, Article e0314582, published 6 March 2025, DOI 10.1371/journal.pone.0314582

## Methods
Data: hourly-averaged, per-buoy z-score-standardized surface sensor records (temperature, dissolved oxygen, chlorophyll-a, phycocyanin, turbidity) from 10 static buoys (multi-institutional, accessed via the Seagull-GLOS platform) in the western basin of Lake Erie, May-Oct 2021 and May-Oct 2022; missing observations were left blank rather than interpolated. A stratification metric, Brunt-Väisälä frequency, was derived from paired surface/bottom temperature profiles at the subset of buoys (n=4) equipped with profiling sensors, computed with the R package rLakeAnalyzer. Synchrony was assessed three ways: (1) pairwise Pearson correlation coefficients across all buoy-pair combinations (R package rendered in extraction as "Ggally", almost certainly GGally); (2) Dynamic Time Warping (DTW) distance between buoy time series (R package 'dtw'), normalized so 0 = perfect synchrony; (3) Moran's Index (R package 'ape') to test spatial autocorrelation (range -1 to 1; 0 = none). The relationship between inter-buoy geographic distance and Pearson r (or DTW) was fit with non-parametric, median-based linear regression (Siegel's repeated medians, R package 'mblm'), with significance assessed via Wilcoxon rank-sum tests; fitted models were solved for the buoy separation distance predicted to yield r = 0.5, a value the authors state was chosen "because a coefficient of 0.5 is generally accepted as being a moderately strong correlation." Daily wind-speed data (R package 'openmeteo') were compared against daily correlation coefficients. All analysis in R (ggplot2 for plotting). The approach worked well (statistically significant, interpretable distance-decay relationships) for dissolved oxygen, turbidity, and chlorophyll in 2022, and for temperature; it worked poorly/was not significant for chlorophyll in 2021 (p=0.20) and for phycocyanin in both years (2021 p=0.05, 2022 p=0.11), and Moran's I registered near-zero (no detectable classic spatial autocorrelation) for every variable including the ones the correlation-distance models flagged as significantly distance-dependent — the authors attribute this apparent conflict to the lake's spatial structure being driven by discrete, moving water masses rather than smooth continuous gradients.

## Stated limitations
The authors state: the analysis "only uses data collected at the surface," making vertical/depth processes hard to investigate; the western basin is typically well-mixed so surface sensors may still capture some vertical flux, but this is not verified. The buoy-spacing guidance (their Table 2) "only represent[s] one region of a single lake," and the underlying distance-correlation model "has only been tested on one, very large lake," so the authors explicitly call for repeating the synchrony analysis on other large-lake ecosystems before generalizing. The chosen correlation threshold (r=0.5) is a judgment call ("moderately strong"); the authors note a stricter (r=0.75) or looser (r=0.25) threshold would give different spacing distances, representing a trade-off, not a single "correct" number. Missing sensor data were left blank rather than interpolated. The study window is restricted to May-October in two years, so behavior outside that seasonal window is unexamined. The authors also acknowledge practical/resource limits: "it is unreasonable to assume in the case of large lakes, one would have the resources to deploy enough buoys to capture the full complexity of the system," and recommend buoys be supplemented with in-situ sampling, remote sensing, and autonomous platforms rather than relied on alone.

## Tensions with other findings
The paper's own logic (not a claim it makes about other specific studies) creates a load-bearing tension for any HAB workflow that treats one in-situ buoy or station as spatially representative of a lake/basin: for the cyanoHAB-relevant variables (chlorophyll-a, phycocyanin), predicted buoy spacing for even a "moderately strong" correlation (r=0.5) was only ~17.6-46.4 km in a basin whose real buoy network is sparser than that in places, and the authors explicitly warn single-buoy data "should not be used to draw conclusions...outside of the area which the buoys monitor." That directly complicates (a) using a single in-situ station to validate or calibrate a satellite-derived cyanobacteria product over a whole lake/basin, and (b) extrapolating one buoy's bloom pigment reading into a lake-wide risk call — both relevant to a HAB tool that fuses remote sensing with in-situ data, since it implies satellite coverage is doing real informational work that sparse buoys cannot, precisely for the pigment variables a HAB early-warning tool cares about most. Conversely, the same study found temperature synchronous over much larger distances (~108 km to drop to r=0.5), suggesting temperature/weather covariates are safer to treat as spatially representative than bio-optical pigment signals — an asymmetry worth carrying into any feature-fusion design.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0

## Provenance
- Canonical URL: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314582 (cross-checked against PMC mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC11884689/)
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary PLOS ONE URL twice with different extraction prompts (one broad/comprehensive, one methods-and-results-focused) as required for a High-relevance source, then reconciled the two into a union. The two passes were highly consistent (same numbers recurred verbatim in both), giving confidence the figures were read off the page rather than invented, though a few phrasings differed slightly (e.g., whether Moran's I near-zero applied only to the four "asynchronous" variables or to temperature as well; two slightly different renderings of the "most lakes are small" statistic). Because this is a High-relevance source, I additionally fetched the PMC open-access mirror (PMC11884689) with a targeted prompt to resolve ambiguities left open by the first two passes: exact abstract wording, full author/affiliation list, journal volume/issue/date/DOI, the precise rationale for the r=0.5 threshold, and whether the "1,239 buoys" figure referred to the western basin or all of Lake Erie (confirmed: all of Lake Erie). One WebSearch confirmed authorship, journal volume/issue, and 2025 publication year/date, since no single fetch pass surfaced a clean citation block. No paywall, CAPTCHA, or robots blocking was encountered; PLOS ONE is fully open access and the PMC mirror independently corroborates the content, so full_text_access is set to "full." Two minor items are flagged as lower-confidence because they were reported by the extraction passes without being re-verified via an exact quote pull: the "388 km" fetch distance figure, and the precise "99.994%"/"0.001 to 0.01 km2" small-lake statistics (two passes gave two different-looking numbers for what may be related but distinct claims about global lake size distribution).
