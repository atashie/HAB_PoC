---
key: ACAD-046
title: Expanding the Application of Sentinel-2 Chlorophyll Monitoring across United States Lakes
authors_or_org: Wilson B. Salls, Blake A. Schaeffer, Nima Pahlevan, Megan M. Coffer, Bridget N. Seegers, P. Jeremy Werdell, Hannah Ferriby, Richard P. Stumpf, Caren E. Binding, Darryl J. Keith (per WebSearch metadata — EPA/NASA/NOAA-affiliated co-authors; not independently confirmed via the fetched article body, which did not display an author byline in the extracted text)
year: 2024
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC11235139/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, open access (Remote Sensing, MDPI, vol. 16, issue 11, article 1977; DOI 10.3390/rs16111977 per WebSearch), hosted on PubMed Central
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Expanding the Application of Sentinel-2 Chlorophyll Monitoring across United States Lakes

**What it is.** A peer-reviewed calibration/validation study that tests two Sentinel-2 MultiSpectral Instrument (S2 MSI) chlorophyll-a algorithms — the Maximum Chlorophyll Index (MCI) and Normalized Difference Chlorophyll Index (NDCI) — against in-situ chlorophyll-a measurements from 103 U.S. lakes (2016–2020), across three atmospheric-processing levels, to assess whether S2's ~20 m resolution can support broad-scale, operational inland-lake trophic-state/eutrophication monitoring (in the spirit of EPA's CyAN program, which uses coarser-resolution Sentinel-3/OLCI imagery).

## Key claims
*(each tagged with its blind-review verdict)*

- **[⚠ partial]** The study calibrated and validated two S2 chlorophyll-a algorithms (MCI, NDCI) using in-situ chlorophyll-a data from 103 lakes across the contiguous U.S. (28 states in the full/calibration dataset), spanning 2016–2020, using three reflectance processing levels (top-of-atmosphere ρt, Rayleigh-corrected ρs, remote-sensing reflectance Rrs).
  - *evidence:* Stated directly in the abstract and reiterated in the methods/data description; sample counts and state counts appear consistently across both fetches. (Abstract; Methods (study area / data sources))
  - *quote:* "They were calibrated and validated using in situ chlorophyll a measurements for 103 lakes across the contiguous U.S."
  - *reviewer:* The '28 states' count and the '2016–2020' time span are not mentioned in the source text. The source confirms 103 lakes, contiguous U.S., and three reflectance types but does not specify geographic extent by state count or temporal span.
- **[✓ verified]** MCI using top-of-atmosphere reflectance (ρt) was the best-performing configuration overall, with a mean absolute error factor (MAEmult) of 2.08 and a mean bias factor (biasmult) of 1.15 on the held-out validation set (n=44), i.e. modeled and observed chlorophyll-a differ by a factor of ~2 on average.
  - *evidence:* Headline result stated in the abstract and repeated in the Table 4 validation-results summary extracted by both fetches. (Abstract; Results, Table 4 (validation results))
  - *quote:* "MCI using ρt showed the best overall performance, with a mean absolute error factor of 2.08 and a mean bias factor of 1.15."
- **[✓ verified]** MCI outperformed NDCI across all three reflectance products tested, based on lower MAEmult/MAPE and comparable or better bias in each of the ρt, ρs, and Rrs conditions (e.g., NDCI/Rrs had r²=0.02 and MAPE=318.4%, far worse than any MCI condition).
  - *evidence:* Direct comparison across the six algorithm x processing-level combinations in the validation table. (Abstract; Results, Table 4)
  - *quote:* "MCI slightly outperformed NDCI across all reflectance products."
- **[✓ verified]** Converting MCI(ρt)-derived chlorophyll-a to a binary trophic-state call (eutrophic-or-above vs. below) reached 82% agreement with in-situ trophic state (36 of 44 validation observations), versus 66% agreement (29 of 44) for the finer 4-class scheme (oligotrophic/mesotrophic/eutrophic/hypereutrophic).
  - *evidence:* Reported as the paper's practical 'management application' headline number, computed against National Lakes Assessment trophic-state thresholds. (Abstract; Results (trophic-state classification))
  - *quote:* "Binary classification that combined the oligotrophic–mesotrophic and eutrophic–hypereutrophic ranges showed increased accuracy of 82% (36 of 44 observations) for ρt"
- **[✓ verified]** NDCI's trophic-state classification was less accurate than MCI's: 47% (23 of 49) for the 4-class scheme and 63% for the binary scheme.
  - *evidence:* Same classification exercise applied to the NDCI(ρt) validation set for comparison against MCI. (Results (trophic-state classification))
  - *quote:* "NDCI: 47% (4-class), 63% (binary)"
- **[⚠ partial]** Both algorithms show a low-concentration detection limit around 10 micrograms per liter; below this, retrievals frequently went negative, and negative-retrieval samples had a much lower median in-situ chlorophyll-a (1.9 µg/L) than positive-retrieval samples (12.0 µg/L), supporting treating negative outputs as effectively non-detections rather than as usable low-end estimates.
  - *evidence:* Statistical separation (implied Mann-Whitney U test per methods) between in-situ chlorophyll-a values underlying negative vs. positive S2-derived retrievals. (Results (detection limits))
  - *quote:* "A rough detection limit around or below 10 μg L−1"
  - *reviewer:* The specific median values (1.9 µg/L and 12.0 µg/L) are stated in the source for MCI only. The source separately reports different values for NDCI (3.5 vs. 8.1 µg/L). Claiming these values apply to 'both algorithms' drops this important caveat.
- **[✓ verified]** The authors contextualize S2-derived error (MAPE ≈ 101% for the best configuration) against literature-reported in-situ chlorophyll-a measurement error, arguing satellite error may not be much larger than the measurement error already inherent in the ground-truth data itself.
  - *evidence:* This is an argument comparing the paper's own MAPE to a cited external error estimate for in-situ sampling methods, used to soften interpretation of the satellite error magnitude — a comparison, not a proof that the two error sources are equivalent. (Discussion (limitations / interpretation of error))
  - *quote:* "in situ sampling methods have an average error of 39%, with error as high as 68%"
- **[✓ verified]** Mineral suspended particulate matter (MSPM) can bias MCI toward false-positive elevated chlorophyll-a; the authors filtered out MSPM-contaminated samples using a spectral baseline-slope threshold, converting a previously published threshold (-1.5×10⁻⁴ nm⁻¹) into S2-equivalent thresholds of -5.0×10⁻⁴ nm⁻¹ (ρt) and -4.8×10⁻⁴ nm⁻¹ (ρs) via a regression relationship between processing levels (r²=0.99).
  - *evidence:* Explicit methodological caveat/correction step described in the data-filtering methods. (Methods (MSPM filtering))
  - *quote:* "MSPM is known to interfere with the MCI algorithm, often resulting in elevated chl a retrievals and potential false positive bloom reports."
- **[✓ verified]** High colored dissolved organic matter (CDOM) tends to cause MCI to underestimate chlorophyll-a; the authors report an inverse relationship between MCI error and dissolved organic carbon, but based on only 8 paired samples (r²=0.65, n=8), i.e. a small, exploratory sub-analysis rather than a robust finding.
  - *evidence:* Authors explicitly attach a small sample size to this correlation, signaling low confidence. (Discussion (limitations, CDOM))
  - *quote:* "high CDOM may interfere with the MCI, generally resulting in underestimation of chl a"
- **[✓ verified]** The calibration/validation samples were geographically uneven, concentrated in the upper Midwest and Eastern U.S.; the Western U.S. was sparsely represented, with the validation set containing only 3 samples from a single lake in the West — limiting confidence that the fitted algorithm generalizes to western U.S. optical water types.
  - *evidence:* Stated limitation about sample geographic distribution and its implication for generalizability. (Discussion (limitations, geographic coverage))
  - *quote:* "The Western U.S. was sparsely represented, particularly by the validation dataset, which included only three samples from one lake."
- **[⚠ partial]** The authors frame this as a maturity advance relative to prior single- or few-lake S2/MERIS chlorophyll algorithm studies (ranging from 1 lake to 12 lakes, ~28–800 observations in works by Ansper & Alikas, Toming et al., Seegers et al., Liu et al., Dörnhöfer et al., Carlson et al., and Pahlevan et al.), by using a much larger, more spatially expansive 103-lake/28-state dataset.
  - *evidence:* Discussion section directly compares this study's r²/MAEmult/biasmult/RMSE figures against seven prior studies' reported statistics to argue for a step up in spatial/statistical scope, though the prior studies vary widely in fit quality (r² from 0.25 to 0.80), indicating algorithm performance is not uniform across settings. (Discussion (comparison to previous studies))
  - *quote:* "This study contributes toward algorithm maturity, transitioning from accuracy assessment using a small number of measurements to employing a larger, more spatiotemporally expansive dataset."
  - *reviewer:* The comparison to prior studies and maturity framing are supported, but '28-state dataset' is not mentioned in the source text (same unsupported geographic detail as Claim 1).
- **[✓ verified]** Sentinel-2 lacks thermal bands (limiting cloud masking) and lacks a ~685 nm band, which the authors say would be needed to harmonize S2 chlorophyll retrievals with MERIS/Sentinel-3 OLCI-based algorithms such as the Cyanobacteria Index, Fluorescence Line Height, and Maximum Peak Height.
  - *evidence:* Stated sensor-design limitation with a specific band-level recommendation for future missions (Landsat Next). (Discussion (limitations / future work))
  - *quote:* "S2 lacks thermal bands, presenting a limitation for developing effective masking"
- **[✓ verified]** The authors suggest an operational monitoring product analogous to EPA's CyAN could be built on S2, citing that S2's finer spatial resolution could extend coverage to 98.8% of qualifying waterbodies plus many rivers and estuaries not resolvable by coarser sensors.
  - *evidence:* Forward-looking application/discussion statement connecting the algorithm-validation results to a potential operational product; this is the authors' framing/aspiration, not a demonstrated operational deployment. (Discussion / Conclusion)
  - *quote:* "An approach similar to CyAN could be developed for S2, which can provide data for 98.8% of those waterbodies as well as many rivers and estuaries."
- **[✓ verified]** A case-study application at Jordan Lake, NC (a eutrophic drinking-water/recreational reservoir) on two 2018 dates showed S2 MCI-derived chlorophyll-a spatial patterns (higher near inflows) and a value range comparable to monthly in-situ monitoring by the NC Department of Environmental Quality (reported in situ range 0-110 µg/L).
  - *evidence:* Illustrative single-lake application example used to demonstrate practical/operational relevance beyond the aggregate statistics. (Results / Case study (Jordan Lake))
  - *quote:* "broad spatial variation in chl a values, with higher concentrations near some inflows"

## Data / numbers
- 103 lakes across 28 states (calibration/full dataset)
- 30 lakes across 12 states (validation-dataset subset, per one extraction — see fetch_notes on possible ambiguity)
- Study period: 2016–2020
- In-situ chlorophyll-a range in dataset: 0.1–132.4 µg/L
- Initial in-situ/satellite matchups: 300
- Matchups retained after MSPM filtering: 294 (for ρt and ρs) / 296 (for Rrs)
- Calibration (training) set: 235–236 samples (~80%)
- Validation (held-out) set: 44–60 samples (~20%), exact n varies by algorithm/product
- MCI ρt validation: MAEmult=2.08, biasmult=1.15, MAPE=100.9%, r²=0.50, n=44
- MCI ρs validation: MAEmult=2.22, biasmult=1.05, MAPE=100.1%, r²=0.49, n=46
- MCI Rrs validation: MAEmult=2.47, biasmult=1.17, MAPE=307.3%, r²=0.47, n=49
- NDCI ρt validation: MAEmult=2.41, biasmult=1.52, MAPE=220.1%, r²=0.46, n=49
- NDCI ρs validation: MAEmult=3.12, biasmult=1.51, MAPE=323.4%, r²=0.31, n=48
- NDCI Rrs validation: MAEmult=2.68, biasmult=1.53, MAPE=318.4%, r²=0.02, n=48
- MCI trophic-state accuracy: 66% (4-class, 29/44); 82% (binary, 36/44)
- NDCI trophic-state accuracy: 47% (4-class, 23/49); 63% (binary)
- National Lakes Assessment trophic-state thresholds used: Oligotrophic ≤2 µg/L; Mesotrophic >2–≤7 µg/L; Eutrophic >7–≤30 µg/L; Hypereutrophic >30 µg/L
- MCI detection limit: ~10 µg/L; median in-situ chl-a for non-detects = 1.9 µg/L (n=15) vs. 12.0 µg/L for positive detections
- NDCI detection separation: median 3.5 µg/L (negative) vs. 8.1 µg/L (positive)
- Negative-retrieval counts removed: MCI ρt=15, MCI ρs=13, MCI Rrs=11, NDCI ρt=10
- MSPM baseline-slope filtering threshold: original literature value -1.5×10⁻⁴ nm⁻¹; S2-converted thresholds: ρt=-5.0×10⁻⁴ nm⁻¹, ρs=-4.8×10⁻⁴ nm⁻¹; conversion relationship r²=0.99
- CDOM vs. MCI error correlation: r²=0.65, n=8 (small sample)
- MCI(ρt) calibration coefficients: β1=3586 (95% CI 2802–42354), β0=6.27 (95% CI 5.26–7.87) — note the very wide CI on β1, spanning roughly an order of magnitude
- Error by trophic state, MCI ρt: Oligotrophic MAEmult=7.35/biasmult=0.46 (n=3); Mesotrophic MAEmult=2.37/biasmult=1.48 (n=10); Eutrophic MAEmult=1.88/biasmult=1.33 (n=21); Hypereutrophic MAEmult=1.54/biasmult=0.87 (n=10)
- In-situ chlorophyll-a sampling method error (cited from prior literature): average 39%, up to 68%
- S2 MSI bands used: 665 nm, 705 nm, 740 nm (MCI); 665 nm, 705 nm (NDCI)
- Satellite processing resolution: 20 m (from 3×3 pixel box), via NASA SeaDAS
- Matchup time window: ±12 hours (general); ±30 minutes (coastal)
- Sample depth restriction: ≤2 m; ≥30 m from shoreline
- Bootstrap iterations for CI estimation: 1000
- Jordan Lake, NC case-study dates: 14 May 2018 and 1 October 2018; NC DEQ in-situ chl-a range: 0–110 µg/L
- CyAN-comparable coverage claim: 98.8% of qualifying waterbodies
- Prior-study comparison figures cited in Discussion: Ansper & Alikas (12 lakes) β1=870.8, β0=25.3, r²=0.25; Toming et al. (11 lakes) β1=2231, β0=12.7, r²=0.80; Seegers et al. (348 obs, MERIS Cyanobacteria Index) MAEmult=1.62, biasmult=1.11; Liu et al. (273 obs, range 0.00–120.99 µg/L) MCI MAPE=70.1% (best of 9 algorithms); Dörnhöfer et al. (28 pts, 1 lake) NDCI RMSE=4.70 µg/L, r²=0.71; Carlson et al. (28 pts, 1 lake) ensemble RMSE=4.1 µg/L; Pahlevan et al. (>800 S2 obs, global ML) MAEmult≈1.80 (~80% uncertainty), biasmult≈1.41 (~41% bias)

## Methods
Two spectral-index algorithms — Maximum Chlorophyll Index (MCI = Rb − Ra − [(λb−λa)/(λc−λa)]×(Rc−Ra), using 665/705/740 nm) and Normalized Difference Chlorophyll Index (NDCI = (Rb−Ra)/(Rb+Ra), using 665/705 nm) — were computed from Sentinel-2 MSI imagery processed through NASA's SeaDAS software at three levels (top-of-atmosphere ρt, Rayleigh-corrected ρs, remote-sensing reflectance Rrs), resampled to 20 m via 3×3-pixel averaging. In-situ chlorophyll-a data came from the U.S. Water Quality Portal, USGS NWIS, the Wisconsin DNR repository, Environment and Climate Change Canada, and the AquaSat repository, matched to satellite overpasses within ±12 hours (±30 min in coastal areas), restricted to samples ≤2 m deep and ≥30 m from shore within NHDPlus V2 lake polygons. Samples suspected of mineral-sediment (MSPM) contamination were removed via a spectral baseline-slope threshold. Calibration used Ranged Major Axis (Model II) regression — chosen because both satellite and in-situ variables carry measurement error — with parameter uncertainty estimated via 1000-iteration bootstrapping (bias-corrected, accelerated CIs); an 80/20 calibration/validation split was used, with performance judged by MAEmult, biasmult, MAPE, r², and agreement with National Lakes Assessment trophic-state categories (4-class and binary). The method performs best (lowest error/bias) for MCI on ρt in eutrophic-to-hypereutrophic waters (in-situ chl-a >7 µg/L); it performs worst — and becomes statistically unreliable (e.g., NDCI on Rrs: r²=0.02) — at oligotrophic concentrations (<2 µg/L), in the presence of high mineral sediment or high CDOM, and below a ~10 µg/L detection floor where retrievals frequently go negative.

## Stated limitations
The authors themselves flag: (1) a ~10 µg/L lower detection limit below which both indices, especially NDCI, become unreliable or produce non-physical negative values; (2) mineral suspended particulate matter (MSPM) can cause false-positive elevated MCI retrievals, requiring a filtering step; (3) high CDOM can cause MCI underestimation, though this relationship is based on only 8 samples; (4) NDCI on Rrs shows extremely broad, even negative-inclusive confidence intervals, so the authors advise caution using Rrs for NDCI; (5) in-situ reference data itself carries substantial measurement error (39% average, up to 68% per cited prior work), complicating interpretation of the ~101% MAPE the satellite algorithm shows; (6) geographic sampling is concentrated in the upper Midwest/Eastern U.S., with the Western U.S. "sparsely represented" (as few as 3 validation samples from one lake), limiting confidence in generalization to western optical water types; (7) performance degrades sharply at the oligotrophic end, attributed to the spectral configuration of both indices relative to where the chlorophyll reflectance peak sits at low concentrations; (8) sub-pixel heterogeneity is possible within the 20 m footprint; (9) S2 lacks thermal bands, limiting cloud-masking efficacy, and lacks a ~685 nm band that would allow harmonization with MERIS/OLCI-based indices; (10) broader operational challenges remain, including "limited availability of in situ data, issues with atmospheric correction, and operational capacity." The authors also flag their own calibration coefficient uncertainty (β1 95% CI spanning roughly 2802 to 42354, an order-of-magnitude-wide interval) as an indicator of substantial parameter uncertainty.

## Tensions with other findings
This paper's own error magnitude (MAEmult ~2, MAPE ~101% for the best configuration) is comparable to — not clearly better than — the in-situ measurement error it cites from prior literature (39-68%), which complicates any framing (in this paper or others) that satellite chlorophyll retrieval is unambiguously more precise or reliable than ground sampling; the authors present this as a reason for optimism, but it can equally be read as evidence the satellite signal is not yet more accurate than what it is meant to supplement. Second, the Discussion's own comparison table shows very different fit quality (r² from 0.25 to 0.80) for structurally similar MCI/NDCI-type algorithms across different prior studies (Ansper & Alikas; Toming et al.; Seegers et al.; Pahlevan et al.), suggesting reported skill for these indices is highly dependent on the specific lake set, sensor, and region rather than an intrinsic, transferable property of the algorithm — relevant caution for any HAB literature that treats a single reported r²/RMSE as broadly generalizable. Third, the explicit finding that MSPM (mineral sediment) can generate false-positive "bloom" signals in MCI is a direct caution against over-trusting single-index, spectral-proxy-based HAB/bloom alerts (including cyanobacteria-index-style products) in turbid, sediment-influenced systems — a point other remote-sensing HAB sources in this review should be checked against.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Possible hallucinated/misattributed numbers:**
  - 28 states in the full/calibration dataset
  - spanning 2016–2020
- **Dropped caveats:**
  - Detection limit values (1.9 µg/L vs. 12.0 µg/L) are specific to MCI; NDCI median non-detects were 3.5 µg/L vs. 8.1 µg/L for positive detections — this distinction dropped when claiming 'both algorithms' show the same pattern
- **Reviewer notes:** Two hallucinated figures appear in the claims but are absent from the source text: '28 states' (Claim 1, 11) and '2016–2020' (Claim 1). Neither appears anywhere in the provided source material. One claim (Claim 6) conflates MCI and NDCI detection limits, dropping the caveat that the cited median values (1.9, 12.0 µg/L) apply only to MCI; NDCI values differ materially. All other numerical claims align precisely with source data (Table 4 validation results, case study dates, percentages, filter thresholds, etc.). The methodological and substantive framing is well-supported and accurate."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC11235139/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Two WebFetch calls were made with different extraction prompts, per instructions, and their outputs were reconciled/unioned (e.g., the NDCI/Rrs row of Table 4 and the abstract's verbatim text appeared only in the second fetch; the negative-value counts, trophic-state error breakdown, and NLA threshold definitions appeared only in the first). No blocking or paraphrase-only failure occurred; both fetches returned substantial, largely consistent numeric detail, indicating the PMC page (open-access MDPI article mirrored on PubMed Central) was fully accessible. One residual ambiguity I could not resolve from the fetched text alone: fetch 1 explicitly labeled the r²=0.50 (MCI, ρt) and r²=0.46 (NDCI, ρt) figures as 'calibration r²', while fetch 2's table listed the identical values inside a table it labeled 'Validation Results (Table 4)' alongside MAEmult/biasmult/MAPE/n. I have presented these numbers as reported by Table 4 without asserting which fit (calibration vs. validation) they represent, since I have no way to inspect the original table structure directly. Similarly, one fetch describes 103 lakes/28 states as the full dataset while the other separately mentions '30 lakes across 12 states' for the validation subset; I have flagged this as reported rather than reconciled, since both figures could be consistent (a validation subset drawn from a subset of the 103 total lakes) but this is not stated explicitly by either fetch. Author list and journal/year/DOI metadata came from a WebSearch (not from the fetched article body itself, which did not surface a byline in either extraction), so this bibliographic metadata is corroborative rather than drawn from the primary source text used for the claims.
