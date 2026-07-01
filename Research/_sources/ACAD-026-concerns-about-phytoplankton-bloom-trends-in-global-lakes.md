---
key: ACAD-026
title: Concerns about phytoplankton bloom trends in global lakes
authors_or_org: Lian Feng, Yanhui Dai, Xuejiao Hou, Yang Xu, Junguo Liu, Chunmiao Zheng (School of Environmental Science and Engineering / State Environmental Key Laboratory of Integrated Surface Water–Groundwater Pollution Control, Southern University of Science and Technology, Shenzhen, China)
year: 2021
url: https://www.nature.com/articles/s41586-021-03254-3
access_date: 2026-07-01
tier: ACAD
source_type: Journal comment ("Matters Arising"), peer-reviewed, Nature
categories: [basic-science]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# Concerns about phytoplankton bloom trends in global lakes

**What it is.** A "Matters Arising" comment in Nature (Feng, Dai, Hou, Xu, Liu & Zheng, 2021; Nature 590, E35–E47) that challenges the methodology and conclusions of Ho, Michalak & Pahlevan (2019, Nature 574), which had reported a global increase in lake phytoplankton bloom intensity. The authors argue that the single-band near-infrared (NIR) Landsat reflectance metric used as a bloom-strength proxy is confounded by sediment and submerged vegetation, and that infrequent Landsat 5 TM (L5TM) sampling undermines the statistical robustness of the reported 30-year trend.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Ho et al. (2019) — the paper under critique — reported an increase in peak summertime bloom intensity in 68% of 71 large lakes worldwide over a 1982–2012 period using Landsat-derived NIR reflectance; this is the finding the current comment contests.
  - *evidence:* Restated by Feng et al. at the outset of the comment to frame what they are disputing; not an original finding of this source, but the target claim. (Main text, opening paragraph)
  - *quote:* "showed an increase in peak summertime bloom intensity in 68% of the 71 large lakes worldwide from 1982 to 2012."
- **[✓ verified]** The authors' central thesis is that there are two fundamental problems with the original study: (1) single-band NIR satellite reflectance is not a reliable proxy for bloom strength, and (2) L5TM's infrequent satellite observations make statistically meaningful long-term conclusions difficult.
  - *evidence:* Presented as the paper's organizing argument, developed through the rest of the comment via image analysis and in-situ data comparisons. (Main text)
  - *quote:* "satellite-derived reflectance in a single near-infrared (NIR) band is not a reliable proxy for bloom strength, and (2) the infrequent satellite observations from L5TM make it difficult to draw statistically meaningful conclusions."
- **[✓ verified]** Re-examining historical Landsat 5 TM true-color imagery for the same 71 lakes used in Ho et al., the authors find that sediment plumes — which can be spectrally confused with phytoplankton blooms in the NIR band — could occur in at least 58 of those 71 lakes, i.e., 82% of the sample.
  - *evidence:* Based on the authors' own visual/qualitative examination of true-color Landsat composites (from the USGS GloVis archive) for the identical 71-lake set. (Main text / Extended Data figures)
  - *quote:* "sediment plumes could occur in at least 58 (82%) of the 71 lakes studied in Ho et al."
- **[✓ verified]** Using independently collected in-situ chlorophyll-a and field spectral reflectance data from 15 lakes in China, the authors found no statistically significant relationship between NIR-band surface reflectance and measured chlorophyll-a, undercutting the premise that NIR reflectance tracks bloom (chlorophyll) concentration.
  - *evidence:* Direct empirical (negative) result presented as evidence against NIR reflectance as a bloom-strength proxy; based on field spectrometer and lab chlorophyll-a measurements across a range of chlorophyll-a concentrations and lakes. (Extended Data Fig. 1 and associated text)
  - *quote:* "The correlations for different Chl_a ranges (colour-coded) and individual lakes are non-significant (P > 0.05)."
- **[✓ verified]** The Fmask algorithm used in the original study's Landsat processing pipeline can erroneously classify intensely bloomed water pixels as non-water, causing the most severe blooms to be excluded from the analyzed record.
  - *evidence:* Illustrated via an Extended Data figure comparing true-color imagery to the Fmask classification output over bloom-affected areas. (Extended Data Fig. 5 (figure/caption description))
  - *quote:* "intense blooms (greenish in the red squares) have been classified as other classes instead of as water"
- **[✓ verified]** Comparing sparse Landsat 5 TM acquisition dates against a higher-frequency (daily) bloom-area record for Taihu Lake (2000–2008) shows that L5TM's infrequent revisit captures only scattered snapshots of a bloom's true day-to-day variability, weakening confidence in long-term trend conclusions drawn from L5TM alone.
  - *evidence:* Presented as a case-study illustration of the sampling-frequency problem underlying concern (2) in the paper's central thesis. (Extended Data Fig. 6)
  - *quote:* "daily areas of algal bloom in Taihu Lake between 2000 and 2008"

## Data / numbers
- 71 large lakes — the global lake sample from Ho et al. (2019) re-examined by this comment
- 68% of the 71 large lakes — share reported by Ho et al. (2019) to show increased peak summertime bloom intensity, 1982–2012 (30-year period); this is the contested figure, not this source's own finding
- 58 lakes (82% of 71) — number/share of Ho et al.'s lake sample in which Feng et al. found sediment plumes could occur, based on historical Landsat true-color imagery
- 15 lakes (China) — in-situ chlorophyll-a and field-spectral validation dataset collected by Feng et al.
- P > 0.05 — reported non-significant correlation between NIR surface reflectance and chlorophyll-a across Chl-a ranges and individual lakes
- Nature volume 590, pages E35–E47, published 17 February 2021 — publication details; DOI 10.1038/s41586-021-03254-3

## Methods
Feng et al. do not propose a new bloom-detection algorithm; they re-analyze the same satellite record used by Ho, Michalak & Pahlevan (2019) — Landsat 5 TM imagery (1982–2012, sourced from the USGS GloVis archive) — for the identical 71 global lakes, examining true-color image composites to visually identify sediment plumes and submerged aquatic vegetation that could be spectrally confused with phytoplankton blooms in the NIR band. They cross-check this against independently collected in-situ data (chlorophyll-a concentrations and field spectral reflectance, reported as measured with a field-portable spectrometer, from 15 lakes in China), correlating in-situ NIR reflectance against measured chlorophyll-a and finding a non-significant relationship (P > 0.05). They also examine the Fmask cloud/water-classification algorithm used in the original study's Landsat processing pipeline, showing it can misclassify intensely bloomed pixels as non-water and thus exclude the most severe blooms from the record, and they contrast L5TM's sparse revisit frequency against a higher-frequency bloom-area time series for Taihu Lake (2000–2008) to argue the original 30-year record undersamples genuine bloom variability. Where the source says the original approach fails: single-band NIR reflectance conflates phytoplankton signal with sediment resuspension and submerged-vegetation reflectance; Fmask masking can drop the most intensely bloomed (and most policy-relevant) pixels; and L5TM's revisit interval is too coarse relative to true bloom dynamics to support statistically robust long-term trend claims.

## Stated limitations
The fetched text — a short Nature "Matters Arising" comment rather than a full research article — does not contain an explicit, labeled self-limitations section. The clearest self-reported caveat embedded in the authors' own presented evidence is that their in-situ NIR-reflectance-vs-chlorophyll-a comparison, across different chlorophyll-a ranges and individual lakes, itself returned only a non-significant relationship (P > 0.05) — a null result the authors use as evidence against the original proxy rather than as an acknowledged weakness of their own critique. Beyond that, the fetched text does not address (nor flag) whether the 15 Chinese lakes used for in-situ validation are geographically or limnologically representative of Ho et al.'s original 71 globally distributed lakes, and it does not report a formal uncertainty estimate (e.g., confidence interval) around the "58 (82%) of 71 lakes" sediment-plume figure, which appears to derive from visual/qualitative examination of true-color imagery rather than a quantified statistical test. These are gaps observed in the extracted text, not caveats the authors themselves stated.

## Tensions with other findings
This source is itself a direct scientific rebuttal of Ho, Michalak & Pahlevan, "Widespread global increase in intense lake phytoplankton blooms since the 1980s" (Nature 574, 667–670, 2019), which reported that 68% of 71 large global lakes showed increasing peak summertime bloom intensity from 1982–2012 using Landsat 5 TM near-infrared reflectance. Feng et al. argue that trend may be a methodological artifact of sediment/vegetation confounding and satellite undersampling rather than a genuine bloom signal — a direct contradiction of the earlier paper's headline claim. Web search (not this article's fetched text) confirms that Ho, Michalak & Pahlevan published a formal reply in the same Nature issue and date ("Reply to: Concerns about phytoplankton bloom trends in global lakes," Nature 590, E48–E50, 17 Feb 2021, https://www.nature.com/articles/s41586-021-03255-2), defending their original approach; that reply was not fetched or summarized here and is a separate, uncited source. Any literature-review entry citing the original 2019 Ho et al. global-bloom-trend finding should cross-reference this unresolved methodological dispute. More broadly, this source is a caution against treating any single-band satellite reflectance index (including cyanobacteria-specific spectral indices such as those used by EPA CyAN) as a reliable bloom-strength proxy without in-situ ground-truthing and adequate revisit frequency — directly relevant to any project design (such as HAB_PoC) that fuses a satellite spectral signal with in-situ data.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All six claims are clearly supported by the source text. The numerical figures (68%, 71 lakes, 58 lakes, 82%, 15 lakes, 2000–2008) are all directly present in the source. The interpretive framing (e.g., that sediment plume confusion 'undercuts' the NIR-proxy premise, or that scattered data points 'weaken confidence') represents reasonable inference from explicitly stated empirical findings, not hallucination or overstatement. No material caveats are dropped from the claims. The claims accurately represent the structure and content of the comment on Ho et al."

## Provenance
- Canonical URL: https://www.nature.com/articles/s41586-021-03254-3
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: The canonical Nature URL initially returned a 303 redirect to an authentication page (idp.nature.com), which the WebFetch tool auto-followed; Nature's server then served substantial article content back through a "?error=cookies_not_supported&code=..." fallback URL rather than a hard paywall block. Three WebFetch calls were made against this same resolved page (two with broad comprehensive-extraction prompts as required for a HIGH-relevance source, plus one additional verification pass requesting strictly verbatim sentence-level quotes) to reconcile content the small extraction model might drop or vary between calls. Key figures — "58 (82%) of the 71 lakes," "68% of the 71 large lakes," and "P > 0.05" — recurred identically, word-for-word, across independent fetch calls, which gives reasonable confidence this is genuine article/Extended-Data text rather than fabrication, though some secondary details (e.g., the "PSR+3500" field-spectrometer model name) appeared in only one of the three fetches and are reported with correspondingly lower confidence. No traditional abstract exists for this comment format (confirmed by one fetch explicitly noting its absence). The companion reply article (Nature 590, E48–E50, s41586-021-03255-2) was identified only via WebSearch, not fetched or read, and is not summarized here.
