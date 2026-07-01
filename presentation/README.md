# HAB Landscape Slides

Two client-orienting slide topics on the current world of freshwater HAB monitoring & forecasting, built entirely from the project's 261-source research corpus. Output: **`HAB_landscape.pptx`** (5 slides, 16:9).

## What's in the deck

| # | Slide | Content |
|---|-------|---------|
| 1 | **Tools — lead** | "What's available today": a compact **3-row stacked** barplot column (org type / access / method), each bar carrying a **red outline = how many of those tools forecast ahead** (vs. nowcast/observe) + an expanded takeaways column + a **forecast-only** tools table (Tool, Method, Refresh, Coverage, Spatial-res-in-m) |
| 2 | **Tools — appendix** | Full 12-tool inventory: method, horizon, refresh, resolution, access, year, evidence-anchored quality tier, citation keys |
| 3 | **Models — lead** | "The research frontier": feature-frequency hero figure — bars **colour-coded by feature class** (weather / hydroclimate / static / earth-obs·bloom-signal / chemistry), with a **red outline** marking how often each feature is a model's #1 predictor — plus takeaways + flagship table |
| 4 | **Models — appendix** | Full inventory (**14 models + 1 review**): algorithm, forecast target, mode, data signal, **features used → top predictor**, citation keys + the algorithm/data-signal context strip |
| 5 | **How to read** | Method, the evidence-anchored quality-tier rubric, the correlation-not-causation caveat, provenance |

Speaker notes on every slide carry the detail held off the grid (per-tool evidence basis, per-model skill metrics).

## Provenance & fidelity

- **Every attribute traces to a source.** Each tool/model cell carries citation key(s) that resolve in [`../Research/REFERENCES.md`](../Research/REFERENCES.md); unknowns are marked **`n/r`** (not reported), never guessed. A build-time check confirms **0 dangling citation keys**.
- **Scope:** freshwater cyanobacteria only; marine systems excluded (a few tools whose parent program also covers marine are footnoted).
- **Quality tiers are evidence-anchored** (rubric on slide 5): established-operational / operational-unbenchmarked / vendor-self-report / research-grade — the cited basis for each is in `data/tools.json` and the source dossiers.
- **Feature "importance" is correlational** (how often a feature is a model's top-ranked predictor), not causal — stated on-slide and in the data.
- **Small N:** counts are raw with N labelled (no percentages) — orientation, not statistics.
- **Consistent model universe:** the inventory has 15 entries = **14 nowcasting/forecasting models** (`is_model=true`) **+ 1 literature review** (ACAD-068, context only). Every model chart uses the 14-model universe; the feature-frequency chart is labelled "10 of 14" because only 10 models report an environmental feature list (the other 4 are abstract-only, a process-model surrogate, or a sensor benchmark).
- Incorporates a Claude design review (2026-07-01) that corrected two mis-keyed citations and one misattributed feature before build (see `../docs/plans/2026-07-01-hab-landscape-slides-design.md`).

## Files

```
presentation/
  HAB_landscape.pptx     # the deck (generated)
  build_figures.py       # matplotlib -> figures/*.png
  build_deck.py          # python-pptx -> HAB_landscape.pptx
  data/
    tools.json           # 12 operational tools; every attribute + source keys
    models.json          # 15 research models; features/top-features + source keys
  figures/
    fig1_tools_panel.png       # 3x1 stacked: org / access / method, red outline = # forecasting
    fig2_feature_frequency.png # hero: features used, class-coloured + red-outline #1-predictor
    fig3_models_context.png    # algorithm family + data signal (N=14 models)
```

## Regenerate

```bash
python presentation/build_figures.py   # rebuild the 3 figures from data/*.json
python presentation/build_deck.py      # rebuild HAB_landscape.pptx
```
Requires `python-pptx`, `matplotlib`, `Pillow`. Edit the `data/*.json` (the single source of truth) and re-run both scripts to update everything.

## Verification performed

- Figures inspected visually (the visual heart of the lead slides).
- Deck verified structurally: 5 slides; table dimensions (12-tool, 15-model, 4-tier rubric); images embedded; all 42 on-slide citation keys resolve; review fixes present on-slide (ACAD-108 for WASP, ACAD-024 for Lake Erie, longitude/geolocation flagged, correlational caveat).
- Table heights estimated to fit within the slide (no overflow).
- **Not done:** no full visual render of the composed slides (no LibreOffice/PowerPoint renderer available in this environment) — open `HAB_landscape.pptx` in PowerPoint to review final visual layout.
```
