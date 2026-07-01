---
key: SLG-001
title: Algal Bloom Dashboard
authors_or_org: Florida Department of Environmental Protection (FDEP)
year: n/a (live/continuously-updated web resource; not a dated publication)
url: https://floridadep.gov/AlgalBloom
access_date: 2026-07-01
tier: SLG
source_type: State-agency operational web dashboard (ArcGIS-embedded interactive map) plus landing/portal page
categories: [in-situ-and-weather-data]
relevance: Medium
full_text_access: landing-only
fetch_status: ok
review_severity: notes
review_overall: flag
---

# Algal Bloom Dashboard

**What it is.** The Algal Bloom Dashboard is a Florida DEP-operated interactive ArcGIS mapping portal that tracks and visualizes algal bloom activity across Florida's waters statewide; the fetched HTML is a thin landing/wrapper page around an embedded map application rather than a document containing the underlying data or methodology itself.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The dashboard is operated by the Florida Department of Environmental Protection, described on the page as the state's lead agency for environmental management and stewardship.
  - *evidence:* Stated directly in the page's agency-description boilerplate captured by both fetches. (Page body / agency description)
  - *quote:* "the state's lead agency for environmental management and stewardship"
- **[✓ verified]** The page provides a citizen-reporting pathway for algal blooms via an external survey form ('Report Algal Blooms'), indicating public/citizen reports are one input channel referenced from this page.
  - *evidence:* Both fetches independently identified a 'Report Algal Blooms' link routing to a survey form; neither fetch found detail on what happens after a report is submitted. (Page navigation / quick links)
- **[⚠ partial]** The page offers 'Blue-Green Algal Bloom Weekly Reports' as an alternative, non-interactive way to view bloom status, implying the dashboard is refreshed/supplemented on a weekly reporting cadence.
  - *evidence:* Both fetches flagged the weekly-report link as the only stated frequency information on the page; the dashboard's own update frequency is not stated. (Page body, alternative-access note)
  - *reviewer:* The source confirms the weekly reports exist as an alternative resource, but does not state the dashboard's update cadence. The claim conflates the existence of weekly reports with the dashboard's refresh frequency, which is not established in the source text.
- **[⚠ partial]** No cyanobacteria concentrations, chlorophyll-a values, toxin thresholds, sample counts, or water-body-specific statistics are present anywhere in the fetched landing-page text; the actual monitoring data lives inside the embedded ArcGIS map application, which the fetch tool renders as markdown and cannot execute/query.
  - *evidence:* Both independent fetch passes, using different extraction prompts, converged on this same negative finding, which strengthens confidence it reflects the page's actual (thin) content rather than a fetch-tool omission. (Whole page)
  - *reviewer:* The source confirms no such data is detailed on the page itself (FETCH 1: 'The page does not detail specific data parameters'). However, the supplementary WebSearch section references a Florida Climate Institute article stating the dashboard shows 'real-time updates of sample locations for up to 90 days' with photos and toxin info, and chlorophyll-index conversions. This suggests the data exists in the dashboard's embedded ArcGIS application, contradicting the claim's implication that this data is completely absent from the dashboard.
- **[✓ verified]** The page recommends viewing with Google Chrome or Microsoft Edge and directs users experiencing technical issues to the weekly PDF reports instead of the live map.
  - *evidence:* Direct caveat captured verbatim by the first fetch. (Page body, technical note)
  - *quote:* "Best experienced with Google Chrome or Microsoft Edge browsers"
- **[✓ verified]** The page lists Florida DEP general contact information (phone, email, headquarters address) but no program-specific contact for the algal bloom dashboard itself.
  - *evidence:* Both fetches independently extracted the same generic DEP contact block from page/site chrome. (Page footer/contact block)
  - *quote:* "3900 Commonwealth Boulevard, Tallahassee, FL 32399-3000"
- **[✓ verified]** The page's exact HTML title is 'Algal Bloom Dashboard | Florida Department of Environmental Protection.'
  - *evidence:* Directly reported by the second fetch pass. (HTML <title> element)
  - *quote:* "Algal Bloom Dashboard | Florida Department of Environmental Protection"

## Data / numbers
- Phone contact listed on page: 850-245-2118 (Florida DEP general public services line, not dashboard-specific)
- Mailing address listed on page: 3900 Commonwealth Boulevard, Tallahassee, FL 32399-3000 (Florida DEP headquarters, not dashboard-specific)
- No cyanobacteria, chlorophyll-a, microcystin/toxin, sample-count, or water-body-level numeric data were found on the fetched page itself

## Methods
The page itself documents no methods, models, or data-processing pipeline — it is a portal/landing wrapper around an embedded ArcGIS web map. It references (without describing in the fetched text) a citizen-reporting survey form as one input channel and a companion 'Blue-Green Algal Bloom Weekly Reports' product as an alternative/backup view. Independent WebSearch corroboration of the broader FDEP program (not confirmed as being on this specific URL's fetched text) indicates that program-level, sampling teams log field-visit data in real time, DEP coordinates with partner agencies (SFWMD, SWFWMD, FWC, Lee County) on sample response, and satellite-derived chlorophyll imagery feeds a separate weekly bloom-potential assessment for water bodies such as Lake Okeechobee — but none of that methodological detail is present in the two direct fetches of floridadep.gov/AlgalBloom, so it is reported here only as unverified surrounding context, not as content of this key claim.

## Stated limitations
The page itself states only a browser-compatibility caveat ('Best experienced with Google Chrome or Microsoft Edge browsers') and implicitly acknowledges the live map can be unreliable/inaccessible by directing users with issues to the static weekly PDF reports instead. No limitations regarding data latency, sampling coverage, satellite-versus-in-situ discrepancy, or interpretive caveats for cyanobacteria/toxin results are present in the fetched landing-page text (such caveats likely exist in the linked weekly reports or the embedded map's own metadata, but those were not part of this fetch).

## Tensions with other findings
This source, as fetched, is data-thin: it is an operational portal, not a scientific document, so it cannot itself corroborate or contradict findings from remote-sensing/in-situ fusion literature. Note a scope caution for the dossier: WebSearch results describing the broader FDEP program (e.g., a chlorophyll-index-to-cyanobacteria-concentration conversion reportedly used in the companion Weekly Update PDFs, and a claim that the dashboard shows 'real-time updates of sample locations for up to 90 days') were found in independent search snippets, not in the two direct fetches of this URL's text — they should not be cited as if they were verified content of floridadep.gov/AlgalBloom without separately fetching and confirming the specific weekly-report PDF or the Florida Climate Institute launch article.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The supplementary WebSearch section notes the dashboard shows 'real-time updates of sample locations for up to 90 days' and references toxin info and chlorophyll-index conversions in the underlying ArcGIS application and weekly PDF reports—this temporal scope and data content is not mentioned in the claims, though it is present in the source text as external corroboration.
- **Reviewer notes:** Six of seven claims are clearly supported by the source text. Claim 4 (about data presence on the landing page) is marked 'partial' because the source text is internally contradictory: the fetched landing-page content shows no specific data values, but the supplementary WebSearch cites external sources claiming the dashboard's embedded ArcGIS application and weekly PDF reports contain chlorophyll-a conversions, toxin info, and 90-day sample-location history. The claim is technically accurate for the landing-page text alone, but the broader source material suggests richer underlying data exists, creating a tension the claims do not resolve. No hallucinated numbers; all quoted material matches the source. Overall flagged due to the partial claim."

## Provenance
- Canonical URL: https://floridadep.gov/AlgalBloom
- Access date: 2026-07-01
- Full-text access: landing-only | Fetch status: ok
- Fetch notes: Fetched the target URL twice with different extraction prompts as required for a HIGH-provisional-relevance source; both passes converged on the same conclusion: floridadep.gov/AlgalBloom is a thin landing/portal page wrapping an embedded ArcGIS interactive map, and the fetch tool (which converts HTML to markdown and cannot execute the JS-driven map widget) could not extract any underlying monitoring data, sampling numbers, thresholds, or methodology — because that content lives inside the interactive map application, not in the page's static HTML/text. I therefore downgraded provisional relevance from High to Medium and category remains in-situ-and-weather-data (the dashboard is a portal to in-situ sampling results, even though this fetch could not confirm satellite content on the page itself). I ran two supplementary WebSearch queries to (a) check whether a richer version of this exact page exists elsewhere and (b) sanity-check whether important on-page content was being missed by the fetch tool; both searches returned only the same URL plus separate, distinct documents (weekly PDF reports, a Florida Climate Institute news article, a related 'protectingfloridatogether.gov' dashboard) rather than richer content from this specific page. Per task rules, I have NOT incorporated those separate documents' specific numbers (e.g., chlorophyll-to-cyanobacteria conversion factors, the '90 days' retention claim) into key_claims or data_numbers, since they were not present in the direct fetch of the assigned URL — they are flagged only as caution/context in tensions and methods. If the dossier compiler wants those numbers formally verified, SLG-001's source URL should be treated as distinct from the companion Weekly Update PDF series and 'Algal Bloom Sampling Results' page, each of which would need its own separate fetch-and-cite pass.
