---
key: ACAD-006
title: A validation of satellite derived cyanobacteria detections with state reported events and recreation advisories across U.S. lakes
authors_or_org: Peter Whitman, Blake Schaeffer, Wilson Salls, Megan Coffer, Sachidananda Mishra, Bridget Seegers, Keith Loftin, Richard Stumpf, P. Jeremy Werdell
year: 2022
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC9677179/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (PMC full-text / author manuscript)
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# A validation of satellite derived cyanobacteria detections with state reported events and recreation advisories across U.S. lakes

**What it is.** A peer-reviewed validation study (Harmful Algae, 2022;115:102191) that tests how well the satellite-derived Cyanobacteria Index (CIcyano, computed from MERIS/OLCI imagery, the algorithm underlying EPA CyAN) agrees with two independent, publicly reported ground-truth datasets — 1,343 state-reported cyanoHAB events and 160 state recreation advisories — across lakes in the conterminous United States, 2008–2019.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** CIcyano satellite bloom detections agreed with state recreation advisories at a 69% true positive rate and with state-reported cyanoHAB events at a 60% true positive rate.
  - *evidence:* Primary headline validation metric, stated in the abstract and derived in Results from a presence/absence confusion-matrix comparison of CIcyano composites against advisory periods and event dates. (Abstract; Results)
  - *quote:* "The true positive rate of agreement with state recreation advisories was 69% and 60% with state reported events."
- **[✓ verified]** CIcyano showed a reduction or absence of cyanobacteria after 76% of state recreation advisories were lifted (the study's true negative rate).
  - *evidence:* Reported in abstract and results, computed as 102 of 134 advisories showing absence/reduction in the composite following the advisory's end date. (Abstract; Results – State Recreation Advisories)
  - *quote:* "CIcyano detected a reduction or absence in cyanobacteria after 76% of the recreation advisories ended."
- **[✓ verified]** Overall recreation-advisory validation performance, beyond TPR/TNR, was: positive predictive value 77%, negative predictive value 68%, overall agreement 73%, and F1 score 0.73.
  - *evidence:* Reported as computed confusion-matrix summary metrics for the 154 analyzed advisories; consistently returned by two independent extractions of the Results section. (Results – State Recreation Advisories)
- **[✓ verified]** The authors present this as the first study to quantitatively evaluate a satellite cyanoHAB algorithm's performance against independent, publicly available state-reported events and recreation advisories nationwide.
  - *evidence:* Stated framing of the paper's novelty/contribution in the abstract and conclusion. (Abstract; Conclusion)
  - *quote:* "This is the first study to quantitatively evaluate satellite algorithm performance for detecting cyanoHABs with state reported events and advisories."
- **[✓ verified]** During state recreation-advisory periods, satellite-derived cyanoHAB magnitude, spatial extent, and temporal frequency were all statistically greater than during non-advisory periods, with effect sizes ranging from small to large.
  - *evidence:* Abstract summary of the paired Wilcoxon signed-rank comparisons detailed in the results table. (Abstract; Table 2)
  - *quote:* "each of these three metrics were greater (r > 0.2) during state recreation advisories compared to non-advisory times with effect sizes ranging from small to large."
- **[✓ verified]** Of the three CIcyano metrics, spatial extent showed the largest advisory-vs-non-advisory effect size (full-year r=0.71; recreation-season r=0.60), followed by magnitude (r=0.38 / r=0.36) and temporal frequency (r=0.24 / r=0.29), each via paired Wilcoxon signed-rank tests with p<0.05 in all six comparisons.
  - *evidence:* Numeric Table 2 results (Wilcoxon W, z, p, and effect size r for each metric, full-year and recreation-season subsets) were returned identically by two independently-prompted fetches of the article, which is strong internal cross-check evidence they reflect the source table rather than a fetch artifact. (Table 2 (Wilcoxon signed-rank test results))
- **[✓ verified]** Agreement between satellite detection and state reports differed sharply by how the state classified the underlying observation: 69% agreement for the 651 events flagged with cyanotoxin detections vs. only 42% agreement for the 379 events flagged simply as 'cyanobacteria' (no toxin/illness co-report); the authors suggest part of this gap reflects state reports of non-cyanobacterial bloom taxa being mislabeled as cyanobacteria.
  - *evidence:* Category breakdown (651+379+93+2=1,125) is internally consistent with the total analyzed event count, supporting its accuracy; the misidentification explanation is the authors' interpretation of the low 42% figure. (Results – State Reported Events; Discussion)
  - *quote:* "many of these state reported events were actually reports of other harmful algal bloom taxa...rather than cyanobacteria"
- **[✓ verified]** A threshold-sensitivity analysis (Table 1) shows the headline TPRs are threshold-dependent: loosening the spatial-extent requirement to a single pixel raises TPR to 77% (events) / 80% (advisories), while raising the magnitude threshold from ≥0.0001 to ≥0.001 drops TPR to 39–40% (events) / 53% (advisories) regardless of the spatial-extent cutoff used.
  - *evidence:* Full table transcribed identically (all 8 rows, both TPR columns) by two separate targeted fetches, and its central row (10% extent, ≥0.0001 magnitude) exactly reproduces the paper's own headline 60%/69% TPR figures — a strong internal consistency check. (Table 1)
  - *quote:* "The true positive rate between CIcyano and state recreation events and recreation advisories given different combinations of bloom spatial extent and bloom magnitude thresholds."
- **[✓ verified]** Roughly 80% of state-reported cyanoHAB records nationally had to be discarded from the analysis because they occurred in waterbodies too small to contain at least three 300-m satellite pixels.
  - *evidence:* Stated directly as a data-availability limitation explaining the gap between all state records and the subset analyzable with CIcyano. (Discussion (limitations))
  - *quote:* "∼80% of the state records had to be discarded from this study because they occurred in lakes and waterbodies that were not of sufficient size or shape to accommodate at least three, 300-m pixels."
- **[✓ verified]** The authors identify a diel-timing mismatch as a source of disagreement: cyanobacteria vertically migrate/regulate buoyancy on a daily cycle, so satellite overpasses (near solar noon) may not align with when/where field crews sample (often morning).
  - *evidence:* Stated as a methodological limitation affecting comparability between satellite and field/state observations. (Discussion (limitations))
  - *quote:* "Cyanobacteria follow diel cycling, which results in metabolic alterations that lead to buoyancy regulation."
- **[✓ verified]** A land-water-interface/shoreline resolution limitation is stated: many state observations are made at lake shorelines where wind concentrates cyanobacteria, but 300-m satellite pixels cannot resolve conditions at that scale, which the authors say is a particularly prevalent limitation for this study's comparisons.
  - *evidence:* Explicit stated limitation connecting satellite spatial resolution to where the reference (state) observations were actually made. (Discussion (limitations))
  - *quote:* "a particularly prevalent limitation in this study because many cyanoHAB state reported events and state recreation advisories were most likely predicated on samples or observations made at the shoreline of a lake where people recreate."
- **[✓ verified]** State cyanoHAB monitoring itself is described as opportunistic/event-triggered rather than systematic, which the authors say likely overweights the reference dataset toward bloom-presence periods and underweights bloom-absence periods, and is seasonally skewed toward the recreation season.
  - *evidence:* Stated as a limitation of the reference (ground-truth) data quality/representativeness, distinct from any satellite algorithm error. (Discussion (limitations))
  - *quote:* "sampling was likely overweighted toward cyanoHAB presence and underweighted during times of minimal or no cyanoHABs."
- **[✓ verified]** Thresholds and criteria that individual states use to issue or lift a recreation advisory are inconsistent across states and change over time, so the study could not assume one common numeric action threshold applied nationally.
  - *evidence:* Stated methodological caveat about heterogeneity in the state advisory reference data. (Discussion (limitations) / Methods)
  - *quote:* "Thresholds and decision criteria to end recreation advisories vary across states and develop over time."
- **[✓ verified]** The study area/data spanned CONUS 2008–2019 using two satellite sensors in sequence (MERIS 2008–2012, OLCI 2016–2019, both 300-m pixels), with 1,343 state-reported events (2008–2018, NRDC database) in 210 lakes across 26 states, and 160 recreation advisories (2008–2019, EPA cyanoHAB newsletters) in 87 lakes across 11 states, out of 2,321 total satellite-resolvable CONUS lakes.
  - *evidence:* Study-area/data-source description, corroborated consistently across three independent fetch passes (counts of lakes, states, events, advisories, sensors, and date ranges all matched). (Methods (Data and Study Area); Results)
  - *quote:* "The state recreation advisories that coincided with CIcyano occurred in 87 lakes across 11 states"

## Data / numbers
- 1,343 state reported cyanoHAB events compiled (2008–2018, from the NRDC database)
- 1,125 events retained for analysis after excluding 218 for QA/insufficient-imagery flags
- 160 state recreation advisories compiled (2008–2019, from EPA monthly cyanoHAB newsletters)
- 154 advisories retained for analysis after excluding 6 for insufficient data
- 2,321 satellite-resolvable lakes analyzed across the conterminous U.S. (CONUS)
- 210 lakes contained state reported events, spanning 26 states
- 87 lakes contained recreation advisories, spanning 11 states
- Top event states: Iowa 601, Vermont 139, North Carolina 101, Ohio 67, California 59
- Top advisory states: California 60, New York 39, Kansas 15, Ohio 11, Wyoming 10, Oregon 10
- 1,247 of 1,343 events (~93%) occurred May–October
- Median recreation-advisory duration: 42 days (range: 1 day to >1 year)
- State reported events True Positive Rate: 60% (674 of 1,125 presence-presence; 451 of 1,125 misfit absence)
- Cyanotoxin-labeled events (n=651): 69% agreement with CIcyano bloom presence
- Cyanobacteria-labeled events (n=379): 42% agreement with CIcyano bloom presence
- Combined cyanobacteria+cyanotoxin events: n=93; Illness-labeled events: n=2 (651+379+93+2 = 1,125, internally consistent with total analyzed)
- Recreation advisories True Positive Rate: 69% (107 of 154)
- Recreation advisories True Negative Rate: 76% (102 of 134)
- Positive Predictive Value: 77%; Negative Predictive Value: 68%; Overall Agreement: 73%; F1 score: 0.73
- Table 1 sensitivity grid, TPR (events / advisories) by spatial-extent & magnitude threshold: 1 pixel & ≥0.0001 → 77%/80%; 10% & ≥0.0001 (study's chosen threshold) → 60%/69%; 20% & ≥0.0001 → 53%/64%; 30% & ≥0.0001 → 49%/61%; 1 pixel & ≥0.001 → 39%/53%; 10% & ≥0.001 → 39%/53%; 20% & ≥0.001 → 40%/53%; 30% & ≥0.001 → 40%/53%
- Table 2, full year (Jan–Dec), Wilcoxon signed-rank: Magnitude n=86, W=2693, z=3.54, p<0.001, r=0.38 (moderate); Temporal frequency n=86, W=2386, z=2.22, p=0.013, r=0.24 (small); Spatial extent n=61, W=1712, z=5.51, p<0.001, r=0.71 (large)
- Table 2, recreation season (May 1–Oct 31), Wilcoxon signed-rank: Magnitude n=85, W=2583, z=3.31, p<0.001, r=0.36 (moderate); Temporal frequency n=85, W=2442, z=2.69, p=0.004, r=0.29 (small); Spatial extent n=57, W=1396, z=4.52, p<0.001, r=0.60 (large)
- CIcyano bloom-presence classification rule: magnitude ≥ 0.0001 AND spatial extent ≥ 10% of lake area
- Satellite pixel resolution: 300 m; minimum resolvable lake size: ≥3 valid 300-m pixels
- Lake/week excluded from analysis if >90% of its pixels are QA-flagged (e.g., cloud, glint)
- ~80% of all state cyanoHAB records nationally were unusable/discarded (waterbody too small for 300-m pixels)
- Satellite sensor coverage: MERIS 2008–2012; OLCI 2016–2019 (~4-year data gap between missions, Apr 2012–Feb 2016)
- Effect-size classification used (Cohen 1988): small r=0.1–0.3, moderate r=0.3–0.5, large r>0.5; 'substantive difference' set at r>0.3
- Publication: Harmful Algae, 2022 May 12; volume 115, article 102191 (PMC9677179)

## Methods
CIcyano is a spectral-shape algorithm applied to Rayleigh-corrected reflectance from ESA MERIS (2008–2012) and Sentinel-3 OLCI (2016–2019) imagery at 300-m pixel resolution over CONUS lakes; daily imagery is composited into 7-day rolling-maximum composites to smooth day-to-day fluctuation in surface cyanobacteria. A lake-week is classified 'bloom present' when CIcyano magnitude ≥0.0001 and ≥10% of lake-area pixels register a detection (lakes need ≥3 valid 300-m pixels to be resolvable at all; a lake-week is excluded if >90% of pixels are QA-flagged). This satellite output was compared against two independent, non-satellite reference datasets: (a) 1,343 'state reported events' (single-date cyanoHAB observations, 2008–2018, from the NRDC nationwide database) and (b) 160 'state recreation advisories' (start/end-dated warnings tied to each state's own risk threshold, 2008–2019, from EPA's monthly cyanoHAB newsletter). Agreement was scored via a presence/absence confusion matrix (presence-presence, absence-absence, misfit-absence, misfit-presence) yielding true positive rate (TPR), true negative rate (TNR), positive/negative predictive value (PPV/NPV), overall agreement, and F1. Differences in CIcyano magnitude, spatial extent, and temporal frequency between advisory and non-advisory periods were tested with paired Wilcoxon signed-rank tests (effect size r = z/√n, Cohen's small/moderate/large bins), run separately for full-year and May–Oct 'recreation season' subsets; advisory end-date effects were assessed with Mann-Whitney U and rank-biserial r. Per the authors, the method performs best (highest TPR, 77–80%) under loose thresholds (1-pixel extent) and for toxin-flagged events (69% agreement), and performs worst (TPR as low as 39–42%) under a stricter magnitude threshold (≥0.001) and for events merely labeled 'cyanobacteria' without a toxin/illness co-report — gaps the authors attribute to shoreline/land-water-interface resolution limits, diel vertical-migration timing mismatches between satellite overpass and field sampling, cloud/glint obscuration, and possible taxonomic misclassification in the state reports themselves.

## Stated limitations
The authors state several limitations: (1) diel cycling — cyanobacteria vertically migrate/regulate buoyancy daily, so satellite overpasses near solar noon may not coincide with when/where field crews sample (often morning); (2) geolocation imprecision — state-reported coordinates could represent the general lake, a sampling site, or an advisory area, making it impossible to know if an event/advisory applied to a specific portion of a lake; (3) the land-water interface/shoreline problem — many state observations were likely made at shorelines where wind concentrates cyanobacteria, but 300-m pixels cannot resolve conditions there; (4) ~80% of all state records nationally had to be discarded because the waterbody was too small for at least three 300-m pixels; (5) state cyanoHAB monitoring is opportunistic/event-triggered rather than systematic, likely overweighting the reference data toward bloom-presence periods and underweighting bloom-absence periods, and it is seasonally biased toward the recreation season (roughly Memorial Day to Labor Day); (6) recreation-advisory issuance/lifting thresholds vary by state and over time, so no single common numeric action threshold could be assumed; (7) low (42%) agreement for events merely labeled 'cyanobacteria' suggests some state reports may reflect other bloom taxa misidentified as cyanobacteria; (8) CIcyano can miss real cyanoHABs due to algorithmic error, biomass below the detection limit, wind advection/mixing, cloud cover, sun glint, or the land-water interface; and (9) the authors did not further test how the choice of a 7-day compositing window itself affects the results.

## Tensions with other findings
The extracted text does not explicitly compare this paper's findings against other named HAB studies (beyond a general statement that its F1 score falls within the range of prior microcystin-detection validation work), so no direct contradiction is evident from the fetched material. However, the source's own numbers complicate any narrative that satellite remote sensing alone can substitute for in-situ/state monitoring, which matters for a fused remote-sensing + in-situ HAB tool: roughly 40% of state-documented cyanoHAB events (and 58% of events labeled simply 'cyanobacteria') show no coincident CIcyano detection, and ~80% of all state records nationally were unusable because the waterbody was too small for 300-m satellite pixels. This bounds how much weight a decision tool can place on satellite-only signals as a stand-in for ground truth, and suggests satellite and in-situ/state records disagree often enough that neither should be treated as an unqualified gold standard for validating the other — a point directly relevant to, and in tension with, any framing that treats EPA CyAN/CIcyano output as equivalent to confirmed bloom presence.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Algorithm may miss cyanoHAB presence due to biomass below detection limit, wind advection, or mixing (stated as a limitation)
  - Cloud cover and sun glint can prevent CIcyano detection
  - Geolocation ambiguity: impossible to determine if observations occurred in specific lake portions
  - Impact of compositing window length on results was not analyzed
- **Reviewer notes:** All 14 claims are factually supported by the source text. Every numeric value (effect sizes, agreement percentages, lake/state counts, sensor specifications, date ranges) traces exactly to the provided source excerpt. Dropped caveats are substantive methodological limitations mentioned in the source's Discussion but not foregrounded in the claims—they are transparently disclosed by the authors as constraints on generalizability, not contradictions of reported results. Minor note on Claim 14: the specific source attribution 'EPA cyanoHAB newsletters' for advisory data is not mentioned in the provided source excerpt (which refers generically to 'state recreation advisories'), but this does not contradict the claim, and the numeric facts are confirmed."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9677179/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Because this is a High-relevance source, the PMC full-text page was fetched via WebFetch FOUR times (exceeding the required minimum of two) with progressively targeted prompts: (1) a comprehensive findings/methods/limitations extraction, (2) a section-by-section extraction with verbatim quotes, (3) a verbatim-abstract-plus-keyword-quote check to resolve ambiguities (e.g., confirming '87 lakes across 11 states' and exact journal citation), and (4) a targeted re-check of the Table 1 sensitivity grid, since it appeared in only one of the first two passes. All four extractions were mutually consistent on every cross-checked figure (abstract wording, TPR/TNR/PPV/NPV/F1, the full Table 1 grid transcribed identically twice, Table 2 Wilcoxon statistics, lake/event/advisory counts, state lists, and stated limitations), and several counts are internally self-consistent (e.g., the four event categories 651+379+93+2 sum exactly to the reported 1,125 analyzed events; the Table 1 row for the study's chosen threshold reproduces the headline 60%/69% TPRs exactly). This convergence gives good confidence the reported numbers are faithful to the source rather than fetch-tool artifacts. No redirect occurred; the PMC page is a full-text 'published in final edited form' manuscript version (Harmful Algae. 2022 May 12;115:102191), so full_text_access is set to 'full.' Two short fragments returned by the fetch tool contained internal ellipses (the sentence explaining the 42% cyanobacteria-category agreement, and the sentence comparing this study's F1 score to prior microcystin-validation work) — these are flagged explicitly in source_extract as incompletely captured rather than presented as complete original sentences, and the corresponding key_claims are phrased as the paraphrasable substance of those points rather than asserting the omitted wording.
