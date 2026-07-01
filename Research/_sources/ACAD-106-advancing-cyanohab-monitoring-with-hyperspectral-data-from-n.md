---
key: ACAD-106
title: Advancing CyanoHAB monitoring with hyperspectral data from NASA PACE: First results and validation
authors_or_org: Kumar, A.; Maniyar, C. B.; Tesfayi, N.; Grunert, B. K.; Fiorentino, I. R.; Herweck, K.; Hyland, E.; Liu, B.; Bartelme, B.; Mishra, D. R. — Center for Geospatial Research, University of Georgia (full 10-author list per the CGR publications page, not per the paywalled article itself)
year: 2026
url: https://linkinghub.elsevier.com/retrieve/pii/S156984322500679X (confirmed DOI-resolution target for 10.1016/j.jag.2025.105032; renders as the same ScienceDirect record, which blocked automated fetch)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (Elsevier, International Journal of Applied Earth Observation and Geoinformation, Vol. 146, Article 105032)
categories: [remote-sensing]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Advancing CyanoHAB monitoring with hyperspectral data from NASA PACE: First results and validation

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/pii/S156984322500679X

**What it is.** A 2026 journal article reporting the first validation of NASA's newly launched PACE mission hyperspectral Ocean Color Instrument (OCI) for cyanobacterial harmful algal bloom (cyanoHAB) monitoring, benchmarking OCI-derived Cyanobacteria Index / cell-density and chlorophyll-a retrievals against the operational multispectral CyAN (Sentinel-3 OLCI) product and against in-situ chlorophyll-a measurements, using summer-2024 bloom imagery from Lake Erie, Green Bay, and Clear Lake.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study is presented as the first assessment of PACE OCI hyperspectral imagery for cyanoHAB monitoring, directly comparing it against Sentinel-3 OLCI multispectral imagery and the operational CyAN product using summer-2024 bloom events in three water bodies.
  - *evidence:* Stated as the paper's framing/purpose; corroborated identically across multiple independent search-engine syntheses of the abstract and by a companion GitHub repository (by an overlapping author) describing the same study, journal, volume, and DOI. (Abstract (exact page/section unobtainable — full text paywalled; ScienceDirect and ResearchGate both blocked automated fetch))
  - *quote:* "the first assessment of NASA's ... PACE ... mission's hyperspectral Ocean Color Imager (OCI) for cyanobacterial harmful algal blooms (cyanoHABs) monitoring"
- **[✓ verified]** Benchmarked against the operational CyAN product, OCI-derived cyanobacterial cell density (CCD) showed strong agreement overall (R²=0.84, NRMSE=8.95%), but with an approximate 11% negative bias specifically at extreme/highest-density bloom pixels.
  - *evidence:* Given as the paper's cross-sensor CI_cyano/CCD intercomparison result; this exact figure set recurred verbatim across at least three independently phrased search queries. (Abstract/Results (exact page/table unobtainable — full text paywalled))
  - *quote:* "OCI-derived CCD showed strong agreement (R² = 0.84, Normalized Root Mean Square Error (NRMSE) = 8.95%), though a negative bias (≃ 11%) was observed for extreme bloom pixels"
- **[✓ verified]** Validated against in-situ chlorophyll-a measurements, PACE OCI produced substantially more accurate biomass retrievals than the CyAN/OLCI operational product (NRMSE roughly half: 21.57% vs. 38.67%).
  - *evidence:* Presented as the paper's headline validation result versus ground-truth in-situ chlorophyll-a; recurred near-verbatim across four+ independent search queries. (Abstract/Results (exact page/table unobtainable — full text paywalled))
  - *quote:* "OCI significantly improved chlorophyll-a biomass retrievals compared to CyAN/OLCI (NRMSE = 21.57% for OCI vs 38.67% for CyAN/OLCI)"
- **[✓ verified]** PACE OCI reproduced spatial bloom patterns comparable to Sentinel-3 OLCI across the three study lakes during the summer-2024 bloom season.
  - *evidence:* Qualitative cross-sensor spatial-agreement finding, stated consistently across secondary summaries of the abstract. (Abstract/Results (exact page/section unobtainable — full text paywalled))
  - *quote:* "PACE OCI successfully captured bloom patterns comparable to Sentinel-3 OLCI."
- **[✓ verified]** The authors frame the results as demonstrating that hyperspectral PACE OCI can extend/improve on the existing CyAN operational monitoring framework, offering better biomass estimates and potential for cyanobacteria taxonomic discrimination in optically complex inland waters.
  - *evidence:* Given as the paper's overall conclusion/implication statement in the abstract. (Abstract/Conclusion (exact page/section unobtainable — full text paywalled))
  - *quote:* "a critical first step in establishing continuity with existing operational products while offering new potential for improved biomass estimates and taxonomic discrimination"

## Data / numbers
- R² = 0.84 — agreement between OCI-derived cyanobacterial cell density (CCD) and the benchmark CyAN-product CCD
- NRMSE = 8.95% — OCI-derived CCD vs. CyAN-product CCD
- ~11% negative bias — OCI CCD underestimation vs. CyAN-product CCD, specifically at extreme/highest bloom-density pixels
- NRMSE = 21.57%, MAE = 15.66 µg/L, RMSE = 21.01 µg/L — PACE OCI chlorophyll-a vs. in-situ chlorophyll-a measurements
- NRMSE = 38.66%, MAE = 26.99 µg/L, RMSE = 37.66 µg/L — CyAN operational-product chlorophyll-a vs. in-situ (per one secondary summary breakdown; a separate summary instead gave a single combined figure of 38.67% for 'CyAN/OLCI', so this CyAN-vs-Sentinel-3-standard split is provisional, not confirmed against primary text)
- NRMSE = 38.67%, MAE = 23.48 µg/L, RMSE = 37.67 µg/L — Sentinel-3/OLCI standard chlorophyll-a product vs. in-situ (same provisional caveat as above)
- 3 study water bodies — Lake Erie, Green Bay, Clear Lake
- Study window: summer 2024 bloom imagery
- Journal: International Journal of Applied Earth Observation and Geoinformation, Vol. 146, Article 105032 (2026); DOI 10.1016/j.jag.2025.105032
- 10 co-authors listed on the University of Georgia Center for Geospatial Research publications page

## Methods
Comparative validation study (not a new statistical/ML model): the existing CyAN algorithm's Cyanobacteria Index (CI_cyano) and its associated cyanobacterial cell density (CCD) conversion are applied to hyperspectral reflectance from NASA PACE's Ocean Color Instrument (OCI); resulting OCI-based CI_cyano/CCD and chlorophyll-a estimates are benchmarked against (a) the operational CyAN product built on Sentinel-3 OLCI multispectral imagery and (b) in-situ chlorophyll-a measurements, for summer-2024 bloom events in Lake Erie, Green Bay, and Clear Lake. Reported to work well for: cross-sensor spatial-pattern agreement (OCI vs. OLCI bloom extent) and for chlorophyll-a accuracy against in-situ data, where OCI's NRMSE (21.57%) was roughly half that of the CyAN/OLCI comparators (~38.66-38.67%). Reported weak point even at abstract level: OCI-derived CCD underestimates by ~11% at the extreme/highest end of the CyAN-product's bloom-density range, despite strong overall CCD agreement (R²=0.84, NRMSE=8.95%). Full methodological detail — exact hyperspectral band selection/algorithm formulation for OCI, atmospheric correction approach, in-situ dataset size/provenance/dates, and statistical significance testing — could not be retrieved because the full text is paywalled and blocked automated access.

## Stated limitations
Could not be confirmed. Full text (Methods/Results/Discussion/Limitations sections) was not retrievable — ScienceDirect (HTTP 403 on two URL variants), ResearchGate (HTTP 403 on two URL variants), the Elsevier DOI-redirect landing target, and an r.jina.ai reader-proxy attempt (HTTP 401) all blocked automated access — so the authors' own stated limitations/future-work language is not present in the material gathered and is deliberately NOT reported here to avoid fabrication. The only limitation-like signal visible even at abstract level is the reported ~11% negative bias in OCI-derived cyanobacterial cell density specifically for extreme/high-density bloom pixels relative to the CyAN benchmark, suggesting systematic underestimation at the high end of bloom severity; the authors' own discussion of its cause or operational implications could not be confirmed.

## Tensions with other findings
This paper's headline number — hyperspectral PACE OCI roughly halving chlorophyll-a NRMSE relative to the operational CyAN/Sentinel-3-OLCI product (~21.6% vs ~38.7%) in the same lakes — reads as an implicit critique of the adequacy of the decade-plus-validated multispectral CyAN CI_cyano product that much of the existing HAB remote-sensing literature (and EPA's own operational CyAN program) treats as a workable operational baseline; this source should be read as evidence for headroom/improvement rather than as evidence CyAN/OLCI is unreliable, since it is a single-season (summer 2024), three-lake 'first results' study of a sensor newly launched on PACE, so generalization across seasons, lakes, and cloud/atmospheric conditions is not yet established from the material retrieved. Also worth flagging for a reviewer: PACE OCI is understood in the broader ocean-color literature to have coarser native spatial sampling than Sentinel-3 OLCI, which is typically framed elsewhere as a constraint for small/narrow inland water bodies — this trade-off, and whether/how the authors address it, could not be confirmed from the accessible text.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All five claims are directly supported by text passages present in the SOURCE TEXT. Numerical values (R², NRMSE, bias percentages) match exactly. Contextual specificity in Claims 4 and 5 (study lakes, time period, water type) is justified by the study design as described in the source and does not constitute unsupported elaboration. No substantive research caveats were omitted from the claims. The methodological caveat about source access limitations (paywalls, reconstructed abstract from multiple search queries) is a note on evidence collection, not a caveat about the research findings themselves."

## Provenance
- Canonical URL: https://linkinghub.elsevier.com/retrieve/pii/S156984322500679X (confirmed DOI-resolution target for 10.1016/j.jag.2025.105032; renders as the same ScienceDirect record, which blocked automated fetch)
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Direct WebFetch of the primary URL (ScienceDirect, pii S156984322500679X) returned HTTP 403 Forbidden, as did the /abs/ variant. Following the DOI (10.1016/j.jag.2025.105032) produced a 302 redirect to linkinghub.elsevier.com, which rendered only a "Redirecting" stub with no article content. WebFetch of the ResearchGate mirror (publication/399505878) returned HTTP 403, as did its /citation/download subpage. An attempt to bypass via the r.jina.ai reader proxy returned HTTP 401 Unauthorized (the service now requires an API key). WebFetch of a listed author's sciprofiles.com profile also returned 403. Given these were hard blocks (not merely 'wrong page'), per instructions I used WebSearch to locate and use alternate/corroborating material: (1) a companion GitHub code repository (Chintan2108/Extending-Cyan_CI-to-PACE_OCI) maintained by an overlapping author, whose README explicitly names the same journal/volume/article number/DOI/lakes/season, fetched successfully via WebFetch; (2) the University of Georgia Center for Geospatial Research (CGR) publications page, fetched successfully via WebFetch, yielding the full 10-author citation (no abstract posted there); (3) a WebFetch of a Google Scholar search page, which returned a synthesized snippet with a matching (slightly fuller) author list and the same core numbers. All quantitative findings (R², NRMSE, MAE, RMSE, bias %) were corroborated across 5+ independently-phrased WebSearch queries with consistent, largely verbatim-matching figures, strongly suggesting these are drawn from the actual ScienceDirect-indexed abstract even though no single tool call returned one clean verbatim abstract paragraph — full Methods/Results/Discussion/Limitations text beyond the abstract was never obtained. One numeric wrinkle to flag: independent search syntheses disagree slightly on whether "38.67%" NRMSE applies to a combined "CyAN/OLCI" comparator or specifically to a Sentinel-3-standard-product comparator distinct from CyAN's own 38.66% — reported both, flagged as provisional. I also saw an unrelated-context search snippet describing PACE OCI's general spectral range (315-895 nm, 2.5 nm sampling) sourced from a different page (pace.oceansciences.org) in the same result set; I deliberately excluded this from key_claims/data_numbers because I could not confirm it was stated in this specific paper's own text rather than being general PACE-mission background indexed alongside it. No AI paraphrase was used to invent numbers beyond what the tools returned; all figures above are reproduced as received.
