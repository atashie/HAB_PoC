---
key: FED-067
title: NLDAS: North American Land Data Assimilation System
authors_or_org: Youlong Xia (SAIC at NASA Goddard Space Flight Center) and David M. Mocko (SAIC at NASA Goddard), Eds.; National Center for Atmospheric Research (NCAR) Climate Data Guide staff (page editors). Underlying NLDAS-2 system: NOAA/NCEP/EMC, NASA GSFC, Princeton University, NWS Office of Hydrological Development, University of Washington, and NCEP's Climate Prediction Center.
year: 2025 (Climate Data Guide page last modified 2025-12-11); primary NLDAS-2 methodology paper cited on the page is Xia et al. 2012
url: https://climatedataguide.ucar.edu/climate-data/nldas-north-american-land-data-assimilation-system
access_date: 2026-07-01
tier: FED
source_type: Web-based curated dataset guide entry (NCAR/UCAR Climate Data Guide), describing an operational government land-data-assimilation product (NASA/NOAA NLDAS-2)
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# NLDAS: North American Land Data Assimilation System

**What it is.** NLDAS (North American Land Data Assimilation System) is a system, described on NCAR/UCAR's Climate Data Guide, that fuses observation-based and model-reanalysis data into a long-term (1979-present), hourly, 1/8-degree-resolution gridded atmospheric forcing dataset over the continental U.S., southern Canada, and northern Mexico (25-53N), which is then used to drive four offline land-surface/hydrological models (NASA Mosaic, NOAA Noah, NWS SAC, and Community VIC in energy mode).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** NLDAS integrates observation-based data and model reanalysis data to produce long-term hourly atmospheric forcing data, which is then used to drive offline (uncoupled) land-surface and/or hydrological models.
  - *evidence:* This is the page's own opening definitional statement of what the system is and does; stated directly, not derived from other evidence in the text. (Main content / opening overview paragraph)
  - *quote:* "The North American Land Data Assimilation System (NLDAS) integrates a large quantity of observation-based and model reanalysis data to produce long-term hourly atmospheric forcing data, and then uses this meteorological data to drive offline (not coupled to the atmosphere) land-surface and/or hydrological models."
- **[✓ verified]** The NLDAS forcing grid has 1/8th-degree (~0.125°) spatial resolution and covers the continental United States, southern Canada, and northern Mexico between 25 and 53 degrees North latitude.
  - *evidence:* Stated directly as the spatial resolution/coverage specification of the dataset. (Spatial Resolution / Spatial Coverage description)
  - *quote:* "1/8th-degree grid spacing over the continental United States, southern Canada, and northern Mexico (25-53 North)"
- **[✓ verified]** The dataset spans 1979 to the present at hourly time steps and is delivered operationally with roughly a 4-day latency behind real time.
  - *evidence:* Stated directly as temporal coverage/latency and corroborated by a figure caption showing an hourly time series running from 1979 through May 2023. (Temporal Coverage field; Key Strengths bullet; Figure 6 caption)
  - *quote:* "Stable near real-time operational product with 4-day latency and an available long-term archive"
- **[✓ verified]** NLDAS-2 forcing data is used to drive four offline land-surface/hydrological models: NASA's Mosaic, NOAA's Noah, the NWS SAC hydrological model, and the Community VIC model run in energy mode.
  - *evidence:* Listed as the four component models whose outputs are produced from the shared forcing dataset; corroborated by the Key Strengths bullet referencing 'four-model outputs' and by four separate figure captions (Figs 2-5) each illustrating one of these models' output. (Models & Components description; Key Strengths bullet; Figures 2-5 captions)
  - *quote:* "Long-term (1979-present) moderate-high spatial resolution hourly data of surface meteorological forcing and four-model outputs"
- **[✓ verified]** The NLDAS forcing dataset provides seven surface meteorological variables: precipitation, 2-m air temperature, 2-m air humidity, downward shortwave radiation, downward longwave radiation, 10-m wind speed, and surface pressure.
  - *evidence:* Listed directly as the forcing variable set, and independently corroborated in a comparison sentence stating NLDAS has 'all seven surface meteorological variables' versus PRISM's precipitation-only content. (Forcing Data Variables description; comparison-to-PRISM/Daymet sentence)
  - *quote:* "NLDAS includes all seven surface meteorological variables needed to drive land/hydrological models but PRISM only includes precipitation"
- **[✓ verified]** The source asserts, as a stated strength, that NLDAS data products have been evaluated and validated against various observations and are widely used in the meteorology and hydrology community.
  - *evidence:* This is a self-assessment / summary claim made by the page itself; no specific validation statistics, comparison datasets, or numeric skill scores are given on the page to substantiate it, so it should be read as an unelaborated claim of the source rather than an independently verifiable result. (Key Strengths bullet list)
  - *quote:* "Data products were well-evaluated and validated against various observations and are widely used in the meteorology and hydrology community"
- **[✓ verified]** The source documents several specific, named precipitation-forcing problems: spurious precipitation along the Canadian side of the U.S.-Canada border in many years, occasional artificial 'dry spots' from gauge quality-control issues that dry out modeled soil moisture, a discontinuity in precipitation behavior after 1 January 2012 caused by switching input precipitation datasets, and an anomalously high, localized precipitation artifact in Texas and the southeastern U.S. in July-August 2008.
  - *evidence:* These are listed by the source as the primary known data-quality caveats/limitations of the product, stated as observed issues rather than as a general disclaimer. (Key Limitations / Expert Guidance caveats list)
  - *quote:* "Changes in the behavior of precipitation after 01 January 2012 due to a change in the use of precipitation from US-Mexico precipitation dataset to global precipitation dataset"
- **[✓ verified]** The source explicitly cautions that, because of its operational nature, not all known issues in NLDAS-2 can be resolved and the datasets re-generated, and that NLDAS is not intended to be used as an independent dataset for monitoring climate variability and change.
  - *evidence:* Stated directly as an intended-use caveat/limitation of the product, i.e., a scope boundary set by the source itself. (Key Limitations list)
  - *quote:* "As it is designed for modeling applications, NLDAS is not intended to be used as an independent dataset for monitoring climate variability and change"
- **[✓ verified]** The source contrasts NLDAS with PRISM and Daymet, noting NLDAS is an hourly product whereas PRISM/Daymet are monthly or daily products.
  - *evidence:* Direct comparative statement made in the page's discussion of related/comparable datasets. (Comparison-to-related-products discussion)
  - *quote:* "NLDAS is hourly product but the PRISM/Daymet is either monthly or daily product"
- **[✓ verified]** The primary methodological reference for NLDAS-2 is a 2012 paper describing continental-scale water and energy flux analysis and validation, including intercomparison and application of the model products.
  - *evidence:* Given as the citation users are directed to use for the NLDAS-2 project/method, i.e., the paper underlying the system's validation approach. (Citation / References)
  - *quote:* "Xia, Y., K. Mitchell, M. Ek, et al., 2012a: Continental-scale water and energy flux analysis and validation for the North American Land Data Assimilation System project phase 2 (NLDAS-2): 1. Intercomparison and application of model products. J. Geophys. Res., 117, D03109"

## Data / numbers
- Spatial resolution: 1/8th-degree (~0.125°) grid spacing
- Spatial domain: continental United States, southern Canada, and northern Mexico, 25-53° North latitude
- Temporal resolution: hourly
- Temporal coverage: 1979 to present, with an example time series shown from 13Z 01 Jan 1979 to 12Z May 2023
- Operational latency: ~4-day latency behind real time
- 7 surface meteorological forcing variables: precipitation, 2-m air temperature, 2-m air humidity, downward shortwave radiation, downward longwave radiation, 10-m wind speed, surface pressure
- 4 land-surface/hydrological models driven by the forcing data: NASA Mosaic, NOAA Noah, NWS SAC, and Community VIC (in energy mode)
- Precipitation annual climatology example period: 1981-2020 (Figure 1 caption)
- Example grid point in Figure 6: 33.9375° North, -86.9375° West
- Soil moisture example depth: top 1-meter (Mosaic model, Figure 3, 00Z 15 Aug 2002)
- Precipitation input dataset change date: 01 January 2012 (switch from US-Mexico precipitation dataset to a global precipitation dataset)
- Documented anomalous precipitation artifact: Texas and southeastern U.S., July-August 2008
- Primary methodological citation: Xia et al. 2012a, J. Geophys. Res., 117, D03109
- Page last modified: 2025-12-11 (per citation block)

## Methods
NLDAS-2 does not collect new field observations itself; it fuses existing observation-based products (e.g., gauge-based precipitation analyses, reanalysis fields) into a common hourly, 1/8-degree gridded atmospheric forcing dataset (precipitation, 2-m air temperature, 2-m air humidity, downward shortwave and longwave radiation, 10-m wind speed, surface pressure) over CONUS, southern Canada, and northern Mexico (25-53N), 1979-present. That shared forcing dataset is then used to run four offline (not atmosphere-coupled) land-surface/hydrological models - NASA's Mosaic, NOAA's Noah, the NWS SAC hydrological model, and the Community VIC model (energy mode) - producing derived fields such as soil moisture, snow cover, and evapotranspiration (illustrated in Figures 3-5). Per the source, the forcing/model products have been "well-evaluated and validated against various observations" and are delivered as a stable, near-real-time operational product (~4-day latency) with a long-term archive, developed through a multi-institution partnership (NOAA/NCEP/EMC, NASA GSFC, Princeton University, NWS Office of Hydrological Development, University of Washington, NCEP Climate Prediction Center). Where the source says it works well: long-term, moderate-high resolution, hourly, operationally stable, and widely adopted in the meteorology/hydrology community. Where the source says it fails or should not be used: precipitation forcing has multiple documented artifacts (Canada-border spurious precipitation, gauge-QC "dry spots," a 2012-01-01 input-dataset-driven discontinuity, and a 2008 TX/Southeast US anomalous spike), the operational system cannot retroactively resolve/regenerate all known issues, and the product is explicitly not intended as a standalone climate-variability/trend-monitoring dataset. Data are distributed via NASA GSFC holdings/the NLDAS homepage (with README documentation) and, for near-real-time products, via NCEP Central Operations in GRIB-2 format; no explicit DOI string, gauge-station count, or grid-cell count was found on the page despite specifically checking for these.

## Stated limitations
The source states multiple, mostly precipitation-related, known issues: (1) unrealistic/spurious precipitation along the Canadian side of the U.S.-Canada border in many years; (2) occasional artificial "dry spots" in precipitation caused by gauge quality-control issues, which in turn produce unrealistically dry modeled soil moisture; (3) a discontinuity in precipitation behavior after 1 January 2012, caused by switching the input precipitation dataset from a US-Mexico product to a global product; (4) an unrealistically high, spatially localized precipitation artifact in Texas and the southeastern U.S. during July-August 2008. Beyond precipitation-specific issues, the source states that because NLDAS-2 is run operationally, "it is not possible to resolve all the known issues and re-generate datasets," and that the product, being designed for modeling applications, "is not intended to be used as an independent dataset for monitoring climate variability and change." No quantitative validation statistics (e.g., RMSE, bias, correlation against station data) are given on the page to substantiate the general "well-evaluated and validated" claim; that claim is presented without supporting figures in the fetched text.

## Tensions with other findings
Two tensions with a HAB-fusion use case are evident directly from the source's own caveats, stated cautiously and without asserting causation beyond what the source says: (1) The source explicitly warns NLDAS is "not intended to be used as an independent dataset for monitoring climate variability and change," yet a HAB-driver analysis fusing NLDAS temperature/precipitation time series with satellite bloom signals to infer long-term warming or wetting trends would be exactly this kind of use; the documented 1-January-2012 precipitation-input discontinuity is a concrete, source-stated mechanism by which an apparent "trend break" in an NLDAS series could be an artifact of input-dataset switching rather than a real hydroclimatic signal - a confound that would need to be checked before attributing any bloom-driver shift to a climate signal. (2) Precipitation is repeatedly singled out by the source as the most error-prone NLDAS variable (border artifacts, gauge-QC dry spots, the 2008 TX/Southeast US spike, the 2012 discontinuity), yet precipitation-driven nutrient/runoff loading is often the mechanistic link researchers draw between weather and HAB nutrient supply; using NLDAS precipitation as a trusted proxy for runoff-driven nutrient loading in a HAB model should be treated with the same caution the source applies to the variable itself. No statement in the fetched text directly addresses HABs, cyanobacteria, or water-quality variables, so any link between NLDAS and bloom dynamics is an inference by the reviewer, not a claim made by the source.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All ten claims are directly supported by verbatim or near-verbatim text in the source. No hallucinated numbers; all dates, parameters, and quantities (spatial/temporal resolution, model count, variable count, latency, latitude bounds) are present in the source text. All major caveats mentioned in the source (operational constraints, precipitation issues, climate-monitoring unsuitability) are captured in the extracted claims. The claims accurately represent both the definitional core and the documented limitations of NLDAS."

## Provenance
- Canonical URL: https://climatedataguide.ucar.edu/climate-data/nldas-north-american-land-data-assimilation-system
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary Climate Data Guide URL successfully with WebFetch; no redirect occurred (url_used = resolved_url = primary URL given). Because a single WebFetch pass risked losing exact wording, I issued four WebFetch calls against the same URL with progressively narrower prompts (general comprehensive extraction; verbatim strengths/limitations/references; verbatim summary/strengths/limitations/citation/version notes; metadata-table fields and figure captions) to triangulate verbatim quotes versus paraphrase and to check for a formal metadata table, DOI string, gauge/grid-cell counts, and spin-up description. The page does not appear to expose a structured metadata sidebar (Type of Data / Ease of Access / DOI fields) to the fetch tool, an explicit DOI identifier string, gauge-station or grid-cell counts, or spin-up/initialization language - these were explicitly checked for and are recorded as absent rather than assumed. Two passes gave slightly different end-dates for the record ('May 2023' vs '2023-08' in one pass); I treat the figure-6-caption-anchored value ('12Z May 2023') as the more reliable verbatim data point since it was tied to a specific, repeatedly consistent figure caption, and flag the other value as a likely summarization artifact rather than asserting it. One pass rendered a strength bullet as '...validated again various observations...' (apparent typo for 'against') versus another pass's '...validated against various observations...'; both are noted, treated as the same underlying claim. No number in this dossier was taken from prior/training knowledge - only from the fetched page text.
