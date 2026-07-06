# Final Presentation — Design & Structure (scrollytelling HTML story)

**Date:** 2026-07-02 · **Status:** structure converged; Codex critical review folded in (2026-07-02); claim-ledger + 45-min timing-budget added; tool hand-off + honesty beats fixed. **Part 3 stays fully loose** per user direction (broad beats + the added negative-result & claim-boundary beats; Part C remains a single bullet — revisit after results land). Timebox note: the brief's 6–8 h cap is **overridden by standing user direction** (build fit-to-purpose; may seed the real tool), so Codex's "don't over-build the deck" concern is moot — but its sequencing wisdom (defensible findings + tool before cinematic polish) holds. The model-independent foundation is built — `presentation/story.html` (Part 1 with Plotly figures + interactive Leaflet maps); Part 2 in-situ/weather layers and Part 3 results pending.
**Replaces:** a PowerPoint deck. **Why HTML:** Claude Code authors it directly; it supports live maps/figures a `.pptx` can't; one artifact presents live *and* leaves behind.
**Model:** scrolling-story style adapted from `CHCCS_geospatial/example_stories/chccs_demographics.html` (scrollama steps, fixed morphing visual pane, `<details>` collapsibles, `.source`/`.limitation`/`.insight` callouts).

## What this artifact is (and is not)
- **Is:** the narrative story covering **five of the six** brief presentation areas — §1 Problem & decision, §2 Data & approach, §3 Findings/validation/defensibility, §5 Prototype→platform, §6 Recommendation.
- **Is not:** the live tool (§4). Per decision **D-P1**, the tool is a **separate app** the presenter switches to for the ~8-min demo. Following the brief's order (§3 findings → §4 demo), the hand-off comes **after Part 3's defensibility beat** — the panel meets the tool only once the validation has earned their trust, not before.
- **Audience:** mixed panel (scientific, platform, commercial, operations). Translate between domain, data, and business at every step.

## The spine (one hook, one decision)
> **"A harmful algal bloom you can see from space is already too late. Can we forecast it weeks earlier — defensibly enough to stand behind a treatment recommendation?"**

- **Decision informed:** where and when a SePRO specialist pre-positions or treats, **1–4 weeks ahead**.
- **Who acts:** SePRO field/technical specialist + their customer (utility, lake manager).
- **The claim we're testing** (not asserting): whether an explainable forecast that **adds in-situ water chemistry** can match or beat the **federal EPA forecast** at h = 1 and **extend useful lead time to h = 2–4**. It may not — that outcome is a real finding, and the deck is built to report it plainly (principle 7).
- **Concrete anchor (open decision D-P2):** thread the story through **Lake Okeechobee + Lake Apopka** (both real, both in the model's validation runs), with the 133-lake portfolio as backdrop.

## Design principles (the directives + the claim gate)
1. **Sources dropdown on every step.** Don't lead with sources — tuck a closed `<details>` at the step's foot showing the origin of every datum used there (name · use · access URL/DOI + date · citation key → `Research/REFERENCES.md`).
2. **Sparing jargon, defined on the spot.** Minimize technical terms; where one is unavoidable, define it in a second closed `<details>` ("Terms"). Both audiences served: laypeople skip it, scientists verify it.
3. **Terse.** Bullets over prose. The panel reads the screen fast; the presenter carries the detail.
4. **Flexible per-step layout.** No fixed "text left / figure right." Each step picks: text-only · figure-only · split-L · split-R · full-bleed.
5. **Claim gate on every number** (inherited, non-negotiable): traces to a cited real source · regenerates from checked-in code · reported **with a baseline and an uncertainty** · **bounded** by its limits. No number that can't pass all four. Weak/negative results are shown, not hidden.
6. **No fabrication.** Any result not yet produced is a labeled **`[PLACEHOLDER]`** (see Design System), never a stand-in number or mock chart that could read as real.
7. **Voice: plain, direct, honest — never marketing-y.** Write like a scientist briefing peers, not a product page. This governs every word on every step:
   - **Frame the work as a test, not a boast.** It is entirely possible our build does **not** add value over the existing public offerings — *that is the hypothesis we are testing,* and the deck says so in plain words. Ban promotional register: no "powerful," "seamless," "revolutionary," "unlock," "game-changing," "cutting-edge," "robust" as filler. State what we did, what we found, and how sure we are.
   - **Be suggestive, not prescriptive, about use.** We do not yet know exactly how a SePRO specialist or customer would use this. Offer possibilities, show the data, and **invite the panel's input** — don't dictate a workflow or imply we know their job better than they do.
   - **Calibrate language to evidence** (see principle 5). Never imply more certainty than the model supports; every value travels with its baseline, uncertainty, and limits.
   - **Smell test:** if a sentence could sit unchanged in generic AI-generated marketing copy, cut it or rewrite it as a short declarative. Concrete and modest beats sweeping and vague.

## Layout engine — three parts
Per decision **D-P3**: front and back are **discrete flexible slides**; the middle "data" part is **one pinned Florida map that morphs** as sources are layered on, QA'd, and explored.

| Part | Layout | DS arc | Brief area | ~time |
|-----|--------|--------|-----------|------|
| **1 · The problem** | discrete slides | define | §1 | ~6–7 min |
| **2 · The data** | **pinned morphing FL map** | acquire · prepare/QA · explore | §2 | ~10 min |
| **3 · Findings → platform → ask** | discrete slides | model · evaluate · communicate · deploy | §3, §5, §6 | ~18 min |

**Layout modes** (a `data-layout` attribute per step drives CSS): `text` · `figure` · `split-l` · `split-r` · `full`. The pinned-map part is its own mode: text steps float beside the map and dim it; a figure-only beat lets the map go full-bleed.

**45-minute timing budget** (the deck is paced to this; sums to 45): **5** problem & decision · **10** data & approach · **10** findings, validation & defensibility · **8** live tool demo (separate app) · **8** prototype→platform · **4** recommendation. Then ~30 min discussion / Q&A.

---

## Part 1 — The problem (discrete slides) — LOCKED
Now carries the motivation (what exists today / what existing models use / our forward-looking approach), built from the 261-source corpus in `presentation/` + the cited EPA facts in `data-sources/cyano-forecasts/`.

1. **Hook** — interactive Lake Erie CyAN map (Leaflet) with an **8-week 2022 slider** (drag to watch the bloom grow/recede); headline "Forecasting harmful algal blooms before they're visible." *(interactive map)*
2. **The decision this informs** — states the operational choice **generally** (no fabricated example, per user preference): a specialist decides week to week whether/where to pre-position treatment; a forecast one–two weeks early beats a reading taken after the bloom is visible. Names who it serves (utility / lake manager / recreation authority). *(text)*
3. **What exists today** — HAB **tools landscape** (port `fig1_tools_panel`): 12 operational tools, **only ~4–5 forecast *ahead***; most observe/nowcast. EPA highlighted as the lone federal forecaster, with its limits (7-day single horizon · CONUS-only · experimental/beta · over-predicts, precision 0.49 · fragile unofficial access). *(Plotly chart / split; Sources dropdown links **all 12 tools** to their pages)* — **may split into a dedicated "EPA up close" slide** to set the benchmark early.
4. **Literature review — features in existing models** (Plotly feature-frequency chart; #1-predictor marked with a **red outline**): water temperature + nutrients are the most common predictors; "strongest predictor" is correlational (often a seasonal proxy). Existing models combine satellite, in-situ, and weather in various ways. *(Plotly chart / split; Sources dropdown lists all 14 models + their citations)*
5. **Our approach** — the differentiator is the **forward-looking forecast**, not fusion: forecast **0–4 weeks ahead** (most tools only observe/nowcast), **extend** EPA's single 7-day forecast, **add in-situ chemistry EPA doesn't use**, keep it **explainable**, **benchmark to EPA at h = 1**. *(text)*
6. **Our question, precisely** — forecast **WHO AL1** blooms in **133 Florida lakes** at **h = 0–4**, benchmarked to EPA at h = 1 → hands into the Part 2 pinned map. *(text; Terms dropdown: AL1, CyAN)*

**Cited-facts note (corrections folded in):** EPA's product is a **single 7-day (1-week)** horizon — *not* 2 weeks (verified: EPA HAB Forecasts page + Schaeffer et al. 2024). This strengthens "net new": our h = 2/3/4 goes beyond the federal product; h = 1 is the head-to-head. "Subject to being eliminated" is softened to the **cited** version — *experimental/beta, paused after the July-2024 launch then resumed, no official API, rolling ~2-season archive that already dropped 2024* — unless a source on program defunding is supplied.

---

## Part 2 — The data (one pinned Florida map, morphing) — LOCKED
The strongest section for the brief's "thoughtful data handling" criterion: every layer arrives with its rough edges and its source. One Florida basemap persists; each step morphs it. Text floats beside and dims the map; QA beats use `.limitation` callouts.

| Morph state | The map does | Rough edges shown | Source (dropdown) |
|---|---|---|---|
| 5 · **Satellite signal** | 133 resolvable lakes light up; CyAN raster over FL | 300 m pixels; OLCI-only | CyAN `METADATA.md` |
| 6 · **What CyAN measures + limits** | zoom to a lake; pixel semantics | cloud gaps · detection limit (DN 0) · land/mixed-pixel masking · resolvable-area blind spots | CyAN `METADATA.md` §3–5 |
| 7 · **In-situ layers** | NWIS gages + WQP stations appear | sparse · irregular · join distance · staleness | NWIS / WQP |
| 8 · **Weather + basin statics** | ERA5 grid + BasinATLAS L12 basins overlay | grid vs lake mismatch; static-in-time | ERA5 / BasinATLAS |
| 9 · **Fusion** | highlight one lake → one fused lake-week row | (value + staleness) rule; EPA-parity vs augmented tracks | DESIGN.md §2–3 |
| 10 · **Explore** | per-lake bloom-frequency heat + seasonality | ~9–10% base rate (imbalanced); **correlation ≠ causation** | derived target parquet |

Backbone exists now: `models/data/derived/fl_resolvable_lakes.gpkg` (the 133 lakes). Overlays that need the target (`cyan_lake_weekly_fl.parquet`, run in progress) fill in as it completes.

**As built:** the 133 FL lakes render on an interactive Leaflet map (hover/click, basemap toggle), morphing per step (fit-all → zoom **Apopka** → zoom **Okeechobee** with a popup). The **in-situ (NWIS/WQP)** and **weather (ERA5)** layers are shown as **pending** — real pulls not yet done, never mocked — and the FL CyAN raster + bloom-frequency overlay await the target run.

---

## Part 3 — Findings → platform → ask (discrete slides) — LOOSE (define later)
**Deliberately not specced.** Content here depends on model results that do not yet exist (Prepare→Evaluate are TBD). We hold the concrete steps, figures, and numbers until the model runs. For now, only the broad beats, each a `[PLACEHOLDER]` until its artifact lands:

- Modeling **approach** (4 explainable classifiers, multi-horizon, matched to EPA).
- The **bar**: baselines to beat (CyAN autoregressive ladder, persistence, climatology, EPA forecast).
- **Headline** skill vs. lead time. `[PLACEHOLDER]`
- **Calibration + event-based** skill. `[PLACEHOLDER]`
- **Head-to-head vs EPA** at h = 1. `[PLACEHOLDER]`
- **Why it says what it says** (importance / incremental lift over the ladder). `[PLACEHOLDER]`
- **Defensibility** (circularity control, oracle-weather caveat, known-lake-only, AL1-is-a-satellite-proxy).
- **The negative-result path** — an explicit beat for "if fusion does *not* beat persistence / climatology / EPA": what we'd say, and why a clear negative is still a real finding (principles 5, 7). A pre-planned branch, not a slide bolted on.
- **Hand-off to the tool** — placed **after defensibility** (brief §3 → §4): switch to the separate app once the results are established.
- **Platform (Part C)** — architecture across research/field-trial/lab/sensor/satellite/distributor/commercial; production/monitoring/drift/auditability; first 6–12 months. *(Codex flags this as thin; kept loose for now per user direction — revisit when we return to Part 3.)*
- **Claim boundary** — one beat *before* the recommendation: where this applies, where it does not, what it cannot support (e.g., AL1 is a satellite chl-a/dominance proxy — **not** a toxin measure or a treatment-efficacy claim).
- **Recommendation** — the action, stated **suggestively, not prescriptively** (principle 7): show the readout, invite the specialist's judgment; bounded by the claim-boundary beat.
- **Sources & methods** — the full running citation list (brief wants this).

Figure choices, step count, and layouts for Part 3 are **TBD after Evaluate**.

---

## Design system

### The two dropdowns (every step)
- **`<details class="sources">` — "▸ Sources & data"** (closed). Per dataset used on this step: name · what we used it for · access (URL/DOI + access date) · citation key(s) → `Research/REFERENCES.md`. A final Part 3 step aggregates the full list.
- **`<details class="terms">` — "▸ Terms"** (closed). Plain-language definition of any technical term on the step (AL1, CyAN/CI_cyano, resolvable lake, staleness, held-out-year split, calibration, PR-AUC…).
- Styling adapts the example's `.source` (blue) as a collapsible; `.terms` neutral/gray. Consistent ▸ affordance. Never auto-open.

### The `[PLACEHOLDER]` convention (serves the claim gate)
Any result not yet produced renders as a **`.placeholder` block**: dashed border, muted fill, a **"⏳ PENDING MODEL RUN"** tag, one line on *what will go here* and *which script/artifact produces it*, and *the baseline + uncertainty it will carry*. **Never** a fake number or mock chart. A registry lists every placeholder → its artifact dependency, so we know exactly what fills each when results land. Placeholders may resolve to **negative results** — that is an acceptable, reportable outcome.

### Claim ledger (required before any number is locked)
Source-disclosure dropdowns show *provenance*; they are **not** the whole claim gate. Before a number appears on a locked slide it must have a row in a **claim ledger** (`docs/plans/claim-ledger.md`, to build): `claim text · source (+ access date) · producing script/artifact · baseline · uncertainty / bounds · display wording`. Anything that can't fill every column becomes a `[PLACEHOLDER]`, is marked "preliminary," or is cut from the locked slides. Numbers already in the plan that need a ledger row before they lock: **133 FL lakes** (`build_fl_lake_mask.py` → `fl_resolvable_lakes.gpkg`); **12 tools / ~4–5 forecast-ahead / 4-of-14 fusion** (`tools.json` / `models.json` + citation keys); **EPA precision 0.49 / ~9–10 % base rate** (Schaeffer 2024 via `cyano-forecasts/METADATA.md`); **531 OLCI weeks**; **"both anchor lakes appear in validation runs"** (`build_cyan_lake_target.py` 4-week check). This is the direct answer to the platform panelist's "can I reproduce every slide number?"

## Tech stack (as built)
- **Libraries vendored locally** (`presentation/vendor/`): Leaflet + Plotly — the app shell loads with no CDN.
- **Scroll engine:** vanilla `IntersectionObserver` (no library) — activates slides and drives the Part 2 map morph.
- **Maps (all interactive — Leaflet, zoom + basemap toggle):** hero = Lake Erie with a georeferenced CyAN bloom overlay (reprojected to **EPSG:3857** so it aligns with the Mercator basemap — audited 2026-07-02, isolated bug; rest of repo CRS is correct — plus an **8-week 2022 slider** showing the bloom grow/recede); Part 2 = the 133 FL lakes (hover/click), morphing per step. **Two basemaps:** *Political (light)* = local state polygons (**offline**); *Satellite (optical)* = Esri World Imagery tiles (**needs internet**). Default view is offline; the optical view is not. In-situ/weather layers show as **pending** until real pulls land (never mocked).
- **Charts:** Plotly (native hover), built from `data/charts.json` (aggregated from `tools.json`/`models.json` by `build_story_assets.py` — not hardcoded).
- **Data loading:** `data/story_data.js` assigns `window.STORY` (charts + lakes + states + overlay), loaded via `<script src>` so it works from `file://` (browsers block `fetch()` of local files).
- **Sources dropdowns cite real external sources only** (datasets, papers, agency products) — never internal repo files. Every tool in the landscape links to its own page; every one of the 14 models lists its citation(s), resolved from `Research/REFERENCES.md` by the build script.
- **Regenerate assets:** `python presentation/build_story_assets.py`. **Output:** open `presentation/story.html` in a browser.

## Open decisions
- **D-P2 · Anchor lakes** — *recommend* Okeechobee + Apopka (real, iconic, in validation). Revisit if another pair tells the story better.
- **D-P4 · Separate tool's tech** — *recommend* a **standalone HTML page reading precomputed `predictions.json`** over Streamlit: no server to crash in the room, works offline. The precomputed values are an **as-of historical replay** of the forecast pipeline (the model's real outputs for past lake-weeks), framed as exactly that — *not* implied live inference (Codex Q&A). Before building Part B, define the **user task** in plain terms: select lake → select horizon/week → risk with **uncertainty + baseline** → top drivers → suggested action window → limits, including **fallback wording when in-situ (WQP / NWIS) is stale or missing** for a lake. Decide when we build Part B.
- **Part 3 concretization** — after the model produces results.

## Build sequencing (for later — not now)
Buildable now (independent of model results): the scaffold + scroll/layout engine, the dropdown + placeholder systems, **all of Part 1** (figures already exist), and the **Part 2 map shell** (133-lake backbone exists). Part 2 overlays fill in as `cyan_lake_weekly_fl.parquet` completes; Part 3 fills in as Evaluate lands. The tool + `predictions.json` are downstream of the model.
