---
key: ACAD-083
title: Relating spectral shape to cyanobacterial blooms in the Laurentian Great Lakes
authors_or_org: T.T. Wynne (I.M. Systems Group Inc.), R.P. Stumpf, M.C. Tomlinson, R.A. Warner (all NOAA Center for Coastal Monitoring and Assessment), P.A. Tester (NOAA Center for Coastal Fisheries and Habitat Research), J. Dyble, G.L. Fahnenstiel (both NOAA Great Lakes Environmental Research Laboratory)
year: 2008
url: Started from the given ResearchGate URL (blocked, HTTP 403, in 3 different URL forms including a direct author-hosted PDF link). WebSearch identified the publisher/DOI page https://doi.org/10.1080/01431160802007640 (redirects to https://www.tandfonline.com/doi/full/10.1080/01431160802007640) as the canonical version, but that too returned HTTP 403 in /full, /abs, and /pdf forms, as did dl.acm.org, cabidigitallibrary.org, ingentaconnect.com, base-search.net, and repository.library.noaa.gov. Actual text ultimately extracted from: (1) Google Scholar's indexed abstract snippet (scholar.google.com/scholar?q=...), fetched twice independently with consistent wording, and (2) Crossref's metadata API (api.crossref.org/works/10.1080/01431160802007640), cross-checked against GLERL's institutional publication list (glerl.noaa.gov/pubs/sixmo/2008fy.html), Pascal-Francis (CNRS), and CiNii Research bibliographic records.
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal short communication (International Journal of Remote Sensing)
categories: [remote-sensing]
relevance: High
full_text_access: abstract
fetch_status: partial
review_severity: notes
review_overall: pass
---

# Relating spectral shape to cyanobacterial blooms in the Laurentian Great Lakes

> Note: provisional URL was resolved to a primary source. Original: https://www.researchgate.net/publication/248977952_Relating_spectral_shape_to_cyanobacterial_bloom_in_the_Laurentian_Great_Lakes

**What it is.** A short 2008 journal communication (International Journal of Remote Sensing, 8 published pages) by NOAA/GLERL-affiliated scientists introducing a MERIS-satellite-derived "spectral shape" metric centered at the 681 nm reflectance band, used to distinguish cyanobacteria-dominated algal blooms from blooms of other phytoplankton in the Laurentian Great Lakes. It is a foundational, heavily-cited precursor to the satellite Cyanobacterial Index approach later used operationally (e.g., in EPA CyAN-type products), though this session could only confirm its abstract, not its full methods/results.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** A change in MERIS-satellite-derived spectral shape at the 681 nm reflectance band is used to distinguish cyanobacteria-dominated blooms from blooms of other (non-cyanobacterial) phytoplankton in the Great Lakes.
  - *evidence:* Stated as the paper's central method/finding; recovered as the opening abstract sentence via Google Scholar's indexed snippet, worded identically across two independent WebFetch calls. (Abstract (as indexed by Google Scholar for IJRS 29(12):3665-3672))
  - *quote:* "A change in the spectral shape at 681 nm is used to distinguish blooms of cyanobacteria from blooms of other phytoplankton via MERIS satellite sensor imagery."
- **[✓ verified]** The proposed mechanism: during large cyanobacterial blooms the 681 nm spectral-shape value flips from positive to negative, because light scattering associated with cyanobacteria overwhelms the chlorophyll fluorescence signal that otherwise produces a positive shape value in other phytoplankton.
  - *evidence:* Direct mechanistic statement from the abstract; identical wording recovered in both independent Google Scholar fetches (one of which itself rendered it as a quoted fragment). (Abstract (as indexed by Google Scholar for IJRS 29(12):3665-3672))
  - *quote:* "During large cyanobacterial blooms, the spectral shape around 681 nm is not a positive quantity as scattering due to cyanobacteria overwhelms the fluorescence signal, thus creating a negative spectral shape."
- **[⚠ partial]** This is a short (8-page) communication by a 7-author NOAA-affiliated team, published in International Journal of Remote Sensing, volume 29, issue 12, pages 3665-3672 (2008), DOI 10.1080/01431160802007640.
  - *evidence:* Bibliographic/header metadata cross-confirmed identically by Crossref's DOI registry, GLERL's own institutional publication list, and the Pascal-Francis (CNRS) bibliographic database. (Journal article header / DOI metadata record)
  - *quote:* "Volume: 29 | Issue: 12 | Pages: 3665-3672"
  - *reviewer:* One author (T. T. Wynne) is explicitly affiliated with I.M. Systems Group Inc., not NOAA; only 6 of 7 authors are directly NOAA-affiliated. The claim of a 'NOAA-affiliated team' technically overstates formal NOAA affiliation.
- **[⚠ partial]** The paper is a highly-cited, foundational reference in satellite cyanoHAB spectral detection.
  - *evidence:* Citation counts pulled directly from Crossref's API field and Google Scholar's rendered 'Cited by' figure at time of fetch; these are index-side counts that will drift over time and differ by index coverage, not a claim made by the paper itself. (Crossref API record; Google Scholar search-result metadata)
  - *quote:* "Citation Count: 258 (is-referenced-by-count)"
  - *reviewer:* 'Highly-cited' is supported by citation data (258–387 depending on index), but 'foundational reference' is not explicitly stated in the source text; it is inferred from citation count and methodological novelty.

## Data / numbers
- 681 nm — MERIS band at which the 'spectral shape' index is centered (per abstract)
- Volume 29, Issue 12, pages 3665-3672 (2008) = 8 published pages (Crossref; Pascal-Francis lists issue as "11-12", a minor discrepancy between secondary bibliographic databases)
- DOI: 10.1080/01431160802007640
- ISSN 0143-1161 (print); 1366-5901 (electronic) (Crossref)
- Published online 16 May 2008; print 15 June 2008 (Crossref)
- 258 citing works per Crossref 'is-referenced-by-count' (as fetched)
- 387 citing works per Google Scholar 'Cited by' count (as fetched)
- Reference count in paper: 14 (Crossref)

## Methods
Per the recovered abstract only: a "spectral shape" quantity computed from MERIS satellite ocean-color reflectance at the band centered on 681 nm is used as a discriminating signal for cyanobacteria-dominated vs. other-phytoplankton-dominated blooms; the authors attribute a negative shift in this quantity during large cyanobacterial blooms to light scattering by cyanobacteria overwhelming the chlorophyll fluorescence peak. No further methodological detail (exact formula, flanking wavelengths, atmospheric correction, validation/ground-truth data, statistics, or study time period) could be confirmed from primary text in this session because full text was inaccessible (see fetch_notes). Caution for reuse: numerous secondary/citing sources encountered during search describe this lineage of work using a 3-band second-derivative-style computation (MERIS bands near 665, 681 and 709 nm) and a later-named "Cyanobacterial Index" (CI = −SS(681)); those specifics are NOT confirmed here against this paper's own full text, and per the chronology (a 2002-2011 data range and a 4-band 620/665/681/709 nm genus-separation extension were both mentioned in search results) likely belong to subsequent papers by an overlapping author group, not to this 2008 short communication. They are flagged, not asserted as this source's content.

## Stated limitations
Not recoverable from the material obtained in this session. Only a 2-sentence abstract fragment was accessible (via Google Scholar's index of the paper); the paper's own Methods, Results, Discussion and any stated caveats live in the full text, which returned HTTP 403 at every host attempted (Taylor & Francis in three URL forms, ResearchGate in three URL forms including a direct author-hosted PDF, CABI, Ingenta, ACM, BASE, and the NOAA repository). This absence should be read as "limitations section unreachable," not as "the paper has no limitations."

## Tensions with other findings
This is a research-process caveat rather than a scientific finding of the paper itself: several WebSearch results during this session attributed to "Wynne et al. 2008" specific details — a formally named "Cyanobacterial Index" (CI = −SS(681)), a 4-band (620/665/681/709 nm) extension used to spectrally separate the cyanobacterial genera Aphanizomenon and Microcystis, and a Lake Erie MERIS time series spanning 2002-2011 — that are chronologically or substantively inconsistent with an 8-page 2008 communication (e.g., a 2002-2011 range extends 3 years past this paper's publication). These almost certainly belong to later papers by an overlapping NOAA/GLERL author group (e.g., a 2010-era Cyanobacterial Index evaluation paper and later MODIS/MERIS comparison work) and were deliberately excluded from key_claims/data_numbers above. Any literature-review synthesis that cites "Wynne 2008" for the formal CI algorithm, the phycocyanin/genus-separation capability, or a multi-year Lake Erie dataset should verify those specific claims against the actual 2008 full text or the correct sequel paper, not assume this dossier's confirmation covers them.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Citation counts differ significantly between indexes: Google Scholar reports 387; Crossref API reports 258. This discrepancy affects quantification of 'highly-cited' and reflects different index coverage and update timing.
- **Reviewer notes:** All bibliographic facts check out precisely against Crossref metadata and Google Scholar records. The two partial claims are defensible: Wynne's contractor affiliation is minor given 6/7 are NOAA (and contractor teams are often considered affiliated with host agencies), and 'foundational' is a reasonable characterization of a 258+ citation paper introducing a novel method now widely adopted—but neither term is explicit in the source. No hallucinated numbers or egregious overclaims; the summary is substantially accurate."

## Provenance
- Canonical URL: Started from the given ResearchGate URL (blocked, HTTP 403, in 3 different URL forms including a direct author-hosted PDF link). WebSearch identified the publisher/DOI page https://doi.org/10.1080/01431160802007640 (redirects to https://www.tandfonline.com/doi/full/10.1080/01431160802007640) as the canonical version, but that too returned HTTP 403 in /full, /abs, and /pdf forms, as did dl.acm.org, cabidigitallibrary.org, ingentaconnect.com, base-search.net, and repository.library.noaa.gov. Actual text ultimately extracted from: (1) Google Scholar's indexed abstract snippet (scholar.google.com/scholar?q=...), fetched twice independently with consistent wording, and (2) Crossref's metadata API (api.crossref.org/works/10.1080/01431160802007640), cross-checked against GLERL's institutional publication list (glerl.noaa.gov/pubs/sixmo/2008fy.html), Pascal-Francis (CNRS), and CiNii Research bibliographic records.
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: partial
- Fetch notes: HIGH-relevance source per the task, so I made an extensive (~10 WebFetch + ~12 WebSearch) effort across every plausible host before concluding abstract-only access. Every full-text host attempted (Taylor & Francis in 3 URL forms, ResearchGate in 3 URL forms, CABI, Ingenta, ACM, BASE, NOAA repository discover page) returned HTTP 403 — a hard access block, not a rendering/parsing failure, so retrying the same URLs would not help. Metadata-only sources (Crossref, GLERL, Pascal-Francis, CiNii) all independently confirmed identical bibliographic facts (7 authors + affiliations, journal, vol 29(12):3665-3672, 2008, DOI), which gives high confidence in the paper's identity even though its body text is inaccessible here. The only actual content text obtained was a 2-sentence abstract fragment, recovered consistently across two independent Google Scholar fetches — I treat this as a faithful (if partial) reproduction of the paper's own abstract, not a WebSearch paraphrase, since it was returned verbatim/near-verbatim by the fetch tool from a rendered results page both times. I deliberately did NOT use the many WebSearch-tool syntheses that described a 620/665/681/709 nm four-band phycocyanin/genus-separation method, a formally named "CI" index, or a 2002-2011 Lake Erie dataset as claims of THIS paper, because those details are inconsistent with an 8-page 2008 communication and most likely belong to later papers by the same NOAA/GLERL author group — see "tensions" field. No sci-hub or other unauthorized-access route was used, consistent with using only legitimate public web search/fetch.
