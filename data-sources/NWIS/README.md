# USGS NWIS (Water Data OGC API) — how to use this dataset in the repo

**What it is + all the metadata:** read [`METADATA.md`](METADATA.md) first — coverage, cadence,
the exact record encoding (`approval_status`/`qualifier`), geotagging + cross-dataset linkage,
access, rate limits, and the modeling role. This README is the **operational run-guide**.

> **⚠️ Legacy `waterservices.usgs.gov` is decommissioned in early 2027.** All code here targets
> the new OGC API at `https://api.waterdata.usgs.gov/ogcapi/v0`. See METADATA.md §0/§7.

## One-time setup

Downloading needs **no authentication**. But the keyless rate limit is **1000 requests/hour**,
so for anything beyond a few sites use a **free API key**.

The client **auto-uses** a key from `NWIS_API_KEY` (or `USGS_API_KEY`) in `../.env` if present,
sent as the `X-Api-Key` header (never in a URL/log). To provision one: sign up at
https://api.waterdata.usgs.gov/signup/ and set `NWIS_API_KEY=<key>` in `../.env` (copy
`../.env.example` first if needed). `.env` is gitignored, so **a fresh clone has no key** — add
your own; small pulls still work keyless. *(This working copy has a key configured.)*

## Directory map

| Path | What | Tracked in git? |
|------|------|-----------------|
| `METADATA.md` | Full dataset characterization | yes |
| `reference/` | Preserved primary docs (OGC collections JSON, provisional-statement text, example site) | yes |
| `access/nwis_api.py` | OGC client: constants, site/catalog/series helpers, rate-limit handling, legacy cross-check | yes |
| `access/pull_nwis.py` | CLI: enumerate sites -> catalog -> pull daily/continuous -> tidy CSV + manifest | yes |
| `qaqc/qa_nwis.py` | CLI: QA checks over pulled series + site table -> JSON + Markdown report | yes |
| `outputs/` | Generated QA report + summary JSON | yes (small) |
| `data/raw/sites/*.csv` | Enumerated site metadata (geotagging tables) per AOI | **no (gitignored)** |
| `data/raw/{daily,continuous}/*.csv` | One tidy series per file (row-per-obs) + `manifest.jsonl` | **no (gitignored)** |

Defaults reflect the project: `--service daily` (the modeling core), the HAB parameter set
(discharge, gage height, temp, specific conductance, DO, pH, turbidity, nitrate), daily-mean
statistic (`00003`). See METADATA.md §4/§9.

## Typical workflow

```bash
cd data-sources/NWIS

# 1) Named sites (the most common, fully-keyless-friendly path): 2 Potomac gages, discharge+temp
python access/pull_nwis.py --sites 01646500 01638500 --service daily \
    --params 00060 00010 --start 2015-01-01 --end 2024-12-31

# 2) Area of interest — ALWAYS narrow by site type (a HUC-8 has 1000s of groundwater wells!):
#    plan first with --dry-run (shows which params exist per site, active vs stale)
python access/pull_nwis.py --huc 02070008 --site-types ST,LK --service daily --dry-run

#    then pull (a key is recommended at this scale; --limit N samples; --workers tunes concurrency)
python access/pull_nwis.py --huc 02070008 --site-types ST,LK --service daily \
    --params 00060 00010 00095 --start 2015-01-01 --limit 25

# 3) Real-time (continuous) instead of daily, in a bounding box, recent window:
python access/pull_nwis.py --bbox -83.8 41.2 -81.5 43.0 --site-types ST \
    --service continuous --params 00010 00095 --start 2026-06-01 --limit 10

# 4) QA/QC everything pulled -> outputs/qa_report.md + outputs/qa_summary.json
python qaqc/qa_nwis.py --today 2026-07-02
```

`--dry-run` needs no data pull (enumerate + catalog only) and prints the plan: for each
`(site, parameter, statistic)` its period of record and whether it's **active** or **STALE**.

## Cross-dataset joins (the payoff — METADATA.md §13)

- **Water Quality Portal:** the site `id` (`USGS-01646500`) **is** the WQP
  `MonitoringLocationIdentifier` — join NWIS sensor data to WQP discrete chemistry with no
  transformation (`nwis_api.to_wqp_id` builds it from a bare number).
- **Watershed / HUC:** every site carries `hydrologic_unit_code` (HUC-8…HUC-12) → WBD polygons
  and any HUC-indexed layer. **EPA NARS/NLA** links **spatially by HUC** (no shared station id).

## Gotchas (see METADATA.md for detail)

- **Never aggregate (spatial or temporal) without explicit permission.** We store native
  per-observation series; NWIS's own daily statistics are provider-side and fine to use as-is.
- **Provisional ≠ missing.** Recent data are `Provisional` (revisable); older are `Approved`.
  Keep the distinction; track `last_modified`. There is no fill value — missing days are omitted.
- **Parameters vary by site.** Never assume a site has temperature/nutrients — the `--dry-run`
  catalog tells you what exists and whether it's still active. Lakes here often have only
  discrete WQP samples, not continuous sensors.
- **A HUC/bbox AOI includes ALL site types** (often >1000 groundwater wells). The tool **refuses**
  to fan out past `--max-sites` (300) without `--limit` — narrow with `--site-types ST,LK,SP`.
- **Rate limit 1000/hr keyless** → HTTP 429 (`Retry-After`); the client raises a clear
  `RateLimitError` (it does *not* blindly retry 429, which would burn more quota). Get an API key.
- **Site-id filter differs by collection:** `monitoring-locations` uses `id` (full `USGS-…`);
  `daily`/`continuous`/`time-series-metadata` use `monitoring_location_id`. The client handles this.
