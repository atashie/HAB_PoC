---
key: ACAD-054
title: Gridded Surface Meteorological (gridMET) Dataset
authors_or_org: John Abatzoglou (dataset creator); University of Idaho — Climatology Lab (gridMET / METDATA project host)
year: 2013 (Abatzoglou methods/validation paper); dataset itself spans 1979-present and is continuously updated
url: https://www.climatologylab.org/gridmet.html
access_date: 2026-07-01
tier: ACAD
source_type: Dataset documentation / project landing page (Climatology Lab, University of Idaho), referencing an associated peer-reviewed methods paper
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Gridded Surface Meteorological (gridMET) Dataset

**What it is.** gridMET is a publicly available, daily gridded surface meteorological dataset at ~4-km (1/24th degree) resolution covering the contiguous United States from 1979 to the present (updated daily), produced by the University of Idaho's Climatology Lab (creator: John Abatzoglou) by blending PRISM's spatial climate patterns with NLDAS-2 regional reanalysis's temporal attributes via "climatically aided interpolation."

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** gridMET is a daily, ~4-km (1/24th degree) resolution gridded surface meteorological dataset covering the contiguous US from 1979 through the present, updated daily.
  - *evidence:* Directly stated in the page's dataset overview/description. (Dataset overview section, climatologylab.org/gridmet.html)
  - *quote:* "a dataset of daily high-spatial resolution (~4-km, 1/24th degree) surface meteorological data covering the contiguous US from 1979-yesterday"
- **[✓ verified]** gridMET is produced by 'climatically aided interpolation' that blends PRISM's spatial climate patterns with NLDAS-2 regional reanalysis's temporal attributes and additional variables.
  - *evidence:* Explicit methodology statement on the page describing how the two input products are combined. (Methodology section)
  - *quote:* "blends spatial attributes of gridded climate data from PRISM with desirable temporal attributes (and additional variables) from regional reanalysis (NLDAS-2) using climatically aided interpolation"
- **[✓ verified]** The dataset provides core variables (max/min temperature, precipitation, downward shortwave radiation, wind velocity, max/min relative humidity, specific humidity) plus derived products including reference evapotranspiration, fire-danger indices, dead fuel moisture, vapor pressure deficit, and a drought index.
  - *evidence:* Direct variable listing given on the page under primary and derived variables. (Variables section)
  - *quote:* "Reference evapotranspiration (ASCE Penman-Montieth)"
- **[✓ verified]** The dataset's construction methods were validated against multiple independent weather-station networks and published in a peer-reviewed paper (Abatzoglou 2013).
  - *evidence:* Page states the validation networks used and cites the methods paper. (Citation / validation section)
  - *quote:* "Validation of the resulting gridded surface meteorological data was conducted against an extensive network of weather stations including RAWS, AgriMet, AgWeatherNet and USHCN-2."
- **[✓ verified]** gridMET cannot resolve microclimates finer than its ~4-km native grid, and its wind and solar radiation fields are limited by the coarser 32-km resolution of the NARR/NLDAS-2 inputs they are interpolated from.
  - *evidence:* Stated directly as a known limitation of the spatial methodology. (Known issues & limitations section)
  - *quote:* "gridMET will likely not capture microclimates that arise at spatial scales finer than the native resolution of the grid or parent datasets (<4-km)"
- **[✓ verified]** Because its NLDAS-2 precipitation input contains inhomogeneities from changing data sources over time, gridMET should not be used to infer trends in precipitation intensity or frequency.
  - *evidence:* Explicit caveat on the page cautioning against a specific downstream use. (Known caveats section)
  - *quote:* "The primary input dataset for daily precipitation (NLDAS-2) contains inhomogeneities due to changes in data sources through time"
- **[✓ verified]** Data for the most recent 60 days are preliminary and subject to revision, since they are initially filled with near-real-time proxies (CFSv2 anomalies for temperature/wind/humidity/radiation; National Water Prediction Service QPE for precipitation) pending final PRISM/NLDAS-2 values.
  - *evidence:* Directly stated data-recency caveat combined with the near-real-time update methodology description. (Near real-time updates / data caveat section)
  - *quote:* "Data for dates within the last 60 days are considered preliminary and subject to change"
- **[⚠ partial]** gridMET defines its daily time step as midnight-to-midnight Mountain Standard Time (7 UTC), a non-default convention relevant to aligning it with other time-referenced datasets.
  - *evidence:* Stated as a technical/known-issue detail on the page. (Known issues section)
  - *quote:* "gridMET nominally considers a 'day' to be midnight-to-midnight Mountain Standard Time (7 UTC)"
  - *reviewer:* Time definition is stated in source, but characterizations as 'non-default convention' and 'relevant to aligning with other time-referenced datasets' are not explicitly supported by the source text.
- **[✓ verified]** NLDAS-2-derived downward shortwave radiation (one of gridMET's inputs) has a documented positive bias over much of North America, and gridMET's own solar radiation is not corrected for topographic shading.
  - *evidence:* Stated as a known caveat about the radiation variable. (Known caveats section)
  - *quote:* "NLDAS2 downward shortwave radiation shows a positive bias over much of North America"
- **[✓ verified]** The dataset (also called METDATA) is distributed as public-domain (CC0) NetCDF4 files via direct download, THREDDS/OPeNDAP, and web tools such as ClimateEngine.org and the USGS Geo Data Portal (zarr format).
  - *evidence:* Access-link listing and licensing statement on the page. (File formats & copyright / data access links sections)
  - *quote:* "To the extent possible under law, John Abatzoglou has waived all copyright and related or neighboring rights to gridMET"

## Data / numbers
- Spatial resolution: ~4-km, 1/24th degree
- Temporal coverage: 1979 to present ('1979-yesterday'), updated daily
- Data within the most recent 60 days flagged as preliminary/provisional and subject to change
- Wind and solar radiation inputs interpolated from NARR/NLDAS-2 at native 32-km resolution
- PRISM climatological baseline used for anomaly construction: 1981-2010 averages (with anomaly period referenced as 2011-2017 in the near-real-time methodology text)
- Primary methods/validation citation: Abatzoglou, J.T. (2013), International Journal of Climatology, vol. 33, pp. 121-131, DOI 10.1002/joc.3413
- Funding: NSF Idaho EPSCoR award EPS-0814387; USDA National Institute for Food and Agriculture competitive grant award 2011-68002-30191
- File format changed to NETCDF4 (HDF5 model) as of August 2019
- Grid centroid offset of ~400 m corrected in May 2018 update; latitude dimension made monotonically increasing
- September 2024 correction: data for 2023-02-19, 2024-08-16 and 2022-02-27 reprocessed; 2022-08-01 to 2024-03-01 recomputed after an NLDAS2 bug was found
- Reference alfalfa evapotranspiration and vapor pressure deficit variables added January 2018
- 'Day' defined as midnight-to-midnight Mountain Standard Time (7 UTC)

## Methods
gridMET's core method is "climatically aided interpolation": daily temperature and precipitation anomalies are computed from PRISM (which supplies fine-scale spatial climate patterns) and superposed onto reanalysis-derived fields, while NLDAS-2 regional reanalysis supplies temporal structure and additional variables (wind, humidity, solar radiation) at the native ~4-km grid. For near-real-time days, before final PRISM/NLDAS-2 inputs are available, temperature is updated using Climate Forecast System v2 (CFSv2) anomalies, precipitation uses National Water Prediction Service QPE, and wind/humidity/solar-radiation anomalies from CFSv2 fill the gap until replaced by NLDAS-2 once available; anomalies are referenced to a shared PRISM 1981-2010 baseline for consistency. Per the page, the resulting gridded fields were validated against independent station networks (RAWS, AgriMet, AgWeatherNet, USHCN-2) in the cited Abatzoglou (2013, Int. J. Climatol.) paper. The method works at ~4-km for temperature/precipitation-derived fields but is explicitly described as inadequate below its own grid scale, and for wind/solar radiation is constrained by the coarser 32-km resolution of its NARR/NLDAS-2 source data; the page also flags that the precipitation input is not homogeneous through time, so it should not be used to study precipitation trend/frequency changes.

## Stated limitations
The page itself states: (1) gridMET cannot resolve microclimates finer than its ~4-km native grid or parent-dataset resolution; (2) wind and solar-radiation fields are interpolated from NARR/NLDAS-2 at only 32-km native resolution, insufficient to capture terrain-driven mesoscale wind effects; (3) solar radiation is not adjusted for topographic shading and is provided for a planar surface; (4) the NLDAS-2 precipitation input contains inhomogeneities from changing data sources through time, so gridMET should not be used to infer trends in precipitation intensity or frequency; (5) NLDAS-2 downward shortwave radiation carries a positive bias over much of North America per cited external studies; (6) data within the most recent 60 days are preliminary/provisional and subject to revision; (7) the dataset's "day" is defined as midnight-to-midnight Mountain Standard Time (7 UTC), a non-obvious convention for date alignment with other sources; (8) periodic reprocessing has been needed for specific dates/ranges due to upstream (NLDAS2) bugs.

## Tensions with other findings
gridMET is a weather-forcing/covariate dataset, not a bloom, chlorophyll, or toxin observation, so it does not itself confirm or contradict HAB findings -- its role in a HAB study is as an explanatory driver layer (temperature, precipitation, wind, radiation, evapotranspiration, drought index) to fuse with satellite/in-situ bloom signals, and any driver relationship built from it would be correlational unless paired with mechanistic or experimental evidence. Two documented properties create friction with common HAB-driver framings: (1) the page's own caution against using gridMET precipitation to infer intensity/frequency trends is in tension with any analysis that wants to attribute changing bloom frequency to changing storm/precipitation patterns over time -- that specific inference is flagged as unsupported by the source itself; (2) gridMET's wind and solar-radiation fields are ultimately bounded by NLDAS-2/NARR's coarser 32-km input resolution, which is much coarser than the ~4-km gridMET grid and far coarser than typical satellite HAB pixel sizes (e.g., ~300 m Sentinel-3 OLCI used by EPA CyAN), so lake-scale wind-driven mixing/bloom-transport dynamics may be under-resolved when fusing gridMET wind/radiation with fine-resolution satellite HAB imagery -- a resolution-mismatch caveat worth flagging in any fusion pipeline.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Files contain scale_factor and offset requiring consideration when reading
  - Recent Data Corrections (September 2024): Data for 2023-02-19, 2024-08-16, and 2022-02-27 were reprocessed; gridMET recomputed 2022-08-01 to 2024-03-01 incorporating new NLDAS2 hourly data
  - Grid adjustments (May 2018): Latitude dimension increases monotonically; ~400m offset corrected in reported centroid
  - Coverage extends to southern British Columbia in real-time products (beyond contiguous US)
- **Reviewer notes:** One claim (8) adds interpretive characterizations not present in the source text. The dropped caveats are technical implementation details and geographic/temporal qualifications important to data users. All core facts are well-supported; no numerical hallucinations detected."

## Provenance
- Canonical URL: https://www.climatologylab.org/gridmet.html
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Both WebFetch calls against the primary URL (https://www.climatologylab.org/gridmet.html) succeeded fully and returned rich, mutually consistent content (no blocking, no binary/garbage content, no redirect reported), so no WebSearch fallback was needed and resolved_url equals the primary URL. The two fetches used different extraction prompts (one focused on dataset overview/variables/methods/citation/limitations; the other on access links, source-input integration, validation, and technical/licensing detail) and were reconciled/unioned into the fields below - overlapping facts (resolution, coverage, variables, methodology, limitations) were cross-confirmed verbatim across both calls, increasing confidence they are faithful to the page rather than a fetch-model artifact. One ambiguity: the page is a continuously-updated dataset landing page rather than a dated paper, so 'year' is reported as the primary methods paper's year (2013) plus the dataset's rolling 1979-present coverage, per the page text itself. No numeric validation statistics (e.g., RMSE/bias magnitudes against station networks) were present in either fetch's extracted text, only the qualitative statement that validation against RAWS/AgriMet/AgWeatherNet/USHCN-2 was performed and is documented in the cited 2013 paper - so no such numbers are claimed here.
