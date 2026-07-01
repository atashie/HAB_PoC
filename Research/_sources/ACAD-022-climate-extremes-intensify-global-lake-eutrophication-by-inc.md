---
key: ACAD-022
title: Climate extremes intensify global lake eutrophication by increasing the stress resistance of harmful bloom-forming algae
authors_or_org: Chenyu Wang, Mengmeng Wang, Mengjiao Xie, Liya Qi, Menggaoshan Chen, Xiaohua Song, Zhi Zhou, Xiaoli Shi, Jingyun Yin, Yong'an Wei, Minxiang Xu, Liyu Pan, Ai-Jun Miao, Liuyan Yang
year: 2026
url: https://www.nature.com/articles/s41467-026-69529-3
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed primary research article, Nature Communications (Springer Nature)
categories: [basic-science]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Climate extremes intensify global lake eutrophication by increasing the stress resistance of harmful bloom-forming algae

**What it is.** A 2026 Nature Communications primary-research article (volume 17, article 2859) that combines a 20-year global satellite bloom-frequency record (2003-2022, 607 large shallow lakes), an in-situ 547-lake nutrient/Chl-a dataset, ERA5 climate-reanalysis data, and laboratory/field physiological experiments on four cyanobacterial species to argue that short-duration climate extremes (heatwaves, extreme precipitation) -- rather than only gradual warming or nutrient loading -- intensify lake eutrophication, via a proposed heat/pH-induced "thermo-alkaline" mechanism in which harmful bloom-forming algae form dense polyphosphate-rich "stabilisome" organelles that act as ballast, driving downward migration to sediment phosphorus and enabling internal phosphorus reserves that carry over between climate-extreme events.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Short-term climate extremes (heatwaves and extreme precipitation) -- not gradual warming -- are presented as the dominant drivers of global bloom variability and intensification.
  - *evidence:* Stated as the paper's central thesis in the title/abstract and supported by a GAM/machine-learning variable-importance analysis showing temperature-anomaly and precipitation-extreme predictors retain high, stable importance across alternative model formulations, while gradual climatic indicators do not. (Abstract; Results section on climate extremes and global bloom trajectories)
  - *quote:* "heatwaves and extreme precipitation drive bloom dynamics beyond gradual warming"
- **[✓ verified]** Heatwave exposure triggers oxidative stress in harmful bloom-forming algae (HBFA) that rapidly induces intracellular polyphosphate and forms dense polyphosphate-rich organelles termed 'stabilisomes.'
  - *evidence:* Central mechanistic finding from laboratory dose-response experiments across four cyanobacterial species and a 25–45°C gradient, visualized via microscopy in Fig. 3. (Abstract; Results 'Stabilisome Formation and Vertical Migration'; Fig. 3 caption)
  - *quote:* "heatwaves trigger oxidative stress that rapidly induces intracellular polyphosphate and stabilisomes, dense polyphosphate-rich organelles"
- **[✓ verified]** Stabilisomes act as intracellular ballast that drives cells to migrate downward in the water column, giving access to sediment-derived phosphorus while letting cells escape near-surface thermal stress.
  - *evidence:* Supported by vertical-migration column experiments (n=5 columns per treatment, 25 vs 40°C) showing greater accumulation at 15-30cm depth, plus a density argument that stabilisomes are denser than other measured cellular constituents. (Abstract; Results 'Stabilisome Formation and Vertical Migration'; Fig. 4 caption)
  - *quote:* "stabilisomes drive downward migration, enabling access to sediment-derived phosphorus while avoiding thermal stress"
- **[✓ verified]** Photosynthetic CO2 depletion during blooms elevates pH, reinforcing what the authors term a 'thermo-alkaline cascade' that amplifies the stress-driven phosphorus response.
  - *evidence:* Linked to a parallel alkaline-stress dose-response experiment (pH 7-10) that reproduces similar phosphorus/oxidative-stress responses as heat stress, plus field co-occurrence of elevated temperature and elevated pH during a Lake Taihu bloom. (Abstract; Discussion mechanism summary)
  - *quote:* "CO2 depletion elevates pH and reinforces a thermo-alkaline cascade amplification effect"
- **[✓ verified]** Extreme precipitation delivers pulsed phosphorus inputs that algae store as intracellular polyphosphate, creating a long-lived phosphorus reserve that 'primes' subsequent heatwave-driven bloom intensification.
  - *evidence:* Supported by sediment/suspended-particulate-matter phosphorus-release experiments and by the GAM finding that adding precipitation terms increases the deviance in Chl-a explained by temperature. (Abstract; Results 'Extreme Precipitation and Phosphorus Uptake'; Results 'GAM Analysis Integration')
  - *quote:* "Extreme precipitation delivers pulsed phosphorus inputs that are stored as intracellular polyphosphate, creating long-lived phosphorus reserves that prime later heatwaves"
- **[✓ verified]** When a precipitation pulse precedes a heatwave, stabilisome formation, vertical migration and bloom expansion are amplified, including in low-nutrient (oligotrophic) lakes that would otherwise be considered less bloom-prone.
  - *evidence:* Synthesis conclusion combining the laboratory precipitation/phosphorus-storage results with the heatwave/bloom mechanism; explicitly extends the claim to oligotrophic systems. (Abstract)
  - *quote:* "When precipitation pulses precede heatwaves, stabilisome formation, vertical migration, and bloom expansion are amplified, even in oligotrophic lakes"
- **[✓ verified]** The global satellite bloom-frequency analysis is built on 607 large shallow lakes with blooms persisting more than 10 years (2003-2022), drawn from an initial global inventory of 1,956 freshwater lakes >50 km², detected across roughly 0.8 million MODIS-Aqua images at about 81% classification accuracy.
  - *evidence:* Describes the scale, provenance (built on the Wang et al. 2025 global lake bloom dataset), and validation of the remote-sensing dataset underlying the global trend/GAM analysis. (Results 'Climate Extremes and Global Bloom Trajectories'; Fig. 1 caption)
  - *quote:* "607 large shallow lakes worldwide that experienced blooms for more than 10 years during 2003–2022"
- **[✓ verified]** GAM-based variable-importance analysis found temperature anomalies and extreme-precipitation metrics to be the dominant and most stable predictors of Chl-a/bloom trajectories, whereas gradual climatic indicators (e.g., mean warming trends) were comparatively more sensitive to how the model was specified.
  - *evidence:* Explicit robustness check described as tested across 'alternative model formulations'; used to argue extremes are a more reliable statistical signal than gradual trends, though this is a correlational/predictive-importance result, not an experimental causal test at the global scale. (Results 'Climate Extremes and Global Bloom Trajectories')
  - *quote:* "temperature anomalies and extreme precipitation metrics retain consistently high importance across alternative model formulations, whereas gradual climatic indicators exhibit greater sensitivity to model structure"
- **[✓ verified]** Adding extreme-precipitation terms to temperature-based GAMs increased the fraction of deviance in lake Chl-a explained by temperature, in both oligotrophic and eutrophic lake subsets, which the authors interpret as precipitation amplifying rather than acting as an independent driver of temperature's effect.
  - *evidence:* Direct quantitative before/after model-comparison result reported as deviance-explained values. (Results 'GAM Analysis Integration')
  - *quote:* "the deviance explained by temperature increased from 0.138 to 0.153 in oligotrophic lakes and from 0.093 to 0.146 in eutrophic lakes when precipitation was included"
- **[✓ verified]** Across a global sample of documented summer lake heatwaves, the large majority co-occurred with pronounced chlorophyll-a increases, with especially large relative increases in nutrient-poor lakes.
  - *evidence:* Direct empirical event-count/attribution result presented as corroborating field-scale evidence for the heatwave-bloom mechanism found in the laboratory work. (Results (heatwave attribution discussion))
  - *quote:* "24 of 29 documented summer lake heatwaves coincided with pronounced Chl-a increases, with mean enhancements exceeding 50% in low-nutrient lakes"
- **[✓ verified]** Laboratory heat stress (40°C vs 25°C) produced large, consistent increases in oxidative-stress markers, antioxidant enzyme activity, and phosphorus fractions across four cyanobacterial bloom-forming species (unicellular and filamentous).
  - *evidence:* Controlled dose-response experiment with n=5 biological replicates per species/treatment across a 25-45°C gradient. (Results 'Heatwave Stress Responses'; Fig. 2 caption)
  - *quote:* "Exposure to 40°C increased reactive oxygen species (ROS) by 35.9–215.8%... elevated antioxidant enzyme activities by 0.55–6.30 fold... raised malondialdehyde levels by ~0.81–1.96 fold relative to 25 °C"
- **[✓ verified]** Alkaline stress alone (pH 10 vs pH 7) independently produced comparably large increases in intracellular phosphorus fractions and oxidative-stress markers as heat stress, supporting the pH side of the proposed 'thermo-alkaline' mechanism.
  - *evidence:* Parallel dose-response experiment (pH 7-10 gradient) run across the same four species, paired with microscopy in Fig. 3. (Results 'Alkaline Stress and polyP Accumulation'; Fig. 3 caption)
  - *quote:* "intracellular TP, DIP, and polyP (27.1–209.1%, 81.6–156.4%, and 98.5–153.5% relative to pH 7)"
- **[✓ verified]** Warmer water accelerates phosphorus release from sediments and suspended particles into the water column, and algae take up phosphorus in 'luxury' excess of immediate metabolic need within hours, providing a rapid physico-chemical-plus-physiological pathway from heat to increased phosphorus availability.
  - *evidence:* Dialysis-bag sediment/suspended-particulate-matter incubation experiments at 15/25/35°C, paired with short-term (4 h) cellular uptake assays. (Results 'Extreme Precipitation and Phosphorus Uptake'; Fig. 5 caption)
  - *quote:* "DIP and TP released from suspended solids and sediments increased by ~1.57–9.43 fold at 25–35 °C relative to 15 °C"
- **[✓ verified]** The authors argue their findings challenge nutrient-centric bloom-management models and recommend shifting from mean-nutrient-load reduction toward management approaches that explicitly account for climate extremes and nutrient 'pulse' regimes, and that internal polyphosphate storage helps explain why external load-reduction programs often show delayed or muted water-quality improvement.
  - *evidence:* Interpretive/normative management recommendation drawn in the Discussion from the combined lab-mechanism and global-pattern results, not itself a new measured quantity. (Discussion)
  - *quote:* "shifting from mean-load reduction to pulse-oriented management strategies"
- **[✓ verified]** The paper cites a prior estimate that roughly 47% of global lake degradation is attributable to intensified land use and nutrient emissions (population-linked pressure), but argues this gradual anthropogenic pressure alone cannot explain the large year-to-year swings observed in bloom extent, which motivates the climate-extremes analysis.
  - *evidence:* Framing/motivation statement citing an external figure to argue that gradual anthropogenic drivers are necessary but insufficient to explain interannual bloom variability -- an explicitly correlational contrast set up before the climate-extremes analysis. (Results 'Climate Extremes and Global Bloom Trajectories' (introductory framing))
  - *quote:* "47% of global lake degradation has been attributed to intensified land use and nutrient emissions"

## Data / numbers
- Satellite record: 2003–2022 (20 years), ~0.8 million MODIS-Aqua images, 1–2 day temporal resolution
- 1,956 large freshwater lakes globally (>50 km² surface area) in the base inventory
- 607 large shallow lakes with persistent blooms >10 years (2003–2022) used for global bloom-frequency trend/GAM analysis
- In-situ Chl-a/nutrient dataset: 547 lakes worldwide (compiled by Qin et al.)
- Satellite bloom classification accuracy: ~81%
- ~47% of global lake degradation attributed (in prior literature cited by authors) to intensified land use and nutrient emissions
- 24 of 29 documented summer lake heatwaves coincided with pronounced Chl-a increases
- Mean Chl-a enhancement >50% in low-nutrient lakes during heatwave-linked bloom events
- Lab temperature treatments: 25, 30, 35, 40, 45 °C; pH treatments: 7, 8, 9, 10
- ROS increase at 40°C vs 25°C: 35.9–215.8%
- SOD/CAT antioxidant enzyme activity increase at 40°C: 0.55–6.30 fold
- MDA (lipid peroxidation) increase at 40°C: ~0.81–1.96 fold
- Heat shock protein (HSP) increase at 40°C: 47.5–66.2%
- Polyphosphate (polyP) increase at 40°C vs 25°C: 57.9–197.0%
- Intracellular TP increase at 40°C: 18.4–86.5%; intracellular DIP increase: 36.7–93.1%
- At pH 10 vs pH 7: TP +27.1–209.1%, DIP +81.6–156.4%, polyP +98.5–153.5%
- Algal accumulation depth from heat-induced stabilisome ballast: 15–30 cm (vs surface layers)
- DIP uptake within 4 h at elevated temperature: +201.1–2,011.1% of initial cellular content; TP uptake: +142.2–868.0%
- Sediment/suspended-particle DIP and TP release: ~1.57–9.43 fold higher at 25–35°C vs 15°C
- Stabilisome bulk density 1.79–3.13 g cm⁻³ vs protein 1.3–1.43, nucleic acid 2, carbohydrate 1.55–1.62, lipid 0.91–1.01 g cm⁻³
- Field validation, Lake Taihu (8 Sept 2022, bloom season): water temp 26–35°C, pH 8.6–9.2, TP 0.076 mg L⁻¹, TN 1.03 mg L⁻¹, DO 8.1 mg L⁻¹
- GAM deviance explained by temperature on Chl-a: oligotrophic lakes 0.138 → 0.153 when precipitation added; eutrophic lakes 0.093 → 0.146 when precipitation added
- Biological replicates: n = 5 per treatment/species across lab experiments
- Global dataset lake coverage: ~51% of global freshwater lake area
- Statistical software: R v4.4.2 with mgcv package v1.9-4; significance threshold p < 0.05; 95% confidence intervals reported
- Precipitation extreme indices used: Rx1day (annual max 1-day precipitation), R95p (annual total precip from days >95th percentile), PTOT (cumulative precip from extreme events >95th percentile)
- Publication: Nature Communications, volume 17, article number 2859, published 17 February 2026

## Methods
Multi-method study combining: (1) Global remote sensing -- built on the Wang et al. (2025) global lake algal-bloom dataset derived from the complete MODIS-Aqua archive (2003-2022, ~0.8 million images, 1-2 day resolution) using Rayleigh-corrected reflectance (Rrc) and normalized Floating Algal Index (nFAI) with CIE color-space masking to separate blooms from sediment, applied to 1,956 lakes >50 km^2 (~81% classification accuracy), yielding a 607-lake subset with >10 years of persistent blooms for trend/GAM analysis; (2) In-situ data -- a 547-lake worldwide Chl-a/nutrient (TN, TP) dataset originally compiled by Qin et al.; (3) Climate/demographic covariates -- ERA5 reanalysis (ECMWF/Copernicus) for temperature anomalies and daily precipitation, extreme-precipitation indices (Rx1day, R95p, PTOT), UN World Population Prospects and WorldPop population data; (4) Statistics -- Generalized Additive Models with penalized smooths (R v4.4.2, mgcv v1.9-4), reporting deviance explained, effective degrees of freedom, F statistics and p-values, plus GAM-based/machine-learning variable-importance analysis tested across 'alternative model formulations' for robustness (p<0.05 significance, 95% CIs); (5) Laboratory experiments -- dose-response exposures of four cultured cyanobacterial HBFA species (Microcystis aeruginosa, Raphidiopsis raciborskii, Dolichospermum flos-aquae, Aphanizomenon flos-aquae; BG11 medium) to temperature (25-45°C) and pH (7-10) gradients, measuring oxidative-stress markers (ROS, SOD, CAT, MDA, HSP via commercial assay kits), photosynthetic performance (Phyto-PAM: Y(II), Fv/Fm, ETRm), phosphorus fractions (TP, DIP, polyP via molybdenum-blue and toluidine-blue-O/HCl-hydrolysis assays), stabilisome nanoparticle characterization (NanoSight NS300 nanoparticle tracking, density via freeze-dry weighing), vertical-migration column experiments, and sediment/suspended-particulate-matter phosphorus-flux experiments using dialysis-bag incubations at 15/25/35°C; (6) Field validation -- bloom and sediment samples from Lake Taihu (8 Sept 2022) and bloom samples from five other Asian lakes (Chaohu, Hulun, Tianlai, Dianchi, Khanka), with in-situ temperature/DO/pH via a HACH HQ30-D probe. The approach works well for detecting broad-scale, statistically robust bloom-frequency trends and for demonstrating a reproducible, cross-species physiological mechanism (n=5 replicates, 4 taxonomically distinct unicellular/filamentous species) linking heat/pH stress to phosphorus storage and vertical migration. It is explicitly stated to fall short of resolving lake-specific hydrodynamics/internal nutrient cycling at global scale, and the satellite bloom metric is acknowledged as surface-biased.

## Stated limitations
Authors state three explicit caveats: (1) the satellite-derived bloom-frequency metric is "surface-sensitive" and "primarily captures surface or near-surface algal accumulations, potentially underrepresenting subsurface biomass in some lake systems"; (2) although a single consistent MODIS-Aqua sensor and validated detection framework "minimizes cross-sensor and classification uncertainties," the global-scale statistical analysis does not explicitly resolve "lake-specific hydrodynamics and internal nutrient cycling processes"; (3) on mechanism, "further work is needed to resolve how thermal stress, hydrological variability, and cellular physiological adjustments interact to support bloom persistence and intensification under extreme climatic conditions." Additionally, the GAM robustness analysis itself notes that "gradual climatic indicators exhibit greater sensitivity to model structure" (i.e., less stable/robust as predictors than the extremes-based metrics), which is a caveat on that portion of the evidence. The laboratory mechanism was demonstrated in only four cultured cyanobacterial species; the source text does not claim this generalizes to all HBFA taxa.

## Tensions with other findings
The paper explicitly positions itself against "nutrient-centric models" of bloom management, arguing internal phosphorus storage (polyphosphate/stabilisomes) driven by climate extremes can sustain and expand blooms "even in oligotrophic lakes" and can explain why external nutrient load-reduction programs "often yield delayed or muted improvements in water quality." This creates tension with HAB literature/management frameworks built primarily around external nutrient (P/N) load reduction as the primary lever, and argues for supplementing them with "pulse-oriented" climate-extreme-aware management. It also complicates simple gradual-warming narratives: the authors report gradual climatic indicators are statistically less robust/more model-sensitive predictors than extreme-event metrics, i.e., mean-warming trend framing may be a less reliable statistical signal for bloom risk than heatwave/precipitation-extreme framing. Methodologically, note a duality worth flagging when citing this source: the global multi-lake link between climate extremes and Chl-a is a statistical/correlational (GAM variable-importance) result, while the causal, mechanistic "why" (stabilisome formation, ballast-driven migration, luxury P uptake) is established separately via controlled laboratory dose-response experiments on 4 species -- the two lines of evidence are complementary but not the same type of evidence, and the source itself does not claim the global correlation alone proves causation.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Satellite observations primarily capture surface or near-surface algal accumulations and may underrepresent subsurface biomass in some lake systems
  - Lake-specific hydrodynamics and internal nutrient cycling processes are not explicitly resolved in the global-scale analysis
  - Further work is needed to resolve how thermal stress, hydrological variability, and cellular physiological adjustments interact to support bloom persistence and intensification under extreme climatic conditions
- **Reviewer notes:** All 15 claims are directly supported by the source text. Every numerical claim traces exactly to the provided excerpts, with no hallucinated figures. The claims accurately represent the paper's findings on climate extremes, mechanistic pathways (stabilisomes, thermo-alkaline cascade), global dataset scale, variable-importance robustness, laboratory dose-response experiments, and management implications. Three significant caveats regarding satellite-observation limitations, unresolved hydrodynamics, and need for future mechanistic integration are present in the source but not reflected in the extraction—these merit flagging for stakeholder communication but do not undermine the supported status of any claim."

## Provenance
- Canonical URL: https://www.nature.com/articles/s41467-026-69529-3
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Followed the automatic redirect chain both times (nature.com -> idp.nature.com/authorize -> idp.nature.com/transit -> nature.com?error=cookies_not_supported&code=...), which resolved back to the same canonical article page each time (this is Nature's cookie-consent bounce, not a paywall block). WebFetch #1 (prompt focused on comprehensive numbers/methods/limitations) and WebFetch #2 (prompt focused on verbatim abstract, authors, Results/Discussion narrative, policy language, limitations, figure captions) both returned substantial, overlapping and complementary content, including full Results subsections, Discussion/mechanism language, explicit limitations, and all 6 main-figure captions -- consistent with this being a fully open-access Nature Communications article (the second fetch explicitly noted 'Open Access: Yes'). Ran one confirmatory WebSearch, which verified the title, DOI/article path (s41467-026-69529-3), volume 17 / article 2859 / publication date 17 Feb 2026, and surfaced an independent ResearchGate mirror (publication ID 400885725) as corroboration that the article exists and is indexed; attempted to WebFetch that ResearchGate mirror to recover fuller author-affiliation detail but it returned HTTP 403 (blocked), so institutional affiliations for the 14 named authors are not resolved beyond names captured from the Nature page (WebFetch #2 could not read institution labels [1],[2],[3] from the rendered page). No numbers were fabricated; all figures reported here are as returned by the fetch tool in quoted form from the source page across the two fetches, reconciled/deduplicated into one set.
