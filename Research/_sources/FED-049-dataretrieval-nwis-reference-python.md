---
key: FED-049
title: dataretrieval.nwis reference (Python)
authors_or_org: U.S. Geological Survey (USGS) / doi-usgs GitHub organization (maintainers of the `dataretrieval` Python package)
year: 
url: https://doi-usgs.github.io/dataretrieval-python/reference/nwis.html
access_date: 2026-07-01
tier: FED
source_type: Software documentation / API reference (Sphinx-generated, Read the Docs theme)
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# dataretrieval.nwis reference (Python)

**What it is.** This is the API reference page for the `dataretrieval.nwis` module of USGS's `dataretrieval` Python package — a set of wrapper functions for programmatically downloading hydrologic and water-quality data (instantaneous values, daily values, site metadata, discharge peaks, rating tables, statistics) from the USGS National Water Information System (NWIS, waterdata.usgs.gov/nwis) web services. It is software/API documentation, not a scientific study.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The dataretrieval.nwis module provides Python functions for downloading data from the USGS National Water Information System (NWIS) web services.
  - *evidence:* Stated directly in the module overview describing the module's purpose and the NWIS site it wraps. (Module Overview section)
  - *quote:* "The `dataretrieval.nwis` module provides functions for downloading data from the National Water Information System (NWIS) at https://waterdata.usgs.gov/nwis."
- **[✓ verified]** get_iv() retrieves instantaneous-values time series for one or more USGS sites over a start/end date range (YYYY-MM-DD), returning a DataFrame plus an NWIS_Metadata object.
  - *evidence:* Documented function purpose, signature, and parameter/return types. (get_iv() section)
  - *quote:* "Retrieve instantaneous values data from NWIS ... start (string): Start date in format YYYY-MM-DD"
- **[✓ verified]** For get_iv(), get_dv(), and get_record(), if no start or end date is supplied, the service returns only the single most recent record rather than a full history.
  - *evidence:* This exact note is repeated under three separate functions and again in the page's summary limitations list, indicating it is a documented, load-bearing default behavior rather than an incidental remark. (get_iv(), get_dv(), get_record() sections; also 'Key Notes & Limitations' item 2)
  - *quote:* "If no start or end date are provided, only the most recent record is returned."
- **[✓ verified]** get_ratings() retrieves the rating table (stage-discharge relationship) for an active USGS streamgage and supports three table formats via the file_type parameter: 'base' (default), 'corr', or 'exsa'.
  - *evidence:* Given in the function's documented parameter list. (get_ratings() section)
  - *quote:* "file_type (string): "base", "corr", or "exsa"; default "base""
- **[✓ verified]** get_stats() supports statReportType values of 'daily' (default), 'monthly', or 'annual', and statTypeCd values of 'all', 'mean', 'max', 'min', 'median', per USGS's water-services statistics documentation.
  - *evidence:* Given as keyword-argument documentation with an explicit link out to the USGS statistics-service details page. (get_stats() section)
  - *quote:* "statReportType (string): "daily" (default), "monthly", or "annual" ... statTypeCd (string): "all", "mean", "max", "min", "median""
- **[✓ verified]** get_info() site searches via bounding box (bBox) are constrained so that the product of the latitude range and longitude range cannot exceed 25 degrees, and the function requires at least one major search parameter.
  - *evidence:* Stated directly as a function note and as a bBox parameter constraint. (get_info() section)
  - *quote:* "Must specify one major parameter. ... bBox (string or list): west longitude, south latitude, east longitude, north latitude (comma-separated); product of latitude/longitude range cannot exceed 25 degrees"
- **[✓ verified]** Geographic filters for get_info()/what_sites() include stateCd (a 2-digit state code, limited to one per request) and huc (hydrologic unit codes: one major 2-digit HUC or up to ten minor HUCs), plus countyCd as a 5-digit FIPS-based code.
  - *evidence:* Listed among get_info()'s documented keyword arguments. (get_info() section, Keyword Arguments)
  - *quote:* "stateCd (string): U.S. postal service 2-digit state code; only 1 per request ... huc (string or list): Hydrologic unit codes; 1 major (2 digits) or up to 10 minor HUCs ... countyCd (string or list): 5-digit county codes (FIPS State Code + county)"
- **[✓ verified]** get_record() is a universal wrapper across NWIS service types, dispatched by a `service` parameter (default 'iv'), with 'iv', 'dv', 'site', 'peaks', 'ratings', and 'stat' currently functional, while 'measurements', 'gwlevels', 'pmcodes', and 'water_use' are marked defunct even within this universal function.
  - *evidence:* Enumerated explicitly in the Service Types list under get_record(). (get_record() section, Service Types)
  - *quote:* "'measurements': (defunct—use waterdata.get_field_measurements()) ... 'gwlevels': (defunct—use waterdata.get_continuous(), waterdata.get_daily(), or waterdata.get_field_measurements()) ... 'pmcodes': (defunct—use waterdata.get_reference_table()) ... 'water_use': (defunct—no replacement available)"
- **[✓ verified]** Five legacy retrieval functions — get_discharge_measurements(), get_gwlevels(), get_pmcodes(), get_qwdata(), and get_water_use() — are now defunct and raise errors pointing to replacement functions, mostly in a separate `waterdata` module.
  - *evidence:* Each function is listed individually with a 'Status: Defunct' / 'Replacement:' entry in a dedicated deprecated-functions section. ('Deprecated Functions (Now NoReturn)' section)
  - *quote:* "get_qwdata() Status: Defunct Replacement: Use waterdata.get_samples()"
- **[✓ verified]** The legacy NWIS water-use web service was retired outright (not just the client-side wrapper), with modeled water-use estimates now served through a different USGS system, the National Water Availability Assessment Data Companion (NWDC).
  - *evidence:* Explicit prose note attached to the get_water_use() deprecation entry. (get_water_use() deprecation note)
  - *quote:* "The legacy NWIS water-use service has been retired. Modeled water-use estimates are now served by the National Water Availability Assessment Data Companion (NWDC)."
- **[✓ verified]** The documented package build is an in-development, pre-release version identifier rather than a fixed numbered release.
  - *evidence:* Given verbatim in the page's version/source footer. ('Version & Source' section (page footer))
  - *quote:* "Package: dataretrieval 0.1.dev1+g74c48569d"

## Data / numbers
- Date parameters use ISO-8601 format: YYYY-MM-DD
- Bounding box (bBox) constraint: product of latitude range × longitude range ≤ 25 degrees
- stateCd: 2-digit U.S. postal state code; only 1 per request
- huc: 1 major HUC (2 digits) or up to 10 minor HUCs per request
- countyCd: 5-digit county code (FIPS State Code + county)
- period keyword example: 'P10W' (ISO-8601 duration = 10 weeks)
- modifiedSince/query_waterservices duration examples: 'P1D' (1 day), 'P1Y' (1 year)
- get_ratings() file_type options: 'base' (default), 'corr', 'exsa'
- get_ratings() site parameter: USGS site number 'typically 8 digits'
- get_stats() statReportType options: 'daily' (default), 'monthly', 'annual'
- get_stats() statTypeCd options: 'all', 'mean', 'max', 'min', 'median'
- get_dv() example uses statCd='00003' (mean statistic code)
- get_iv() example uses parameterCd='00060' (discharge) for site 05114000, 2013-11-03 to 2013-11-03
- what_sites() example uses parameterCd='00665' (phosphorus) with stateCd='OH'
- get_discharge_peaks() example date ranges: 1980-01-01 to 1990-01-01 (site 01491000); 1980-01-01 to 1980-01-02 (stateCd='HI')
- get_dv() statistics example date range: 2012-01-01 to 2012-06-30 for site 04085427
- Example 8-digit USGS site numbers appearing in documented code samples: 05114000, 04085427, 01646500, 01491000, 01594440, 01585200, 09423350
- Package version documented: dataretrieval 0.1.dev1+g74c48569d

## Methods
Documentation of a Python software package providing thin wrapper functions around USGS NWIS web services (waterservices.usgs.gov for 'dv'/'iv'/'site'/'stat' queries via `query_waterservices()`, and separate waterdata endpoints for 'peaks'/'ratings' via `query_waterdata()`). Functions return `pandas` DataFrames alongside an `NWIS_Metadata` object (containing response URL, query elapsed time, `httpx.Headers`, comments, and an optional `site_info` property). Underlying HTTP transport is `httpx` (per the `NWIS_Metadata.header` type and the `httpx.Response` return type of the internal query functions). There is no statistical or predictive model here — it is purely a data-access API, so "where it works or fails" is about query semantics (valid parameter combinations, defunct endpoints) rather than predictive skill.

## Stated limitations
The page itself documents several functional limitations/caveats: (1) five previously core functions — get_discharge_measurements(), get_gwlevels(), get_pmcodes(), get_qwdata(), and get_water_use() — are now "defunct" and raise errors ("NoReturn") redirecting users to replacement functions, mostly in a different module (`waterdata`); (2) the legacy NWIS water-use web service itself "has been retired" server-side, so within `dataretrieval.nwis` "no replacement available" exists there (a different data source, NWDC, must be used via a different sub-package, `dataretrieval.wateruse`); (3) bounding-box site searches are capped such that the product of latitude and longitude range "cannot exceed 25 degrees"; (4) get_iv(), get_dv(), and get_record() silently return only the most recent record if no start/end date is given, which could be mistaken for full history; (5) get_info() requires at least "one major parameter" and the lower-level query_waterservices() requires "one major filter: sites, stateCd, or bBox" — under-specified queries are not supported; (6) the documented package build is a development/pre-release version ("dataretrieval 0.1.dev1+g74c48569d"), not a fixed numbered release, meaning the exact API surface may shift.

## Tensions with other findings
This is a software/API reference with no HAB-specific scientific claims, so it does not directly support or contradict biological/water-quality findings elsewhere in the literature. The relevant tension for a HAB data pipeline is reproducibility/traceability: get_qwdata() — historically the function used to pull discrete water-quality samples (e.g., nutrients, possibly chlorophyll-adjacent measures) from NWIS/STORET-derived data — is now defunct and redirects to a different module (`waterdata.get_samples()`), as are get_gwlevels(), get_pmcodes(), and get_water_use(). Any code, tutorial, or prior HAB analysis that cites `dataretrieval.nwis` for water-quality or water-use retrieval using these older function names will not run against the current package version documented here, and should be re-verified against the current API before being treated as reproducible for this project's in-situ data acquisition step.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0

## Provenance
- Canonical URL: https://doi-usgs.github.io/dataretrieval-python/reference/nwis.html
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: A single WebFetch on the primary URL returned comprehensive, well-structured reference content (module overview, all documented functions/signatures/parameters/examples, a deprecated-functions list, a "Key Notes & Limitations" summary, and a version/source footer). No WebSearch fallback was needed since the fetch was complete and clearly the correct page (it matches the exact URL and describes the `dataretrieval.nwis` module). Content below is taken as given by the fetch tool; no prior/training knowledge of the package was used.
