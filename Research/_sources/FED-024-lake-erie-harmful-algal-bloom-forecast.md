---
key: FED-024
title: Lake Erie Harmful Algal Bloom Forecast
authors_or_org: NOAA National Centers for Coastal Ocean Science (NCCOS), with Ohio Sea Grant (co-host of seasonal announcement), and cited relationships to Ohio EPA, Ohio State University, Heidelberg University National Center for Water Quality Research, and NOAA GLERL
year: 2026
url: https://coastalscience.noaa.gov/science-areas/habs/hab-forecasts/lake-erie/
access_date: 2026-07-01
tier: FED
source_type: Government agency operational science/decision-support webpage (NOAA NCCOS program page)
categories: [models-and-methods, remote-sensing]
relevance: High
full_text_access: full
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Lake Erie Harmful Algal Bloom Forecast

**What it is.** NOAA NCCOS's operational Lake Erie page bundling several linked cyanobacterial-HAB decision products for western Lake Erie: a seasonal (July–October) bloom-severity outlook and Severity Index, pre-season weekly severity projections, and near-real-time (≥96-hour) bloom position and vertical-mixing forecasts, built by fusing satellite imagery, a hydrodynamic/mixing model, river-discharge and nutrient-load data, and field toxicity sampling.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** NOAA issues seasonal forecasts for cyanobacteria (blue-green algae) blooms in Lake Erie, framed around the July–October window when warm water favors blooms.
  - *evidence:* Stated directly as the page's framing/purpose statement, returned verbatim in the targeted verbatim-quote fetch pass and paraphrased consistently in the other two passes. (Page overview/intro section)
  - *quote:* "NOAA provides forecasts for seasonal blooms of cyanobacteria (blue-green algae) in Lake Erie, typically from July to October when warmer water creates favorable bloom conditions."
- **[✓ verified]** The forecast's Severity Index (SI) is defined as bloom biomass integrated over a sustained 30-day period, normalized to the historically lowest (2005) and highest (2011, 'to date') observed bloom-biomass years.
  - *evidence:* Definition returned as an exact quote in the verbatim-focused fetch pass; the other two passes independently paraphrased the same 2005-minimum/2011-maximum calibration and 30-day biomass basis, so the core definition is corroborated across all three passes. (Page section describing the Severity Index)
  - *quote:* "The SI is based on the quantity (biomass) of the bloom over a sustained 30 day period and is scaled to the minimum observed bloom biomass (2005) and maximum observed bloom biomass (2011) to date."
- **[✓ verified]** A bloom position/extent forecast product provides a minimum 96-hour forecast lead time, generated from hydrodynamic modeled currents combined with satellite imagery used to fix the initial bloom location.
  - *evidence:* Exact wording returned in the verbatim-quote fetch pass; both other passes independently reported the same '96 hours' minimum horizon and the hydrodynamic-model-plus-satellite-imagery method. (Page section describing the Bloom Position Forecast product)
  - *quote:* "Forecasted extent and position of the bloom for a minimum of 96 hours, based on a combination of a hydrodynamic modeled currents and satellite imagery for initial bloom location."
- **[✓ verified]** A companion vertical-mixing forecast, over the same minimum ~96-hour window, estimates the likelihood the bloom is at the surface versus subsurface.
  - *evidence:* Exact wording returned in the verbatim-quote fetch pass; corroborated by the other two passes describing a 'vertical mixing forecast' with a 96-hour-plus horizon. (Page section describing the Vertical Mixing Forecast product)
  - *quote:* "Forecast of the potential for mixing over the next at least 96 hours, to determine the likelihood that the bloom is at the surface or subsurface."
- **[✓ verified]** Ahead of the full seasonal severity forecast, NOAA issues weekly 'early season' bloom-severity projections (starting in May) that are driven by Maumee River discharge and modeled phosphorus loads.
  - *evidence:* Driver description ('Maumee River discharge and modeled phosphorus loads') returned verbatim; weekly-from-May cadence reported consistently in the other two extraction passes. (Page section describing the Early Season Projection)
  - *quote:* "The early season projection estimates bloom severity based on Maumee River discharge and modeled phosphorus loads."
- **[✓ verified]** The 2026 western Lake Erie seasonal HAB forecast was announced June 25, and the immediately preceding (2025) forecast season's operational window ran through November 19, 2025.
  - *evidence:* Both dates returned as exact strings in the verbatim-quote fetch pass; the June 25 announcement (via live webinar) and the November 19, 2025 season-end date were each independently reported in the other two passes as well. (Page section on seasonal forecast announcement / forecast-season dates)
  - *quote:* "The 2026 Western Lake Erie HAB seasonal forecast was issued on June 25th" / "11/19/2025 is the final day of the 2025 Lake Erie HAB forecast season."
- **[✓ verified]** The program is run by NOAA NCCOS, with Ohio Sea Grant named as the partner that co-hosts the live seasonal-forecast announcement webinar; Ohio EPA, Ohio State University, and Heidelberg University's National Center for Water Quality Research are also named in connection with the program.
  - *evidence:* NCCOS as operator and Ohio Sea Grant as webinar co-host reported in the first extraction pass; the second, independently-prompted pass returned the same core partner list (Ohio Sea Grant, Ohio EPA, Ohio State University, Heidelberg University, NOAA GLERL) without being shown the first pass's answer, so the partner list is corroborated across two independent passes. (Partners/attribution section of the page)
- **[✓ verified]** The forecast system fuses multiple data streams: satellite imagery (OLCI and true-color) for bloom location/extent, hydrodynamic/mixing model output, Maumee River discharge and modeled phosphorus loads, and field-collected toxicity measurements.
  - *evidence:* Synthesized from the first pass's itemized 'Data Sources and Models' list plus the third pass's verbatim descriptions of the position, mixing, and early-season-projection products, which each name a subset of these same inputs. (Distributed across the Data Sources/Models overview and the individual product-description sections)
- **[✓ verified]** No explicit statement of forecast accuracy, uncertainty, skill score, or an itemized list of what the forecast cannot predict was recoverable from the page text, despite a fetch pass specifically targeted at finding such wording.
  - *evidence:* The third, verbatim-targeted extraction pass returned 'No explicit text found addressing forecast limitations or uncertainty' in response to a direct request for that content; the first pass reached the same conclusion independently ('The page does not explicitly state forecast accuracy limitations or skill scores'). (Absence noted across the whole page (no dedicated limitations section found))
- **[✓ verified]** One extraction pass (not corroborated by the other two) reported that satellite data underlying the severity time series was reprocessed after the 2024 bloom with new calibrations, and separately described a 20-meter-resolution 'Demonstration Great Lakes HAB Monitoring' weekly imagery product for Maumee Bay.
  - *evidence:* Both details appeared only in the first extraction pass; the second and third passes, run with different prompts, did not surface either the 2024-reprocessing note or the '20m' figure, so this claim is flagged as lower-confidence/single-source-pass and reported here only as such rather than as a fully corroborated fact. (First fetch pass only: 'Limitations' and 'Related NOAA Products' subsections)

## Data / numbers
- 96 hours — minimum forecast lead time for both the bloom position/extent forecast and the vertical-mixing forecast
- 30-day period — sustained window over which bloom biomass is integrated to compute the Severity Index
- 2005 — calibration year used as the Severity Index scale's minimum observed bloom biomass
- 2011 — calibration year used as the Severity Index scale's maximum observed bloom biomass 'to date' (per source wording)
- June 25 — announcement date of the 2026 western Lake Erie seasonal HAB forecast
- 11/19/2025 — final day of the 2025 Lake Erie HAB forecast season
- 20 m — resolution cited for a 'Demonstration Great Lakes HAB Monitoring' weekly imagery product (single fetch-pass only, not corroborated — low confidence)

## Methods
Per the fetched page text: a weekly, pre-season 'early season projection' (issued from May) estimates bloom severity from Maumee River discharge and modeled phosphorus loads using statistical relationships built from a historical time series. The full seasonal forecast (announced June 25 via live webinar co-hosted with Ohio Sea Grant) expresses expected bloom severity via a Severity Index — bloom biomass integrated over a sustained 30-day period, scaled against the historical minimum (2005) and maximum ('to date', 2011) observed-biomass years. Separately, an operational near-term system produces daily-updated forecasts, each with a minimum 96-hour lead time, of (a) bloom position/extent, combining hydrodynamic modeled currents with satellite imagery (OLCI/true-color) for the initial bloom location, and (b) vertical mixing, i.e., the likelihood the bloom sits at the surface versus subsurface. Field sampling supplies toxicity measurements as a further, separate input. The fetched text does not state quantitative skill/validation metrics (e.g., hindcast accuracy, RMSE, hit rate) for either the seasonal SI forecast or the 96-hour position/mixing forecasts — no such figures were returned by any of the three extraction passes.

## Stated limitations
Across three separately-prompted extraction passes — including one pass explicitly asking for limitations/uncertainty language — no dedicated limitations, accuracy, or uncertainty statement was recoverable from the page text ('No explicit text found addressing forecast limitations or uncertainty'). The only limitation-adjacent details surfaced are implicit and, in one case, single-pass only: (1) the program's geographic scope is explicitly bounded to western Lake Erie/Maumee Bay, not the whole lake; (2) one (uncorroborated) extraction pass reported that satellite data feeding the severity time series was reprocessed after the 2024 bloom "with new calibrations and improved algorithms, generating a more consistent data set," which — if accurate — would imply pre- vs. post-reprocessing severity values may not be perfectly comparable; this detail should be treated as tentative since it did not appear in the other two passes. No statement was found on what the forecast does NOT predict (e.g., point-location toxin concentration, human-health risk thresholds, bloom duration).

## Tensions with other findings
Not directly evidenced against other sources within this task (only this one source was reviewed here). Two points are worth flagging for cross-source reconciliation later: (1) the Severity Index is normalized to a fixed historical calibration window (floor = 2005, ceiling = 2011 "to date" per the source's own wording) — the fetched text does not clarify how, or whether, the scale has been revised to accommodate any bloom years whose biomass may have exceeded the 2011 reference after that year, which matters for comparing SI values across the full 2000–2025 record the page references; (2) the page bundles three distinct predictive claims — seasonal bloom-size severity, short-term (96-hour) bloom position/mixing, and field-measured toxicity — that address different questions (how big vs. where vs. how toxic) and should not be conflated when this source is cited alongside literature that treats HAB 'severity' as a single unified metric.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All 10 claims are directly supported by the source text or explicitly confirmed as properly-qualified lower-confidence findings (claim 10). No hallucinated numbers detected—all numerical figures cited (96 hours, 30 days, 2005, 2011, July–October, May, June 25, 11/19/2025, 2026, 20m) appear verbatim or paraphrased in the source. No material caveats were dropped from claims. The analyst's evidence notes accurately reflect corroboration across multiple extraction passes where applicable, and claim 10 is transparently labeled as single-pass and uncorroborated by the other two passes, which the source text confirms."

## Provenance
- Canonical URL: https://coastalscience.noaa.gov/science-areas/habs/hab-forecasts/lake-erie/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: partial
- Fetch notes: Fetched the single primary URL three times with three differently-worded extraction prompts (two broad comprehensive-extraction prompts as required for a High-relevance source, plus a third pass specifically requesting verbatim, word-for-word quotations to firm up numbers/definitions for source_extract, since WebFetch renders pages through a small summarizing model that can drop or lightly paraphrase content between calls). No redirect occurred; url_used and resolved_url are identical to the primary URL given. Core facts were corroborated across at least two of the three independent passes: the Severity Index definition (30-day biomass window, 2005 min / 2011 max calibration), the 96-hour minimum lead time for both the bloom-position and vertical-mixing forecasts, the Maumee-River/phosphorus-driven weekly early-season projections, the June 25 (2026) seasonal-announcement date and the 11/19/2025 end of the 2025 season, NCCOS as the operating body, and the named partner list (Ohio Sea Grant, Ohio EPA, Ohio State University, Heidelberg University, NOAA GLERL). Two items appeared in only one of the three passes and are flagged as lower-confidence in the claims/data above: a post-2024-bloom satellite reprocessing note, and a '20 m' resolution figure for a separate demonstration imagery product. Despite a fetch pass specifically designed to surface limitations/uncertainty/accuracy language, none was found in the rendered page text — this is reported honestly as an absence rather than inferred. No year-by-year numeric Severity Index values (e.g., a rank/score for 2011, 2015, 2019, 2023, etc.) were recoverable via text extraction; these likely live in an embedded chart or a linked spreadsheet (one pass named a file "NOAA_NCCOS_2000to2025_Curated_LE_Annual_Severity.xlsx") that a text-rendering fetch cannot parse — this is the main reason fetch_status is marked "partial" rather than "ok," even though full_text_access to the page itself was not blocked in any way (marked "full"). No training/prior knowledge of NOAA's Lake Erie HAB program was used; every claim above traces only to the three fetch outputs quoted or paraphrased in key_claims and source_extract.
