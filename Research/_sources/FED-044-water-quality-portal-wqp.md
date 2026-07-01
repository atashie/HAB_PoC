---
key: FED-044
title: Water Quality Portal (WQP)
authors_or_org: Cooperative service of the U.S. Geological Survey (USGS) and U.S. Environmental Protection Agency (EPA); data contributed by 400+ state, federal, tribal, and local agencies; National Water Quality Monitoring Council (NWQMC) also referenced on-site in connection with the portal.
year: N/A — live, continuously updated web portal, not a dated publication; pages were accessed 2026-07-01, and the fetched text itself references a stated USGS-data cutoff of 2024-03-11 for the default (WQX2.2) interface and a stated data-volume snapshot dated December 2021.
url: https://www.waterqualitydata.us/
access_date: 2026-07-01
tier: FED
source_type: Federal government data portal / web service (public data infrastructure; USGS–EPA cooperative service), not a peer-reviewed publication.
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Water Quality Portal (WQP)

**What it is.** The Water Quality Portal (WQP) is a free, public web portal and companion web-service API that describes itself as "the premiere source of discrete water-quality data in the United States and beyond." It is a cooperative service sponsored jointly by USGS and EPA that federates two backend U.S. government water-quality databases — USGS's National Water Information System (NWIS) and EPA's Water Quality Exchange (WQX) Data Warehouse, the latter fed by 400+ contributing state, federal, tribal, and local agencies — behind one shared query interface, returning site/organization metadata and physical/chemical or biological sample results rather than performing any HAB-specific analysis itself.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** WQP describes itself as the leading U.S. source for discrete (i.e., non-continuous, sample-based) water-quality data, run as a cooperative service integrating publicly available water-quality information from multiple source systems rather than being a single agency's in-house database.
  - *evidence:* Direct self-description text pulled identically from two independent homepage extractions. (WQP homepage (waterqualitydata.us) — introductory/mission text)
  - *quote:* "the premiere source of discrete water-quality data in the United States and beyond"
- **[✓ verified]** WQP is jointly sponsored by USGS and EPA, each of which supplies one of the two backend databases the portal federates — USGS via the National Water Information System (NWIS), EPA via the Water Quality Exchange (WQX) Data Warehouse.
  - *evidence:* Explicit sponsorship/role statement on the portal's own description page. (WQP description page (waterqualitydata.us/wqp_description/))
  - *quote:* "a cooperative service sponsored by the United States Geological Survey (USGS) and the Environmental Protection Agency (EPA)"
- **[⚠ partial]** Beyond USGS and EPA, more than 400 additional state, federal, tribal, and local agencies contribute monitoring data that flows into the portal (largely via the EPA/WQX side, which receives submissions from states, tribes, watershed groups, other federal agencies, volunteer groups, and universities).
  - *evidence:* Stated verbatim and identically across both independent homepage fetches; contributor description elaborated on the description page. (WQP homepage; WQP description page)
  - *quote:* "over 400 state, federal, tribal, and local agencies"
  - *reviewer:* The source states 'Over 400 state, federal, tribal, and local agencies' contribute and lists the types of contributors via WQX, but does not explicitly use the word 'additional' or state these 400+ are separate/beyond the two sponsoring agencies. The 'additional' framing is a reasonable contextual inference but not explicit in the SOURCE TEXT.
- **[✓ verified]** The USGS NWIS system underlying WQP alone covers more than 1.5 million monitoring sites nationwide (current and historical), indicating the scale of one of the portal's two backends.
  - *evidence:* Stated when the description page explains what NWIS is. (WQP description page)
  - *quote:* "current and historical water data from more than 1.5 million sites across the nation"
- **[✓ verified]** As a portal-wide (not NWIS-only) figure, WQP's FAQ states that as of December 2021, results from more than 2.6 million monitoring locations were accessible through the portal — a dated snapshot statistic rather than a live counter.
  - *evidence:* Given as a direct data-volume statistic in the FAQ; no more recent figure was found in the fetched pages. (WQP FAQs page (waterqualitydata.us/faqs/))
  - *quote:* "results from over 2.6 million monitoring locations were accessible through the portal"
- **[✓ verified]** The two backend systems refresh on different schedules and the default interface has a hard USGS data-currency cutoff: EPA/WQX data refreshes weekly (Thursday evenings), while USGS/NWIS data feeding the default (WQX2.2) interface stopped updating as of March 11, 2024; more recent USGS records require the separate beta interface serving WQX 3.0 profiles.
  - *evidence:* FAQ gives the WQX refresh cadence and confirms the NWIS refresh stopped on that date; homepage and description pages both independently state the same March 11, 2024 USGS-data cutoff for the legacy interface. (WQP FAQs page; WQP homepage; WQP description page)
  - *quote:* "refreshed once a week on Thursday evening"
- **[✓ verified]** Site identifiers are not harmonized between the WQX and NWIS source systems, so the same physical monitoring site can appear under different, non-matching IDs across the two backends; the FAQ instructs users to prepend organization identifiers (e.g., "USGS-") when searching to disambiguate.
  - *evidence:* Stated directly in the FAQ's discussion of known site-identifier issues — a practical data-linkage risk for anyone joining WQP records to another system by site ID. (WQP FAQs page)
  - *quote:* "have not been harmonized"
- **[✓ verified]** The FAQ warns that large or broad queries are slow, and specifically that applying the "Filter Results" option is reported to make the portal process roughly 100 times more data than a query restricted to sites alone, so it recommends narrowing by date range first to shrink the result set.
  - *evidence:* Direct performance guidance/caveat given in the FAQ, framed as the portal's own advice for avoiding slow or oversized queries. (WQP FAQs page)
  - *quote:* "100x more data than site-dependent queries"
- **[✓ verified]** The portal exposes multiple distinct data profiles beyond a simple site list — organization/site data, project data, sample results with both physical/chemical and biological metadata, sampling activity records, biological habitat metrics, and detection/quantitation-limit data — retrievable either through a web UI (CSV, TSV, or Excel 2007+ downloads) or through machine-readable web services (shareable query URLs, cURL commands, WFS GetFeature requests).
  - *evidence:* Enumerated on the homepage under the portal's stated data profiles and listed access/download methods. (WQP homepage)
  - *quote:* "Sample Results (physical/chemical metadata)"

## Data / numbers
- More than 400 state, federal, tribal, and local agencies contribute data to WQP (stated identically on two independent homepage fetches)
- USGS NWIS (one of WQP's two backend systems) holds "current and historical water data from more than 1.5 million sites across the nation" (WQP description page)
- "results from over 2.6 million monitoring locations were accessible through the portal" as of December 2021 (WQP FAQ page — a dated statistic, likely an undercount of current coverage)
- EPA-side WQX data is "refreshed once a week on Thursday evening" (WQP FAQ)
- USGS-side NWIS data behind the default/legacy interface is "no longer refreshed," with final refresh on 2024-03-11; the legacy interface explicitly "do[es] NOT contain USGS data added after March 11, 2024" (WQP homepage / description page)
- FAQ states the "Filter Results" query option is reported to process roughly "100x more data than site-dependent queries" — an approximate performance ratio, not a precise benchmark
- Support contact figures given on the homepage: phone 1-800-424-9067, email WQX@epa.gov (administrative, not a data statistic)

## Methods
WQP is not a research study and has no statistical/analytic "method" of its own; it is a federated data-access system. Functionally, it works by placing one shared query layer (web UI with basic/advanced download in CSV/TSV/Excel formats, plus machine-readable access via shareable query URLs, cURL, and WFS GetFeature requests) on top of two independently maintained source databases: USGS's NWIS (>1.5 million sites) and EPA's WQX Data Warehouse (fed by states, tribes, watershed groups, other federal agencies, volunteer groups, and universities), with 400+ total contributing organizations. Per the fetched FAQ, the federation "works" for cross-agency discovery and bulk download, but its two stated points of failure/friction are (a) the two backends update on different schedules and, in the default interface, USGS/NWIS data is frozen as of March 11, 2024 (EPA/WQX still refreshes weekly), and (b) site identifiers are not harmonized across NWIS and WQX, so naive ID-based joins across the two backends (or to an external dataset) risk duplication or mismatch unless organization-prefixed IDs are used.

## Stated limitations
The fetched pages state four explicit caveats: (1) The default interface only serves "WQX2.2" profiles, which do NOT contain USGS data added after March 11, 2024 (NWIS refresh into this instance has stopped, with a final refresh on that date); EPA/WQX data continues to refresh weekly (Thursday evenings). Users needing newer USGS records must switch to the separate beta interface serving "WQX 3.0" profiles at waterqualitydata.us/beta/. (2) Site identifiers "have not been harmonized" between the WQX and NWIS backends, so the same physical site can surface under non-matching IDs; users must prepend organization prefixes (e.g., "USGS-") to disambiguate — a concrete risk for any workflow joining WQP records to another dataset by raw site ID. (3) Query performance is flagged as a practical limitation: large date ranges/geographies are slow, and using the "Filter Results" option is said to process roughly 100x more data than a site-only query, so the FAQ recommends narrowing by date range first. (4) The FAQ and description pages fetched contained no statement on provisional-vs-approved data flags or on data licensing/terms of use; this may be addressed elsewhere on the site (e.g., a web-services or user guide not fetched here) rather than being an actual gap in WQP's documentation — it simply could not be confirmed from the pages retrieved in this task.

## Tensions with other findings
WQP is a data-access/aggregation layer, not a HAB-specific scientific finding, so it makes no empirical claims that could directly contradict other HAB literature. The practically relevant tension for this project is a data-fusion risk rather than a scientific one: (a) the source itself states that site IDs "have not been harmonized" between its NWIS and WQX backends, so naively joining WQP in-situ records (e.g., chlorophyll-a, nutrients) to another keyed dataset — including a satellite product like EPA CyAN, or a raw USGS gage ID — by site ID alone risks silent duplication or mismatch; matching should instead use organization-prefixed IDs and/or lat/long rather than assuming a shared key space. (b) The default (legacy/WQX2.2) interface's USGS-sourced data is frozen as of March 11, 2024; a project pulling from waterqualitydata.us today without deliberately switching to the beta WQX 3.0 endpoint would silently miss USGS in-situ observations from after that date — a currency gap that should be logged as a known limitation if this instance is used as the in-situ backbone for a HAB analysis intended to include recent data.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** Eight of nine claims are directly and explicitly supported by the SOURCE TEXT. One claim (Claim 3) uses the qualifier 'additional' when referring to the 400+ contributing agencies, but the source text does not explicitly state these 400+ are separate from or in addition to the two sponsoring agencies (USGS and EPA). While the contextual structure of the source (sponsors described separately from contributors) supports this inference, the term 'additional' itself is not present in the SOURCE TEXT. No hallucinated numbers were detected; all figures cited (1.5M sites, 2.6M locations, 400+ agencies, 100x data, March 11 2024, December 2021) are present in the source. No material caveats were omitted from the claims."

## Provenance
- Canonical URL: https://www.waterqualitydata.us/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Per instructions for a High-relevance source, WebFetch was run TWICE on the primary URL (https://www.waterqualitydata.us/) with different extraction prompts; both succeeded and were largely consistent (cooperative USGS/EPA service, >400 contributing agencies, WQX2.2-vs-3.0 data-currency caveat) but neither surfaced quantitative data-volume statistics, which the homepage itself does not appear to display. To meet the "comprehensive... every number" requirement, two supplementary WebFetches were then made on same-domain subpages discovered via WebSearch: https://www.waterqualitydata.us/wqp_description/ (succeeded; supplied the NWIS ">1.5 million sites" figure and USGS/EPA sponsorship wording) and https://www.waterqualitydata.us/faqs/ (succeeded; supplied the "2.6 million monitoring locations" figure, refresh cadence, site-ID harmonization caveat, and query-performance caveat). A fifth attempt at https://www.waterqualitydata.us/about/ returned HTTP 404 (page does not exist at that path) and is not used. The "2.6 million" figure first surfaced in a WebSearch synthesis but was independently confirmed by directly WebFetching the FAQ page itself, so it is treated as sourced from the FAQ page. No PDF or paywalled content was involved; nothing here is synthetic. Because WebFetch renders through a small intermediate model, quoted strings reflect that model's verbatim extraction rather than my own direct HTML read, per the tool's known behavior.
