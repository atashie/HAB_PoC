---
key: FED-060
title: HAB Forecasts | US EPA
authors_or_org: U.S. Environmental Protection Agency (EPA), Office of Water — HABs program, produced jointly with references to NOAA (incl. NOAA/NCCOS, NANOOS, SCCOOS partner programs)
year: 2026 (page states "Last updated on April 14, 2026"; underlying cited model publications are Myer et al. 2020 and Schaeffer et al. 2024)
url: https://www.epa.gov/habs/hab-forecasts
access_date: 2026-07-01
tier: FED
source_type: federal portal/index page
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# HAB Forecasts | US EPA

**What it is.** An EPA program web page (part of the EPA HABs "Trends, Monitoring Results & Forecasts" section) that describes the operational HAB forecasting products available for U.S. waters: EPA's own CyAN-satellite-based weekly cyanoHAB probability forecast for the freshwater lakes/reservoirs, plus a directory of NOAA/NCCOS/NANOOS/SCCOOS marine and coastal HAB forecast products for several U.S. coastal regions.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** EPA scientists built a weekly forecast model that predicts the probability of a cyanobacteria-dominated harmful algal bloom (cyanoHAB), using data from the Cyanobacteria Assessment Network (CyAN) satellite-based system, covering over 2,000 of the largest U.S. lakes and reservoirs in the lower 48 states, running seasonally from March/April through November.
  - *evidence:* Directly stated in the 'Freshwater Forecasts' section describing the model's scope, data source, and operating season. (Freshwater Forecasts section)
  - *quote:* "over 2,000 of the largest U.S. lakes and reservoirs across the lower 48 states"
- **[✓ verified]** The freshwater forecast model's stated overall prediction accuracy is 90 percent.
  - *evidence:* Stated as a flat headline figure in the Freshwater Forecasts section; the page gives no validation methodology, dataset, time window, or uncertainty interval behind this number. (Freshwater Forecasts section)
  - *quote:* "overall prediction accuracy of 90 percent"
- **[✓ verified]** The model operationally defines a cyanoHAB bloom as a median lake chlorophyll-a concentration of at least 12 µg/L together with cyanobacteria dominance of the phytoplankton community.
  - *evidence:* Given as the explicit bloom-threshold definition underlying the forecast model. (Freshwater Forecasts section)
  - *quote:* "median lake chlorophyll a ≥12 ug/L with cyanobacteria dominance"
- **[✓ verified]** The forecast output is a probability from 0 to 100% that a given lake/reservoir will experience a cyanobacteria-dominated bloom within the next 7 days.
  - *evidence:* Explicit definition of what the forecast number means, given under an interpretive-guidance subsection. ("Something to remember when interpreting these forecasts" subsection)
  - *quote:* "The value the forecast generates is a probability (or likelihood) from 0 to 100% that the lake or reservoir may experience a cyanobacteria dominated bloom in the next 7 days."
- **[✓ verified]** EPA explicitly states the forecast is meant to support, not substitute for, on-the-ground monitoring.
  - *evidence:* Direct disclaimer sentence framing appropriate use of the tool. ("Something to remember when interpreting these forecasts" subsection)
  - *quote:* "Note that the forecast is not meant to replace regular sampling or observation, but to help inform those monitoring efforts."
- **[✓ verified]** The underlying CyAN satellite data cannot resolve shallow near-shore areas, small embayments, or narrow parts of a lake/reservoir, which limits the forecast's ability to detect localized blooms in those zones.
  - *evidence:* Stated directly as a satellite/sensor limitation in the interpretive-guidance subsection. ("Something to remember when interpreting these forecasts" subsection)
  - *quote:* "The CyAN satellite generally does not resolve ('accurately see') shallow areas along the edge of the lake, small embayments, narrow areas of the lake/reservoir, etc."
- **[✓ verified]** Beyond U.S. freshwater lakes, NOAA and its partners/collaborators separately serve HAB forecasts for several U.S. coastal/marine regions: the Gulf of America and Florida, the Gulf of Maine, the Pacific Northwest, and California, via NCCOS, NANOOS, and SCCOOS partner sites; the Gulf of Maine product is specifically named as an Alexandrium catenella predictive model.
  - *evidence:* Marine Forecasts section lists these regions and links out to partner agency products; the page gives no quantitative accuracy/threshold data for the marine forecasts (unlike the freshwater section). (Marine Forecasts section)
  - *quote:* "Similar to that for Lake Erie, NOAA, its partners, and collaborators serve forecasts for a number of coastal regions including the Gulf of America and Florida, the Gulf of Maine, the Pacific Northwest and California."
- **[✓ verified]** The page cites two underlying peer-reviewed model publications: a 'National Forecasting Model' (Schaeffer et al., 2024) and a 'State Forecasting Model' (Myer et al., 2020), as the scientific basis for the freshwater CyAN-based forecasts.
  - *evidence:* Named and linked as supporting publications for the national- and state-level forecast models respectively; titles/authors as labeled by the EPA page's link text. (Freshwater Forecasts section (linked references))
  - *quote:* "National Forecasting Model Publication – Schaeffer et al. 2024; State Forecasting Model Publication - Myer et al. 2020"

## Data / numbers
- over 2,000 of the largest U.S. lakes and reservoirs across the lower 48 states — freshwater forecast coverage
- 90 percent — stated "overall prediction accuracy" of the freshwater cyanoHAB forecast model (no CI, sample size, or validation period given on this page)
- median lake chlorophyll a ≥12 µg/L with cyanobacteria dominance — the operational bloom definition used by the model
- 0 to 100% — probability scale reported by the weekly forecast
- 7 days — forecast horizon ("in the next 7 days")
- cyanoHAB season: March to November; forecasts "typically generated from the beginning of April through November"
- Page "Last updated on April 14, 2026"

## Methods
Two distinct forecast pipelines are described. (1) Freshwater: EPA scientists built a model that consumes Cyanobacteria Assessment Network (CyAN) satellite-derived cyanobacteria detections and produces a weekly 0-100% probability that each of >2,000 of the largest U.S. lakes/reservoirs (lower 48 states) will have a cyanobacteria-dominated bloom (operationally defined as median lake chlorophyll-a >=12 µg/L with cyanobacteria dominance) in the following 7 days; it runs seasonally (cyanoHAB season March-November; forecasts typically generated from early April through November). The page states the model's overall prediction accuracy as 90 percent, validated against CyAN satellite observations, but this specific page gives no further methodological detail (algorithm type, train/validation split, sample size, confidence interval) — it instead links to two underlying publications: a 'National Forecasting Model' (Schaeffer et al. 2024, ScienceDirect) and a 'State Forecasting Model' (Myer et al. 2020, Frontiers in Environmental Science). (2) Marine/coastal: the page describes, only qualitatively, that NOAA and partner programs (NCCOS, NANOOS, SCCOOS) serve HAB forecasts for the Gulf of America/Florida, Gulf of Maine (Alexandrium catenella predictive models), Pacific Northwest, and California; no thresholds, accuracy statistics, or methodological detail are given for these on this page — it functions as a links-out directory. Where the source says the freshwater approach works: whole-lake weekly probability classification at 90% stated accuracy across >2,000 lakes. Where it says the approach is limited: the CyAN satellite "generally does not resolve ... shallow areas along the edge of the lake, small embayments, narrow areas of the lake/reservoir," so localized near-shore blooms may not register in the lake-level probability.

## Stated limitations
The page itself states: (1) "the forecast is not meant to replace regular sampling or observation, but to help inform those monitoring efforts" — an explicit disclaimer against over-reliance on the forecast in place of ground-truth monitoring; (2) the CyAN satellite "generally does not resolve ('accurately see') shallow areas along the edge of the lake, small embayments, narrow areas of the lake/reservoir, etc." — meaning localized, near-shore, or small-water-body blooms may be missed or under-represented in the reported lake-level probability. No limitations are stated on this page for the marine/coastal forecasts specifically (that section is purely a links-out directory with no discussion of accuracy or caveats).

## Tensions with other findings
The page asserts a headline "90 percent" overall prediction accuracy for the freshwater forecast model but, on this page, gives no validation dataset, time period, sample size, or confidence interval for that figure — it points instead to the underlying Schaeffer et al. (2024) and Myer et al. (2020) papers, so the number cannot be treated as a rigorous, self-contained baseline without pulling that primary literature. There is also an internal tension between the confidently stated 90% accuracy and the source's own admission that the CyAN satellite cannot resolve shallow edge areas, small embayments, or narrow lake sections: the accuracy figure likely reflects whole-lake/reservoir classification performance, while a documented category of near-shore blooms (often where recreational exposure and drinking-water intakes concentrate) sits in a stated blind spot. For the HAB_PoC project specifically, this both supports and complicates use of CyAN-derived lake-level probabilities as a benchmark: it gives a usable external accuracy figure and an operational bloom-threshold definition (chlorophyll-a >=12 µg/L with cyanobacteria dominance), but any product claim built on CyAN data should explicitly flag the same near-shore/shallow-water coverage gap this EPA page flags for itself.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Source distinguishes 'cyanoHAB season from March to November' but notes 'forecasting data are typically generated from the beginning of April through November'—claim condenses this to 'March/April through November,' omitting the 'typically' qualifier and the April start date for actual data generation.
  - Source states the CyAN satellite 'generally does not resolve' certain shallow/embayment zones; claim's paraphrase to 'cannot resolve' slightly strengthens this to absolute rather than qualified language.
- **Reviewer notes:** All eight claims are directly supported by the source text. The analyst accurately extracted the key technical details (bloom thresholds, forecast output format, geographic scope, cited publications) and appropriately flagged what the source does NOT provide (e.g., validation methodology for the 90% accuracy; quantitative details for marine forecasts). Minor qualification: the claim's March/April dating and the omission of 'generally' from 'generally does not resolve' slightly flatten distinctions present in the source, but do not misrepresent the substance."

## Provenance
- Canonical URL: https://www.epa.gov/habs/hab-forecasts
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the live EPA page https://www.epa.gov/habs/hab-forecasts directly; no redirect occurred (url_used = resolved_url). The page is HTML, not a PDF, so full text was accessible. I issued one initial broad WebFetch and then several follow-up, narrowly-scoped WebFetch calls specifically asking for VERBATIM text (rather than paraphrase) because the first pass summarized numbers in prose; the follow-ups confirmed the exact wording used here for every quoted figure/threshold. One candidate detail from the very first (paraphrase-oriented) fetch pass — a claim that "long, thin lakes may show low probability despite localized blooms" — could not be reconfirmed as verbatim text in the follow-up verbatim-focused fetches, so it was DROPPED from this dossier entry rather than asserted as sourced. The page mentions "Lake Erie" exactly once, in passing ("Similar to that for Lake Erie, NOAA... serve forecasts for a number of coastal regions..."), with no hyperlink and no further elaboration — the page assumes reader familiarity with a NOAA Lake Erie HAB forecast product that is not itself described or linked on this page, so I have not characterized that product beyond noting the passing reference. This is a living, continuously-updated EPA web page (not a fixed dated publication) — content may change after the access date of this review.
