---
key: FED-025
title: Lake Erie HAB Tracker Archive (NOAA GLERL) — successor to the Lake Erie Harmful Algal Bloom Forecast bulletin
authors_or_org: NOAA Great Lakes Environmental Research Laboratory (GLERL), in collaboration with NOAA National Ocean Service (NOS) and the Cooperative Institute for Great Lakes Research (CIGLR). Named point of contact for the HAB Tracker: Mark Rowe, Research Physical Scientist, NOAA GLERL. General contact for the successor operational forecast: hab@noaa.gov.
year: Not stated on page (archived seasons run 2017–2019; page reflects a post-discontinuation status with no explicit publication/update date in the fetched text)
url: https://www.glerl.noaa.gov/res/HABs_and_Hypoxia/habTracker.html
access_date: 2026-07-01
tier: FED
source_type: U.S. federal government agency webpage / archived operational-forecast tool documentation (NOAA GLERL program page)
categories: [in-situ-and-weather-data, models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Lake Erie HAB Tracker Archive (NOAA GLERL) — successor to the Lake Erie Harmful Algal Bloom Forecast bulletin

**What it is.** The page documents the (now-discontinued) Experimental Lake Erie Harmful Algal Bloom (HAB) Tracker, a NOAA GLERL/NOS 5-day forecasting tool that combined satellite-derived cyanobacterial chlorophyll-a imagery, wind/wave hydrodynamic forecasts, and weekly in-situ microcystin sampling to depict likely surface bloom extent/movement and (via a separate vertical-distribution sub-model) the depth distribution of Microcystis in Lake Erie, and it points to the tool's operational successor, the NOAA Lake Erie HAB Forecast.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The Experimental Lake Erie HAB Tracker model has stopped running entirely; its functionality was transitioned into an operational successor product, the NOAA Lake Erie HAB Forecast.
  - *evidence:* Stated directly as the page's lead status information across all three fetches. (Overview / status section of the HAB Tracker Archive page)
  - *quote:* "The Experimental Lake Erie Harmful Algal Bloom (HAB) Tracker model is no longer running."
- **[✓ verified]** The Tracker's core product was a 5-day-ahead forecast of surface HAB concentration expressed as cyanobacterial chlorophyll-a, alongside supporting wind speed, wave height, and microcystin data.
  - *evidence:* Described in the 'Forecast Components' section of the page. (Forecast Components section)
  - *quote:* "5-day forecast"
- **[✓ verified]** A companion vertical-distribution component modeled how wind-driven mixing and thermal stratification move Microcystis through the water column, built on the assumption that colonies float — while explicitly noting some colonies instead sink and settle on the bottom under the same calm conditions that produce surface scums.
  - *evidence:* Direct model-assumption/caveat language captured from the 'Vertical Distribution Modeling' section. (Vertical Distribution Modeling section)
  - *quote:* "sinking Microcystis colonies, and other sinking algae, will accumulate on the bottom under the same calm conditions that lead to formation of floating scums at the surface."
- **[✓ verified]** Satellite inputs come from NASA MODIS Aqua/Terra and Copernicus Sentinel-3, processed through a named NOAA system and converted from a cyanobacterial index into a cyanobacterial chlorophyll-a scale.
  - *evidence:* Listed under 'Data Sources & Satellite Information'; the named processing system is given explicitly. (Data Sources & Satellite Information section)
  - *quote:* "NOAA HAB Operational Forecasting System"
- **[✓ verified]** Wind/wave conditions used by the model come from the Great Lakes Coastal Forecasting System (GLCFS), using observed lake-station winds for the nowcast and the National Weather Service's National Digital Forecast Database for the forecast period.
  - *evidence:* Described under 'Oceanographic Modeling'. (Oceanographic Modeling section)
  - *quote:* "Great Lakes Coastal Forecasting System (GLCFS)"
- **[✓ verified]** The Tracker does not itself forecast toxin (microcystin) levels — toxin data comes from separate weekly in-situ sampling, and values exceeding Ohio's Elevated Recreational Public Health Advisory level are flagged in red on the monitoring maps.
  - *evidence:* Explicit scope-limiting statement plus the color-coding rule, both under 'Toxin Thresholds'. (Toxin Thresholds section)
  - *quote:* "The HAB Tracker doesn't predict toxin concentrations."
- **[✓ verified]** In-situ water-quality/toxin samples are collected weekly at monitoring stations, with surface samples drawn from approximately 0.75 m depth.
  - *evidence:* Given under 'Water Quality Monitoring' / 'Sampling Frequency' across two of the fetches. (Water Quality Monitoring section)
  - *quote:* "approximately 0.75 m deep in the water column"
- **[✓ verified]** Dates for which satellite coverage was unusable due to clouds are flagged with an asterisk and backfilled using the most recent relatively cloud-free imagery rather than left blank.
  - *evidence:* Described under 'Data Gaps'. (Data Gaps section)
  - *quote:* "satellite data was unavailable due to cloud cover, therefore most the recent relatively cloud-free data was used"
- **[✓ verified]** NOAA GLERL explicitly disclaims operational-center status for this program and labels all of its forecasts/products, including the Tracker, as experimental with no guarantee of availability or accuracy.
  - *evidence:* Standalone disclaimer text returned identically by two separate fetches, indicating it is fixed site-wide/page language. (Limitations & Disclaimers section (site disclaimer))
  - *quote:* "NOAA/GLERL is not an operational center. We make every effort to ensure accuracy and minimize downtime, however, we cannot guarantee that data and products will always be available and/or accurate. Our forecasts and products should be considered experimental."
- **[✓ verified]** Archived full-season Tracker animations and archived forecasts are retained on the page for the 2017–2019 period only.
  - *evidence:* Listed under 'Archived Data'; one fetch pass surfaced all three years for animations, another surfaced only 2017/2018 as individually selectable archived forecasts, suggesting slightly different UI elements for animations vs. individual forecast selection. (Archived Data section)
  - *quote:* "Full-season animations available for: 2019, 2018, 2017"
- **[✓ verified]** The operational successor, the NOAA Lake Erie HAB Forecast, only begins issuing bulletins after in-situ sampling confirms Microcystis presence, runs during the bloom season typically from July to October, and is updated daily with current bloom extent and trajectory.
  - *evidence:* Described under 'Current Operational Product'. (Current Operational Product section)
  - *quote:* "typically July to October"

## Data / numbers
- 5-day forecast horizon for the HAB Tracker's surface bloom prediction
- ~0.75 m depth for in-situ surface water toxin/quality samples
- Weekly (approximately 7-day) in-situ sampling frequency for microcystin monitoring
- Bloom/forecast season described only qualitatively as 'typically July to October' (no exact calendar dates given)
- Archived seasons span 2017-2019 (full-season animations for 2019, 2018, 2017; individually selectable archived forecasts noted for 2017 and 2018 in one extraction pass)
- No numeric microcystin concentration threshold (e.g., in µg/L) for the 'Elevated Recreational Public Health Advisory' was present in the fetched text -- the page references the Ohio EPA advisory level by name only, without stating the value
- No satellite pixel resolution (m/km), model grid resolution, or exact tracker start/discontinuation calendar dates were present in the fetched text despite a targeted extraction attempt

## Methods
The (now-retired) HAB Tracker fused three data/method streams to make short-term, spatially explicit bloom forecasts for Lake Erie: (1) Remote sensing -- NASA MODIS Aqua/Terra and Copernicus Sentinel-3 imagery processed through the 'NOAA HAB Operational Forecasting System,' converting a cyanobacterial index into a cyanobacterial chlorophyll-a scale as the surface-bloom-extent input; (2) Hydrodynamic/weather modeling -- wind and wave nowcasts/forecasts from the Great Lakes Coastal Forecasting System (GLCFS), combining observed near-lake station winds (nowcast) with the National Weather Service's National Digital Forecast Database (forecast period), used to drive a vertical-distribution sub-model of wind-driven mixing and thermal stratification that estimates how buoyant (assumed-floating) Microcystis colonies redistribute through the water column, while acknowledging some colonies sink instead; (3) In-situ monitoring -- weekly water sampling at fixed stations (surface draws at ~0.75 m) for microcystin, cross-referenced against the Ohio EPA's Elevated Recreational Public Health Advisory level (exact concentration value not given on this page) and displayed on maps rather than forecast by the model itself. The page states the underlying model 'is no longer running' and that this functionality was transitioned into the operational NOAA Lake Erie HAB Forecast, which instead issues daily-updated bulletins on current bloom extent/trajectory once in-situ sampling has confirmed Microcystis presence, rather than continuously running the Tracker's own physically based forecast.

## Stated limitations
The source states, in its own disclaimer, that "NOAA/GLERL is not an operational center. We make every effort to ensure accuracy and minimize downtime, however, we cannot guarantee that data and products will always be available and/or accurate. Our forecasts and products should be considered experimental." Specific caveats from the page: (1) the HAB Tracker explicitly "doesn't predict toxin concentrations" -- microcystin risk is monitored separately via weekly in-situ sampling, not forecast; (2) the vertical-distribution component "does not predict the presence of HABs at the station" (per one extraction pass), i.e., it characterizes likely depth distribution conditional on a bloom being present rather than predicting occurrence; (3) the vertical model assumes Microcystis colonies float, but the page itself flags that some colonies sink and settle on the bottom under calm conditions, a known deviation from the model's core assumption; (4) satellite-derived inputs have data gaps from cloud cover, flagged with an asterisk and backfilled with the "most recent relatively cloud-free" imagery rather than true same-day data; (5) as a whole, the experimental model has been discontinued ("no longer running"), so it is no longer a live, current data source -- only the 2017-2019 archive remains, and its methodology has been superseded by a different, simpler operational bulletin workflow (sampling-confirmed, daily-updated) rather than continuing to run the original forecast model.

## Tensions with other findings
Two tensions relevant to the HAB_PoC project: (1) The source explicitly and repeatedly separates satellite-derived cyanobacterial chlorophyll-a signal from actual toxin (microcystin) risk -- "The HAB Tracker doesn't predict toxin concentrations" -- which cautions against treating a satellite/chlorophyll-based "bloom" signal as equivalent to a public-health/toxin risk signal; any product claim in this PoC that frames a satellite-driven risk score as a toxin-exposure risk should be bounded accordingly, consistent with the project's own claim-gate discipline. (2) The fact that NOAA GLERL's own physically based, multi-data-stream forecast model was fully discontinued and replaced by a simpler, sampling-triggered, non-model-driven bulletin is a real-world precedent that a more complex fused model is not always operationally sustained even by the agency that built it -- relevant to this project's Part C production/monitoring and drift discussion, and a point of tension with any assumption that more sophisticated data fusion necessarily "wins" operationally. No direct numeric contradiction with other HAB sources was evident in the fetched text (this page does not report a bloom severity index or comparable quantitative bloom-intensity metric to cross-check against other sources).

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The vertical distribution model 'does not predict the presence of HABs at the station' — a significant scope limitation present in the source text but not reflected in any of the claims.
- **Reviewer notes:** All 11 claims are clearly supported by the source text. No hallucinated numbers were detected; all numeric details (5-day forecast, 0.75 m depth, 2017–2019 archive span, July–October season) are present in the source. One meaningful caveat was omitted: the source explicitly states that vertical distribution analysis 'does not predict the presence of HABs at the station,' a limitation not mentioned in claim 3 (which discusses the vertical distribution component) or elsewhere. This omission does not affect the 'pass' rating (based on absence of unsupported claims and hallucinated figures) but represents incomplete representation of model scope."

## Provenance
- Canonical URL: https://www.glerl.noaa.gov/res/HABs_and_Hypoxia/habTracker.html
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Performed three WebFetch passes on the single primary URL (exceeding the required two, since the first two passes -- one broad/comprehensive, one focused on numbers/links/history -- did not surface fine-grained numeric detail such as pixel resolution or an exact microcystin threshold, so a third pass explicitly targeted numbers/dates/thresholds). The URL did not redirect in any pass, so url_used = resolved_url = the given primary URL. All three passes agreed closely on content and reused near-identical wording for the site disclaimer, the 5-day forecast horizon, the 0.75 m sampling depth, the satellite sources, GLCFS, and the 2017-2019 archive years, which increases confidence those figures are genuinely on the page rather than fetch-tool invention. A supplementary WebSearch (not treated as a substitute source, only as corroboration since the primary fetch succeeded) returned matching claims from the same URL's search snippet and from NOAA's own decision-support-tools page, and also surfaced a related NOAA repository journal article ("Vertical distribution of buoyant Microcystis blooms in a Lagrangian particle tracking model for short-term forecasts in Lake Erie") that appears to be the underlying peer-reviewed methods paper for the vertical-distribution sub-model; I did NOT pull any claims from that paper into this dossier entry because it was not confirmed to be quoted/named on the fetched habTracker.html page itself, and the task requires claims to trace only to the fetched source text -- flagging it here only as a lead for a possible separate dossier entry. No numeric microcystin threshold (µg/L), no satellite/model spatial resolution, no exact tracker start date, and no grant/funding-award numbers were present in any of the three fetches despite a dedicated attempt -- these are reported as explicit absences rather than filled from outside knowledge, per the fidelity rule against inventing plausible-sounding numbers. Category was reassessed from the provisional "in-situ-and-weather-data" to "models-and-methods" because the page's substantive content centers on describing a forecast model/tool (its data-fusion methodology, forecast horizon, vertical-distribution sub-model and assumptions, and its discontinuation/replacement) rather than serving primarily as an in-situ or weather dataset description; relevance is kept at High because the tool is a directly on-point, real-world precedent for exactly the satellite+in-situ/weather fusion and non-technical-user decision-support framing this PoC's Parts A-C are meant to address, including a candid, quotable disclaimer of experimental status and a concrete example of a fused model being discontinued in favor of a simpler operational product.
