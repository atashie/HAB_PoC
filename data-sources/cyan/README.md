# CyAN (CI_cyano) — how to use this dataset in the repo

**What it is + all the metadata:** read [`METADATA.md`](METADATA.md) first. It covers coverage,
resolution, the exact DN/flag encoding, known limitations, access, and the modeling role.

This README is the **operational run-guide**.

## One-time setup (for downloading)

Downloading CyAN GeoTIFFs needs a free NASA Earthdata Login AppKey:

1. Create an account: https://urs.earthdata.nasa.gov/users/new
2. Generate an AppKey: https://oceandata.sci.gsfc.nasa.gov/appkey/
3. `cp ../.env.example ../.env` and set `OB_DAAC_APPKEY=<your key>` (the `.env` is gitignored).

*Searching/enumerating files needs no auth — only the actual file download does.*

## Directory map

| Path | What | Tracked in git? |
|------|------|-----------------|
| `METADATA.md` | Full dataset characterization | yes |
| `reference/` | Preserved primary docs (V6 release notes PDF + extracted text) | yes |
| `access/cyan_api.py` | Encoding constants, DN↔CI math, filename parsing, file search | yes |
| `access/pull_cyan.py` | CLI: enumerate → categorize → download → manifest | yes |
| `qaqc/qa_cyan.py` | CLI: QA checks over the pulled rasters → JSON + Markdown report | yes |
| `viz/viz_cyan.py` | CLI: interactive HTML map + summary plots from the pulled rasters | yes |
| `outputs/` | Generated summaries, QA report, interactive HTMLs | yes (small) |
| `data/raw/conus_mosaic_weekly/` | **CANONICAL bulk dataset**: full weekly CONUS-mosaic period of record (6.0) + `manifest.jsonl` | **no (gitignored)** |
| `data/raw/*.tif` (top level) | Lake Erie tile `7_2` 2022 weekly **demo** (52 files) — used by default QA/viz | **no (gitignored)** |
| `data/derived/` | Intermediate products (e.g. mosaic crops used in checks) | **no (gitignored)** |

Defaults reflect project preferences: **`--period weekly`** and **`--stream CYAN` (version 6.0, consistent
across the record)**. Preferred period of record: **2008–2012 + 2016–present** (skip the sparse
2002–2007 MERIS and the 2012–2016 gap). See METADATA.md §2, §10, §11.

## Typical workflow

```bash
cd data-sources/cyan/access

# 1) Plan (no auth): what would we pull? — Lake Erie tile 7_2, summer 2022 (weekly is default)
python pull_cyan.py --tiles 7_2 --sdate 2022-06-01 --edate 2022-10-01 --dry-run

# 2) Download (needs OB_DAAC_EDL_TOKEN or OB_DAAC_APPKEY in ../.env). --limit caps for a sample.
python pull_cyan.py --tiles 7_2 --sdate 2022-06-01 --edate 2022-10-01

# 3) QA/QC the pulled rasters -> writes outputs/qa_report.md + outputs/qa_summary.json
cd ../qaqc && python qa_cyan.py

# 4) Visualize -> native-resolution interactive map + summary plots into outputs/
#    --bbox crops scope (keeps native res at a usable size); --agg N is OPT-IN aggregation only.
cd ../viz && python viz_cyan.py --tile 7_2 --bbox -83.8 41.2 -81.5 43.0
```

For national coverage use the mosaic (`--tiles all` → one whole-CONUS file/date), not 54 tiles (METADATA §3/§11).

## Gotchas (see METADATA.md for detail)

- **Never aggregate (spatial or temporal) without explicit permission** — analysis *or* viz. Default to
  native 300 m; reduce scope, not resolution, if something is too heavy. (`viz --agg` is opt-in only.)
- **DN 0 is "below detection," not missing.** Don't fold it into NaN. There is **no NaN / no nodata flag** —
  land=`254`, no-data=`255`, clear water=`0` are all explicit integer codes we mask ourselves.
- **Use the merged `L…` product**, not the per-satellite `S3A_/S3B_` files (both are returned).
- **Default stream `CYAN` = version `6.0`** (consistent across the record); `CYANV6T` = `6T` is a partial
  batch. Version is verified from the `OBPG_version` GeoTIFF tag at QA time, not the filename.
- **The search endpoint 502s intermittently** — the client retries automatically.
- **Don't bulk-mirror the archive** — subset by tile + date (or use the mosaic for national).
