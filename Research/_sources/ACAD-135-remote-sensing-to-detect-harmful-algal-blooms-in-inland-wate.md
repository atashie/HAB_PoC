---
key: ACAD-135
title: Remote sensing to detect harmful algal blooms in inland waterbodies
authors_or_org: Liu, S.; Glamore, W.; Tamburic, B.; Morrow, A.; Johnson, F. — per independent UNSW Sydney staff/research pages (Dr Shuang Liu, Dr Bojan Tamburic) surfaced in search, the author team appears affiliated with UNSW Sydney (Water Research Laboratory / Nuisance and Harmful Algae Science-Practice Partnership, NHASP); this affiliation is corroborating context, not verified against the paper's own affiliation line, which was not accessible.
year: 2022
url: https://www.sciencedirect.com/science/article/abs/pii/S0048969722051956
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (primary research study)
categories: [remote-sensing]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Remote sensing to detect harmful algal blooms in inland waterbodies

**What it is.** A peer-reviewed primary-research journal article (Liu, Glamore, Tamburic, Morrow & Johnson, 2022, Science of the Total Environment, 851(Pt 1):158096) that empirically compares three satellite platforms (Planetscope, Sentinel-2, Landsat-8) and 20 existing spectral-index algorithms plus a Self-Organizing Map (SOM) method for detecting harmful algal blooms (HABs) in small-to-medium inland waterbodies, a setting where satellite-based HAB detection is far less established than in large lakes.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Satellite remote sensing is already a well-established HAB monitoring tool for large lakes, but reliably detecting HABs in small-to-medium waterbodies via satellite data is still an unsolved problem.
  - *evidence:* Stated directly in the abstract as the motivating problem for the study, contrasting large-lake RS maturity against small/medium-waterbody difficulty. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "accurate HAB detection in small-medium waterbodies via satellite data remains a challenge"
- **[✓ verified]** The abstract enumerates three specific current barriers to satellite-based HAB detection in small/medium waterbodies: waterbody size itself, scarcity of freely available high-resolution imagery, and lack of field (in-situ) calibration data.
  - *evidence:* Direct enumerated list in the abstract's framing of the problem. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "the waterbody size, the limited freely available high resolution satellite data, and the lack of field calibration data"
- **[✓ verified]** The study empirically compared three satellite platforms — Planetscope, Sentinel-2, and Landsat-8 — specifically to isolate how spatial resolution, spectral-band availability, and waterbody size each affect HAB detection skill.
  - *evidence:* Describes the core experimental design/comparison set up by the authors. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "three satellites (Planetscope, Sentinel-2 and Landsat-8) were used to understand how spatial resolution, the availability of spectral bands, and the waterbody size itself effect HAB detection skill"
- **[✓ verified]** Among 20 existing HAB-detection spectral-index algorithms tested (alongside a non-parametric Self-Organizing Map method), the indices 'Curvature Around Red' and 'NIR minus Red' performed best.
  - *evidence:* Direct result statement ranking algorithm performance; this is the paper's central algorithmic finding. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "Curvature Around Red and NIR minus Red had the best HAB detection skill of the 20 existing algorithms that were tested"
- **[⚠ partial]** Landsat-8 and Sentinel-2 outperformed Planetscope for HAB detection in small-to-medium waterbodies, despite Planetscope's finer native spatial resolution.
  - *evidence:* Direct comparative result across the three tested satellite platforms. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "Landsat 8 and Sentinel 2 were the best satellites for HAB detection in small to medium waterbodies"
  - *reviewer:* Core finding (L8 and S2 were best) is supported by the source, but the explanatory clause about Planetscope having finer native spatial resolution is not stated in the abstract and relies on outside knowledge.
- **[⚠ partial]** The single most important satellite attribute for HAB detection is which spectral bands are available on the sensor, because band availability constrains which detection algorithms can even be applied — outweighing spatial resolution as a driver of performance.
  - *evidence:* Explicit attribution statement in the abstract; framed as the study's key mechanistic explanation for why some satellites/algorithms outperform others. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "The most critical attribute for detecting HABs were the available satellite bands, which determine the detection algorithms that can be used"
  - *reviewer:* Source confirms bands are 'most critical' and determine which algorithms can be used, but does not explicitly compare or state they outweigh spatial resolution as a relative driver of performance—that comparative claim is inferential.
- **[✓ verified]** Across the satellites and algorithms tested, detection-algorithm performance showed little relationship to the physical size of the waterbody being monitored (an associational finding from this comparison, not a demonstrated causal mechanism).
  - *evidence:* Direct empirical result stated in the abstract; framed here as correlational, per instructions to avoid causal overreach. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "algorithm performance was mostly unrelated to waterbody size"
- **[✓ verified]** Even where a good detection algorithm/satellite pairing exists, practical barriers remain: algae dynamics, macrophyte (aquatic plant) cover within the waterbody, weather effects, and imperfect satellite data correction models, plus a need to time-match satellite overpasses with field sampling for calibration.
  - *evidence:* Direct list of caveats/barriers stated by the authors after presenting their main results, framed as remaining operational challenges. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "algae dynamics, macrophyte cover within the waterbody, weather effects, and the correction models for satellite data"
- **[✓ verified]** The authors' operational recommendation is to combine regular in-situ/field sampling with satellite remote sensing, rather than relying on satellite data alone, for monitoring and managing small-to-medium waterbodies.
  - *evidence:* Direct closing recommendation of the abstract. (Abstract; Sci. Total Environ. 2022;851(Pt 1):158096 (PMID 35987216, via PubMed))
  - *quote:* "integrating regular sampling activities and remote sensing is recommended for monitoring and managing small-medium waterbodies"

## Data / numbers
- 3 satellite platforms compared: Planetscope, Sentinel-2, Landsat-8
- 20 existing HAB-detection algorithms tested, plus 1 additional non-parametric method (Self-Organizing Map, SOM)
- Science of the Total Environment, Vol. 851 (Part 1), article no. 158096
- Publication date: 10 Dec 2022 (Epub 18 Aug 2022)
- PMID 35987216; DOI 10.1016/j.scitotenv.2022.158096
- No quantitative accuracy/validation statistics (e.g., R², %, kappa, sample sizes) were present in the abstract-level text obtained for this entry — the full Methods/Results tables were inaccessible (paywalled) and are NOT reported here to avoid fabrication

## Methods
Per the abstract (full Methods section not accessible): three satellite platforms — Planetscope, Sentinel-2, and Landsat-8 — were compared over small-to-medium inland waterbodies to test how spatial resolution, spectral-band availability, and waterbody size affect HAB detection skill. Twenty existing spectral-index/threshold-style HAB-detection algorithms were tested, plus one additional non-parametric method, a Self-Organizing Map (SOM, an unsupervised neural-network clustering technique). No specific waterbody names/locations, date ranges, in-situ sample sizes, or validation statistics (R², accuracy %, kappa, etc.) are given in the abstract text obtained; these would presumably appear in the full-text Methods/Results, which were not accessible for this entry (ScienceDirect blocked; UTS repository PDF unreadable/unverifiable). Reported "works": Landsat-8 and Sentinel-2 (with the "Curvature Around Red" and "NIR minus Red" indices) gave the best detection skill, attributed to available spectral bands rather than spatial resolution or waterbody size. Reported "fails"/limits: Planetscope underperformed the other two despite finer spatial resolution; and even the best algorithm/satellite combinations are constrained in practice by algae dynamics, macrophyte cover, weather effects, imperfect atmospheric/data correction models, and the need to match satellite-overpass timing with field sampling for calibration.

## Stated limitations
The abstract itself frames several explicit barriers: (1) small/medium waterbody size, "the limited freely available high resolution satellite data," and "the lack of field calibration data" are named as the current barriers motivating the study; (2) even after identifying the best-performing satellite/algorithm combinations, the authors state "there remain some barriers in utilizing satellite data for HAB detection, including algae dynamics, macrophyte cover within the waterbody, weather effects, and the correction models for satellite data"; (3) a calibration-design caveat: "it is important to consider the match time between satellite overpass and sampling activities for calibration." Beyond the abstract, the paper's full Methods/Results/Discussion and any dedicated Limitations section were not accessible for this dossier entry (see fetch_notes), so limitations stated only in the body text (e.g., specific failure modes per algorithm, statistical uncertainty on the "unrelated to waterbody size" finding, or geographic/climatic generalizability of the study sites) could not be captured here and should not be assumed absent.

## Tensions with other findings
Three points worth flagging for a HAB literature review: (a) The abstract's own framing implies a scale-dependent split already present in the field: remote sensing is "an increasingly important tool for HAB detection and monitoring in large lakes" (the regime that moderate-resolution operational products such as EPA CyAN/Sentinel-3 OLCI target), but is explicitly harder for "small-medium waterbodies" — meaning large-lake-oriented HAB remote-sensing claims/tools may not transfer to the small ponds and reservoirs that make up much of SePRO's likely customer base. (b) The finding that Landsat-8 (30 m) and Sentinel-2 (10-20 m) "were the best satellites for HAB detection in small to medium waterbodies," beating Planetscope despite Planetscope's substantially finer (~3 m) native spatial resolution, cuts against an intuitive assumption that higher spatial resolution alone should help most in small waterbodies; the authors instead attribute this to spectral-band availability ("the most critical attribute"), which is the study's own attributional interpretation of a comparison across three sensors, not a controlled causal experiment. (c) The claim that "algorithm performance was mostly unrelated to waterbody size" is reported here as a correlational/associational finding from one study's comparison set; without the full-text statistics (not accessible here), it should not be generalized as a causal or universal law about sensor choice.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** Two claims (5 and 6) add interpretive or explanatory elements that are reasonable inferences but not explicitly stated in the source abstract. Claim 5's reference to Planetscope's finer spatial resolution is factually correct as general knowledge but is not mentioned in the abstract itself. Claim 6's explicit statement that band availability outweighs spatial resolution is a reasonable reading of 'most critical attribute' but is not directly comparative as phrased. All core findings are supported by the abstract; no material facts are hallucinated or omitted."

## Provenance
- Canonical URL: https://www.sciencedirect.com/science/article/abs/pii/S0048969722051956
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: Primary URL (ScienceDirect abs page) returned HTTP 403 Forbidden on WebFetch (bot/paywall block) on the first attempt and a retry via a text-proxy (r.jina.ai) returned HTTP 401. Per protocol, pivoted to WebSearch, which identified DOI 10.1016/j.scitotenv.2022.158096 and PMID 35987216. A candidate open PDF (UTS "Opus" institutional-repository bitstream) surfaced when searching the DOI string directly; WebFetch attempted it twice but could only retrieve raw, unparsed PDF binary/FlateDecode stream data (no readable text), so it was discarded as unusable and its identity as this specific article could not even be confirmed — it is NOT used as a source here. WebFetch of the PubMed record (PMID 35987216) succeeded and returned a complete, verbatim abstract plus authors, journal/volume/pages, DOI, dates, keywords, and MeSH terms. This was cross-checked against a direct WebFetch of the AGRIS/FAO bibliographic record, which mirrors the same abstract content and metadata (consistent, no discrepancies found). Full text (Introduction, Methods, Results tables/figures, Discussion, and the paper's own stated Limitations section) was never accessible, so this dossier entry is built strictly from the abstract and standard bibliographic metadata — no numeric accuracy/validation statistics could be extracted because none appear in the abstract. A separate WebSearch synthesis (not a direct fetch of the paper) additionally asserted a CRediT author-contribution breakdown and a funding acknowledgment (Hunter Water and Melbourne Water via the "Nuisance and Harmful Algae Science-Practice Partnership," NHASP). NHASP was independently confirmed as a real UNSW Sydney program via a separate direct search, but the specific claim that this paper credits/acknowledges it was not verified against the paper's own text, so it is excluded from key_claims/data_numbers and reported only here as an unverified aside.
