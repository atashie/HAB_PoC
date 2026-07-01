---
key: FED-078
title: What Are Probability Surveys?
authors_or_org: U.S. Environmental Protection Agency (EPA) — National Aquatic Resource Surveys (NARS) program
year: Page footer states "Last updated on April 15, 2026"; no original publication date is given on the page.
url: https://www.epa.gov/national-aquatic-resource-surveys/what-are-probability-surveys
access_date: 2026-07-01
tier: FED
source_type: Government agency web page (EPA program explainer / FAQ page, non-peer-reviewed)
categories: [in-situ-and-weather-data]
relevance: Low
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# What Are Probability Surveys?

**What it is.** A short EPA "National Aquatic Resource Surveys" (NARS) program webpage that defines "probability surveys" (random-site-selection sample/statistical surveys) as the general survey-design concept NARS uses to assess the condition of the nation's waters, with a map of the 2013-2014 National Rivers and Streams Assessment sites as its sole illustrative example.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Probability (a.k.a. sample- or statistical-) surveys select sampling sites randomly, and each site represents a specific portion of the total resource/population of interest (e.g., all river and stream length in the nation).
  - *evidence:* Stated directly as the page's core definition of the term 'probability survey' in the second body paragraph; no supporting data or citation is given, it is presented as a methodological definition. (Body text, paragraph 2 (page: 'What Are Probability Surveys?'))
  - *quote:* "In probability surveys (also known as sample-surveys or statistical surveys), sampling sites are selected randomly."
- **[✓ verified]** Because site selection is random/statistical, results from the sampled sites can be extrapolated to the entire population of interest, which the page says makes probability surveys well suited for unbiased assessment of a whole resource across large areas without monitoring every waterbody.
  - *evidence:* Asserted as a direct methodological consequence of random site selection; presented as a general statistical property, not tied to any specific empirical validation or error estimate in this text. (Body text, paragraph 2)
  - *quote:* "Because of the statistical nature of site selection, results from the sample population can be extrapolated to the entire population. For this reason, probability surveys are well suited for making unbiased assessments of the condition of an entire resource across large geographic areas without monitoring every waterbody."
- **[✓ verified]** EPA's National Aquatic Resource Surveys (NARS) use probability-based survey designs specifically to meet the objective of assessing the condition of the nation's waters.
  - *evidence:* Stated as the opening/framing sentence connecting the general concept of probability surveys to NARS's own program design. (Body text, paragraph 1)
  - *quote:* "The National Aquatic Resource Surveys (NARS) use probability-based survey designs in order to achieve the objectives of assessing the condition of the nation's waters."
- **[✓ verified]** Probability surveys are a general statistical method used across many fields (e.g., medical studies, political opinion polls) when a population of interest is too large to sample every individual/unit.
  - *evidence:* Given as contextual justification for why a random-sampling approach is used, by analogy to other disciplines; no specific medical or polling study is cited. (Body text, paragraph 1)
  - *quote:* "Probability surveys are widely used in many disciplines, such as in medical studies and political opinion polls, where information is needed about a population that is too large to allow every individual to be sampled."
- **[✓ verified]** As a worked example of the design, the 2013-2014 National Rivers and Streams Assessment randomly selected its original sampling sites so that they were distributed across the entire conterminous United States.
  - *evidence:* Given only as an image caption illustrating the general definition above; no site count, stratification detail, or statistical parameters (e.g., number of base sites, oversample rate) are included in the caption or surrounding text. (Map image caption)
  - *quote:* "Map of the United States showing the sites originally selected for sampling for the National Rivers and Streams Assessment 2013-2014. Sites are spread out across the entire conterminous U.S."

## Data / numbers
- No sample sizes, percentages, confidence levels, margins of error, or other quantitative statistics are stated anywhere on this page.
- Only date/identifier present: '2013-2014' — the survey cycle name of the National Rivers and Streams Assessment, shown in the map image caption; not attached to any numeric statistic.
- Footer date: page 'Last updated on April 15, 2026' (site metadata, not a study finding).

## Methods
The only "method" described is the general statistical concept of probability-based (random) site selection for survey sampling, contrasted implicitly with non-random/judgment-based site choice (the contrast is implied, not spelled out). The source states the method "works" for producing assessments that can be statistically extrapolated from a sample to an entire population/resource, and calls this "well suited for making unbiased assessments of the condition of an entire resource across large geographic areas without monitoring every waterbody." No specific algorithm (e.g., stratification scheme, spatially balanced design name, weighting formula), software, sample-size formula, or dataset details are named in this text. No discussion of where or how the method fails, underperforms, or requires caveats is present in this source.

## Stated limitations
The page states no limitations, caveats, or failure modes of probability surveys at all. It does not discuss: sources of bias (e.g., site non-response or inaccessibility and substitution), margin of error or confidence intervals, minimum sample size or statistical power needed for valid extrapolation, cost/logistics trade-offs versus targeted sampling, or the temporal representativeness of a single survey (i.e., whether a snapshot random sample captures time-variant conditions). It presents the method only in affirmative terms ("unbiased assessments"), with no discussion of when or why it could underperform.

## Tensions with other findings
This page makes a general design-based statistics claim — that random site selection yields "unbiased assessments" extrapolatable to a whole population — but this is a claim about representativeness of the sampled *population/frame*, not a claim about temporal sensitivity. It does not address (and a reader should not assume it addresses) whether infrequent, multi-year probability-survey snapshots (e.g., NARS/National Lakes Assessment index-period visits) can characterize fast-changing, time-variant phenomena such as harmful algal blooms, which can emerge and dissipate on time scales far shorter than typical survey revisit cycles. Any use of this source to justify the adequacy of NARS-type in-situ data for HAB timing/early-warning purposes would be an inference beyond what this page itself claims, since the page never mentions blooms, chlorophyll, cyanotoxins, or temporal frequency at all.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All five claims are directly supported by the source text. The claims accurately represent the source material: the definition and methodology of probability surveys (Claims 1–2), NARS's use of this approach (Claim 3), the general interdisciplinary context (Claim 4), and the 2013-2014 NRSA as a worked example (Claim 5). No hallucinated numbers or significant dropped caveats detected."

## Provenance
- Canonical URL: https://www.epa.gov/national-aquatic-resource-surveys/what-are-probability-surveys
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched successfully on first attempt (no block, no wrong-page redirect). Ran WebFetch twice against the same primary URL: once for a comprehensive extraction and once explicitly requesting verbatim full-page text, to make sure no numeric/statistical content was paraphrased away. Both fetches returned consistent, matching content. The page is a short EPA explainer/FAQ page (title, one map image with caption, two body paragraphs, and a 'last updated' footer) — there is no additional substantive text, table, or figure beyond what is captured in source_extract; standard EPA site navigation/header/footer boilerplate was excluded as non-substantive. No redirect occurred, so url_used = resolved_url = the primary URL given.
