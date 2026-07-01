---
key: ACAD-090
title: Selection of photosynthetic traits by turbulent mixing governs formation of cyanobacterial blooms in shallow eutrophic lakes
authors_or_org: Huaming Wu, Xingqiang Wu, Lorenzo Rovelli, Andreas Lorke (Institute for Environmental Sciences, RPTU Kaiserslautern-Landau; Chinese Academy of Sciences co-authorship per search metadata)
year: 2024
url: https://academic.oup.com/ismej/article/18/1/wrae021/7597770 (cross-checked against full-text mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC10945370/)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article — numerical/mechanistic modeling study (The ISME Journal)
categories: [basic-science]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Selection of photosynthetic traits by turbulent mixing governs formation of cyanobacterial blooms in shallow eutrophic lakes

> Note: provisional URL was resolved to a primary source. Original: https://academic.oup.com/ismej/article/18/1/wrae021/7597770

**What it is.** A numerical modeling study (The ISME Journal, vol 18, issue 1, article wrae021, published 2 Feb 2024, DOI 10.1093/ismejo/wrae021) that couples a one-dimensional hydrodynamic model with a trait-based phytoplankton model to test whether intraspecific variation in photosynthetic capacity (Pmax) within Microcystis populations — as shaped by turbulent mixing and turbidity — governs the timing, severity, and phenotypic composition of cyanobacterial bloom/surface-scum formation in shallow eutrophic lakes. It is a purely simulation-based mechanistic study (no new field or lab data collected), run across 126 idealized scenarios (6 populations × 7 turbulence levels × 3 turbidity levels, 180 simulated days each).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Turbulence acts as a directional selective driver on the Pmax composition of a Microcystis population: depending on the intensity of daily-periodic (wind-driven) turbulence, the population-averaged phenotype shifts toward either low Pmax (favoring light capture in upper layers) or high Pmax (favoring efficient light use).
  - *evidence:* Stated as the paper's top-line result in the abstract, derived from comparing simulation outcomes across 7 turbulence intensities (Dz,max from 10⁻⁶ up to 10⁻³ m² s⁻¹ plus a 'complete mixing' condition). (Abstract; Results)
  - *quote:* "Our results revealed that turbulence acts as a directional selective driver for changes in Pmax."
- **[✓ verified]** Moderate turbulence produces a stable, near-total dominance of the lowest-Pmax trait group (g1) — its relative cell density exceeded 99.9% under Dz,max = 1×10⁻⁴ m² s⁻¹ — whereas stronger turbulence (Dz,max = 1×10⁻³ m² s⁻¹) preserved substantially more trait diversity (other trait groups g2–g10 collectively reaching roughly 8% or more).
  - *evidence:* Simulation output tracking relative cell density (RC) of each of 10 discretized Pmax trait groups (g1-g10) through the 180-day runs; corroborated across two independent extraction passes of the same article. (Results (population composition dynamics))
  - *quote:* "Moderate turbulence can induce a stable reduction in the photosynthetic capacity of the population."
- **[✓ verified]** Populations with wider intraspecific Pmax diversity form severe surface scum up to more than four times faster than populations with narrower Pmax diversity, all else equal.
  - *evidence:* Comparison across the six simulated Microcystis populations (I–VI), which differ only in their initial range of Pmax values, under matched turbulence/turbidity conditions. (Abstract; Results)
  - *quote:* "high intraspecific diversity in Pmax accelerated the formation of surface scum by up to more than four times compared to a lower diversity."
- **[✓ verified]** Higher background turbidity speeds up the onset of decline in population-averaged Pmax (time-to-onset fell from 40 days at Kbg=0.6 m⁻¹, to 12 days at 1.2 m⁻¹, to 7 days at 1.8 m⁻¹) but delays the later reversal/recovery of Pmax, with high turbidity delaying the reversal point by a factor of 2.5 relative to low turbidity.
  - *evidence:* From simulations that varied the background light-extinction coefficient (Kbg) across three levels while holding other conditions fixed; numbers confirmed verbatim in the PMC full-text pass. (Results (turbidity effects))
  - *quote:* "as turbidity increased, the time at which Pmax started to change decreased from 40 to 12 days and 7 days ... High turbidity (1.8 m−1) delayed the occurrence of the reversal by a factor of 2.5"
- **[⚠ partial]** Across all 126 simulated scenarios, the time needed to reach a moderate or severe bloom threshold ranged from 26 days up to more than 180 days (i.e., some parameter combinations never crossed the threshold within the simulated period); under the most favorable condition (low turbulence, low turbidity) all six populations reached a moderate bloom within a similar, narrow 26–27 day window regardless of their Pmax diversity.
  - *evidence:* Bloom-timing outcome compared across the full simulation matrix (6 populations x 7 turbulence levels x 3 turbidity levels). (Results)
  - *quote:* "The timescale for moderate and severe bloom formation ranged from 26 to >180 days ... the time required for all the tested populations to form a moderate bloom was similar, ranging from 26 to 27 days"
  - *reviewer:* The timescale ranges (26–>180 days) are clearly stated in the source. However, the source does not explicitly specify that the 26–27 day convergence occurs under 'the most favorable condition (low turbulence, low turbidity)'. This condition attribution is an inference by the claim-maker, not a stated fact in the source text.
- **[✓ verified]** The model architecture couples (i) a one-dimensional hydrodynamic model, (ii) an ensemble-averaged transport model for trait-specific cell density/colony size/cell-tissue density, and (iii) an ecological (photosynthesis/growth) model; it was run for 6 Microcystis populations (each split into 10 Pmax trait groups, g1-g10) x 7 turbulence levels x 3 turbidity levels = 126 total 180-day simulations, implemented in MATLAB 2022b.
  - *evidence:* Direct methods description of model structure and simulation design, confirmed verbatim via the PMC full-text pass. (Methods)
  - *quote:* "Our model consists of three components: (i) a one-dimensional hydrodynamic model, (ii) an ensemble-averaged transport model for simulating the trait-specific vertical distribution dynamics of cell number concentration, colony size, and cell-tissue density, and (iii) an ecological model describing cell and colony photosynthesis and growth. ... We used six Microcystis populations with initially varying ranges of Pmax (population I – VI) ... each population is composed of ten trait groups (g1-g10) ... resulting in a total of 126 simulations (6 × 7 × 3)."
- **[✓ verified]** The authors propose that controlled, moderate artificial mixing applied during a bloom event could reduce the diversity of photosynthetic capacity within the population, lower its resilience, and thereby help mitigate future blooms — framed as a model-derived management hypothesis, not a field-tested intervention.
  - *evidence:* Discussion-section implication drawn from the simulated mechanism (moderate turbulence suppressing trait diversity); the source does not report any field or mesocosm trial of artificial mixing. (Discussion)
  - *quote:* "implementing controlled, moderate artificial mixing during bloom events could potentially reduce the diversity of photosynthetic capacity, lower the resilience of the population, and mitigate future blooms."
- **[✓ verified]** The model assumes Microcystis growth depends solely on irradiance, holds Pmax fixed within each trait group (no phenotypic plasticity), and neglects temperature effects, nutrient limitation, cell adhesion/colony disaggregation, and other traits (e.g., toxigenicity, variable optimal light intensity); the authors state it does not capture all processes that influence real bloom dynamics.
  - *evidence:* Self-stated scope limitations in the discussion/conclusion, confirmed verbatim in the PMC pass and consistent across both OUP passes. (Discussion (limitations))
  - *quote:* "Our model did not account for all the processes that may directly or indirectly influence the dynamics of cyanobacterial populations due to the partially unclear mechanisms involved."

## Data / numbers
- Water depth (model domain): 3 m
- Vertical grid resolution: 0.05 m
- Cell-tissue density range: 996–1130 kg m⁻³ (resolution 3.35 kg m⁻³)
- Colony size range: 10–420 μm (resolution 10 μm)
- Initial cell density: 2×10⁴ cells mL⁻¹
- Initial colony size: 50 μm; initial cell-tissue density 998 kg m⁻³ (neutrally buoyant)
- Optimal light intensity Iopt ≈ 277.5 μmol photons m⁻² s⁻¹
- Initial slope of P–I curve S = 2×10⁻⁷ (μmol photons)⁻¹ m²
- Max carbon uptake rate gmax = 5.5×10⁻⁶ s⁻¹ (≈0.48 d⁻¹)
- Respiration rate R = 0.55×10⁻⁶ s⁻¹
- Loss (mortality) rate = 0.1 d⁻¹
- Cell volume 67×10⁻¹⁸ m³; carbon content per cell 14×10⁻¹⁵ kg
- Carbohydrate/glycogen ballast Bg = 2.38 g per g assimilated carbon
- Population mean Pmax = 28.9×10⁻⁶ s⁻¹
- Nighttime turbulent diffusivity Dz,max = 10⁻⁶ m² s⁻¹ (constant, 18:00–6:00)
- Daytime Dz,max levels tested: 5×10⁻⁶, 1×10⁻⁵, 5×10⁻⁵, 1×10⁻⁴, 5×10⁻⁴, 1×10⁻³ m² s⁻¹, plus a 'complete mixing' condition (7 turbulence conditions total)
- Background light extinction coefficients Kbg: 0.6, 1.2, 1.8 m⁻¹ (3 turbidity levels)
- 10 trait groups per population (g1–g10); 6 populations (I–VI); 126 total simulations (6×7×3)
- Simulation duration: 180 days; temporal resolution 1.2–120 s
- Max depth-averaged cell density reached: ~3.2×10⁶ cells mL⁻¹
- Surface scum cell density: ~1.8×10⁸ cells mL⁻¹
- Scum formation acceleration with high vs low Pmax diversity: >4× faster (verbatim: 'up to more than four times')
- g1 relative cell density under moderate turbulence (Dz,max=1×10⁻⁴ m² s⁻¹): >99.9%
- Non-g1 trait groups' combined relative cell density under strong turbulence (Dz,max=1×10⁻³ m² s⁻¹): ~8% (single-pass corroboration only)
- Time to onset of Pmax change vs turbidity: 40 days (Kbg 0.6 m⁻¹) → 12 days (Kbg 1.2 m⁻¹) → 7 days (Kbg 1.8 m⁻¹) — verbatim-confirmed
- Pmax-reversal delay under high vs low turbidity: factor of 2.5 — verbatim-confirmed
- Bloom-formation timescale range across all scenarios: 26 to >180 days
- Moderate-bloom timescale under optimal (low turbulence/low turbidity) conditions: 26–27 days across all 6 populations
- Cell density, Population I vs Population VI: up to 2.5× higher (single-pass corroboration only)
- Total cell density decrease under high (1.8 m⁻¹) vs low (0.6 m⁻¹) turbidity at high turbulence: up to 55% (single-pass corroboration only)

## Methods
Coupled 1-D hydrodynamic + trait-based ecological model, implemented in MATLAB 2022b, governed by an extended Langevin–Fokker–Planck equation (vertical distribution dynamics), a classic photosynthesis–irradiance (P–I) relationship, Stokes' law (colony vertical migration velocity as a function of cell-tissue density and colony size), and Lambert–Beer's law (light attenuation with self-shading from population biomass). Model has three coupled components: (i) 1-D hydrodynamic (turbulent mixing) model, (ii) ensemble-averaged transport model for trait-specific cell density/colony size/cell-tissue density, and (iii) ecological model of photosynthesis, growth, and loss. Six idealized Microcystis populations (I–VI) were constructed, each discretized into 10 evenly spaced Pmax trait groups (g1–g10); simulations were run for every combination of population × 7 turbulence regimes (diel-periodic, nighttime constant at 10⁻⁶ m² s⁻¹, daytime varied from 5×10⁻⁶ to 1×10⁻³ m² s⁻¹ plus a complete-mixing case) × 3 turbidity levels (Kbg = 0.6/1.2/1.8 m⁻¹) = 126 simulations, each run for 180 days with adaptive time-stepping (1.2–120 s). Initial conditions (uniform vertical trait distribution, 50 μm colony size, neutral buoyancy) were set to represent the early bloom phase of Lake Taihu (~April), since natural trait distributions are unknown. No nutrient limitation or water-temperature dynamics were included; forcing was an idealized, repeating diel light/dark and turbulence cycle rather than real synoptic/seasonal weather. The source reports the model reproduces plausible-order-of-magnitude bloom and scum cell densities and the qualitative turbulence/turbidity-dependent trait-selection and bloom-timing patterns described in the key claims; it states the model does not capture temperature effects, nutrient limitation, cell adhesion/colony disaggregation, other traits (toxigenicity, variable optimal light intensity), or more complex/variable atmospheric forcing. Scripts and datasets are archived at the Knowledge Network for Biocomplexity (KNB) repository (doi:10.5063/F1V986J0); funded by the German Research Foundation (grant LO 1150/18) and the National Natural Science Foundation of China (grant 42061134013).

## Stated limitations
The authors explicitly state the model (1) assumes Microcystis growth depends solely on irradiance, disregarding temporally/vertically varying water temperature and nutrient limitation; (2) fixes Pmax (and the initial slope S and optimal light intensity Iopt) per trait group with no phenotypic plasticity in response to environment; (3) neglects cell adhesion, even though colonies formed via adhesion are more readily disaggregated; (4) varies only one trait (Pmax), not others such as toxigenicity or variable optimal light intensity; (5) is limited to a narrow range of idealized environmental conditions representing a period of relatively stable water conditions with no significant nutrient limitation, using an idealized repeating diel forcing rather than real variable atmospheric/seasonal forcing; and (6) had to assume an unknown natural trait distribution, using a uniform initial distribution as a simplification because obtaining real initial trait-composition data would require substantial field sampling. Verbatim: "Our model did not account for all the processes that may directly or indirectly influence the dynamics of cyanobacterial populations due to the partially unclear mechanisms involved." The authors recommend future work incorporate nutrient limitation, more sophisticated (e.g., variable atmospheric forcing) hydrodynamics, and additional trait variation.

## Tensions with other findings
The paper explicitly frames itself against prior HAB literature that treats a cyanobacterial population's traits (growth rate, mortality, Pmax) as spatiotemporally fixed and representative of the whole population — abstract: most previous studies "considered specific properties of cyanobacterial cells as representative for the entire population... and assumed that they remained spatiotemporally unchanged." This is a direct, source-stated complication for any simpler bulk/homogeneous-population HAB model. Separately, this is a purely idealized, mechanistic numerical-simulation study with no field validation, no observed time-series fitting, and no statistical uncertainty quantification (no confidence intervals, replicate runs, or significance tests are reported in the extracted text) — its physical drivers (small-scale turbulent mixing, background turbidity) differ from the nutrient/temperature/satellite-reflectance drivers typically used in field-data-driven or remote-sensing HAB forecasting, so its mechanism cannot be directly transferred to an empirical or satellite-based model without independent field validation. Its proposed management lever (moderate artificial mixing to suppress trait diversity and bloom resilience) is explicitly a model-derived hypothesis rather than a tested field intervention, which the source itself does not reconcile against any observed mixing/aeration management outcomes.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Claim 5: The source text does not explicitly state which environmental conditions (low turbulence, low turbidity) produce the 26–27 day convergence window; the claim infers this rather than citing it.
- **Reviewer notes:** All numerical claims (99.9% g1 dominance, ~8% other-trait diversity, 40/12/7 day timings, 2.5× reversal delay, 26–>180 day bloom range, 26–27 day convergence, 6×10×7×3=126 simulations) are present and accurate in the source text. No numbers are hallucinated. Seven of eight claims are directly supported by verbatim source quotes. Claim 5 is partial because while the timescale data is confirmed, the specific condition attribution (low turbulence, low turbidity producing the 26–27 day window) is an interpretation by the claim-maker and not explicitly stated in the provided source excerpt. The model limitations (irradiance-only growth, fixed Pmax, no temperature/nutrient/adhesion effects, no toxigenicity/Iopt variation) are all enumerated in OUP-extracted limitation detail. The management hypothesis (artificial mixing) is correctly framed as model-derived, not field-tested."

## Provenance
- Canonical URL: https://academic.oup.com/ismej/article/18/1/wrae021/7597770 (cross-checked against full-text mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC10945370/)
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary OUP URL twice with different extraction prompts as required for a High-relevance source (one pass focused on comprehensive findings/numbers, one on citation metadata + exhaustive quantitative results/methods/limitations). Both passes agreed closely on nearly all figures. Because the ISME Journal is fully open access, both passes returned full-text-level detail (methods, equations, results, discussion, limitations, funding, data availability) rather than just an abstract. To raise confidence given the 'do not let the fetch paraphrase numbers' instruction, I ran a WebSearch that surfaced a PMC full-text mirror (PMC10945370) and did a third WebFetch pass against it requesting exact verbatim sentences for every key number/claim; this third pass supplied true verbatim quotes (not paraphrases) for the core findings (turbulence selection, scum-formation diversity effect, turbidity timing figures, bloom-timescale range, model structure/simulation counts, management implication, and stated limitations), which I used preferentially in key_claims quotes. A handful of granular figures (the 'day 90' timing detail for g1 dominance, the 2.5x Population I vs VI cell-density comparison, the 55% cell-density reduction under high turbidity, and the secondary comparison-lake list — Kasumigaura, Dianchi, Nakdong River, Central Park Lake, Prospect Park Lake) appeared in only one of the three extraction passes each; I retained them (flagged as single-pass) rather than silently dropping data, but they carry lower corroboration confidence than the multiply-confirmed figures. No confidence intervals, error bars, replicate-run variance, or p-values were surfaced in any pass — this is a deterministic idealized simulation study, and the source itself reports no statistical uncertainty on its numbers. Category was reassessed and left as basic-science (mechanistic/ecological insight into what drives bloom formation) rather than models-and-methods, since the paper's contribution is scientific understanding of trait-selection mechanisms rather than an operational forecasting tool; relevance confirmed High given its direct bearing on bloom-formation timing/drivers, though note its physical drivers (turbulence, turbidity) and idealized simulation design are mechanistically distinct from the empirical/satellite/in-situ data streams likely used elsewhere in this HAB PoC.
