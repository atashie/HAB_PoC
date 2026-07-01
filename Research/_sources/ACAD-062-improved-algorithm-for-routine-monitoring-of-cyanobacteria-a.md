---
key: ACAD-062
title: Improved algorithm for routine monitoring of cyanobacteria and eutrophication in inland and near-coastal waters
authors_or_org: Mark William Matthews (Dept. of Oceanography, University of Cape Town, South Africa); Daniel Odermatt (Brockmann Consult GmbH, Geesthacht, Germany; and Odermatt & Brockmann GmbH, Zurich, Switzerland)
year: 2015
url: https://www.cyanolakes.com/publications/Matthews&Odermatt_2015.pdf
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (short communication); PDF copy hosted on the author/publisher-affiliated site cyanolakes.com; per the paper's own citation block, formally published as Matthews, M.W., & Odermatt, D. (2015), Remote Sensing of Environment, 156, 374–382.
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Improved algorithm for routine monitoring of cyanobacteria and eutrophication in inland and near-coastal waters

**What it is.** A short communication (Matthews &amp; Odermatt, 2015, Remote Sensing of Environment) documenting incremental improvements to the Maximum Peak Height (MPH) satellite algorithm for MERIS/BEAM imagery — refined pixel-flagging that reduces false-positive cyanobacteria detection, a new stray-light/adjacency-effect flag, and an NDVI-based floating-vegetation test — together with an initial multi-lake in-situ validation of MPH chlorophyll-a retrievals.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The MPH algorithm estimates chlorophyll-a and detects cyanobacteria/surface scum/floating vegetation in inland and near-coastal waters by computing the position and height of a reflectance peak among MERIS red-edge bands (681, 709, 753 nm) against a 665–885 nm baseline, using Rayleigh-corrected (not fully aerosol-corrected) reflectance to avoid aerosol-correction error over optically complex water.
  - *evidence:* Stated directly in the algorithm description (Section 1) as the paper's own characterization of how MPH works and why bottom-of-Rayleigh reflectance (BRR) is used instead of a full atmospheric/aerosol correction. (Section 1 (Introduction))
  - *quote:* "the narrow red-edge MERIS bands positioned at 681, 709 and 753 nm and, using the 665 and 885 nm bands as a baseline, computes the position and height of the maximum peak"
- **[✓ verified]** The revised cyanobacteria flag adds a requirement that the newly introduced BAIR (backscatter and absorption induced reflectance) peak exceed 0.002, on top of existing spectral (SICF/SIPAF) conditions, specifically to suppress false-positive cyanobacteria detections that the original 2012 flag produced in clear, oligotrophic water.
  - *evidence:* Given as the paper's core methodological fix, with exact conditional logic, and demonstrated with a before/after Lake Michigan case study (Fig. 4) attributed to residual aerosol/cloud artifacts in the reflectance. (Sections 2 and 3; Fig. 4)
  - *quote:* "If SICFpeak < 0 and SIPFpeak > 0 and BAIRpeak > 0.002, cyano_flag = TRUE."
- **[✓ verified]** The source states that cyanobacteria-specific (phycocyanin) spectral features only become clearly resolvable above roughly chl-a > 20 mg m-3, so cyanobacteria detection from MERIS (or, as stated, any other currently available satellite imagery) is considered infeasible/unlikely at low-to-medium biomass; the improved flag is therefore restricted to eutrophic waters.
  - *evidence:* Justification given for limiting the improved cyano_flag to higher-biomass waters; cites Kutser et al. (2006) and Metsamaa et al. (2006) for the phycocyanin-visibility threshold, and Hu et al. (2012) for MERIS red-band signal-to-noise limits (~200–500 in full-resolution mode) as a compounding constraint. (Section 3)
  - *quote:* "cyanobacteria phycocyanin pigment related features only clearly become visible at high biomass chl-a concentrations greater than ± 20 mg m-3"
- **[✓ verified]** A minimum MPH1 value of 0.02 combined with an NDVI threshold of 0.2 is used to distinguish genuine floating vegetation/cyanobacterial scum (a 753 nm reflectance peak) from a spurious 753 nm peak caused by the adjacency effect (stray light from adjacent land) or, rarely, sun glint.
  - *evidence:* Exact conditional logic given for float_flag vs. adj_flag; rationale is that adjacency- and cloud-affected pixels keep both MPH0 and MPH1 below 0.01, while genuine floating vegetation/scum push MPH1 above 0.02. (Sections 2 and 4)
  - *quote:* "If λRmax,1 = 753 nm and MPH1 ≥ 0.02 and NDVI ≥ 0.2, float_flag = TRUE, adj_flag = FALSE"
- **[✓ verified]** Adjacency effects (stray light scattered from brighter adjacent land pixels into the sensor field of view) can contribute more than 50% of the at-sensor NIR radiance in spatially constrained inland/near-coastal waters, and can be observed many kilometers offshore.
  - *evidence:* Cited from Odermatt et al. (2008) and Santer & Schmechtig (2000) as the physical basis for adding the adj_flag; the paper explicitly distinguishes this from any blurring introduced by geo-rectification or image processing. (Section 4)
  - *quote:* "often contribute more than 50% of the at-sensor radiance"
- **[✓ verified]** MPH chlorophyll-a estimates were matched against several thousand in-situ chl-a measurements from more than 40 lakes worldwide and were found to be more robust than several other algorithms specifically in eutrophic-to-hypertrophic waters.
  - *evidence:* Reported as the outcome of validation runs in the Calvalus processing system over the full MERIS FR archive; the underlying large in-situ dataset is cited only as 'Odermatt and Brockmann, in prep.' (not separately published at time of writing). (Section 5)
  - *quote:* "found to provide more robust chl-a estimates than several other algorithms in eutrophic to hypertrophic waters"
- **[✓ verified]** In a 9-lake matchup comparison, MPH chl-a reached regression coefficients up to R > 0.6, with correlation strength statistically similar to the FLH and MCI spectral indices (MPH best in 4/9 lakes, MCI in 3/9, FLH in 2/9), but MPH's regression slope was far less variable across water types than FLH/MCI, which the authors interpret as MPH being better suited to deriving absolute chl-a concentrations across trophic states.
  - *evidence:* Based on the Fig. 6/7 matchup analysis in Section 5, comparing MPH, FLH and MCI (per Gower & King, 2006) against in-situ chl-a using 9-pixel satellite averages with the pixel-window standard deviation as a rough uncertainty estimate. (Section 5; Figs. 6-7)
  - *quote:* "the regression slopes vary much more widely for the MCI and FLH, confirming that MPH is more suitable for the derivation of absolute concentration values across different trophic ranges and water types"
- **[✓ verified]** Unlike MPH, the FLH and MCI products used as a comparison benchmark are index values only and do not themselves provide quantitative chlorophyll-a concentration estimates, which qualifies the 'comparable correlation' finding.
  - *evidence:* Explicitly noted as a parenthetical caveat by the authors when introducing the FLH/MCI comparison in the validation section. (Section 5)
  - *quote:* "these processors do not provide actual quantitative chl-a estimates, only index values"
- **[✓ verified]** Despite generally stable performance across water types, MPH tends to systematically overestimate chlorophyll-a relative to in-situ measurements, and the authors conclude the MPH coefficients need to be re-trained on a global dataset.
  - *evidence:* Self-reported result from the matchup validation (Fig. 7), framed by the authors as motivation for future work rather than a fully resolved outcome. (Section 5)
  - *quote:* "In general the MPH tends to overestimate with respect to the in situ chl-a concentration"
- **[✓ verified]** Within the algorithm's processing logic, a user-configurable chl-a threshold — typically 350 mg m-3 — is used to raise a 'floating matter' flag once cyanobacteria-attributed chl-a exceeds this level.
  - *evidence:* Given as part of the step-2 conditional processing logic for pixels already classified as cyanobacteria-dominant. (Section 2)
  - *quote:* "a certain user-defined threshold, typically 350 mg m-3, a flag for floating matter is raised"

## Data / numbers
- MERIS bands used by MPH: 620, 664, 681, 709, 753, 885 nm (BEAM band numbers 6–10 and 14)
- Revised cyano_flag threshold: BAIR peak > 0.002 (dimensionless BRR peak-height units)
- Floating vegetation/scum threshold: MPH1 ≥ 0.02; adjacency- or cloud-affected pixels instead show MPH0 and MPH1 < 0.01
- NDVI threshold: ≥ 0.2 → floating vegetation classification; < 0.2 (with MPH1 < 0.02) → adjacency-effect flag
- Floating-matter chl-a flag threshold: typically 350 mg chl-a m-3 (user-configurable)
- Cyanobacteria optical-detectability floor: chl-a > approx. 20 mg m-3 ('±20 mg m-3'), below which phycocyanin features are not clearly resolvable (source cites Kutser et al. 2006; Metsamaa et al. 2006)
- MERIS full-resolution red-band signal-to-noise ratio: approx. 200–500 (source cites Hu et al., 2012)
- Adjacency-effect contribution to at-sensor NIR radiance: >50% in spatially constrained waters (source cites Odermatt et al., 2008)
- In-situ validation set: several thousand in-situ chl-a measurements from >40 lakes worldwide (dataset described only as 'Odermatt and Brockmann, in prep.')
- Matchup protocol: same-day, same-GPS-position pairing; satellite value = mean of 9 pixels around the sampling point; uncertainty = standard deviation of those 9 pixels, described as 'a rough error estimate'
- 9-lake regression comparison: maximum R > 0.6 (from about 40 processing schemes tested); MPH gave the best correlation in 4/9 lakes vs. MCI in 3/9 and FLH in 2/9
- MERIS full-resolution archive processed: 2002–2012
- Planned scale-up: MPH to process MERIS L3 products for 300 lakes worldwide under ESA's Diversity II project; adaptation planned for Sentinel-3 OLCI, stated as 'scheduled for launch in mid-2015'

## Methods
The MPH (Maximum Peak Height) algorithm computes, per pixel, the position and height of a reflectance peak among MERIS red/NIR bands (620/664/681/709/753/885 nm), using bottom-of-Rayleigh reflectance (BRR, via the Idepix processor in BEAM 5) rather than a full aerosol-corrected water-leaving reflectance — explicitly to avoid aerosol-correction error over optically complex inland/coastal waters. From the peak variables it derives chlorophyll-a (via separate equations for eukaryotic algae vs. cyanobacteria-dominant waters, per Matthews et al. 2012) and a set of boolean flags (cyano_flag, float_flag, adj_flag) using conditional thresholds on SICF, SIPAF, the newly added BAIR variable, MPH0/MPH1, and NDVI, yielding four distinguishable cases: normal immersed eukaryotic phytoplankton; submerged/mixed cyanobacterial blooms; floating cyanobacteria scum; and floating aquatic macrophytes. The algorithm is packaged as a BEAM 5 plugin and was run at scale in the Calvalus processing system over the full MERIS full-resolution (FR) archive (2002-2012). Validation used matchup analysis (same-day, same-GPS-position) between satellite estimates (mean of a 9-pixel window) and in-situ chl-a from 9 routinely monitored lake datasets (drawn from a larger, >40-lake in-situ collection), via linear regression, benchmarked against two established spectral index products, FLH and MCI (Gower & King, 2006), computed from the same BRR inputs. The source states the method performs well (comparable-or-better correlation than FLH/MCI, and much more stable regression slopes across trophic/water types, per the Moore et al. 2014 optical water-type classification) in eutrophic-to-hypertrophic waters, but states cyanobacteria detection is not attempted/reliable in low/medium-biomass oligo-mesotrophic waters, and that MPH chl-a values are systematically biased high relative to in-situ measurements.

## Stated limitations
The authors themselves state: (1) cyanobacteria detection is "likely to be either very challenging or infeasible" in low-biomass oligo/mesotrophic waters, and is considered unlikely from MERIS "or any other currently available satellite imagery" at low/medium biomass, so the improved flag is deliberately restricted to eutrophic waters (chl-a > ~20 mg m-3). (2) For pixels flagged with the adjacency effect, "valid chl-a retrievals are still feasible in most cases using the peak height at 681 or 709 nm, however outliers may occur." (3) MPH chl-a estimates "tend to overestimate with respect to the in situ chl-a concentration," and the authors conclude there is a "need for re-training of the MPH algorithm coefficients using a global dataset" — i.e., the coefficients from the smaller dataset in Matthews et al. (2012) are not considered adequately generalized. (4) The large in-situ validation dataset underlying the headline validation claim is cited only as "Odermatt and Brockmann, in prep." — not a separately published, independently checkable dataset at the time of this paper. (5) The paper is explicitly framed as a "short communication" documenting incremental fixes and "initial validation," not a full algorithm redevelopment or exhaustive multi-region validation; some supporting evidence is referenced but not shown ("Similar improvements were found in other oligotrophic lakes (not shown)").

## Tensions with other findings
This source's own findings imply a meaningful floor on satellite-based cyanobacteria detectability: cyanobacteria-specific (phycocyanin) spectral features are stated to become resolvable only above roughly chl-a > 20 mg m-3, and low/medium-biomass detection is called "unlikely" for MERIS "or any other currently available satellite imagery." That complicates any framing (elsewhere in a HAB literature/decision context) that treats optical satellite cyanobacteria products as capable of true early warning ahead of visible bloom development: by this paper's own logic, MERIS/MPH-style detection is better suited to confirming already-substantial (eutrophic-to-hypertrophic) blooms than to catching emerging, low-biomass ones — relevant to, and in tension with, any lead-time/early-warning framing that assumes satellite chlorophyll/cyanobacteria signals alone can flag a bloom before it becomes visible. Separately, the paper's own report that MPH "tends to overestimate" chl-a relative to in-situ measurements is a caution against treating satellite-derived chl-a as a bias-free, drop-in substitute for in-situ chl-a in any downstream model that fuses the two signal types. These are correlational/algorithmic-performance observations reported by the source itself, not causal claims about bloom drivers.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Section 2 caveat: 'For waters where an adj_flag is raised, valid chl-a retrievals are still feasible in most cases using the peak height at 681 or 709 nm, however outliers may occur' — not reflected in Claim 4, though not material to the core assertion
- **Reviewer notes:** All 10 claims are directly supported by the source text. No numeric hallucinations detected; all figures cited in the claims (wavelengths, thresholds, R coefficients, lake/measurement counts, biomass limits, percentages) appear verbatim or are correctly paraphrased from the paper. The claims accurately capture the paper's methodology, validation results, and known limitations. A minor caveat about adjacency-flagged pixels was not emphasized in the claims, but this does not constitute a material omission."

## Provenance
- Canonical URL: https://www.cyanolakes.com/publications/Matthews&Odermatt_2015.pdf
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: No WebFetch or WebSearch was performed. All required bibliographic metadata (authors, year, journal, volume, pages) was already present within the pre-extracted source text's own citation block ("Matthews, M. W., & Odermatt, D. (2015)... Remote Sensing of Environment, 156, 374-382"), so no external lookup was needed under the task's rules. All claims, quotes, and numbers above are drawn exclusively from the pre-extracted text supplied in the task.
