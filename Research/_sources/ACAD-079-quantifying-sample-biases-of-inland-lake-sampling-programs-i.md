---
key: ACAD-079
title: Quantifying sample biases of inland lake sampling programs in relation to lake surface area and land use/cover
authors_or_org: Tyler Wagner, Patricia A. Soranno, Kendra Spence Cheruvelil, William H. Renwick, Katherine E. Webster, Peter Vaux, Robbyn J. F. Abbitt (Quantitative Fisheries Center, Dept. of Fisheries and Wildlife, Michigan State University)
year: 2008
url: https://pubmed.ncbi.nlm.nih.gov/17724567/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (primary research, statistical/methodological study), Environmental Monitoring and Assessment (Springer)
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: abstract
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Quantifying sample biases of inland lake sampling programs in relation to lake surface area and land use/cover

**What it is.** A statistical/methodological study that quantifies systematic sampling bias in non-probability-based inland lake monitoring programs run by six U.S. state agencies (MI, WI, IA, OH, ME, NH), by comparing which lakes get monitored against the full census of lakes in each state (from the National Hydrography Dataset) with respect to lake surface area and surrounding land use/land cover (LULC).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Across all six study states, larger lakes have a consistently higher probability of being included in state-agency lake monitoring programs than smaller lakes.
  - *evidence:* Derived from generalized linear mixed models (GLMMs) comparing each state's monitored-lake list against a full census of lakes (from the National Hydrography Dataset) for that state; the size effect held for every one of the six states examined. (Abstract)
  - *quote:* "For all states, we found that larger lakes had a higher probability of being sampled compared to smaller lakes."
- **[✓ verified]** Sampling probability is related to surrounding land use/land cover (LULC), but a significant lake-size × LULC statistical interaction prevents the authors from isolating a clean 'main effect' of LULC; the overall qualitative pattern is that lakes most likely to be sampled tend to have high urban land use, high agricultural land use, high forest cover, or low wetland cover.
  - *evidence:* Based on GLMM interaction terms testing lake size together with surrounding LULC as joint predictors of a lake's probability of being sampled. (Abstract)
  - *quote:* "Significant interactions between lake size and LULC prohibit us from drawing conclusions about the main effects of LULC; however, in general lakes that are most likely to be sampled have either high urban use, high agricultural use, high forest cover, or low wetland cover."
- **[✓ verified]** Study design: state-monitored ('non-probability based') lakes from six state agencies were compared against a census population of all lakes (derived from the National Hydrography Dataset), and the probability of a lake being sampled was modeled using generalized linear mixed models.
  - *evidence:* This is the core method stated directly in the abstract. (Abstract / Methods (as described in abstract))
  - *quote:* "we compared state-monitored lakes to a census population of lakes derived from the National Hydrography Dataset. We then estimated the probability of lakes being sampled using generalized linear mixed models."
- **[✓ verified]** The authors conclude that data from non-probability-based lake surveys must be used cautiously when generalizing to the full population of lakes, and that probability-based survey designs are needed for unbiased, accurate estimates of lake status and trends at regional-to-national scales.
  - *evidence:* Stated as the paper's overarching conclusion/implication in the abstract. (Abstract / Conclusion)
  - *quote:* "data derived from non-probability-based surveys must be used with caution when attempting to make generalizations to the entire population of interest, and that probability-based surveys are needed to ensure unbiased, accurate estimates of lake status and trends at regional to national scales."
- **[✓ verified]** The study specifically examined LULC-related bias because surrounding land use is already an established driver of lake water quality, so biased selection of lakes by LULC context could distort water-quality conclusions drawn from monitoring-network data.
  - *evidence:* States the rationale for testing LULC (not just lake size) as a bias dimension. (Abstract)
  - *quote:* "We examined the biases associated with surrounding LULC because of the established links between LULC and lake water quality."
- **[✓ verified]** The publicly accessible text of this source (the PubMed abstract) contains no quantitative statistical results — no percentages, odds ratios/effect sizes, per-state sample sizes (numbers of lakes), or p-values are reported; only qualitative/directional findings are stated. No open-access full text or PDF of the paper (which would contain such numbers, plus Methods/Results tables and a Discussion/Limitations section) could be located.
  - *evidence:* Confirmed by a dedicated second-pass re-extraction of the PubMed page targeting numeric content, and independently corroborated by a Semantic Scholar bibliographic record for the same DOI, which shows the abstract field itself withheld and no open-access PDF link. (PubMed abstract page (re-extraction pass); Semantic Scholar API record for DOI 10.1007/s10661-007-9883-z)
  - *quote:* "Abstract: Not available (elided by publisher) ... OpenAccessPdf URL: Not provided (closed access)"

## Data / numbers
- Six (6) U.S. state monitoring agencies analyzed: Michigan, Wisconsin, Iowa, Ohio, Maine, New Hampshire (count of jurisdictions, not a measured statistic)
- Citation numbers only: Environmental Monitoring and Assessment, Volume 141, Issue 1-3, pages 131-147, published June 2008 (ePub 28 Aug 2007); DOI 10.1007/s10661-007-9883-z; PMID 17724567
- No quantitative results (percentages, odds ratios/effect sizes, per-state lake counts/sample sizes, confidence intervals, or p-values) for the sampling-probability GLMMs are present in the publicly accessible abstract text; this absence was explicitly checked for and confirmed via a targeted re-extraction and via a Semantic Scholar metadata check — no baseline or uncertainty values are stated in the material we could access, so none are reported here rather than estimated.

## Methods
Non-probability ('targeted'/agency-selected) lake lists from six U.S. state monitoring programs (Michigan, Wisconsin, Iowa, Ohio, Maine, New Hampshire) were compared against a census population of all lakes in those states, drawn from the National Hydrography Dataset (NHD). Generalized linear mixed models (GLMMs) were used to estimate each lake's probability of being sampled as a function of lake surface area and surrounding land use/land cover (LULC), including a lake-size x LULC interaction term. Per the abstract, the approach reliably detects a lake-size-driven sampling bias (larger lakes over-represented) consistently across all six states; it is explicitly reported as unable to cleanly separate a 'main effect' of LULC on sampling probability because of a significant interaction between lake size and LULC, so only a composite/qualitative LULC pattern (bias toward high urban, high agricultural, high forest, or low wetland cover) is reported rather than an isolated LULC effect size.

## Stated limitations
The abstract itself states one core analytical limitation: a significant statistical interaction between lake size and surrounding LULC "prohibit[s]" the authors "from drawing conclusions about the main effects of LULC" — i.e., they cannot cleanly attribute sampling bias to specific LULC categories independent of lake size. Beyond this, the study's scope is implicitly bounded to six specific U.S. state agency monitoring programs and to the two predictors examined (lake area and surrounding LULC); no other limitations can be confirmed because only the abstract was accessible — any additional caveats the authors may state in the full Discussion/Limitations section (which was not reachable with the tools available) are not reported here to avoid fabrication.

## Tensions with other findings
This is not a HAB-specific ecological finding but a monitoring-design/statistics paper, so it does not directly contradict any HAB causal claim. However, it creates an important tension for HAB analyses (including this project's) that draw 'in-situ aquatic data' from state DEQ lake-monitoring programs or aggregators like the Water Quality Portal as though those records represent a random/unbiased sample of lakes: this source shows such agency-run networks are systematically skewed toward larger lakes and toward particular surrounding land-use contexts (high urban/agricultural/forest cover or low wetland cover), which could bias the population of lakes available for training or validating a fused remote-sensing + in-situ HAB model and limit how far its conclusions generalize to smaller or wetland-dominated water bodies. A WebSearch for related literature also surfaced a 2019 paper, Stanley et al., 'Biases in lake water quality sampling and implications for macroscale research' (Limnology and Oceanography), whose title suggests this same sampling-bias concern was still an active, unresolved topic in the field roughly a decade later — noted here only by title/venue from the search result, since its content was not fetched or verified.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All six claims are directly supported by the source text. The source is limited to a PubMed abstract and access metadata (no full-text PDF retrieved), but all claims stay within that scope and are traceable to specific passages. Claim 6 explicitly addresses the availability (or lack thereof) of quantitative results and full-text access, which is confirmed by the source metadata showing closed access via Springer and failed attempts to retrieve ResearchGate/full-text versions. No numbers are hallucinated and no substantive caveats are dropped."

## Provenance
- Canonical URL: https://pubmed.ncbi.nlm.nih.gov/17724567/
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: ok
- Fetch notes: Primary URL (PubMed, https://pubmed.ncbi.nlm.nih.gov/17724567/) was fetched TWICE with different extraction prompts (one general/comprehensive, one targeting numeric/metadata detail); both returned the same complete abstract text verbatim, with no discrepancies to reconcile. Attempts to reach full text beyond the abstract were made given the High provisional relevance: (1) ResearchGate page for this paper returned HTTP 403 Forbidden; (2) the Springer publisher page (link.springer.com) redirected to a login/authorization wall (idp.springer.com) rather than showing content, indicating paywalled access; (3) a Semantic Scholar API query for the same DOI confirmed the abstract is withheld ('elided by publisher') and no open-access PDF is available. Given this, full_text_access is set to 'abstract' and all key_claims, data_numbers, methods, and stated_limitations above are drawn solely from the PubMed abstract text (plus bibliographic metadata visible on that page); no content from the paper's full Introduction, Results tables, Discussion, or Limitations sections could be verified and none is claimed.
