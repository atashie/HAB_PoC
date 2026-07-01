---
key: ACAD-140
title: Retrieval of phycocyanin concentration from remote-sensing reflectance using a semi-analytic model in eutrophic lakes
authors_or_org: Heng Lyu, Qiao Wang, Chuanqing Wu, Li Zhu, Bin Yin, Yunmei Li, Jiazhu Huang
year: 2013
url: https://doi.org/10.1016/j.ecoinf.2013.09.002
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article
categories: [remote-sensing]
relevance: Medium
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# Retrieval of phycocyanin concentration from remote-sensing reflectance using a semi-analytic model in eutrophic lakes

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/pii/S1574954113000861

**What it is.** A 2013 peer-reviewed methods paper (Lyu, Wang, Wu, Zhu, Yin, Li & Huang; Ecological Informatics, Vol. 18, pp. 178-187) that evaluates the semi-analytic phycocyanin (PC) retrieval algorithm of Simis et al. (2005) and proposes a modified version -- replacing a constant specific-absorption coefficient with a concentration-dependent power-function and recalibrating the model's correction coefficients from in-situ data -- calibrated on the eutrophic Taihu Lake (China) and validated against Dianchi Lake (China).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Phycocyanin (PC) is framed as a pigment unique to freshwater cyanobacteria ('blue-green algae') and is commonly used as a quantitative indicator of cyanobacteria abundance in eutrophic inland waters -- the motivating rationale for retrieving it remotely.
  - *evidence:* Opening framing sentence of the abstract, establishing why remote retrieval of PC is useful for eutrophic-lake / HAB monitoring. (Abstract)
  - *quote:* "Phycocyanin (PC), an accessory pigment unique to freshwater blue-green algae, is often used as a quantitative indicator of blue-green algae in eutrophic inland waters."
- **[✓ verified]** The study's stated purpose was to evaluate the existing semi-analytic PC retrieval algorithm developed by Simis et al. and to test whether it could be improved for eutrophic lakes such as Taihu Lake.
  - *evidence:* Direct statement of study aim, recurring identically across independent search retrievals of the abstract. (Abstract)
  - *quote:* "The purpose of this study was to evaluate the semi-analytic PC retrieval algorithm proposed by Simis et al. and to explore the potential to improve this PC algorithm so that it is more suitable for eutrophic lakes, such as Taihu Lake."
- **[✓ verified]** The authors recalibrated the Simis-model correction coefficients (γ and δ) -- which scale the absorption of chlorophyll-a at 665 nm and of PC at 620 nm -- from their own in-situ measurements rather than reusing the originally published coefficients.
  - *evidence:* Describes the specific recalibration step taken to adapt the algorithm; reconstructed consistently (though with some reworded phrasing each time) across independent search summaries, so treated as a paraphrase rather than an exact quote. (Abstract/Methods (as indexed by search))
- **[✓ verified]** The specific absorption coefficient of PC at 620 nm, a*pc(620), was found to decrease exponentially as PC concentration increases rather than being constant as Simis et al. assumed; the authors replaced the constant with a non-linear power-function of a*pc(620) in their revised algorithm.
  - *evidence:* Central methodological change reported in the abstract, explaining why a fixed coefficient from the original algorithm was judged inadequate for this system. (Abstract)
  - *quote:* "a non-linear power–function of apc*(620), instead of a constant value of apc*(620) as used by Simis et al., was proposed for an improved PC retrieval algorithm"
- **[✓ verified]** In Taihu Lake, the improved retrieval algorithm achieved R² = 0.55 and RMSE = 58.89 µg/L for phycocyanin concentration.
  - *evidence:* Primary quantitative performance figures given in the abstract for the calibration lake; no confidence interval or error bound on R2/RMSE was present in any retrieved text. (Abstract)
  - *quote:* "yielding a squared correlation coefficient (R2) of 0.55 and a root mean square error (RMSE) of 58.89µg/L"
- **[✓ verified]** The improved algorithm is reported to have 'generally superior performance' relative to the original Simis et al. algorithm, but the source text as retrieved does not give the original algorithm's own R2/RMSE figures on the same Taihu data, so no side-by-side numeric baseline could be confirmed.
  - *evidence:* Comparative claim stated qualitatively in the abstract; the quantitative baseline for the 'original' algorithm was not recoverable via the available access route, which is itself a gap worth flagging under the fidelity/baseline standard. (Abstract)
  - *quote:* "the improved retrieval algorithm has generally superior performance compared with the original PC retrieval algorithm by Simis et al."
- **[✓ verified]** The improved algorithm was validated against an independent dataset from Dianchi Lake, and an accompanying error analysis is reported to show it generalizes ('universality') better than the original algorithm, particularly at higher PC concentrations.
  - *evidence:* States the out-of-sample validation lake and the qualitative conclusion drawn from that validation step. (Abstract)
  - *quote:* "Validation in Dianchi Lake and an error analysis proved that the improved PC algorithm has a better universality and is more suitable for eutrophic lakes with higher PC concentrations."
- **[✓ verified]** Retrieval error is reported to be primarily associated with the ratio of total suspended solids to phycocyanin (TSS:PC), rather than the ratio of chlorophyll-a to phycocyanin (Chl-a:PC); both the original and improved models are indicated to perform poorly when PC concentration is low and TSS is high.
  - *evidence:* Reconstructed consistently (recurring across at least three independent search retrievals with the same TSS:PC framing) as an error-source / limitation finding, though no single verbatim sentence could be isolated, so it is reported as paraphrase rather than quoted. (Discussion/Conclusion (as indexed by search))
- **[✓ verified]** The recalibrated correction coefficients (γ, δ) are described as differing from values used/reported elsewhere, attributed to the coefficients being site-dependent because of differing bio-optical properties among lakes.
  - *evidence:* Implies the fixed semi-analytic parameterization is not directly transferable across water bodies without local recalibration -- relevant to any assumption that one algorithm generalizes across lakes. (Discussion (as indexed by search))

## Data / numbers
- R² = 0.55 (improved phycocyanin retrieval algorithm, calibrated/tested in Taihu Lake)
- RMSE = 58.89 µg/L (improved phycocyanin retrieval algorithm, Taihu Lake; no confidence interval reported in retrievable text)
- Journal: Ecological Informatics, Volume 18, pp. 178–187 (2013)
- DOI: 10.1016/j.ecoinf.2013.09.002
- Key absorption wavelengths used in the underlying semi-analytic (Simis-type) model: 620 nm (phycocyanin absorption) and 665 nm (chlorophyll-a absorption)

## Methods
Builds on the semi-analytic bio-optical phycocyanin (PC) retrieval framework originated by Simis et al. (2005), which estimates PC concentration from remote-sensing reflectance via absorption terms at 620 nm (PC) and 665 nm (chlorophyll-a), scaled by correction coefficients gamma and delta. This paper (a) recalibrates gamma and delta from in-situ measurements rather than reusing the original published values, and (b) replaces Simis et al.'s constant specific-absorption coefficient a*pc(620) with a non-linear power-function of PC concentration, based on the observation that a*pc(620) declines exponentially as PC increases. The revised ("improved") model was developed/fit using data from the eutrophic, cyanobacteria-affected Taihu Lake (China) and then independently tested against data from a second eutrophic system, Dianchi Lake (China). Reported to work: fits Taihu data at R2=0.55, RMSE=58.89 ug/L, and -- per the Dianchi validation and accompanying error analysis -- generalizes better than the original Simis algorithm, especially at higher PC concentrations. Reported to fail / degrade: both the original and improved formulations are indicated to underperform when PC concentration is low and total suspended solids (TSS) are high, with the TSS:PC ratio (rather than Chl-a:PC) flagged as the dominant factor associated with retrieval error. Exact sample sizes, sampling dates, and the original algorithm's own numeric R2/RMSE on the same data were not recoverable through the abstract-level access obtained for this dossier.

## Stated limitations
From the retrievable (abstract-level) text: (1) both the original Simis et al. algorithm and this paper's improved version are indicated to perform poorly when PC concentration is low and total suspended solids (TSS) are high; (2) the TSS:PC ratio, rather than the Chl-a:PC ratio, is identified as the main factor associated with retrieval error, implying sensitivity to non-algal turbidity/sediment; (3) the recalibrated correction coefficients (gamma, delta) are described as site-dependent, differing from values used in other studies because of differing lake bio-optical properties -- implying the parameterization is not a plug-and-play fit across arbitrary water bodies without local recalibration. Caveat on this dossier's own limitation: because full text was not accessible (paywalled; all WebFetch attempts on the article and its mirrors returned HTTP 403/301 or empty content), these limitation statements were reconstructed from convergent search-engine summaries rather than a single directly-quoted passage, and exact sample sizes, sampling dates/sites, and the original algorithm's own R2/RMSE for direct comparison could not be verified or reported.

## Tensions with other findings
The paper's central move -- replacing a constant specific-absorption coefficient a*pc(620) (as used in the original Simis et al. 2005 algorithm, calibrated elsewhere) with a lake/concentration-dependent power-function to fit Taihu Lake, plus finding the gamma/delta coefficients themselves to be "site dependent" -- indicates that semi-analytic phycocyanin retrieval algorithms do not transfer cleanly across water bodies without local recalibration. For a HAB early-warning or multi-lake product, this complicates any assumption that a single reflectance-to-pigment algorithm (or a single set of coefficients) generalizes across different lakes/regions; it supports treating satellite-retrieved pigment concentrations as requiring site-specific validation. Separately, the reported R2 of 0.55 is a modest fit (roughly half the variance explained) with no stated confidence interval, and the qualitative claim of "generally superior performance" over the original algorithm could not be checked against the original algorithm's own quantitative error statistics in the text recovered for this dossier -- a gap that itself illustrates the risk of accepting comparative claims without the matching baseline number, consistent with the general principle that every reported metric needs a stated baseline and uncertainty. All reflectance-to-pigment relationships here are empirical/semi-analytic curve fits, not causal claims about bloom formation.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All nine claims are directly supported by the source text. No hallucinated numbers detected; all performance metrics (R² = 0.55, RMSE = 58.89 µg/L) and wavelength references (620 nm, 665 nm) are present in the source. Claim 6, which is meta-analytical in nature (noting what the source does NOT provide), is accurate to the source text as presented. No material scientific caveats are dropped. The source text is a reconstruction via convergent WebSearch queries and Semantic Scholar metadata rather than direct access to the full published abstract or paper, but all claims extract and accurately reflect the reconstructed content."

## Provenance
- Canonical URL: https://doi.org/10.1016/j.ecoinf.2013.09.002
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Primary URL blocked WebFetch with HTTP 403 (bot/paywall block) on both the /pii/ and /abs/ ScienceDirect variants of this article. A WebFetch of the ResearchGate mirror (researchgate.net/publication/259163338) also returned HTTP 403. A WebFetch of the FAO AGRIS record page returned an unresolved HTTP 301 redirect. A WebFetch of the Lens.org scholar-search page returned only the site's navigation shell (JS-rendered, no article content). A WebFetch of the Semantic Scholar Graph API (paper DOI:10.1016/j.ecoinf.2013.09.002) succeeded and confirmed authoritative bibliographic metadata (title, 7 authors, year 2013, venue "Ecological Informatics") but returned the paper's abstract field as "Not available (elided by publisher)" -- i.e., not accessible via that route either. Per the task's fallback instruction, I then used WebSearch (multiple independent queries) to reconstruct abstract-level content. Across roughly 8 separate WebSearch calls, the same sentences, numbers, and special notation (R2, RMSE, Greek letters γ/δ, the term "a_pc*(620)") recurred essentially verbatim, which gives reasonable confidence these reflect the actual publicly indexed abstract text rather than model invention -- but I cannot rule out minor paraphrasing by the search layer, so quotes below are limited to the fragments that recurred identically across calls, and other content is flagged as paraphrase. No full-text methods/results (exact sample sizes, sampling dates/sites, original Simis-algorithm's own R2/RMSE for direct numeric comparison, explicit statistical uncertainty on R2/RMSE) could be recovered through this route; those specifics are therefore omitted rather than guessed. url_used = the ScienceDirect PII URL given in the task (confirmed as the correct/canonical landing page by every WebSearch call); resolved_url = the DOI resolver URL for the same article.
