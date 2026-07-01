---
key: FED-068
title: NOAA Lake Erie Harmful Algal Bloom Forecast Products
authors_or_org: NOAA Great Lakes Environmental Research Laboratory (GLERL); NOAA National Centers for Coastal Ocean Science (NCCOS), with University of Michigan / Cooperative Institute for Great Lakes Research (CIGLR), North Carolina State University, Heidelberg University National Center for Water Quality Research, Ohio Sea Grant, Ohio State University Stone Laboratory, University of Toledo, Ohio EPA, and NWS Ohio River Forecast Center
year: n.d. (continuously updated NOAA operational webpage; content reflects the 2025 and 2026 forecast seasons as fetched on 2026-07-01)
url: https://www.glerl.noaa.gov/res/HABs_and_Hypoxia/bulletin.html
access_date: 2026-07-01
tier: FED
source_type: Government agency operational webpage / recurring forecast bulletin (NOAA GLERL and NCCOS)
categories: [models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# NOAA Lake Erie Harmful Algal Bloom Forecast Products

**What it is.** A NOAA GLERL webpage describing NOAA's operational suite of Lake Erie harmful-algal-bloom (HAB) forecast products for coastal managers and drinking-water facility operators: an early-season projection (from May), an early-July seasonal severity forecast, an in-season (roughly June/July–October) short-term bloom extent/concentration outlook, and a November seasonal retrospective. It is the landing page for a real-world operational analog of a satellite + in-situ HAB early-warning/action-window product.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** NOAA/GLERL issues three distinct Lake Erie HAB forecast products across the year: an early-season projection (from May), a seasonal severity forecast (early July), and a seasonal retrospective (November, after the bloom season ends).
  - *evidence:* Stated as the page's core structure describing the annual cadence of products for coastal managers and drinking-water operators. (glerl.noaa.gov/res/HABs_and_Hypoxia/bulletin.html, page overview)
  - *quote:* "NOAA issues a seasonal forecast in early July"
- **[✓ verified]** The early-season projection and seasonal forecast estimate how severe the upcoming bloom season is likely to be primarily from measured phosphorus loading in the Maumee River, combined with long-range weather/hydrological forecasts and historical bloom records.
  - *evidence:* Directly stated as the basis of the early-season and seasonal severity estimates; presented by the source as a predictive/associative input, not framed as a proven causal mechanism. (bulletin.html, early-season projections section)
  - *quote:* "measurements of phosphorus loading from the Maumee River combined with long-range forecasts and historical records"
- **[✓ verified]** During the bloom season, NOAA issues an in-season operational bulletin giving current bloom extent plus a 5-day outlook of where the bloom will move and what algae concentrations are likely, updated twice weekly, to support managers' decisions on preventative action.
  - *evidence:* Describes the short-horizon, decision-oriented product distinct from the once-a-season severity number. (bulletin.html, operational/in-season forecast section)
  - *quote:* "provides the current extent and 5-day outlooks of where the bloom will travel and what concentrations are likely to be seen"
- **[✓ verified]** The companion NOAA/NCCOS Lake Erie HAB forecast portal, linked from the GLERL bulletin page as the main forecast portal, describes a shorter, 96-hour minimum horizon for its bloom-position and vertical-mixing forecasts, generated from hydrodynamic modeled currents combined with the most recent satellite imagery.
  - *evidence:* Indicates the continuously-updated online model tool has a different stated horizon than the twice-weekly emailed bulletin, even though both are part of the same NOAA system. (coastalscience.noaa.gov/science-areas/habs/hab-forecasts/lake-erie/, Bloom Position Forecast / Vertical Mixing Forecast sections)
  - *quote:* "96 hours"
- **[✓ verified]** Current bloom location/extent for the online tool is derived from satellite true-color imagery from the Ocean Land Color Imager (OLCI) sensor, and the bloom-position layer is updated daily.
  - *evidence:* Identifies the specific satellite instrument feeding the current-conditions layer of the forecast. (coastalscience.noaa.gov Lake Erie HAB forecast portal, Satellite Imagery / Forecast Products section)
  - *quote:* "Ocean Land Color Imager (OLCI)"
- **[✓ verified]** The forecast's Severity Index (SI) is a unitless seasonal metric anchored to the lowest observed bloom-biomass season (2005) at one end and the highest observed bloom-biomass season (2011) at the other, computed over a 30-day assessment window.
  - *evidence:* Defines how the headline severity number is scaled to historical extremes, making it comparable across years. (coastalscience.noaa.gov Lake Erie HAB forecast portal, Severity Index / Seasonal Forecast section)
  - *quote:* "minimum observed bloom biomass (2005)"
- **[✓ verified]** For summer 2026, NOAA and partners forecast a moderate bloom with a Severity Index of 3.5 and a potential range of 3 to 4.5; the source defines 3-5 as the moderate band, above 5 as more severe, and above 7 as particularly severe with extensive scum formation.
  - *evidence:* Gives both the concrete 2026 point forecast/range and the qualitative bands used to interpret any SI value. (coastalscience.noaa.gov news release, "Moderate Harmful Algal Bloom Predicted for Western Lake Erie in Summer 2026")
  - *quote:* "Moderate blooms have an index of 3-5, while an index above 5 indicates more severe HABs. Blooms over 7 are particularly severe, with extensive scum formation and bloom coverage affecting the lake."
- **[✓ verified]** NOAA attributes the width of the forecast's severity range (e.g., 3-4.5 for 2026) explicitly to two unresolved factors: nutrients already resident in the lake from prior seasons, and competition from other (non-target) algal species.
  - *evidence:* This is the source's own explicit uncertainty/limitation statement explaining why the point forecast is given as a range rather than a single number. (coastalscience.noaa.gov news release, forecast-uncertainty paragraph)
  - *quote:* "The range in forecasted severity reflects the uncertainty in accounting for the influence of factors such as residual nutrients already in the lake, or competition from other algal species."
- **[✓ verified]** NOAA states that bloom duration is additionally gated by a factor with no advance predictability at seasonal-forecast lead time: the frequency of high wind events in September.
  - *evidence:* A second explicit, source-acknowledged limitation on forecast skill, specific to bloom persistence/duration rather than peak severity. (coastalscience.noaa.gov news release, forecast-uncertainty paragraph)
  - *quote:* "the duration of the bloom depends on the frequency of high winds in September, which can't be predicted this far in advance"
- **[⚠ partial]** The forecast system is a multi-institution operational partnership: nutrient-loading data from Heidelberg University's National Center for Water Quality Research; forecast models run by NOAA NCCOS, the University of Michigan, and North Carolina State University; field observations from the NWS Ohio River Forecast Center, NOAA GLERL, CIGLR, Ohio Sea Grant, Ohio State University's Stone Laboratory, the University of Toledo, and Ohio EPA.
  - *evidence:* Lists the specific organizations responsible for each data/modeling component, relevant to provenance/traceability of the product. (coastalscience.noaa.gov news release, methods/partners section)
  - *quote:* "Forecast models are run by NCCOS, University of Michigan, and North Carolina State University"
  - *reviewer:* The source identifies the partner as 'Ohio River Forecast Center' (URL 3) but the claim specifies 'NWS Ohio River Forecast Center'—the 'NWS' prefix does not appear in the source text.

## Data / numbers
- Severity Index (SI, unitless) forecast for 2026: 3.5 point value, potential range 3-4.5, classified "moderate"
- SI interpretation bands per NCCOS: "Moderate blooms have an index of 3-5", "an index above 5 indicates more severe HABs", "Blooms over 7 are particularly severe, with extensive scum formation and bloom coverage"
- SI scale anchors: minimum observed bloom biomass = 2005; maximum observed bloom biomass = 2011
- 3 distinct forecast products issued per year (early-season projection, seasonal forecast, seasonal retrospective)
- Early-season projections issued weekly from May until the seasonal forecast is announced
- Seasonal forecast generally issued "in early July"; the actual 2025 seasonal forecast was issued June 25, 2025 ("June 25th")
- Bloom/forecast season window given as "June until October" (GLERL bulletin page) vs. "July to October" (NCCOS forecast portal)
- 2025 forecast season ended 11/19/2025 ("final day of the 2025 Lake Erie HAB forecast season")
- In-season bulletin update frequency: twice weekly (GLERL bulletin page); online "Observed and Forecasted Bloom Position" tool updated daily (NCCOS portal)
- In-season outlook horizon: "5-day outlooks" (GLERL bulletin page) vs. "96 hours" minimum (NCCOS portal), for bloom position and vertical-mixing forecasts
- Severity assessment period described as a "30 day period" (NCCOS portal)
- Historical comparison bar graph in the 2026 news release spans years "dating back to 2002"
- Example model-update timestamp at time of access: "Model Last Updated: 2026-07-01 02 PM EST" (NCCOS portal)

## Methods
The seasonal severity forecast is built from measured total phosphorus loading in the Maumee River (data from Heidelberg University's National Center for Water Quality Research), combined with long-range weather/hydrological forecasts and historical bloom records; the resulting "Severity Index" (SI) is a unitless seasonal metric scaled between the minimum observed bloom biomass (2005) and maximum observed bloom biomass (2011), computed over what one linked page calls a "30 day period." In-season operational forecasts add satellite true-color imagery from the Ocean Land Color Imager (OLCI) for current bloom location/extent, hydrodynamic modeled currents for a bloom-position outlook (described as "5-day outlooks" on the GLERL bulletin page and as a "96 hours" minimum horizon on the linked NCCOS forecast portal), a separate vertical-mixing forecast (surface vs. sub-surface likelihood), and field toxicity samples. Forecast models are run by NCCOS, the University of Michigan, and North Carolina State University; nutrient and field observations come from a multi-partner network (Ohio Sea Grant, GLERL, CIGLR, Ohio State University's Stone Laboratory, University of Toledo, Ohio EPA, NWS Ohio River Forecast Center). The fetched pages do not report quantitative hindcast/validation skill statistics (no RMSE, correlation, or hit-rate figures) for either the severity index or the position/mixing forecasts; the only explicit uncertainty language is the qualitative severity-index range (e.g., 3-4.5 for the 2026 season) attributed to named unresolved factors, and a 2025 satellite "reprocessing" with "new calibrations and improved algorithms" that may affect comparability of index values across years.

## Stated limitations
The fetched material's own explicit caveats: (1) the severity-index range for a season (e.g., 3-4.5 for 2026) reflects uncertainty from "residual nutrients already in the lake, or competition from other algal species"; (2) bloom duration/persistence "depends on the frequency of high winds in September, which can't be predicted this far in advance," i.e., a known driver the forecast cannot resolve at seasonal lead time; (3) the current-conditions/position layer depends on availability of "the most recent satellite image," implying gaps from cloud cover or revisit timing can limit inputs; (4) a 2025 satellite reprocessing introduced "new calibrations and improved algorithms," which is only mentioned in passing and not accompanied by a stated correction factor or comparability statement across pre-/post-reprocessing years. No quantitative accuracy or skill metric (e.g., RMSE, correlation coefficient, false-alarm/hit rate, confidence interval) for the severity forecast, the position forecast, or the mixing forecast was present in any of the fetched pages.

## Tensions with other findings
No direct contradiction with other HAB literature is stated in the source itself, but two internal inconsistencies across NOAA's own linked pages describing this one forecast system are worth flagging: (a) the bloom/forecast season window is "June until October" on the GLERL bulletin.html landing page but "July to October" on the directly-linked NCCOS forecast portal; (b) the in-season outlook horizon is "5-day outlooks" on bulletin.html but a "96 hours" (4-day) minimum on the NCCOS portal. These likely describe two layers of the same system (an emailed twice-weekly bulletin vs. a continuously/daily-updated online model tool) rather than a true contradiction, but the source text never reconciles them explicitly, so exact figures should be attributed to the specific page/product, not the system as a whole. More conceptually: this product's headline metric is a single seasonal "Severity Index" summarizing cumulative bloom biomass relative to the 2005 (min) and 2011 (max) reference seasons -- i.e., it answers "how bad will this whole season be," a different question from a short-horizon, location-specific early-warning signal. For anyone building a week-to-week risk/action-window tool (as this project intends), the closer analog in this source is the 5-day/96-hour bloom-position-and-concentration outlook, not the once-a-season Severity Index, and the two should not be conflated when citing "the NOAA forecast."

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Forecasts depend on satellite availability (stated in URL 2: 'Forecasts depend on satellite availability') — this operational constraint is not reflected in any of the claims, which present the forecast products as functioning products without noting that unavailability of satellite imagery would limit them.
- **Reviewer notes:** Nine of ten claims are fully supported by the source text with direct quotes and corroborating details. Claim 10 is substantially correct—all organizations and their roles are accurately listed per URL 3 and URL 2—but one minor naming detail diverges: the claim specifies 'NWS Ohio River Forecast Center' while the source texts state only 'Ohio River Forecast Center' without the NWS prefix. This does not rise to material error (NWS = National Weather Service is a real suffix, and the organization is clearly identified), but it technically adds information not present in the source. A significant operational caveat—that forecast accuracy depends on satellite data availability—is stated in URL 2 but is not mentioned in any claim. All numerical values (dates, indices, ranges, hours, timescales) are verified against the source. No hallucinated numbers. Recommendation: Overall assessment is 'pass' because no claims are unsupported and no numbers are fabricated; the partial claim and omitted caveat are minor."

## Provenance
- Canonical URL: https://www.glerl.noaa.gov/res/HABs_and_Hypoxia/bulletin.html
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Primary URL fetched twice with different prompts (a targeted-extraction prompt, then a request for verbatim/section-by-section reproduction); both returned materially consistent facts (May start, early-July seasonal forecast, June-October window, 5-day outlooks, twice-weekly updates), which is treated as internal cross-validation given that the WebFetch tool itself routes fetched HTML through an intermediate small summarizing model rather than returning raw markup -- flagged here per the project's transparency norms since I cannot independently re-verify the raw HTML myself with the tools available. To build the comprehensive picture the task requests (methods, models, numbers, limitations), I additionally fetched two pages directly hyperlinked from the primary bulletin.html page as its "main forecast portal" and as a linked news item: (1) https://coastalscience.noaa.gov/science-areas/habs/hab-forecasts/lake-erie/ (the NCCOS operational forecast portal bulletin.html points to) and (2) https://coastalscience.noaa.gov/news/moderate-harmful-algal-bloom-predicted-for-western-lake-erie-in-summer-2026/ (NOAA/NCCOS news release giving the concrete 2026 Severity Index value, its interpretation bands, partner list, and the two explicit uncertainty statements). These are treated as extensions of the same NOAA forecast-product ecosystem described by the primary page, not as a replacement source; all claims are tagged above with which specific page they came from. Category reassessed from provisional "models-and-methods" (confirmed: the page is fundamentally about applied forecast models/products) and relevance upgraded from provisional "Medium" to "High" because this is a close real-world operational precedent for exactly what the HAB_PoC brief asks for -- fusing an in-situ nutrient/river signal with a satellite (OLCI) signal into a severity readout and a short action-window outlook for a non-technical field/operations audience -- making it directly useful for framing both the Part A analysis and the Part B tool. No numeric hindcast-skill figures were found anywhere in the fetched text, which is itself a notable gap worth carrying into any comparison against this project's own validated baselines.
