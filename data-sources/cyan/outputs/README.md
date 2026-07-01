# CyAN outputs

Generated artifacts from the QA and viz steps. All regenerate from checked-in code +
a re-pull of the (gitignored) raw tiles.

| File | What | Tracked? | Regenerate with |
|------|------|----------|-----------------|
| `qa_report.md` | Human-readable QA/QC report | yes | `qaqc/qa_cyan.py` |
| `qa_summary.json` | Machine-readable QA (per-file + cross-file) | yes | `qaqc/qa_cyan.py` |
| `cyan_<tile>_summary.html` | Interactive Plotly: CI over time + DN-category composition. **⚠ Aggregated diagnostic** (per-date spatial stats), labeled as such — not a model input; native values live in the map hover / raw GeoTIFFs | yes (small) | `viz/viz_cyan.py` |
| `cyan_<tile>_peakbloom_*.png` | Static snapshot of a peak-bloom week (visual proof) | yes (small) | `viz/viz_cyan.py` (or the QA/verify script) |
| `cyan_<tile>_map.html` | Interactive Folium map; per-week CI overlay + **native 300 m hover** (DN, CI, ~cells/mL, per pixel — **no aggregation**) + live lat/lon; weeks radio-selectable | **no (gitignored)** — ~9 MB, embeds rasters | `viz/viz_cyan.py` (use `--bbox` to scope; `--agg` opt-in only) |

## Current sample (tile 7_2, Lake Erie region, 2022 weekly)

- **`cyan_7_2_peakbloom_2022-07-17.png`** — western Lake Erie CI for the week of 2022-07-17.
  Shows the classic Maumee-Bay-initiated *Microcystis* bloom (high CI, red) with an eastward
  plume and a secondary Sandusky Bay bloom — the rest of the lake below detection (grey).
- **`cyan_7_2_summary.html`** — the full-year 2022 seasonal cycle: valid-CI coverage and mean
  CI rise from a winter floor (~0.0003) to a mid-summer peak (~0.0065), then recede.
- **`cyan_7_2_map.html`** (regenerate locally) — cropped to the Lake Erie region, 8 evenly-spaced
  weeks, **native 300 m hover** (point at any bloom pixel for its exact DN / CI / ~cells·mL⁻¹). Flip
  between weeks (radio) to watch the bloom appear and dissipate. Series is the consistent `6.0` stream.

Every number here traces to a specific cached file (sha256 in `../data/raw/manifest.jsonl`).
