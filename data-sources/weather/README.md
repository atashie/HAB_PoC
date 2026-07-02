# Weather layer — ERA5 reanalysis + ECMWF medium-range forecast

**What it is + all the metadata:** read [`METADATA.md`](METADATA.md) first. It covers the two paired
products (`era5` history + `ecmwf_fc` forecast), the shared 0.25° grid, licensing (CC-BY), the
accumulation/`expver` encoding traps, watershed-linkage design, the **reconciliation recipe (§6)**, access, and
the modeling role. Load-bearing source quotes + our live-probe log are in
[`reference/PRIMARY-SOURCES.md`](reference/PRIMARY-SOURCES.md).

This README is the **operational run-guide**.

> **Status (2026-07-02):** `METADATA.md` + `reference/` (*document-before-you-pull*) complete. **Both `access/`
> paths live-validated end-to-end:** the forecast path (pulled the 2026-07-02 06z IFS run → decoded → QA'd →
> mapped) **and ERA5** (CDS key in `../.env` + licence accepted → Aug-2022 W. Lake Erie pull succeeded → decoded →
> QA'd, 0 flags). `qaqc/qa_weather.py` + `viz/viz_weather.py` run on real files. **Next:** the daily-driver
> reconciliation (de-accumulate → daily → bias-correct) + the leakage-safe as-of join to CyAN.

## Directory map

| Path | What | Tracked in git? |
|------|------|-----------------|
| `METADATA.md` | Full characterization of both products (11 sections) | yes |
| `reference/PRIMARY-SOURCES.md` | Verbatim source quotes + our 2026-07-02 probe log | yes |
| `access/ecmwf_forecast.py` | ECMWF open-data IFS forecast pull (no auth); latest/named run → one GRIB2 + manifest; `--dry-run` | ✅ built + run live |
| `access/era5_cds.py` | ERA5 single-levels CDS pull (auth); bounded region×vars×time → GRIB + manifest; `--dry-run` (no auth) | ✅ built; `--dry-run` verified, live pull pending CDS key |
| `qaqc/qa_weather.py` | Integrity (sha256) · grid/encoding from the file · `expver`/accumulation · native-crop sanity → `outputs/` | ✅ built + run |
| `viz/viz_weather.py` | **Native-resolution** per-cell Folium map + static PNG (no aggregation) | ✅ built + run |
| `outputs/qa_report.md` + `qa_summary.json` | QA report (human + machine) | yes |
| `outputs/*.png` | Small static proof renders | yes |
| `outputs/*_map.html` | Interactive maps | **no (gitignored — heavy)** |
| `data/raw/…` + `*_manifest.jsonl` | Cached GRIB/GRIB2 pulls + manifest | **no (gitignored)** |

## Credentials

- **Forecast (`ecmwf_forecast.py`): none.** Open data is auth-free (CC-BY-4.0). Just run it.
- **ERA5 (`era5_cds.py`): a CDS token + one-time licence accept.**
  1. Free account → copy the key from https://cds.climate.copernicus.eu/how-to-api
  2. Put it in `~/.cdsapirc` **or** add `CDSAPI_URL` / `CDSAPI_KEY` to `../.env` (gitignored).
  3. Open the [dataset page](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels) and
     **accept the licence once** (or `retrieve()` returns 403).

## Quickstart (verified 2026-07-02)

```bash
# From data-sources/weather/access/  (deps: pip install -r ../../requirements.txt)

# 1) Plan without downloading (no auth needed for either):
python ecmwf_forecast.py --dry-run
python era5_cds.py --years 2022 --months 8 --dry-run

# 2) Pull the latest IFS forecast (no auth) — core drivers, 3-day window:
python ecmwf_forecast.py --params 2t tp 10u 10v msl --steps 0 24 48 72

# 3) QA every pulled file (integrity + grid + encoding + native sanity):
python ../qaqc/qa_weather.py

# 4) Native-resolution render of one field/step:
python ../viz/viz_weather.py --file ../data/raw/forecast/<run>-oper-fc-0p25.grib2 --var t2m --step 72

# 5) (after CDS key set) Live ERA5 pull for the same scope:
python era5_cds.py --years 2022 --months 8
```

## Starting scope (user decision, parameterized)

**Western Lake Erie basin, 2008→present** — matches the CyAN validation tile `7_2` and WQP's Maumee
**HUC8 `04100009`** scope, so all layers fuse on one region/time. Bbox default `N42.5 W-84.5 S41.0 E-82.0`
(`--area` / `--bbox` to widen). ERA5 product = **single-levels 0.25° only** (aligns cell-for-cell with the
forecast grid). Access = **bounded CDS pulls** (scripted/cached/manifested), matching the CyAN/NARS/WQP discipline.

## Gotchas (see METADATA.md for detail)

- **Forecast history is ephemeral** — open data keeps only ~2–3 days of runs. Capture runs on a schedule to build
  an archive; ERA5 is the history.
- **`tp` accumulation differs** — ERA5 hourly de-accumulated vs forecast accumulated-from-start. **De-accumulate the
  forecast** before comparing (METADATA §4/§6).
- **ERA5T (`expver=5`)** — the last ~5 days→~2 months of ERA5 is preliminary/revisable; default to **GRIB** so the flag survives; refresh recent windows later.
- **No watershed IDs** — lat/lon only; build HUC linkage via WBD overlay (area-weighting = opt-in aggregation).
- **CDS throttles** — keep ERA5 requests bounded; loop rather than one heavy pull.
- **Never aggregate (spatial or temporal) without explicit permission** — project rule; default to native cell/hour.
- **CC-BY attribution is a licence condition** (not public domain) — carry it on every derived artifact.
