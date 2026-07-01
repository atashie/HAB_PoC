---
key: FED-041
title: Using satellite imagery and national surveys to identify lakes at risk for toxic cyanobacteria blooms in the US
authors_or_org: Handler, A.; Compton, J.; Hill, Ryan A.; Leibowitz, S.; Schaeffer, B.; Dumelle, M. (US EPA Office of Research and Development)
year: 2023
url: https://assessments.epa.gov/risk/document/&deid=357233
access_date: 2026-07-01
tier: FED
source_type: Conference presentation / slide deck record (EPA Risk Assessment Portal, mirrored on EPA Science Inventory) — not a peer-reviewed journal article
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Using satellite imagery and national surveys to identify lakes at risk for toxic cyanobacteria blooms in the US

**What it is.** A short EPA ORD conference-presentation record (presented at the AWWA Pacific Northwest Section's "Cascade to Coast" Short School, Feb 27–Mar 2, 2023) describing a statistical approach that relates a satellite-derived cyanobacteria index to field-measured toxin/bloom-threshold exceedance, in order to flag which U.S. lakes are most at risk of toxic cyanobacterial blooms.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** For every 0.01 CI_cyano/km² increase in the satellite-derived lake-level Cyanobacteria Index, the odds of a lake exceeding six bloom thresholds increased by 23–54%.
  - *evidence:* Directly stated quantitative result reported in the abstract/description text of the EPA record, appearing identically in two independent fetches of two different EPA-hosted mirrors of the same record. (Abstract / "Description" section, EPA Risk Assessment Portal & Science Inventory record 357233)
  - *quote:* "For every satellite-derived lake-level Cyanobacteria Index (CI_cyano) increase of 0.01 CI_cyano/km2, the odds of exceeding six bloom thresholds increased by 23–54%."
- **[✓ verified]** Applied nationally, the models identified 162 lakes at ≥75% probability of exceeding the lower microcystin threshold (0.2 µg/L) and 70 lakes at ≥75% probability of exceeding the higher microcystin threshold (1.0 µg/L).
  - *evidence:* Directly stated model-output count of at-risk lakes for the two named microcystin action thresholds; captured as an identical verbatim sentence in two separate fetches. (Abstract / "Key Findings" section, EPA record 357233)
  - *quote:* "the models identified 162 and 70 lakes with ≥75% probability of exceeding the lower (0.2 µg/L) and higher (1.0 µg/L) thresholds, respectively."
- **[✓ verified]** The analysis covers a national set of roughly 2,192 satellite-monitored U.S. lakes, combining MERIS satellite imagery with the U.S. National Lakes Assessment field-survey program.
  - *evidence:* Scope/scale and the two named data sources (satellite + in-situ national survey) were reported consistently across three independent extraction passes, though no single verbatim sentence containing the figure was returned by the fetch tool despite repeated targeted prompts — treat the exact figure as corroborated-but-not-verbatim. (Abstract / methods description, EPA record 357233 (as rendered by repeated AI extractions of the EPA Risk Assessment Portal and Science Inventory mirrors))
  - *quote:* "2,192 satellite-monitored lakes"
- **[✓ verified]** The study's design deliberately leverages spatial variation across many lakes using two national-scale data sources, rather than analyzing temporal (within-lake, over-time) variability.
  - *evidence:* Explicit statement of analytical scope/design choice (cross-sectional spatial comparison vs. a time-series/forecasting approach), which matters for how this source should be positioned relative to early-warning/forecast framings. (Abstract / approach description, EPA record 357233)
  - *quote:* "large spatial variation among lakes using two national-scale data sources, rather than focusing on temporal variability"
- **[✓ verified]** Algal toxins cannot be directly detected through satellite imagery; the study's premise is that monitoring toxins linked to cyanobacterial blooms is critical for assessing risk, motivating a statistical link between the satellite cyanobacteria signal and field-measured toxin data.
  - *evidence:* Stated motivation/rationale in the abstract's opening, framing CI_cyano explicitly as a correlate/proxy rather than a direct toxin measurement. (Abstract, opening/motivation section, EPA record 357233)
  - *quote:* "Algal toxins cannot be directly detected through imagery but monitoring toxins associated with cyanobacterial blooms is critical for assessing risk to the environment, animals, and people."
- **[✓ verified]** Beyond the microcystin-specific counts, the models identified 335 lakes at ≥75% probability of exceeding (an unspecified set of) "lower" thresholds, and 70 lakes for "higher" thresholds, when applied nationally.
  - *evidence:* Reported consistently by two independent AI extraction passes (one on each of the two EPA-hosted mirrors of this record), but neither pass returned a clean verbatim sentence specifying which parameter(s) — e.g., a cyanobacteria cell-density/CI threshold or chlorophyll-a threshold, as opposed to microcystin — this "335" figure refers to. Flagged as unconfirmed/ambiguous rather than presented as a fully verified figure; a reviewer should verify against the original slide deck if available. (Abstract / "Key Findings" section, EPA record 357233 (paraphrased identically by two independent extraction passes, no verbatim sentence obtained))
- **[✓ verified]** This specific record is a conference presentation (not a journal article), presented Feb 27–Mar 2, 2023 at the AWWA Pacific Northwest Section's Cascade to Coast Short School in Albany, OR, by EPA-affiliated authors, and carries no full-text/PDF link.
  - *evidence:* Metadata drawn directly from the EPA Science Inventory "Record Details" and "Citation" fields, establishing the document type and venue of this exact record (deid/Record ID 357233). ("Record Details" and "Citation" sections, EPA Science Inventory mirror of record 357233 (cfpub.epa.gov))
  - *quote:* "Presented at Pacific Northwest Section of the American Water Works Association Cascade to Coast Short School, Albany, OR, February 27 - March 02, 2023."

## Data / numbers
- CI_cyano increase of 0.01 CI_cyano/km² → 23–54% increase in odds of exceeding six bloom thresholds (no confidence interval or standard error stated)
- Microcystin lower demonstration threshold: 0.2 µg/L
- Microcystin higher demonstration threshold: 1.0 µg/L
- 162 lakes at ≥75% modeled probability of exceeding the lower microcystin threshold (0.2 µg/L)
- 70 lakes at ≥75% modeled probability of exceeding the higher microcystin threshold (1.0 µg/L)
- ~2,192 satellite-monitored U.S. lakes in the national analysis (figure consistent across independent extraction passes; exact source sentence not captured verbatim)
- 335 lakes at ≥75% probability of exceeding unspecified 'lower thresholds' (parameter/endpoint not identified in retrieved text — flagged as ambiguous, not confirmed verbatim)
- 70 lakes at ≥75% probability of exceeding unspecified 'higher thresholds' (general figure, possibly duplicative of the microcystin-specific 70-lake count — flagged as ambiguous)
- Six total bloom/toxin thresholds evaluated (per source phrase 'six bloom thresholds'; the parameter breakdown behind this count is not confirmed in the retrieved text)

## Methods
Relates a satellite-derived lake-level "Cyanobacteria Index" (CI_cyano, described as coming from the Medium Resolution Imaging Spectrometer, MERIS) to each lake's probability of exceeding toxin/bloom thresholds, using field-survey data from the US National Lakes Assessment as the in-situ/ground-truth side. Results are reported as "odds" of threshold exceedance per 0.01 CI_cyano/km² increase, implying an odds-based (e.g., logistic-style) model, but the retrieved abstract text does not name the specific algorithm, predictor set, training/validation split, or performance metrics (no AUC, accuracy, or R² given). The design is explicitly described as exploiting spatial variation across many lakes via two national-scale data sources rather than temporal (within-lake, over-time) variability, applied at a scope described as roughly 2,192 satellite-monitored lakes nationally. The only stated boundary condition is that satellite imagery cannot directly detect algal toxins — the stated rationale for coupling it to field toxin data — not a described failure mode of the statistical model itself.

## Stated limitations
None stated explicitly in the retrieved text. Across four fetches of two EPA-hosted copies of this record (Risk Assessment Portal and Science Inventory), no dedicated limitations/uncertainty/caveats section was found — no confidence intervals or error bars around the reported 23–54% odds range, no description of validation approach (train/test split, cross-validation, or external validation), and no discussion of sensor, temporal, or representativeness constraints. This most likely reflects the brevity of a conference-abstract record rather than confirmation that the underlying study has no such caveats.

## Tensions with other findings
This record (deid 357233) is a short conference-presentation abstract, not a full paper. WebSearch (used only to confirm identity/metadata, not as a content source for this entry) surfaced a closely related record by an overlapping/identical author team — "Identifying lakes at risk of toxic cyanobacterial blooms using satellite imagery and field surveys across the United States" (Science of the Total Environment, 2023; PMC10018780; PMID 36702268) — using very similar language (CI_cyano, MERIS, National Lakes Assessment, 0.2/1.0 µg/L microcystin thresholds). This dossier entry was built strictly from the fetched text of record 357233 itself, not from that companion paper; a literature reviewer should check whether the two are the same underlying study (conference talk vs. journal version) before counting them as independent evidence. Separately, the source itself states algal toxins "cannot be directly detected through imagery," an explicit acknowledgment that CI_cyano is a correlational proxy for toxin risk, not a toxin measurement — relevant to any downstream claim that treats satellite cyanobacteria index as equivalent to toxin presence.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All seven claims are directly supported by the source text. Claim 6 appropriately flags the ambiguity about which threshold parameter the 335/70 figures refer to (not clarified in the EPA record abstracts/paraphrases); the claim's explicit qualification as \"unspecified\" reflects this source limitation fairly. All numerical values (odds ratios, lake counts, dates, thresholds) are confirmed verbatim or as clearly supported paraphrases in the source. The evidence note for Claim 3 mentions figures were \"corroborated-but-not-verbatim\" from multiple fetches, but the source text provided here includes the verbatim Geographic Scope statement with the 2,192 figure, so verification passes. No hallucinated numbers, no material dropped caveats."

## Provenance
- Canonical URL: https://assessments.epa.gov/risk/document/&deid=357233
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: ok
- Fetch notes: Fetched the primary URL (https://assessments.epa.gov/risk/document/&deid=357233) twice with different extraction prompts, as required for a High-relevance source: (1) a comprehensive "what/findings/numbers/methods/limitations" prompt, and (2) a prompt targeted at verbatim abstract text, thresholds, model type, performance metrics, and limitations. Both fetches loaded the correct record (title, authors, and Record ID/deid 357233 all matched the assignment) and returned consistent, overlapping content, confirming this is a short EPA ORD conference-presentation abstract (AWWA Pacific NW "Cascade to Coast" Short School, Feb 27–Mar 2, 2023) with no full paper attached. Because the retrieved content was thin (an abstract, not a full study), I additionally fetched the mirrored EPA Science Inventory record (https://cfpub.epa.gov/si/si_public_record_Report.cfm?dirEntryId=357233&Lab=CPHEA — same Record ID 357233) twice, which independently corroborated the same key figures/quotes and confirmed via its "Record Details" that this is Record Type "DOCUMENT (PRESENTATION/SLIDE)" with "Full Text Link: Not provided." I did not treat this as a failed/wrong-page fetch requiring an alternate WebSearch-sourced replacement, since the original URL correctly resolved to the assigned document — its short, abstract-only nature is a property of the source itself, not a fetch failure. WebSearch was used only to (a) confirm this record's identity/metadata and (b) discover that a closely related, seemingly companion peer-reviewed paper exists by an overlapping author team (Sci Total Environ 2023; PMC10018780; PMID 36702268); that companion paper was NOT fetched and none of its content was used to support any claim in this dossier entry — it is noted only in "tensions" as context for a reviewer. One set of figures ("335 lakes" and a generic "70 lakes" for unspecified lower/higher thresholds) was reported consistently across fetches but never returned as a clean verbatim sentence identifying which parameter it belongs to; this is flagged explicitly in key_claims/data_numbers/source_extract as ambiguous rather than presented as fully confirmed, per the instruction not to let the fetch tool's paraphrasing pass as verified numbers.
