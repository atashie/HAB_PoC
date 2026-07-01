---
key: ACAD-052
title: Forecasting short-term cyanobacterial blooms in Lake Taihu, China, using a coupled hydrodynamic-algal biomass model
authors_or_org: Wei Li; Boqiang Qin; Guangwei Zhu
year: 2014
url: Switched from the provided ResearchGate aggregator URL to the paper's DOI/publisher record (doi.org/10.1002/eco.1402 → onlinelibrary.wiley.com/doi/10.1002/eco.1402, Ecohydrology, Wiley). Both the ResearchGate page and the Wiley publisher page returned HTTP 403 Forbidden to automated fetch; usable abstract-level content was instead obtained via the CrossRef API (api.crossref.org/works/10.1002/eco.1402) and the Semantic Scholar Graph API, corroborated by repeated WebSearch queries.
access_date: 2026-07-01
tier: ACAD
source_type: peer-reviewed journal article
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Forecasting short-term cyanobacterial blooms in Lake Taihu, China, using a coupled hydrodynamic-algal biomass model

> Note: provisional URL was resolved to a primary source. Original: https://www.researchgate.net/publication/261331548_Forecasting_short-term_cyanobacterial_blooms_in_Lake_Taihu_China_using_a_coupled_hydrodynamic-algal_biomass_model

**What it is.** A 2014 peer-reviewed journal article (Ecohydrology, Wiley) by Li, Qin & Zhu describing an operational short-term (3-day-ahead) forecasting system for cyanobacterial blooms in Lake Taihu, China, that couples a 3-D hydrodynamic-algal biomass numerical model with a statistical bloom-occurrence probability model, initialized from a network of 18 monitoring buoys plus boat surveys and validated against remote sensing and independent boat-survey data from 2009-2010.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The paper presents an operational short-term (3-day-ahead) cyanobacterial bloom forecasting system for Lake Taihu built from two coupled components: a three-dimensional hydrodynamic–algal biomass numerical model, and a separate statistical model that forecasts the probability of bloom occurrence.
  - *evidence:* This is the paper's core method as stated in its title and abstract, corroborated identically across CrossRef metadata and multiple independent WebSearch extractions of the abstract. (Title / Abstract)
  - *quote:* "a three-dimensional, coupled hydrodynamic-algal biomass model and a probability of bloom occurrence forecasting model"
- **[✓ verified]** The model is initialized with real observed data: initial algal chlorophyll-a concentrations come from a network of 18 automatic monitoring buoys plus boat-survey measurements, not from remote sensing alone.
  - *evidence:* Stated as the model's input/initialization data in the abstract; the '18 automatic monitoring buoys' phrase recurred verbatim across independent search extractions. (Abstract)
  - *quote:* "18 automatic monitoring buoys"
- **[✓ verified]** The forecast mechanism works by combining calculated/predicted hydrological and meteorological scenarios over the next 3 days to simulate the spatial distribution of algal concentration, with bloom probability then predicted from a model using algal biomass weight, wind velocity, and weather condition as inputs.
  - *evidence:* Paraphrase of the abstract's description of the two-stage forecast pipeline (hydrodynamic-biomass simulation feeding a probability model); phrasing was stable across multiple independent search extractions. (Abstract)
  - *quote:* "the weight of algal biomass, wind velocity, and weather condition"
- **[⚠ partial]** The governing equations of cyanobacterial bloom dynamics in the shallow lake are solved using the finite volume method on an unstructured computational mesh, chosen to fit the lake's irregular shoreline while preserving conservation properties.
  - *evidence:* Numerical-method detail recurring consistently across independent WebSearch extractions of the paper's methods; not independently confirmed against the original PDF since full text was inaccessible. (Methods (as summarized in abstract-derived text))
  - *quote:* "finite volume method"
  - *reviewer:* Finite volume method and unstructured mesh are confirmed by the source; however, the phrase 'while preserving conservation properties' is not explicitly stated in the source text. This is an inference about a known property of the finite volume method, not a claim made in the accessible source material.
- **[✓ verified]** The system was applied and tested by forecasting bloom occurrence 3 days ahead in Lake Taihu across the bloom seasons (April–September) of both 2009 and 2010.
  - *evidence:* States the study's validation window; consistent across all abstract extractions. (Abstract)
  - *quote:* "April to September in 2009 and 2010"
- **[✓ verified]** When checked against independent remote-sensing images and independent boat-survey data, the 3-day-ahead bloom forecasts were more than 80% accurate.
  - *evidence:* This is the paper's headline validation result, given as a single point accuracy figure with no stated uncertainty interval or comparison baseline in any of the accessible text (CrossRef abstract quote and repeated WebSearch abstract extractions all state the same bare figure). (Abstract)
  - *quote:* "the accuracy of these bloom forecasts was more than 80%"
- **[✓ verified]** The study is motivated by Lake Taihu's status as China's third-largest freshwater lake, a drinking-water source for roughly five million people, which has experienced serious cyanobacterial blooms over the preceding ~30 years severe enough to degrade drinking-water quality and trigger water-supply crises.
  - *evidence:* Background/motivation framing given in the abstract; treated as the paper's own contextual claim, not independently verified against a separate source here. (Abstract)
  - *quote:* "the third largest freshwater lake of China"

## Data / numbers
- 18 automatic monitoring buoys used (plus boat-survey measurements) to initialize algal chlorophyll-a concentrations
- 3-day forecast horizon (lead time) for bloom occurrence/distribution
- Validation period: April–September, in both 2009 and 2010
- >80% forecast accuracy against independent remote-sensing imagery and boat-survey data (no confidence interval, error bar, or baseline/persistence comparison stated in the accessible text)
- Lake Taihu described as the 3rd-largest freshwater lake in China, supplying drinking water to approximately five million people (contextual, not a study result)
- Ecohydrology, 2014, Vol. 7, Issue 2, pp. 794–802; DOI 10.1002/eco.1402; published online 13 June 2013, in print April 2014; 32 references (CrossRef metadata)

## Methods
Coupled, physically-based 3-D hydrodynamic–algal biomass numerical model (governing equations for cyanobacterial bloom dynamics in a shallow lake, discretized with the finite volume method on an unstructured mesh to handle irregular shoreline geometry) feeding into a separate empirical/statistical model that forecasts bloom-occurrence probability from algal biomass weight, wind velocity, and weather condition. Initialized from real in-situ data (18 automatic monitoring buoys plus boat-survey chlorophyll-a measurements) combined with predicted hydrological/meteorological scenarios over a 3-day forecast window. Validated (where the source states it "works") by comparing 3-day-ahead forecasts against independent MODIS/remote-sensing imagery and independent boat-survey observations for the bloom seasons (April–September) of 2009 and 2010 in Lake Taihu, reporting >80% forecast accuracy. No information on where/how the model fails, its error distribution, or performance outside this lake/season/horizon was recoverable from the accessible text (full Methods/Results/Discussion sections were behind the Wiley paywall and could not be fetched).

## Stated limitations
Full text (Methods/Results/Discussion/Limitations sections) could not be retrieved — the Wiley publisher page and the ResearchGate aggregator page both blocked automated fetch (HTTP 403), and no open-access mirror was found. Only the abstract was recoverable, so any limitations the authors themselves discuss in the body of the paper are unknown and not represented here. Within the abstract itself, the claims are implicitly bounded: the forecast horizon tested is only 3 days ahead; the system was validated in only one lake (Taihu); the validation window covers only two bloom seasons (April-September of 2009 and 2010); and the reported ">80% accuracy" figure is stated as a bare point estimate with no confidence interval, error distribution, or explicit comparison against a naive/persistence/climatology baseline in any of the text retrieved. Generalizability to other lakes, other seasons/years, longer lead times, or lakes without a comparable dense buoy network (18 units) cannot be assessed from the accessible text.

## Tensions with other findings
This is a physically-based, process-model (hydrodynamic + biomass PDE) approach requiring a dense in-situ telemetry network (18 buoys) for initialization, which contrasts with purely statistical/ML or satellite-only HAB forecasting approaches likely elsewhere in this literature review; it suggests high (>80%) short-term forecast skill is achievable, but potentially at an infrastructure cost that may not be replicable in lakes lacking comparable monitoring investment — a relevant contrast for any proof-of-concept that leans on satellite plus sparse in-situ data fusion rather than dense buoy telemetry. Note this tension is this analyst's contextual observation given the limited (abstract-only) text retrieved, not a comparison the source itself makes explicit.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** Six of seven claims are directly supported by explicit statements in the source text with high fidelity. One claim (Claim 4) is marked partial because while the source confirms the finite volume method and unstructured mesh design to fit irregular boundaries, the phrase 'preserving conservation properties' is an inference about the method's theoretical properties rather than an explicit statement in the source text. All numerical figures trace directly to the source. No hallucinated numbers or dropped caveats detected."

## Provenance
- Canonical URL: Switched from the provided ResearchGate aggregator URL to the paper's DOI/publisher record (doi.org/10.1002/eco.1402 → onlinelibrary.wiley.com/doi/10.1002/eco.1402, Ecohydrology, Wiley). Both the ResearchGate page and the Wiley publisher page returned HTTP 403 Forbidden to automated fetch; usable abstract-level content was instead obtained via the CrossRef API (api.crossref.org/works/10.1002/eco.1402) and the Semantic Scholar Graph API, corroborated by repeated WebSearch queries.
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Provided URL is a ResearchGate aggregator page; WebFetch on it returned HTTP 403 Forbidden on two separate attempts (with two different extraction prompts). WebSearch identified the primary/publisher record: Li, Qin & Zhu (2014), Ecohydrology 7(2):794-802, DOI 10.1002/eco.1402 (Wiley). WebFetch of the publisher page itself (onlinelibrary.wiley.com/doi/10.1002/eco.1402, plus /doi/abs/ and /doi/full/ variants, plus the DOI resolver which redirects there) returned HTTP 403 Forbidden every time — Wiley blocks automated fetch entirely. WebFetch of the ADS abstract page and the Semantic Scholar paper page both returned blank/empty content (JS-rendered, not captured). WebFetch of the Semantic Scholar Graph API succeeded and returned bibliographic metadata only (title/authors/year/external IDs) with the abstract field explicitly marked closed-access/unavailable. WebFetch of Unpaywall's API errored (422 — no OA copy indexed). WebFetch of the CrossRef API (api.crossref.org/works/10.1002/eco.1402) succeeded and returned official bibliographic metadata plus two short direct quotes drawn from the abstract. These were cross-checked against, and are consistent with, abstract-level phrasing that recurred stably (often with matching quoted fragments) across five-plus independent WebSearch queries targeting this exact title/DOI. No legal open-access full-text mirror (PMC, preprint, institutional repository, or author page) could be located, so no Methods/Results/Discussion/Limitations section beyond the abstract was recoverable. IMPORTANT EXCLUSION: some WebSearch result-list summaries introduced numbers (a "72%/65% hit rate for blooms >100 km²" figure, and a "cyanobacterial fluorescence... 1/4/7-day" forecasting description) that on inspection belong to two DIFFERENT co-listed papers (a 2025 Sustainability article, DOI 10.3390/su17188376, and a bioRxiv preprint), not to ACAD-052 — these were deliberately excluded from this dossier to avoid cross-paper conflation. Net result: abstract-only access, assembled from CrossRef + Semantic Scholar metadata plus corroborated WebSearch snippets, no clean single full-page fetch was possible for this paywalled paper.
