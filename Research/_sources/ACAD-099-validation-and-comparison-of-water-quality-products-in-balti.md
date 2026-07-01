---
key: ACAD-099
title: Validation and Comparison of Water Quality Products in Baltic Lakes Using Sentinel-2 MSI and Sentinel-3 OLCI Data
authors_or_org: Tuuli Soomets, Kristi Uudeberg, Dainis Jakovels, Agris Brauns, Matiss Zagars, Tiit Kutser
year: 2020
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC7038399/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed open-access journal article, Sensors (MDPI), full text hosted on PubMed Central (PMC)
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Validation and Comparison of Water Quality Products in Baltic Lakes Using Sentinel-2 MSI and Sentinel-3 OLCI Data

> Note: provisional URL was resolved to a primary source. Original: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7038399/

**What it is.** A 2020 peer-reviewed validation study (Sensors, MDPI) that compares water-quality products (chlorophyll-a, total suspended matter, CDOM absorption, Secchi-depth transparency) retrieved from Sentinel-2 MSI and Sentinel-3 OLCI satellite imagery against a shared in-situ reference dataset from four lakes in Latvia and Estonia sampled across 2018, testing many candidate retrieval algorithms and two atmospheric-correction processors (C2RCC, C2X) organized by optical water type (OWT).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study validates Sentinel-2 MSI and Sentinel-3 OLCI water-quality products against a shared in-situ reference dataset from four lakes in Latvia and Estonia, sampled across 2018.
  - *evidence:* Stated as the study's core design in the abstract. (Abstract)
  - *quote:* "in-situ data from 49 sampling points across four different lakes, collected during 2018"
- **[✓ verified]** Across the water-quality products evaluated, Sentinel-2 MSI matchups agreed with in-situ measurements better than Sentinel-3 OLCI matchups did.
  - *evidence:* Reported as the study's headline result, with an overall R2 range for MSI given across products. (Abstract / Results summary)
  - *quote:* "MSI always outperformed OLCI, with R² 0.84–0.97 for different water quality products"
- **[✓ verified]** Chlorophyll-a retrieval: MSI achieved R2=0.84 and RMSE=10.5 mg/m3 (n=41 matchups); OLCI achieved R2=0.83 and RMSE=9.8 mg/m3 (n=79 matchups).
  - *evidence:* Overall sensor-level Chl-a validation statistics extracted from the results section/table. (Results - Chl-a validation)
  - *quote:* "R² = 0.84; RMSE = 10.5 mg/m³ (n=41)"
- **[✓ verified]** Chlorophyll-a retrieval was least accurate for OLCI in Clear (oligotrophic-type) water (R2=0.34) and most accurate for both sensors in Brown (humic-rich) water (MSI R2=0.90; OLCI R2=0.96).
  - *evidence:* From the per-optical-water-type breakdown of Chl-a validation statistics. (Results - Chl-a by optical water type)
  - *quote:* "Clear OWT: R² = 0.34, RMSE = 4.74"
- **[✓ verified]** Total suspended matter (TSM) retrieval was more accurate for MSI (R2=0.89, RMSE=3.4 mg/L) than OLCI (R2=0.81) overall.
  - *evidence:* Overall sensor-level TSM validation statistics. (Results - TSM validation)
  - *quote:* "R² = 0.89; RMSE = 3.4 mg/L"
- **[✓ verified]** CDOM absorption at 400 nm was better retrieved by MSI (R2=0.91) than OLCI (R2=0.76) overall.
  - *evidence:* Overall sensor-level CDOM validation statistics. (Results - CDOM validation)
  - *quote:* "R² = 0.91"
- **[✓ verified]** Secchi depth (water transparency) showed the largest MSI-OLCI gap of the four products: MSI R2=0.97, RMSE=0.36 m versus OLCI R2=0.69, RMSE=1.1 m.
  - *evidence:* Overall sensor-level Secchi depth validation statistics. (Results - Secchi depth validation)
  - *quote:* "R² = 0.97; RMSE = 0.36 m"
- **[✓ verified]** Optical water type (OWT) classification accuracy differed by processor: MSI with the C2X processor reached 72% accuracy (R2=0.81, n=32); MSI with C2RCC reached only 50% (R2=0.5); OLCI with C2RCC reached 65% (R2=0.49, n=60).
  - *evidence:* Reported directly as OWT-classification accuracy/R2 statistics per processor/sensor combination. (Results - OWT classification accuracy)
  - *quote:* "accuracy 72%, R² = 0.81, and n = 32"
- **[✓ verified]** The best-performing retrieval methods overall were band-ratio algorithms applied with optical-water-type guidance, for both sensors.
  - *evidence:* Stated as a general conclusion after comparing many candidate algorithms per product/sensor. (Discussion/Conclusion)
  - *quote:* "In most cases, the band ratio algorithms for both sensors with optical water type guidance gave the best results"
- **[✓ verified]** The C2RCC atmospheric-correction processor (used for both sensors) tended to underestimate in-situ reflectance, while the C2X processor (available only for MSI) reproduced realistic spectral shape and magnitude even in clear water.
  - *evidence:* Comparison of retrieved vs. in-situ reflectance spectra by processor. (Results/Discussion - reflectance spectra comparison)
  - *quote:* "MSI and OLCI C2RCC reflectance spectra mostly underestimated the in-situ reflectances, but MSI C2X were able to retrieve similar spectral shapes."
- **[✓ verified]** OLCI's 300 m spatial resolution is stated to restrict its practical water-quality-monitoring use to roughly the 1000 largest lakes on Earth.
  - *evidence:* Given as a stated limitation of OLCI for broader lake-monitoring applicability. (Discussion - limitations)
  - *quote:* "about 1000 of the largest lakes on Earth"
- **[✓ verified]** The authors identify the Clear (low-concentration, oligotrophic-type) water class as the hardest optical water type for OLCI to retrieve Chl-a, TSM, and especially Secchi depth accurately.
  - *evidence:* Explicit statement of where the retrieval most struggled. (Discussion - limitations)
  - *quote:* "The most challenging part of this study proved to be obtaining the Chl-a, TSM, and especially, SD for the Clear OWT from OLCI data"
- **[✓ verified]** The four study lakes span a trophic gradient, from oligotrophic Razna (57.6 km2, median Secchi depth 5.5 m) to the eutrophic Lubans (25-100 km2, 0.9 m), Burtnieks (40.2 km2, 1.0 m), and Vortsjarv (270 km2, 0.6 m).
  - *evidence:* From a study-area characteristics table (lake area, trophic status, median Secchi depth) as reconstructed by the fetch from the paper's table; not a prose sentence, so treated as table data rather than a verbatim quote. (Study area / lake-characteristics table)
  - *quote:* "Razna | Latvia | 57.6 | Oligotrophic | 5.5 m"
- **[✓ verified]** The paper's practical recommendation is to use MSI for national/operational lake monitoring, applying optical-water-type guidance before selecting a retrieval algorithm.
  - *evidence:* Stated as the paper's closing practical recommendation. (Conclusion)
  - *quote:* "using MSI for national monitoring with OWT guiding prior application of the algorithms"

## Data / numbers
- 49 in-situ sampling points across 4 lakes (2018)
- 10 field campaigns, April-November 2018
- 41 MSI satellite match-ups (35 distinct sampling points), +/-1-day window
- 79 OLCI satellite match-ups (42 distinct sampling points), +/-1-day window
- Chl-a MSI: R2=0.84, RMSE=10.5 mg/m3, n=41
- Chl-a OLCI: R2=0.83, RMSE=9.8 mg/m3, n=79
- Chl-a MSI by OWT: Clear R2=0.67/RMSE=2.04; Moderate R2=0.72/RMSE=6.15; Turbid R2=0.61/RMSE=9.17; Very Turbid R2=0.73/RMSE=14.33; Brown R2=0.90/RMSE=14.26 (mg/m3)
- Chl-a OLCI by OWT: Clear R2=0.34/RMSE=4.74; Moderate R2=0.72/RMSE=4.85; Turbid R2=0.43/RMSE=13.92; Very Turbid R2=0.77/RMSE=11.21; Brown R2=0.96/RMSE=8.00 (mg/m3)
- TSM MSI: R2=0.89, RMSE=3.4 mg/L (overall)
- TSM OLCI: R2=0.81 (overall; overall RMSE not given in extracted text)
- TSM MSI by OWT: Clear R2=0.60/RMSE=0.34; Moderate R2=0.72/RMSE=2.78; Turbid R2=0.86/RMSE=3.28; Very Turbid R2=0.85/RMSE=4.64; Brown R2=0.87/RMSE=3.41 (mg/L)
- TSM OLCI by OWT: Clear R2=0.21/RMSE=3.07; Moderate R2=0.36/RMSE=4.19; Turbid R2=0.66/RMSE=6.07; Very Turbid R2=0.94/RMSE=3.55; Brown R2=0.78/RMSE=3.53 (mg/L)
- CDOM(400nm) MSI: R2=0.91 (overall)
- CDOM(400nm) OLCI: R2=0.76 (overall)
- CDOM MSI by OWT (m^-1): Clear R2=0.15/RMSE=0.07; Moderate R2=0.91/RMSE=0.10; Turbid R2=0.71/RMSE=0.95; Very Turbid R2=0.73/RMSE=1.28; Brown R2=1.00/RMSE=0.001
- CDOM OLCI by OWT (m^-1): Clear R2=0.70/RMSE=1.50; Moderate R2=0.55/RMSE=0.23; Turbid R2=0.34/RMSE=1.47; Very Turbid R2=0.64/RMSE=1.04; Brown R2=0.51/RMSE=1.41
- Secchi depth MSI: R2=0.97, RMSE=0.36 m (overall)
- Secchi depth OLCI: R2=0.69, RMSE=1.1 m (overall)
- Secchi depth MSI by OWT (m): Clear R2=0.63/RMSE=0.71; Moderate R2=0.97/RMSE=0.03; Turbid R2=0.68/RMSE=0.15; Very Turbid R2=0.78/RMSE=0.14; Brown R2=0.96/RMSE=0.06
- Secchi depth OLCI by OWT (m): Clear R2=0.48/RMSE=1.70; Moderate R2=0.80/RMSE=0.40; Turbid R2=0.67/RMSE=0.65; Very Turbid R2=0.95/RMSE=0.03; Brown R2=0.87/RMSE=0.09
- OWT classification accuracy: MSI C2X 72% (R2=0.81, n=32); MSI C2RCC 50% (R2=0.5); OLCI C2RCC 65% (R2=0.49, n=60)
- OWT 'large difference' rate: MSI C2X 6%; OLCI C2RCC 22% (fetch #1) vs. 'Clear OWT misclassified in 14% of cases' (fetch #2) - discrepancy unresolved
- Sentinel-2 MSI: 13 spectral bands, 10-20 m spatial resolution, ~5-day global revisit
- Sentinel-3 OLCI: 21 spectral bands, 300 m spatial resolution, ~2-day revisit at the equator
- Algorithms screened: MSI 21 Chl-a / 14 TSM / 10 CDOM / 21 SD algorithms; OLCI 16 Chl-a / 9 TSM / 5 CDOM / 12 SD algorithms
- Lake Razna (Latvia): 57.6 km2, oligotrophic, median Secchi depth 5.5 m
- Lake Lubans (Latvia): 25-100 km2 (water-level dependent), eutrophic, median Secchi depth 0.9 m
- Lake Burtnieks (Latvia): 40.2 km2, eutrophic, median Secchi depth 1.0 m
- Lake Vortsjarv (Estonia): 270 km2, eutrophic, median Secchi depth 0.6 m
- In-situ spectrometer: PSR-3500 (Spectral Evolution Inc.), 348-1000 nm range
- Publication: Sensors 2020, 20(3), 742; DOI 10.3390/s20030742; PMID 32013214; PMCID PMC7038399

## Methods
In-situ sampling: 49 sampling points across 4 lakes (Razna, Lubans, Burtnieks in Latvia; Võrtsjärv in Estonia), 10 field campaigns April-November 2018, using a hand-held PSR-3500 field spectrometer (348-1000 nm), Secchi disk transparency, and lab analyses (spectrophotometric Chl-a at 665 nm, gravimetric TSM, CDOM absorption coefficients). Satellite matchups: cloud-free Sentinel-2 MSI (41 matchups/35 points) and Sentinel-3 OLCI (79 matchups/42 points) images within a ±1-day window of field sampling; MSI extracted as a 3x3 pixel average, OLCI as a single pixel. Atmospheric correction via C2RCC and C2X ("Case-2 Regional" / "Case-2 Extreme") processors in SNAP v6.0 (C2X unavailable for OLCI). Retrieval: many candidate algorithms per product (MSI: 21 Chl-a/14 TSM/10 CDOM/21 SD algorithms; OLCI: 16/9/5/12 respectively), selected/guided by classifying each matchup into one of five Optical Water Types (Clear, Moderate, Turbid, Very Turbid, Brown) via spectral correlation and modified spectral-angle similarity. Validation statistics: R² and RMSE against in-situ values, both overall per sensor/product and broken out per OWT class. Where it works best: band-ratio algorithms applied with OWT guidance, for both sensors; MSI paired with the C2X processor, which reproduced realistic reflectance spectral shape and magnitude even in clear water. Where it struggles: OLCI in the Clear (oligotrophic, low-concentration) OWT class, and the C2RCC processor generally, which "mostly underestimated the in-situ reflectances" for both sensors.

## Stated limitations
The paper itself states: (1) atmospheric correction over lakes needs improvement, especially for OLCI C2RCC, because "even a small error can cause significant changes" in retrieved values; (2) OLCI's 300 m spatial resolution restricts practical monitoring applicability to roughly "1000 of the largest lakes on Earth," excluding most smaller water bodies; (3) the Clear/oligotrophic optical water type was "the most challenging part of this study" for OLCI to retrieve Chl-a, TSM, and especially Secchi depth accurately; (4) the C2X processor, identified as the best performer for MSI, is "currently not available for OLCI," which the authors suggest may explain part of the MSI-OLCI performance gap; (5) satellite remote sensing only sees the surface layer, so vertical stratification in small, sharply stratified lakes cannot be resolved this way, unlike in large, well-mixed lakes or seas; (6) a non-trivial share of OWT classifications were flagged as large-difference or misclassified (extracted as either ~6% for MSI C2X vs ~22% for OLCI C2RCC "large OWT difference," or ~14% "OLCI misclassification of Clear OWT" depending on which fetch's phrasing is used - see fetch_notes for the unresolved discrepancy between the two extractions).

## Tensions with other findings
This source is directly relevant to (and complicates) the HAB PoC's plan to fuse a satellite chlorophyll/cyanobacteria signal (e.g., EPA CyAN, which is built on this same Sentinel-3 OLCI heritage/resolution class) with in-situ data: the paper's central, quantified finding is that the coarser-resolution ocean-color sensor (OLCI, 300 m) is measurably and substantially less accurate than the finer-resolution sensor (MSI, 10-20 m) for the same chlorophyll-a/TSM/CDOM/Secchi-depth retrievals, and performs worst specifically in "Clear," low-concentration water - the regime where catching an incipient/early bloom matters most for an early-warning framing. This is evidence-based caution against treating OLCI/CyAN-class chlorophyll retrievals as ground truth at face value in clearer or smaller lakes without local in-situ calibration, and it reinforces the CLAUDE.md principle against overclaiming remote-sensing certainty. It also shows that OWT-guided, locally-selected algorithms clearly outperform a single fixed global algorithm - relevant if the PoC's design uses an off-the-shelf chlorophyll algorithm without regional/optical-water-type tuning. No causal claims are made by the source about drivers of bloom formation; this is purely a sensor/algorithm validation study, not a bloom-driver or treatment study.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - MSI lacks a critical spectral band at the Chl-a absorption peak (665 nm)
  - Atmospheric correction performance should be improved; even small errors cause significant changes in retrieved values
  - Different validation methodologies used (3×3 pixel averaging for MSI vs. single-pixel for OLCI)
  - Clear OWT is inherently challenging due to weak absorption peaks at low concentrations
- **Reviewer notes:** All 14 claims are directly supported by explicit statements or verifiable data in the source text. No hallucinated numbers detected. All cited R², RMSE, sample sizes, lake areas, and Secchi depths match the source exactly. The ranking claim in Claim 7 (Secchi depth as largest MSI-OLCI gap) is verifiable from the complete R² dataset provided in the source. Important technical caveats present in the source regarding MSI spectral limitations, atmospheric correction accuracy, and inherent optical challenges in clear-water retrieval were not carried into the claims—these are design/limitation notes rather than results claims, but worth flagging as context lost in summary form."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7038399/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: The provided URL (www.ncbi.nlm.nih.gov/pmc/articles/PMC7038399/) returned a 301 redirect to the new PMC host (pmc.ncbi.nlm.nih.gov/articles/PMC7038399/); I followed the redirect and re-fetched from that URL twice with two different extraction prompts, per instructions, then reconciled into one union (both fetches independently returned matching title/authors/DOI/journal and largely consistent numbers, giving confidence the full text - not just an abstract - was retrieved). One unresolved discrepancy between the two fetches: fetch #1 reported OLCI C2RCC optical-water-type (OWT) classification had "22%" of cases flagged as "large OWT difference," while fetch #2 characterized a limitation as "OLCI misclassification of Clear OWT in 14% of cases." These may describe different metrics (overall large-difference rate vs. a Clear-class-specific misclassification rate) or one fetch summarized imprecisely; I could not adjudicate this with the tools available (no Read/file access, and a third fetch was not authorized by the task's "fetch twice" instruction), so both figures are reported with the discrepancy flagged rather than resolved. Also note: "Baltic lakes" in the title refers to inland freshwater lakes in the Baltic states (Latvia, Estonia), not the Baltic Sea itself.
