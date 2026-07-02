# EPA NARS / National Lakes Assessment (`nars_nla`) — how to use this dataset

**What it is + all the metadata:** read [`METADATA.md`](METADATA.md) first. It covers coverage,
cadence, the exact encoding/flags, the geotagging & WQP/NWIS/CyAN linkage design, licensing, known
limitations, and the modeling role. This README is the **operational run-guide**.

**Scope of this folder:** the **National Lakes Assessment (NLA)** — the HAB-relevant NARS survey.
The framework (catalog → pull → QA → viz) is built so other NARS surveys (NRSA/NCCA/NWCA) can be
added later with the same pattern. Worked example = **NLA 2022**.

## One-time setup

No credentials needed — NLA files are U.S. public-domain, no authentication. Just the shared env:

```bash
cd data-sources
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Directory map

| Path | What | Tracked in git? |
|------|------|-----------------|
| `METADATA.md` | Full dataset characterization (read first) | yes |
| `reference/` | Preserved primary docs: field dictionaries (`*_siteinfo.txt`, `*_algaltoxins.txt`, `*_waterchem_wide.txt`) | yes |
| `access/nars_catalog.py` | Pinned NLA file manifest + filename parsers + live-page drift `discover`/`reconcile` | yes |
| `access/pull_nars.py` | CLI: select cycle/indicators → download → cache → sha256 manifest | yes |
| `qaqc/qa_nars.py` | CLI: integrity + header-vs-dictionary + distributions + join-key + geotag checks → report | yes |
| `viz/viz_nars.py` | CLI: per-lake interactive map + Plotly summary + static PNG | yes |
| `tests/` | Unit tests for the catalog parsing/manifest logic | yes |
| `outputs/` | `qa_report.md`, `qa_summary.json`, `nla2022_summary.html`, `*_map.png` | yes (small) |
| `outputs/*_map.html` | Heavy interactive Folium map | **no (gitignored)** |
| `data/raw/nla<cycle>/` | Downloaded CSVs + metadata `.txt` + `manifest.jsonl` | **no (gitignored)** |
| `data/derived/` | Any intermediate products | **no (gitignored)** |

Defaults: **`--cycle 2022`**, **`DEFAULT_INDICATORS = siteinfo, waterchem, algaltoxins, secchi,
lakes_shp`** (the minimum to fuse with CyAN and build the WQP/NWIS linkage). See METADATA §13.

## Typical workflow

```bash
cd data-sources/EPA-NARS/access

# 1) Plan (no network): what would we pull for the default HAB set, NLA 2022?
python pull_nars.py --dry-run

# 2) Check for drift vs the pinned manifest (network; no download) — should say "clean".
python pull_nars.py --check-drift

# 3) Download the default set (no auth). --indicators all for everything; --limit N to sample.
python pull_nars.py
#    e.g. a specific subset:
python pull_nars.py --indicators siteinfo,waterchem,algaltoxins

# 4) QA/QC the pulled files -> outputs/qa_report.md + qa_summary.json
cd ../qaqc && python qa_nars.py

# 5) Visualize -> per-lake map (native coords, no aggregation) + summary + static PNG
cd ../viz && python viz_nars.py
#    Layered, multi-variable map for ONE state (toggle chl-a/TP/TN/microcystin/cylindrospermopsin/
#    Secchi/turbidity/pH/conductivity per lake; ND shown hollow-grey; evaluated-not-sampled layer):
python viz_nars.py --state NC      # -> outputs/nla2022_<state>_layered_map.html (gitignored; heavy)

# 6) Run the tests (catalog parsing / manifest integrity)
cd .. && python -m pytest tests/ -q
```

## Gotchas (see METADATA.md for detail)

- **No API.** Static CSVs + an interactive Shiny tool only. Data are tiny (~33 MB) → we bulk-mirror
  locally; `--check-drift` catches EPA's incremental re-publishing.
- **Raw file ≠ the 981-lake headline.** The site file (3,880 rows) includes oversample/hand-picked/
  NES/revisit sites. **National/regional %s need the survey weights** (`WGT_TP_CORE_NLA`); `WGT_DSGN`
  is explicitly *do-not-use*. QA §3 reconciles the counts.
- **Sparse coverage — it's a ~981-lake national sample.** Most individual counties have **0–1**
  sampled lakes (e.g. Orange County, NC = **0**; nearest sampled lakes are ~25 km away in Alamance).
  County/local asks should widen to state/region, or use WQP (`../WQP/`) for true local coverage. Use
  `--state` for the finest NLA-supported scope that reliably has data.
- **Non-detect ≠ missing ≠ zero.** `NARS_FLAG=ND` is a *measured* below-detection result (left-censored).
  Blank = not measured. Don't fold ND into 0/NaN.
- **Join keys:** NLA 2022 → `UID`; NLA 2007/older → `SITE_ID`+`VISIT_NO`; same lake across cycles →
  `UNIQUE_ID`. Use `INDEX_LAT_DD`/`INDEX_LON_DD` (sampled point) for matchups, not the centroid.
- **Never aggregate** (spatial/temporal) without explicit permission — viz shows per-lake points at
  native coordinates and is labeled **UNWEIGHTED / not a national estimate**.
- **Units vary within a column** — read the per-row `*_UNITS` field; `NITRATE_N` is ~63% populated
  (use `NITRATE_NITRITE_N` where blank).
- **Linkage to WQP/NWIS/CyAN is designed, not yet built** — see METADATA §11 for the `COMID`/NLDI/
  `HUC8` recipes and their polygon-vs-gage limitation.
