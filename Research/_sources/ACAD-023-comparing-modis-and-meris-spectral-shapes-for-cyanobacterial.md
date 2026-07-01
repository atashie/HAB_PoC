---
key: ACAD-023
title: Comparing MODIS and MERIS spectral shapes for cyanobacterial bloom detection
authors_or_org: Wynne, T.T.; Stumpf, R.P.; Briggs, T.O. (NOAA National Centers for Coastal Ocean Science; T.O. Briggs affiliated with CSS-Dynamac per one search snippet)
year: 2013
url: https://doi.org/10.1080/01431161.2013.804228 (resolves via 302 redirect to https://www.tandfonline.com/doi/full/10.1080/01431161.2013.804228 — blocked, HTTP 403)
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article
categories: [remote-sensing]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: flag
---

# Comparing MODIS and MERIS spectral shapes for cyanobacterial bloom detection

> Note: provisional URL was resolved to a primary source. Original: https://www.researchgate.net/publication/260972802_Comparing_MODIS_and_MERIS_spectral_shapes_for_cyanobacterial_bloom_detection

**What it is.** A 2013 peer-reviewed methods paper (International Journal of Remote Sensing) by NOAA scientists Wynne, Stumpf, and Briggs that develops and cross-validates a MODIS-based analogue of an existing MERIS spectral-shape index (S2d) for satellite detection of cyanobacterial harmful algal blooms, undertaken because the MERIS satellite mission ended in 2012 and continuity of the Lake Erie bloom-monitoring time series required a substitute sensor-algorithm.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** A spectral-shape algorithm applied to MERIS imagery detects cyanobacterial blooms, demonstrated extensively in Lake Erie, using an approximation of the second derivative around the 681 nm band as the shape metric, denoted S2d(681).
  - *evidence:* This description recurred verbatim/near-verbatim across at least 6 independent WebSearch queries pulling from indexed abstract content; treated as a faithful paraphrase of the paper's core method statement. (Abstract (exact page/section within the 6668-6678 page range not independently visible to me))
  - *quote:* "an approximation of the second derivative as a measure of spectral shape around the 681 nm band S2d(681)"
- **[✓ verified]** After the MERIS mission ended, the authors developed a MODIS analogue of the shape metric, S2d(678), computed from MODIS Rayleigh-corrected reflectance, to continue bloom monitoring.
  - *evidence:* Recurred consistently across multiple search snippets, including a mention that the MODIS metric is computationally equivalent to the negative of the MODIS fluorescent line height (FLH). (Abstract / Methods)
  - *quote:* "an analogue was developed for MODIS to continue monitoring for these blooms"
- **[✓ verified]** The MERIS mission's end date, cited as the reason the MODIS analogue was needed, was 8 April 2012.
  - *evidence:* This specific date appeared identically across several independent search results, suggesting it is quoted directly from the paper. (Introduction/Abstract)
  - *quote:* "With the end of the MERIS mission on 8 April 2012"
- **[✓ verified]** The two products (MERIS S2d(681) and MODIS S2d(678)) were compared using image pairs drawn from a 2008-2011 period described as one of relatively severe cyanobacterial blooms.
  - *evidence:* Reported consistently in at least two independent search snippets describing the comparison dataset/timeframe. (Methods/Results)
  - *quote:* "a period of relatively severe blooms of cyanobacteria (2008-2011)"
- **[⚠ partial]** When MODIS bands do not saturate, the two algorithms produce comparable results related by a linear transform of the MODIS S2d(678) value -- this is the paper's central finding supporting MODIS as a viable continuation of the MERIS bloom-detection capability.
  - *evidence:* This finding-plus-caveat pairing recurred across multiple independent search results using different query phrasings, indicating it reflects the paper's actual conclusion rather than a single search artifact. (Results/Discussion)
  - *quote:* "the algorithms produce comparable results with a linear transform of the MODIS S2d(678)"
  - *reviewer:* Source text states the algorithms produce comparable results 'with a linear transform' but does not explicitly state this is the paper's 'central finding' or characterize it as proof that MODIS is a 'viable continuation.' The interpretation of significance/centrality exceeds what the source directly claims.
- **[⚠ partial]** The paper states an explicit limitation: the MODIS-MERIS agreement breaks down when MODIS bands saturate, which occurs due to surface scums from high cyanobacteria biomass or due to sun glint or dense aerosol conditions.
  - *evidence:* This limitation/failure-condition statement recurred across multiple independent search snippets in near-identical wording, so it is treated as a faithful representation of a stated limitation rather than a paraphrase artifact. (Results/Discussion (stated as a caveat on the main comparability finding))
  - *quote:* "MODIS bands do not saturate due to surface scums from high cyanobacteria biomass or conditions of glint or dense aerosols"
  - *reviewer:* Source text states 'when the MODIS bands do NOT saturate due to surface scums from high cyanobacteria biomass or conditions of glint or dense aerosols'—the logic is inverted. The source specifies when algorithms DO produce comparable results (when saturation does NOT occur), not when agreement breaks down. This is a logical inversion of the actual caveat.

## Data / numbers
- 681 nm — spectral band used for MERIS second-derivative spectral-shape metric S2d(681)
- 678 nm — analogous band used for MODIS metric S2d(678)
- 8 April 2012 — date the MERIS mission ended, prompting development of the MODIS analogue
- 2008-2011 — period of image pairs used to compare the two products, described as a period of 'relatively severe blooms of cyanobacteria'
- 667 nm, 678 nm, 754 nm — MODIS bands referenced as adjacent bands used in one search-snippet description of the S2d(678) calculation (not independently confirmed against the source text itself, so treated as low-confidence)

## Methods
Method: a spectral-shape / second-derivative reflectance index computed around the red-edge/chlorophyll-fluorescence region (681 nm for MERIS; the analogous 678 nm band for MODIS), applied to satellite ocean-color imagery. Data: MERIS (Medium Resolution Imaging Spectrometer, ESA Envisat) imagery for the original S2d(681) algorithm, and MODIS (Moderate Resolution Imaging Spectroradiometer) Rayleigh-corrected reflectance for the S2d(678) analogue; the MODIS metric is described as computationally equivalent to the negative of the standard MODIS fluorescent line height (FLH) product. Study location: Lake Erie (cited as the primary demonstration case), with a comparison dataset of image pairs spanning 2008-2011. Per the recurring search evidence, the method "works" (produces comparable MODIS/MERIS results, supporting continuity of the cyanobacteria-monitoring time series after MERIS ended in April 2012) when MODIS bands are not saturated, and reportedly fails/diverges when MODIS bands saturate under high-biomass surface scums, sun glint, or dense aerosol conditions. I was not able to confirm exact statistical fit values (e.g., slope, R², sample size) from verified source text, so none are reported as confirmed methods-performance numbers.

## Stated limitations
The one limitation consistently and independently corroborated in search results is a saturation failure mode: the MODIS-vs-MERIS agreement (comparable results via linear transform) holds only "when the MODIS bands do not saturate," and saturation is attributed to (a) surface scums arising from high cyanobacteria biomass, (b) sun/sensor glint, or (c) dense aerosol conditions. Beyond this, I could not access the paper's full discussion/limitations section (e.g., sample size caveats, geographic generalizability beyond Lake Erie, or measurement uncertainty), so no further stated limitations can be faithfully reported without over-reaching beyond the abstract-level content actually retrieved.

## Tensions with other findings
Two tensions are evident from the broader search landscape, though I did not verify them against this paper's own text (they come from surrounding literature encountered during search, not from ACAD-023 itself, so I flag them as context rather than confirmed claims of this source): (1) A related/possibly-successor paper on intercalibrating MERIS, MODIS, and OLCI (2021, MDPI) appears to revisit and refine the MODIS-MERIS cross-sensor conversion this 2013 paper first proposed, which could mean the original linear-transform relationship reported here was later updated or superseded — this bears on how current any single-sensor conversion factor from 2013 should be treated. (2) The paper's core method relies on a spectral-shape/second-derivative index that is described as "computationally equivalent to the negative of MODIS FLH," meaning its added value over a plain FLH-based approach (a longstanding alternative bloom index) is a reparameterization/renaming for cross-sensor continuity rather than a novel physical signal — worth noting if this source is used to claim a distinct method rather than an equivalent formulation of an existing one. Neither tension could be text-confirmed from ACAD-023 itself given full-text was inaccessible.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Dropped caveats:**
  - The source text explicitly notes that unconfirmed numerical figures (average slope, R² ranges, and a 'slope of 2.92 and R² of 0.97') were excluded because they could not be reproducibly verified across multiple searches and may represent conflation with a different 2021 paper. This methodological caution about data integrity and confidence is dropped from the claims.
- **Reviewer notes:** Five of six claims are well-supported or directly traceable to the source text. Two significant issues warrant flagging: (1) Claim 5 overstates the source by labeling something the 'central finding' and 'proof of viability' when the source only states the algorithms produce comparable results under specified conditions—the interpretation of significance exceeds what is explicitly claimed. (2) Claim 6 contains a critical logical error: it inverts the source text's caveat. The source states 'when the MODIS bands do not saturate due to surface scums...the algorithms produce comparable results'; the claim rewrites this as 'saturation occurs due to those conditions and agreement breaks down.' The source is describing the condition for agreement to hold (non-saturation), not conditions that cause saturation. This is a material misrepresentation of the limitation statement. The source also explicitly notes that full-text retrieval failed and unverifiable numerical figures were excluded; this epistemic caution about reproducibility is absent from the claims."

## Provenance
- Canonical URL: https://doi.org/10.1080/01431161.2013.804228 (resolves via 302 redirect to https://www.tandfonline.com/doi/full/10.1080/01431161.2013.804228 — blocked, HTTP 403)
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: FULL TEXT WAS NOT OBTAINABLE. I attempted WebFetch six times against every plausible host: (1) ResearchGate publication page — HTTP 403 Forbidden; (2) Tandfonline DOI abstract page (tandfonline.com/doi/abs/...) — HTTP 403 Forbidden; (3) Tandfonline full-text page (tandfonline.com/doi/full/...), reached via the doi.org redirect — HTTP 403 Forbidden; (4) doi.org/10.1080/01431161.2013.804228 — resolved (302) to the blocked Tandfonline full-text URL above; (5) OUCI citation-index page — loaded but did not contain this paper; (6) Google/Bing search-result pages fetched directly — returned only search-UI chrome, no article content (WebFetch cannot render live JS search results). No PMC, NOAA institutional-repository copy, or other open-access mirror of this specific paper could be located via WebSearch (NOAA repository hits returned were all for OTHER papers, e.g., the 2021 Intercalibration paper and Saginaw Bay phenology paper). Given the total WebFetch failure, I relied on WebSearch, which repeatedly and independently surfaced consistent abstract-level snippets (evidently indexed from the abstract text) across ~10 separate queries. I cross-checked repeated snippets against each other and only retained facts that recurred verbatim/near-verbatim across multiple independent search calls. One search response asserted a Lake Erie MODIS-vs-MERIS 'average slope from four image pairs of 1.3 +/- 0.3' and an unrelated 'R² of 0.97' from an 'integrated technique' with slope 2.92 — I could NOT reproduce or corroborate these numbers in any subsequent targeted search, and the second figure's phrasing ('integrated technique') strongly suggests conflation with the separate 2021 Lehrter/Wynne intercalibration paper (Int'l J of Remote Sensing readers will note MDPI rs13122305 covers similar MODIS/MERIS/OLCI intercalibration with its own slope/R2 stats). I have EXCLUDED those unconfirmed numbers from data_numbers/key_claims per the rule against letting a fetch paraphrase or hallucinate numbers. Because I never accessed the actual PDF/HTML body, I could not extract precise table values, exact sample sizes, or the full stated-limitations section beyond the saturation caveat that recurred consistently. fetch_status is 'partial' (some faithful information obtained, but not via a successful WebFetch of the source itself) and full_text_access is 'abstract' (only abstract-level content reachable, not the full body/tables/figures).
