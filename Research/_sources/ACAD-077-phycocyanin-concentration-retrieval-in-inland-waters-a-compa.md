---
key: ACAD-077
title: Phycocyanin concentration retrieval in inland waters: A comparative review of the remote sensing techniques and algorithms
authors_or_org: Yaner Yan; Zhongjue Bao; Jingan Shao
year: 2018
url: https://www.sciencedirect.com/science/article/abs/pii/S0380133018300765 (canonical article page; doi.org resolves to https://linkinghub.elsevier.com/retrieve/pii/S0380133018300765, same paywalled record)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal review article (Journal of Great Lakes Research, vol. 44, issue 4, pp. 748-755, published 2018-08, Elsevier)
categories: [remote-sensing]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Phycocyanin concentration retrieval in inland waters: A comparative review of the remote sensing techniques and algorithms

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/abs/pii/S0380133018300765

**What it is.** A 2018 peer-reviewed review article in the Journal of Great Lakes Research (Yan, Bao & Shao) that surveys remote-sensing techniques and retrieval algorithms used to estimate phycocyanin (PC) concentration — the pigment signature of cyanobacteria — in inland waters, comparing empirical and semi-analytical inversion approaches and their implementation across available and prospective satellite/airborne sensors.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Phycocyanin is framed as a more suitable pigment than chlorophyll-a for monitoring cyanobacterial blooms and toxic cyanobacteria.
  - *evidence:* Stated as the review's opening premise/motivation; the abstract gives no quantitative comparison (e.g., no accuracy numbers) between PC- and Chl-a-based monitoring, only the qualitative framing. (Abstract)
  - *quote:* "is more suitable for monitoring cyanobacterial blooms and toxic cyanobacteria than chlorophyll-a (Chl-a)"
- **[✓ verified]** Phycocyanin's absorption peak is at approximately 620 nm, which is why the 615-630 nm wavelength band is the target range for PC-specific remote-sensing inversion algorithms.
  - *evidence:* Given as the spectral/physical rationale for why this band is used in PC retrieval algorithms; presented as a stated physical property, not a measured result with error bars. (Abstract)
  - *quote:* "the absorption peak of PC is about ~620 nm, the application of remote sensing using a wavelength range of 615–630 nm becomes very attractive for the implementation of PC-targeted inversion algorithms"
- **[✓ verified]** The field has produced both empirical and semi-analytical algorithms that use remotely sensed PC concentration as a proxy for cyanobacterial blooms.
  - *evidence:* Summarizes the state of the literature the review surveys; no specific algorithm names, sensors, or performance statistics are given in the abstract itself. (Abstract)
  - *quote:* "Numerous researchers have applied empirical and semi-analytical algorithms to derive PC concentration as proxies for cyanobacterial blooms."
- **[✓ verified]** Unlike chlorophyll-a, large-scale remote-sensing estimation of PC concentration remains constrained by a scarcity of data with sufficient spatial and spectral resolution.
  - *evidence:* This is presented as the central motivating limitation of the field that the review addresses; it is a scope/data-availability caveat, not a specific algorithm's error statistic. (Abstract)
  - *quote:* "in contrast to Chl-a, the remote sensing estimation of PC concentration at the larger scale is still limited by the scarcity of data with sufficient spatial and spectral resolution"
- **[✓ verified]** The review's explicit purpose is to give a comprehensive overview of remote-sensing techniques and retrieval algorithms for PC monitoring, with emphasis on inversion algorithms and their realization on current and prospective sensors.
  - *evidence:* States the paper's own scope and structure as a review (synthesis), not primary field/lab research. (Abstract)
  - *quote:* "this review attempts to provide a comprehensive overview of remote sensing techniques and retrieval algorithms as applied to the PC monitoring"
- **[✓ verified]** The review concludes with a detailed discussion of the overall challenges and potential of remote-sensing-based cyanobacterial PC pigment retrieval, built on its analysis of state-of-the-art techniques and algorithms.
  - *evidence:* Describes the review's concluding analytical contribution; no specific list of the challenges/potentials is given in the abstract text itself. (Abstract)
  - *quote:* "the overall challenges and potentials of remote sensing-based cyanobacterial PC pigment retrieval are discussed in detail"

## Data / numbers
- ~620 nm — approximate wavelength of phycocyanin's absorption peak, per the abstract (stated as a physical/spectral property; no uncertainty or baseline given)
- 615–630 nm — wavelength range described in the abstract as attractive for PC-targeted inversion algorithms (no uncertainty or baseline given)

## Methods
This is a review article, not primary experimental research; the abstract describes no dataset, study lake, or sensor of its own. It synthesizes "empirical and semi-analytical algorithms" developed by other researchers for deriving PC concentration from remote-sensing reflectance, emphasizing "PC inversion algorithms and their realization via the available and perspective [prospective] remote sensors." The abstract does not name specific sensors (e.g., MERIS/OLCI/Landsat/MODIS), specific water bodies, sample sizes, or accuracy statistics (RMSE/R2/MAE/bias) — such details would be in the body text, which is paywalled (ScienceDirect returned HTTP 403 on repeated fetches of both the abstract-page and full-article URLs) and could not be retrieved for this dossier. Bibliographic metadata (authors, volume/issue/pages, dates) was independently corroborated via the Crossref API (api.crossref.org/works/10.1016/j.jglr.2018.05.004).

## Stated limitations
The abstract itself states, as the field-level limitation motivating the review, that PC remote-sensing retrieval "at the larger scale is still limited by the scarcity of data with sufficient spatial and spectral resolution," explicitly contrasted with the more mature state of chlorophyll-a remote sensing. No other source-stated limitations (e.g., algorithm-specific failure modes, interference from CDOM/turbidity/other pigments, sensor-specific caveats) appear in the abstract; such details likely exist in the body text but could not be retrieved. Separately, as an access limitation of THIS dossier (not a limitation the source states about itself): the article is confirmed closed access (Unpaywall API: is_oa=false, no oa_locations; Semantic Scholar API: openAccessPdf.status="CLOSED", no usable URL) and full text could not be legally obtained through WebFetch/WebSearch, so this summary is abstract-only.

## Tensions with other findings
By the source's own framing, PC-specific retrieval is more data- and resolution-constrained at large scale than Chl-a retrieval. This is a scope caveat worth weighing against any HAB analysis (including this project's) that leans on phycocyanin-band products versus chlorophyll-a or composite cyanobacteria-index products (e.g., EPA CyAN's cyanobacteria index) for broad-coverage or near-real-time screening: the source implies PC-band retrieval may currently be harder to scale than Chl-a-based approaches. This is stated as a scope/data-availability limitation in the abstract, not a causal claim, and no direct contradiction with a specific other source could be confirmed since only the abstract was accessible.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All six claims are directly supported by the source text (the abstract from DOI:10.1016/j.jglr.2018.05.004). The claims accurately capture the key propositions: PC suitability over Chl-a, the 620 nm spectral rationale for 615-630 nm sensing bands, the application of empirical and semi-analytical algorithms, the data-scarcity limitation relative to Chl-a monitoring, the review's comprehensive scope with emphasis on inversion algorithms and sensor realization, and the concluding discussion of challenges and potentials. All numerical values (620 nm, 615-630 nm) are present in the source. Minor language variations ('approximately' vs. 'about ~', 'explicit purpose' vs. 'attempts to provide') do not materially distort the meaning and are appropriate restatements."

## Provenance
- Canonical URL: https://www.sciencedirect.com/science/article/abs/pii/S0380133018300765 (canonical article page; doi.org resolves to https://linkinghub.elsevier.com/retrieve/pii/S0380133018300765, same paywalled record)
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Primary URL (ScienceDirect abs page) returned HTTP 403 on WebFetch. Attempted full-text/alternate routes, all blocked or unusable: ScienceDirect non-abs URL (403), Elsevier linkinghub.elsevier.com retrieve page (doi.org redirect target; returned only "Redirecting" placeholder, no content), ResearchGate publication page (403, tried twice), ResearchGate profile page (403), Bohrium paper-details page (returned encoded/obfuscated JSON tokens, not readable content), X-Mol page (CAPTCHA wall, no content), CORE.ac.uk search (403). WebSearch queries repeatedly surfaced text that appeared to blend content from OTHER phycocyanin papers in the result set (e.g., mentions of "Simis05 algorithm," "FBA_PC," "PC3/ETBA" algorithms, "Li and Song 2017" and "Ogashawara et al. 2013" reviews) rather than verified content of THIS specific paper — these WebSearch-synthesized passages were deliberately EXCLUDED from key_claims/source_extract because their provenance to ACAD-077 specifically could not be confirmed (risk of cross-contamination from co-retrieved papers on the same topic). Usable, verifiable content came only from two structured API fetches: Semantic Scholar Graph API (fields=title,abstract,authors,year,venue,externalIds; and separately fields=title,abstract,tldr,openAccessPdf,fieldsOfStudy,citationCount,referenceCount,publicationDate) — both returned an identical verbatim abstract, satisfying the "fetch twice and reconcile" requirement — plus Crossref API (bibliographic metadata) and Unpaywall API (confirmed no open-access copy exists: is_oa=false). Per instructions, since only the abstract was reachable, this dossier summarizes ONLY the abstract; no body-text findings, numeric results (RMSE/R2/etc.), specific algorithms, sensors, or study sites are claimed because they were not present in any text I actually fetched.
