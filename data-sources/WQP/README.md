# Water Quality Portal (WQP) — how to use this dataset in the repo

**What it is + all the metadata:** read [`METADATA.md`](METADATA.md) first. It covers the source systems, the
two coexisting schemas (legacy WQX 2.2 + WQX 3.0 beta), the 2024-03-11 USGS split, geotagging + NWIS/NARS linkage,
the exact result encoding + censoring, known limitations, access, and the modeling role.

This README is the **operational run-guide**. Load-bearing source quotes are preserved in
[`reference/PRIMARY-SOURCES.md`](reference/PRIMARY-SOURCES.md).

> **Status (2026-07-01):** `METADATA.md` + `reference/` (*document-before-you-pull*) and the **`access/` layer**
> (`wqp_api.py` + `discover_wqp.py` + `xcheck_dataretrieval.py`, 17 unit tests, run live on the Lake Erie scope)
> are complete and Codex-reviewed. **Next:** freeze `reference/inclusion-rules.md`, then `qaqc/` → `viz/`. No auth
> is needed for WQP, so there is no credential setup step.

## Directory map

| Path | What | Tracked in git? |
|------|------|-----------------|
| `METADATA.md` | Full dataset characterization | yes |
| `reference/PRIMARY-SOURCES.md` | Preserved verbatim source quotes + live-probe log | yes |
| `reference/schema_crosswalk.csv` | legacy WQX2.2 ↔ WQX3 column map (from EPA published crosswalk) | yes *(pending)* |
| `reference/analyte-dictionary.md` | Human-reviewed analyte harmonization groups (post-discovery) | yes *(pending)* |
| `reference/inclusion-rules.md` | Predeclared site/parameter inclusion thresholds (anti result-shopping) | yes *(pending)* |
| `access/wqp_api.py` | REST client over `../_common/net.py`: URL/param build (both schemas), ISO→MM-DD-YYYY dates, count headers, legacy↔WQX3 crosswalk, cross-schema dedup key, censoring logic, cached+sha256+manifest fetch | ✅ built (17 unit tests) |
| `access/discover_wqp.py` | Discovery-first CLI: legacy Summary inventory + WQX3 post-split freshness probe → report + CSV | ✅ built (run live) |
| `access/xcheck_dataretrieval.py` | Cross-validation vs the USGS `dataretrieval` package (independent check, not canonical) | ✅ built |
| `tests/test_wqp_api.py` | Unit tests for the pure logic (URL build, crosswalk, dedup key, censoring, counts, dates) | yes (17 pass) |
| `qaqc/qa_wqp.py` | Schema conformance · legacy↔WQX3 reconciliation/dedup · censoring-state · units/fraction/method · datum/coords · dup + revision-delta report | *(pending)* |
| `viz/viz_wqp.py` | Native-resolution site map (by recency/availability) + per-characteristic count-over-time | *(pending)* |
| `outputs/` | Discovery table, QA report + JSON, revision report, small PNG, summary HTML | yes (small) |
| `data/raw/`, `data/derived/` | Cached pulls + `manifest.jsonl` | **no (gitignored)** |

## Build order (why this sequence)

1. **Document** — `METADATA.md`, `reference/` ✅
2. **Discover** — run `discover_wqp.py` over the start scope → availability/recency table (parameters are chosen
   *from real availability*, per the discovery-first decision).
3. **Freeze inclusion rules** — write `reference/inclusion-rules.md` **before** selecting features.
4. **Pull** — `wqp_api.py` for Result + **DQL** (censoring) over the frozen selection; cached + manifested.
5. **Reconcile + QA** — `qa_wqp.py`: dedup legacy↔WQX3 to the canonical key, derive censoring, harmonize analytes,
   check datum/coords, emit QA + revision reports.
6. **Visualize** — `viz_wqp.py`.

## Starting scope (assumption, parameterized)

Discovery starts at the **western Lake Erie basin** — Maumee **HUC8 `04100009`** + Lucas County OH (`US:39:095`)
+ states OH/MI — to fuse with the CyAN Lake Erie validation tile (`7_2`). All scripts take `--bbox` / `--statecode`
/ `--huc` / `--countycode` so scope widens to CONUS without code changes.

## Gotchas (see METADATA.md for detail)

- **Two schemas, don't blind-union.** Ingest legacy + WQX3, then **reconcile to one canonical de-duplicated
  record set** (METADATA §10). WQX3 is backward-compatible → a naive union double-counts.
- **Legacy has no post-2024-03-11 USGS data** (added *or modified*). Prefer WQX3 for USGS.
- **No `/wqx3/summary`** (404). Discovery = legacy Summary (broad) + WQX3 Station/Result probes (post-2024 USGS).
- **`ResultMeasureValue` is a string** — `"NA"`/blank ≠ 0 and ≠ non-detect. Pull the **DQL** profile; derive an
  explicit censoring state; **no imputation** before modeling.
- **Analyte ≠ name.** Same characteristic varies by fraction/unit/method/speciation; harmonize via the reviewed
  dictionary, not by `CharacteristicName` alone. WQX and USGS naming differ (DO vs "oxygen").
- **Coordinates:** filters expect **WGS84**; keep datum/accuracy; prefer **activity** coords over station centroid;
  reproject explicitly before any CyAN pixel join.
- **Values revise** (provisional→accepted; USGS reprocessing). Same URL ≠ same bytes — the revision-delta report
  makes changes visible.
- **CyAN join = the main leakage surface.** As-of joins only; blocked spatial (site/HUC) + temporal (season/year)
  splits; never same-station random splits (METADATA §9).
- **Never aggregate (spatial or temporal) without explicit permission** — project rule; default to native records.
- **Subset, don't mirror** — bounded queries by space × characteristic × time.
