---
key: ACAD-024
title: Comparison of Eulerian and Lagrangian transport models for harmful algal bloom forecasts in Lake Erie
authors_or_org: Xing Zhou, Mark D. Rowe, Qianqian Liu, Pengfei Xue
year: 2023
url: https://www.sciencedirect.com/science/article/pii/S1364815223000270
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (Environmental Modelling &amp; Software, Elsevier), Vol. 162, Article 105641
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Comparison of Eulerian and Lagrangian transport models for harmful algal bloom forecasts in Lake Erie

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/abs/pii/S1364815223000270

**What it is.** A 2023 peer-reviewed modeling study (Zhou, Rowe, Liu &amp; Xue, Environmental Modelling &amp; Software, DOI 10.1016/j.envsoft.2023.105641) that compares three 3-D transport-model approaches - a Lagrangian particle model (LPM), an Eulerian tracer model (ETM), and a hybrid property-carrying particle model (PCPM) - for short-term (24-240 hour) hindcast forecasting of cyanobacterial harmful algal bloom (CHAB) intensity and spatial distribution in Lake Erie. Model hindcasts are evaluated against ESA Sentinel-3 OLCI satellite bloom imagery across the 2017-2019 bloom seasons.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study evaluates three transport-model approaches for Lake Erie CHAB forecasting: a Lagrangian particle model (LPM), an Eulerian tracer model (ETM), and a property-carrying particle model (PCPM) using a hybrid Eulerian-Lagrangian approach.
  - *evidence:* Stated directly as the paper's core study design in the abstract. (Abstract)
  - *quote:* "a Lagrangian particle model (LPM), 2) an Eulerian tracer model (ETM), and 3) a property-carrying particle model (PCPM) that utilizes the hybrid Eulerian-Lagrangian approach"
- **[✓ verified]** Model hindcasts (24 to 240 hours ahead) were evaluated against Sentinel-3 OLCI satellite bloom-detection imagery for every CHAB occurrence across three consecutive bloom seasons, 2017-2019.
  - *evidence:* Stated as the paper's validation data source and evaluation design in the abstract. (Abstract)
  - *quote:* "We evaluated the models' performance against the latest high-resolution satellite product from the European Space Agency's Sentinel-3 OLCI sensor over 24- to 240-h hindcasts for each CHAB occurrence in three consecutive CHAB seasons (2017–2019)."
- **[✓ verified]** All three transport models (LPM, ETM, PCPM) achieve comparable levels of hindcast accuracy in statistical skill assessments - no model is dramatically better across the board.
  - *evidence:* Directly stated conclusion of the model comparison in the abstract. (Abstract)
  - *quote:* "statistical skill assessments show that these three transport models attain comparable levels of hindcast accuracy"
- **[✓ verified]** The Eulerian tracer model and the hybrid property-carrying particle model perform as well as, or better than, the Lagrangian particle model, which the authors present as support for building more biological realism into future operational forecast models via Eulerian or hybrid approaches.
  - *evidence:* Presented as the paper's headline interpretive finding/implication in the abstract. (Abstract)
  - *quote:* "the fact that the ETM and PCPM perform as well as or better than the LPM sets up a promising path to developing more biological realism in future operational forecast models using Eulerian or hybrid approaches"
- **[✓ verified]** The study attributes short-term (day-to-day and within-day) variability in CHAB fields to the relative contributions of horizontal transport, vertical turbulent mixing, and algal buoyancy, and stresses that short-term forecast skill depends heavily on how fast lake currents respond to weather-scale wind events.
  - *evidence:* Stated as a specific analytic focus/finding in the abstract. (Abstract)
  - *quote:* "We examined the relative contributions of horizontal transport, vertical turbulent mixing, and algal buoyancy on the CHAB inter- and intra-day variability. In the short-term forecast, we emphasize the highly dynamic reaction of currents to weather-scale wind events that are crucial to CHAB transport."
- **[✓ verified]** Lake Erie has experienced a re-emergence of cyanobacterial HABs since the early 2000s, with impacts on drinking water, human health, fisheries, tourism, and water quality, framed by the authors as the motivation for improved CHAB forecast modeling.
  - *evidence:* Background/motivation statement opening the abstract; contextual rather than a novel empirical finding of this study. (Abstract)
  - *quote:* "Lake Erie has experienced a re-emergence of cyanobacterial harmful algal blooms (CHABs) since the early 2000s, posing significant socioeconomic and ecological consequences that impact drinking water, human health, fisheries, tourism, and water quality."

## Data / numbers
- 24 to 240 hours — hindcast/forecast horizon evaluated for each CHAB occurrence (Abstract)
- 2017–2019 — three consecutive CHAB seasons used for hindcast evaluation (Abstract)
- 3 transport models compared: Lagrangian particle model (LPM), Eulerian tracer model (ETM), property-carrying particle model (PCPM) (Abstract)
- Environmental Modelling & Software, Vol. 162, Article 105641, published April 2023; DOI 10.1016/j.envsoft.2023.105641 (bibliographic identifiers, via Crossref API)

## Methods
Per the abstract: three transport-model configurations for simulating Lake Erie CHAB fields are compared - (1) a Lagrangian particle model (LPM), (2) an Eulerian tracer model (ETM) that represents planktonic biomass/chlorophyll as a tracer concentration field, and (3) a property-carrying particle model (PCPM), a hybrid Eulerian-Lagrangian approach. Each model is run as 24- to 240-hour hindcasts for every CHAB occurrence across three consecutive bloom seasons (2017, 2018, 2019), with skill assessed statistically against the "latest high-resolution satellite product from the European Space Agency's Sentinel-3 OLCI sensor." The abstract states the analysis also decomposes the relative contributions of horizontal transport, vertical turbulent mixing, and algal buoyancy to CHAB inter- and intra-day variability, emphasizing the fast/dynamic response of lake currents to weather-scale wind events during short-term forecasting. Result: all three models "attain comparable levels of hindcast accuracy," and the ETM and PCPM perform "as well as or better than" the LPM. Exact statistical skill metrics, error definitions, hydrodynamic driver-model details, and grid/particle configuration are in the paywalled full text and were not retrievable for this dossier - the abstract does not itself give numeric skill values (e.g., no RMSE, correlation, or bias figures appear in the accessible text).

## Stated limitations
The accessible text (abstract only) does not contain an explicit limitations section - that discussion is presumably in the paywalled Discussion/Conclusion, which could not be retrieved for this dossier. The closest thing to a caveat in the abstract is definitional: the result is framed only as "comparable levels of hindcast accuracy" among the three models (not a claim that any model achieves high absolute accuracy), and the ETM/PCPM finding is explicitly framed as motivation for "developing more biological realism in future operational forecast models," implying the authors regard current transport-only representations (across all three model types) as an interim step rather than a finished, sufficient solution. No exact skill-score values, uncertainty bounds, or explicit authors'-stated caveats/assumptions could be confirmed from the accessible text.

## Tensions with other findings
Full text was unavailable, so direct contradiction with specific other HAB sources cannot be verified from this dossier alone. At the abstract level, the paper's central finding - that Eulerian (ETM) and hybrid (PCPM) transport models match or exceed a Lagrangian particle model's (LPM) hindcast skill - sits in tension with treating Lagrangian particle tracking as the default/preferred approach for short-term bloom-transport forecasting (a common framing encountered elsewhere in Great Lakes HAB-forecasting literature during search). The authors' own abstract argues that choice is not obviously the most defensible one on hindcast-skill grounds alone; this is the source's own framing, not a numeric head-to-head against one specific named competing publication. Also worth flagging for a HAB review: this paper addresses spatial/transport forecasting of an already-detected bloom (where/how it will move), which is a different decision problem from bloom onset or risk-level prediction (whether/when a bloom will occur) addressed by other categories of HAB literature - correlation between transport-model skill and broader "risk forecasting" utility should not be assumed.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All six claims are directly supported by the verbatim abstract text. No hallucinated numbers detected. No material caveats were dropped. The claims accurately capture the study design (three models), evaluation approach (24-240 hour hindcasts vs. Sentinel-3 OLCI satellite data, 2017-2019), key findings (comparable model skill, ETM/PCPM competitive with LPM), process focus (transport, mixing, buoyancy contributions), and motivation (Lake Erie CHAB re-emergence since early 2000s). Cautious language in the source (e.g., "sets up a promising path") is appropriately reflected in claim reporting rather than overclaimed."

## Provenance
- Canonical URL: https://www.sciencedirect.com/science/article/pii/S1364815223000270
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: STATUS: partial / abstract-only. The primary ScienceDirect URL is genuinely bot-blocked (HTTP 403) - confirmed on three URL variants (/abs/pii/, plain /pii/, and the Elsevier "/am/" open-access-manuscript path), not a one-off glitch. This is despite the article being classified "Bronze" open access per Unpaywall/OpenAlex (i.e., free-to-read at the publisher for a human browser, but blocked for the fetch tool's request pattern). I exhausted the reasonable alternative-access options visible via WebSearch: NOAA's own public-access repository copy, ResearchGate, SSRN, ACM Digital Library, and an OpenAlex-cached PDF all returned 403/401; the one full-text PDF mirror I could locate and confirm was genuine (hosted by co-author Pengfei Xue's lab at Michigan Tech, linked directly from that lab's own publications page) exceeded the WebFetch tool's 10 MB content-size limit and could not be processed at all (hard tool error, not a paywall). What I was able to obtain, and cross-validate three independent ways (Semantic Scholar API, OpenAlex API, Michigan Tech Digital Commons), is the complete verbatim abstract, retrieved through Google Scholar's rendering of the ScienceDirect abstract page, fetched twice with differently worded prompts and reconciled (both fetches agreed word-for-word on the abstract text). Bibliographic metadata (authors, journal, volume/page, DOI, funding acknowledgment, 42 references) came cleanly from the Crossref API. Net effect: every key_claim, data_number, and the methods/limitations synthesis above is grounded in the abstract only - no quantitative skill/error statistics (RMSE, correlation, bias, etc.), no grid/particle configuration details, and no explicit authors'-stated-limitations text from the Discussion/Conclusion could be retrieved or verified, and none is claimed here. A downstream reviewer who has direct journal access (e.g., through an institutional subscription) should treat the "methods" and "stated_limitations" fields here as abstract-derived inference, not full-text confirmation, and could usefully upgrade this record if the full PDF becomes reachable.
