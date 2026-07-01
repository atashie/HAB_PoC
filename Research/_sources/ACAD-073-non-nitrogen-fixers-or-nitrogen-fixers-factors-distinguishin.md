---
key: ACAD-073
title: Non-Nitrogen-Fixers or Nitrogen-Fixers? Factors Distinguishing the Dominance of Chroococcal and Diazotrophic Cyanobacterial Species
authors_or_org: Elżbieta Wilk-Woźniak, Ewa Szarek-Gwiazda, Edward Walusiak, Joanna Kosiba, Wojciech Krztoń (Institute of Nature Conservation, Polish Academy of Sciences, Kraków, Poland)
year: 2022
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC9738033/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, open access (International Journal of Environmental Research and Public Health, MDPI; vol. 19, issue 23, article 15980; DOI 10.3390/ijerph192315980)
categories: [basic-science]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Non-Nitrogen-Fixers or Nitrogen-Fixers? Factors Distinguishing the Dominance of Chroococcal and Diazotrophic Cyanobacterial Species

> Note: provisional URL was resolved to a primary source. Original: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9738033/

**What it is.** A 2022 field study of four small, shallow (max depth 4 m), eutrophic water bodies near Kraków, Poland, in which paired upper- and bottom-layer water chemistry (temperature, oxygen saturation, PO4^3-, NO3-, NH4+, SO4^2-, total dissolved iron) from 62 sampling events (May-October) was analyzed with decision-tree classification to identify which factors best distinguish dominance by non-nitrogen-fixing (chroococcal: Microcystis, Woronichinia) versus nitrogen-fixing (diazotrophic: Aphanizomenon, Dolichospermum) cyanobacteria. It empirically tests and extends a prior hypothesized driver model (Molot et al.) linking anoxia, nutrients, iron, and sulfate to cyanobacterial blooms.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Sulfate (SO4^2-) concentration was the single most important factor distinguishing whether non-nitrogen-fixing or nitrogen-fixing cyanobacteria dominated, ranking above water temperature, phosphate, and oxygen saturation in both the upper- and bottom-layer decision-tree models.
  - *evidence:* Stated as the headline result in the abstract and conclusions, and corroborated by decision-tree variable-importance scores where SO4^2- ranked first in both layer models (18.1 upper, 18.3 bottom). (Abstract; Conclusions; Results (decision-tree variable importance))
  - *quote:* "SO42− was the most important factor that explained whether non-nitrogen-fixing or nitrogen-fixing species would dominate."
- **[✓ verified]** In the upper water layer, sulfate above 69 mg/L was associated with dominance by non-nitrogen-fixing (chroococcal) taxa, while sulfate below that level was associated with nitrogen-fixing (diazotrophic) dominance.
  - *evidence:* First (root) split of the upper-layer decision tree, reported directly in Results. (Results, upper-layer decision tree)
  - *quote:* "When the SO42− concentration was higher than 69 mg/L, the non-nitrogen-fixing cyanobacteria dominated."
- **[✓ verified]** In the bottom layer, Microcystis spp. (non-nitrogen-fixing) dominance occurred under a combination of sulfate >73 mg/L, a PO4:NH4 ratio >0.051, and oxygen saturation >7.5%, a combination present in 12% of samples.
  - *evidence:* Directly reported terminal-node condition of the bottom-layer decision tree. (Results, bottom-layer decision tree)
  - *quote:* "For Microcystis spp. dominance, the most important factors were a SO42− concentration greater than 73 mg/L, a PO43−:NH4+ ratio greater than 0.051, and an oxygen saturation greater than 7.5%. These conditions occurred in 12% of the samples."
- **[✓ verified]** Across the 62 sampling events, nitrogen-fixing taxa were the dominant cyanobacterium far more often than non-nitrogen-fixing taxa (57% vs. 17% of samples), with no clearly dominant species in the remaining samples (26%).
  - *evidence:* Reported as per-taxon and aggregate dominance-frequency figures in the Results (A. flos-aquae 49% + D. planctonicum 8% = 57%; M. ichthyoblabe 10% + W. naegeliana 7% = 17%); figures were consistent across both independent extraction passes. (Results (dominance-frequency summary))
- **[✓ verified]** The authors' proposed mechanism is that sulfate inhibits molybdate uptake, and because molybdenum is a required cofactor for nitrogenase (N2-fixation) enzymes, elevated sulfate suppresses nitrogen fixation and thereby disadvantages diazotrophic cyanobacteria relative to non-fixers.
  - *evidence:* Presented in the Discussion as the explanatory hypothesis for the sulfate association; the authors did not themselves measure molybdate uptake or nitrogenase activity to confirm it directly. (Discussion)
  - *quote:* "Sulphate is an important inhibitor of molybdate uptake in natural waters, and molybdenum (Mo) is one of the essential cofactors for the vast majority of known N2 fixation systems and many nitrate reductases."
- **[✓ verified]** Total dissolved iron (TDFe), despite being one of the five candidate environmental drivers measured, was found not to meaningfully distinguish which cyanobacteria group dominated.
  - *evidence:* Explicit stated null result for one of the study's five hypothesized drivers, despite TDFe being elevated and Fe2+ release being plausible in the poorly oxygenated bottom layers of two sites. (Discussion)
  - *quote:* "in our studies, total dissolved Fe concentration showed little significance and was not responsible for differentiating the dominance of cyanobacterial species."
  - *reviewer:* Source lists seven environmental drivers measured (temperature, O2, PO4, NO3, NH4, TDFe, SO4), not five
- **[✓ verified]** The authors' own sulfate-molybdenum limitation mechanism is not universally supported in the literature: they cite a contradicting study reporting no molybdenum limitation of nitrogen-fixing cyanobacteria in a different set of eutrophic saline lakes, and flag their own explanation as potentially questionable as a result.
  - *evidence:* Self-identified tension/caveat regarding the paper's central causal mechanism, attributed to Evans & Prepas in the reference list. (Discussion)
  - *quote:* "there are some studies showing that nitrogen-fixing cyanobacteria were not limited by Mo in a group of eutrophic saline lakes with high sulphate/Mo ratios, so the above explanation may be questionable."
- **[✓ verified]** The authors explicitly characterize their causal explanation as partly speculative because they did not directly measure nitrogen-fixation rates or nutrient uptake in this study.
  - *evidence:* Self-stated methodological limitation distinguishing the correlational decision-tree result from a mechanistically confirmed causal pathway. (Discussion/Conclusion)
  - *quote:* "Because we did not measure nutrient uptake or nitrogen fixation rates, the discussion of our results remains partially hypothetical, but the idea is worth developing in the future."
- **[✓ verified]** The statistical approach used classification (decision) trees (R package 'rpart'), fit separately on upper-layer and bottom-layer predictor sets, to classify which cyanobacterium taxon dominated at each of the 62 sampling events; tree depth was manually restricted to reduce overfitting risk.
  - *evidence:* Directly describes the modeling method and the authors' explicit overfitting-control step. (Methods (statistical analysis))
  - *quote:* "we used decision trees (package 'rpart')... The depth of each decision tree was manually determined to avoid overfitting the prediction."
- **[✓ verified]** The upper-layer decision-tree model correctly explained the dominant taxon in 74% of samples, and the bottom-layer model in 76% of samples — i.e., roughly a quarter of samples were not correctly classified by either layer's model.
  - *evidence:* Reported model-fit figures for the two decision trees; no separate held-out test-set accuracy or cross-validation score was reported in the extracted text. (Results)
- **[✓ verified]** The dataset comprised 62 total paired (upper 1 m + near-bottom ~10 cm above sediment) water samples collected May-October from four shallow, eutrophic water bodies near Kraków, Poland, sampled monthly outside bloom periods and weekly during blooms.
  - *evidence:* Describes the sampling design underlying all reported statistics; no specific calendar year of collection was given in the retrieved text. (Methods (study sites and sampling))
  - *quote:* "A total of 62 samples were collected for physical, chemical, and biological analyses."
- **[✓ verified]** Prior laboratory culture experiments (cited from earlier literature, not this study's own field data) have shown that Aphanizomenon flos-aquae growth does not occur at or below 11°C, with a preference for higher temperatures (~20-25°C).
  - *evidence:* This is the authors citing external culture-based literature (attributed to Wu et al. in the reference list) as background support, not a finding derived from this paper's own field data — should not be conflated with the field study's own temperature-threshold results. (Discussion)
  - *quote:* "Experiments with cultures have shown that water temperature is crucial for the growth of A. flos-aquae and that growth does not occur at a temperature of 11 °C or below."
- **[✓ verified]** Within each layer's decision tree, A. flos-aquae dominance was recovered under two different combinations of environmental variables rather than one, which the authors interpret (speculatively) as possible evidence of different physiological strains of the species.
  - *evidence:* Authors' own hypothesis to explain why one species, uniquely among the four studied, needed multiple different rule-sets to be classified as dominant. (Discussion)
  - *quote:* "The dominance of Aphanizomenon flos-aquae was explained by different sets of variables, indicating the presence of different strains of this species."

## Data / numbers
- Study design: 62 total paired upper/bottom water samples, May-October, 4 shallow eutrophic water bodies (max depth 4 m) near Kraków, Poland
- Site surface areas: Piekary 1.6 ha; Tyniec 5.75 ha; Podkamycze 1 16.82 ha; Podkamycze 2 17.28 ha
- Trophic State Index (chlorophyll-a based): Piekary 64.7; Tyniec 66.1; Podkamycze 1 57.8; Podkamycze 2 65.1 (all classed 'eutrophy')
- Water temperature range: upper layer 7.2-25.6 °C; bottom layer 7.0-24.1 °C
- Oxygen saturation range: upper layer 11.8-236.6%; bottom layer 2.2-226.2%
- PO4^3- range: upper layer 0-0.538 mg/L; bottom layer 0-0.573 mg/L
- SO4^2- range: upper layer 21.2-100.1 mg/L; bottom layer 17.7-91.8 mg/L
- NH4+ range: upper layer 0.02-0.78 mg/L; bottom layer 0.01-1.96 mg/L
- NO3- range: upper layer 0.18-12.11 mg/L; bottom layer 0.14-13.65 mg/L
- Total dissolved Fe (TDFe) range: upper layer 0.8-160.0 µg/L; bottom layer 1.6-204.4 µg/L
- Cyanobacterial biomass range: overall 0-12.830 mg/L (Piekary 0-0.354; Tyniec 0-12.830; Podkamycze 1 0.11-5.61; Podkamycze 2 0.06-9.23 mg/L)
- Dominance frequency (of 62 samples): non-nitrogen-fixing (chroococcal) 17%; nitrogen-fixing (diazotrophic) 57%; no dominant species 26%
- Per-taxon dominance: Aphanizomenon flos-aquae 49%; Dolichospermum planctonicum 8%; Microcystis ichthyoblabe 10%; Woronichinia naegeliana 7%
- Upper-layer split: SO4^2- > 69 mg/L -> non-nitrogen-fixing dominance
- Upper-layer split: PO4^3- > 0.029 mg/L & temperature > 16 °C -> M. ichthyoblabe dominant (10% of samples)
- Upper-layer split: PO4^3- > 0.029 mg/L & temperature < 16 °C -> W. naegeliana dominant (7% of samples)
- Upper-layer split: SO4^2- 39-69 mg/L & temperature > 16 °C -> A. flos-aquae dominant (44% of samples)
- Upper-layer split: SO4^2- < 39 mg/L & temperature > 16 °C -> D. planctonicum dominant (8% of samples)
- Upper-layer split: SO4^2- < 41 mg/L & temperature < 16 °C & NH4+ < 0.11 mg/L -> A. flos-aquae dominant (5% of samples)
- Bottom-layer split: SO4^2- > 73 mg/L, PO4:NH4 ratio > 0.051, O2 saturation > 7.5% -> Microcystis spp. dominant (12% of samples)
- Bottom-layer split: SO4^2- > 73 mg/L & O2 saturation < 7.5% -> W. naegeliana dominant
- Bottom-layer split: SO4^2- 53-73 mg/L -> A. flos-aquae dominant (47% of samples)
- Bottom-layer split: SO4^2- < 53 mg/L & NH4+ > 0.37 mg/L -> D. planctonicum dominant (9% of samples)
- Bottom-layer split: SO4^2- < 53 mg/L, NH4+ 0.18-0.37 mg/L, temperature > 14 °C -> A. flos-aquae dominant (3% of samples)
- Decision-tree model fit: upper-layer model explained 74% of samples; bottom-layer model explained 76% of samples (no separate cross-validated accuracy reported)
- GLM layer comparison: water temperature difference between layers p = 0.0636; oxygen saturation difference p = 0.0185 (significance threshold p < 0.05)
- Variable importance, unitless rpart score (upper layer): SO4^2- 18.1 > temperature 10.6 > PO4^3- 8.5 > PO4:NH4 ratio 6.3 > TDFe 5.2 > NH4+ 4.8
- Variable importance, unitless rpart score (bottom layer): SO4^2- 18.3 > NH4+ 9.6 > PO4:NH4 ratio 9.1 > O2 saturation 8.6 > temperature 3.9 > PO4^3- 3.8 (one extraction pass also listed 'total dissolved Fe' as a 7th bottom-layer factor name without a distinct score -- unresolved/flagged, not invented)
- Cited prior literature: A. flos-aquae culture growth does not occur at <=11 °C, preferring ~20-25 °C (Wu et al., as cited in this paper)
- Cited prior literature: SO4^2- concentrations typically 4-6 times higher than molybdate concentrations can inhibit molybdate uptake (Cole et al., as cited in this paper)

## Methods
Field observational study (not remote sensing). Four shallow (max depth 4 m), eutrophic water bodies near Kraków, Poland (surface areas 1.6-17.28 ha; TSI 57.8-66.1, all eutrophic) were sampled May-October (monthly outside bloom periods, weekly during blooms) at an upper (1 m) and near-bottom (~10 cm above sediment) depth, yielding 62 total samples. Water temperature, oxygen saturation, and chlorophyll-a were measured in situ with a YSI 6600 V2 multiparameter probe; SO4^2-, NO3-, PO4^3- and NH4+ were measured by ion chromatography (Dionex IC25/ICS-1000); total dissolved iron (TDFe, used as a proxy for bioavailable Fe2+ because Fe2+ "is very difficult to measure in the field") was measured by atomic absorption spectrophotometry (Varian Spectr AA-20). Cyanobacteria were sampled with a 5 L Ruttner sampler, concentrated with a 10 µm-mesh plankton net, fixed in Lugol's solution for counting and left unfixed for live taxonomic identification under light microscopy (Nikon, 40-1000x) using published keys; biomass was computed from cell counts and geometric biovolume formulas. Trophic State Index was computed from chlorophyll-a via TSI = 10x[6-(2.04-0.68*ln(CHL-a))/ln2]. Differences in temperature and oxygen saturation between the two depth layers were tested with generalized linear models (GLM, categorical predictor, alpha=0.05). The core analysis used classification/decision trees (R package 'rpart', in R/RStudio) fit separately on upper-layer and on bottom-layer predictor sets to classify which cyanobacterium taxon was dominant per sample; tree depth was manually limited by the authors to reduce overfitting risk (no separate held-out test set or formal cross-validated accuracy was reported in the retrieved text). The approach is reported to "work" in that SO4^2- emerged as the top-ranked splitting variable in both layer models and the trees explained 74% (upper) / 76% (bottom) of samples; it is explicitly reported as not working for total dissolved Fe (little explanatory significance) and only partially resolves Aphanizomenon flos-aquae, which required two different variable combinations per layer rather than one clean rule.

## Stated limitations
The authors state several explicit caveats: (1) total dissolved Fe (TDFe) was used only as an indirect proxy for bioavailable Fe2+ because Fe2+ itself "is very difficult to measure in the field"; (2) they did not directly measure nitrogen-fixation rates or molybdate/nutrient uptake, so the paper states its central sulfate-molybdate-nitrogenase mechanism "remains partially hypothetical"; (3) despite being one of five candidate drivers measured, TDFe "showed little significance and was not responsible for differentiating the dominance of cyanobacterial species" -- an acknowledged null result; (4) the authors themselves flag their proposed molybdenum-limitation mechanism as potentially "questionable" because another cited study (Evans & Prepas) found no such Mo limitation of nitrogen-fixing cyanobacteria in a different set of eutrophic saline lakes; (5) decision-tree depth was manually restricted by the authors as a subjective choice to control overfitting, rather than tuned via a reported formal validation procedure; (6) the paper recommends future field studies directly measuring heterocyte presence/abundance as a function of sulfate and nitrogen source, implying this was not done here. The paper also states its underlying data are available only "from the first author after request," i.e., not openly archived.

## Tensions with other findings
Within the paper itself, the authors' central proposed mechanism (sulfate blocks molybdate uptake, starving the molybdenum-dependent nitrogenase enzyme and thereby suppressing N2-fixers) is directly complicated by their own cited counter-example: Evans & Prepas reportedly found nitrogen-fixing cyanobacteria were NOT molybdenum-limited in a different set of eutrophic saline lakes with high sulfate/Mo ratios, leading the authors to call their own explanation "questionable." Separately (reviewer context, not a claim this source makes about other specific papers), this study foregrounds sulfate/molybdenum availability rather than the nitrogen:phosphorus ratio framing more commonly used elsewhere in HAB literature to explain diazotroph vs. non-diazotroph dominance; nitrate and an NH4-based ratio were both measured here, yet plain N:P framing does not appear among the paper's own top-ranked explanatory variables in either layer's decision tree -- a different emphasis than ratio-centric accounts common in other cyanobacteria-dominance literature, worth flagging as a complication rather than a direct contradiction.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Possible hallucinated/misattributed numbers:**
  - five candidate environmental drivers measured (source explicitly lists seven: temperature, O2 saturation, PO43−, NO3−, NH4+, TDFe, SO42−)
- **Dropped caveats:**
  - Elevated TDFe concentrations in bottom waters were specific to two of four water bodies (Piekary, Tyniec), not uniformly present
  - Statistical layer comparison (GLM results): oxygen saturation difference between layers was significant (p=0.0185), but water temperature difference was not (p=0.0636)
  - Dataset geographic and temporal scope limited to Poland near Kraków, May-October period, which bounds generalizability
- **Reviewer notes:** All 13 claims are substantively supported by explicit statements, quoted passages, or data tables in the source text. The core empirical findings (dominance frequencies, decision-tree thresholds, variable importance rankings) all trace cleanly to the Results section. The authors' mechanistic hypothesis (sulfate-molybdenum inhibition) is accurately characterized as present in Discussion but not experimentally confirmed. The methodological limitations (no direct nitrogenase or uptake measurements) are explicitly acknowledged. However, Claim 6 contains a hallucinated number: it states TDFe was 'one of the five candidate environmental drivers measured,' but the abstract explicitly enumerates seven variables. This factual error about the driver count does not invalidate the core finding that TDFe showed no significance."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9738033/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Two WebFetch calls were made against https://pmc.ncbi.nlm.nih.gov/articles/PMC9738033/ (the given ncbi.nlm.nih.gov/pmc/articles/PMC9738033/ URL returned a 301 redirect to this host, which was followed) using two different extraction prompts, and the outputs were reconciled by union as instructed. Full text was accessible (open-access PMC/MDPI article): abstract, methods, results (including exact decision-tree split values and variable-importance scores), discussion, conclusions, funding, conflict-of-interest, and data-availability statements were all retrieved. One minor inconsistency surfaced between the two passes: the bottom-layer variable-importance list was given as 6 named factors with 6 matching scores in the first pass, but the second pass appended "total dissolved Fe" as a named 7th factor without a distinct score -- likely an artifact of the fetch tool's small extraction model dropping a value; I treated the internally-consistent 6-factor/6-score version as primary and flagged rather than invented the discrepancy. The two passes also initially presented some A. flos-aquae decision-tree percentages (44%, 5%, 47%, 3%) without consistently labeling which belonged to the upper vs. bottom layer tree; the second, more detailed pass explicitly assigned layers, and these assignments were cross-checked as consistent with the first pass's raw percentages before being used to attribute upper- vs bottom-layer splits above. The exact calendar year(s) of the 62 field samples (only "May to October" is given, no year) was not present in either retrieved extraction. No data point in this dossier entry was invented; all figures are either direct quotes or values explicitly extracted from the article text by WebFetch.
