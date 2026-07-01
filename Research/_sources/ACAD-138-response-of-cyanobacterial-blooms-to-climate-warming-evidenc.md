---
key: ACAD-138
title: Response of cyanobacterial blooms to climate warming: evidence from satellite observations and long-term trends in Lake Taihu in China
authors_or_org: Li, X., Hang, X., Zhu, S., et al. — Scientific Reports 15, 38820 (2025), Springer Nature
year: 2025
url: https://www.nature.com/articles/s41598-025-22633-8?error=cookies_not_supported&code=3bb27a45-ea20-4684-be14-c86836efbcd1
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed open-access journal article (Scientific Reports / Springer Nature)
categories: [basic-science]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Response of cyanobacterial blooms to climate warming: evidence from satellite observations and long-term trends in Lake Taihu in China

> Note: provisional URL was resolved to a primary source. Original: https://www.nature.com/articles/s41598-025-22633-8

**What it is.** A peer-reviewed, open-access study (Scientific Reports, 2025) that fuses 20 years (2003–2022) of MODIS/Aqua and MODIS/Terra satellite imagery (NDVI-based cyanobacterial bloom detection, ~14,600 images) with in-situ hourly meteorological station data (5 ground stations run by the Jiangsu Climate Center) to quantify how local climate warming has changed the extent, frequency, onset/offset timing, duration and spatial distribution of cyanobacterial blooms in Lake Taihu, China, and to characterize an empirical "S-shaped" bloom–temperature response curve.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Lake Taihu's annual average air temperature rose over 2003–2022 (mean 17.1°C), increasing by about 0.4°C per decade; linear trend Tyear = 0.04t + 16.86 (R = 0.49, p < 0.05).
  - *evidence:* Linear regression of the 20-year annual mean temperature series from 5 meteorological stations; the paper reports the equation, R and significance directly. (Results – regional temperature trend)
  - *quote:* "average increase of 0.4 °C per decade"
- **[✓ verified]** The headline dose–response finding: for every 1°C rise in annual average temperature, annual cumulative satellite-detected bloom area is estimated to increase by about 5,377 km² (S = 5377.1T − 78931; R = 0.44, p < 0.05); cumulative bloom area itself trended upward by about 3,566 km²/decade on average.
  - *evidence:* Central quantitative claim, stated in both the abstract and results as a linear regression of annual cumulative bloom area (from satellite) against annual mean temperature (from met stations) across 2003–2022. (Abstract; Results – bloom area regression)
  - *quote:* "for every 1 °C increase in the annual average temperature, the annual cumulative area of cyanobacterial blooms will increase by approximately 5377 km2"
- **[⚠ partial]** The first observed bloom date (FOD) each year shifted earlier over the record — about 39 days/decade earlier on average (41 days earlier comparing the second half of the record to the first) — and is negatively correlated with winter–spring (Dec–May) mean temperature (FOD = −0.02·TWin-Spr + 12.55; R = −0.73), a temperature series that itself rose ~0.7°C/decade.
  - *evidence:* Regression of day-of-year of first satellite-detected bloom against winter-spring mean temperature, plus a direct first-decade-vs-second-decade comparison. (Abstract; Results – bloom phenology (FOD))
  - *quote:* "FOD in the second decade was 41 days earlier than that in the first decade"
  - *reviewer:* Claim specifies month range as '(Dec–May)' but source text only says 'winter–spring' without explicitly stating these months in the provided excerpt.
- **[✓ verified]** The last observed bloom date (LOD) each year shifted later — about 18 days/decade later on average (23 days later in the second half of the record vs. the first) — and is positively correlated with November–December mean temperature (LOD = 0.02·TNov-Dec + 2.34; R = 0.6); the Nov–Dec temperature trend itself was weak (TNov-Dec = 0.02t − 21.49, R = 0.11).
  - *evidence:* Same regression/decade-comparison approach as FOD, applied to the last day-of-year a bloom was detected by satellite. (Abstract; Results – bloom phenology (LOD))
  - *quote:* "delay of 18 days per decade"
- **[✓ verified]** The annual cyanobacterial bloom season lengthened, from 238 days in the first decade of the record to 302 days in the second decade — a 27% increase in duration.
  - *evidence:* Direct comparison of bloom-season length (span between FOD and LOD) between the first and second halves of the 2003–2022 record. (Results – bloom duration)
  - *quote:* "from 238 days in the first decade to 302 days in the second decade, an increase of 27%"
- **[✓ verified]** The relationship between temperature and bloom extent/frequency follows an empirical S-shaped curve: blooms are rarely observed below 5°C; area and frequency both exceed 10% of their annual totals at 15°C, rising above 20% at 20°C; both peak at 30°C (32% of area, 28% of frequency); and both decline sharply above 30°C.
  - *evidence:* Built by binning temperature into eight 5°C-wide intervals and computing the share of total bloom area/frequency falling in each bin, pooled across the 20-year record. (Results – temperature response curve)
  - *quote:* "area and frequency proportion reaching 32% and 28%, respectively"
- **[✓ verified]** The annual frequency (count) of satellite-detected bloom events shows a continuous increasing trend over 2003–2022 (Frequencyyear = 5.69t + 38.86).
  - *evidence:* Linear trend fit of yearly bloom-event counts. The fetched summary renders the fit statistic as "R**=0.92", which is ambiguous notation (possibly R², possibly a formatting artifact for R — see fetch_notes); reported here as given, not resolved. (Results – bloom frequency trend)
  - *quote:* "continuous increasing trend"
- **[✓ verified]** 2006–2007, 2017 and 2019–2020 were the most severe bloom periods in the 20-year record, with annual bloom areas roughly 30% above the long-term average; 2003, 2004, 2009 and 2014 had areas roughly 30% below average.
  - *evidence:* Based on comparing each year's cumulative satellite-detected bloom area to the 20-year mean. (Results – interannual variability / spatial distribution)
  - *quote:* "areas in 2006, 2007, 2017, 2019, and 2020 were 30% greater than average"
- **[✓ verified]** Bloom extent was mapped from 14,600 MODIS/Aqua and MODIS/Terra images (2003–2022, cloud-masked and 6S-atmospherically-corrected) using an NDVI-based threshold of −0.02, calibrated from 100 paired MODIS RGB/NDVI images (candidate thresholds ranged −0.0086 to −0.0325); 1,973 images retained a detectable bloom area ≥1 km².
  - *evidence:* Methods description of satellite dataset volume, preprocessing, and the empirically calibrated NDVI bloom-detection threshold. (Methods – satellite data and NDVI algorithm)
  - *quote:* "-0.0086 to −0.0325 with an average of −0.02"
- **[✓ verified]** The authors themselves caution that temperature alone does not fully explain interannual bloom variability — e.g., 2004 and 2016–2020 had similar average annual temperatures but markedly different cumulative bloom areas — attributing residual variation to other climatic factors, nutrient levels and human intervention, and stating no single climatic factor can comprehensively describe bloom dynamics.
  - *evidence:* Stated directly in the paper's own discussion of the limits of its temperature-only regression framework; also flags that the common 'control variable method' for isolating single-factor contributions 'has obvious limitations.' (Discussion/Limitations)
  - *quote:* "no single climatic factor such as temperature, wind, precipitation, or sunlight can comprehensively describe the potential linkages"

## Data / numbers
- Study period: 2003–2022 (20 years)
- Lake Taihu area: ≈2338 km²; average depth: 1.9 m (described as third-largest freshwater lake in China)
- Reported coordinates: 30°50′–32°80′N, 119°80′–121°55′E (minute values >59 are internally inconsistent — likely a transcription/OCR artifact in the source extraction; reported as-is, not corrected)
- Satellite images used: 14,600 MODIS/Aqua + MODIS/Terra images (2003–2022)
- Images retained with detectable bloom (≥1 km²): 1,973 images
- NDVI bloom threshold: −0.02 (candidate range −0.0086 to −0.0325, calibrated from 100 image pairs)
- Meteorological stations: 5 (Dongshan, Wujiang, Suzhou, Wuxi, Yixing), hourly data, 2003–2022, per standard GB/T 35226−2017
- Annual mean temperature: 17.1°C; trend +0.4°C/decade; Tyear = 0.04t + 16.86, R = 0.49, p < 0.05
- Seasonal warming rate: 0.2–0.7°C/decade; spring/winter ≈0.6°C/decade vs. summer/autumn ≈0.2°C/decade
- Winter–spring (Dec–May) temperature trend: +0.7°C/decade
- Nov–Dec temperature trend: TNov-Dec = 0.02t − 21.49, R = 0.11
- Bloom-area sensitivity to warming: +5,377 km² per +1°C annual mean temperature; S = 5377.1T − 78931, R = 0.44, p < 0.05
- Cumulative annual bloom area trend: +3,566 km²/decade (average)
- Bloom frequency trend: Frequencyyear = 5.69t + 38.86 (fit statistic reported as "R**=0.92" — notation ambiguous, see fetch_notes)
- First Observed Date (FOD) shift: ≈39 days/decade earlier on average; 41 days earlier in decade 2 vs decade 1; FOD = −0.02·TWin-Spr + 12.55, R = −0.73
- Last Observed Date (LOD) shift: ≈18 days/decade later on average; 23 days later in decade 2 vs decade 1; LOD = 0.02·TNov-Dec + 2.34, R = 0.6
- Bloom season duration: 238 days (decade 1) → 302 days (decade 2); +27%
- Temperature-response bins: 8 bins of 5°C width; blooms rare below 5°C; >10% of area/frequency at 15°C; >20% at 20°C; peak 32% (area) / 28% (frequency) at 30°C; sharp decline above 30°C
- Phase-wise temperature correlations: Phase I 2003–2007 R=0.74 (rising trend); Phase II 2008–2012 R=0.77 (falling trend); Phase III 2013–2022 R=0.37 (rising trend)
- Severe bloom years (~30% above average area): 2006, 2007, 2017, 2019, 2020
- Low bloom years (~30% below average area): 2003, 2004, 2009, 2014
- Representative years used for spatial-distribution analysis: 2003, 2007, 2011, 2015, 2019, 2022
- DOI: 10.1038/s41598-025-22633-8; Scientific Reports 15, 38820 (2025) (from cross-check search, not the fetched body text)

## Methods
MODIS/Aqua and MODIS/Terra imagery (14,600 scenes, 2003–2022), cloud-masked with MOD35/MYD35 products and atmospheric-corrected with the 6S radiative-transfer model; bloom pixels delineated via an NDVI-based method (NDVI = (ρNIR−ρRED)/(ρNIR+ρRED)) with an empirically calibrated threshold of −0.02 (from 100 paired MODIS RGB/NDVI images); 1,973 images retained bloom area ≥1 km². In-situ hourly air-temperature data from 5 ground meteorological stations (Jiangsu Climate Center, per national standard GB/T 35226−2017), 2003–2022. Statistical approach: simple linear trend fits (T = kt+b) and Pearson-style correlation/regression (R, with p<0.05/p<0.01 significance) relating temperature to bloom area, frequency, first/last observed dates; temperature binned into eight 5°C intervals to build an empirical S-shaped dose–response curve; first-decade-vs-second-decade comparisons for phenology and duration; three "phase" sub-periods (2003–2007, 2008–2012, 2013–2022) analyzed separately for temperature-trend strength. The source reports the main temperature–bloom-area, FOD and LOD relationships as statistically significant (p<0.05) but explicitly states this single-factor (temperature-only) framework leaves substantial variance unexplained (see limitations), and that the Nov–Dec temperature trend used to explain LOD was itself weak (R=0.11) and Phase III's temperature trend fit was comparatively weak (R=0.37).

## Stated limitations
The paper states: (1) "no single climatic factor such as temperature, wind, precipitation, or sunlight can comprehensively describe" bloom linkages, since blooms result from "synergistic effects of various climatic factors"; (2) temperature alone leaves large unexplained variance — years with similar mean temperature (2004 vs. 2016–2020) show very different cumulative bloom areas, implying "changes in other climatic factors, nutrient levels, and human intervention may influence cyanobacterial blooms"; (3) general remote-sensing caveats — "atmospheric effects, cloud cover, and aquatic plants can interfere with the accurate acquisition of cyanobacteria information in inland waters," and "there is no universally applicable remote sensing inversion algorithm for cyanobacterial blooms"; (4) the "control variable method" commonly used in this field to isolate individual climatic factors' contributions "has obvious limitations"; (5) spatial coverage gap — the eastern coastal area of Lake Taihu, "a clean water area with abundant of aquatic plants," was excluded from the study.

## Tensions with other findings
The paper's own limitations section already undercuts a simple "warming alone drives blooms" reading: it explicitly notes that years with near-identical mean temperature had very different bloom extents and attributes the gap to nutrients and human intervention, and that no single climatic factor can fully explain bloom dynamics. Despite this, the abstract/conclusion use causal-sounding language ("climate warming promotes/drives the expansion of cyanobacterial blooms") that is stronger than what a purely correlational satellite-vs-meteorology regression (Pearson R, simple linear/decade-comparison trends, no confidence intervals reported) can rigorously support — a caution worth carrying into any downstream driver claims. Titles surfaced in a supporting search (e.g., a separate ScienceDirect paper on "Contributions of meteorology and nutrient to the surface cyanobacterial blooms... in Lake Taihu") suggest other literature on this same lake frames bloom drivers as jointly meteorological-and-nutrient rather than temperature-centric; this is noted only as a title-level observation since that source was not fetched or verified here, not as a confirmed contradiction.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Source notes that satellite detection can be interfered with by 'atmospheric effects, cloud cover, and aquatic plants,' and that 'there is no universally applicable remote sensing inversion algorithm for cyanobacterial blooms'
  - Source states the eastern coastal area (clean water with abundant aquatic plants) was excluded from the study
  - Source notes the 'control variable method' used to quantify single-factor contributions 'has obvious limitations'
- **Reviewer notes:** All quantitative claims trace directly to the source text with high fidelity. One claim (FOD phenology) adds an explicit month specification '(Dec–May)' that, while reasonable as a standard interpretation of 'winter–spring,' is not explicitly stated in the provided source text excerpt. No numbers are hallucinated; all figures, equations, and coefficients match the source exactly. The extraction appropriately omits methodological limitations and caveats, capturing only substantive findings. The source was marked as published in Scientific Reports (2025) and attribution is clear."

## Provenance
- Canonical URL: https://www.nature.com/articles/s41598-025-22633-8?error=cookies_not_supported&code=3bb27a45-ea20-4684-be14-c86836efbcd1
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: WebFetch on the primary URL triggered Nature's standard identity-provider cookie redirect chain (nature.com → idp.nature.com/authorize → idp.nature.com/transit → back to nature.com/articles/...?error=cookies_not_supported); following the chain as instructed by the tool's own redirect messages landed on the article page and returned a detailed, structured extraction (verbatim abstract, specific regression equations/R/p values, named meteorological stations, NDVI calibration procedure, limitations/discussion, conclusion) consistent with full-text access to an open-access Scientific Reports article, not just an abstract. Cross-checked via WebSearch: the abstract text, headline numbers (5,377 km²/°C; R=−0.73 FOD; R=0.6 LOD; 39 days/decade; 18 days/decade), title, and citation (Li, X., Hang, X., Zhu, S. et al., Sci Rep 15, 38820 (2025), DOI 10.1038/s41598-025-22633-8) all matched independently across two separate searches, giving confidence the WebFetch content is genuine rather than fabricated. Two notational issues to flag for any reviewer: (a) the fetched summary uses \"R**\" for the FOD, LOD and frequency-trend fit statistics while using plain \"R\" elsewhere for numerically identical values (the abstract states \"R = -0.73\" and \"R = 0.6\" for the same FOD/LOD relationships) — since R² cannot be negative, \"R**=-0.73\" cannot literally be R-squared, so this is almost certainly a markdown-bolding artifact for plain R rather than a distinct statistic, though this is inferred rather than directly confirmed in the source text; (b) the reported lake coordinate string (\"32°80'N\", \"119°80'E\") contains minute values above 59, which is internally impossible for degree-minute notation and is likely a transcription artifact — reported verbatim rather than corrected. No numeric confidence intervals (only R and p-value thresholds) were reported by the source for any regression.
