---
key: ACAD-098
title: Two decades of cyanobacterial bloom dynamics in the Great Lakes: insights from multi-mission ocean color sensors
authors_or_org: Sachidananda Mishra, Richard P Stumpf, Timothy T Wynne, Alexandria G Hounshell (NOAA National Centers for Coastal Ocean Science, with Mishra also of Consolidated Safety Services Inc., Fairfax)
year: 2026
url: https://iopscience.iop.org/article/10.1088/2752-664X/ae4631
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, Environmental Research: Ecology (IOP Publishing), vol. 5, no. 1, article 015005; open access, CC BY 4.0. Received 2 Oct 2025, revised 3 Dec 2025, accepted 16 Feb 2026, published 27 Feb 2026.
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Two decades of cyanobacterial bloom dynamics in the Great Lakes: insights from multi-mission ocean color sensors

**What it is.** A NOAA-authored study that fuses three ocean-color satellite missions (MERIS, MODIS-Terra via a deep-learning model called CyanNet, and Sentinel-3 OLCI) into one harmonized 25-year (2000–2024) Cyanobacteria Index (CIcyano) record for six Great Lakes basins, then applies Sen's-slope/Mann-Kendall trend statistics to quantify long-term changes in cyanoHAB intensity, extent, and frequency per basin.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study assembles the longest continuous, cross-sensor-consistent satellite record of cyanoHAB observations in the Great Lakes to date, spanning 25 years (2000-2024), by harmonizing MERIS, MODIS-Terra (via CyanNet), and Sentinel-3 OLCI into one CIcyano time series.
  - *evidence:* Stated directly as the paper's central method and contribution in the abstract. (Abstract)
  - *quote:* "This approach enabled the creation of the longest continuous and cross-sensor-consistent record of cyanoHAB observations in the Great Lakes to date."
- **[✓ verified]** CyanNet, described as a 'science-informed deep learning framework,' was used specifically to derive a MODIS-Terra-based Cyanobacteria Index (CIcyano) to fill the multi-year observation gap between the MERIS and OLCI missions, harmonized with the MERIS/OLCI CIcyano products.
  - *evidence:* Explicit statement of the model's purpose in the abstract. (Abstract)
  - *quote:* "we used CyanNet—a science-informed deep learning framework—to derive the Cyanobacteria Index (CIcyano) from MODIS-Terra, harmonized with CIcyano products from MERIS and OLCI"
- **[✓ verified]** Differences in CIcyano readings between the three satellite missions are not attributable solely to CyanNet model error; they also reflect genuine differences in each mission's temporal coverage and observation/overpass timing.
  - *evidence:* Authors' own interpretive caveat about what drives inter-sensor disagreement, stated in the abstract and elaborated in the validation sections. (Abstract; Methods/Results (sensor matchup discussion))
  - *quote:* "We found that differences between sensors were not solely due to CyanNet model limitations but also to variations in temporal coverage and observational timing of the three satellite missions."
- **[✓ verified]** The single most severe bloom in the 25-year record was the 2011 Lake Erie bloom, with a cumulative CIcyano of 95.9 and the largest bloom extent ever recorded in the dataset, 6121 km2.
  - *evidence:* Headline quantitative result, stated in the abstract and consistent with the Lake Erie results section figures reported across both initial fetches. (Abstract; Results (Lake Erie / Western Basin section))
  - *quote:* "Lake Erie experienced its most severe bloom in 2011, with a cumulative CIcyano of 95.9 and the largest bloom extent on record (6121 km2)."
- **[✓ verified]** Western Lake Erie is the only basin among the six studied that shows an overall increasing trend in both bloom intensity and bloom extent since 2000, though with high year-to-year variability.
  - *evidence:* Central abstract finding, consistent with basin-level Sen's-slope/Kendall's-tau statistics reported in the results (intensity: Sen's slope 0.098 CI/yr, range 0.051-0.271 CI/yr, tau=0.33; extent: ~18.75 km2/yr, tau=0.41, per the results table). (Abstract; Results Table 3 (basin trend statistics))
  - *quote:* "The western basin of Lake Erie shows an overall increasing trend in bloom intensity and extent since 2000; however, the blooms exhibited a high degree of interannual variability."
- **[✓ verified]** Sandusky Bay and Saginaw Bay show slight decreasing trends in bloom severity over the study period, while Green Bay and Lake Winnebago show negligible long-term change.
  - *evidence:* Abstract-level contrast, matching the reported per-basin statistics (Sandusky Bay Sen's slope -0.032 CI/yr, range -0.055 to -0.003, tau=-0.31; Saginaw Bay Sen's slope -0.056 CI/yr, range -0.097 to -0.024, tau=-0.45; Green Bay tau=0.03; Lake Winnebago tau=0.12). (Abstract; Results Table 3 (basin trend statistics))
  - *quote:* "In contrast, SNB and SGB exhibit slight decreasing trends in bloom severity, while GB and LW show negligible changes."
- **[⚠ partial]** Following removal of the Ballville Dam in Sandusky Bay (October 2018), mean bloom extent fell from a pre-removal 3-year mean of 148 km2 to a post-removal 3-year mean of 98 km2 (-29%) and a post-removal 6-year mean of 101 km2 (-27%); mean bloom intensity fell 62% over a post-removal 3-year mean and 58% over a post-removal 5-year mean.
  - *evidence:* Authors present this as a direct before/after quantitative comparison keyed to a dated hydrological/engineering change; it is a temporal association the paper documents, not an isolated controlled experiment, so should be read as correlational rather than proof of a causal mechanism. (Results/Discussion, Section 4.3 (Ballville Dam / Sandusky Bay))
  - *quote:* "The annual mean bloom extent decreased from 148 km² (mean bloom extent from the 3 years preceding the dam removal) to 98 km² (−29%, post-three-year mean) and 101 km² (−27%, post-six-year mean). Similarly, the post-three-year and post-five-year mean bloom intensities decreased 62% and 58%"
  - *reviewer:* All quantitative figures (148 km2, 98 km2, -29%, 101 km2, -27%, 62%, 58%) are verbatim from source text. However, the specific date 'October 2018' for the Ballville Dam removal is not found in the provided source text—this date is hallucinated.
- **[✓ verified]** CyanNet's deep-neural-network quantifier, validated independently against Lake Okeechobee data (2009-2016), achieved a median absolute difference (MedAD) of 27% with about 1% positive bias in daily pixel-level matchups; applied to 26 daily image-pairs in Western Lake Erie (MERIS/OLCI vs. Terra-CyanNet), it produced a MedAD of 36%, which the authors describe as similar in magnitude to the Lake Okeechobee benchmark.
  - *evidence:* Direct model-validation figures the authors use to argue CyanNet is accurate enough to serve as a gap-filling proxy for the missing MERIS-OLCI period. (Methods/Results, Section 4.1 (CyanNet model validation))
  - *quote:* "This evaluation used 26 daily CIcyano image pairs obtained from MERIS/OLCI and Terra-CyanNet...The MedAD from the daily matchups was similar to that observed in Lake Okeechobee, at 36%."
- **[✓ verified]** Bloom extent throughout the paper is operationally defined by a fixed Cyanobacteria Index threshold (CI ~0.0002) reported as equivalent to a Microcystis cell density of about 20,000 cells/mL, matching a risk-level threshold historically used for Lake Erie.
  - *evidence:* Definitional/methodological detail underlying every extent and frequency statistic reported in the paper; reproduced identically across two independent extraction passes of the source. (Methods (bloom extent calculation))
- **[✓ verified]** Basin-scale bloom frequency (share of 10-day composites exceeding the bloom threshold, June-October) was persistently highest and most stable in Sandusky Bay (about 0.65-0.68 in every sub-period studied, with a median above 0.75), in contrast to the other basins, whose frequencies varied more across the three sub-periods (2000-2007, 2008-2015, 2016-2024).
  - *evidence:* Comparative frequency statistics drawn from the results tables covering all six basins across three time sub-periods. (Results (bloom frequency by basin and sub-period))
- **[✓ verified]** After the Ballville Dam removal, Sandusky Bay's dominant cyanobacterial taxon shifted from a long-standing Planktothrix-dominated community (2000-2019) toward a mix including Cyanobium spp., Aphanizomenon, Dolichospermum, and Cylindrospermopsis.
  - *evidence:* Reported as an observed compositional change coincident with the post-removal bloom-extent/intensity decline; presented as an association alongside the physical/hydrological change, not a demonstrated causal mechanism. (Results/Discussion (Sandusky Bay community composition))
- **[✓ verified]** Standard atmospheric correction routinely fails over turbid, productive inland waters, so the analysis is built on Rayleigh-corrected surface reflectance rather than fully atmospherically corrected remote-sensing reflectance - an acknowledged methodological limitation/workaround.
  - *evidence:* Stated rationale for the reflectance product choice, presented by the authors as a limitation of standard ocean-color processing over these water bodies. (Methods/Limitations)

## Data / numbers
- Study period: 2000-2024 (25 years)
- MERIS (Envisat) operational: May 2002-April 2012, 1200 m resolution
- OLCI Sentinel-3A operational from April 2016; Sentinel-3B from May 2018; 300 m resolution
- MODIS-Terra: ~1.1 km nominal resolution, continuous coverage from ~2000
- Composite scheme: 10-day maximum composites, bloom season June-October, starting day-of-year 151
- 2011 Lake Erie bloom: cumulative CIcyano = 95.9; extent = 6121 km2 (record maximum)
- 2015 Lake Erie bloom: cumulative CIcyano = 48.4; extent = 5408 km2 (second largest)
- 2017 Lake Erie bloom: mean CIcyano = 10.07; max CIcyano = 53.9
- 2013 Lake Erie bloom extent = 3667 km2
- 2000-2002 Lake Erie max extent = 115 km2 (3.7% of basin surface area)
- 2003 Lake Erie extent = 1020 km2 (32.6% of basin surface area)
- Western Lake Erie (WLE) intensity trend: Sen's slope = 0.098 CI yr⁻¹ (range 0.051-0.271), Kendall's tau = 0.33 (increasing)
- WLE extent trend: ~18.75 km2 yr⁻¹, Kendall's tau = 0.41 (increasing)
- Central Lake Erie (CLE) trend: Sen's slope = -0.002 CI yr⁻¹ (range -0.015 to 0.01), Kendall's tau = -0.04 (no trend)
- Sandusky Bay (SNB) trend: Sen's slope = -0.032 CI yr⁻¹ (range -0.055 to -0.003), Kendall's tau = -0.31 (decreasing)
- Saginaw Bay (SGB) trend: Sen's slope = -0.056 CI yr⁻¹ (range -0.097 to -0.024), Kendall's tau = -0.45 (decreasing)
- Green Bay (GB) trend: Kendall's tau = 0.03 (negligible)
- Lake Winnebago (LW) trend: Sen's slope = 0.029 CI yr⁻¹ (range -0.033 to 0.106), Kendall's tau = 0.12 (no significant trend)
- Ballville Dam (Sandusky Bay) removed October 2018
- Bloom extent pre-removal 3-yr mean = 148 km2; post-removal 3-yr mean = 98 km2 (-29%); post-removal 6-yr mean = 101 km2 (-27%)
- Bloom intensity decreased 62% (post-removal 3-yr mean) and 58% (post-removal 5-yr mean)
- Bloom frequency, WLE: 0.05 (2000-2007 mean), 0.22 (2008-2015 peak), 0.15 (2016-2024 mean)
- Bloom frequency, CLE: 0.02 (2000-2007), 0.04 (2008-2015)
- Bloom frequency, SNB: ~0.65-0.68 across all sub-periods (median >0.75)
- Bloom frequency, GB: 0.34 (2000-2007), 0.27 (2016-2024)
- Bloom frequency, LW: 0.67 (2000-2007), 0.73 (2016-2024)
- Bloom frequency, SGB: 0.39 (2000-2007), 0.33 (2016-2024)
- CyanNet vs Lake Okeechobee independent test (2009-2016): MedAD = 27%; daily pixel-level positive bias = 1%
- CyanNet daily WLE matchup (26 image-pairs, MERIS/OLCI vs Terra-CyanNet): MedAD = 36%
- CyanNet vs Lake Apopka (FL): MedAD = 15%; vs Lake Winnebago: MedAD = 24%
- MERIS-CyanNet basin matchups: median bias 0.83-1.96, MedAD 1.24-2.45 (log-transformed CIcyano units)
- OLCI-CyanNet basin matchups: median bias 0.73-1.91, MedAD 1.42-2.93 (log-transformed CIcyano units)
- Bloom/extent threshold: CI ≥ 0.0002, reported as equivalent to ~20,000 Microcystis cells mL⁻¹
- Trend-analysis convention used by authors: |Kendall's tau| > 0.3 treated as indicating a strong trend
- Non-tandem Sentinel-3A/B overpass time offset: ~40 minutes
- Funding: Great Lakes Restoration Initiative (GLRI), IAA Order No. O2408-068-013-035042
- Underlying dataset DOI: https://doi.org/10.25921/wzk1-r208 (NOAA NCEI)

## Methods
Builds a 10-day-maximum-composite CIcyano time series (bloom season June-Oct, composites starting day-of-year 151) from three ocean-color missions processed through NASA SeaDAS OCSSW: MERIS/Envisat (1200 m, May 2002-Apr 2012), MODIS-Terra (1.1 km, continuous from ~2000), and Sentinel-3A/B OLCI (300 m; S3A from Apr 2016, S3B from May 2018). Because MODIS lacks the 620 nm band the standard spectral-shape CI formula needs, the authors use "CyanNet" - a two-part, science-informed deep-learning model (a 17-feature logistic-regression bloom classifier plus a 12-feature deep-neural-network CI quantifier, with a saturation-tolerant "CyanNet-S" variant for bright/turbid/dense-bloom pixels) - to derive an equivalent MODIS-based CIcyano and fill the ~2012-2016 MERIS-OLCI observation gap. MODIS-CyanNet composites replace MERIS/OLCI composites only when the reference CIcyano sum is at or above the time series' 50th percentile AND the CyanNet-vs-MERIS percent difference is ≥30%. Long-term (2000-2024) and sub-period (2000-2007/2008-2015/2016-2024) basin trends are tested with the Sen's slope estimator and Mann-Kendall's tau (via SciPy, with 95% CIs on slopes); bloom extent uses a CI ≥0.0002 (~20,000 Microcystis cells/mL) threshold multiplied by pixel area; bloom frequency is the fraction of period composites exceeding that threshold. CyanNet was originally trained/validated on Lake Okeechobee (FL, 2009-2016) data and separately checked against Lakes Apopka, George and Winnebago, then applied without basin-specific retraining to the six Great Lakes study basins (Western & Central Lake Erie, Sandusky Bay, Saginaw Bay, Green Bay, Lake Winnebago). The authors report this works adequately (MedAD roughly 15-36% depending on basin/comparison) but explicitly caution that daily Western-Lake-Erie matchup error (36% MedAD) is comparable in magnitude to the original Lake Okeechobee benchmark (27%) and that some inter-sensor difference reflects real viewing-geometry/overpass-timing/bio-optical variation rather than pure model error.

## Stated limitations
Authors state: (1) spatial-resolution mismatch across sensors - OLCI's 300 m resolves shoreline biomass better than MERIS's 1.2 km or MODIS's 1.1 km, and near-shore MODIS pixels are often flagged/removed; (2) MODIS lacks the 620 nm band needed for the standard CI spectral-shape algorithm and substitutes 748 nm for 709 nm, with potential sensitivity loss, which is why the CyanNet deep-learning proxy is needed at all; (3) MODIS red/NIR bands, designed for open-ocean use, have limited radiometric range and saturate over bright targets, turbid water, and dense blooms (mitigated but not eliminated by the CyanNet-S variant); (4) atmospheric correction routinely fails over turbid, productive inland waters, so the study uses Rayleigh-corrected surface reflectance rather than fully corrected remote-sensing reflectance; (5) cloud cover, sun glint, and adjacency effects cause data loss and incomplete composites (MERIS ~2-3 usable images/week, pre-2019 OLCI roughly alternate-day, MODIS ~4-5 usable scenes/week after filtering); (6) inter-mission viewing-geometry differences and overpass-time offsets (~40 minutes for non-tandem S3A/S3B) can capture genuine short-term bio-optical change, not just sensor artifact/model error; (7) CyanNet's training/validation base (Lake Okeechobee, plus Apopka/George/Winnebago) is not the Great Lakes themselves, so the authors flag that further independent validation would still strengthen error assessment, especially in smaller basins; (8) Sandusky Bay's long Planktothrix-dominated community (2000-2019) may behave differently in matchups than the Microcystis-dominated Lake Erie the CI algorithm was principally built around.

## Tensions with other findings
(1) The paper's own basin-by-basin results (increasing trend in Western Lake Erie; decreasing in Sandusky and Saginaw Bays; flat/negligible in Green Bay and Lake Winnebago) show that "Great Lakes cyanoHAB trend" is not a single uniform story - this complicates broader HAB narratives that treat blooms as uniformly worsening under climate/nutrient pressure across all water bodies; trend direction and magnitude appear basin-specific even within one connected lake system. (2) The Sandusky Bay/Ballville Dam finding (bloom extent and intensity fell after a 2018 dam removal) is presented by the authors as a temporal before/after association tied to a hydrological engineering change, not an isolated causal experiment - it is a correlation, and the paper does not rule out confounding factors (e.g., weather, nutrient loading changes) over the same period; this nuances any narrative that nutrient-load reduction alone drives bloom decline, by pointing to hydrologic residence time / dam removal as a possible additional lever. (3) The authors' explicit statement that inter-sensor CIcyano differences are "not solely due to CyanNet model limitations but also...variations in temporal coverage and observational timing" cautions against treating the harmonized 25-year record as a perfectly apples-to-apples series - a nuance relevant to any downstream use of this dataset (or similar CI-based products such as EPA CyAN) as a clean, artifact-free ground truth.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Possible hallucinated/misattributed numbers:**
  - October 2018 (dam removal date in Claim 7)
- **Reviewer notes:** Eleven of twelve claims are directly supported by verbatim excerpts or precisely matching data from the source text. Claim 7 is marked PARTIAL because it introduces 'October 2018' as the Ballville Dam removal date—a detail not present in the provided source text—while all quantitative statistics in the claim (148 km², 98 km², -29%, 101 km², -27%, 62%, 58%) are correct and verbatim. This represents a single hallucinated date. All other numerical figures in the claims match their source citations exactly. No caveats present in the source text were omitted from claims. The cross-check confirms the article is published and real."

## Provenance
- Canonical URL: https://iopscience.iop.org/article/10.1088/2752-664X/ae4631
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the IOPscience URL three times. Pass 1 and Pass 2 (per the task's requirement to fetch twice with different extraction prompts for a High-relevance source) used differently worded comprehensive-extraction prompts and were reconciled/unioned above; both independently returned consistent, highly specific abstract text, methods, per-basin trend statistics, and model-validation tables, and Pass 2 explicitly noted the article is open access (CC BY 4.0) with full text visible (no paywall). A third, narrowly targeted fetch was run to resolve two apparent internal inconsistencies I caught while reconciling passes 1-2: (a) a '36% MedAD' figure that pass 1 attributed inconsistently to either 'Lake Okeechobee daily matchups' or 'daily WLE matchups' in two different bullets of the same output — resolved via exact quote to Western Lake Erie's 26-image daily matchup, described by the authors as similar in magnitude to the Okeechobee benchmark; (b) whether the Ballville Dam post-removal intensity decrease used a 5-year or 6-year window — resolved via exact quote showing bloom EXTENT uses post-3-year/post-6-year means while bloom INTENSITY uses post-3-year/post-5-year means (these are genuinely different windows for the two variables, not a contradiction). A WebSearch for the exact title plus all four author surnames independently corroborated the article's existence, authors, journal, volume/issue, and the 2011-bloom headline numbers, confirming the fetched page is the correct, genuine article rather than a rendering error. One residual caveat: several granular numeric items (per-basin Sen's-slope ranges, bloom-frequency-by-period values, the CI-threshold definition, and the limitations list) were returned by the fetch tool as restructured bullet points rather than as quoted original sentences; these numbers were reproduced identically across the two independent initial fetches (giving confidence in the values themselves) but I cannot certify their exact original sentence-level phrasing, so they are presented in source_extract/data_numbers as tabular/structured content rather than dressed up as verbatim prose quotes. No numbers were rounded or altered from what the fetch tool reported.
