---
key: ACAD-025
title: Comparison of iCOR and Rayleigh atmospheric correction methods on Sentinel-3 OLCI images for a shallow eutrophic reservoir
authors_or_org: Katsoulis-Dimitriou S, Lefkaditis M, Barmpagiannakos S, Kormas KA, Kyparissis A
year: 2022
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC9639424/
access_date: 2026-07-01
tier: ACAD
source_type: peer-reviewed journal article
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Comparison of iCOR and Rayleigh atmospheric correction methods on Sentinel-3 OLCI images for a shallow eutrophic reservoir

> Note: provisional URL was resolved to a primary source. Original: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9639424/

**What it is.** A 2022 PeerJ methods-comparison study that uses 53 Sentinel-3 OLCI satellite images of Karla Reservoir (a shallow, highly eutrophic reservoir in Thessaly, Greece) to test whether a fast, partial Rayleigh-scattering-only atmospheric correction can substitute for the much slower, full iCOR atmospheric correction when deriving chlorophyll and cyanobacteria (phycocyanin) indices for HAB/water-quality monitoring. It is a preprocessing/methodology paper, not a study of HAB drivers, and includes no in-situ (field) validation of the retrieved pigment values.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Across all 16 common Sentinel-3 OLCI spectral bands, the iCOR (full) and Rayleigh (partial) atmospheric correction methods are very highly correlated with each other (r > 0.73), and their derived chlorophyll (CHL) and cyanobacteria (CI) indices are even more highly correlated (r > 0.95), even though the two methods' absolute values do not coincide.
  - *evidence:* Pearson correlation analysis (JASP v0.14) across N=2,597 pixels (53 images × 49 pixels/image) for the 16 shared bands (Table 1), and across N=2,597 (pixel level) and N=53 (per-date average level) for the CHL/CI indices (Figures 4-6); all correlations reported at P < 0.0001. (Abstract; Results Table 1; Figures 4-6)
  - *quote:* "The results showed, that although the absolute values between the two correction methods did not coincide, there was a very good correlation between the two methods for both bands' reflectance (r > 0.73) and the CHL and CI indices values (r > 0.95)."
- **[✓ verified]** iCOR (full atmospheric correction) takes roughly 25 times longer to process a Sentinel-3 image than the Rayleigh partial-correction method on the same hardware (about 2 hours vs about 5 minutes).
  - *evidence:* Authors timed the two processing workflows on identical hardware (Intel Core i5 7th-gen, 4 core/4 thread, 16 GB RAM) and reported the elapsed time per image for each method. (Methods/Discussion (processing time comparison))
  - *quote:* "the 25 times faster and/or less resource demanding image processing of the Rayleigh correction method compared to iCOR may be of critical importance, especially in cases of long timeseries for monitoring algal blooms"
- **[✓ verified]** Based on the strong correlation and large time savings, the authors propose that the simpler Rayleigh partial-correction method could be used as an alternative to full iCOR correction specifically for seasonal, long time-series water/HAB monitoring — while explicitly not recommending it as a general replacement for full atmospheric correction.
  - *evidence:* Stated as the paper's central recommendation in both Abstract and Conclusion, with an explicit hedge against over-generalizing it. (Abstract; Conclusion)
  - *quote:* "it is proposed that the Rayleigh partial correction method may be alternatively used for seasonal water monitoring, especially in cases of long time-series, enhancing time and resources use efficiency... Even though it is not recommended to replace the full atmospheric correction algorithms, the application of only a partial correction for Rayleigh scattering in a shallow eutrophic reservoir seems sufficiently functional"
- **[✓ verified]** The study performed no in-situ (field) validation of the satellite-derived chlorophyll or cyanobacteria/phycocyanin values; it only compared two atmospheric-correction methods against each other on the same imagery, and treats this as an indirect evaluation requiring future field validation.
  - *evidence:* Authors explicitly state this omission and justify it as out of scope, framing their approach as a preliminary, method-vs-method comparison rather than an accuracy assessment against ground truth. (Discussion)
  - *quote:* "The best practice for the validation of our results would be a direct comparison of the satellite derived CHL and CI indices with field measured chlorophyll and phycocyanin concentrations. However, this is a laborious and time-consuming task, which is beyond the aims of the current paper... our comparison of Rayleigh to iCOR may be considered as an indirect evaluation, which remains to be validated by combining in situ data."
- **[✓ verified]** Karla Reservoir (the study site) is a shallow (max depth 2 m), 34 km², highly eutrophic reservoir in Thessaly, Greece that was a natural lake drained in 1962 and reconstructed in 2010, and it now experiences frequent, prolonged, toxin-producing cyanobacterial blooms occasionally associated with fish and bird kills.
  - *evidence:* Site-description passage from the Methods/Study Area section, establishing why this reservoir was chosen (shallow + eutrophic + HAB-prone). (Methods - Study Area)
  - *quote:* "Karla was a natural lake, which was drained in 1962. However, a series of negative consequences resulting from its drainage has led to its reconstruction in 2010. In its current state, the reservoir occupies a surface of 34 km2 with a maximum water depth of 2 m... eutrophication and frequent and prolonged cyanobacterial blooms that produce toxins... the severity of such blooms has been associated to mass kills of fish and migrating birds."
- **[✓ verified]** This result echoes a prior, independent finding that simple Rayleigh-only atmospheric correction is likely sufficient for broad trophic-status assessment in turbid (case II) waters, avoiding more complex and error-prone full aerosol correction.
  - *evidence:* Authors cite Matthews, Bernard & Robertson (2012) as converging evidence for the same conclusion in a different context, used to support generalizing beyond their single study site. (Discussion)
  - *quote:* "Similar results have been reported by Matthews, Bernard & Robertson (2012)... stating that for broad trophic status assessment, simple Rayleigh atmospheric corrections are likely sufficient and avoid the more complicated and error-prone aerosol atmospheric corrections in turbid case II waters."
- **[✓ verified]** iCOR was chosen as the 'full correction' reference method because it has previously been benchmarked against several other established atmospheric correction algorithms (Acolite, C2RCC, l2gen, Polymer, Sen2Cor, ATCOR) and found to be a reliable method for inland water imagery.
  - *evidence:* Background justification for treating iCOR's output as the accuracy reference point against which Rayleigh-only correction is compared. (Introduction/Discussion)
  - *quote:* "systematically evaluated in comparison with several other full atmospheric correction methods (Acolite, C2RCC, l2gen, Polymer, Sen2Cor, ATCOR) for land images of Sentinel-2 and Sentinel-3 OLCI... Overall, it gives good results and is a reliable method for inland water images atmospheric correction."
- **[✓ verified]** The dataset comprised 53 cloud-free Level-1B Sentinel-3 OLCI images (300 m pixel size), each sampled at 49 pixels (7×7 grid) over the reservoir, yielding N = 2,597 pixels used for the band-level correlation statistics in Table 1.
  - *evidence:* Direct dataset/methods description with exact counts (53 × 49 = 2,597, internally consistent). (Methods; Table 1 caption)
  - *quote:* "Band intercomparison statistics (intercept, slope and correlation coefficient r) between iCOR and Rayleigh corrected data. For all bands P < 0.0001 and N = 2597."

## Data / numbers
- 53 cloud-free, full-resolution Level-1B Sentinel-3 OLCI images used (OL_1__EFR__ products), 300 m pixel size
- 49 pixels sampled per image (7×7 pixel grid) → N = 2,597 total pixels for band-level statistics
- 16 of 21 OLCI spectral bands common to both methods (bands 13, 14, 15, 19, 20 excluded from iCOR output)
- Band correlation coefficients (iCOR vs Rayleigh, Table 1): r = 0.734 at 400 nm up to r = 0.972 at 708.75 nm; all bands P < 0.0001, N = 2,597 (full 16-band table with slope and intercept per band also reported, e.g. 560 nm: r=0.933, slope=0.9057, intercept=0.0162; 1020 nm: r=0.952, slope=0.9122, intercept=0.0114)
- Chlorophyll (CHL) and cyanobacteria (CI) index correlations: r > 0.95, P < 0.0001, at pixel level (N = 2,597) and at pixel-average/per-date level (N = 53 dates)
- Rayleigh atmospheric correction processing time: ~5 minutes per Sentinel-3 image
- iCOR atmospheric correction processing time: ~2 hours per Sentinel-3 image
- iCOR is ~25 times slower / more resource-demanding than Rayleigh correction (stated ratio)
- Test hardware: Intel Core i5 (7th generation), 4 core/4 threads, 16 GB RAM
- Karla Reservoir location: 39°29′27″N, 22°49′19″E (Thessaly, Greece); surface area 34 km²; maximum water depth 2 m
- Karla was drained as a natural lake in 1962; reconstructed as a reservoir in 2010
- Example bloom-contrast dates: June 1, 2018 (low pigment concentration) vs July 21, 2019 (high pigment/bloom)
- Publication: PeerJ 2022 Nov 4; 10:e14311; DOI 10.7717/peerj.14311; PMID 36353601; PMCID PMC9639424
- No funding reported: 'The authors received no funding for this work.'

## Methods
Two atmospheric-correction pipelines were run on the same 53 Sentinel-3 OLCI Level-1B images (300 m, OL_1__EFR__ products) of Karla Reservoir and then cross-compared (no independent in-situ ground truth was used). (1) iCOR ('full' correction): a free, open-source SNAP plug-in applicable to Landsat-8 OLI, Sentinel-2 MSI and Sentinel-3 OLCI; four-step workflow = land/water pixel classification → Aerosol Optical Thickness (AOT) retrieval over land (Guanter et al. 2007 approach, extended into the SWIR over dark/black water pixels) → adjacency correction → atmospheric correction via pre-calculated MODTRAN 5 look-up tables (rural aerosol model), with the SIMilarity Environment Correction (SIMEC, based on the NIR similarity spectrum) applied over water; AOT, water vapor and ozone were estimated from data embedded in the Sentinel-3 product itself. iCOR outputs only 16 of the original 21 OLCI bands (5 bands dropped). (2) Rayleigh correction: a partial correction accounting only for Rayleigh (molecular) scattering, the dominant component of the top-of-atmosphere signal; originally built for MERIS, here applied to Sentinel-3 OLCI L1B bands 1-21 in SNAP v8.0. Both corrected reflectance sets were used to compute a Chlorophyll index (CHL = 1/r665 − 1/r708 × r753) and a Cyanobacteria/phycocyanin index (CI = −(r681 − r665 − (r708 − r665)×(λ681−λ665)/(λ708−λ665))), band-ratio formulas the paper describes as giving accurate estimations in eutrophic waters (citing Gitelson et al. 2008; Wynne et al. 2008). Comparison between the two correction methods' bands and indices used Pearson correlation (r), slope, intercept and significance (P) computed in JASP v0.14, at pixel level (N=2,597) and per-date/pixel-average level (N=53). The method works (per the authors) as a fast, resource-light, highly-correlated proxy for full correction in this specific shallow, eutrophic reservoir setting for relative/seasonal time-series monitoring; it explicitly does NOT work as a substitute when absolute (not just relative/correlative) reflectance or index values are required, since Rayleigh-corrected values are systematically higher than iCOR-corrected values across every band.

## Stated limitations
The authors explicitly flag: (1) No in-situ/field validation was performed — the study compares two atmospheric-correction pipelines against each other on the same imagery, not against measured chlorophyll/phycocyanin concentrations; direct field validation is called "laborious and time-consuming" and left for future work requiring "a very specific sampling strategy covering at least 1 calendar year, including episodic events, several sampling stations." (2) Because iCOR itself has not been validated with in-situ data in this study (only cited as reliable from other work), the Rayleigh-vs-iCOR comparison is described as only "an indirect evaluation, which remains to be validated by combining in situ data." (3) Absolute reflectance/index values differ systematically between the two methods (Rayleigh values run higher than iCOR across all bands), so the methods are described as usable interchangeably only for relative/time-series/correlative monitoring, not for absolute-value comparisons. (4) Single study site (Karla Reservoir only); authors state "additional research is needed to confirm our results in other shallow eutrophic lakes." (5) iCOR processing drops 5 of the original 21 OLCI bands (13, 14, 15, 19, 20), so it is not a fully like-for-like spectral comparison. (6) The authors explicitly caution that Rayleigh-only correction "is not recommended to replace the full atmospheric correction algorithms" in general — their proposal is scoped narrowly to efficiency-driven seasonal/time-series monitoring in shallow eutrophic reservoirs like Karla. (7) No external funding was received for the study.

## Tensions with other findings
This is a remote-sensing preprocessing/methodology paper, not a HAB driver, exposure, or ecological-forecasting study, so it does not directly contradict driver-based HAB findings. Its main tension with a broader HAB literature review is methodological: it demonstrates that satellite-derived chlorophyll/cyanobacteria index values are NOT an absolute, correction-method-independent quantity — Rayleigh-only correction yields systematically higher reflectance than the full iCOR correction across every band, even though the two are highly correlated (r > 0.73 bands, r > 0.95 indices). For any project (such as HAB_PoC) that plans to fuse a satellite cyanobacteria/chlorophyll signal (e.g., EPA CyAN, which itself depends on a specific processing/atmospheric-correction chain) with in-situ concentration data, this is a caveat: absolute satellite-derived values may not be directly comparable across products or processing pipelines, and a resulting model calibrated against one atmospheric-correction chain's outputs may not transfer to another's without re-calibration. It also underscores, by its own admission, that neither correction method's absolute output has been checked against ground-truth field measurements in this study — a limitation common to remote-sensing-only HAB papers that a fused remote-sensing + in-situ approach (as the HAB_PoC brief requires) is explicitly designed to address.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Source specifies the Rayleigh correction recommendation applies specifically to 'a shallow eutrophic reservoir' (Karla specifically), but Claim 3 generalizes the use case to 'water/HAB monitoring' without this geographic/water-type qualifier.
  - Source explicitly states 'Additional research is needed to confirm our results in other shallow eutrophic lakes', but the claims do not mention that validation in other water systems is required before generalizing this finding.
- **Reviewer notes:** All eight claims are textually supported by the source material. The primary issue is not false claims, but rather Claim 3 omits important context about the specificity of the study site (shallow eutrophic reservoir) and the authors' explicit call for validation in other systems. The source material uses both specific language ('in a shallow eutrophic reservoir') and broader language ('seasonal water monitoring') in the abstract, and the claim selectively adopts the broader framing without the limiting qualifiers. The evidence note for Claim 1 references 'JASP v0.14' which does not appear in the source text, but this is metadata rather than part of the claim itself."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9639424/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched PMC full text (open-access PeerJ article) twice with different extraction prompts, as required for a High-relevance source. First fetch targeted comprehensive numeric/methods extraction (got full Table 1 band statistics, index formulas, processing-time figures, hardware specs, limitations). Second fetch targeted verbatim abstract/discussion/conclusion text, site history, cited comparator algorithms, funding/data-availability, and figure/table captions. The two fetches were mutually consistent (matching r-values, processing times, N counts) and complementary (first gave the full quantitative table; second gave verbatim abstract/discussion prose and metadata), so they were combined via union with no contradictions to reconcile. Original URL (ncbi.nlm.nih.gov/pmc/articles/PMC9639424/) issued a 301 redirect to pmc.ncbi.nlm.nih.gov/articles/PMC9639424/, which was fetched successfully both times — no WebSearch fallback was needed. This is a methodology/preprocessing paper, not an ecological driver or prediction study, and it performs NO in-situ (field) validation of retrieved chlorophyll/cyanobacteria concentrations — it only cross-compares two atmospheric-correction pipelines against each other on the same imagery. That is treated here as a first-class stated limitation, not concealed.
