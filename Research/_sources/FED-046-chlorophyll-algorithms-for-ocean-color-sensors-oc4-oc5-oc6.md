---
key: FED-046
title: Chlorophyll algorithms for ocean color sensors - OC4, OC5 & OC6
authors_or_org: John E. O'Reilly (NOAA National Marine Fisheries Service) and P. Jeremy Werdell (NASA Goddard Space Flight Center)
year: 2019
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC6677157/
access_date: 2026-07-01
tier: FED
source_type: Peer-reviewed journal article (public-access author manuscript hosted on PMC; NASA/NOAA co-authored technical report), Remote Sensing of Environment, Vol. 229, pp. 32-47
categories: [remote-sensing]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Chlorophyll algorithms for ocean color sensors - OC4, OC5 & OC6

> Note: provisional URL was resolved to a primary source. Original: https://ntrs.nasa.gov/citations/20190025308

**What it is.** A methods paper by O'Reilly and Werdell (2019, Remote Sensing of Environment) that develops and documents 65 empirical "maximum band ratio" (MBR) chlorophyll-a algorithms - the OC2/OC3/OC4/OC5/OC6 family - for 25 past, current, and planned global open-ocean color satellite instruments, tuned on a shared in-situ chlorophyll/reflectance training database so that chlorophyll products stay internally consistent when merged across missions. It is a foundational open-ocean (Case-1-type) chlorophyll retrieval algorithm reference, not a HAB- or cyanobacteria-specific study.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The paper develops 65 empirical ocean-color (OC) maximum band ratio (MBR) chlorophyll algorithms for 25 satellite instruments, tuned on the largest available globally representative in-situ chlorophyll/reflectance database, to support merging and extending chlorophyll time series across overlapping and future missions (PACE, OLCI, HawkEye, EnMAP, SABIA-MAR).
  - *evidence:* Stated directly as the paper's central methodological contribution in the abstract. (Abstract)
  - *quote:* "we developed 65 empirical ocean color (OC) maximum band ratio (MBR) algorithms for 25 satellite instruments using the largest available and most globally representative database of coincident in situ chlorophyll a and remote sensing reflectances"
- **[✓ verified]** The new 'Version -7' algorithm set shows high mutual (cross-algorithm) consistency: median R2 = 0.859 and median regression slope = 0.985 across 903 pairwise comparisons of OC-modeled chlorophyll.
  - *evidence:* Headline internal-consistency statistic given in the abstract; the fetch also reported a percentile breakdown attributed to a results table (5th pct R2=0.853449; 50th pct R2=0.858966; 95th pct R2=0.859563; 50th pct slope=0.984516) - treat the extra decimal precision as a secondary, less-certain detail relative to the abstract figures. (Abstract; results table on pairwise algorithm consistency)
  - *quote:* "Excellent internal consistency was achieved across these OC 'Version -7' algorithms, as demonstrated by a median regression slope and coefficient of determination (R2) of 0.985 and 0.859, respectively, between 903 pairwise comparisons of OC-modeled chlorophyll."
- **[✓ verified]** In direct satellite-to-in-situ matchups, the new algorithms perform about as well as, and sometimes slightly better than, the current operational heritage algorithm (OCI): OC4_SEAWIFS was closer to in-situ chlorophyll than OCI in 51.4% of SeaWiFS matchup pairs, and OC3_MODIS was closer than OCI in 51.6% of MODIS-Aqua matchup pairs.
  - *evidence:* Reported as the fraction of paired satellite-to-in-situ matchups ('wins') where the new OC algorithm's chlorophyll estimate was closer to the in-situ measurement than the heritage OCI algorithm's estimate. (Results (heritage-algorithm comparison, SeaWiFS n=2,278 and MODIS-Aqua n=955 matchups))
  - *quote:* "OC4 more closely matched in situ CHL than OCI for 51.4% of these pairs ... OC3 more closely matched in situ CHL than OCI for 51.6% of these pairs"
- **[✓ verified]** OC6 is defined using the same numerator bands as OC5 (max band ratio among violet/blue bands over green) but replaces the single green denominator band with the mean of a green and a red band (e.g., Rrs555 and Rrs670 for SeaWiFS), approximating a band near 613 nm.
  - *evidence:* Algorithm-family definition, corroborated consistently across two independent extractions of this source (the NTRS-page-linked summary and the full-text fetch's own band-list description of OC4/OC5/OC6). (Methods / algorithm definitions)
  - *quote:* "OC6 algorithms use the same bands in the numerator of its MBR as OC5, but employ the mean of Rrs555 and Rrs670 in the denominator of the MBR, approximating radiances for a band at 613 nm."
- **[✓ verified]** The OC/MBR approach rests on an assumption that does not always hold: that optically relevant seawater constituents other than phytoplankton - non-algal particles (NAP) and colored dissolved organic material (CDOM) - co-vary with chlorophyll a.
  - *evidence:* Presented by the authors themselves as an inherent structural limitation of the empirical band-ratio approach, independent of any single sensor. (Discussion / limitations)
  - *quote:* "the limitation of an inherent assumption of the OC approach – namely, that all optically relevant seawater constituents, such as non-algal particles (NAP) and colored dissolved organic material (CDOM), co-vary with chlorophyll a"
- **[⚠ partial]** Any MBR algorithm's accuracy is contingent on accurate radiometric calibration and internal consistency across the 3 to 6 bands it uses; early SeaWiFS retrievals of the violet/blue bands were frequently unusable (negative) in phytoplankton-rich continental shelf waters.
  - *evidence:* Flags a hardware/atmospheric-correction-driven failure mode that disproportionately affects the violet-band (OC5/OC6) algorithms in optically complex, productive coastal waters. (Discussion / limitations)
  - *quote:* "A known potential shortcoming of any MBR algorithm is its requirement for accurate radiometric calibration and internal consistency across three (OC3) to six (OC6) bands ... nearly 25% and 7% of the retrievals of Rrs412 and Rrs443 respectively, were negative in phytoplankton-rich continental shelf water"
  - *reviewer:* Source confirms negative retrievals occurred in shelf waters (25% Rrs412, 7% Rrs443) but does not specify 'early' SeaWiFS or provide temporal framing. The claim adds a temporal qualifier not in the source text.
- **[✓ verified]** CDOM absorption is well known to strongly influence (confound) the Rrs412 retrieval used by OC5/OC6, yet algorithms including Rrs412 still achieved R2 comparable to the algorithm excluding it (OC5=0.836, OC6=0.851, vs OC4=0.851 for SeaWiFS).
  - *evidence:* The authors note the theoretical CDOM-confounding concern but report that, empirically, adding the 412 nm band did not degrade overall fit relative to the band's absence. (Discussion (violet-band / CDOM section))
  - *quote:* "It is also well known that CDOM absorption can strongly influence the Rrs412 retrieval ... the empirical OC algorithms that include Rrs412, such as OC5_SEAWIFS and OC6_SEAWIFS, have comparable R2 for MBR versus in situ CHL (0.836 and 0.851, respectively) with those not using Rrs412, such as OC4_SEAWIFS (0.851)"
- **[✓ verified]** The newer, more bio-optically diverse Version -7 training set yields a lower internal R2 for OC4_SEAWIFS (0.851) than earlier algorithm versions (Version-1: 0.932; Version-4: 0.892), which the authors attribute to the broader diversity of the new dataset rather than to a worse-performing algorithm.
  - *evidence:* An explicit, self-reported case where a newer model version shows a numerically lower goodness-of-fit than its predecessors, with the authors' own explanation for why. (Results / version-comparison discussion)
  - *quote:* "Lower than that for Version -1 (0.932), and Version -4 (0.892), most likely because Version -7 encompasses greater bio-optical diversity"
- **[⚠ partial]** At very low chlorophyll concentrations (CHL <= 0.1 mg m-3), the violet/blue single-band ratios (412:555, 443:555) correlate with in-situ chlorophyll better than the standard blue 490:555 ratio, which the authors present as part of the rationale for adding the 412 nm band in OC5/OC6.
  - *evidence:* Reported as band-specific R2 values restricted to the lowest chlorophyll subset, contrasted with the full-range result where the 490:555 ratio performs best overall. (Results, band-ratio comparison table (subset CHL <= 0.1 mg m-3))
  - *quote:* "Rrs490:Rrs555 band ratio model yielded the highest coefficient of determination (R2) with in situ CHL when considering the full range"
  - *reviewer:* Source provides the R² data supporting relative performance at low CHL (412:555 R²=0.480, 443:555 R²=0.496 vs. 490:555 R²=0.294). However, the claim asserts authors 'present as part of the rationale for adding the 412 nm band'—the source never explicitly connects this low-CHL performance to the decision to include 412 nm. The causal rationale is inferred, not stated.
- **[✓ verified]** The algorithms are explicitly scoped as intended for global open-ocean application, and the authors frame the broader effort as potentially extending the satellite chlorophyll climate data record to roughly fifty years once combined with heritage sensors (CZCS, 1978) and upcoming ones (PACE, 2022).
  - *evidence:* A scope/applicability caveat paired with the paper's stated long-term motivation. (Discussion / conclusion)
  - *quote:* "While algorithms presented here are primarily intended for application at a global ocean scale ... Conceptually, this could stretch the climate data record of CHL to upwards of fifty years"
- **[✓ verified]** Estimating remote-sensing reflectance at wavelengths a given sensor does not directly measure (needed to fit some of the 65 algorithms) is undesirable but was unavoidable for this exercise; the log-linear interpolation method used was accurate to only about 1-8%.
  - *evidence:* Self-reported accuracy bound on an interpolation step the algorithms depend on for sensors lacking certain native bands. (Methods (interpolated-Rrs validation))
  - *quote:* "While it remains undesirable to estimate Rrs at wavelengths not directly measured, doing so remains unavoidable within an activity such as this ... remaining nine slopes range between 0.9195 and 1.0053, indicating an approximate accuracy for the IRrs values of between 1 and 8 percent"

## Data / numbers
- 65 empirical OC (maximum band ratio) chlorophyll algorithms developed, for 25 satellite instruments
- Median regression slope = 0.985 and median R2 = 0.859 across 903 pairwise inter-algorithm comparisons (Version -7 algorithms)
- Training/tuning dataset: 2,720 paired in-situ chlorophyll-a and Rrs(lambda) observations (1,341 HPLC-derived + 1,379 fluorometric), CHL range 0.012-77.9 mg m-3
- SeaWiFS satellite-to-in-situ matchups: n = 2,278; OC4_SEAWIFS closer to in-situ CHL than heritage OCI in 51.4% of pairs
- MODIS-Aqua satellite-to-in-situ matchups: n = 955; OC3_MODIS closer to in-situ CHL than heritage OCI in 51.6% of pairs
- OC4_SEAWIFS R2 across algorithm versions: Version-1 = 0.932; Version-4 = 0.892; Version-7 = 0.851
- SeaWiFS R2 (Version-7): OC4 = 0.851; OC5 = 0.836; OC6 = 0.851
- Oligotrophic-water SeaWiFS matchups (CHL <= 0.2 mg m-3), n = 439: MAE range OCI 58%, OC4 60%, OC5 64%, OC6 67%; bias range 28% (OC5) to 45% (OCI)
- Productive-water SeaWiFS matchups (CHL > 0.2 mg m-3) bias: OCI 4.4%, OC4 2.3%, OC5 2.2%, OC6 1%
- Version-7 improved bias relative to prior version for >97% of SeaWiFS pairs and >99% of MODIS pairs
- Global 40-year mean-CHL trophic-status breakdown: oligotrophic (CHL < 0.1 mg m-3) = 24.25% of global ocean; mesotrophic (0.1 <= CHL < 1.67 mg m-3) = 67.04%; eutrophic (CHL >= 1.67 mg m-3) = 8.71%
- MBR dynamic range at CHL = 0.1 mg m-3: OC4_SEAWIFS ~ 5.0; OC5_SEAWIFS ~ 5.9; OC6_SEAWIFS ~ 10.6
- Sensitivity: a 10% change in MBR yields a CHL change of +/-16.7% (OC4), +/-14.6% (OC5), +/-13.5% (OC6)
- Interpolated-Rrs (IRrs) validation: regression slopes 0.9195-1.0053 (~1-8% accuracy), all R2 > 0.9731
- Clear-water anchor point added at CHL = 0.0001 mg m-3 (Morel & Maritorena 2001 clear-water reflectances); clear-water MBR: OC4_SEAWIFS = 21.35, OC5_SEAWIFS = 33.98
- Early SeaWiFS retrievals in phytoplankton-rich shelf waters: ~25% of Rrs412 and ~7% of Rrs443 values were negative
- Chlorophyll absorption at 412 nm = 71.3% of peak absorption at 443 nm (Bricaud et al. 1998 model cited); 31.3% of total 400-700 nm CHL absorption occurs below 443 nm
- R2 range across all 65 tuned algorithms: 0.791-0.861
- Band-ratio R2 at CHL <= 0.1 mg m-3: Rrs412:Rrs555 = 0.480; Rrs443:Rrs555 = 0.496; Rrs490:Rrs555 = 0.294; Rrs510:Rrs555 = 0.040

## Methods
Empirical, per-instrument, fourth-order polynomial regressions of log10(chlorophyll a) on log10(maximum band ratio, MBR) - the OC2/OC3/OC4/OC5/OC6 family, differing in how many and which violet-blue bands enter the MBR numerator and (for OC6) whether the denominator is a single green band or the mean of a green and a red/NIR band. Coefficients were fit with an IDL "AMOEBA" (Nelder-Mead-type) minimization targeting simultaneously a slope of 1.0, intercept of 0, maximum Type-2 (reduced major axis) R2, and minimum RMSE between log-transformed CHL quantiles; the paper reports the fit was numerically stable (100 replicate runs of OC4_SEAWIFS converged identically to the 5th decimal place in the same number of iterations). Training/tuning data came from a shared global in-situ chlorophyll-a/Rrs database (Valente et al. 2015 "satbands_6_nm.tab" file, spectra aggregated to within 6 nm of each sensor's band centers), supplemented with 7 clear-water anchor points. Reflectances at wavelengths a sensor does not natively measure were filled by a log-linear ("LOG") interpolation across the measured spectrum, itself validated against held-out measured bands. Independent validation used NASA Ocean Biology Processing Group Level-2 satellite-to-in-situ match-ups (2018 reprocessing; match-up exclusion criteria per Bailey & Werdell 2006) for SeaWiFS and MODIS-Aqua, with performance judged via bias, median absolute error, and pairwise "win" percentage against the current heritage OCI algorithm.

## Stated limitations
The source itself flags: (1) the OC/MBR approach's core assumption - that CDOM and non-algal particles co-vary with chlorophyll a - does not universally hold; (2) MBR algorithms need accurate radiometric calibration and consistency across 3-6 bands, and historically a substantial fraction of violet/blue-band retrievals (near 25% for Rrs412, 7% for Rrs443) were negative/unusable in phytoplankton-rich shelf waters; (3) CDOM absorption is well known to strongly confound the Rrs412 signal specifically; (4) estimating reflectance at non-native wavelengths (needed to port algorithms across sensors) is "undesirable" and only ~1-8% accurate; (5) the newer, more diverse Version-7 training data yields measurably lower internal R2 (0.851) than earlier algorithm versions (0.892, 0.932), an explicit acknowledgment that fit quality dropped even though the authors attribute it to broader data diversity rather than a worse model; (6) bias and error are higher and more variable for MODIS-Aqua than SeaWiFS in validation, partly attributed to smaller MODIS matchup sample size and lower temporal/spatial variability in that matchup set; (7) all algorithms (including the heritage OCI) show larger relative bias/error in oligotrophic, low-chlorophyll waters than in more productive waters; (8) the algorithms are "primarily intended for application at a global ocean scale," a scope caveat about regional/coastal-specific use; (9) band-ratio algorithms in general are sensitive to errors in atmospheric correction and to adjacent bright targets.

## Tensions with other findings
This source is exclusively an open-ocean (marine, Case-1-oriented) chlorophyll-retrieval algorithm paper: it never discusses cyanobacteria, harmful algal blooms, inland lakes/reservoirs, or the EPA CyAN cyanobacteria index, so any link to HAB detection is this reviewer's inference from the source's own stated scope and limitations, not a claim the source makes. That said, the source's self-described structural limitation - that the OC/MBR approach assumes CDOM and non-algal particles co-vary with chlorophyll a, and that the algorithms are "primarily intended for application at a global ocean scale" - is in tension with applying this algorithm family to the optically complex, terrestrially influenced inland and coastal waters where cyanoHABs commonly occur, since watershed-driven CDOM/sediment inputs there routinely decouple from phytoplankton biomass (precisely the failure mode the authors themselves describe, generalized from their coastal-shelf calibration/validation cases). The paper's own finding that violet-band (412 nm) retrievals were frequently negative in "phytoplankton-rich continental shelf water" is a concrete, source-stated instance of this algorithm family struggling in exactly the kind of productive, optically complex coastal waters that are closer to typical HAB settings than the open ocean the algorithms target.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Atmospheric correction and adjacent bright-target sensitivity as sources of band-ratio error
  - Severe performance degradation in oligotrophic waters: biases 28–45% (vs. 2–4% in productive waters)
  - Systematic MODIS-Aqua band biases: positive bias in numerator (412/443), negative in denominator (547/667) leading to elevated satellite MBRs
  - Global ocean trophic distribution: 24.25% oligotrophic, 67.04% mesotrophic, 8.71% eutrophic—indicating most water is NOT ultra-low-chlorophyll
- **Reviewer notes:** The source is a dense methods/results paper excerpt. Two claims are marked PARTIAL: Claim 6 adds a temporal qualifier ('early') and Claim 9 claims an explicit causal rationale ('presented as part of the rationale') that the source does not spell out—though both are factually grounded in data or discussion present in the source. No claims are wholly unsupported or contain hallucinated numbers. Significant caveats about performance breakdown by water regime and sensor-specific biases are present in the source but not woven into the claims; however, these are complementary details rather than contradictions."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC6677157/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetch chain: (1) WebFetch on the primary NTRS citation URL (https://ntrs.nasa.gov/citations/20190025308) succeeded but returned only landing-page metadata plus the abstract (partial/abstract-level, not the full manuscript) and pointed to a ScienceDirect DOI link. (2) WebFetch on the NTRS direct PDF-download API URL returned binary/unparseable PDF content - this fetch failed to extract text (the tool explicitly reported it could not parse the encoded PDF streams), so it was discarded per the task's binary/garbage-content rule. (3) WebFetch on the ScienceDirect published-article URL returned HTTP 403 Forbidden (paywalled/blocked). (4) WebSearch located a full-text mirror on PubMed Central (PMC6677157) - this is a public-access author manuscript because the work is co-authored by NOAA/NASA federal scientists. (5) WebFetch on that PMC URL succeeded and returned comprehensive full-text content (abstract, methods, multiple results tables, discussion, limitations, future-mission notes), which is used as url_used/resolved_url and as the basis for this dossier. Cross-check: the headline statistics (65 algorithms, 25 instruments, median R2=0.859, median slope=0.985, 903 pairwise comparisons) appeared consistently across both the NTRS-page fetch and the independent PMC full-text fetch, increasing confidence in those figures. Some very high-precision figures relayed by the fetch (e.g., six-decimal percentile values attributed to a results table, and the OC4_MODIS/OC4_MERIS per-sensor R2 list from the first NTRS-linked pass) came through an LLM-mediated extraction of a long HTML page rather than a table screenshot I could inspect directly; they are plausible for a table-heavy methods paper but were treated as secondary/lower-confidence relative to the abstract-level figures, which are quoted verbatim and corroborated twice. No claim in this dossier draws on anything beyond the fetched text - the source itself never mentions cyanobacteria, HABs, or freshwater lakes, and the HAB-relevance framing in 'tensions' is explicitly marked as this reviewer's inference from the source's own stated scope/limitations, not a source claim.
