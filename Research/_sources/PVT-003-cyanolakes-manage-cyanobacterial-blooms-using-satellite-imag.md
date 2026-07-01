---
key: PVT-003
title: CyanoLakes — Manage Cyanobacterial Blooms Using Satellite Imagery
authors_or_org: CyanoLakes (Pty) Ltd; Founder & CEO Mark Matthews (PhD, bio-optical remote sensing, University of Cape Town, 2014)
year: n.d. (live commercial website; most recent guideline it cites is dated 2023; company traces to a 2015 award and a 2014 PhD)
url: https://www.cyanolakes.com/
access_date: 2026-07-01
tier: PVT
source_type: Commercial product / company website (SaaS product marketing, features, pricing, FAQ, and about pages) — not a peer-reviewed publication
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# CyanoLakes — Manage Cyanobacterial Blooms Using Satellite Imagery

**What it is.** CyanoLakes is a commercial satellite-remote-sensing product (enterprise web app + iOS/Android mobile app) built by Mark Matthews (PhD, bio-optical remote sensing, U. Cape Town, 2014) that maps and forecasts cyanobacterial (harmful algal) blooms in lakes/reservoirs from EU Copernicus and NASA satellite imagery, with no in-situ instruments required, and sells this to water utilities while also pushing public-facing 'weather-app-for-lakes' risk alerts.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** CyanoLakes markets itself as the first product able to distinguish harmful cyanobacteria from non-toxic algae using satellite imagery.
  - *evidence:* Stated as the site's core differentiator on the homepage hero/discovery section and repeated on the Features page as a competitive advantage versus a named competitor/EPA app. (Homepage (hero/discovery section))
  - *quote:* "first product that can distinguish harmful cyanobacteria from algae"
- **[✓ verified]** The service claims to give up to three weeks of advance warning of cyanobacteria blooms compared with routine in-situ (field) monitoring.
  - *evidence:* Repeated verbatim across the homepage and the How-It-Works/Plans page as the core value proposition; no study, sample size, or lake list is given to substantiate the figure on these pages. (Homepage; 'How It Works' (plans-pricing) page)
  - *quote:* "up to three-weeks advance warning of cyanobacteria blooms compared with routine in situ monitoring"
- **[✓ verified]** The underlying satellite data comes from the EU Copernicus Program and NASA (no specific sensor/mission named on the fetched pages).
  - *evidence:* Direct statement of data provenance on the FAQ page; only 'Sentinel-3' is separately name-checked elsewhere on the site as 'a game changer' in blog-style content, without further sensor specification. (FAQ page ('Satellite Imagery Source'))
  - *quote:* "The information provided via the Application is derived exclusively from satellite imagery. We use multiple sources of satellite data from the EU Copernicus Program and NASA."
- **[✓ verified]** Premium imagery is delivered at 10 m spatial resolution (high-resolution tier); a medium-resolution tier is 300 m.
  - *evidence:* 10 m confirmed on both the FAQ and Features pages; 300 m medium-resolution figure given on the Plans-Pricing/How-It-Works page listing both tiers side by side. (FAQ page; Plans-Pricing ('How It Works') page; Features page)
  - *quote:* "a 10 m pixel size (spatial resolution)"
- **[✓ verified]** Update cadence is generally 5-6 days/week, while the high-definition imagery product updates 2-3 times/week; both are reduced by cloud, ice, or snow cover and vary seasonally.
  - *evidence:* Two distinct cadence figures given for what appear to be two different imagery products/tiers on the same FAQ page; both explicitly caveated by weather/season. (FAQ page ('Update Frequency'))
  - *quote:* "the information is updated 5 to 6 days per week, however cloud, ice or snow cover may result in fewer updates"
- **[✓ verified]** The per-waterbody cyanobacteria risk level is computed from the median (50th percentile) chlorophyll-a of pixels classified as cyanobacteria, following WHO (2021) recreational-water guidance, and only counts if cyanobacterial bloom coverage reaches a minimum area threshold (10% of the waterbody for larger lakes, 50% for small lakes).
  - *evidence:* This is the site's own stated calculation method for its headline 'risk level' output, directly tying the product's algorithm to a named external guideline (WHO 2021) and giving explicit area-coverage gating thresholds. (FAQ page ('Cyanobacteria Risk Level Determination'))
  - *quote:* "The risk level is calculated using the median (50th percentile) value of chlorophyll-a for pixels identified as cyanobacteria. In addition, coverage by cyanobacterial blooms must be at least 10% of the area for larger lakes, and 50% of the area for small lakes."
- **[✓ verified]** The site tabulates specific WHO (2021), Australian NHMRC (2008), California Water Board (2023), and US EPA (2019) numeric thresholds for chlorophyll-a, cyanobacterial biovolume, cell counts, and microcystin that it uses to classify risk.
  - *evidence:* Full guideline table given verbatim on the FAQ page; used as the basis for the app's four-tier risk classification (Low/Medium/High/Very High). (FAQ page ('Water Quality Thresholds & Guidelines'))
  - *quote:* "Alert Level 2: 24 ug/L chlorophyll-a or 8 mm3/L biovolume (Microcystin ~ 10 ug/L)"
- **[✓ verified]** The site states a fixed conversion of 1 µg/L chlorophyll-a to approximately 2,000 cyanobacteria cells/mL, attributed to WHO, and a companion conversion of 0.4 µg/L microcystin per µg/L chlorophyll-a.
  - *evidence:* Two explicit unit-conversion factors given on the FAQ page as the basis for the app's derived 'cell count' and 'potential microcystin' outputs; both attributed to WHO recommendation rather than the vendor's own calibration. (FAQ page ('Conversion Formulas'))
  - *quote:* "the World Health Organisation recommended conversion of 1 ug/l chl-a to 2,000 cell/ml"
- **[✓ verified]** The vendor states its high-risk bloom forecasts are 'up to 80% accurate' at a 1-week lead time and drop to '70% accurate' at a 2-week lead time.
  - *evidence:* Stated as a flat accuracy percentage with no defined metric (e.g., not specified whether this is classification accuracy, precision, or recall), no sample size, no study period, and no citation given on the fetched FAQ page. (FAQ page ('Forecast Accuracy & Availability'))
  - *quote:* "Forecasts for high-risk blooms are up to 80% accurate 1-week in advance, but only 70% accurate 2-weeks in advance."
- **[✓ verified]** A separate '3 weeks' figure is used for a different purpose: new lakes can take up to three weeks of processing-queue time before forecasts become available at all.
  - *evidence:* This is an onboarding/operational latency caveat, distinct from the marketing '3-week early warning' claim above, and appears directly beneath the accuracy figures on the FAQ page — the two '3 week' claims should not be conflated. (FAQ page ('Forecast Accuracy & Availability'))
  - *quote:* "It may take up to 3 weeks for forecasts to become available for your lakes, depending on the length of processing queues."
- **[✓ verified]** The product explicitly disclaims coverage of any water-quality hazard other than cyanobacteria/algal blooms (no pathogens, heavy metals, or chemical contaminants), so its recreational-safety guidance is stated to be non-comprehensive.
  - *evidence:* A direct, capitalized self-imposed scope limitation on the FAQ page, paired with a blanket instruction to defer to local-authority warnings. (FAQ page (disclaimer section))
  - *quote:* "This Application provides information ONLY related to cyanobacteria and algal blooms. It does not provide any information related to other important water quality indicators such as microbiological organisms (other bacteria and viruses), heavy metals, pathogens and diseases, inorganic and organic chemicals, or other contaminants. Therefore, the recreational recommendations provided by the App are NOT comprehensive."
- **[✓ verified]** The 'Low Risk' classification does not guarantee cyanobacteria are absent, because cyanobacteria can be present below the satellite's detection limit.
  - *evidence:* Self-stated detection-limit caveat embedded directly in the definition of the app's own lowest risk tier. (FAQ page (risk-level definitions))
  - *quote:* "since cyanobacteria can exist below the detection limit of the satellite, it does not guarantee that cyanobacteria are not present"
- **[✓ verified]** CyanoLakes received R1 million (South African Rand) from the South African Water Research Commission's Water Technologies Demonstration Programme (WADER) to pilot the technology with three operational water utilities: City of Cape Town, Rand Water, and Umgeni Water.
  - *evidence:* Funding source, amount, and named pilot partners given directly on the WADER page; each pilot is specified as a 12-month subscription covering up to 5 waterbodies with a validation report comparing satellite output to the utility's own measurements. (WADER page)
  - *quote:* "R1m from the South African Water Research Commission's Water Technologies Demonstration Programme (WADER)"
- **[✓ verified]** The company states its underlying detection algorithms are open, peer-reviewed, and cited more than 500 times on Google Scholar.
  - *evidence:* Self-reported citation count used as a credibility signal on the Features page; the specific underlying papers (e.g., Matthews et al. 2020; Matthews & Odermatt 2015; Matthews 2012) are linked elsewhere on the site but were not themselves fetched or verified for this dossier entry. (Features page ('Competitive Advantages'))
  - *quote:* "cited 500+ times (Google Scholar)"
- **[✓ verified]** CyanoLakes won the Copernicus Masters Ideas Challenge (a global Earth-observation business-idea competition), which the homepage's 'Approvals' section dates to 2015.
  - *evidence:* Award confirmed in full sentence form on the About page; the specific year 2015 came from the Approvals/badge section of the homepage rather than from a quoted sentence, so the year attribution is slightly less certain than the award claim itself. (About page; Homepage ('Approved By' section))
  - *quote:* "CyanoLakes is the winner of the Copernicus Masters Ideas Challenge, a worldwide competition for novel earth observation business ideas."
- **[✓ verified]** The platform guarantees 99% uptime and offers unlimited waterbodies per subscription (priced by waterbody count), with a standard 6 months of included historical data and up to 6 years purchasable, plus API data download.
  - *evidence:* Uptime figure is a direct quote from the Features page; the historical-data figures (6 months standard / up to 6 years) were rendered by the fetch as unquoted bullet points on the Plans-Pricing page, so their exact on-page wording is less certain even though the numbers themselves are clearly stated. (Features page; Plans-Pricing ('How It Works') page)
  - *quote:* "Guaranteed 99% uptime, support and training"

## Data / numbers
- 10 m — pixel size of the premium/high-resolution satellite imagery product (FAQ; Features; Plans-Pricing pages)
- 300 m — pixel size of the medium-resolution imagery tier (Plans-Pricing page)
- 5-6 days/week — general data update frequency, reduced by cloud/ice/snow cover (FAQ page)
- 2-3 times/week — update frequency specifically for the 'high definition' imagery product (FAQ page)
- up to 3 weeks — (a) marketed 'advance warning' lead time vs. routine in-situ monitoring (homepage/How-It-Works), and (b) separately, the onboarding delay before forecasts become available for a new lake due to processing queues (FAQ) — two distinct uses of the same figure
- 80% — stated forecast accuracy for high-risk blooms at 1-week lead time (FAQ page; no metric definition, n, or study period given)
- 70% — stated forecast accuracy for high-risk blooms at 2-week lead time (FAQ page; same caveats as above)
- 1-1000 µg/L — stated measurement range of the chlorophyll-a satellite data product (FAQ page)
- WHO (2021) recreational-water thresholds: Vigilance 3 µg/L chl-a or 1 mm3/L biovolume (microcystin ~1.2 µg/L); Alert 1: 12 µg/L or 3 mm3/L (microcystin ~4.8 µg/L); Alert 2: 24 µg/L or 8 mm3/L (microcystin ~10 µg/L) (FAQ page)
- Australian NHMRC (2008) thresholds: Green 0.04 mm3/L or 500 cells/mL (chl-a ~0.25 µg/L); Amber 0.4 mm3/L or 5,000 cells/mL (chl-a ~2.5 µg/L); Red 4 mm3/L or 50,000 cells/mL (chl-a ~25 µg/L, microcystin ~10 µg/L) (FAQ page)
- California Water Board (2023) thresholds: Tier 1 <0.8 µg/L microcystin or <4000 cells/mL toxin producers (chl-a ~2 µg/L); Tier 2 >6 µg/L microcystin (chl-a ~15 µg/L); Tier 3 >20 µg/L microcystin (chl-a ~50 µg/L) (FAQ page)
- US EPA (2019) recreational guideline: microcystin ≥ 8 µg/L (chl-a ~20 µg/L) (FAQ page)
- Conversion factors (attributed by the site to WHO): 1 µg/L chlorophyll-a ≈ 2,000 cyanobacteria cells/mL; 0.4 µg/L microcystin per µg/L chlorophyll-a (FAQ page)
- ≥10% of waterbody area (large lakes) / ≥50% (small lakes) — minimum cyanobacterial bloom coverage required before the risk-level calculation applies (FAQ page)
- 99% — guaranteed platform uptime (Features page)
- R1,000,000 (R1m, South African Rand) — WADER grant amount from the Water Research Commission (WADER page)
- 12 months — duration of each WADER utility pilot subscription (WADER page)
- up to 5 — waterbodies covered per WADER pilot subscription (WADER page)
- 6 months (standard) / up to 6 years (purchasable) — historical satellite data availability (Plans-Pricing page; wording not fully verbatim, see key_claims caveat)
- 500+ — Google Scholar citation count claimed for the underlying algorithms (Features page)
- 2015 — year cited in the homepage 'Approved By' section for the Copernicus Masters Ideas Challenge win (Homepage; About page confirms the award without repeating the year in the same sentence)
- 2014 — year founder Mark Matthews completed his PhD in bio-optical remote sensing at the University of Cape Town (About page)

## Methods
CyanoLakes is a proprietary commercial SaaS product, not a peer-reviewed study. Per the FAQ page, it ingests 'multiple sources of satellite data from the EU Copernicus Program and NASA' (no specific sensor named on the fetched pages, though 'Sentinel-3' is separately mentioned once in passing) and generates chlorophyll-a and true-colour maps at two resolution tiers (10 m high-resolution 'premium'; 300 m medium-resolution), updated 5-6 days/week generally and 2-3 times/week for the high-definition product, subject to cloud/ice/snow gaps. Water pixels are classified as cyanobacteria vs. other algae (the site's central differentiator), and a per-waterbody 'risk level' is derived from the median (50th-percentile) chlorophyll-a of cyanobacteria-classified pixels, gated by a minimum bloom-coverage-area rule (≥10% for large lakes, ≥50% for small lakes), and mapped onto WHO (2021), Australian NHMRC (2008), California Water Board (2023), and US EPA (2019) guideline tiers, all reproduced with numeric thresholds on the FAQ page. Chlorophyll-a is converted to cyanobacteria cell counts and to a 'potential microcystin' estimate using two WHO-attributed conversion factors (1 µg/L chl-a ≈ 2,000 cells/mL; 0.4 µg/L microcystin per µg/L chl-a) rather than site-specific calibration. A short-term forecast product claims 'up to 80%' accuracy at 1-week lead and '70%' at 2-week lead, with no metric definition, validation sample, or study period stated on the fetched pages. The site says its detection algorithm is grounded in 'peer-review science' 'cited 500+ times (Google Scholar)' and links to named publications (Matthews et al. 2020; Matthews & Odermatt 2015; Matthews 2012; a South African Journal of Science article) that were identified via search but not themselves fetched or reviewed for this entry. Validation against customer-held in-situ data is offered via an optional 'My-Data'/'Validation' tool and, for WADER pilot partners, 'a validation report comparing the piloter's measurements with those from satellite' — but no aggregate accuracy statistic (R², RMSE, bias, n) for this validation is given anywhere on the fetched pages.

## Stated limitations
The site itself states: (1) update frequency and imagery availability are degraded by cloud, ice, and snow cover and vary seasonally; (2) cyanobacteria can exist below the satellite's detection limit, so a 'Low Risk' reading does not guarantee absence; (3) the product covers ONLY cyanobacteria/algal blooms and explicitly does not address other water-quality hazards (other bacteria/viruses, heavy metals, pathogens, organic/inorganic chemicals), making its recreational-safety guidance 'NOT comprehensive'; (4) conditions may have changed since the satellite's last overpass, so field observations can legitimately disagree with the app; (5) imagery may be 'blacked or whited out' due to cloud cover or coverage gaps; (6) the delivered imagery is at 'a slightly lower spatial resolution than Google,' a stated trade-off the vendor frames as improving derived-product accuracy; (7) forecast accuracy explicitly degrades with lead time (80% at 1 week vs. 70% at 2 weeks) and new-lake forecasts can take up to 3 weeks to become available due to processing queues; (8) users are told to 'always follow warnings issued by your local authorities,' i.e., the tool is not positioned as a substitute for official monitoring; (9) no USD/regional pricing figures, and no aggregate count of lakes/waterbodies monitored globally, are disclosed on the fetched pages ('Pricing differs regionally – US pricing shown' with no amount given).

## Tensions with other findings
Two internal readings of the same '3 weeks' figure should not be conflated: a marketing claim of 3-weeks earlier warning than in-situ sampling versus a separate operational caveat that new-lake forecasts can take up to 3 weeks to activate due to processing queues. More substantively, the headline claims most useful to a literature review — the '3-week early warning' value proposition and the '80% / 70%' forecast-accuracy figures — are presented on marketing/FAQ pages with no visible methodology, validation sample, study period, or comparison baseline; that puts them in tension with this review's bar that a finding needs a stated baseline and uncertainty, and they should be treated as vendor self-report rather than a validated result unless corroborated by the peer-reviewed publications the site links to (Matthews et al. 2020; Matthews & Odermatt 2015; Matthews 2012), which were not fetched for this entry. Separately, the product's stated 10 m 'premium' resolution and near-daily (5-6 days/week) cadence are considerably finer/more frequent than the ~300 m, weekly cadence typically associated with the public Sentinel-3-based cyanobacteria products (e.g., EPA CyAN) referenced elsewhere in this literature review; the FAQ attributes the 10 m product only to unnamed 'EU Copernicus... and NASA' sources without naming a specific sensor, so the two product classes (a free ~300 m/weekly public indicator vs. this vendor's paid 10 m/near-daily product) are not directly comparable from the text fetched here. Finally, the site's explicit, self-imposed scope limit (cyanobacteria/algal blooms only, not pathogens/metals/chemicals) is a useful boundary condition to keep in mind whenever this vendor's 'risk level' output is compared against broader water-safety or regulatory findings from other sources in the review.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All 16 claims are directly supported by explicit statements in the source text. No hallucinated numbers detected. No significant caveats from the source text were omitted from the claims. Update cadences (5-6 days/week vs. 2-3 times/week), spatial resolutions (300 m vs. 10 m), risk thresholds, conversion factors, forecast accuracy figures, funding amount, award year, and platform features all verify verbatim or near-verbatim against the fetched pages. Where the source text contains caveats (weather/seasonal effects on update frequency, detection-limit caveats on Low Risk, processing-queue time), they are appropriately incorporated into the claim language or flagged in the evidence notes. The claims accurately reflect what CyanoLakes states on its public-facing pages without overstatement or invention."

## Provenance
- Canonical URL: https://www.cyanolakes.com/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the primary URL (https://www.cyanolakes.com/) twice with different extraction prompts as required for a High-relevance source, then followed same-domain internal links to fill gaps the homepage alone did not cover: Features (/product-features/), 'How It Works'/Plans-Pricing (/plans-pricing/ — the actual URL for the nav item labeled 'How It Works', found via WebSearch after a guessed URL /how-it-works returned HTTP 404), WADER (/wader/), FAQs (/faqs/), and About (/about/). The FAQ page was the single richest source of numeric thresholds, conversion factors, and forecast-accuracy figures. Two WebSearch calls were used only to locate correct subpage URLs and confirm founder/about-page content; both searches' result snippets are noted as such in source_extract and were corroborated by a direct WebFetch of /about/. Publications linked from the site (Matthews et al. 2020; Matthews & Odermatt 2015; Matthews 2012; an EJC170780.pdf South African Journal of Science article) were identified by URL but not fetched or read, so no claims from those underlying peer-reviewed papers are included here — if the review wants the primary scientific validation of CyanoLakes' algorithm, those should be logged as separate source keys. No USD/regional pricing figures and no aggregate 'number of lakes monitored globally' figure were found on any fetched page.
