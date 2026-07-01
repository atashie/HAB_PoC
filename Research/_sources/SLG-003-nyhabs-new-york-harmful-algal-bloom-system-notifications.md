---
key: SLG-003
title: NYHABS: New York Harmful Algal Bloom System — Notifications
authors_or_org: New York State Department of Environmental Conservation (NYSDEC) — Division of Water (DOW), Bureau of Water Assessment and Management
year: 2019 (system launch); ongoing
url: https://dec.ny.gov/environmental-protection/water/water-quality/harmful-algal-blooms/notifications
access_date: 2026-07-01
tier: SLG
source_type: Government agency web page — state environmental agency operational notification/reporting system (NYSDEC), not a peer-reviewed publication
categories: [in-situ-and-weather-data]
relevance: High
full_text_access: full
fetch_status: ok
review_severity: clean
review_overall: pass
---

# NYHABS: New York Harmful Algal Bloom System — Notifications

**What it is.** NYHABS (New York Harmful Algal Bloom System) is a New York State DEC operational notification service, combining an online public/agency reporting form with a public interactive map, that compiles and displays DEC-verified reports of confirmed freshwater harmful algal bloom (cyanobacteria) locations across New York State waterbodies, along with report date, status, spatial extent, submitter, county, and photos.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** NYHABS is a two-part system — an online reporting system plus a public interactive map — through which DEC compiles and publishes notifications of documented HAB locations reported by government personnel, trained monitors, and the public.
  - *evidence:* Both independent fetch passes returned this structural description; it frames everything else on the page (reporting, verification, mapping). (Overview/description section of the Notifications page)
  - *quote:* "composed of 1) an online reporting system, and 2) an interactive map."
- **[✓ verified]** A report only earns "Confirmed Bloom" status after DEC staff determine it meets HAB criteria using visual observation, digital photographs, and/or water sampling results — i.e., confirmation is a human/agency verification step, not an automated or purely citizen-reported label.
  - *evidence:* Identical quoted sentence returned verbatim by both separately-prompted fetch passes, indicating high-fidelity capture of this operational definition of "confirmed." (HAB status / verification description)
  - *quote:* "DEC staff determined that conditions fit the criteria of a HAB, based on visual observations, digital photographs, and/or water sampling results."
- **[✓ verified]** The live interactive map is restricted to a rolling 2-week window of current reports, with icon styling distinguishing recently-reported points from points archived earlier in the same season.
  - *evidence:* The "past 2 weeks" figure was returned by both fetches; the icon-styling explanation (blue icon with black halo = recent; blue icon without halo = archived-this-season) was given as descriptive paraphrase by the fetch tool rather than in quotation marks, so it is reported here as paraphrase, not verbatim. (Map legend / status-indicator description)
  - *quote:* "reported in the past 2 weeks"
- **[✓ verified]** Reports are classified into four standardized bloom-extent categories: Small Localized, Large Localized, Widespread or Lakewide, and Open Water.
  - *evidence:* Both fetch passes returned this identical four-item label set (one pass also gave paraphrased spatial descriptions: Small Localized = one to several neighboring properties; Large Localized = entire cove/large shoreline segment/specific region; Widespread or Lakewide = entire waterbody or most shoreline; Open Water = center-lake sample suggesting widespread conditions). Cross-fetch agreement on the exact labels supports treating the four terms themselves as verbatim legend text, though the descriptive glosses are paraphrase. (Bloom Extent classification / map legend)
  - *quote:* "Small Localized"
- **[✓ verified]** Each point on the map carries a defined metadata schema: observation date, HAB status, extent category, submitter identity, county, and any submitted photographs; users can filter the map by county and waterbody, and the print function only outputs the currently filtered/displayed records.
  - *evidence:* Described in the map-features section of one fetch pass as the structure behind each plotted report. (Map features / filtering description)
- **[✓ verified]** Reports feeding NYHABS originate from four streams: the general public, DEC's Lake Classification and Inventory Program, Citizen Statewide Lake Assessment Program (CSLAP) volunteers, and other partner monitoring programs.
  - *evidence:* Listed as the data-provider sources for the notification system. (Data providers section)
- **[✓ verified]** NYHABS explicitly scopes itself to freshwater cyanobacteria HABs and states it does not cover marine HABs (red tide, brown tide), filamentous green algae blooms, most Lake Champlain HAB reports (NY-side beach reports only; the Vermont Department of Health runs a separate cyanobacteria notification system for the rest of that lake), or beach-closure/drinking-water safety information (referred instead to DEC's swimming page or local health departments).
  - *evidence:* Both fetch passes independently listed this same set of scope exclusions, increasing confidence in its accuracy. (System scope / limitations section)
- **[✓ verified]** Historical (prior-season) HAB notification summaries are not kept on the live map but are archived separately on Open Data NY, with coverage going back to 2012.
  - *evidence:* Both fetch passes returned this same sentence/figure independently, supporting near-verbatim confidence. (Historical data / archive section)
  - *quote:* "Compiled summaries of waterbodies with reported HABs since 2012 are provided on Open Data NY."
- **[✓ verified]** DEC explicitly states that the notification map is not a complete, exhaustive inventory of all HABs statewide, since it depends on reports actually being submitted to DEC.
  - *evidence:* Direct DEC caveat about the reporting-dependent (non-exhaustive) nature of the dataset — a key caution against treating an absence of a mapped report as evidence of a confirmed absence of a bloom. (Data caveats section)
  - *quote:* "There may be other waterbodies with HABs that have not been reported to DEC."
- **[✓ verified]** A HAB reported on part of a large lake or river does not imply the entire waterbody is affected; other portions may remain clear and fully usable for recreation, and DEC's assurance of recreational safety applies only to "designated swimming areas," not to the waterbody as a whole.
  - *evidence:* DEC caveat clarifying the spatial scope of both HAB impact and of DEC's own safety assurance within a single large waterbody. (Data caveats section)
  - *quote:* "designated swimming areas"

## Data / numbers
- 2 weeks — rolling window for which the interactive map displays current HAB reports ("reported in the past 2 weeks")
- 2012 — start year of the historical HAB-notification archive maintained on Open Data NY ("Compiled summaries of waterbodies with reported HABs since 2012 are provided on Open Data NY")
- 518-402-8179 — contact phone number, DOW Bureau of Water Assessment and Management
- 625 Broadway, Albany, NY 12233 — DEC Division of Water office address (contact info, not a data statistic)

## Methods
NYHABS is not a statistical, forecasting, or remote-sensing model — it is an operational surveillance/notification workflow described on the page as follows: (1) intake via an online "Suspicious Algal Bloom Report Form" (ArcGIS Survey123, for the general public) plus a companion "HABs Reporting Guide" PDF for trained program participants; (2) human verification — DEC staff confirm a report only when conditions are judged, via visual observation, digital photographs, and/or water sampling results, to fit HAB criteria; (3) confirmed points are geocoded onto a public interactive map and tagged with observation date, status, an extent category (Small Localized / Large Localized / Widespread or Lakewide / Open Water), submitter identity, county, and photos; (4) the live map shows only a rolling 2-week window of current-season reports and is filterable by county/waterbody; (5) anything older than the current season is moved off the live map into a separate Open Data NY archive covering data since 2012. Contributing data streams are the public, DEC's Lake Classification and Inventory Program, CSLAP volunteers, and partner monitoring programs. The page states no algorithm, sensor, or predictive/statistical model — it is a human-verified, crowdsourced-plus-agency observational reporting and mapping system, explicitly scoped to freshwater cyanobacteria HABs in New York State.

## Stated limitations
The source itself states: (1) scope is freshwater HABs only — marine HABs (red tide, brown tide) are excluded; (2) filamentous green algae blooms are excluded; (3) Lake Champlain HAB coverage is partial — only NY-side beach reports appear in NYHABS, while the Vermont Department of Health maintains a separate cyanobacteria notification system for the rest of the lake; (4) beach closures and drinking-water safety are out of scope, with users referred to DEC's swimming page or local health departments instead; (5) the live map shows only current-season data within a 2-week window — historical notifications are relegated to a separate Open Data NY archive (since 2012), so the notifications page/map is not itself a complete historical record; (6) coverage is explicitly acknowledged as incomplete/reporting-dependent: "There may be other waterbodies with HABs that have not been reported to DEC"; (7) a single HAB report on a large lake or river does not mean the entire waterbody is affected — other portions may remain clear, and DEC's assurance of recreational safety applies specifically to "designated swimming areas," not to entire waterbodies.

## Tensions with other findings
NYHABS is a presence-only, opportunistically-reported and then agency-verified observational dataset (someone must notice a bloom and report it, and DEC staff must confirm it) rather than a systematic, continuous-coverage survey. That creates a methodological tension when pairing it with remote-sensing products such as EPA CyAN (mentioned in this project's own sanctioned source list) that aim for regular wall-to-wall satellite coverage: NYHABS can supply confirmed positive HAB dates/locations/extents for validation or as training labels, but the absence of a NYHABS report at a given waterbody/date cannot be read as a confirmed true negative, since DEC's own text acknowledges unreported blooms occur ("There may be other waterbodies with HABs that have not been reported to DEC"). Any use of NYHABS as ground truth alongside satellite-derived cyanobacteria indices should treat it as a recall-limited, human-verified positive-label source rather than a full presence/absence layer. This tension assessment is my own analytical framing for the literature review, not a statement made by DEC in the source text.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0

## Provenance
- Canonical URL: https://dec.ny.gov/environmental-protection/water/water-quality/harmful-algal-blooms/notifications
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: Fetched the assigned URL twice with different extraction prompts (per HIGH-relevance protocol) and reconciled by union. Both independent passes converged on the same core facts (two-part system description, the "confirmed bloom" verification wording, the "past 2 weeks" map window, the "since 2012" Open Data NY archive line, the four bloom-extent labels, and the core exclusions list), which gives high confidence those specific strings are close-to-verbatim rather than model paraphrase. No redirect occurred; URL resolved directly and content clearly matches the expected page (NYHABS notifications/reporting description, DEC contact block, links to the Suspicious Algal Bloom Report Form and interactive map), so no WebSearch fallback was needed. This is a live, continuously-updated system/landing page rather than a data table or research report, so it is numerically sparse by nature (only a few concrete figures: the 2-week display window, the 2012 archive start year, and contact details) — this scarcity is a property of the page type, not a fetch failure. One pass explicitly noted that the page's status legend, as captured, exposes only a single "Confirmed Bloom" status and does not visibly distinguish toxin-detected from non-toxin-detected confirmations in the legend text returned; I have not asserted this as a DEC-stated limitation (since DEC did not say so), only as an observation about what the fetched legend does/doesn't show — a point worth re-checking against the live map UI/legend directly if this source is used to build toxin-risk labels.
