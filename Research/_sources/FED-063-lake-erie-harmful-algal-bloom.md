---
key: FED-063
title: Lake Erie Harmful Algal Bloom
authors_or_org: NOAA National Weather Service (Cleveland, OH forecast office), in cooperation with NOAA National Ocean Service, NOAA Office of Atmospheric Research/GLERL, and NOAA National Centers for Coastal Ocean Science (NCCOS)
year: Undated / continuously-updated operational page (accessed 2026-07-01; content confirmed current via an on-page item dated June 14, 2026)
url: https://www.weather.gov/cle/LakeErieHAB
access_date: 2026-07-01
tier: FED
source_type: Government agency operational forecast/informational webpage (NOAA/National Weather Service field office)
categories: [models-and-methods]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Lake Erie Harmful Algal Bloom

**What it is.** A National Weather Service (NWS) Cleveland forecast-office webpage that serves as the public portal for NOAA's operational Lake Erie Harmful Algal Bloom (HAB) forecast — a multi-agency (NOAA National Ocean Service, OAR/GLERL, NWS, and NCCOS) daily product that models cyanobacterial bloom position/trajectory during bloom season — rather than a peer-reviewed research paper.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The page's own definition frames HABs as a rapid overgrowth of algae that causes toxic/harmful effects on people, wildlife, and local economies.
  - *evidence:* This is the page's opening definition, establishing why the forecast product exists. (Page introduction / definition of HABs)
  - *quote:* "rapid growth of algae that produce toxic or harmful effects on people, fish, marine mammals, birds and local economies"
- **[✓ verified]** The Lake Erie HAB forecast is produced jointly by four NOAA components: National Ocean Service, Office of Atmospheric Research/GLERL, National Weather Service, and the National Centers for Coastal Ocean Science (NCCOS).
  - *evidence:* The fetched page text explicitly labels the product a 'multi-agency effort' and names these NOAA offices as co-producers; NCCOS is identified as the office that issues the forecasts to aid responders and public decision-making. (Introductory/attribution section)
  - *quote:* "multi-agency effort"
- **[✓ verified]** NCCOS only issues the daily forecast during the bloom season (typically July–October) once field/in-situ sampling has confirmed the HAB species Microcystis is present.
  - *evidence:* States the operational trigger conditions — a seasonal window plus an in-situ confirmation step — that gate when the forecast product starts running each year. (Forecast Details section)
  - *quote:* "typically July to October"
- **[✓ verified]** The forecast is updated daily and reports the bloom's current extent and trajectory as it forms.
  - *evidence:* Describes the update cadence and communicative purpose of the product (extent + movement, not just a static snapshot). (Forecast Details section)
  - *quote:* "updated daily"
- **[✓ verified]** The bloom position forecast projects the bloom's modeled location for a minimum of 96 hours from the date of publication by advecting the satellite-observed bloom using 3-D hydrodynamic lake-current output from the Lake Erie Operational Forecast System (LEOFS).
  - *evidence:* Confirmed by the primary page fetch (satellite imagery + LEOFS current data + hydrodynamic/3-D modeling) and independently corroborated by a search-surfaced NCCOS description of the same product using near-identical wording. (Technical approach / methodology section)
  - *quote:* "a minimum of 96 hours from the date of publication"
- **[✓ verified]** The product explicitly disclaims quantitative reliability: predicted bloom concentrations are guidance only and may not reflect the true, on-the-ground bloom condition.
  - *evidence:* A direct, source-stated limitation on how much weight users should put on the forecast's numeric/visual output. (Caveats/disclaimer text accompanying the bloom position forecast graphic)
  - *quote:* "The concentration predicted by the bloom position forecast is for guidance only, and may not represent the actual bloom condition in Lake Erie."
- **[⚠ partial]** The model visualization has stated representational gaps: cloud cover is not depicted, and the color legend distinguishing 'no chlorophyll' from 'no data' could be misread if not understood.
  - *evidence:* Source states the modeled output excludes clouds and defines a black-vs-grey color convention for absence-of-signal versus absence-of-data. (Caveats/disclaimer text (image legend))
  - *quote:* "The modeled output does not contain clouds"
  - *reviewer:* Source explicitly states that cloud cover is not depicted in the modeled output and provides the color convention (black = absence of chlorophyll, grey = no data), but does not explicitly characterize the color legend as something that 'could be misread if not understood.' The potential for misreading is an analyst inference, not an explicit statement in the source.
- **[✓ verified]** The weather.gov/cle page itself functions mainly as a navigation portal to the authoritative NOAA/NCCOS materials (a seasonal bulletin PDF and the NCCOS Lake Erie HAB forecast website) rather than hosting the underlying bloom imagery/data directly.
  - *evidence:* The page's HAB-specific hyperlinks route to an external current-conditions bulletin PDF and to NCCOS's own Lake Erie HAB forecast site, plus a separate 'Supplemental Information' page, indicating the weather.gov page is a front door rather than the primary data repository. (Available Resources / Access section and full hyperlink listing)

## Data / numbers
- 96 hours — minimum forecast horizon of the bloom position forecast loop 'from date of publication'; consistent across the primary page fetch and a corroborating NCCOS-derived description found via search ('a minimum of 96 hours from the date of publication')
- Bloom season window: 'typically July to October' — period during which NCCOS issues the daily Lake Erie HAB forecast
- '2025' — appeared once, in what one fetch pass characterized as a page title ('2025 Harmful Algal Blooms (HAB) for Lake Erie'); NOT reconfirmed in two subsequent fetch passes of the same URL, so treated here as unverified rather than a confirmed fact

## Methods
Not a statistical/ML model in the research sense — an operational nowcast/forecast pipeline: (1) satellite imagery establishes the bloom's initial/observed position (remote-sensing input, only usable once in-situ sampling confirms Microcystis presence); (2) a 3-dimensional hydrodynamic circulation model, the Lake Erie Operational Forecast System (LEOFS), supplies modeled lake-current fields; (3) the observed bloom is advected forward using those modeled currents to produce a 'bloom position forecast' out to a minimum of 96 hours from publication; (4) western-basin water-temperature and wind averages are overlaid (in magenta) on the model output. Source-stated 'works for': daily guidance on bloom extent and trajectory during bloom season. Source-stated 'fails/does not work for': precise concentration values ('guidance only... may not represent the actual bloom condition'), and any cloud-obscured area (model output contains no cloud representation, so those pixels cannot be assessed).

## Stated limitations
Source-stated limitations found on the page itself: (1) predicted bloom concentrations are "for guidance only, and may not represent the actual bloom condition in Lake Erie"; (2) "the modeled output does not contain clouds," i.e., cloud-obscured areas are not represented in the bloom-position visualization; (3) the color legend requires correct interpretation — black means "absence of chlorophyll" while grey means "areas with no data," and conflating the two would misread the map. Beyond what the page states about itself, a targeted check of the fetched content found this source contains no bloom severity index/numeric severity scale, no microcystin concentration thresholds (µg/L or otherwise), no mention of the 2014 Toledo water-supply crisis, no historical multi-year bloom comparisons (e.g., 2011/2015/2019), and no phosphorus-loading discussion — so, taken alone, this page provides no forecast-skill/accuracy statistics and no historical trend data against which to benchmark the 96-hour bloom-position product.

## Tensions with other findings
As an operational public-communication portal rather than a peer-reviewed model paper, this source reports no accuracy, skill score, or uncertainty quantification for its 96-hour bloom-position forecast — its own disclaimer ("guidance only... may not represent the actual bloom condition") functions as an implicit acknowledgment of that gap, in contrast to more quantitative HAB literature (e.g., EPA CyAN cyanobacteria index products or peer-reviewed bloom-forecast validation studies) that typically report explicit skill metrics or thresholds. Because this is a live, continuously updated field-office page, its exact text/graphics likely shift with the season and date of access: one of three fetch passes surfaced a "2025" season-year label not reconfirmed on the other two passes, so any date-specific wording here should be re-verified at time of actual use rather than treated as fixed.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - when conditions are optimal for growth (stated in source context for seasonal forecasting trigger, not emphasized in claim 3)
- **Reviewer notes:** Seven of eight claims are clearly supported by the source text. Claim 7 contains a factual kernel (cloud cover omission, color definitions) that is explicitly stated, but adds an inference ('could be misread') not present in the source. The source provides the color convention but does not characterize it as potentially confusing. All numerical references (four components, July–October, 96 hours, 3-D) are present in the source. No hallucinated numbers detected. One minor dropped caveat regarding 'optimal growth conditions' in the seasonal forecasting section."

## Provenance
- Canonical URL: https://www.weather.gov/cle/LakeErieHAB
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary URL (https://www.weather.gov/cle/LakeErieHAB) three times with WebFetch using different prompts: (1) a general comprehensive-extraction prompt, (2) a request for verbatim/literal reproduction of page text, and (3) a targeted prompt checking for specific absent content (severity index, microcystin thresholds, historical bloom years, phosphorus loading) plus a full hyperlink/list dump. All three succeeded on the same URL with no redirect, paywall, or block. A supplementary WebSearch was run to corroborate the exact wording of the '96 hours' forecast-horizon figure against NOAA/NCCOS's own description, since two WebFetch passes phrased it slightly differently ('minimum of 96 hours from date of publication' vs. 'up to 96 hours ahead'); the search-derived NCCOS description confirms 'a minimum of 96 hours from the date of publication' is the accurate framing. Because WebFetch is AI-mediated (it converts HTML to markdown and summarizes via a small model rather than returning raw HTML), byte-exact page wording could not be independently confirmed in every instance; where passes disagreed I flagged it rather than asserting a single wording as certain (see the '2025' title discrepancy in data_numbers). The page is a live, continuously-updated NWS field-office page — one fetch surfaced an on-page item dated "June 14, 2026," confirming the fetch reflects current (2026) content rather than a stale cache. This page is an operational public-facing forecast portal, not a peer-reviewed paper, so it contains no validation statistics, historical bloom time series, or toxin-threshold data; those would live in the linked NCCOS bulletin PDF or FAQ pages, which were not separately fetched for this dossier (out of scope: only the primary URL was reviewed per instructions).
