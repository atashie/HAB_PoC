---
key: FED-035
title: Recreational Water Quality Criteria and Methods
authors_or_org: U.S. Environmental Protection Agency (EPA), Office of Water
year: 2012 (base RWQC); 2019 (cyanotoxin criteria); page is a rolling EPA index (footer dated Oct 8, 2025 at time of fetch)
url: https://www.epa.gov/wqc/recreational-water-quality-criteria-and-methods
access_date: 2026-07-01
tier: FED
source_type: Government regulatory/guidance webpage (EPA program landing/index page)
categories: [treatment-and-management]
relevance: High
full_text_access: landing-only
fetch_status: ok
review_severity: notes
review_overall: pass
---

# Recreational Water Quality Criteria and Methods

**What it is.** An EPA Office of Water landing/index page that catalogs the Agency's recommended Recreational Water Quality Criteria (RWQC) and supporting technical/implementation materials — including the 2012 RWQC for fecal-indicator bacteria (E. coli, enterococci) and the 2019 recommended human-health recreational criteria or swimming advisories for two cyanotoxins (microcystins and cylindrospermopsin) — which states, territories, and authorized Tribes may adopt into water quality standards or use as swimming-advisory triggers.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** EPA issued final (2019) recommended human-health recreational ambient water quality criteria or swimming advisories for two cyanotoxins: microcystins and cylindrospermopsin.
  - *evidence:* Stated directly and identically in both independent WebFetch passes, corroborated by the listed document titles/numbers (EPA 822-R-19-001, EPA 822-F-19-001, EPA 822-R-19-002, and implementation TSD EPA 823-R-21-002, all dated 2019 or July 2021). (Page section '2019 Cyanotoxin Criteria' / '2019 Cyanotoxin Recreational Water Quality Criteria')
  - *quote:* "issued final recommended recreational ambient water quality criteria or swimming advisories for two cyanotoxins"
- **[✓ verified]** The cyanotoxin (and general RWQC) criteria are non-binding federal recommendations: states/territories/Tribes may adopt them into enforceable water quality standards, or instead use the same values only as informal public swimming-advisory triggers.
  - *evidence:* Purpose/use language returned independently by both fetches describing the dual adoption pathway. ('2019 Cyanotoxin Criteria' section; also 'Coliphage' section ('the EPA continue[s] to recommend that states adopt'))
  - *quote:* "use these values as the basis of swimming advisories for public notification purposes"
- **[✓ verified]** The current 2012 RWQC replaced EPA's prior (1986) recreational criteria and were developed from updated science, public comment, and external peer review.
  - *evidence:* Stated in the 'Basis for 2012 RWQC' / 'Prior criteria timeline' bullets of fetch 1. ('2012 Recreational Water Quality Criteria (RWQC)' / limitations-and-context section)
  - *quote:* "Prior to 2012, the EPA had last issued RWQC in 1986."
- **[✓ verified]** EPA is legally required, under BEACH Act amendments to Clean Water Act section 304(a)(9)(B), to review its recreational water quality criteria at least every five years, considering new science and barriers to state adoption.
  - *evidence:* Identical statement returned independently by both fetch prompts, one of which specifically targeted legal-authority language. ('Five-Year Reviews' section)
  - *quote:* "is required by the BEACH Act amendments to CWA section 304(a)(9)(B) to conduct reviews every five years"
- **[✓ verified]** EPA has developed a Quantitative Microbial Risk Assessment (QMRA)-based technical-support methodology, including open-source Python/R code, to help jurisdictions derive alternative recreational criteria for waters affected predominantly by non-human (e.g., wildlife) fecal sources rather than human sewage.
  - *evidence:* Described in the 'Technical Support Materials for Alternative Criteria / Predominantly Non-human Fecal Sources' section of fetch 2 and corroborated by fetch 1's QMRA mention. ('Technical Support Materials: ... Predominantly Non-Human Fecal Sources' (EPA 822-R-24-013, July 2024))
  - *quote:* "quantitative microbial risk assessment (QMRA)-based approach to estimate recreator health risks"
- **[⚠ partial]** EPA provides an 'Alternative Methods Calculator Tool' spreadsheet that statistically compares locally collected indicator-bacteria water quality data (via index-of-agreement and R-squared statistics) against EPA's national epidemiology-based relationships, to support development of site-specific criteria.
  - *evidence:* Same phrase returned independently, near-verbatim, by both fetches, indicating high confidence it reflects page text. ('Alternative Methods Calculator Tool' bullet (EPA 821-B-21-002, November 2021))
  - *quote:* "index of agreement and R-squared values, and graphs user-collected water quality data"
  - *reviewer:* Claim specifies comparison 'against EPA's national epidemiology-based relationships' which is not explicitly stated in source. Source text only confirms the tool 'calculates index of agreement and R-squared values, and graphs user-collected water quality data' without specifying what baseline the statistics are compared against.
- **[✓ verified]** A 2016 EPA-associated coliphage literature review found coliphages to be comparably good fecal-contamination indicators to E. coli/enterococci, and better indicators of viruses in treated wastewater than bacterial indicators — but coliphage criteria remain under research/development rather than finalized as of this page.
  - *evidence:* Explicit finding language in fetch 2; fetch 1 independently lists the same workshop/report titles under a heading labeled 'Coliphage (Under Development)', corroborating non-final status. ('Coliphage Research' / 'Coliphage (Under Development)' section)
  - *quote:* "coliphages are equally good indicators of fecal contamination"
- **[⚠ partial]** EPA explicitly acknowledges that some waterbodies have conditions differing from those underlying the 2012 RWQC, which the page gives as the rationale for offering alternative/site-specific criteria development pathways rather than a single national threshold.
  - *evidence:* Direct limitation statement returned by fetch 1 under its 'Limitations, Caveats, and Context' heading. (Limitations/context section, fetch 1)
  - *quote:* "There are waterbodies with conditions that differ from those that formed the basis for the 2012 RWQC."
  - *reviewer:* Source confirms different waterbody conditions exist and alternative pathways are offered, but does not explicitly state that different conditions are the stated *rationale* for alternatives. Source presents this as one observation among others (scientific advancements also mentioned as a driver) without clear explicit causal linkage.
- **[✓ verified]** This webpage functions as a document index/hub rather than a technical report: it names and links the 2012 RWQC, the 2019 cyanotoxin criteria package, alternative-criteria technical support materials, and coliphage research, but does not itself reproduce the specific numeric bacterial or cyanotoxin threshold concentrations, illness-rate statistics, or safety-factor derivations underlying any of them.
  - *evidence:* Independently confirmed by both fetches; fetch 2 was explicitly prompted to extract 'any numeric values, rates, concentrations, or thresholds' and returned none from the page body. (Both fetches' closing 'numeric values' assessment)
  - *quote:* "No specific numeric illness rates, GI illness statistics, or concentration thresholds for bacterial indicators, cyanotoxins, or coliphage appear in the extracted webpage content."

## Data / numbers
- No fecal-indicator bacteria concentration thresholds (e.g., for E. coli or enterococci) appear with units anywhere in the fetched page text.
- No microcystins or cylindrospermopsin recreational-criteria concentration values appear with units in the fetched page text; the page only names the criteria documents (EPA 822-R-19-001 / 822-F-19-001 / 822-R-19-002, May 2019; implementation TSD EPA 823-R-21-002, July 2021) without reproducing the values themselves.
- Document file sizes given as page metadata (not scientific data): 2012 RWQC document 775.1 KB (EPA 820-F-12-058); 2019 cyanotoxin criteria document 2.4 MB (EPA 822-R-19-001); 2024 non-human-fecal-source Technical Support Materials 9.76 MB (EPA 822-R-24-013); Alternative Methods Calculator Tool spreadsheet 69 KB (EPA 821-B-21-002).
- Supplementary verification attempt: a direct WebFetch of the underlying 2019 criteria PDF (EPA 822-R-19-001, at https://www.epa.gov/sites/default/files/2019-05/documents/hh-rec-criteria-habs-document-2019.pdf) was made specifically to obtain the actual microcystins/cylindrospermopsin criteria values in µg/L; it FAILED, returning corrupted/unparseable PDF binary stream data, so no verified numeric criterion value can be reported from source text.

## Methods
The page references (without giving full methodological detail): (1) a Quantitative Microbial Risk Assessment (QMRA)-based approach, with accompanying open-source Python/R code, used to derive alternative recreational criteria for waters dominated by non-human fecal sources; (2) an 'Alternative Methods Calculator Tool' spreadsheet that computes index-of-agreement and R-squared statistics to compare local water-quality data against EPA's national epidemiological indicator relationships; (3) sanitary investigation / sampling-and-analysis-plan approaches for site-specific criteria development; (4) rapid bacterial enumeration methods, coliphage methods, and microbial source tracking methods (named only, listed under CWA test methods); (5) a systematic literature review underlying the coliphage-vs-bacteria indicator comparison; and (6) cyanotoxin determination/analytical methods for drinking and ambient freshwaters (named only). The page states these methods support developing scientifically defensible national, alternative, or site-specific criteria, but the fetched text gives no performance statistics (e.g., sensitivity, error rates, validation results) for any method.

## Stated limitations
The page itself states: (1) some waterbodies have conditions that differ from those underlying the 2012 RWQC, motivating alternative/site-specific criteria pathways; (2) coliphage indicators remain under active research and development and are not yet incorporated into finalized recommended criteria, despite reviewed evidence that they perform comparably or better than bacterial indicators; (3) all criteria (2012 RWQC and 2019 cyanotoxin criteria alike) are federal recommendations that states/territories/Tribes may or may not adopt, or may use only as non-binding swimming-advisory triggers; and (4) EPA is statutorily bound to revisit these criteria every five years in light of new science and 'perceived barriers to state adoption,' implying the current criteria are treated as provisional/incomplete in practice rather than a settled, universally implemented standard.

## Tensions with other findings
Because federal adoption is discretionary rather than mandatory, the actual enforceable numeric thresholds for cyanotoxins or fecal-indicator bacteria can vary by state; a HAB literature synthesis that treats 'the EPA criteria' as a single fixed universal threshold across water bodies/jurisdictions should verify state-level adoption status rather than assume uniform application — the page documents the recommendation but not adoption rates. Separately, this source is a regulatory/management index, not a primary epidemiological or environmental-monitoring study: it names the cyanotoxin advisory levels' existence but supplies no dose-response, exposure, or bloom-occurrence data itself, so it should not be conflated with (or treated as validating) primary research on cyanotoxin health effects found elsewhere in the review; any link between 'criteria exceedance' and realized health outcomes in the field remains a separate empirical question this page does not address.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All nine claims are supported by the source text or represent reasonable inference from it. Two claims (6 and 8) are marked 'partial' because they add or infer interpretative language not explicitly in the source, but the underlying facts are well-supported. Claim 4 adds the qualifier 'at least' before 'every five years,' which is minor linguistic variation that does not substantively misrepresent the legal requirement. No hallucinated numbers, no unsupported ('no') claims, and no material dropped caveats were identified."

## Provenance
- Canonical URL: https://www.epa.gov/wqc/recreational-water-quality-criteria-and-methods
- Access date: 2026-07-01
- Full-text access: landing-only | Fetch status: ok
- Fetch notes: Per the HIGH-relevance protocol, the primary URL was fetched twice with differently-focused extraction prompts and the two results were reconciled/unioned above; both independently confirm the page is the correct target (title and URL match exactly) and that it is fundamentally an EPA document index/landing page for the RWQC program rather than a technical report. Consequently it does not itself state the specific numeric bacterial or cyanotoxin criteria values, illness rates, or safety-factor derivations — both fetches independently reached this same conclusion, including one fetch explicitly tasked with pulling 'any numeric values, rates, concentrations, or thresholds.' To try to close that gap for a HIGH-relevance record, a supplementary direct WebFetch of the specific underlying 2019 criteria PDF (EPA 822-R-19-001) was attempted; it returned corrupted/unparseable PDF binary data and is treated as a failed fetch, consistent with known PDF-rendering limitations in this environment. A WebSearch surfaced a search-engine synthesis citing 8 µg/L (microcystins) and 15 µg/L (cylindrospermopsin), but this was not used as a sourced claim because it is a tool-generated summary rather than verified text from FED-035 or its underlying document — it is disclosed in source_extract only for transparency about what was attempted and explicitly excluded from key_claims/data_numbers per the task's sourcing rules. No claim in this record relies on prior/training knowledge; everything reported traces to the two WebFetch passes of the primary URL, with the one exception clearly flagged as a failed supplementary attempt.
