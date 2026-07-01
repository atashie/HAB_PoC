---
key: FED-061
title: Harmful Algal Bloom Monitoring System
authors_or_org: NOAA National Centers for Coastal Ocean Science (NCCOS)
year: 
url: https://coastalscience.noaa.gov/science-areas/habs/hab-monitoring-system/
access_date: 2026-07-01
tier: FED
source_type: Government agency program/landing page (NOAA NCCOS official website)
categories: [remote-sensing]
relevance: Medium
full_text_access: landing-only
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Harmful Algal Bloom Monitoring System

**What it is.** An official NOAA National Centers for Coastal Ocean Science (NCCOS) program landing page describing the "Algal Bloom Monitoring System" — an operational application delivering near-real-time, image-based bloom detection products for a currently limited set of named U.S. coastal and lake regions — together with NOAA's companion short-term (weekly-cadence) and seasonal HAB forecast products aimed at coastal/water managers.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** NCCOS's 'Algal Bloom Monitoring System' is described as routinely delivering near-real-time, satellite-derived, image-based bloom detection products for locating, monitoring, and quantifying algal blooms, but is explicitly scoped to only a limited, currently 'selected' set of U.S. coastal and lake regions, with further expansion contingent on future evaluation.
  - *evidence:* Directly stated in the page's own description of the system's purpose and current rollout status. (Main body, 'Harmful Algal Bloom Monitoring System' page, paragraph beginning "NCCOS developed the Algal Bloom Monitoring System...")
  - *quote:* "At this time products are available for selected regions. New products are being evaluated, and new regions are being considered; as they are proven useful, they will be made available through this system."
- **[✓ verified]** The system's linked products, as of this page, cover 11 distinct region-specific monitoring pages spanning 13 named water bodies — nearly all lakes/estuaries rather than open ocean: Green Bay & Lake Winnebago (WI), Saginaw Bay (MI), Western Lake Erie Basin, a Great Lakes high-resolution demonstration product, Lake Champlain, Coastal Northeast US, Chesapeake Bay, Albemarle & Pamlico Sounds (NC), Lake Pontchartrain (LA), Southwest Florida, and Lake Okeechobee (FL).
  - *evidence:* Enumerated by tallying the distinct 'HAB Monitoring Products' links on the page, each pointing to a region-specific bloom-monitoring subpage; this is a count derived from the link list, not a number stated in the page's prose. ('HAB Monitoring Products' link list section of the page)
- **[✓ verified]** Exactly one of the eleven regional products — covering the Great Lakes — is explicitly labeled a 'Demonstration' and is the only product on the page carrying a stated spatial resolution (20 meters); no other regional product states a resolution.
  - *evidence:* Confirmed via a targeted follow-up fetch checking the literal anchor text of each product link; only this one link contains a numeric/unit value. ('HAB Monitoring Products' link list; link anchor text for the Great Lakes chlorophyll-a product)
  - *quote:* "Demonstration Great Lakes (20m)"
- **[✓ verified]** NOAA/NCCOS issues two tiers of HAB forecasts: short-term forecasts, issued once or twice per week, that locate and size a bloom and project where it is headed; and longer-term seasonal forecasts that predict overall bloom severity for a region's season.
  - *evidence:* Stated directly in the 'HAB Forecasting' section describing forecast types and cadence; no accuracy or skill statistics accompany either forecast type on this page. ('HAB Forecasting' section)
  - *quote:* "Short-term (once or twice weekly) forecasts identify which blooms are potentially harmful, where they are, how big they are, and where they're likely headed. Longer-term, seasonal forecasts predict the severity of HABs for the bloom season in a particular region."
- **[✓ verified]** The stated purpose of the early-warning forecasts is decision support: enabling health officials, environmental managers, and water treatment facility operators to target testing and time beach/shellfish-bed closures or water treatment appropriately, and letting seafood/tourism industries reduce impacts.
  - *evidence:* Direct statement of the intended end-user decisions the forecast product is meant to support — i.e., an operational 'action window' framing rather than a raw detection output. ('HAB Forecasting' section, final two sentences)
  - *quote:* "Early warning provides health officials, environmental managers and water treatment facility operators information to focus their testing to guide beach and shellfish bed closures or water treatment in a more appropriate timeframe."
- **[✓ verified]** The page frames HABs generally as caused by a small subset of naturally occurring algal species capable of producing toxins, and asserts (without citation on this page) that HABs now occur in every U.S. state and that new HAB problems have emerged in recent years.
  - *evidence:* General definitional/background claim opening the page; presented as fact with no data, count, or reference to support the 'every state' or 'new HABs emerged' assertions on this page. (Opening definitional paragraph)
  - *quote:* "HABs occur in every state, and new HABs have emerged in recent years, adding new threats to regions already impacted."

## Data / numbers
- 20 m spatial resolution — stated only in the link label 'Demonstration Great Lakes (20m)' for one Great Lakes chlorophyll-a product; no other product on the page states a resolution; no baseline or uncertainty given, and the product is explicitly labeled a 'Demonstration' (not a mature operational layer).
- Short-term HAB forecasts issued 'once or twice weekly' (~1-2 times per week); no accuracy/skill statistic or uncertainty given for these forecasts.
- 11 distinct regional-product links enumerated on the page, covering 13 named water bodies/regions (two links each bundle two places: Green Bay + Lake Winnebago, WI; and Albemarle + Pamlico Sounds, NC). This count was derived by tallying the page's links; it is not a number stated explicitly in the source text.

## Methods
The page names no specific satellite sensor (no MODIS, VIIRS, Sentinel, or Landsat mentioned anywhere in the fetched text), no retrieval algorithm, and no cyanobacteria/chlorophyll index formula. It describes the system only generically as producing "a suite of bloom detection products in the form of geographic based images" processed in near-real-time for selected U.S. coastal/lake regions, alongside a separate two-tier forecast product (short-term situational forecasts 1-2x/week; longer-term seasonal severity outlooks). The only technical specification present anywhere on the page is a 20-meter resolution label attached to one product explicitly marked "Demonstration" for the Great Lakes, implying a higher-resolution capability is being trialed there, but the underlying sensor, algorithm, or validation method for that product is not disclosed on this page. No skill assessment, accuracy statistic, or comparison to in-situ/ground-truth data is presented anywhere in the fetched text.

## Stated limitations
The page itself states its current scope is limited: "At this time products are available for selected regions. New products are being evaluated, and new regions are being considered; as they are proven useful, they will be made available through this system." This signals (a) not all US water bodies are covered yet, (b) additional candidate products remain in a pre-operational evaluation phase before being added, and (c) the one higher-resolution Great Lakes product is explicitly labeled a "Demonstration," i.e., presented as a trial/pilot rather than a mature, fully operational layer like the other ten regional products. No other caveats (e.g., cloud cover, algorithm error, seasonal data gaps, or forecast skill limits) are stated anywhere in the fetched text.

## Tensions with other findings
This is an official program/landing page, not a peer-reviewed study: it makes broad framing statements ("HABs occur in every state," blooms' effects "can be severe," forecasts serve as actionable early warning) without disclosing any sensor, algorithm, spatial/temporal resolution (aside from the single 20 m demonstration-product label), or any accuracy/validation/skill statistic. That absence of quantified performance or uncertainty is in tension with the rigor this literature review otherwise expects (baselines, error bars, validation) and with peer-reviewed HAB remote-sensing/forecasting studies that do report such metrics. Consequently this source can responsibly support only descriptive/contextual claims about the existence, structure, and stated intent of NOAA's operational monitoring/forecasting program — not any quantitative claim about detection accuracy or forecast skill. Its assertion that new HABs "have emerged in recent years" is stated as fact with no supporting count or citation on this page, so it should not be treated as an independently evidenced trend.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All six claims are directly supported by the source text. No hallucinated numbers, dropped important caveats, or unsupported assertions detected. The extraction is accurate and faithful to the source material."

## Provenance
- Canonical URL: https://coastalscience.noaa.gov/science-areas/habs/hab-monitoring-system/
- Access date: 2026-07-01
- Full-text access: landing-only | Fetch status: ok
- Fetch notes: Fetched the primary URL directly (https://coastalscience.noaa.gov/science-areas/habs/hab-monitoring-system/); it loaded and matched the expected title/topic, so no WebSearch fallback was needed. Ran three targeted WebFetch passes on the same URL to (1) get a first general extraction, (2) enumerate every link/region and full paragraph text, and (3) verify verbatim anchor text for the one link carrying a numeric resolution value ("Demonstration Great Lakes (20m)"), since the first two passes disagreed on whether any number was present. This source is fundamentally a NOAA/NCCOS program landing page (an index of an operational system with links to per-region product pages, a separate forecasting page, and a "more information" page), not a technical report or peer-reviewed paper — hence full_text_access is set to landing-only even though the page's own visible text was fully retrieved. It contains no satellite/sensor names (no MODIS/VIIRS/Sentinel/Landsat mentioned), no algorithm or index description, and no accuracy/validation statistics. Deeper technical content, if any, would live on the linked sub-pages (e.g., /hab-monitoring-system/more-information/, /hab-forecasts/, and the individual region pages), which were not fetched and are out of scope for this single-URL dossier entry.
