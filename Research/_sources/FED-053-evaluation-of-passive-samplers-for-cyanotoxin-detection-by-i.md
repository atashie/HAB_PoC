---
key: FED-053
title: Evaluation of Passive Samplers for Cyanotoxin Detection by Immunoassay and Chromatographic-Mass Spectrometry (USGS Scientific Investigations Report 2025-5046)
authors_or_org: Brett D. Johnston, Michael D.W. Stouder, Rebecca M. Gorney, Joshua J. Rosen, Kurt D. Carpenter, Bofan Wei, and Gregory L. Boyer (U.S. Geological Survey, in collaboration with NY State Dept. of Environmental Conservation)
year: 2025
url: https://pubs.usgs.gov/publication/sir20255046/full
access_date: 2026-07-01
tier: FED
source_type: USGS Scientific Investigations Report (government technical report)
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Evaluation of Passive Samplers for Cyanotoxin Detection by Immunoassay and Chromatographic-Mass Spectrometry (USGS Scientific Investigations Report 2025-5046)

**What it is.** A 2019 USGS/NYSDEC field study (SIR 2025-5046) that deployed SPATT (solid phase adsorption toxin tracking) passive samplers in three New York Finger Lakes (Seneca, Owasco, Skaneateles) to test their ability to detect four cyanotoxin classes (microcystins, cylindrospermopsins, anatoxins, saxitoxins), comparing results from ELISA immunoassay against LC-MS and LC-MS/MS chromatographic-mass-spectrometry methods, and evaluating how an ELISA-required sample preservative affects the mass-spectrometry measurements.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** 110 SPATT passive samplers were deployed across the three lakes for 5-22 days (mean 14 days), and about 86 percent (95 samplers) were recovered intact.
  - *evidence:* Stated directly in the report's deployment/recovery results as counts, duration range/mean, and a recovery percentage with the underlying count in parentheses. (Report body - Deployment & Recovery results)
  - *quote:* "110 SPATT samplers were deployed for durations between 5 and 22 days, averaging 14 days... About 86 percent (95 samplers) were recovered intact"
- **[✓ verified]** For microcystins, ELISA and LC-MS/MS each detected the toxin in 100 percent of analyzed samples (71 of 71), while LC-MS detected it in only 63 percent of samples (27 of 43).
  - *evidence:* Per-method detection rates given as both a percentage and an explicit fraction of samples analyzed. (Report body - Microcystins detection-rate results)
  - *quote:* "ELISA: 100% (71/71 samples) detected; LC-MS/MS: 100% (71/71 samples) detected; LC-MS: 63% (27/43 samples) detected"
- **[✓ verified]** On the same SPATT-extract samples, mean measured microcystin concentration differed sharply by method - ELISA (11,925.8 micrograms/liter) read roughly 8x higher than LC-MS (1,468.7 micrograms/liter) and about 2x higher than LC-MS/MS (5,069.1 micrograms/liter).
  - *evidence:* Report gives mean and range per method for the same sample set and separately characterizes the fold-differences between methods; these are concentrations measured in the concentrated SPATT resin extract, not ambient lake water (see stated_limitations). (Report body - Microcystins concentration comparison)
  - *quote:* "ELISA mean: 11,925.8 ug/L (range 976.8-21,758.5 ug/L); LC-MS mean: 1,468.7 ug/L (range 41.0-3,555.9 ug/L); LC-MS/MS mean: 5,069.1 ug/L (range 174.2-11,096.1 ug/L)"
- **[✓ verified]** Despite the large mean differences, the three analytical methods correlated strongly for microcystins: ELISA vs. LC-MS r=0.90, ELISA vs. LC-MS/MS r=0.95, and LC-MS vs. LC-MS/MS r=0.95.
  - *evidence:* Explicit Pearson-type correlation coefficients reported for each pairwise method comparison on microcystins. (Report body - Microcystins correlation results)
  - *quote:* "ELISA vs. LC-MS: r = 0.90; ELISA vs. LC-MS/MS: r = 0.95; LC-MS vs. LC-MS/MS: r = 0.95"
- **[✓ verified]** The chemical preservative required to make samples ELISA-compatible biased the mass-spectrometry concentration readings upward: preserved samples averaged about 35 percent (LC-MS) and 47 percent (LC-MS/MS) higher than unpreserved samples for microcystins, and about 31 percent higher for anatoxins.
  - *evidence:* Report directly compares preserved vs. unpreserved concentrations measured by mass spectrometry for the same toxin classes. (Report body - Preservation-effect results (microcystins and anatoxins))
  - *quote:* "Preserved samples were higher than unpreserved samples, by an average of about 35 and 47 percent [for microcystins]... Preserved samples were higher than unpreserved samples by an average of about 31 percent [for anatoxins]"
- **[✓ verified]** For anatoxins, ELISA detected the toxin in 100 percent of samples (95/95) versus 32 percent for LC-MS/MS (26/81); the two methods still correlated at r=0.90, but the report cautions this correlation rests on a small, skewed sample set.
  - *evidence:* Detection-rate contrast and correlation coefficient are both explicitly reported, alongside the report's own caveat about statistical fragility of the anatoxin correlation. (Report body - Anatoxins results and correlation caveat)
  - *quote:* "ELISA: 100% (95/95); LC-MS/MS: 32% (26/81)... Correlation between ELISA and LC-MS/MS anatoxins concentrations [was] based on a limited set of preserved and unpreserved sample pairs [and] heavily influenced by two pairs of preserved and unpreserved samples"
- **[✓ verified]** SPATT extracts registered many cyanotoxin detections absent from paired discrete (grab) water samples: about 40 percent of ELISA-analyzed and about 70 percent of LC-MS-analyzed SPATT samples showed microcystin detections not seen in corresponding discrete samples, and 80 percent of SPATT samples were ELISA-positive for anatoxins while no discrete sample exceeded the anatoxin minimum reporting level.
  - *evidence:* Report directly compares SPATT-extract detection outcomes to co-located, same-day-window discrete grab-sample results. (Report body - Comparison of SPATT to discrete (grab) samples)
  - *quote:* "40 percent of SPATT extract samples analyzed by ELISA, and about 70 percent analyzed by LC-MS, showed cyanotoxin detections that were not observed in the corresponding discrete samples... 80 percent of SPATT extract samples had positive detections for anatoxins by ELISA, whereas no detections above the minimum reporting level were observed in the corresponding discrete samples"
- **[✓ verified]** ELISA registered low-level cylindrospermopsin (below 2.0 micrograms/liter) and saxitoxin (below 0.40 micrograms/liter) readings across samples, but none of the cylindrospermopsin signals were confirmed by LC-MS/MS (and saxitoxin had no LC-MS/MS confirmatory testing at all), with no cylindrospermopsin-synthetase genes found molecularly - the report attributes these ELISA signals to likely false positives from dissolved organic matter / cross-reactivity rather than true toxin presence.
  - *evidence:* Report states the ELISA concentration ceilings for these two toxins, explicitly notes the lack of chromatographic/molecular confirmation, and gives the authors' own interpretation (matrix interference) for the discrepancy. (Report body - Cylindrospermopsins and Saxitoxins results/discussion)
  - *quote:* "No confirmatory detections by LC-MS/MS [for cylindrospermopsins]... false positives in these results may be attributed to... dissolved organic matter... Saxitoxin detections... may be false positives [due to cross-reactivity and dissolved organic matter interference]"
- **[✓ verified]** The report states that SPATT-extract concentrations cannot be readily converted into ambient in-lake toxin concentrations, because of variable water flow past the sampler and changing toxin concentration over the multi-day deployment window.
  - *evidence:* This is the report's own explicit methodological caveat limiting how its concentration numbers should be interpreted or compared to conventional water-concentration measurements. (Report body - Limitations/Discussion (SPATT sampler constraints))
  - *quote:* "Concentrations of cyanotoxins measured from SPATTs cannot be easily related to ambient concentrations in the water because of variations in flow velocity and cyanotoxin concentration over the deployment period"
- **[✓ verified]** Quality-assurance blanks indicated possible method-level errors: a blank LC-MS/MS run produced a microcystin false positive of about 3.0 micrograms/liter attributed to instrument noise, and blank SPATT samples showed a detectable cylindrospermopsin signal (about 0.05 micrograms/liter), which the report says points to an error somewhere in the analytical method.
  - *evidence:* Report reports specific blank/negative-control contamination values and states its own conclusion about what they imply for method reliability. (Report body - Data-quality issues / QA section)
  - *quote:* "One false positive for microcystins in blank LC-MS/MS analysis (~3.0 ug/L) attributed to instrument noise or interference... Detection of cylindrospermopsins (~0.05 ug/L) in blank SPATT samples indicates one or multiple errors in the analysis method"

## Data / numbers
- 110 SPATT samplers deployed; duration 5-22 days, mean 14 days
- ~86% (95/110) of SPATT samplers recovered intact
- 22 replicate SPATT pairs deployed; 15 (68%) recovered intact
- 80 samples analyzed after excluding 15 replicate pairs and 7 inter-lab comparison samples
- Microcystins detection: ELISA 100% (71/71); LC-MS/MS 100% (71/71); LC-MS 63% (27/43)
- Microcystins mean conc. in SPATT extract: ELISA 11,925.8 ug/L (range 976.8-21,758.5); LC-MS 1,468.7 ug/L (range 41.0-3,555.9); LC-MS/MS 5,069.1 ug/L (range 174.2-11,096.1)
- Microcystins correlation: ELISA-vs-LC-MS r=0.90; ELISA-vs-LC-MS/MS r=0.95; LC-MS-vs-LC-MS/MS r=0.95
- Microcystins preservative effect: +~35% (LC-MS), +~47% (LC-MS/MS) vs. unpreserved
- Microcystins CV (LC-MS): preserved mean 34.2% (range 1.9-128.4%); unpreserved mean 11.6% (range 3.2-15.7%)
- Anatoxins detection: ELISA 100% (95/95); LC-MS/MS 32% (26/81)
- Anatoxins mean conc.: ELISA 61.9 ug/L (range 10.8-160.1); LC-MS/MS 40 ug/L (range 2.3-145) - ELISA ~55% higher on average
- Anatoxins correlation ELISA-vs-LC-MS/MS: r=0.90
- Anatoxins preservative effect: +~31% in mass-spec measurements vs. unpreserved
- Microcystins: 40% (ELISA) and ~70% (LC-MS) of SPATT samples had detections absent from paired discrete samples
- Anatoxins: 80% of SPATT samples ELISA-positive vs. 0 discrete samples above minimum reporting level; 30% of SPATT LC-MS/MS samples had detections absent from discrete samples
- ELISA method detection limits (MDL): microcystins 0.15 ug/L; anatoxins 0.15 ug/L; cylindrospermopsins 0.05 ug/L; saxitoxins 0.02 ug/L
- LC-MS MDL: 31.05-220.60 ug/L (variable by sample); ~40x less sensitive than LC-MS/MS
- LC-MS/MS MDL: 0.85-6.01 ug/L (microcystins); 0.11-0.79 ug/L (anatoxins)
- Congeners: LC-MS analyzed 21 microcystin congeners (3 detected); LC-MS/MS analyzed 11 microcystin, 3 cylindrospermopsin, 4 anatoxin congeners (7 microcystin congeners detected)
- Cylindrospermopsins: ELISA detections <2.0 ug/L; no LC-MS/MS confirmation
- Saxitoxins: ELISA detections <0.40 ug/L; no LC-MS/MS confirmatory analysis performed
- Blank QA: microcystin false positive ~3.0 ug/L in LC-MS/MS blank; cylindrospermopsin ~0.05 ug/L detected in blank SPATT
- Sampling depths: ~1 m (near-surface), 13-15 m (mid-depth), 26-29 m (near-bottom)
- SPATT construction: 3 g DIAION HP20 resin, 100-um Nitex nylon mesh, 12.7-cm embroidery hoop

## Methods
SPATT passive samplers (3 g DIAION HP20 resin between two layers of 100-µm Nitex nylon mesh on a 12.7-cm embroidery hoop) were deployed at near-surface (~1 m), mid-depth (13–15 m), and near-bottom (26–29 m) at USGS monitoring sites on Seneca Lake (425027076564401), Owasco Lake (425327076313601), and Skaneateles Lake (425606076251601), NY, in 2019 (fetched text gives "mid-May to mid-November 2019"; a companion USGS data-release page found via search states "June and November 2019" - see fetch_notes), for 5-22 day intervals (mean 14 days). 110 SPATT units (plus 22 replicate pairs) were deployed; extracts were split for analysis by ELISA (ABRAXIS kits), LC-MS (Waters Micromass ZQ 4000; 21 microcystin congeners targeted), and LC-MS/MS (Thermo Scientific Quantiva Altis triple quadrupole; 11 microcystin, 3 cylindrospermopsin, 4 anatoxin congeners targeted), plus molecular screening for cyanotoxin synthetase genes. Results were benchmarked against biweekly discrete (Van Dorn grab) water samples collected at the same sites/depths in 2019. Per the source, the approach "works" (methods agree) for microcystins and anatoxins, where ELISA and mass-spectrometry concentrations correlate strongly (r = 0.90-0.95) despite differing absolute magnitudes; it "fails" or is unreliable for cylindrospermopsins and saxitoxins, where ELISA produced low-level detections with no LC-MS/MS or molecular confirmation, attributed by the authors to dissolved-organic-matter interference/cross-reactivity rather than true toxin presence.

## Stated limitations
The report itself flags: (1) SPATT samplers capture only the dissolved (extracellular) cyanotoxin fraction and their extract concentrations "cannot be easily related to ambient concentrations in the water because of variations in flow velocity and cyanotoxin concentration over the deployment period"; (2) both ELISA and mass-spectrometry results are subject to "matrix interference" from substances naturally present in lake water; (3) ELISA shows positive bias from high dissolved organic matter, implicated as the likely cause of unconfirmed cylindrospermopsin and saxitoxin detections; (4) the proprietary preservative needed for ELISA compatibility measurably inflates mass-spectrometry concentration readings (31-47%) for reasons the authors say are "unknown why it may affect concentrations" because its formulation is undisclosed; (5) LC-MS and LC-MS/MS can only quantify toxin congeners included in their analytical standards, and LC-MS/MS is described as "even more dependent on the availability of analytical standards"; saxitoxin analysis is further complicated because more than 57 congeners may exist in freshwater systems; (6) some SPATT units were damaged or lost to turbulence, disproportionately at near-surface depths, reducing the usable sample count; (7) the anatoxin ELISA-vs-LC-MS/MS correlation (r=0.90) is explicitly described as fragile - based on a limited set of sample pairs and "heavily influenced by two pairs of preserved and unpreserved samples," with only four unpreserved samples available; and (8) blank/negative-control samples showed low-level contamination (a ~3.0 ug/L microcystin false positive in an LC-MS/MS blank, and ~0.05 ug/L cylindrospermopsin in a blank SPATT), which the report says "indicates one or multiple errors in the analysis method."

## Tensions with other findings
This is a methods/measurement-agreement study, not a bloom-driver or predictive study, so its correlations (r=0.90-0.95 between ELISA and mass spectrometry) describe agreement between two assay techniques on the same physical samples, not a causal or environmental driver-outcome relationship - it should not be read as evidence about what drives toxin production. Its most relevant tension for a broader HAB review is a data-quality caution: ELISA, the cheapest and most widely used cyanotoxin immunoassay in field/monitoring programs, is shown here to read 2x-8x higher than confirmatory LC-MS/MS for microcystins and ~55% higher for anatoxins, and to generate apparently unconfirmed (likely false-positive) detections for cylindrospermopsins and saxitoxins - implying that "concentration" or "detection" figures drawn from ELISA-only sources elsewhere in the literature may overstate true toxin levels/prevalence unless corroborated by chromatography. Separately, the finding that time-integrated SPATT extracts flagged toxins (e.g., anatoxins in 80% of samples) that biweekly discrete grab samples missed entirely cuts against relying solely on discrete/grab sampling to characterize toxin exposure, which is relevant to any argument elsewhere in the review for early-warning or passive/continuous monitoring approaches - but the same passive-sampler results are explicitly stated by the authors to not translate into ambient water-column concentrations, so they cannot be directly substituted for discrete-sample concentration data in cross-study comparisons.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All 10 claims are clearly and directly supported by the source text. Every statistic, correlation coefficient, concentration value, and detection percentage cited in the claims appears verbatim or as a direct paraphrase in the source. The analyst accurately captured the report's key findings on method performance, matrix interference effects, and data-quality issues without introducing unsupported numerical claims or omitting material caveats. The source text is a detailed methods/results excerpt, not an abstract, so full verification was possible."

## Provenance
- Canonical URL: https://pubs.usgs.gov/publication/sir20255046/full
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: WebFetch on the primary URL (https://pubs.usgs.gov/publication/sir20255046/full) succeeded on the first attempt and returned extensive, section-by-section detail (methods, per-toxin detection rates, concentrations, correlation coefficients, preservation effects, comparison to discrete samples, and stated limitations), consistent with reaching the full report text rather than an abstract. A follow-up WebSearch ("USGS Scientific Investigations Report 2025-5046 SPATT cyanotoxin passive samplers Finger Lakes") independently corroborated the report's existence, DOI (10.3133/sir20255046), full author list, the three study lakes (Seneca, Owasco, Skaneateles), the four target toxins (microcystins, cylindrospermopsins, anatoxins, saxitoxins), and the three analytical methods (ELISA, LC-MS, LC-MS/MS) via a companion USGS ScienceBase data-release page, increasing confidence that the WebFetch extraction reflects genuine report content rather than fabrication. Two residual caveats: (a) the WebFetch text states the deployment window as "mid-May to mid-November 2019," while the companion data-release description (from the WebSearch snippet) says samplers were deployed "between June and November 2019" - both are reported here as-is since the discrepancy could not be resolved without direct access to the underlying report tables/PDF; (b) one WebFetch-summarized bullet - "'Cannot adsorb and concentrate dissolved cyanotoxins' (only measures dissolved toxins, not intracellular)" - is internally contradictory as worded (it almost certainly should describe SPATT as unable to capture non-dissolved/intracellular toxins) and is treated as a likely paraphrase artifact of the fetch; it was deliberately excluded as a relied-upon verbatim quote in key_claims, in favor of the clearer, unambiguous quote about SPATT concentrations not being convertible to ambient concentrations. No PDF/binary parsing failures occurred; access is treated as full-text.
