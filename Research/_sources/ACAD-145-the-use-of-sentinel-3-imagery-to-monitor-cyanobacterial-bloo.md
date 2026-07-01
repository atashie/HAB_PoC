---
key: ACAD-145
title: The Use of Sentinel-3 Imagery to Monitor Cyanobacterial Blooms
authors_or_org: Igor Ogashawara (Department of Earth Sciences, Indiana University-Purdue University Indianapolis, Indianapolis, IN, USA; ORCID 0000-0001-6328-0001)
year: 2019
url: https://www.mdpi.com/2076-3298/6/6/60
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article, open access (MDPI, Environments, CC-BY 4.0)
categories: [remote-sensing]
relevance: Medium
full_text_access: abstract
fetch_status: partial
review_severity: clean
review_overall: pass
---

# The Use of Sentinel-3 Imagery to Monitor Cyanobacterial Blooms

**What it is.** A short, single-author open-access journal article (Ogashawara, 2019, Environments 6(6):60, MDPI) that case-studies whether the Ocean and Land Colour Instrument (OLCI) aboard the Sentinel-3 satellite can identify the two pigments used to remotely detect cyanobacterial harmful algal blooms (CHABs) — phycocyanin (PC) and chlorophyll-a (chl-a) — using OLCI imagery over the western basin of Lake Erie, U.S.A., across the 2016, 2017 and 2018 bloom seasons.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study's explicit goal was to evaluate whether Sentinel-3/OLCI can identify phycocyanin and chlorophyll-a.
  - *evidence:* Stated directly as the study's goal in the opening of the abstract. (Abstract)
  - *quote:* "The goal of this study is to evaluate the potential of recent launch the Ocean and Land Color Instrument (OLCI) on-board the Sentinel-3 satellite to identify PC and chl-a."
- **[✓ verified]** Remote monitoring of CHABs is explicitly grounded in the optical properties of two specific pigments, phycocyanin and chlorophyll-a.
  - *evidence:* Definitional statement of the bio-optical targets used throughout the study. (Abstract)
  - *quote:* "Remote monitoring of CHABs relies on the optical properties of pigments, especially the phycocyanin (PC) and chlorophyll-a (chl-a)."
- **[✓ verified]** Data consisted of OLCI images over the western part of Lake Erie, USA, collected during three summer bloom seasons: 2016, 2017 and 2018.
  - *evidence:* Direct statement of study area and study period (three years of summer imagery). (Abstract)
  - *quote:* "OLCI images were collected over the Western part of Lake Erie (U.S.A.) during the summer of 2016, 2017, and 2018."
- **[✓ verified]** None of the traditional remote-sensing algorithms tested could accurately estimate both PC and chl-a together.
  - *evidence:* Reported as a negative/cautionary result for legacy algorithms applied to OLCI data. (Abstract)
  - *quote:* "When comparing the use of traditional remote sensing algorithms to estimate PC and chl-a, none was able to accurately estimate both pigments."
- **[✓ verified]** Simpler empirical approaches (single bands and band ratios) gave stronger correlations for estimating the pigments than the traditional algorithms did.
  - *evidence:* Presented as the counterpoint finding to the traditional-algorithm failure noted above. (Abstract)
  - *quote:* "However, when single and band ratios were used to estimate these pigments, stronger correlations were found."
- **[✓ verified]** The authors' recommendation is that OLCI spectral band selection be re-examined to build new, sensor-specific retrieval algorithms.
  - *evidence:* Stated as the paper's actionable takeaway following the band-ratio result. (Abstract)
  - *quote:* "These results indicate that spectral band selection should be re-evaluated for the development of new algorithms for OLCI images."
- **[✓ verified]** Overall conclusion is a hedged, qualified endorsement: Sentinel-3/OLCI has potential for PC/chl-a identification but is not yet operationally validated because dedicated algorithm development is still required.
  - *evidence:* Final summary sentence of the abstract; explicitly qualifies the positive finding. (Abstract / Conclusion)
  - *quote:* "Sentinel 3/OLCI has the potential to be used to identify PC and chl-a. However, algorithm development is needed."
- **[✓ verified]** The paper frames CHABs as a concern specifically for water bodies used for drinking-water supply and recreation, motivating why CHAB monitoring matters for water-governance policy.
  - *evidence:* Opening motivational framing of the abstract; sets up why remote monitoring of CHABs is treated as necessary. (Abstract (opening/introduction sentences))

## Data / numbers
- Imagery/study period: summers of 2016, 2017, and 2018 (three bloom seasons) over the western basin of Lake Erie, U.S.A. — no baseline or uncertainty stated in the abstract.
- Bibliographic: Environments 2019, Volume 6, Issue 6, article/page no. 60 (MDPI); published 2019-06-03; DOI 10.3390/environments6060060; Crossref reference-count (length of the paper's own bibliography) = 40.
- Bibliometric context only (not a scientific finding; current as of this fetch, varies by database, no fixed audit date available): OpenAlex citation count = 35 (FWCI 3.4917, 91.97th percentile); Semantic Scholar citation count = 31; Crossref is-referenced-by-count = 31.
- No R^2, RMSE, p-value, band-wavelength (nm), sample-size (n), or concentration-threshold (µg/L) figures could be retrieved for this specific paper — such figures would be in the Methods/Results sections, which were not accessible in this fetch (abstract-only access).

## Methods
Sensor/data: Ocean and Land Colour Instrument (OLCI) aboard the Sentinel-3 satellite (Copernicus/ESA). Design (per abstract only): OLCI imagery acquired over the western basin of Lake Erie, U.S.A., during the bloom-season summers of 2016, 2017 and 2018, used to test retrieval of two CHAB-indicator pigments — phycocyanin (PC) and chlorophyll-a (chl-a). Two classes of retrieval approach were compared: (a) unnamed "traditional remote sensing algorithms" for PC/chl-a, which could not jointly/accurately estimate both pigments; and (b) simpler empirical single-band and band-ratio approaches, which produced "stronger correlations." The abstract does not name the specific traditional algorithms tested (e.g., whether Gons-, Simis-, or Mishra-type phycocyanin algorithms, or two-band/three-band chlorophyll algorithms were used), does not identify which individual bands or ratios performed best, does not describe the in-situ sampling/matchup protocol (sample counts, matchup time window, lab analysis method), and gives no quantitative accuracy statistics (R², RMSE, bias, n). Those specifics would presumably appear in the Methods/Results/Tables of the full text, which could not be retrieved in this fetch (see fetch_notes).

## Stated limitations
Only the abstract was accessible, and it contains no itemized "limitations" statement. The closest self-declared caveats retrievable are: (1) the negative result that none of the traditional algorithms tested could jointly/accurately estimate both PC and chl-a ("none was able to accurately estimate both pigments"), and (2) the hedged closing statement that although OLCI "has the potential" to identify PC and chl-a, "algorithm development is needed" — i.e., the authors do not claim a validated, ready-to-use retrieval algorithm, only sensor potential. Any further caveats the full paper may state (e.g., atmospheric correction, cloud contamination, matchup time-lag between satellite overpass and in-situ sampling, near-shore mixed-pixel/spatial-resolution effects, or single-lake/single-region generalizability) could not be verified because the Methods/Discussion sections were not retrievable in this fetch — this is a limitation of the extraction, not a claim about what the paper itself does or doesn't say beyond the abstract.

## Tensions with other findings
The paper's central self-reported negative finding — that "traditional remote sensing algorithms" could not jointly retrieve both phycocyanin and chlorophyll-a from OLCI imagery — is a useful caution against treating "Sentinel-3 can monitor cyanoHABs" as a single, settled, algorithm-agnostic capability; it separates the sensor's raw potential from the maturity of any specific retrieval algorithm. This is worth flagging against HAB literature (e.g., material built on EPA CyAN's operational Sentinel-3-based cyanobacteria index) that may present satellite-derived cyanobacteria detection as already fully solved: this source suggests that, at least as of 2019 and for this one lake, algorithm/band-selection choice was still an open problem for jointly estimating PC and chl-a. This is the paper's own qualitative claim, not a quantitative benchmark against CyAN specifically, and no causal claim is implied or should be drawn from it.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0

## Provenance
- Canonical URL: https://www.mdpi.com/2076-3298/6/6/60
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Primary URL (https://www.mdpi.com/2076-3298/6/6/60) returned HTTP 403 Forbidden on repeated WebFetch attempts (base URL x2, /htm variant, /pdf variant; the DOI resolver redirects back to the same blocked URL). ResearchGate mirror also 403. The MDPI-hosted PDF was fetched as raw bytes via the author's institutional repository (IUPUI ScholarWorks, hdl.handle.net/1805/22501 -> scholarworks.indianapolis.iu.edu bitstream) — confirmed ~2.5MB retrieved — but WebFetch's content processor could not extract readable text from the binary PDF stream, so full body text (Methods/Results/Discussion/explicit Limitations) was not recoverable. web.archive.org is blocked entirely for this tool ("Claude Code is unable to fetch from web.archive.org"). The r.jina.ai reader proxy returned 401 Unauthorized. Europe PMC has no indexed record for this DOI (0 hits on direct DOI query). Successfully obtained the full VERBATIM abstract independently from two structured bibliographic APIs — Semantic Scholar Graph API (field explicitly labeled verbatim) and OpenAlex (reconstructed word-for-word from the raw abstract_inverted_index) — and the two reconstructions matched exactly, giving high confidence in the abstract text; the author's IUPUI ScholarWorks landing page independently corroborated the same key sentences via a separate HTML-scrape fetch. Crossref metadata confirmed volume/issue/date/license/reference-count but returned only a paraphrased (non-verbatim) abstract summary, so it was used for bibliographic fields only, not quotes. A WebSearch snippet surfaced a specific R^2 figure set ("0.47 (0.42) for chlorophyll-a, 0.69 (0.22) for phycocyanin, 0.70 (0.41) for Pc:Chla") attributed only tentatively ("appears to be from research by Ogashawara and colleagues") and structured as paired Sentinel-2/Sentinel-3 comparisons that this 2019 Sentinel-3-only paper's abstract never mentions — judged likely to belong to a different Ogashawara publication and deliberately excluded from this dossier to avoid misattribution. No numeric results (R^2, RMSE, band wavelengths, sample sizes, concentration thresholds) could be verified as belonging to THIS specific paper; only the qualitative abstract-level claims are reported. full_text_access is therefore set to "abstract" and fetch_status to "partial."
