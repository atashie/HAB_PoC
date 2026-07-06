# Presentation

This folder holds the **final presentation** — `story.html`, an interactive scrolling story — plus the
**landscape data and figure builders** it draws on. Design spec:
[`../docs/plans/2026-07-02-presentation-design.md`](../docs/plans/2026-07-02-presentation-design.md).

---

## The presentation — `story.html`

A **self-contained, scrolling-story** presentation for a mixed panel (scientific / platform / commercial /
operations). Open it directly in a browser (`file://`); no server needed. Slide numbers are auto-assigned
in DOM order at boot (bottom-right of each slide). Parts:

- **Part 1 · The problem** — discrete slides: the hook (a real inland-bloom photo), a **multiple-hypotheses**
  framing of who wants HAB info and what each need takes (→ the use case we chose), the existing-tools
  landscape, the literature's predictors (coloured by the dataset **we** ingest), and our goals + the
  question stated exactly (every claim-narrowing word highlighted into a limitations box).
- **Part 2 · The data** — one **pinned Florida map** that morphs as each source is layered on and QA'd:
  raw CyAN → masking → HydroBASINS → NWIS → WQP → ERA5 → fusion → bloom-frequency. Each source has its
  own step + a dedicated **limitations box**.
- **Part 2b · From data to features** — the feature families (raw → derived) that feed the model.
- **Part 3 · Findings → platform → ask** — now carries **real results** (baseline head-to-head, feature
  ablation, skill-vs-lead-time), parsed from the modeling outputs; Parts B/C stay lightweight slices.

What it uses:
- **Interactive maps (Leaflet, vendored):** the Part 2 map is the **133 CyAN-resolvable Florida lakes**
  plus **real** layers that morph per step — a Florida CyAN raster with an **8-week 2016 slider** (the same
  Lake Okeechobee bloom as the hero photo), the **HydroBASINS L12 sub-basins**, the **NWIS gages** and
  **WQP stations** we linked (real coordinates), and the **ERA5 0.25° grid**. Zoom + a basemap toggle:
  *Political (light)* = local state polygons (**offline**) · *Satellite (optical)* = Esri tiles (**needs internet**).
- **Interactive charts (Plotly, vendored):** the tools landscape; the feature-frequency chart (coloured by
  the dataset we ingest); and the Findings charts (baseline AUC all-weeks-vs-flips, block permutation
  importance, skill-vs-lead-time) — all built from `data/*.json`, none hardcoded.
- **Real photograph hero:** a public-domain USGS photo of the 2016 Lake Okeechobee bloom (credited on-image).
- **Three dropdowns per step:** *Sources & data* (the real external source of every datum), *Terms*
  (plain-language), and *Known limitations* (a terse, honest limitations box on most steps).
- **`[PLACEHOLDER]` blocks** only where a result genuinely does not exist yet (Part B tool, Part C sketch).

Fully offline **except** the optical basemap tiles. Terminology: we forecast **harmful algal blooms
(HABs)**; "cyanobacteria index / dominance" and EPA's "CyanoHAB forecast" are kept where they are the
correct technical names.

---

## Build the presentation's data — `build_story_assets.py`

Deterministic + regenerable (claim gate). Reads only checked-in real data and writes to `data/` + `assets/`:

| Output | What |
|--------|------|
| `data/charts.json` | aggregated chart data for the Plotly figures + **every tool's link** and **every model's citation** (resolved from `../Research/REFERENCES.md`); features carry a **dataset-we-ingest** colour |
| `data/fl_lakes.geojson` | the 133 CyAN-resolvable Florida lakes (EPSG:4326) + per-lake **bloom frequency** (real AL1 target) |
| `data/basemap_states.geojson` | CONUS state outlines for the offline "political" basemap |
| `data/results.json` | **Findings metrics parsed from `../models/outputs/*.md`** (EPA head-to-head at **W-2/h1**; **positive-flip / onset** metrics + EPA cutoffs from `headtohead_onset.md`; feature ablation; model-family grid; a real Lake-Okeechobee example slice) — nothing hand-entered |
| `data/{nwis,wqp}_points.geojson` | the **real** NWIS gages / WQP stations linked to FL lakes (from the pulled `site_linkage` tables) |
| `data/fl_basins.geojson` | the **real** HydroBASINS L12 sub-basins containing our lakes (needs the BasinATLAS gdb on `D:`; skipped with a warning if absent) |
| `data/story_data.js` | one file assigning `window.STORY` (all of the above + overlays); loaded via `<script src>` so it works from `file://` (browsers block `fetch()` of local files) |
| `assets/erie_cyan_*.png` + `.json` | 8 weekly CyAN overlays (Western Lake Erie, 2022), EPSG:3857 — kept for reference |
| `assets/fl_cyan_*.png` + `fl_cyan.json` | **8 weekly Florida CyAN overlays (2016 Okeechobee bloom season)**, EPSG:3857 — the data-section raster |
| `assets/hero_okeechobee_bloom_2016_usgs.jpg` | **downloaded** public-domain USGS hero photo (N. Aumen, 2016-07-09) — not generated, cited on-slide |

```bash
python presentation/build_story_assets.py
```
Requires `geopandas`, `rasterio`, `matplotlib`, `numpy` (+ `python-pptx`, `Pillow` for the legacy deck below).
Edit the source `data/*.json`, re-run, and everything downstream regenerates.

**CRS note (audited 2026-07-02):** the CyAN raster overlay is reprojected to **EPSG:3857** (the earlier
4326 version bowed ~5–9 km at these latitudes); vectors are EPSG:4326 (correct for Leaflet); the modeling
pipeline uses EPSG:5070 equal-area. The rest of the repo's CRS handling was audited and is correct.

---

## Files

```
presentation/
  story.html              # THE PRESENTATION (interactive scrolling story) — open in a browser
  build_story_assets.py   # -> data/{charts.json,fl_lakes.geojson,basemap_states.geojson,story_data.js} + assets/
  vendor/                 # Leaflet + Plotly (vendored locally; no CDN for the app shell)
  data/
    tools.json            # 12 operational tools; every attribute + source keys   (source of truth)
    models.json           # 15 research models; features/top-features + source keys (source of truth)
    charts.json           # generated: Plotly chart data + tool links + model citations + feature->dataset
    fl_lakes.geojson      # generated: 133 FL lakes (+ bloom_freq)
    basemap_states.geojson# generated: CONUS states (offline political basemap)
    results.json          # generated: Findings metrics parsed from ../models/outputs/*.md
    {nwis,wqp}_points.geojson # generated: real linked station points
    fl_basins.geojson     # generated: real HydroBASINS L12 sub-basins
    story_data.js         # generated: window.STORY bundle
  assets/                 # generated: erie_cyan_*.png + fl_cyan_*.png (8 weeks each) + *.json;
                          #   hero_okeechobee_bloom_2016_usgs.jpg (downloaded, public domain)

  # --- legacy landscape deck (superseded by story.html for the talk; still the source of the tool/model data) ---
  HAB_landscape.pptx      # earlier 5-slide landscape deck (pptx)
  build_figures.py        # matplotlib -> figures/*.png (static versions of the Plotly charts)
  build_deck.py           # python-pptx -> HAB_landscape.pptx
  figures/                # fig1_tools_panel.png, fig2_feature_frequency.png, fig3_models_context.png
```

`tools.json` / `models.json` remain the single source of truth for the landscape; they now feed **both**
the legacy figures (`build_figures.py`) and the live Plotly charts (`build_story_assets.py`).

---

## Provenance & fidelity

- **Real sources only.** Every tool and every model links to its actual public source; citation keys resolve
  in [`../Research/REFERENCES.md`](../Research/REFERENCES.md); unknowns are `n/r`, never guessed.
- **Model universe:** 15 inventory entries = **14 nowcasting/forecasting models** (`is_model=true`) + 1
  literature review (context). The feature-frequency chart is "10 of 14" — only 10 report a feature list.
- **Feature "importance" is correlational** (how often a feature is a model's top-ranked predictor), not causal.
- **Claim gate:** every number traces to a cited real source + the code that produced it; TBD results are
  `[PLACEHOLDER]`, never fabricated; the claim ledger (`../docs/plans/claim-ledger.md`, to build) is the audit list.

## Verification performed

- `build_story_assets.py` runs deterministically; outputs spot-checked (133 lakes incl. Okeechobee/Apopka
  with real bloom-frequency; 12/12 tools linked; 14 models / 19 citations; 8 Erie + 8 Florida CyAN weeks;
  395 NWIS + 8,726 WQP linked station points; 94 L12 sub-basins; `results.json` numbers matched to their
  source tables in `../models/outputs/*.md`).
- `story.html` verified structurally: balanced tags (5/5 sections, 49/49 details), inline JS parses
  (`node --check`), all local asset references resolve, 30 auto-numbered slides (22 `.slide` + 8 map-steps),
  14 limitations boxes, all six Plotly chart IDs unique. Findings numbers (incl. the EPA head-to-head)
  are pinned to the **W-2 / h1** scenario end-to-end (the correct 1-week-ahead, latency-fair case).
  Non-ASCII in JS is intentional and valid UTF-8 (—, –, ·, ↔, ©, ², ½); the file declares `charset=utf-8`.
- Technical-accuracy pass (two Codex reviews): cross-checked every deck number against `models/outputs/*.md`
  + docs; reconciled W-1/W-2 consistency, a per-lake-identity overclaim, and the **both-direction "flip" vs
  onset mislabel**. The Findings now use true **positive-flip (onset)** metrics from a new evaluator,
  `../models/model/eval_headtohead_onset.py` → `../models/outputs/headtohead_onset.md` (all five predictor
  classes — persistence · climatology · CyAN-ladder · fusion · EPA @0.10/@0.50 — on the identical shared
  FL-2025 weeks, horizons 0–4; it reproduces the verified W-2/h1 threshold-free numbers as a consistency
  check). The Copernicus "global product already exists" claim is labelled **external / web-research** on-slide.
- CRS handling audited across the repo (see CRS note above).
- **Not done:** no in-environment browser render — open `story.html` in a browser to confirm the visual
  layout (map layering per step, slider, Plotly figures). The basin layer needs the BasinATLAS gdb on `D:`
  to regenerate; the checked-in `fl_basins.geojson` already contains it.
```
