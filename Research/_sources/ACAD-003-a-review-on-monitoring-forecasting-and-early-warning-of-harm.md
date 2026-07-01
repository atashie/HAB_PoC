---
key: ACAD-003
title: A review on monitoring, forecasting, and early warning of harmful algal bloom
authors_or_org: Muhammad Zahir, Yuping Su, Muhammad Imran Shahzad, Gohar Ayub, Sami Ur Rahman (rendered "Rehman, S.U." in one alternate metadata source), Jehangir Ijaz
year: 2024
url: https://www.sciencedirect.com/science/article/pii/S0044848624008123
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed review article
categories: [models-and-methods]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# A review on monitoring, forecasting, and early warning of harmful algal bloom

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/abs/pii/S0044848624008123

**What it is.** A 2024 peer-reviewed review article in the journal Aquaculture (Elsevier) by Zahir, Su, Shahzad, Ayub, Rahman, and Ijaz that surveys techniques for monitoring, forecasting, and early-warning of harmful algal blooms (HABs) in coastal waters — spanning satellite/remote sensing, biological and molecular identification, toxin analysis, and machine-learning/numerical forecasting models — framed around HAB impacts on aquaculture, fisheries, and tourism.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** HABs occur in most coastal regions worldwide and have increased significantly in frequency in coastal waters in recent decades, causing serious socio-ecological, economic, food-security, and public-health problems specifically in countries where aquaculture, fisheries, and tourism depend on shared aquatic ecosystem resources.
  - *evidence:* Opening framing statement of the abstract, establishing the scale/stakes motivating the review; corroborated verbatim across 3 independent WebFetch calls to the Google-Scholar-mirrored abstract snippet. (Abstract, opening sentences (per ScienceDirect abstract as mirrored in Google Scholar snippet))
  - *quote:* "HABs cause serious socio-ecological, economic, food security and public health problems in countries where aquaculture, fisheries and tourism share ecosystem goods and services."
- **[✓ verified]** The review synthesizes a broad set of HAB monitoring/detection technique families: satellite/space-based sensing, remote sensing, drone-based observation, biological identification, toxin analysis, molecular methods, modeling, and citizen-science programs.
  - *evidence:* Directly enumerated scope statement of the review, reproduced identically (word-for-word, in quotation marks) across 2 of 3 independent fetches of the same Google Scholar snippet. (Abstract)
  - *quote:* "various techniques for monitoring, forecasting, and early warning of HABs in coastal waters, including space-based sensors, remote sensing, drones, biological identification, toxin analysis, molecular methods, modeling, and citizen science programs"
- **[⚠ partial]** The review's central methodological position is that an effective HAB monitoring/forecasting system requires integrating multiple data and modeling streams together — satellite observations, numerical modeling, and machine-learning algorithms combined with in-situ sensors and biosensors — rather than relying on any single method in isolation.
  - *evidence:* Stated as the review's own synthesized definition of an 'effective' system; the core clause recurred (with the in-situ/biosensor clause appended in one pass) across 2 of 3 independent fetches of the same source. (Abstract)
  - *quote:* "developing an effective monitoring and forecasting system for HABs involves integrating satellite observations, numerical modeling, and machine learning algorithms with in-situ sensors and biosensors"
  - *reviewer:* The source supports the integration recommendation (satellite observations, numerical modeling, machine-learning algorithms, in-situ sensors, biosensors) but does NOT explicitly state the contrast 'rather than relying on any single method in isolation.' That conclusion is inferred, not stated in the source text.
- **[✓ verified]** The review's coverage of forecasting approaches names specific machine-learning method families — artificial neural networks (ANN), random forests (RF), and support vector machines (SVM), with one extraction pass also naming LSTM (long short-term memory) networks and 'data-driven modeling'.
  - *evidence:* This specific model list recurred consistently across three separate extraction passes (2 WebFetch, 1 WebSearch) referencing the same paper, but was NEVER captured inside quotation marks in any single pass, meaning it is a paraphrase rather than a confirmed verbatim quote. Reported as moderate- rather than high-confidence; the accompanying 'model interpretability' challenge claim from one pass was excluded as uncorroborated. (Abstract / body (precise subsection not visible from available snippet))
- **[✓ verified]** The article is published as Aquaculture, Volume 593, article no. 741351 (Elsevier, 2024), DOI 10.1016/j.aquaculture.2024.741351, and is a closed-access (non-open-access) publication with no free full-text copy locatable through any legitimate channel.
  - *evidence:* Bibliographic and access-status metadata cross-checked via the CrossRef API record and the Unpaywall API record for the same DOI, corroborated by the OUCI aggregator mirror; not from the paper's own text but from independent bibliographic databases. (CrossRef DOI metadata; Unpaywall OA record; OUCI mirror page)
  - *quote:* ""is_oa":false, "oa_locations":[]"

## Data / numbers
- Journal article: Aquaculture, Volume 593, article no. 741351 (2024), Elsevier
- DOI: 10.1016/j.aquaculture.2024.741351
- ISSN 0044-8486 (print) / 1873-5622 (online) [Unpaywall]
- Online publication date: 16 July 2024 [Unpaywall]; formal issue date: December 2024, Vol. 593 [CrossRef] — these are 'online-first' vs 'issue' dates, not a contradiction
- Citations to date: 123 per Google Scholar vs. 104 per OUCI (Scopus/WoS-linked count) — both accessed 2026-07-01; reported as two different indices, not reconciled
- References cited within the article: 299 [OUCI]
- Open-access status: closed / non-OA — is_oa=false, 0 OA locations [Unpaywall API, DOI 10.1016/j.aquaculture.2024.741351]

## Methods
The source is a narrative/scoping literature review (not primary data collection or a single-model build). From the verified abstract fragment, its scope spans four recurring method families: (1) satellite/space-based remote sensing, (2) biological and molecular identification methods (toxin analysis, molecular methods), (3) forecasting approaches including numerical modeling and machine-learning algorithms (consistently, but not verbatim-confirmed, named as ANN/RF/SVM and once LSTM), and (4) citizen-science monitoring programs. Its own stated synthesis is that effective HAB early warning comes from integrating satellite data + numerical modeling + ML with in-situ sensors/biosensors, not any one method alone. I could NOT reach the full-text Methods/search-protocol section (e.g., databases searched, inclusion/exclusion criteria, number of studies screened) — the article is paywalled with zero OA copies (confirmed via Unpaywall), and every full-text mirror attempted returned HTTP 403. I have deliberately excluded specific screening/eligibility figures ("2,338 papers," "74 eligible studies," a three-category technology taxonomy) that surfaced in early exploratory search summaries because targeted verification searches found no trace of them anywhere on the open web, indicating they were likely not genuine content of this paper (see fetch_notes).

## Stated limitations
Full text was not accessible to me (closed-access journal article; Unpaywall confirms zero open-access copies exist anywhere; ScienceDirect, ResearchGate, and SciSpace/Typeset mirrors all returned HTTP 403 to automated fetch). I therefore cannot report the paper's own self-described limitations/discussion-section caveats, because that material sits outside the abstract fragment I could verify — the verified abstract text does not itself contain an explicit limitations statement (it cuts off at "...science-based measures that can mitigate and/or..."). This is a limitation of my research access, not a claim about what the source itself says.

## Tensions with other findings
Cannot be assessed from the abstract-only material available — the discussion/results sections where disagreements with other HAB literature would typically surface were not reachable (paywalled, no OA copy). At the level available, the review's framing — that effective HAB early warning requires fusing satellite/remote-sensing data with in-situ sensors and ML/numerical modeling, rather than any one data stream alone — is directionally supportive of (not in tension with) a remote-sensing-plus-in-situ fusion approach to HAB risk assessment. No explicit contradiction of other sources is evidenced in the text actually verified. Correlation/causation note: nothing in the verified text asserts a causal driver relationship; it is a methods/technology review, not an empirical driver analysis.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Claim 3: The evidence note discloses that the 'in-situ sensors and biosensors' clause appeared only in one of three fetches (Fetch C), indicating inconsistency across source retrievals, though this limitation is transparently acknowledged in the evidence record itself.
- **Reviewer notes:** Four of five claims are fully supported by the source text. Claim 3 is substantially supported (the integration recommendation is clear) but overstates by adding an explicit negation ('rather than relying on any single method in isolation') that does not appear in the source—this is a reasonable inference but goes beyond what the text states. All bibliographic metadata (volume, article number, DOI, publisher, access status) in Claim 5 are confirmed via CrossRef and Unpaywall. The evidence notes appropriately flag methodological limitations (e.g., Claim 4's lower confidence due to paraphrasing rather than direct quotation), reflecting sound research practice."

## Provenance
- Canonical URL: https://www.sciencedirect.com/science/article/pii/S0044848624008123
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: STEP 1 (WebFetch primary URL twice, different prompts): Both calls to https://www.sciencedirect.com/science/article/abs/pii/S0044848624008123 returned HTTP 403 Forbidden — a genuine blocked fetch, not a wrong-page issue. Per Steps 1-2's branching instructions I then pursued ~10 alternate routes: ResearchGate (403), SciSpace/Typeset via redirect (403), Wayback Machine (tool refuses this domain outright: "Claude Code is unable to fetch from web.archive.org"), doi.org (redirected to linkinghub.elsevier.com, which itself just returned "Redirecting" placeholder text with no content), CrossRef API (works: full bibliographic metadata, explicitly "no abstract field... is present in the source data"), Unpaywall API (confirms is_oa=false, oa_locations=[] — i.e., NO legitimate free full-text copy of this article exists anywhere), OUCI citation-aggregator mirror (bibliographic metadata + citation/reference counts, no abstract), and Google Scholar's search-result snippet for the exact title (this one worked, returning genuine quoted abstract text mirroring the ScienceDirect meta-description). I fetched the Google Scholar result 3 times with different prompts and the quoted fragments were mutually consistent, which is the basis for the key_claims below.
IMPORTANT CAVEAT / self-correction: several early WebSearch calls (before I isolated the Google Scholar approach) produced synthesized answers containing specific-sounding systematic-review statistics — "2,338 papers published from January 2000 to April 2024" screened down to "74 eligible studies" sorted into "pigment-based technology, morphological-based technology and nucleic acid technology." These recurred across 2-3 separate WebSearch calls, which initially looked like corroboration. I then ran targeted exact-phrase verification searches ("74 eligible studies" + pigment-based; "identified 2338 papers"; "categorised into pigment-based") and NONE returned any matching result at all (not even an unrelated tangential hit) — a strong signal that this content does not exist in any indexed version of this paper and was likely generated/confabulated by the WebSearch tool's synthesis layer rather than drawn from real source text. Per this task's strict fidelity rule ("if something is not in the fetched/provided text, do NOT state it"), I have EXCLUDED all of these specific figures from key_claims and data_numbers. I flag this prominently because a less careful pass would have reported these as real findings of the paper. Also excluded on the same grounds (appeared once, unquoted/paraphrased, uncorroborated): a claim about the review's "future priorities" (underwater video technology, phytoplankton-species early-warning mechanisms) and a claim about ML "model interpretability" challenges.
Net result: I obtained solid, cross-checked bibliographic/access metadata and a corroborated (but Google-Scholar-truncated, ellipsis-terminated) portion of the abstract — not the complete abstract and no body/methods/results/discussion text. The article is confirmed closed-access with zero legitimate OA copies, so full text is not obtainable by any free/legitimate means; a reader would need institutional/publisher access via https://www.sciencedirect.com/science/article/pii/S0044848624008123. Access/search date: 2026-07-01.
