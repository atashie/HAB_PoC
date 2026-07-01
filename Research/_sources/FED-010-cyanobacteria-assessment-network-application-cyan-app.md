---
key: FED-010
title: Cyanobacteria Assessment Network Application (CyAN app)
authors_or_org: U.S. Environmental Protection Agency (EPA), Office of Research and Development — developed in collaboration with NASA (National Aeronautics and Space Administration), NOAA (National Oceanic and Atmospheric Administration), and USGS (U.S. Geological Survey)
year: Not a single-dated publication (living program webpage). Key dated milestones stated on the page: CyAN Android public release 2018; CyANWeb release 2021; cyanoHAB forecasting model beta-testing started July 2024; CyAN Android support ended December 31, 2024; page "Last updated on March 31, 2026" (date of this access).
url: https://www.epa.gov/water-research/cyanobacteria-assessment-network-application-cyan-app
access_date: 2026-07-01
tier: FED
source_type: Government agency program/tool web page (EPA "Water Research" site) — describes an operational tool, not a peer-reviewed paper
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Cyanobacteria Assessment Network Application (CyAN app)

**What it is.** EPA's Cyanobacteria Assessment Network application family — currently the browser-based "CyANWeb" tool (successor to the now-deprecated "CyAN Android" app) — which gives water-quality managers a no-programming-required interface to satellite-derived cyanobacteria bloom estimates for over 2,000 of the largest U.S. lakes and reservoirs, built by EPA with NASA, NOAA, and USGS from Sentinel-3 OLCI satellite data.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** CyANWeb provides satellite-derived cyanobacteria bloom data for over 2,000 of the largest lakes and reservoirs across the United States.
  - *evidence:* Stated as the tool's core description/purpose in the page's lead section. (Lead section, "Make faster decisions related to cyanobacterial algal blooms")
  - *quote:* "provides access to cyanobacterial bloom satellite data for over 2,000 of the largest lakes and reservoirs across the United States"
- **[✓ verified]** The app was built specifically so local and state water quality managers could make faster, better-informed HAB management decisions.
  - *evidence:* Direct statement of intended purpose/audience. (Lead section)
  - *quote:* "EPA scientists developed the app to help local and state water quality managers make faster and better-informed management decisions related to cyanobacterial blooms."
- **[✓ verified]** CyANWeb is a browser-based interface that is OS- and device-agnostic, unlike the deprecated CyAN Android app.
  - *evidence:* Stated under the compatibility section describing the technical delivery mechanism. ("Compatibility and Availability" section)
  - *quote:* "a web browser-based interface available on EPA's website that will work with any operating system and is compatible with most devices"
- **[✓ verified]** The tool is designed for fast, initial-assessment use and is constrained to water bodies of roughly 1 km² or larger.
  - *evidence:* Stated as a capability/constraint of the tool tied to satellite resolution. ("Capabilities and Applications" section)
  - *quote:* "allow fast and efficient initial assessments across water bodies that are roughly one square kilometer or greater"
- **[✓ verified]** The tool does not impose a single EPA-defined cyanobacteria concentration threshold; users set their own, because jurisdictions handle HABs differently.
  - *evidence:* Explicit design rationale given in the capabilities description. ("Capabilities and Applications" section)
  - *quote:* "Because states and localities may address harmful algal blooms differently, users can determine their own thresholds for cyanobacteria concentrations."
- **[⚠ partial]** The sole satellite sensor named as the data source is ESA's Copernicus Sentinel-3 Ocean and Land Colour Instrument (OLCI).
  - *evidence:* Directly named data source, with an external link to ESA's Sentinel-3 page. ("Capabilities and Applications" section, closing note)
  - *quote:* "The primary satellite sensor collecting data is the European Space Agency's Copernicus Sentinel-3 Ocean and Land Colour Instrument."
  - *reviewer:* Source states 'primary satellite sensor,' not 'sole'—'primary' permits other sensors whereas 'sole' implies exclusivity. Additionally, the acronym 'OLCI' does not appear in the source text; only the full instrument name is provided.
- **[✓ verified]** EPA explicitly labels the app and its underlying satellite measures as experimental, provisional, and potentially erroneous.
  - *evidence:* Direct self-disclaimer from EPA about data/tool maturity. ("Capabilities and Applications" section, closing note)
  - *quote:* "The CyANWeb app is an experimental application and provides provisional satellite derived measures of cyanobacteria, which may contain errors and should be considered a research level tool."
- **[✓ verified]** EPA began beta-testing an experimental predictive cyanoHAB forecasting model in July 2024 that produces weekly forecasts for over 2,000 lakes.
  - *evidence:* Direct statement describing a newer, separate forecasting capability layered on the same lake set. ("Cyanobacterial HABs Forecasting" section)
  - *quote:* "In July 2024, researchers started beta-testing an experimental cyanoHAB forecasting model to produce weekly forecasts for over 2,000 lakes across the U.S."
- **[✓ verified]** Both CyAN app versions were independently tested for over a year, with functionality and satellite data validated and published in multiple peer-reviewed papers, developed jointly with NASA, NOAA, and USGS.
  - *evidence:* Direct statement of the multi-agency collaboration and validation process. ("Background and Research Collaboration" section)
  - *quote:* "Both versions were tested separately for over one year and the functionality and satellite data were successfully validated and published in multiple peer-reviewed publications."
- **[✓ verified]** The original CyAN Android app was publicly released in 2018.
  - *evidence:* Stated in the FAQ answering why/when the Android app existed before deprecation. (FAQ: "Why has support ended for the CyAN Android App?")
  - *quote:* "since its public release in 2018"
- **[✓ verified]** CyANWeb launched in 2021 with additional features and became a full functional superset of the CyAN Android app.
  - *evidence:* Direct FAQ statement on the relationship between the two app versions. (FAQ: "Why has support ended for the CyAN Android App?")
  - *quote:* "With the release of CyANWeb and additional feature enhancements in 2021, everything available on the CyAN Android app also became available on CyANWeb."
- **[✓ verified]** EPA officially ended support for the CyAN Android app on December 31, 2024.
  - *evidence:* Direct FAQ statement with an exact end date, echoed in the page's top user-notice banner. (FAQ: "When did support end for the CyAN Android app?" / User Notice banner)
  - *quote:* "EPA support for the CyAN Android app ended on December 31, 2024."
- **[✓ verified]** Despite the Android app's discontinuation, the CyAN REST API providing processed cyanobacteria index (CI) data continues unchanged with no planned changes.
  - *evidence:* Direct FAQ statement distinguishing the discontinued client app from the still-supported underlying data service. (FAQ: "Will the CyAN data services still function after support ends?")
  - *quote:* "the CyAN REST API will remain unchanged and continue to provide processed cyanobacteria index (CI) estimate data with no planned changes at this time"
- **[✓ verified]** The CyANWeb Fact Sheet PDF is 245.67 KB (document EPA/600/F-19/061b, updated Dec 31 2024) and the Palm Card PDF is 1.67 MB (dated Dec 31 2024).
  - *evidence:* Exact file metadata listed alongside the downloadable resource links. ("Communications and Outreach Resources" section)
  - *quote:* "CyANWeb App Fact Sheet (pdf) (245.67 KB, Updated December 31, 2024, EPA/600/F-19/061b)"

## Data / numbers
- Coverage: 'over 2,000 of the largest lakes and reservoirs across the United States'
- Minimum useful water-body size for assessment: 'roughly one square kilometer or greater'
- CyAN Android app public release year: 2018
- CyANWeb release year (added features, functional superset of Android app): 2021
- Independent app validation/testing duration stated: 'tested separately for over one year' (no numeric accuracy statistic given)
- cyanoHAB forecasting model beta-testing start date: July 2024
- cyanoHAB forecasts: weekly cadence, for 'over 2,000 lakes across the U.S.'
- CyAN Android app support end date: December 31, 2024
- CyANWeb App Fact Sheet (PDF): 245.67 KB; document no. EPA/600/F-19/061b; 'Updated December 31, 2024'
- CyANWeb App Palm Card (PDF): 1.67 MB; dated December 31, 2024
- Page access/version metadata: 'Last updated on March 31, 2026'

## Methods
The CyAN app family is a front-end/delivery layer over satellite remote sensing, not a from-scratch model described in full on this page. Per the page: the primary (and only sensor named) is ESA's Copernicus Sentinel-3 Ocean and Land Colour Instrument (OLCI); this feeds a "cyanobacteria index (CI) estimate" data product served through a "CyAN REST API," which CyANWeb/CyAN Android visualize nationally or per-waterbody at a stated minimum useful resolution of "roughly one square kilometer or greater." The page states the app's "functionality and satellite data were successfully validated and published in multiple peer-reviewed publications" after both app versions were "tested separately for over one year," but it does not itself restate the detection algorithm's mathematical form or quantitative accuracy statistics — it instead links out to ~9 separate peer-reviewed papers (2017–2024) for that detail, including a 2018 Environmental Modelling & Software paper describing the original Sentinel-3-based mobile app (doi:10.1016/j.envsoft.2018.08.015) and a 2021 paper "Evaluation of a satellite-based cyanobacteria bloom detection algorithm using field-measured microcystin data." Separately, an "experimental cyanoHAB forecasting model" (beta since July 2024) extends the same data into predictive weekly forecasts for the same >2,000-lake set; its methodology lives on a distinct linked EPA page ("Cyanobacterial HABs Forecasting Research"), not within this source.

## Stated limitations
The source explicitly labels the tool "an experimental application" providing "provisional satellite derived measures of cyanobacteria, which may contain errors and should be considered a research level tool." The newer cyanoHAB forecasting capability is likewise described as an "experimental...model" still in "beta-testing." The CyAN Android app is deprecated (EPA support ended December 31, 2024); only CyANWeb and the underlying CyAN REST API continue to be supported "into 2025 and beyond." The page provides no EPA-set universal risk thresholds (no cells/mL or similar cutoffs for low/medium/high risk) — it states users must "determine their own thresholds for cyanobacteria concentrations" because "states and localities may address harmful algal blooms differently," which also means the page reports no accuracy/validation statistics (no error rates, no R², no comparison against in-situ cell counts) — validation is only referenced as having occurred ("tested...for over one year," "published in multiple peer-reviewed publications") without those results being restated here. A standard non-endorsement disclaimer is also given: "Any mention of trade names, products, services, or enterprises does not imply an endorsement by the U.S. Government or EPA."

## Tensions with other findings
This source is EPA's own "provisional / experimental / research level tool" framing for the exact satellite cyanobacteria signal (Sentinel-3 OLCI → CI index) that CLAUDE.md names as the project's primary remote-sensing data source ("EPA CyAN"). That reinforces the project's "calibrate language to evidence" principle: even the originating agency does not treat this satellite signal as validated-for-decisions truth, and it deliberately withholds a universal risk threshold, leaving threshold-setting to the user/jurisdiction — meaning any fixed risk cutoff our own tool adopts is a local convention we choose, not an EPA-endorsed number, and should be disclosed as such. There is also an internal tension in the source between operational marketing language (informing "recreational and drinking water safety" decisions, prompting managers to "issue a public advisory to close local shores to recreation") and its own disclaimer that the data "may contain errors" and is "research level" — i.e., EPA promotes real-world decision use of a tool it simultaneously labels experimental/provisional. No causal claims are made in this source about bloom drivers or treatment; it is purely descriptive of a detection/monitoring tool, so no correlation-vs-causation conflict arises here, but the "informs decisions" language should not be read as EPA asserting the satellite signal is validated for direct causal attribution of bloom risk.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** 13 of 14 claims are clearly supported by the source text. One claim (Claim 6) uses imprecise language: it states 'sole satellite sensor' when the source says 'primary satellite sensor'—a meaningful distinction, as 'primary' does not preclude others. Additionally, the acronym 'OLCI' appears in the claim but is not explicitly stated in the source text (only the full instrument name is provided). All numbers referenced in the claims (2,000 lakes, 1 km², 2018, 2021, 2024, file sizes, document ID) are present in the source. No evidence of result-shopping or exaggeration beyond this single partial overstatement."

## Provenance
- Canonical URL: https://www.epa.gov/water-research/cyanobacteria-assessment-network-application-cyan-app
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: WebFetch succeeded directly on the primary URL with no redirect (not blocked/paywalled) — no WebSearch fallback was needed. Per the HIGH-relevance protocol, I ran two independent WebFetch extraction passes with differently framed prompts, then ran a third WebFetch requesting a verbatim, section-by-section transcription specifically to cross-check figures that risked small-model rounding/hallucination (e.g., PDF file sizes, exact dates, document numbers). All three passes agreed on every number and quote reported here (e.g., 245.67 KB, 1.67 MB, EPA/600/F-19/061b, December 31, 2024), so these are treated as confirmed verbatim page text rather than model paraphrase. Note that this source is a program/tool landing page, not a peer-reviewed paper — "full_text_access: full" means the entire webpage (nav through FAQ/footer) was retrieved and is reflected here, not that all underlying CyAN science is covered: the page itself links out to roughly nine separate peer-reviewed publications (2017–2024) for algorithm/validation detail, none of which were themselves fetched as part of this dossier entry, and to a separate "Cyanobacterial HABs Forecasting Research" page for forecasting-model methodology. Those would need their own dossier entries if algorithmic/validation depth is required.
