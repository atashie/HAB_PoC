# Weather layer — primary sources (verbatim) + live-probe log

Preserved so the audit trail survives link rot. Every load-bearing claim in `../METADATA.md` traces here.
**All web sources accessed 2026-07-02.** Probes run 2026-07-02 on Python 3.13, win32.

---

## A. Verbatim / near-verbatim source statements

### Licensing (CC-BY)
- C3S/CDS: *"On July 2, 2025, the License to use Copernicus Products in the Climate Data Store (CDS), Atmosphere
  Data Store (ADS) and the CEMS Early Warning Data Store (EWDS) was replaced with the Creative Commons Attribution
  License (CC-BY)."* Attribution notices: *"Generated using Copernicus Climate Change Service information [Year]"*
  and, for modified products, *"Contains modified Copernicus Climate Change Service information [Year]."*
  — https://forum.ecmwf.int/t/cc-by-licence-to-replace-licence-to-use-copernicus-products-on-02-july-2025/13464
- ECMWF open data: *"Products are available at 0.25 degrees resolution in GRIB2 format"* under a
  *"Creative Commons CC-BY-4.0 licence"* allowing commercial redistribution with attribution.
  — https://www.ecmwf.int/en/forecasts/datasets/open-data
- **[probe] the client's own on-download notice:** *"By downloading data from the ECMWF open data dataset, you agree
  to the terms: Attribution 4.0 International (CC BY 4.0). Please attribute ECMWF when downloading this data."*

### ERA5 resolution / coverage / ERA5T
- CDS ERA5 single-levels: reanalysis **0.25° × 0.25°** (~28 km at equator), **"Regular latitude-longitude grid"**,
  **hourly**, period **"1940 to present"**, latency **"about 5 days"** (early release) with final **"2-3 months
  later"**, **GRIB** format, **CC-BY**. — https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
- ECMWF ERA5 docs: native **spectral T639** (~31 km) regridded via MIR to a **0.25° regular lat/lon** grid.
  **ERA5T** (near-real-time) is **~5 days behind real time**; *"ERA5T data for a month is overwritten with the
  final ERA5 data about two months after the month in question."* GRIB headers: **`expver=0001`** = final ERA5,
  **`expver=0005`** = ERA5T. For a request straddling both, accumulated files can be *"00-06 UTC … from ERA5
  (expver 1) [and] 07-23 UTC … from ERA5T (expver 5)."* NetCDF cannot distinguish the two unless the request
  returns a mixture. — https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation

### ECMWF forecast (IFS / open data) cadence, steps, retention
- Runs **00/06/12/18 UTC**: 00z/12z → **0–144 h (3-hourly), then 150–360 h (6-hourly)**; 06z/18z → **0–144 h**.
  Models: **IFS** (deterministic `oper` + ensemble `enfo`) and **AIFS**. Access: `data.ecmwf.int/forecasts/`,
  AWS/Azure/GCP replicas, and the `ecmwf-opendata` Python client. **Rolling archive = the most recent 12 forecast
  runs (~2–3 days)**; full history needs a service agreement (MARS). — https://www.ecmwf.int/en/forecasts/datasets/open-data
- IFS medium-range resolution unified to **TCo1279 (~9 km)** (Jun 2023 upgrade); open data served at
  **0.1°/0.25°**. IFS **Cy49r1** operational Oct 2024. — https://www.ecmwf.int/en/forecasts/datasets/set-i ;
  https://www.ecmwf.int/en/newsletter/176/earth-system-science/ifs-upgrade-brings-many-improvements-and-unifies-medium

### CDS API / access
- New CDS: *"On September 26, 2024, CDS-Beta officially became the new CDS"*; the legacy system is
  *"decommissioned and no longer accessible."* — https://forum.ecmwf.int/t/goodbye-legacy-climate-data-store-hello-new-climate-data-store-cds/6380
- `cdsapi` needs an account + key in `~/.cdsapirc`; *"One must agree to the Terms of Use of a dataset before
  downloading … done manually from the dataset page."* The CDS *"will queue requests"* that would exceed limits;
  *"submit small requests over very large and heavy requests to ensure their requests are not penalised."*
  — https://cds.climate.copernicus.eu/how-to-api ; CDS user guide.

### Alternatives
- **ARCO-ERA5** (Google public data): ERA5 as **Zarr**, *"regridded to a uniform 0.25° equiangular horizontal
  resolution"*, ML-ready (WeatherBench2), bucket `gcp-public-data-arco-era5` (us-central1), *"updated on a monthly
  cadence … with a 3 month delay."* — https://github.com/google-research/arco-era5 ;
  https://cloud.google.com/storage/docs/public-datasets/era5
- **ERA5-Land** (documented alternative, not chosen): **0.1° (~9 km)**, hourly, **1950→present**, ~50 land
  variables, ~3-month lag (ERA5-Land-T exists). — https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
- **Earthmover** (commercial): *"Icechunk-ERA5: a daily updating, performance-optimized ARCO data cube, with 86
  years of 43 surface and pressure-level variables"* (Zarr/Icechunk); no public pricing. — https://www.earthmover.io/

---

## B. Live-probe log (2026-07-02) — what we ran and saw

Reproducible via `../access/`, `../qaqc/`, `../viz/`.

1. **Installability / versions.** `pip install` resolved & installed on Python 3.13 (win32):
   `cdsapi==0.7.7`, `ecmwf-opendata==0.3.30` (+ `ecmwf-datastores-client==0.5.1`, `multiurl==0.3.9`),
   `cfgrib==0.9.15.1`, `eccodes==2.47.0` (binary eccodes bundled — GRIB decode works with no system install).
2. **Latest run discovery (no auth).** `ecmwf.opendata.Client(source="ecmwf").latest(type="fc", stream="oper",
   step=24, param=["2t"])` → **`2026-07-02 06:00:00`** (today's 06z; ~hours latency). Client emitted the
   500-simultaneous-connection notice + AWS/Azure/GCP replication note.
3. **Single-field download.** `2t`, step 24, `resol=0p25` → `20260702060000-24h-oper-fc.grib2`, **652,687 bytes
   (~637 KB)**, magic bytes `GRIB`. Attribution notice printed on download.
4. **GRIB decode (`cfgrib`/xarray).** Field → variable `t2m`, shape **(721, 1440)** = the global 0.25° grid;
   latitude **90..−90**, longitude **−180..179.75** (−180..180 convention, not 0..360); sample near center
   ≈ **22.1 °C**.
5. **Module pull (`ecmwf_forecast.py`).** Latest `oper` run, params `[2t, tp, 10u, 10v, msl]` × steps `[0,24,48,72]`
   → one concatenated GRIB2 `20260702060000-oper-fc-0p25.grib2`, **13,799,517 bytes (~13.2 MB)**, sha256 recorded
   in `data/raw/forecast_manifest.jsonl`.
6. **QA (`qa_weather.py`).** Integrity **verified** (sha256 vs manifest); grid **721×1440 @ 0.25°** (−180..180);
   steps `[0,24,48,72]`; `expver` = none (forecast). Over the W. Lake Erie crop (77 native cells):
   `t2m` 292–303 K; `msl` 1.01–1.02×10⁵ Pa; `tp` 0→0.0222 m accumulated (GRIB `stepType=accum`, flagged
   `is_accumulation=yes`); `u10`/`v10` `stepType=instant`. 0 flags.
7. **ERA5 CDS request build (`era5_cds.py --dry-run`).** Built a valid `reanalysis-era5-single-levels` request
   (7 core vars, area `[42.5,-84.5,41.0,-82.0]`, `grid [0.25,0.25]`, `data_format grib`) with **no account** —
   confirms request construction; live retrieve pending a CDS key + one-time licence accept.
8. **Viz (`viz_weather.py`).** Native per-cell render of `t2m` at +72 h over W. Lake Erie → `outputs/t2m_step72.png`
   (tracked) + `outputs/t2m_step72_map.html` (gitignored); coherent warm band, no aggregation.
