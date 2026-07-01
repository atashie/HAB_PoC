---
key: ACAD-045
title: Evaluation of a satellite-based cyanobacteria bloom detection algorithm using field-measured microcystin data
authors_or_org: Mishra, S., Stumpf, R.P., Schaeffer, B., Werdell, P.J., Loftin, K.A., Meredith, A. — NOAA National Centers for Coastal Ocean Science; EPA Center for Environmental Measurement and Modeling; NASA Goddard Space Flight Center Ocean Ecology Laboratory; USGS Kansas Water Science Center; Consolidated Safety Services Inc.
year: 2021
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC9677180/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (Science of the Total Environment, 2021), full text hosted on PubMed Central (NIH public-access repository)
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Evaluation of a satellite-based cyanobacteria bloom detection algorithm using field-measured microcystin data

**What it is.** A field-validation study assessing the accuracy of CIcyano — a satellite spectral-index algorithm (a sub-component of the Cyanobacteria Index used in products such as EPA CyAN) derived from MERIS and OLCI ocean-color imagery — for detecting cyanobacterial harmful algal bloom (CyanoHAB) presence/absence, using field-measured microcystin concentrations (and, secondarily, cyanobacteria cell density) as ground truth across 30 lakes in 11 U.S. states over 11 bloom seasons (2005-2011, 2016-2019; n=281 satellite-field matchups).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The CIcyano satellite algorithm classifies CyanoHAB presence/absence with 84% overall accuracy against field-confirmed (microcystin-based) ground truth, with 87% precision and 90% recall, using same-day satellite-field matchups.
  - *evidence:* Headline result stated in the abstract and reproduced in unrounded form (84.34/86.77/89.62%) in the Table 2 'combined reference' results; computed from a confusion matrix over n=281 matchups across 30 lakes/11 states. (Abstract; Results, Table 2 ('CIcyano algorithm accuracy assessment metrics'))
  - *quote:* "With same-day matchups, the overall accuracy of CyanoHAB detection was found to be 84% with precision and recall of 87 and 90% for bloom detection."
- **[✓ verified]** The 84% accuracy estimate carries a 95% confidence interval of 77-87%, derived from a bootstrapping simulation that corrects for class imbalance in the dataset.
  - *evidence:* 10,000 bootstrap iterations, each resampling 98 observations (the minority-class size) from each class; yielded mean accuracy 82.1%, median 82%. (Abstract; Results (bootstrapping simulation))
  - *quote:* "Overall accuracy was expected to be between 77% and 87% (95% confidence) based on a bootstrapping simulation."
- **[✓ verified]** When only microcystin concentration is used as the ground-truth reference (instead of MC plus cyanobacteria cell density), measured accuracy is markedly lower: 72.24% overall accuracy, 68.78% precision, 87.25% recall, 55.30% specificity.
  - *evidence:* Reported as a distinct row/case in Table 2; the gap versus the combined-reference case (below) is attributed to CIcyano also flagging real cyanobacteria blooms that are not producing detectable microcystin. (Results, Table 2, MC-only case)
  - *quote:* "Overall Accuracy: 72.24% ... Recall: 87.25% ... Specificity: 55.30% ... Precision: 68.78%"
- **[✓ verified]** Adding cyanobacteria cell density (>10,000 cells/mL) as a second ground-truth criterion raises measured accuracy to 84.34% (precision 86.77%, recall 89.62%, specificity 74.49%, F1=0.88 for the 'Presence' class), with 237 of 281 samples correctly classified.
  - *evidence:* This is the 'combined reference' case in Table 2, used as the study's headline (rounded) result. (Results, Table 2, combined MC+cell-density case)
  - *quote:* "Overall Accuracy: 84.34% ... Recall: 89.62% ... Specificity: 74.49% ... Precision: 86.77%"
- **[✓ verified]** 34 of 281 field records (12%) were reclassified from microcystin 'non-detect' to bloom 'Presence' because measured cyanobacteria cell density exceeded 10,000 cells/mL, concentrated in four states.
  - *evidence:* Directly explains the difference between the MC-only and combined-reference accuracy figures. (Results/Methods (data reconciliation paragraph))
  - *quote:* "In total, 34 out of 281 records (or 12 %) across Florida (n=9), Vermont (n=15), Utah (n=6) and Washington (n=4) were converted from non-detect to bloom 'Presence' when cyanobacteria cell density was greater than 10,000 cell mL−1"
- **[✓ verified]** The study's operational ground-truth label defines field bloom 'Presence' as microcystin > 0.2 micrograms/L and 'Absence' as < 0.2 micrograms/L (the lab minimum detection level), subject to the cell-density exception above.
  - *evidence:* This threshold is what the satellite classification is validated against. (Methods (field data classification criteria))
  - *quote:* "'Presence': MC > 0.2 μg L⁻¹ ... 'Absence': MC < 0.2 μg L⁻¹"
- **[✓ verified]** Satellite-derived bloom 'Presence' is operationally defined as a lake-wide median CIcyano value (among valid pixels) greater than 0.0001, corresponding to roughly 10,000 cells/mL of Microcystis-equivalent biomass; 'Absence' is assigned when no CIcyano-positive pixel exists.
  - *evidence:* This is the threshold converting the continuous spectral index into the binary label compared against field microcystin data. (Methods (CIcyano bloom classification thresholds))
  - *quote:* "'Presence': Median value of detectable CI_cyano_ pixels > 0.0001 (representing 10,000 cells mL⁻¹ Microcystis-equivalent cells)"
- **[✓ verified]** The satellite sensors used cannot detect cyanotoxins directly; microcystin data serve only as a proxy confirming a bloom is/was toxin-producing, and the authors state there is no established quantitative relationship between cyanobacterial biomass and cyanotoxin concentration.
  - *evidence:* Central framing caveat: explains why no CIcyano threshold maps onto a specific toxin concentration. (Abstract; Discussion)
  - *quote:* "While the satellite sensors cannot detect toxins, MCs are used as the indicator of health risk, and as a confirmation of cyanoHAB presence.' ... 'lack of a functional relationship between the cyanobacterial biomass and cyanotoxins"
- **[✓ verified]** USEPA has set 8 micrograms/L microcystin as the threshold considered problematic in recreational waters (citing USEPA 2019), but the study did not derive a matching CIcyano numeric threshold for this specific health guideline.
  - *evidence:* Gives the regulatory benchmark the paper references while underscoring that validation here was only against binary bloom presence/absence, not against this numeric health threshold. (Discussion)
  - *quote:* "The USEPA has established an MC threshold of 8 μg L⁻¹ as problematic in recreational waters (USEPA, 2019)."
- **[⚠ partial]** A 300 m inward land-adjacency mask is applied to remove shoreline vegetation contamination from the satellite reflectance signal, and this masking is cited as one cause of missed (false-negative) detections for near-shore blooms.
  - *evidence:* Methodological detail on satellite preprocessing tied directly to a stated failure mode. (Methods (satellite data processing); Discussion (false-negative causes))
  - *quote:* "CyanoHAB was present in a specific part of the lake but satellite data didn't capture it because of either land proximity (we are masking 300 m inward) or due to obscurity from partial cloud cover"
  - *reviewer:* Source describes the 300 m buffer mask and lists 'land contamination' as a cause of misses, but does not explicitly state that the mask itself is cited as causing false negatives for near-shore blooms. The connection is logical but not directly stated.
- **[⚠ partial]** The false omission (missed-bloom) rate declines as the Valid Pixel Fraction (VPF, the share of a lake's area with usable, unmasked pixels) increases, indicating cloud cover and sun glint directly drive false negatives.
  - *evidence:* Sensitivity analysis varied VPF thresholds (10/25/50/80%) and tracked false-omission rate; the study's headline matchups required VPF > 0.5. (Results (VPF sensitivity analysis))
  - *reviewer:* Source mentions VPF > 50% as a threshold for inclusion and lists cloud/sun glint as causes of misses, but the detailed sensitivity analysis showing how false-omission rate varies with different VPF levels is not described in the provided source text excerpts.
- **[✓ verified]** Field microcystin monitoring data used for validation are likely biased toward bloom 'Presence' because state agencies tend to sample in response to observed bloom events rather than on a fixed, representative schedule.
  - *evidence:* A stated limitation affecting how representative the 'Absence' class (and thus the accuracy figures) are of a randomly chosen lake-day. (Discussion (limitations))
  - *quote:* "State agencies tend to collect water samples for laboratory analysis based on event response. As a result, the available field datasets tend to be biased towards CyanoHAB presence."
- **[✓ verified]** Restricting the toxin reference data to microcystins only can inflate the apparent false-positive rate, because CIcyano also detects cyanobacteria genera that may produce non-MC toxins (anatoxin-a, saxitoxin, cylindrospermopsin) or no toxin at all.
  - *evidence:* Mechanistic explanation for why MC-only accuracy (72.24%) is lower than combined-reference accuracy (84.34%). (Discussion (limitations))
  - *quote:* "Although MCs are the most common group of cyanotoxins, restricting the toxin data to MC only can increase the likelihood of artificial false positives."
- **[✓ verified]** Because toxins (unlike photosynthetic/pigment biomass) have no distinct optical signature, dissolved microcystin can persist in the water after a bloom has optically dissipated, which the authors identify as a source of false negatives (or of field 'positives' the satellite no longer registers).
  - *evidence:* Explains a specific mismatch between what the sensor detects (pigment/biomass) and what the field assay detects (dissolved + cell-bound toxin). (Discussion (limitations))
  - *quote:* "Toxins may be intra and extracellular and do not have a known detectable optical signal. Therefore, MC from a previous bloom event may remain in the water, in the dissolved form, after the bloom has disappeared."

## Data / numbers
- Overall accuracy (headline, same-day matchups) = 84% (rounded from 84.34%, combined MC+cell-density reference)
- Precision = 87% (rounded from 86.77%); Recall = 90% (rounded from 89.62%), combined reference
- 95% CI on overall accuracy = 77-87%, from bootstrapping (10,000 iterations, n=98 samples/iteration = minority-class size); bootstrap mean=82.1%, median=82%
- MC-only reference case (Table 2): overall accuracy=72.24%, precision=68.78%, recall(sensitivity)=87.25%, specificity=55.30%, F1(Presence)=0.77
- Combined MC+cell-density reference case (Table 2): overall accuracy=84.34%, precision=86.77%, recall=89.62%, specificity=74.49%, F1(Presence)=0.88; 237/281 samples correctly classified
- n = 281 field microcystin samples; 30 lakes; 11 U.S. states; 11 bloom seasons (2005-2011, 2016-2019)
- MC concentration range across samples: 0 to 750 micrograms/L (single-fetch figure, not cross-corroborated)
- Classification thresholds: field 'Presence' = MC > 0.2 micrograms/L; 'Absence' = MC < 0.2 micrograms/L (lab MDL); exception: non-detect reclassified to 'Presence' if cyanobacteria cell density > 10,000 cells/mL
- 34 of 281 records (12%) reclassified from non-detect to 'Presence' via the cell-density rule: Florida n=9, Vermont n=15, Utah n=6, Washington n=4
- Satellite CIcyano 'Presence' threshold: lake-wide median of detectable CIcyano pixels > 0.0001, ~10,000 cells/mL Microcystis-equivalent biomass
- Land-adjacency masking buffer: 300 m inward from shoreline
- Valid Pixel Fraction (VPF) inclusion threshold for headline results: VPF > 0.5 (50% of lake area); sensitivity tested at VPF = 10%, 25%, 50%, 80%
- USEPA recreational-water microcystin threshold cited: 8 micrograms/L (USEPA, 2019) — no matching CIcyano numeric threshold was derived for this value
- MC-only confusion matrix (self-consistent across 2 of 3 fetch passes and arithmetically verified against the percentages above): TP=130, FN=19 (Presence total=149); TN=73, FP=59 (Absence total=132); total N=281
- Combined-reference confusion matrix raw counts: reported inconsistently across extraction passes (TP=149-150, FN=18-19, TN=87-88, FP=25-26); only the aggregate '237/281 correct' and the Table 2 percentages were identical across all three fetch passes, so the individual cell counts should be treated as approximate pending direct check of Table 2/Figure 3 in the original PDF

## Methods
Satellite processing: Level-1B reflectance from MERIS and OLCI (via NASA OBPG/GSFC) processed with NASA's l2gen software into spectral water-leaving reflectances; cloud-masked, land-masked (300 m inward buffer), reprojected (Albers). CIcyano algorithm: a spectral "peak-height" index computed at 681 nm (referenced to 665/709 nm bands), with a secondary check at 665 nm (using 620/665/681 nm) to confirm the phycocyanin pigment characteristic of cyanobacteria; a lake-wide median of positive CIcyano pixels above 0.0001 is called 'Presence' (~10,000 cells/mL Microcystis-equivalent), else 'Absence'. Field data: microcystin measured mainly by ELISA (a couple of states, UT/VT, also used strip tests, excluded if not confirmed by ELISA) from 11 states' lake-monitoring programs; 'Presence' if MC>0.2 microg/L, 'Absence' if below, with a cyanobacteria-cell-density (>10,000 cells/mL) override for non-detects. Same-day satellite-field matchups (VPF>0.5) were compared via a confusion matrix and 6 standard classification metrics (overall accuracy, precision, recall/sensitivity, specificity, F1, false omission rate); class imbalance (~65% Presence/~35% Absence) was addressed with a 10,000-iteration bootstrap (98 samples/class per draw) to obtain a 95% CI on accuracy. The method works comparably well (~84% accuracy) for same-day, well-imaged (VPF>50%) matchups using the combined MC+cell-density reference, but underperforms (72% accuracy) when the ground truth is restricted to microcystin alone, and its false-omission rate rises as valid-pixel coverage falls (more cloud/sunglint obscuration).

## Stated limitations
The authors state: (1) field MC samples often lacked exact sampling coordinates, so some true blooms may have been missed by the satellite due to cloud, sunglint, land contamination, or sensor-saturation flags; (2) restricting the toxin reference to microcystin alone likely inflates apparent false positives, since other cyanotoxins (anatoxin-a, saxitoxin, cylindrospermopsin) exist and are not captured by MC assays; (3) CIcyano detects cyanobacteria biomass broadly (Anabaena/Dolichospermum, Aphanizomenon, Cylindrospermopsis, Microcystis, etc.), including non-toxin-producing strains, further inflating apparent false positives relative to an MC-only ground truth; (4) toxins have no distinctive optical signature — the sensor detects pigment/biomass, not the toxin itself — so dissolved residual MC from a decayed bloom can create false negatives (or field-positive/satellite-negative mismatches); (5) at low bloom concentrations, the phycocyanin absorption feature at 620 nm may be too weak to trigger detection; (6) in-situ MC measurements were used as supplied despite known variation across states in extraction protocol and analytical precision/accuracy; and (7) field datasets are likely biased toward bloom "Presence" because state agencies tend to sample in response to observed events rather than on a fixed representative schedule. The paper also notes no CIcyano threshold has been established that corresponds to the USEPA's 8 microg/L recreational-water microcystin guideline, because no functional (quantitative) relationship exists between cyanobacterial biomass and cyanotoxin concentration.

## Tensions with other findings
This source both supports and constrains any product claim that a satellite cyanobacteria spectral index (CIcyano, a component of EPA CyAN) can serve as a bloom/risk signal. It supports use as a synoptic presence/absence screening tool (84% accuracy, 90% recall against field-confirmed blooms). But it explicitly warns that the satellite signal detects cyanobacterial biomass/pigment, not toxin, and states there is no established quantitative link between biomass and cyanotoxin concentration — so satellite detection of "a bloom" cannot be equated with exceedance of a specific health threshold (e.g., the cited EPA 8 microg/L recreational guideline) without an intermediate, unvalidated inferential step. This is a direct instance of the "correlation is not causation" / proxy-vs-measurement caution relevant to calibrating any HAB tool's risk language. The paper also shows methodologically that reported accuracy is highly sensitive to how "ground truth" is defined: accuracy swings from 72.24% (MC-only) to 84.34% (MC + cell density) depending on whether non-toxigenic cyanobacteria blooms are counted as true positives — a caution for any downstream project (including this repository's HAB PoC) about pre-specifying validation labels rather than choosing whichever reference definition flatters the reported number.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** Verification result: 12 of 14 claims fully supported; 2 claims partially supported (no completely unsupported claims). No hallucinated numbers detected. All numeric values present in source text. Claims 10 and 11 are partially supported because they reference specific analyses or causal linkages that are logically implicit but not explicitly stated in the provided source text excerpts."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9677180/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Performed 3 WebFetch calls against the same URL (no redirect; PMC full-text page loaded each time, full_text_access=full). Fetch 1: comprehensive extraction prompt (findings/numbers/methods/limitations). Fetch 2: citation/abstract/results/limitations-focused prompt. Both converged tightly on the abstract's headline numbers (84% accuracy / 87% precision / 90% recall; 95% CI 77-87%), on Table-2-style percentage metrics for both the "MC-only" and "MC+cell-density" reference cases, and on the qualitative limitations. Because the raw confusion-matrix cell counts for the combined-reference case varied between fetch 1 (TP=150,TN=87,FP=25,FN=19) and a third, more targeted fetch aimed specifically at the confusion-matrix table/figure (TP=149,TN=88,FP=26,FN=18) — and neither set of raw counts divides out to *exactly* reproduce the Table 2 percentages (84.34/89.62/74.49/86.77%) — I treat those specific raw cell counts as approximate/extraction-uncertain (likely because they come from reading a figure, Figure 3, rather than the text-based Table 2) and flagged this in data_numbers rather than asserting a single precise value. In contrast, the MC-only confusion matrix (130/73/59/19) was identical across two passes and is internally consistent with 72.24/68.78/87.25/55.30%, so it is reported with confidence. One fetch pass also listed "Wisconsin" once among the 11 states (in a data-sources bullet) while every other mention (including named lakes like Vancouver Lake and Lake Sammamish, both in Washington State) said "Washington" — treated as a transcription slip and resolved to Washington. Bibliographic metadata (journal = Science of the Total Environment; year 2021) came from fetch 2 only, so I independently cross-checked it with one WebSearch, which corroborated: Science of the Total Environment, vol. 774, article 145462 (2021), same author list, also indexed on ScienceDirect and NOAA's institutional repository. No paywall or binary/garbage content was encountered; this is a fully open full-text PMC page.
