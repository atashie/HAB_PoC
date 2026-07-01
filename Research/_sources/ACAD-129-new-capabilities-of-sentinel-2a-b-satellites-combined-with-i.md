---
key: ACAD-129
title: New capabilities of Sentinel-2A/B satellites combined with in situ data for monitoring small harmful algal blooms in complex coastal waters
authors_or_org: Caballero, I., Fernández, R., Moreno Escalante, O., Mamán, L., Navarro, G.
year: 2020
url: https://www.nature.com/articles/s41598-020-65600-1
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, Scientific Reports (Nature Publishing Group), open access, Vol. 10, Article 8743, published 26 May 2020, DOI 10.1038/s41598-020-65600-1
categories: [remote-sensing]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# New capabilities of Sentinel-2A/B satellites combined with in situ data for monitoring small harmful algal blooms in complex coastal waters

**What it is.** A single-event case study (Guadiana estuary, SW Iberian Peninsula, Spain-Portugal border, late June-July 2019) that fuses Sentinel-2 MSI (10 m) satellite imagery with weekly in-situ phytoplankton cell counts to map a small, patchy bloom of the toxic dinoflagellate Lingulodinium polyedra, benchmarking Sentinel-2's detection capability against coarser Sentinel-3 OLCI (300 m) and Landsat-8 OLI (30 m) imagery.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Sentinel-2's 10 m spatial resolution allowed detection and mapping of a small, patchy, elongated bloom slick that Sentinel-3's 300 m OLCI resolution could not resolve.
  - *evidence:* Authors directly compare S2 vs S3 imagery of the same bloom event (Figs 4-5) and attribute S3's failure to detect the bloom's thin, elongated patches to its coarser pixel size, restating the same conclusion in the paper's Conclusions section. (Discussion (S2 vs S3 comparison) and Conclusions)
  - *quote:* "This species usually forms very elongated and thin slicks with widths varying from a few to tens of metres, so OCLI's spatial resolution (300 m) is not sufficient to resolve the patchiness. In contrast, S2 was able to accurately detect and map the bloom extension close to the coast thanks to its 10 m spatial resolution."
- **[✓ verified]** Bloom presence/extent was mapped using a red-edge-based Normalized Difference Chlorophyll Index (NDCI) computed from ~665 nm and ~708 nm reflectance bands (only possible for Sentinel-2/3), with NDCI values above zero used as the bloom-presence flag; observed NDCI over bloom pixels ranged 0 to 0.7.
  - *evidence:* Methods define the NDCI band inputs and the zero-threshold masking rule used to delineate bloom pixels; Results (Figure 4) report the pixel value range actually observed. (Methods (NDCI/Equation 1) and Results (Figure 4 caption))
  - *quote:* "665 nm (red) and 708 nm (red-edge)"
- **[✓ verified]** At three spot-check points on the 16 July scene, NDCI was 0.62 and 0.38 inside the bloom versus -0.1 outside it, and the ~704 nm red-edge reflectance peak was identified as the most informative band for bloom mapping.
  - *evidence:* A point-by-point spectral comparison (in-bloom vs out-of-bloom) is used to justify why the red-edge band was chosen for the index. (Results/Discussion (Figure 7, 16 July control points))
  - *quote:* "the 704 nm band is suggested as the best option for HABs mapping"
- **[✓ verified]** In-situ phytoplankton counts peaked at 8x10^5 cells/L (monitoring Area 102) during the July 2019 event, far below the up-to-2x10^7 cells/L concentrations the authors cite from the literature for this species elsewhere (Adriatic Sea).
  - *evidence:* Numeric in-situ cell counts from weekly sampling (Figure 2) are reported and contrasted against a literature-cited historical maximum for the species, used only as background context, not as this study's own measurement. (Results (Figure 2, in-situ cell counts) and Introduction (literature comparison))
  - *quote:* "8×10⁵ cells per liter"
- **[✓ verified]** The satellite record shows the bloom first appearing (via Landsat-8) on 30 June 2019, reaching its largest mapped extent on 11 July, and contracting to two confined patches by 16 July.
  - *evidence:* This bloom timeline is built from sequential RGB-composite/NDCI maps across the multi-date Sentinel-2/Landsat-8 image series. (Results (bloom detection timeline))
  - *quote:* "16 July, the bloom was confined to two regions"
- **[✓ verified]** Several Sentinel-2 scenes (4, 6, 9, 14 and 19 July 2019) were degraded by severe sun-glint on the eastern side of the satellite swath and required masking of affected pixels, a data-quality limitation the authors say could be mitigated by preferring western-swath tiles in this region during summer.
  - *evidence:* Stated directly by the authors as an operational/geometric limitation of the S2 acquisitions used, with an explicit recommendation for future monitoring. (Results/Discussion - stated limitation)
  - *quote:* "Some S2 images acquired on 4, 6, 9, 14, and 19 July 2019 were of poor quality after ACOLITE due to extremely severe sun glint effects, so the affected pixels were flagged and masked out."
- **[✓ verified]** Landsat-8 cannot compute the NDCI at all because it lacks red-edge bands (700-720 nm), and its fallback OC3 chlorophyll algorithm is acknowledged to lose accuracy in optically complex coastal waters containing non-covarying CDOM and suspended matter.
  - *evidence:* Presented as a structural sensor limitation distinguishing what Landsat-8 can vs cannot detect relative to Sentinel-2/3. (Discussion (sensor comparison / limitations))
  - *quote:* "Landsat satellites do not have bands in the red-edge spectral range (700–720 nm)"
- **[✓ verified]** The authors conclude ACOLITE-plus-NDCI is a robust way to map this bloom's extent from Sentinel-2 imagery, but explicitly call for validation across more bloom events and note that shellfish yessotoxin levels linked to this species have never been measured in this region.
  - *evidence:* Stated directly in the Conclusions/Discussion, combining a positive methodological claim with self-identified caveats on generalizability and on the (untested) human-health/toxin linkage. (Conclusions; Discussion (limitations))
  - *quote:* "The obtained results confirm the robustness of the ACOLITE atmospheric correction model combined with NDCI for mapping the bloom extension using S2 imagery."

## Data / numbers
- Sentinel-2 MSI spatial resolution: 10 m (bands also at 10-20-60 m depending on band)
- Sentinel-3 OLCI spatial resolution: 300 m
- Landsat-8 OLI spatial resolution: 30 m
- Sentinel-2 revisit time: ~5 days at the equator (twin S2A+S2B constellation), better at higher latitudes
- Sentinel-3 revisit frequency: 1-2 days
- Landsat-8 repeat cycle: 16 days
- Sentinel-2 radiometric resolution: 12 bits
- Sentinel-3 OLCI: 21 bands, 400-1020 nm, 14-bit radiometric resolution, ~1270 km swath width
- Landsat-8: 12-bit radiometric resolution, tile size 170 km x 185 km
- NDCI bands: Rrs at 665 nm (red) and 708 nm (red-edge); bloom-flag threshold NDCI > 0
- Observed NDCI range across bloom pixels: 0 to 0.7 (Figure 4)
- Spot-check NDCI values, 16 July scene: P1 in-bloom = 0.62; P2 in-bloom = 0.38; P3 outside bloom = -0.1 (Figure 7)
- Peak in-situ cell concentration: 8x10^5 cells/L, Area 102, July 2019 (this study's own measurement)
- Literature-cited historical maximum for L. polyedra: up to 2x10^7 cells/L, Adriatic Sea (not this study's data, cited context only)
- First satellite detection of bloom: 30 June 2019 (Landsat-8)
- Maximum mapped bloom extent: 11 July 2019 (Sentinel-2)
- Bloom contraction to two confined regions: 16 July 2019
- 8 Sentinel-2 scenes used, 1-19 July 2019, selected for low cloud cover
- 3 Landsat-8 scenes used
- In-situ sampling: weekly, 4 monitoring areas (101-104), 4-17 July 2019
- S2A launch date: 23 June 2015; S2B launch date: 7 March 2017
- Guadiana River basin population: ~2 million people, ~90% in Spain
- ACOLITE processor version used: 20190326.0

## Methods
Remote-sensing data: Sentinel-2 MSI (10-20-60 m, 12-bit), Sentinel-3 OLCI (300 m, 21 bands 400-1020 nm, 14-bit, ~1270 km swath), and Landsat-8 OLI (30 m, 12-bit, 16-day repeat, 170x185 km tiles) imagery covering 1-19 July 2019 (8 Sentinel-2 scenes, coincident Sentinel-3 OLCI scenes, 3 Landsat-8 scenes). All imagery was atmospherically corrected to bottom-of-atmosphere remote-sensing reflectance (Rrs) using the ACOLITE Dark Spectrum Fitting processor (version 20190326.0) with optional sun-glint correction. Bloom presence/extent was mapped with the red-edge Normalized Difference Chlorophyll Index (NDCI, from ~665 nm and ~708 nm reflectance), computable only for Sentinel-2/3 because Landsat-8 lacks red-edge bands; Landsat-8 instead used the OC3 ocean-color chlorophyll algorithm as a proxy. In-situ validation: weekly integrated water-column sampling (interconnected hoses) plus vertical net tows (20 micron bongo-type net) at 4 stations (Areas 101-104) in the Guadiana estuary, 4-17 July 2019, with Lingulodinium polyedra cells counted by inverted Utermohl microscopy under the EN 15204 standard at an ENAC-accredited (ISO 17025) laboratory. The paper reports the ACOLITE+NDCI approach "seemed to perform correctly for both satellites" and that Sentinel-2's 10 m resolution succeeded in resolving the bloom's thin, patchy structure where Sentinel-3's 300 m resolution and Landsat-8's lack of red-edge bands could not; standard OC3 chlorophyll retrieval is stated to fail in this optically complex coastal water.

## Stated limitations
The authors themselves flag: (1) severe sun-glint contamination on several Sentinel-2 scenes (4, 6, 9, 14, 19 July 2019), concentrated on the eastern side of the satellite swath, requiring pixel masking, with a recommendation to prefer western-swath tiles in this region during summer; (2) Sentinel-2 was designed primarily for vegetation/land applications, so atmospheric correction for water-quality use needs further validation - they explicitly call for "a more exhaustive evaluation of the ACOLITE method, usually with in situ radiance measurements... for a more comprehensive comparison"; (3) Landsat-8 cannot compute NDCI at all (no red-edge bands 700-720 nm), and the OC3 fallback used for Landsat-8 is acknowledged to lose accuracy in optically complex coastal waters with non-covarying CDOM/suspended matter; (4) the analysis covers a single bloom event, and the authors call for "gathering field data covering a higher number of algal bloom scenarios" before generalizing further; (5) a health-risk/toxin data gap - yessotoxin levels in shellfish linked to this species "have never been measured in the Gulf of Cadiz region."

## Tensions with other findings
This is a marine/estuarine dinoflagellate (Lingulodinium polyedra) case, not a freshwater cyanobacterial bloom, so its NDCI thresholds and ACOLITE settings are not validated by this study for the freshwater cyanoHAB context (e.g., EPA CyAN's Sentinel-3-based cyanobacteria index) that is this project's focus - any transfer is methodological/analogical, not a direct application. More substantively, the paper's central finding - that a 300 m sensor (Sentinel-3 OLCI) and coarser sensors generally can entirely miss small, thin, patchy blooms that 10 m Sentinel-2 imagery resolves - is a direct caution against over-trusting coarser-resolution operational products (such as the ~300 m OLCI imagery underlying much of EPA CyAN) for water bodies with small or narrow bloom features; it bounds rather than contradicts CyAN-style monitoring. The paper also treats the red-edge reflectance shift as an optical/spectral correlate of phytoplankton concentration rather than a causally validated, chlorophyll-a-calibrated retrieval - the in-situ ground truth used is cell counts, not measured chlorophyll-a - so any driver language about reflectance "indicating" bloom concentration should be read as a correlational optical index, not a calibrated causal retrieval.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Claim 8: The source calls for 'a more exhaustive evaluation of the ACOLITE method, usually with in situ radiance measurements' in addition to validation across more bloom events, but the claim omits this ACOLITE-specific methodological caveat.
- **Reviewer notes:** All eight claims are factually supported by the source text with accurate numeric details, proper attribution of literature vs. this study's data, and correctly identified data sources and methods. No hallucinated numbers detected. One minor caveat is present in the source (need for in situ radiance measurements in ACOLITE validation) that is omitted from Claim 8, but this does not contradict or undermine the claim—it is simply an additional methodological consideration mentioned separately in the Discussion section."

## Provenance
- Canonical URL: https://www.nature.com/articles/s41598-020-65600-1
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: The first WebFetch to the canonical Nature URL (https://www.nature.com/articles/s41598-020-65600-1) triggered a Nature IDP cookie/login redirect chain (idp.nature.com/authorize -> idp.nature.com/transit -> back to the article URL with a "?error=cookies_not_supported&code=..." query string appended). Following the WebFetch tool's own redirect instructions, the final call (to that same article URL with the cookie-error query string) returned full article content: complete verbatim abstract, and a detailed numeric breakdown of methods/results/discussion/conclusions plus publication metadata (Sci Rep vol. 10, article 8743, published 26 May 2020) - i.e., the login-wall redirect was a false alarm, consistent with this being an open-access Scientific Reports article rather than a genuine paywall. Cross-checked authorship, year, and DOI independently via WebSearch (Mendeley and SciSpace listings for this title agree: Caballero, I., Fernandez, R., Moreno Escalante, O., Maman, L., Navarro, G., 2020, DOI 10.1038/s41598-020-65600-1), which matched the WebFetch-extracted author list, increasing confidence the fetched content reflects the genuine article rather than a hallucination. No PDF was involved; all quotes above come from the WebFetch tool's HTML-to-text extraction of the live, open-access article page. One internal inconsistency in the source material itself (or in the fetch's rendering of it) should be flagged for a reviewer: the red-edge band used for NDCI is referred to as both "708 nm" (in the NDCI equation/Methods description) and "704 nm" (in the Introduction's list of S2 red-edge bands and in the Discussion's band-selection rationale) - both figures are reported here as given rather than reconciled, since Sentinel-2's actual red-edge band center is ~705 nm and the original NDCI formulation (Mishra & Mishra 2012) was defined for a MERIS band centered near 708 nm.
