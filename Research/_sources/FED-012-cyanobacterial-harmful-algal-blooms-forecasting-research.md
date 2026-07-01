---
key: FED-012
title: Cyanobacterial Harmful Algal Blooms Forecasting Research
authors_or_org: U.S. Environmental Protection Agency (EPA), Office of Research and Development (page presented as "EPA researchers" work, part of the multi-agency Cyanobacteria Assessment Network (CyAN) project)
year: 2024 (forecasting model developed/launched; underlying workflow published as Schaeffer et al. 2024); forecasts resumed 2025; page itself "Last updated on April 3, 2026"
url: https://www.epa.gov/water-research/cyanobacterial-harmful-algal-blooms-forecasting-research
access_date: 2026-07-01
tier: FED
source_type: U.S. federal government agency research program web page (EPA Office of Research and Development, water-research site)
categories: [models-and-methods]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Cyanobacterial Harmful Algal Blooms Forecasting Research

**What it is.** An EPA Office of Research and Development web page describing EPA's experimental cyanobacterial harmful algal bloom (cyanoHAB) forecasting research, conducted as part of the multi-agency Cyanobacteria Assessment Network (CyAN) project. It describes a model, launched in 2024, that issues a weekly 7-day-ahead probability-of-bloom forecast for 2,192 Sentinel-3-satellite-resolvable lakes in the contiguous United States, and states the model's definitions, seasonal scope, and known limitations (notably a false-positive bias).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** In 2024 EPA developed and launched an experimental cyanoHAB forecasting model that issues a 7-day probability-of-bloom forecast for the population of lakes EPA already monitors via near-real-time satellite data.
  - *evidence:* Stated directly in the page's introductory framing of the research program and its 2024 deliverable. (Page overview / introductory section)
  - *quote:* "This new forecast model now provides a 7-day prediction of the probability of a cyanoHAB in these lakes."
- **[✓ verified]** The forecast model's coverage is capped at 2,192 lakes in the contiguous United States, specifically those large enough to be resolved by the Sentinel-3 satellite's 300 x 300 meter pixel resolution.
  - *evidence:* Two independent broad fetches and one targeted verification fetch all independently returned this same lake count and resolution figure, indicating it is stated directly on the page rather than inferred. (Model scope / "Interpreting Forecast Results" section)
  - *quote:* "2,192 lakes in the contiguous United States that are resolvable by the Sentinel-3 satellite" / "The spatial resolution of the Sentinel-3 satellite images used to train the forecast model is 300 x 300 meters"
- **[✓ verified]** A cyanoHAB "bloom" is operationally defined by the model as median lake chlorophyll-a of 12 ug/L or greater together with cyanobacteria dominance, based on the surface layer only (typically the upper two meters or less).
  - *evidence:* This is the core outcome/label definition the forecasting model is trained to predict; combines a concentration cutoff, a taxonomic-dominance condition, and a depth caveat. ("Interpreting Forecast Results" section)
  - *quote:* "median lake chlorophyll a >=12 ug/L with cyanobacteria dominance" ... "the median lake chlorophyll-a in the surface (typically upper two meters or less)"
- **[✓ verified]** Each weekly forecast is valid for a fixed 7-day window running Sunday through Saturday, and forecasts are typically only produced from April through November because bloom probability is generally lower in colder months.
  - *evidence:* Describes forecast cadence and the seasonal operating window, stated as an operational design choice tied to seasonal bloom likelihood. ("Forecast Data" section)
  - *quote:* "The forecast model is structured to generate weekly cyanoHABs probabilities that are valid for a seven-day period extending Sunday through Saturday." ... "Forecasting data are typically generated from the beginning of April through November as the probabilities of harmful algal blooms are generally lower during colder months."
- **[✓ verified]** The chlorophyll-a input feeding the model is computed by masking out unusable satellite pixels (cloud, cloud shadow, glint, straylight, snow, ice, land cover) and taking the median chlorophyll-a of the retained pixels per lake, following a workflow detailed in a separate 2024 methods publication (Schaeffer et al. 2024).
  - *evidence:* Describes the data-processing pipeline that converts raw Sentinel-3 imagery into the per-lake chlorophyll-a series used to define bloom/no-bloom and to train the forecast. (Methods / Publications section)
  - *quote:* "pixels that included cloud, cloud shadow, glint, straylight, snow, ice, or land cover" are removed, then "a median chlorophyll-a concentration is calculated for each lake and is compared to the a threshold of 12 ug/L." ... "The weekly bloom probability forecasts have been produced following the workflow described in detail in Schaeffer et al. 2024."
- **[✓ verified]** EPA states the model currently overpredicts positive bloom events (a false-positive bias) and recommends this be offset with complementary field sampling or additional remote sensing.
  - *evidence:* Self-reported qualitative performance characterization from the model developers themselves; no numeric error rate is given alongside it. (Limitations paragraph within "Interpreting Forecast Results")
  - *quote:* "Currently, the model overpredicts positive events, where additional complementary field sampling or additional remote sensing may be useful."
- **[✓ verified]** EPA characterizes the model as having "low false omission," i.e., rarely missing a true bloom, which it frames as a deliberately conservative, health-protective design trade-off, while providing no quantitative accuracy, precision, recall, or AUC statistic anywhere on the page.
  - *evidence:* Qualitative trade-off statement; the absence of a quantitative validation metric was explicitly checked for and confirmed not present in a targeted follow-up fetch. (Limitations paragraph)
  - *quote:* "The model has low false omission and is therefore more conservative in protecting health."
- **[✓ verified]** EPA explicitly states the forecasting model must not substitute for direct field sampling or observation, and that it may contain errors and will be refined over time.
  - *evidence:* Direct disclaimer bounding appropriate use of the forecast relative to ground-truth monitoring. (Limitations / disclaimer section)
  - *quote:* "This model should not replace regular sampling or observation methods." ... "This forecasting model was trained and validated with the CyAN satellite data but may contain errors and will be continuously improved over time."
- **[✓ verified]** Weekly forecasts, after being paused, resumed for the 2025 season and are now hosted on a separate EPA "Harmful Algal Bloom Forecasting" webpage rather than on this research description page.
  - *evidence:* Administrative/operational note distinguishing this page (research description) from the live operational forecast output. (Page administrative note (near top of page))
  - *quote:* "Weekly forecasts previously posted on this webpage have resumed for 2025 and are now housed on EPA's Harmful Algal Bloom Forecasting webpage"

## Data / numbers
- 2,192 lakes — number of contiguous-U.S. lakes covered by the forecast model ("2,192 lakes in the contiguous United States that are resolvable by the Sentinel-3 satellite")
- 300 x 300 meters — Sentinel-3 satellite image spatial resolution used to train the model ("The spatial resolution of the Sentinel-3 satellite images used to train the forecast model is 300 x 300 meters")
- 12 ug/L — chlorophyll-a threshold defining a bloom, combined with cyanobacteria dominance ("median lake chlorophyll a >=12 ug/L with cyanobacteria dominance")
- upper two meters or less — surface depth represented by the satellite chlorophyll-a value ("the median lake chlorophyll-a in the surface (typically upper two meters or less)")
- 7-day / seven-day forecast validity window, Sunday through Saturday ("a seven-day period extending Sunday through Saturday")
- April through November — seasonal window when forecasts are typically generated
- 2024 — year the experimental forecasting model was developed/launched
- 2025 — year weekly forecasts "resumed" and were relocated to a separate EPA forecasting webpage
- Page "Last updated on April 3, 2026"
- No quantitative accuracy/precision/recall/AUC statistic is stated anywhere on the page (explicitly confirmed absent via targeted re-fetch) — i.e., no numeric baseline or uncertainty is given for forecast skill itself, only the qualitative statements that it "overpredicts positive events" and has "low false omission"

## Methods
Remote-sensing-driven probabilistic forecasting model for cyanobacterial HABs (cyanoHABs), developed by EPA as part of the multi-agency CyAN project. Input: Sentinel-3 satellite ocean-color imagery at 300 x 300 m pixel resolution. Preprocessing: pixels contaminated by cloud, cloud shadow, glint, straylight, snow, ice, or land cover are masked out; a per-lake median chlorophyll-a concentration is then computed from the surface layer (typically upper two meters or less) using the retained pixels. Label/target definition: a lake-week is labeled a "bloom" when median chlorophyll-a is >=12 ug/L with cyanobacteria dominance. The model, whose workflow is detailed in a separate 2024 publication (Schaeffer et al. 2024), outputs a 7-day-ahead (Sunday-Saturday) probability of a cyanoHAB for each of 2,192 Sentinel-3-resolvable lakes in the contiguous U.S., generated seasonally from April through November. Per the page's own framing, the model "works" in the sense of being conservative/protective (low false omission — it rarely misses a true bloom), which is presented as an intentional health-protective trade-off; it currently "fails" toward over-prediction (frequent false positives), for which EPA recommends supplementing with field sampling or additional remote sensing. No quantitative validation statistics (accuracy, precision/recall, AUC, etc.) are reported on this page; the underlying model-development detail is deferred to Schaeffer et al. 2024, which was not itself fetched in this pass.

## Stated limitations
Page states directly: (1) "This forecasting model was trained and validated with the CyAN satellite data but may contain errors and will be continuously improved over time"; (2) "No forecast is perfect, and most forecast models will result in false positives and negatives"; (3) "Currently, the model overpredicts positive events, where additional complementary field sampling or additional remote sensing may be useful" — an explicit self-reported false-positive bias; (4) "This model should not replace regular sampling or observation methods"; (5) coverage is restricted by construction to the 2,192 lakes large enough to be "satellite-resolvable" at Sentinel-3's 300x300 m resolution, excluding smaller lakes; (6) forecasts are only generated seasonally (April-November), so there is no forecast coverage in winter months; (7) no quantitative accuracy, precision, recall, or AUC statistic is published anywhere on this page to substantiate forecast skill.

## Tensions with other findings
This page defines a "bloom" purely via satellite chlorophyll-a (>=12 ug/L) plus cyanobacteria dominance, and it explicitly admits the resulting forecast model over-predicts positive events — i.e., by EPA's own account, satellite chlorophyll-a is an imperfect, false-positive-prone proxy for actual cyanotoxin/health risk. This is directly relevant to (and in tension with) any other source in this review that treats CyAN/satellite chlorophyll-a detections as equivalent to a confirmed toxic bloom, or that argues remote sensing alone is sufficient without in-situ verification — this EPA page argues the opposite ("should not replace regular sampling or observation methods"). It also bounds the generalizability of any "national" CyAN-based HAB risk claims: only 2,192 (comparatively large, satellite-resolvable) CONUS lakes are in scope, so conclusions drawn from this line of research cannot automatically be extended to the many smaller lakes and ponds where recreational HAB advisories also commonly occur — a scope caveat other CyAN-derived sources in this review likely share. Correlation/causation note: nothing on this page claims a causal driver mechanism (e.g., nutrients -> bloom); it is purely a detection/forecasting definition and workflow, so no causal-inference tension arises on that front.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - General epistemic caveat from source: 'No forecast is perfect, and most forecast models will result in false positives and negatives' — implicit but not explicitly surfaced in individual claims.
- **Reviewer notes:** All 9 claims are directly and clearly supported by the source text. No hallucinated numbers. No unsupported claims. The analyst conducted thorough multi-pass verification and correctly cited the source material. The dropped caveat is a general statement about forecast uncertainty present in the source but not critical to any individual claim's validity."

## Provenance
- Canonical URL: https://www.epa.gov/water-research/cyanobacterial-harmful-algal-blooms-forecasting-research
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary URL four times with WebFetch (two broad comprehensive-extraction passes per the task instructions, plus two additional narrow verification passes) because the first two passes described several numbers/dates in prose without quotation marks (e.g., the 300x300 m resolution, the "upper two meters" depth, the Sunday-Saturday cadence, the 2025 resumption note, and whether any quantitative accuracy statistic exists). The two follow-up fetches returned exact verbatim sentences for each of these, which I used to confirm rather than reject the earlier paraphrases. All four fetches hit the same URL with no redirect, so no WebSearch fallback was needed; resolved_url = url_used = the given primary URL. No accuracy/precision/recall/AUC figure exists on the page — this absence was explicitly checked for and confirmed "not found on page" by the model doing the fetch, so it is reported here as a genuine gap rather than an extraction failure. All content is attributed to what the fetch tool returned from the live page; no prior/training knowledge of this specific EPA program was used.
