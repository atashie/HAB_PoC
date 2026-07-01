---
key: ACAD-088
title: Satellite and in situ cyanobacteria monitoring: Understanding the impact of monitoring frequency on management decisions
authors_or_org: Natalie Reynolds; Blake A. Schaeffer; Lucie Guertault; Natalie G. Nelson
year: 2023
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10807294/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article — Journal of Hydrology (Amsterdam), Elsevier, 2023; DOI 10.1016/j.jhydrol.2023.129278; PMID 38273893; full text retrieved via PubMed Central (PMC10807294)
categories: [remote-sensing]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: notes
review_overall: flag
---

# Satellite and in situ cyanobacteria monitoring: Understanding the impact of monitoring frequency on management decisions

**What it is.** A peer-reviewed case study (Lake Okeechobee and the St. Lucie Estuary, FL, USA; May 2016-April 2021 / Water Years 2017-2021) that directly compares in-situ chlorophyll-a monitoring against Sentinel-3 OLCI/CyAN satellite-derived cyanobacteria bloom detection to (1) quantify how monitoring frequency/spatial resolution changes measured bloom frequencies and (2) test whether satellite imagery near a discharge structure can flag conditions associated with downstream cyanoHAB export relevant to reservoir-release management decisions.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Agreement between in-situ and satellite bloom-frequency rankings for the whole lake is strong and statistically significant at monthly resolution, but essentially absent at annual resolution.
  - *evidence:* Kendall's tau-b correlation between in-situ and remotely sensed bloom-frequency rankings was 0.85 (p=0.0002) at monthly scale lake-wide, versus tau=0 (p=1) at annual scale lake-wide. (Results - frequency comparisons (in situ vs. remotely sensed))
  - *quote:* "Strong agreement was observed in frequency rankings between the in situ and remotely sensed data in capturing intra-annual variability in bloom frequencies across Lake Okeechobee (Kendall's tau = 0.85, p-value = 0.0002)... No alignment was observed when evaluating inter-annual variation (Kendall's tau = 0, p-value = 1)."
- **[✓ verified]** In Water Year 2019, in-situ sampling recorded a far lower lake-wide bloom frequency than the satellite data for the same year, the largest such disparity of the five study years.
  - *evidence:* In-situ bloom frequency for WY2019 was 1.7% versus a satellite-derived total potential bloom frequency of 12.7% lake-wide. (Results - annual frequency comparison)
  - *quote:* "The least similar frequencies across the two datasets occurred in WY 2019, where the in situ bloom frequency was 1.7 % and the satellite-derived total potential bloom frequency was 12.7 % across Lake Okeechobee."
- **[✓ verified]** At quadrant scale, in-situ sampling recorded zero blooms in periods where satellite imagery detected blooms in over 10% of observations.
  - *evidence:* In-situ bloom frequency was 0% in the northeast and southwest quadrants while satellite total-potential-bloom frequency was 11.8% (NE) and 14.5% (SW) for the same comparison (text follows directly from the WY2019 statistic, so likely refers to the same year, though the sentence itself does not repeat 'WY2019'). (Results - frequency comparisons by quadrant)
  - *quote:* "The greatest differences occurred in the northeast and southwest quadrants, where the in situ bloom frequency was 0 % while the respective total potential bloom frequencies from the satellite imagery were 11.8 % and 14.5 %."
- **[✓ verified]** Aggregated across all study years, July shows the single largest monthly disparity between the two monitoring streams.
  - *evidence:* 5-year-aggregated satellite bloom frequency for July was 31.5% versus 10% in situ, a 21.5-percentage-point difference, the largest monthly gap reported. (Results - monthly frequency comparison)
  - *quote:* "The greatest difference in frequencies occurred in the aggregated data for July, where the satellite-derived total potential bloom frequency was 31.5 % and the in situ bloom frequency was 10 %, yielding a difference of 21.5 %."
- **[✓ verified]** Satellite imagery revealed high bloom frequency near the Lake Okeechobee-to-St. Lucie Estuary discharge inlet coinciding with high discharge only in the two years that produced downstream states of emergency — a pattern the in-situ data alone did not show.
  - *evidence:* A discharge 'Area of Influence' (AOI, max 4.8 km2, radius 1502 m) around the S-308 structure showed high bloom frequency coincident with high S-308 discharge only in WY2017 and WY2019 (the state-of-emergency years); in all other years flow was low/negative during frequent-bloom periods in the AOI. (Results/Discussion - Area of Influence and discharge analysis)
  - *quote:* "Remotely sensed observations revealed that cyanoHABs were highly frequent near the inlet to the canal connecting Lake Okeechobee to the St. Lucie Estuary in state-of-emergency years, a pattern not evident from in situ data alone... the only two years when these high frequencies coincided with high discharges from S-308 were WY 2017 and WY 2019, when the states of emergency occurred. In all other years, flow at S-308 was either very low or negative when the AOI experienced frequent or highly frequent cyanoHABs."
- **[✓ verified]** Matchup error between in-situ and satellite-derived chlorophyll-a in Lake Okeechobee is substantial, and larger than in a national comparison dataset over the full concentration range.
  - *evidence:* 78 in-situ/satellite chlorophyll-a matchups (16 hypereutrophic) yielded log-scale MAE (MAElog) of 2.2 (~+/-120% error) and bias (biaslog) of 1.63 (+63%) for the full range in Lake Okeechobee, versus MAElog 1.8 (~+/-80%) and biaslog 1.33 (+33%) nationally; within the hypereutrophic range (30-90 ug/L) errors were smaller but still sizeable (Lake Okeechobee MAElog 1.8/biaslog 0.55; national MAElog 1.3/biaslog 1.16). (Results - validation / error analysis)
  - *quote:* "78 matchups of in situ and remotely sensed chlorophyll-a observations from Lake Okeechobee, 16 of which had in situ measurements within the hypereutrophic range... [Lake Okeechobee] MAElog: 2.2... biaslog: 1.63... [national] MAElog: 1.8... biaslog: 1.33 (full range); [hypereutrophic range] Lake Okeechobee MAElog: 1.8... biaslog: 0.55... national MAElog: 1.3... biaslog: 1.16."
- **[✓ verified]** Satellite CIcyano values are converted to chlorophyll-a via a published regression and classified into three explicit bloom categories; in-situ classification uses a separate state regulatory threshold.
  - *evidence:* CIcyano-to-chlorophyll-a conversion follows Tomlinson et al. (2016); satellite pixels are classified bloom/possible bloom/no bloom by chlorophyll-a thresholds, while in-situ bloom status uses the Florida DEP 40 ug/L standard. (Methods - satellite and in-situ classification)
  - *quote:* "chla=4050(±271)∗CIcyano+20(±3)... Bloom: '≥52 μg/L'; Possible bloom: '[28, 52) μg/L'; No bloom: '[0, 28) μg/L'... in situ bloom threshold '≥40 μg/L' based on Florida Department of Environmental Protection (FDEP) standard."
- **[⚠ partial]** The authors conclude monthly (not annual) bloom-frequency aggregation is more informative for characterizing historical cyanoHAB patterns because annual aggregation flattens seasonal variability.
  - *evidence:* Stated directly in the conclusions, drawing on the annual-vs-monthly Kendall's tau contrast. (Conclusions)
  - *quote:* "Our examination of cyanoHAB frequencies on multiple spatial and temporal scales indicate that monthly, rather than annual, frequencies are more informative in examining historical cyanoHABs in reservoirs... this disparity indicates that examining annual frequencies may flatten seasonal variation in cyanoHABs and frequencies should rather be considered on finer timescales due to limited in situ sampling."
  - *reviewer:* The claim is well-supported by the source text, but the provided quote is not verbatim. The opening phrase ('Our examination of cyanoHAB frequencies...monthly, rather than annual, frequencies are more informative in examining historical cyanoHABs in reservoirs') does not appear in the source text as written. Only the final portion ('this disparity indicates that examining annual frequencies may flatten seasonal variation...') matches the source.
- **[✓ verified]** The authors caution that in-situ and satellite chlorophyll-a measurements differ structurally (point vs. areal/composite) and both carry error, so a perfect match should not be expected; they also note Sentinel-2's finer spatial resolution cannot substitute for Sentinel-3/CyAN because it cannot detect phycocyanin.
  - *evidence:* Stated in the discussion/limitations regarding matchup interpretation and sensor choice. (Discussion / Limitations)
  - *quote:* "Both in situ and remotely sensed data are subject to error and matchups, therefore, should not be expected to perfectly fit a one-to-one regression... Sentinel-2 offers a finer spatial resolution, it lacks the spectral resolution for detecting phycocyanin fluorescence, so it cannot be used to differentiate cyanobacteria from other chlorophyll-a-containing biomass."
- **[✓ verified]** The authors frame satellite remote sensing as a relatively low-cost complement (not a replacement) to in-situ monitoring that can inform reservoir-release management decisions, e.g. by revealing bloom concentration near a discharge point.
  - *evidence:* Stated in the conclusions/discussion, tied to the AOI/discharge findings and the practical management-decision framing that is the paper's title theme. (Conclusions / Discussion)
  - *quote:* "Although there are sources of error and uncertainty in employing satellite imagery for cyanoHAB monitoring, it serves as a powerful tool for expanding monitoring regimes with relatively low cost to resource managers... satellite imagery could reveal whether cyanoHABs are concentrated near a primary discharge point, resulting in a manager potentially deciding to postpone releasing water until the bloom has dissipated or migrated to another region."

## Data / numbers
- Kendall's tau = 0.85 (p=0.0002) — monthly bloom-frequency ranking agreement, whole lake
- Kendall's tau = 0 (p=1) — annual bloom-frequency ranking agreement, whole lake
- Monthly quadrant tau: NW=0.68 (p=0.003); NE=0.68 (p=0.005); SW=0.33 (p=0.2, ns); SE=0.44 (p=0.1, ns)
- Annual quadrant tau: NW=0 (p=1); NE=-0.11 (p=0.8); SW=0.32 (p=0.5); SE=0.32 (p=0.4)
- WY2019 whole-lake bloom frequency: in situ = 1.7%; satellite total-potential-bloom = 12.7%
- Quadrant bloom frequency: NE in situ = 0% vs satellite = 11.8%; SW in situ = 0% vs satellite = 14.5%
- July (5-yr aggregate): satellite = 31.5%; in situ = 10%; difference = 21.5 percentage points
- Annual bloom frequency (satellite / in situ) by water year: WY2017 8.2%/5.3%; WY2018 3.3%/4.2%; WY2019 12.7%/1.7%; WY2020 9.5%/11.3%; WY2021 8.1%/6.8%
- Maximum discharge 'Area of Influence' (AOI) near S-308 = 4.8 km2, radius = 1,502 m, overlapping 56 Sentinel-3 pixels
- AOI total-potential-bloom-frequency percentiles: 0th=0%, 50th=1.9%, 70th=5.6%, 80th=18.4%, 90th=33.1%, 100th=50.2% (max monthly, vs. 31.5% lake-wide in July)
- 78 in situ-satellite chlorophyll-a matchups total (16 within hypereutrophic range)
- Lake Okeechobee chlorophyll-a matchup range = 3-86 ug/L vs. national comparison dataset range = 0-700 ug/L
- Full-range matchup error: Lake Okeechobee MAElog=2.2 (~+/-120%), biaslog=1.63 (+63%); national MAElog=1.8 (~+/-80%), biaslog=1.33 (+33%)
- Hypereutrophic-range (30-90 ug/L) matchup error: Lake Okeechobee MAElog=1.8 (~+/-80%), biaslog=0.55 (-45%); national MAElog=1.3 (~+/-30%), biaslog=1.16 (+16%)
- Satellite bloom classification thresholds (chlorophyll-a): bloom >=52 ug/L; possible bloom 28-<52 ug/L; no bloom 0-<28 ug/L
- In-situ bloom threshold: >=40 ug/L (Florida DEP standard)
- CIcyano-to-chlorophyll-a conversion: chla = 4050(+/-271) x CIcyano + 20(+/-3) (Tomlinson et al., 2016)
- Sentinel-3 OLCI spatial resolution = 300 m; per-satellite revisit = 2-3 days; near-daily combined revisit with 3A+3B
- 10 in situ chlorophyll-a stations used (selected from 36 active, requiring <=1 month missing data WY2017-2021): 3 NW, 2 NE, 1 SW, 4 SE
- Study period: May 2016-April 2021 (Water Years 2017-2021); Sentinel-3A launched April 2016, Sentinel-3B launched May 2018
- S-308 chlorophyll-a during high discharge, WY2017: June 6 = 74.7 ug/L; June 20 = 27.2 ug/L. WY2019: June 4 = 81.4 ug/L; June 18 = 5.9 ug/L; Aug 13 = 45.8 ug/L; Aug 27 = 20.1 ug/L
- St. Lucie Estuary states of emergency: summer 2016 (WY2017) and summer 2018 (WY2019)
- Funding: NSF Graduate Research Fellowship grant DGE-2137100; USDA NIFA Hatch project 1016068

## Methods
Two parallel bloom-detection streams over Lake Okeechobee/St. Lucie Estuary, FL, WY2017-2021 (May 2016-April 2021): (1) In-situ — surface grab samples (top 0.5 m) from 10 of 36 active SFWMD DBHYDRO chlorophyll-a stations (3 NW/2 NE/1 SW/4 SE quadrant), analyzed by HPLC (Method 447.0, 440 nm), sampled monthly/occasionally twice-monthly; bloom threshold >=40 ug/L (Florida DEP). (2) Satellite — Sentinel-3A (launched Apr 2016) and 3B (launched May 2018) OLCI, 300 m resolution, ~2-3 day revisit per satellite (near-daily combined), processed by NASA OBPG into weekly CyAN composites using the Cyanobacteria Index (CIcyano) algorithm; CIcyano converted to chlorophyll-a via Tomlinson et al. (2016): chla = 4050(+/-271)*CIcyano + 20(+/-3); classified no bloom [0,28) ug/L, possible bloom [28,52) ug/L, bloom >=52 ug/L. Agreement in bloom-frequency rankings tested with Kendall's tau-b (chosen for robustness to ties/small non-normal samples) at annual and monthly (5-yr aggregated) scales, lake-wide and by quadrant. In-situ vs. satellite chlorophyll-a matchup error quantified via log-scale MAE (MAElog) and bias (biaslog) for Lake Okeechobee (n=78 matchups, 16 hypereutrophic) versus a national comparison dataset; national MAElog (1.3, hypereutrophic range) was adopted as the operating uncertainty bound because of its larger sample size. A discharge "Area of Influence" (AOI, up to 4.8 km2/radius 1502 m/56 pixels) around the S-308 structure (USGS gage, 15-min discharge data, 2016-2020) tested whether satellite-observed bloom frequency near the outlet coincided with high discharge in years preceding St. Lucie Estuary states of emergency (2016, 2018). Result: the approach "works" (strong, significant rank agreement; useful spatial signal invisible to point sampling) at monthly resolution lake-wide and in the northern quadrants, and for flagging bloom concentration near the discharge point; it "fails" (no significant agreement) at annual resolution and in the southern quadrants, and matchup error between in-situ and satellite chlorophyll-a remains substantial (MAElog ~1.3-2.2, roughly +/-30% to +/-120%).

## Stated limitations
Authors state: (1) the study period is limited to the post-Sentinel-3-launch era, so earlier extreme-bloom events (e.g., pre-2016) could not be included; (2) the CIcyano-to-chlorophyll-a relationship used (Tomlinson et al. 2016) is Florida-lake-specific — other algorithms/error metrics exist and may be needed for other systems; (3) there is measurable, non-trivial error between in-situ and satellite-derived chlorophyll-a in their own system that must be accounted for when interpreting results, and the two data types "should not be expected to perfectly fit a one-to-one regression" because in-situ grab samples are point/instant measurements while satellite pixels represent areal, time-composited estimates; (4) Sentinel-2, despite finer spatial resolution, lacks the spectral bands to detect phycocyanin fluorescence and so cannot substitute for Sentinel-3/CyAN in distinguishing cyanobacteria from other chlorophyll-a-containing biomass; (5) finer temporal-resolution satellite analysis is constrained by cloud cover, sun glint, land presence, vegetation, and satellite flyover rate; (6) they did not adjust CIcyano classification thresholds for the observed bias, which they flag as a possible source of error; (7) sparse in-situ sampling under-observes short bloom pulses (e.g., grab samples fell during the ~70-75% of time when no bloom was occurring in the southern quadrants during July events).

## Tensions with other findings
This source is a direct methodological caution for any project (including this one) that fuses satellite and in-situ HAB signals: it shows point-based, monthly in-situ sampling can miss most of the blooms a satellite detects in the same period/location (e.g., 0% in situ vs. 11.8-14.5% satellite by quadrant; 1.7% vs. 12.7% lake-wide in WY2019), and that in-situ/satellite bloom-frequency agreement is highly scale-dependent — strong and significant at monthly resolution (tau=0.85, p=0.0002) but statistically absent at annual resolution (tau=0, p=1) — a warning against validating a satellite signal against coarsely aggregated in-situ "ground truth," or vice versa. It also reports sizeable in-situ-vs-satellite chlorophyll-a matchup error even in the best case (national, hypereutrophic-range MAElog=1.3, i.e. ~+/-30%), which argues against treating either stream as an error-free reference. This does not contradict a specific causal HAB-driver claim from other sources; the tension is about measurement/validation methodology (matching resolution, quantifying cross-sensor error, and choosing aggregation scale) rather than about what drives blooms.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Dropped caveats:**
  - Study period limited to time following Sentinel-3 launch in April 2016
  - Classification thresholds were not adjusted for bias when classifying CIcyano images, identified as a possible source of error
  - In-situ grab samples covered only 70-75% of the time when blooms were not occurring in southern quadrants during July events, indicating sampling bias
  - CIcyano-to-chlorophyll-a relationship was specific to Florida lakes; other published algorithms and error metrics exist and could be applied
  - Methods are directly applicable only to freshwater reservoirs resolvable by Sentinel-3 OLCI imagery, limiting generalizability
- **Reviewer notes:** Nine of ten claims are directly supported by the source text with accurate numbers and interpretations. Claim 8 is partially supported: the substantive conclusion about monthly aggregation being more informative is clearly stated in the source, but the provided quote is inaccurate/paraphrased. The opening portion of the quote does not appear verbatim in the source text. No numerical hallucinations detected; all figures trace correctly. Several important methodological caveats are present in the source but not reflected in the claims, most notably that classification thresholds were not bias-adjusted and in-situ sampling has documented gaps that could bias the comparisons."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10807294/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched https://pmc.ncbi.nlm.nih.gov/articles/PMC10807294/ (PMC full-text) twice with WebFetch using two different extraction prompts, per the HIGH-relevance protocol: (1) a general comprehensive extraction (what it is, all findings, every number+units, methods/models/data, limitations, authorship); (2) a targeted extraction of research questions, full methods detail, all numerical results/tables, management-decision discussion, verbatim conclusions/limitations, and funding/COI. Both calls returned full-text content spanning abstract through methods, results (including statistical tables), discussion, conclusions, limitations, and funding/COI statements — no paywall, truncation, or garbled/binary content was encountered, so no WebSearch fallback was needed; url_used = resolved_url = the given primary URL. The two extractions were highly consistent with each other (identical tau/p-values and error metrics), so they were reconciled by union: fetch 1 supplied more narrative quote context, fetch 2 supplied the fuller quadrant-level/per-water-year numeric tables and the verbatim limitations/funding text. One noted ambiguity, flagged in the relevant key_claim's evidence_note: the source sentence giving the NE/SW '0% in situ vs 11.8%/14.5% satellite' quadrant disparity immediately follows the WY2019 lake-wide statistic but does not itself repeat 'WY2019,' so its exact water-year attribution is inferred from context rather than stated outright in that sentence.
