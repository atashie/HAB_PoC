# weather/outputs

Regenerable artifacts from `../qaqc/` and `../viz/`. **Tracked:** QA reports (`qa_report.md`,
`qa_summary.json`) and small static PNGs. **Gitignored:** heavy interactive maps (`*_map.html`,
they embed per-cell geometry). Everything here regenerates from checked-in code over a fresh pull.

- `qa_report.md` / `qa_summary.json` — integrity + grid/encoding + native-crop sanity per pulled file.
- `<var>_<step>.png` — native-resolution static render (visual proof).
- `<var>_<step>_map.html` — interactive Folium per-cell map (regenerate with `viz/viz_weather.py`).
