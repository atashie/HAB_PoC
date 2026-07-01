---
key: ACAD-091
title: Sentinel-2 and Landsat-8 Observations for Harmful Algae Blooms in a Small Eutrophic Lake
authors_or_org: Miao Liu, Hong Ling, Dan Wu, Xiaomei Su, Zhigang Cao (published in MDPI Remote Sensing)
year: 2021
url: https://www.mdpi.com/2072-4292/13/21/4479
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, open access (MDPI Remote Sensing, Vol. 13, Issue 21, Article 4479; DOI 10.3390/rs13214479)
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Sentinel-2 and Landsat-8 Observations for Harmful Algae Blooms in a Small Eutrophic Lake

**What it is.** A remote-sensing methods paper that builds a two-sensor "virtual constellation" (Sentinel-2A/2B MSI + Landsat-8 OLI) and applies the Floating Algae Index (FAI) to map spatial and seasonal patterns of floating (cyanobacterial) algae blooms in Lake Xingyun, a small eutrophic plateau lake in China, over 2016-2020, and cross-checks the FAI derived from the two sensor families against each other.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Widespread harmful cyanobacterial bloom is framed by the authors as one of the most pressing concerns for lakes and reservoirs, motivating the study.
  - *evidence:* Opening motivating statement of the paper (found via targeted verbatim text search). (Introduction/Abstract (exact page/section number not confirmable from the extraction tool's output))
  - *quote:* "Widespread harmful cyanobacterial bloom is one of the most pressing concerns in lakes and reservoirs"
- **[✓ verified]** The authors state that low-spatial-resolution ocean-color satellite instruments, already used to monitor cyanobacterial blooms in large lakes, cannot be applied well to small water bodies -- the stated rationale for using Sentinel-2/Landsat-8 instead.
  - *evidence:* Stated rationale for sensor choice / research gap; directly bounds the applicability of coarse ocean-color sensors (e.g., the ~300 m OLCI instrument behind EPA CyAN) to small lakes. (Introduction/Abstract (exact page/section number not confirmable))
  - *quote:* "Ocean color instruments with low spatial resolution have been used to monitor cyanobacterial bloom in large lakes ... [but] cannot be applied to small water bodies well"
- **[✓ verified]** The study assembles Sentinel-2A, Sentinel-2B (carrying the Multi-Spectral Instrument, MSI) and Landsat-8 (carrying the Operational Land(sat) Imager, OLI) into what the authors call a "virtual constellation" to monitor Lake Xingyun, China, from 2016-2020.
  - *evidence:* Core method/data framing: using multiple independent optical satellites together to raise effective revisit frequency over one small lake. (Abstract/Methods (exact section number not confirmable))
  - *quote:* "Multi-Spectral Instrument (MSI) onboard Sentinel-2A and -2B ... Operational Landsat Imager (OLI) onboard Landsat-8 ... were employed to assemble the virtual constellation"
- **[✓ verified]** Floating algae was mapped using the Floating Algae Index (FAI), computed from Rayleigh-corrected reflectance in the red, near-infrared, and short-wave-infrared bands, with pixels classified as floating algae above a threshold of 0.0693 determined from bimodal histograms of FAI images.
  - *evidence:* Core algorithm and the specific numeric threshold used to convert a continuous index into a bloom/no-bloom classification. (Methods (exact section number not confirmable))
  - *quote:* "FAI was calculated using Rayleigh-corrected reflectance in the red, near-infrared, and short-wave infrared bands ... Then, an FAI threshold, 0.0693, was determined using bimodal histograms of FAI images for floating algae extraction."
- **[✓ verified]** FAI derived from Sentinel-2 MSI showed a similar pattern to, and reasonable numerical agreement with, FAI derived from Landsat-8 OLI, quantified as a mean absolute percentage error (MAPE) of 19.98% and an unbiased percentage difference (UPD) of 17.05%.
  - *evidence:* This is a cross-sensor consistency check (MSI-derived product vs. OLI-derived product), not a comparison against independent in-situ/ground-truth chlorophyll or bloom measurements -- no in-situ validation term (see stated_limitations) was found in the extracted text. No confidence interval, standard deviation, or p-value accompanies the MAPE/UPD figures in the retrieved text. (Results/Abstract (exact section number not confirmable))
  - *quote:* "The MSI-derived FAI had a similar pattern to the OLI-derived FAI, with a mean absolute percentage error of 19.98% and unbiased percentage difference of 17.05%."
- **[✓ verified]** Floating algae occurrence was spatially uneven within the lake, higher in the northern region than the southern region.
  - *evidence:* Descriptive spatial finding from the multi-year FAI occurrence mapping; no numeric magnitude (e.g., percentage-point gap) for this north-south difference was found in the retrieved text. (Results (exact section number not confirmable))
  - *quote:* "The floating algae had a higher occurrence in the northern region than the southern region in this lake"
- **[✓ verified]** Floating algae occurrence followed a seasonal pattern, higher in summer and autumn than in spring and winter.
  - *evidence:* Descriptive seasonal finding from the same occurrence mapping; no numeric magnitude for the seasonal gap was found in the retrieved text. (Results (exact section number not confirmable))
  - *quote:* "the occurrence of floating algae in summer and autumn was higher than that in spring and winter"
- **[✓ verified]** The authors relate (associate) the observed spatial and seasonal bloom pattern to variability in air temperature, wind speed and direction, and nutrients.
  - *evidence:* This is presented as a descriptive/qualitative association ("was related to"), not a tested causal or even quantified statistical relationship -- no regression coefficients, correlation values, or the underlying temperature/wind/nutrient time series were found in the retrieved text, so correlation/attribution should not be read as demonstrated causation. (Discussion (exact section number not confirmable))
  - *quote:* "Such a spatial and seasonal pattern was related to the variability in air temperature, wind speed and direction, and nutrients."
- **[✓ verified]** The climatological annual mean occurrence of floating algae in Lake Xingyun significantly decreased from 2016 to 2020, which the authors relate to nutrient decreases attributed to ecological restoration efforts by the local government.
  - *evidence:* A trend claim with an attribution to a restoration policy; presented as an association ("was related to," "resulting from") rather than backed, in the retrieved text, by a nutrient time series, an explicit trend-test statistic, or a p-value -- treat as the authors' interpretation, not a demonstrated causal effect of the restoration program. (Discussion/Conclusion (exact section number not confirmable))
  - *quote:* "The climatological annual mean occurrence of floating algae from 2016 to 2020 in Lake Xingyun exhibited a significant decrease, which was related to decreases in nutrients, resulting from efficient ecological restoration by the local government."

## Data / numbers
- FAI classification threshold = 0.0693 (dimensionless spectral index; pixels above this are classed as floating algae)
- Mean Absolute Percentage Error (MAPE) between MSI-derived and OLI-derived FAI = 19.98%
- Unbiased Percentage Difference (UPD) between MSI-derived and OLI-derived FAI = 17.05%
- Monitoring period = 2016-2020 (5 years)
- No confidence interval, standard deviation, or p-value was found accompanying the MAPE/UPD figures in the retrieved text -- i.e., no stated uncertainty band for the cross-sensor error metrics

## Methods
Two-sensor "virtual constellation" combining Sentinel-2A/2B (MSI) and Landsat-8 (OLI) optical imagery over 2016-2020 for Lake Xingyun, a small eutrophic plateau lake in China. Floating algae is detected via the Floating Algae Index (FAI) computed on Rayleigh-corrected reflectance in red/NIR/SWIR bands, with a bimodal-histogram-derived threshold (0.0693) separating floating-algae pixels from open water. The two sensors' FAI products are cross-compared (MAPE 19.98%, UPD 17.05%) to check they can be merged into one consistent time series; bloom occurrence is then aggregated spatially (north vs. south) and seasonally (summer/autumn vs. spring/winter), and the multi-year trend and spatial/seasonal pattern are qualitatively related to temperature, wind, nutrients, and a local ecological-restoration program. Where the approach appears to "work" per the source: it achieves reasonably consistent FAI retrievals across the two independent sensor families (MAPE ~20%, UPD ~17%), supporting the premise that combining medium/high-resolution optical sensors can substitute for a single coarse-resolution ocean-color sensor on a small lake. Gaps I could not fill despite repeated, differently-worded targeted searches of the extracted PDF text: no mention of in-situ chlorophyll-a, other in-situ water-quality measurements, or "ground truth" was found -- the validation shown is satellite-vs-satellite agreement, not agreement with independently measured bloom/chlorophyll data; no explicit accuracy figures for the underlying FAI-to-bloom classification (e.g., a confusion matrix or per-class accuracy) were retrieved.

## Stated limitations
Despite roughly a dozen WebFetch passes with differently worded, increasingly targeted verbatim-search prompts against the extracted PDF text, I could not find the words/phrases "limitation," "limitations," "future work," "cloud," "mixed pixel," "in situ," "in-situ," "chlorophyll," or "ground truth" anywhere in the text the fetch tool returned. I cannot tell whether that means the paper truly has no explicit limitations passage using this language, or whether that passage simply fell outside what this fetch tool could reliably extract (the same tool intermittently refused to parse the PDF at all on several calls, reporting it as unreadable "binary/compressed streams," so an extraction gap rather than a genuine absence in the paper cannot be ruled out). I am reporting this as an honest gap rather than inventing limitations language the source did not give me. The one caveat I can support directly from retrieved text is methodological, not the authors' own words: the reported cross-sensor MAPE (19.98%) and UPD (17.05%) describe agreement between two satellite-derived products, not agreement with independently measured (in-situ) bloom or chlorophyll-a data, and the spatial/seasonal/trend "driver" statements (temperature, wind, nutrients, restoration) are framed descriptively ("was related to") rather than supported, in the retrieved text, by the underlying driver data, a statistical test, or a p-value.

## Tensions with other findings
This source's central rationale -- that "ocean color instruments with low spatial resolution ... cannot be applied to small water bodies well" -- directly bounds the applicability of EPA CyAN, which is itself built on Sentinel-3 OLCI ocean-color imagery (~300 m pixels), for small lakes. That is not a data-driven contradiction of CyAN's validity for the larger lakes it targets, but it is an explicit, peer-reviewed rationale for why CyAN-based claims in this project should be scoped to lakes large enough for OLCI's resolution, and why a finer-resolution multi-sensor approach (as here) may be needed for smaller water bodies -- directly relevant to how the HAB_PoC should bound its own product claim by lake size. Separately, because this paper's own validation step is a satellite-vs-satellite (MSI vs. OLI) cross-check rather than a fusion with in-situ or weather data, it does not itself satisfy the brief's "fuse remote-sensing with in-situ" mandate: it is a complementary remote-sensing-only reference useful for the spectral-signal side of a fusion design, not a template for the fusion step itself.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All nine claims are directly supported by verbatim text in the source. All numeric thresholds and metrics (0.0693, 19.98%, 17.05%) are present in the source text. The claims correctly characterize associations as associations (via language like 'relate to'), avoiding unwarranted causal claims. The evidence notes in the claim set appropriately flag methodological limitations (cross-sensor comparison, lack of in-situ validation, no confidence intervals) but these are analyst observations, not overstatements in the claims themselves. No hallucinated numbers or dropped material safety caveats detected."

## Provenance
- Canonical URL: https://www.mdpi.com/2072-4292/13/21/4479
- Access date: 2026-07-01
- Full-text access: full | Fetch status: partial
- Fetch notes: The canonical landing page (https://www.mdpi.com/2072-4292/13/21/4479) returned HTTP 403 Forbidden on WebFetch (twice, including the /htm full-text variant), and a r.jina.ai proxy attempt returned HTTP 401. I located the open-access PDF's direct URL via WebSearch (hosted on MDPI's own mdpi-res.com CDN, so still the publisher's authoritative copy) and used that as the primary source, fetching it far more than the minimum two times (roughly a dozen calls with different, increasingly targeted prompts) because: (a) broad/holistic extraction prompts frequently failed outright, with the small extraction model reporting the PDF as unparseable "binary/FlateDecode compressed streams," while (b) narrow "find this exact substring and quote the sentence" prompts often succeeded and returned internally consistent, repeatable exact-sentence matches -- exactly the call-to-call unreliability the task brief warned about. Critically, this repeated targeted verification exposed that one early broad-extraction pass had produced lake-morphometry, image-count, and band-wavelength figures that could not be reproduced by direct substring search and conflict with independent sources on this lake's real morphometry -- I have excluded those specific numbers as likely fabrications (full explanation in source_extract's verification note) rather than report them as the paper's claims. I was not able to retrieve, despite repeated attempts, the paper's exact Introduction opening sentences, Conclusion closing paragraph, Funding statement, Data Availability statement, or any passage using the words "limitation(s)"/"future work"/"in situ"/"chlorophyll"/"ground truth" -- so full_text_access is "full" (I did hold and query the genuine open-access PDF and pulled verbatim sentences from its Methods, Results, and Discussion, not just the abstract) but fetch_status is "partial" (several sections and fields remained unconfirmed after exhausting reasonable retries). No prior/training knowledge of this specific paper was used; all claims above trace to text the fetch tool actually returned for this PDF, cross-checked where feasible against an independent AGRIS metadata record and WebSearch summaries.
