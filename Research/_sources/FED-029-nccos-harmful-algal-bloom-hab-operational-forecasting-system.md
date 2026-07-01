---
key: FED-029
title: NCCOS Harmful Algal Bloom (HAB) Operational Forecasting System
authors_or_org: NOAA National Centers for Environmental Information (NCEI), in partnership with NOAA National Centers for Coastal Ocean Science (NCCOS)
year: Undated on the page itself; the cited processing-methodology reference is dated 2020 (Wynne et al.), and the archive listings span bloom seasons 2021-2024
url: https://www.ncei.noaa.gov/products/nccos-harmful-algal-blooms-operational-forecasting-system
access_date: 2026-07-01
tier: FED
source_type: NOAA government operational-program / data-archive product page (non-peer-reviewed federal agency web page)
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# NCCOS Harmful Algal Bloom (HAB) Operational Forecasting System

**What it is.** HABOFS (NCCOS Harmful Algal Bloom Operational Forecast System) is a NOAA operational program -- catalogued and archived at NCEI -- that issues regionally-specific HAB nowcasts plus short-term (roughly weekly to twice-weekly) and seasonal forecasts by fusing processed satellite ocean-color imagery with meteorological data, field/in-situ monitoring data, and bloom-trajectory models; NCEI currently archives its bulletin and model-output products specifically for Lake Erie and for the Florida & Texas Gulf of Mexico region.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** HABOFS is a national network of NOAA HAB forecast products spanning current-condition nowcasts, short-term (once/twice-weekly) forecasts, and seasonal forecasts.
  - *evidence:* Stated verbatim in the opening description, consistently returned by both independent fetches of the primary URL. (NCEI product page (primary URL), introductory description)
  - *quote:* "a national network of HAB forecasts which provide guidance on regionally-specific risks and impacts of HABs, including current bloom conditions (nowcasts), as well as short-term (once or twice weekly) and seasonal forecasts of future HAB conditions and impacts"
- **[✓ verified]** The stated purpose of HABOFS is to give advance warning of HABs affecting coastal natural resources, people, communities, and economies.
  - *evidence:* Purpose statement given verbatim, identically, in both fetches of the primary page. (NCEI product page (primary URL))
  - *quote:* "HABOFS provides advanced warning of HABs that impact coastal natural resources, people, communities, and economies"
- **[✓ verified]** NCEI currently archives HABOFS output for two specific regions: Lake Erie (bloom seasons 2021-2023) and the Florida & Texas Gulf of Mexico system (2022-2024).
  - *evidence:* Both independent fetches of the primary page listed the same two regions and matching year ranges. (NCEI product page (primary URL), coverage/archive listing)
  - *quote:* "Data archived for 2021, 2022, and 2023" (Lake Erie); "Data archived for 2022, 2023, and 2024" (Florida and Texas)"
- **[✓ verified]** For Lake Erie, the archived products are daily-frequency processed satellite imagery inputs and a daily HAB Bulletin.
  - *evidence:* Listed in the first fetch's regional breakdown of product types and update frequency. (NCEI product page (primary URL))
  - *quote:* "Processed Satellite Imagery Input (Daily frequency) ... HAB Bulletin (Daily frequency)"
- **[✓ verified]** For the Gulf of Mexico, the Florida & Texas Respiratory Irritation Forecast runs on a 3-hour model cycle, alongside daily 8-day satellite composite images for each state.
  - *evidence:* The "3 hour" cycle for the respiratory-irritation product was returned independently by both fetches; the daily 8-day composite products were listed in the first fetch's regional breakdown. (NCEI product page (primary URL))
  - *quote:* "Florida and Texas Respiratory Irritation Forecast ("3 hour" model cycle)"
- **[✓ verified]** HAB forecast bulletins produced by the system look up to five days into the future.
  - *evidence:* Explicit forecast-horizon figure given in the first fetch's technical-details section. (NCEI product page (primary URL))
  - *quote:* "up to five days in the future"
- **[⚠ partial]** HABOFS archived imagery/model-output products are retained at NCEI for one year after processing.
  - *evidence:* Explicit retention statement in the first fetch's technical-details section. (NCEI product page (primary URL))
  - *quote:* "archived within one year"
  - *reviewer:* Source states data are 'archived within one year,' which describes archival *timing* (when data become available), not retention *duration* (how long they remain accessible). The claim interprets this as a one-year retention policy, but the source does not explicitly specify retention duration.
- **[✓ verified]** Forecasts are issued on a routine, pre-set schedule that is tailored per region and end-user need rather than a single fixed national cadence.
  - *evidence:* Identical phrasing returned by both fetches of the primary page. (NCEI product page (primary URL))
  - *quote:* "generated on a routine, pre-defined schedule, based on regional conditions and end-user needs"
- **[✓ verified]** The satellite imagery feeding HABOFS is processed through a separate NCCOS product, the "Harmful Algal Bloom Monitoring System," and archived copies of that imagery reflect whichever processing version was used for the forecast at the time -- not necessarily the most current reprocessing.
  - *evidence:* Stated in the "data sources" and "caveats" sections of the first fetch of the primary page. (NCEI product page (primary URL))
  - *quote:* "corresponds to the version used in the associated HABOFS products" and "may not reflect the most current satellite reprocessing version"
- **[✓ verified]** The satellite ocean-color processing methodology underlying HABOFS is documented in a specific, citable NOAA technical report with its own DOI.
  - *evidence:* Full citation with DOI returned verbatim by the second fetch of the primary page. (NCEI product page (primary URL), citation/reference section)
  - *quote:* "Wynne, T., Meredith, A., Stumpf, R., Briggs, T., & Litaker, W. (2020). Harmful Algal Bloom Forecasting Branch Ocean Color Satellite Imagery Processing Guidelines, 2020 Update. https://doi.org/10.25923/606t-m243"
- **[✓ verified]** Beyond the two regions NCEI itself archives, NOAA NCCOS's live operational program runs its own forecasts for three regions (Florida & Texas, Gulf of Maine, Lake Erie) and additionally lists two externally-run partner forecasts (Pacific Northwest via NANOOS, California via SCCOOS).
  - *evidence:* Found by fetching the companion "HAB Forecasts" landing page that the primary NCEI page itself names as the source of "real-time forecasts and additional information"; resolves the primary page's own (otherwise unconfirmed) reference to covering "three regions." (coastalscience.noaa.gov/science-areas/habs/hab-forecasts/ -- companion page explicitly linked from the primary URL, NOT the primary URL's own text)
  - *quote:* "Florida & Texas Forecasts / Gulf of Maine Forecast / Lake Erie Forecast"
- **[✓ verified]** The forecasting effort targets different HAB-causing organisms by region: Karenia brevis in Florida/eastern and western Gulf waters, cyanobacteria in Lake Erie, Alexandrium fundyense in the Gulf of Maine, Pseudo-nitzschia off the Washington coast, and multiple species along the California coast and in Chesapeake Bay.
  - *evidence:* Species-by-region table returned from the companion NCCOS project page describing the same HAB-forecasting program in more depth than the bare NCEI archive listing. (coastalscience.noaa.gov/project/harmful-algal-bloom-hab-forecasting/ -- companion page, not the primary URL)
  - *quote:* "Karenia brevis | Florida and eastern Gulf; Western Gulf ... Cyanobacteria | Lake Erie ... Alexandrium fundyense | Gulf of Maine"
- **[✓ verified]** Forecasts are produced by fusing multiple observing streams -- satellite imagery, NOAA-station meteorological data, state/university field monitoring data, and bloom-trajectory models -- rather than from satellite data alone.
  - *evidence:* Directly quoted data-fusion sentence from the companion project page; the primary NCEI page itself only mentions the satellite-imagery component of this fusion. (coastalscience.noaa.gov/project/harmful-algal-bloom-hab-forecasting/ -- companion page, not the primary URL)
  - *quote:* "combining data from various ocean-observing systems, including satellite imagery, meteorological data from NOAA observing stations; field data collected by state and university monitoring programs; and models which predict where a bloom is going to go"
- **[⚠ partial]** For Lake Erie specifically, forecast issuance steps up from weekly during non-bloom periods to twice-weekly ("bi-weekly") once a bloom is active.
  - *evidence:* Explicit region-specific frequency statement from the companion project page. (coastalscience.noaa.gov/project/harmful-algal-bloom-hab-forecasting/ -- companion page, not the primary URL)
  - *quote:* "bi-weekly during an active bloom and weekly during non-bloom periods"
  - *reviewer:* Source states 'bi-weekly during an active bloom' but 'bi-weekly' is ambiguous in English—it can mean either twice per week or every other week. While the claim's interpretation ('twice-weekly') is contextually logical (frequency should increase, not decrease, during active blooms), the source term itself is not unambiguous. The claim adds a specific interpretation of an ambiguous term.
- **[✓ verified]** NOAA's own program page states an explicit resource constraint and an acknowledged shortfall from a true national forecasting capability.
  - *evidence:* Self-reported limitation quoted directly from the companion project page -- an unusually candid admission on a federal operational-program page. (coastalscience.noaa.gov/project/harmful-algal-bloom-hab-forecasting/ -- companion page, not the primary URL)
  - *quote:* "There are not sufficient funds to sample every event ... we still have a long way to go to reach a National Forecast capacity for HABs"
- **[✓ verified]** None of the fetched pages (the primary NCEI page or the two linked NCCOS companion pages) publish a quantitative accuracy, skill, or validation statistic for the forecasts.
  - *evidence:* Both companion-page extractions explicitly flagged this as absent, and no accuracy figure appeared in either fetch of the primary page either -- an absence noted across four independent extraction passes. (Absence checked across NCEI product page (primary URL) and both companion pages)

## Data / numbers
- Forecast bulletin horizon: "up to five days in the future"
- Archive retention: processed imagery/model output "archived within one year"
- Florida & Texas Respiratory Irritation Forecast model cycle: "3 hour"
- Lake Erie archived seasons at NCEI: 2021, 2022, and 2023
- Florida & Texas (Gulf of Mexico) archived seasons at NCEI: 2022, 2023, and 2024
- System-wide short-term forecast frequency: "once or twice weekly"
- Lake Erie forecast frequency: weekly during non-bloom periods, stepping up to "bi-weekly" (twice weekly) "during an active bloom"
- Methodology citation DOI for satellite-imagery processing: https://doi.org/10.25923/606t-m243 (Wynne, Meredith, Stumpf, Briggs & Litaker, 2020)
- No quantitative accuracy/skill/validation percentage is stated anywhere in the fetched pages (explicitly noted as absent by two independent extractions)

## Methods
HABOFS nowcasts/forecasts are generated by fusing: (1) satellite ocean-color imagery processed through NCCOS's separate "Harmful Algal Bloom Monitoring System" (described as delivering "near real-time information for locating and quantifying HABs"), following a specific documented methodology (Wynne et al. 2020, "Harmful Algal Bloom Forecasting Branch Ocean Color Satellite Imagery Processing Guidelines, 2020 Update," DOI 10.25923/606t-m243); (2) meteorological data from NOAA observing stations; (3) field/in-situ monitoring data collected by state and university programs; and (4) models that project where a detected bloom will move over the following days (companion project page). Regional products differ: Lake Erie receives daily processed-imagery inputs and a daily HAB Bulletin (forecast horizon "up to five days in the future"); the Gulf of Mexico (Florida & Texas) receives a Respiratory Irritation Forecast on a "3 hour" model cycle plus daily 8-day satellite composite images per state. The source describes the pipeline as operating routinely enough to be archived at NCEI and reused, but the fetched pages give no quantitative accuracy/skill/validation statistic for forecast performance -- they document the pipeline's inputs, products, and cadence, not independently verified predictive skill.

## Stated limitations
The fetched material states several explicit caveats: (1) forecasts are "based on our understanding of HABs and how they respond to regionally changing weather and ocean conditions" -- i.e., skill is bounded by current scientific understanding, not guaranteed; (2) the whole approach "rel[ies] on the ability to routinely and remotely detect HABs, their toxins, and environmental conditions that foster blooms," making it contingent on detection capability; (3) archived processed-satellite imagery "corresponds to the version used in the associated HABOFS products" at the time and "may not reflect the most current satellite reprocessing version" -- a versioning/reproducibility caveat for anyone re-analyzing archived imagery; (4) the linked NCCOS project page states plainly "There are not sufficient funds to sample every event" and that NOAA "still ha[s] a long way to go to reach a National Forecast capacity for HABs" -- an explicit admission of incomplete national coverage and resource constraints; (5) no page fetched (primary or companion) gives a quantitative accuracy/skill/validation number for any of the forecasts, an absence explicitly flagged by the extraction process on two separate pages.

## Tensions with other findings
This source complicates a satellite-only framing of HAB early warning: NOAA's own operational system explicitly fuses satellite imagery with meteorological data, field/in-situ monitoring, and predictive models rather than issuing forecasts from remote sensing alone -- implying that a model built solely on a satellite signal (e.g., an EPA CyAN-type product) is, by NOAA's own operational design choice, a partial input rather than a full analog of an operational "forecast." It also complicates any assumption that operational HAB forecasting is a mature, nationally uniform, validated capability: coverage is explicitly regional and patchy (only three NCCOS-run regions plus two externally-run partner regions per the linked landing page; NCEI itself currently archives only two of those regions), the program states outright that it lacks funds to sample every event and is far from "National Forecast capacity," and none of the fetched pages publish a quantitative accuracy or skill statistic for the forecasts -- so this source should not be cited as evidence that operational HAB forecasts are independently validated at any stated accuracy level; it documents the existence, inputs, and cadence of the operational pipeline, not its verified predictive skill.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** Verification against primary NCEI page and linked companion pages (NCCOS HAB forecasts and HAB forecasting project pages). Two claims are marked PARTIAL for semantic ambiguity in the source text itself, not factual error: (1) Claim 7 conflates archival timing with retention duration; the source does not explicitly state how long products remain available, only when they are archived. (2) Claim 14 interprets the source's 'bi-weekly' as 'twice-weekly', which is a reasonable contextual reading (forecasts should increase during active blooms) but 'bi-weekly' is inherently ambiguous in English. All 14 numeric values in the claims are present in the source text. No hallucinated figures or unsupported claims identified."

## Provenance
- Canonical URL: https://www.ncei.noaa.gov/products/nccos-harmful-algal-blooms-operational-forecasting-system
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary NCEI URL twice with different extraction prompts, as instructed for a HIGH-relevance source, and reconciled the two (union of content). Both fetches succeeded, returned substantive and mutually consistent content (same core description, same two archived regions, same "3 hour" and "five days" figures, same citation), so the page was judged correct/not blocked -- no substitute source was needed and url_used = resolved_url = the given primary URL.

One inconsistency surfaced between the two primary-page fetches: fetch #1's extraction stated "the system currently covers three regions" but then enumerated only two (Lake Erie; Florida & Texas/Gulf of Mexico); fetch #2 also enumerated only two. This looks like exactly the small-model content-dropping problem the task description warns about (a third region's name was likely lost). To resolve this ambiguity and to more fully describe what HABOFS actually is (the primary NCEI page is essentially an archive/catalog entry that itself says "Real-time forecasts and additional information are available at" a companion NOAA NCCOS site), I additionally fetched two pages directly hyperlinked from the primary source: (a) https://coastalscience.noaa.gov/science-areas/habs/hab-forecasts/ (the "real-time forecasts" page named in the primary source's own text) and (b) https://coastalscience.noaa.gov/project/harmful-algal-bloom-hab-forecasting/ (the parent NCCOS project page, surfaced via one confirmatory WebSearch). These two companion-page fetches confirmed the live operational system runs three NCCOS-operated forecasts (Florida & Texas, Gulf of Maine, Lake Erie) plus lists two externally-run partner forecasts (Pacific Northwest via NANOOS, California via SCCOOS) -- resolving the "three regions" reference -- and supplied the species-by-region table and the explicit data-fusion sentence that the bare NCEI archive page did not itself contain. I have labeled every claim's "location" field so a reviewer can see exactly which claims come from the primary NCEI URL itself versus the two directly-linked companion pages; nothing is asserted from prior/training knowledge. I reassessed category from the provisional "in-situ-and-weather-data" to "models-and-methods" because the artifact itself is an operational forecasting SYSTEM/pipeline (nowcast + forecast models fusing satellite, met, and field data), not a raw in-situ/weather dataset per se.
