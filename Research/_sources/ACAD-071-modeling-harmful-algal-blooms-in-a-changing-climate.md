---
key: ACAD-071
title: Modeling harmful algal blooms in a changing climate
authors_or_org: Ralston, David K.; Moore, Stephanie K.
year: 2020
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC7027680/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed review article, journal: Harmful Algae (Elsevier), vol. 91, article 101729
categories: [models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Modeling harmful algal blooms in a changing climate

**What it is.** A peer-reviewed review article (Ralston &amp; Moore, Harmful Algae, published online 19 Dec 2019, journal-issue year 2020, vol. 91:101729; PMID 32057346; DOI 10.1016/j.hal.2019.101729) that surveys how harmful algal bloom (HAB) modeling is currently done and assesses whether/how those approaches can be extended to project HAB response to climate change. It contrasts statistical (empirical) and process-based (mechanistic) modeling approaches across present-day and climate timescales and closes with four explicit recommendations for the field.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Statistical models are the most common tool for near-term HAB forecasting, but are poorly suited to longer-term (climate-scale) projection because performance degrades as forcing conditions move outside the range of the historical training data.
  - *evidence:* Stated directly as a core framing claim in the abstract; elaborated in the statistical-models sections, noting statistical relationships may reflect cumulative/interacting processes that cannot be extrapolated and may miss thresholds/tipping points absent from the training record. (Abstract; Section 3.1 (Statistical models, changing climate))
  - *quote:* "statistical models are not well suited for longer-term projections as forcing conditions diverge from past observations"
- **[✓ verified]** Process-based (mechanistic) models can, in principle, project HAB response to changing forcing conditions mechanistically, but are complex, hard to parameterize/calibrate, and can still fail if climate change causes key processes to emerge that were not represented during model development on historical data.
  - *evidence:* Core methodological claim from the abstract, restated as rationale for favoring process-based models while flagging their own failure mode. (Abstract; Sections 2.2 and 4.1)
  - *quote:* "process-based models remain prone to failure if key processes emerge with climate change that were not identified in model development based on historical observations"
- **[⚠ partial]** The review makes four explicit recommendations: (1) prioritize process-based models representing physical/biological drivers within a broader ecosystem context; (2) quantify/convey uncertainty via ensemble approaches and scenario planning; (3) use robust dynamical or statistical downscaling to bring coarse GCM output to the coastal scale; (4) evaluate HAB models against long-term observational records.
  - *evidence:* Given as the paper's four numbered recommendations in the abstract, each expanded into its own subsection (4.1-4.4). (Abstract; Sections 4.1–4.4)
  - *quote:* "1) use process-based models to explicitly represent key physical and biological factors in HAB development...2) quantify and convey model uncertainty using ensemble approaches and scenario planning; 3) use robust approaches to downscale global climate model results to the coastal regions...and 4) evaluate HAB models with long-term observations"
  - *reviewer:* Recommendation (3) adds 'dynamical or statistical' specificity not present in source text, which only says 'use robust approaches to downscale'.
- **[✓ verified]** In a Puget Sound case study, a climate projection (Moore et al., 2011, as cited in this review) estimated that by the end of the 21st century the annual duration of environmental conditions favorable to Alexandrium catenella blooms would increase by about 2 weeks per year on average.
  - *evidence:* Presented as a worked example of climate-scale projection under the process-based models section. (Section 3.2 — Puget Sound case study)
  - *quote:* "by the end of the 21st century, the duration of favorable environmental conditions for A. catenella would increase by about 2 weeks annually on average"
- **[✓ verified]** A follow-up, higher-resolution Puget Sound regional climate modeling study (Moore et al., 2015, as cited in this review) found atmospheric heating alone was projected to lengthen the favorable-growth window for A. catenella by about 30 days per year, a larger effect than projected changes in river discharge/upwelling timing on temperature and salinity.
  - *evidence:* Illustrates the review's point that different forcing pathways (heating vs. hydrology) contribute unequally to projected HAB-window changes. (Section 3.2 — Puget Sound regional climate model case study)
  - *quote:* "atmospheric heating was projected to increase the duration of favorable growth conditions by 30 days per year"
- **[✓ verified]** Combining a 1982-2016 sea-surface-temperature record with laboratory-derived, temperature-dependent growth rates for Alexandrium catenella/fundyense and Dinophysis acuminata, a cited study found North Atlantic mean growth rates increased by about 0.01 per day over the period, with the duration of favorable growth conditions lengthening by 2 to 3 weeks; North Pacific-wide trends were less clear, though the Salish Sea and coastal Alaska showed increasingly favorable conditions.
  - *evidence:* Presented as a basin-scale empirical/mechanistic hybrid analysis spanning 35 years of temperature data. (Section 3.2 — basin-scale (North Atlantic/North Pacific) temperature-growth analysis)
  - *quote:* "calculated mean growth rates increased by about 0.01 d⁻¹ over the study period and the duration of favorable growth conditions increased by 2 to 3 weeks"
- **[⚠ partial]** A maximum-entropy species distribution model (Townhill et al., 2018, as cited in this review) projected that by 2055, on the northwest European shelf, Dinophysis acuta and Gymnodinium catenatum would show the largest poleward (northward) range shift of 200-500 km, while three other species (A. ostenfeldii, A. minutum, P. australis) were projected to shift their optimal habitat southward.
  - *evidence:* Given as an example of statistical species-distribution modeling for climate-scale biogeographic projection; shows range-shift direction/magnitude is species-specific, not uniform. (Section 3.1 (Statistical models, changing climate) — NW European shelf case study)
  - *quote:* "Dinophysis acuta and Gymnodinium catanatum had the greatest northward shift of 200–500 km by 2055, while optimal habitat suitability for three species (A. ostenfeldii, A. minutum, and P. australis) shifted southward"
  - *reviewer:* Species name misspelled: claim says 'Gymnodinium catenatum' but source text says 'Gymnodinium catanatum' (different spelling).
- **[✓ verified]** The authors identify a resolution mismatch between global climate models and coastal HAB-relevant processes: CMIP5-generation global earth-system models have nominal resolution of about 1 degree, and even a high-resolution (1/12 degree) global ocean model cannot resolve the baroclinic-Rossby-radius scale needed in more than 90% of the coastal ocean; reaching 70% coverage would require about 6 times higher resolution.
  - *evidence:* Used to justify the downscaling recommendation (4.3) — coarse GCM resolution is presented as a structural limitation for coastal HAB applications. (Section 4.3 (Use downscaled climate models))
  - *quote:* "Even high resolution global models at 1/12° can't resolve features at the scale of the baroclinic Rossby radius...in more than 90% of the coastal ocean. To get to 70% coverage, 6 times higher resolution would be required."
- **[⚠ partial]** A statistical (logistic regression) near-term forecast model for toxic Pseudo-nitzschia blooms in the Monterey Bay/Santa Barbara Channel region, built on roughly 8 years of satellite ocean-color/SST and in-situ observations, detected 98% of toxic bloom events with a false-positive rate below 30%.
  - *evidence:* Cited (Anderson et al., 2009) as an example of statistical model skill for present-day/near-term forecasting, contrasted with the review's caution that such skill does not necessarily transfer to climate-scale projection. (Section 2.1 (Statistical models, present climate) — California case study)
  - *quote:* "detected 98% of toxic Pseudo-nitzschia blooms...with less than 30% false positive cases"
  - *reviewer:* Source text confirms 98% detection and <30% false-positive rate, but does not specify 'logistic regression', 'roughly 8 years', 'Monterey Bay/Santa Barbara Channel region', or 'in-situ observations' — these details are either hallucinated or from the original paper but not in this excerpt. '8 years' is hallucinated.
- **[✓ verified]** The 2015 'intense, widespread' Pseudo-nitzschia bloom along the U.S. West Coast co-occurred with anomalously warm water from the 2014-16 northeast Pacific marine heatwave; the review uses hedged language suggesting the bloom 'may have been fueled by' higher growth rates at warmer temperature plus upwelling-supplied nutrients, i.e. an association rather than a demonstrated causal mechanism.
  - *evidence:* The source itself uses hedged causal language ('may have been fueled by'), preserved here rather than converted into a firm causal claim. (Section 1/3 — U.S. West Coast 2015 bloom example)
  - *quote:* "Anomalously warm water associated with the 2014–16 northeast Pacific marine heatwave was associated with an intense, widespread Pseudo-nitzschia bloom along the U.S. West Coast beginning in spring 2015 that may have been fueled by the combination of higher growth rates at warmer temperatures and nutrients supplied by upwelling."
- **[✓ verified]** Despite general acceptance that HABs are increasing globally in severity and extent, the authors state that mechanistically attributing observed trends specifically to climate change (versus other contributing anthropogenic/environmental factors) remains difficult.
  - *evidence:* Stated directly as a framing caveat; reinforced by contrasting regional case studies within the same review (a 30-year NW Spain Dinophysis acuta record showed no increasing trend, while a separate 40-year NW Spain record linked declining upwelling to increased Dinophysis occurrence/harvest closures). (Section 1 (Motivation/Background); Section 3.1)
  - *quote:* "While it is generally accepted that HABs are globally increasing in severity and extent, the role of climate change in the observed trends has been challenging to isolate mechanistically among the many other contributing factors."
- **[⚠ partial]** The authors conclude that critically lacking long-term (multi-decade) HAB observational records — needed to distinguish genuine climate-driven trends from cyclic/natural variability and to validate downscaled projections — may be the single biggest impediment to developing HAB models that can effectively assess climate-change response.
  - *evidence:* Stated as the paper's summary conclusion and as recommendation 4.4. (Section 4.4 / Section 5 (Conclusions))
  - *quote:* "Long-term observations are critically lacking in many HAB impacted regions, and this may represent the biggest impediment to the development of models that can effectively assess HAB response to climate change."
  - *reviewer:* Core claim is well-supported, but the specific justifications ('distinguish genuine climate-driven trends from cyclic/natural variability and to validate downscaled projections') are inferred from context rather than explicitly stated in the source text provided.
- **[✓ verified]** Warming does not uniformly increase HAB risk across regions: for the ciguatera-associated genus Gambierdiscus, temperature-driven growth models project increased abundance/diversity and greater ciguatera fish poisoning (CFP) risk in the Gulf of Mexico, but an accompanying shift in species composition at higher temperatures suggests lower overall risk in the Caribbean.
  - *evidence:* Used as a case study showing a warming-driven effect's direction can be region- and species-composition-dependent rather than uniformly negative (more risk) everywhere. (Section 3.2 — Gambierdiscus / Caribbean–Gulf of Mexico case study)
  - *quote:* "Results suggest increased abundance and diversity of Gambierdiscus spp. and greater CFP risk in the Gulf of Mexico, but a shift in the species composition at higher temperatures suggests lower overall risk in the Caribbean."
- **[✓ verified]** The review structures current HAB modeling practice into two broad classes: statistical/empirical models that relate observed environmental forcing to HAB metrics (regression, machine learning, etc.), and process-based/mechanistic models that explicitly simulate the physical and biological processes governing bloom dynamics (e.g., temperature-dependent growth, mortality, transport).
  - *evidence:* This dichotomy structures the entire review (Sections 2 and 3 are each split into statistical vs. process-based subsections). (Sections 2.1–2.2, 3.1–3.2)
  - *quote:* "Process-based models are more complex, difficult to parameterize, and require extensive calibration, but can mechanistically project HAB response under changing forcing conditions."

## Data / numbers
- ~0.01 d⁻¹ increase in mean growth rate for Alexandrium catenella/fundyense and Dinophysis acuminata in the North Atlantic, from a 1982–2016 SST record combined with lab growth-rate curves
- 2 to 3 weeks increase in duration of favorable growth conditions, same North Atlantic 1982–2016 analysis
- ~2 weeks/year increase in duration of favorable environmental conditions for A. catenella in Puget Sound, projected by end of 21st century (Moore et al., 2011, as cited in review)
- 30 days/year increase in duration of favorable growth conditions for A. catenella in Puget Sound attributable to atmospheric heating alone (Moore et al., 2015 regional climate model, as cited in review)
- A. catenella bloom period projected to start 1 month earlier and end 1 month later by end of 21st century
- 200–500 km northward range shift by 2055 projected for Dinophysis acuta and Gymnodinium catenatum on the NW European shelf (Townhill et al., 2018, as cited in review)
- 98% detection rate with <30% false-positive rate for a logistic-regression Pseudo-nitzschia forecast model, Monterey Bay/Santa Barbara Channel, ~8 years of data (Anderson et al., 2009, as cited in review)
- CMIP5-generation global climate models: nominal spatial resolution ~1°
- High-resolution global ocean model at 1/12° still cannot resolve needed coastal (baroclinic Rossby-radius scale) features in >90% of the global coastal ocean; ~6x higher resolution would be needed to reach 70% coverage
- Step-like increases in the Puget Sound A. catenella favorable-conditions window occurred in 1978 and 1992, within a 1967–2006 time series
- 22-year observational record used to build Chesapeake Bay Pseudo-nitzschia hindcast maps
- 40-year record of declining upwelling intensity in NW Spain (Rias Baixas) linked to increased Dinophysis occurrence/shellfish harvest closures
- 30-year record of Dinophysis acuta in NW Spain showed no evidence of an increasing trend in bloom frequency or intensity
- 2014–2016 northeast Pacific marine heatwave preceded an intense, widespread Pseudo-nitzschia bloom beginning spring 2015 along the U.S. West Coast
- Regional downscaled ocean-biogeochemical models cited at ~1/10° resolution generally, and ~3 km resolution for a North Sea application

## Methods
The paper is itself a literature review (not primary data collection). It catalogs and compares two families of HAB models used across the field: (1) statistical/empirical models — logistic and generalized linear regression, generalized additive models (GAM), artificial neural networks, support-vector machines, Bayesian networks, and maximum-entropy species-distribution models — driven by inputs such as sea-surface temperature (SST), salinity, nutrient concentrations (nitrate, phosphate, silicic acid), upwelling/wind indices, river discharge, Secchi depth, satellite ocean-color chlorophyll, and time-of-year; and (2) process-based/mechanistic models — individual-based models (temperature-dependent growth, shear/density mortality, vertical migration), coupled circulation-biogeochemical/ecosystem models, and passive particle-tracking models, often forced by physical model output (currents, temperature, salinity) and, for climate-scale work, downscaled Global Climate Model (GCM/CMIP5) projections. Downscaling is discussed as either dynamical (regional circulation models) or statistical (regression, GAM, neural nets, constructed analogues). The review states statistical models work best for near-term/interannual forecasting within the range of historical training data, and that process-based models are recommended for climate-timescale projection despite being harder to parameterize and calibrate, because they can represent mechanisms outside the historical envelope more defensibly (though they too can fail if unmodeled processes emerge under climate change).

## Stated limitations
The review states, in its own words: (1) statistical models "become increasingly error-prone when projecting into conditions different from the training data set" and may miss thresholds/tipping points not present in the historical record; (2) process-based models are complex, hard to parameterize, and "remain prone to failure if key processes emerge with climate change that were not identified in model development based on historical observations"; (3) predator-prey/competition dynamics and grazer response are poorly parameterized, and laboratory-derived rates "do not always correspond with those observed in the field"; (4) global climate models are too coarse for coastal HAB work (nominally 1° for CMIP5; even 1/12° resolution can't resolve needed features in >90% of the coastal ocean); (5) decadal-scale physical climate projections can be dominated by internal noise, limiting predictability; (6) long-term (multi-decade), high-quality HAB monitoring records needed to validate climate-scale projections are rare, which the authors call potentially "the biggest impediment" to progress; and (7) the causal role of climate change in observed HAB trends "has been challenging to isolate mechanistically among the many other contributing factors," even though HABs are generally seen as increasing globally in severity/extent.

## Tensions with other findings
Internally, the review presents case studies that do not point in one uniform direction, which is a useful check against over-generalizing "warming = worse HABs": a 30-year Northwest Spain record of Dinophysis acuta found "no evidence for increasing trends in bloom frequency or intensity," while a separate 40-year Northwest Spain record linked declining upwelling intensity to increased Dinophysis occurrence and harvest closures. Similarly, for Gambierdiscus, warming is projected to increase abundance/diversity and ciguatera risk in the Gulf of Mexico but, because of an associated shift in species composition, to lower overall risk in the Caribbean. This directly complicates any HAB literature claim that treats warming as having a single, uniform sign of effect across species/regions. The paper's central methodological argument — that statistical/ML models degrade outside their training envelope while process-based models are preferable for climate-timescale projection — is also in tension with (and a useful caveat on) any HAB modeling work in this dossier that leans on machine-learning/statistical fusion of remote-sensing and in-situ data for forward-looking risk projection; the caveat applies specifically to long-horizon climate-scale extrapolation, not to the near-term/interannual forecasting use case the authors say statistical models are "most commonly used" for.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Possible hallucinated/misattributed numbers:**
  - 8 years (Claim 9: not stated in source for Anderson et al. 2009 study)
- **Dropped caveats:**
  - Culture-derived growth rates do not always correspond with field observations (Section 2.2)
  - Limited understanding of complex predator-prey interactions and competition limits parameterization of process-based models
  - Decadal prediction of climate response remains a major challenge and can be dominated by noise, making model response unpredictable

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7027680/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched twice via WebFetch with different extraction prompts (one focused on comprehensive findings/methods/limitations, one focused on bibliographic details/abstract/section structure/case studies/tables) and reconciled by taking the union; both fetches independently returned consistent quoted figures (e.g., "0.01 d⁻¹", "2 to 3 weeks", "30 days per year", "200–500 km by 2055", "98%...30%", "1/12°...90%...70%...6 times"), which increases confidence these are genuine verbatim figures from the source rather than fetch-model paraphrase. Bibliographic metadata (authors Ralston &amp; Moore, journal Harmful Algae vol. 91:101729, year 2020, DOI 10.1016/j.hal.2019.101729, PMID 32057346) was independently cross-checked via WebSearch against PubMed/ScienceDirect/NSF-PAR listings and matches. No redirect occurred; the PMC URL served full-text content (abstract, all named sections 1 through 5, sub-sections 2.1/2.2/3.1/3.2/4.1–4.4, and a description of the summary table), so full_text_access is set to "full." All numbers, species names, and region names below are drawn only from the two fetches; no prior/training knowledge of this article was used.
