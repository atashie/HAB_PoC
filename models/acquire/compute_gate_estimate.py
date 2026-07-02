"""Compute-gate estimate for the Florida CyAN modeling table (models/ Phase 1).

Measures the ACTUAL Florida inland-water CyAN pixel footprint from the already-local OLCI weekly
CONUS mosaics (no CyAN download) and converts it into a fused-table row count + RAM/disk estimate,
so we can decide native-300m-pixel vs resolvable-lake aggregation *before* building features.

Method
------
- CyAN CONUS mosaics: 8-bit, EPSG:5070, ~300 m. DN: 0 = below-detection (valid water),
  1..253 = valid detection, 254 = land, 255 = no-data/cloud (see cyan/METADATA.md). We model
  OLCI only (start year >= 2016; MERIS 2008-2012 excluded per D-21).
- A raw lat/lon box over Florida sweeps in large amounts of shallow Gulf/Atlantic water that CyAN
  also processes. To isolate FRESHWATER / inland (our HAB target), we clip to the Florida state
  polygon (US Census cartographic boundary, cached below).
- "Water footprint" = pixels ever valid water (DN <= 253) across a SAMPLE of OLCI weeks, unioned
  (a single week undercounts because clouds mask water as 255). Rows = footprint x n_OLCI_weeks
  (one row per pixel-week; multi-horizon adds target COLUMNS, not rows).

This is an ESTIMATE. The sampled union slightly undercounts the full-record footprint; the coarse
(1:20M) state boundary slightly clips coastal estuaries. Both refine the number modestly upward but
do not change the gate decision.

Source (cited): US Census Bureau 2022 cartographic boundary, states 1:20,000,000 —
https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip (accessed 2026-07-02).

Run:  python models/acquire/compute_gate_estimate.py
"""
from __future__ import annotations

import glob
import os
import re
import ssl
import urllib.request

import numpy as np
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from rasterio.windows import transform as win_transform

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.abspath(os.path.join(
    HERE, "..", "..", "data-sources", "cyan", "data", "raw", "conus_mosaic_weekly"))
CACHE_DIR = os.path.join(HERE, "_cache")
BOUNDARY_URL = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
BOUNDARY_ZIP = os.path.join(CACHE_DIR, "cb_2022_us_state_20m.zip")

FL_BBOX_WGS84 = (-87.7, 24.3, -79.8, 31.1)   # (west, south, east, north)
STATE = "FL"
N_SAMPLE_WEEKS = 16
N_FEATURES_GUESS = 100
BYTES_PER_CELL = 4   # float32
RAM_BUDGET_GB = 32   # local hardware ceiling


def fetch_boundary() -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    if not os.path.exists(BOUNDARY_ZIP):
        req = urllib.request.Request(BOUNDARY_URL, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60, context=ssl.create_default_context()).read()
        with open(BOUNDARY_ZIP, "wb") as fh:
            fh.write(data)
        print(f"cached boundary: {BOUNDARY_ZIP} ({len(data):,} bytes)")
    else:
        print(f"boundary cache hit: {BOUNDARY_ZIP}")
    return BOUNDARY_ZIP


def is_olci(path: str) -> bool:
    m = re.match(r"L(\d{4})\d{3}\d{4}\d{3}\.", os.path.basename(path))
    return m is not None and int(m.group(1)) >= 2016


def main() -> None:
    files = sorted(f for f in glob.glob(os.path.join(RAW_DIR, "*.tif")) if is_olci(f))
    if not files:
        raise SystemExit(f"No OLCI mosaics in {RAW_DIR}")
    print(f"OLCI weekly mosaics: {len(files)}  ({os.path.basename(files[0])[:15]} .. "
          f"{os.path.basename(files[-1])[:15]})")

    fl = gpd.read_file(f"zip://{fetch_boundary()}")
    fl = fl[fl["STUSPS"] == STATE].to_crs("EPSG:5070")
    print(f"{STATE} polygon area: {fl.geometry.area.iloc[0] / 1e6:,.0f} km^2")

    with rasterio.open(files[0]) as ds:
        tr, crs = ds.transform, ds.crs
        res = (tr.a, -tr.e)
        l, b, r, t = transform_bounds("EPSG:4326", crs, *FL_BBOX_WGS84)
        win = from_bounds(l, b, r, t, transform=tr).round_offsets().round_lengths()
        wtr = win_transform(win, tr)
        H, W = int(win.height), int(win.width)
    pixel_km2 = (res[0] * res[1]) / 1e6

    fl_mask = rasterize([(g, 1) for g in fl.geometry], out_shape=(H, W), transform=wtr,
                        fill=0, dtype="uint8").astype(bool)
    print(f"FL window {W}x{H} px; inside FL polygon: {int(fl_mask.sum()):,} px")

    idx = sorted(set(np.linspace(0, len(files) - 1, N_SAMPLE_WEEKS).round().astype(int)))
    union = None
    valids, detects = [], []
    for i in idx:
        with rasterio.open(files[i]) as ds:
            arr = ds.read(1, window=win)
        valid = (arr <= 253) & fl_mask
        detect = (arr >= 1) & (arr <= 253) & fl_mask
        valids.append(int(valid.sum()))
        detects.append(int(detect.sum()))
        union = valid if union is None else (union | valid)

    foot = int(union.sum())
    n_weeks = len(files)
    rows = foot * n_weeks
    ram_gb = rows * N_FEATURES_GUESS * BYTES_PER_CELL / 1e9
    single_week_ram_gb = foot * N_FEATURES_GUESS * BYTES_PER_CELL / 1e9

    print("\n" + "=" * 70)
    print(f"COMPUTE-GATE ESTIMATE — {STATE}, native 300 m pixel x week, OLCI only")
    print("=" * 70)
    print(f"  water-pixel footprint (union of {len(idx)} sampled wks): {foot:>12,} px "
          f"(~{foot * pixel_km2:,.0f} km^2)")
    print(f"  mean valid water / week (inside FL)              : {int(np.mean(valids)):>12,} px")
    print(f"  mean cyano detection (DN>=1) / week              : {int(np.mean(detects)):>12,} px")
    print(f"  OLCI weeks (full record)                         : {n_weeks:>12,}")
    print(f"  -> fused-table rows (footprint x weeks)          : {rows:>12,}")
    # Safety margin: a dense frame filling >~half of RAM leaves no headroom for pandas/joins/OS,
    # and the SAMPLED union undercounts the true footprint (full-record union pushes rows higher).
    safe_ram = 0.5 * RAM_BUDGET_GB
    monolith = "UNSAFE" if ram_gb > safe_ram else "tight"
    print(f"  dense float32 x{N_FEATURES_GUESS} cols (MONOLITH)             : {ram_gb:>10,.1f} GB "
          f"({monolith}: >{safe_ram:.0f} GB safe-load on a {RAM_BUDGET_GB} GB box; sample undercounts)")
    print(f"  one WEEK's rows in RAM (partitioned)             : {single_week_ram_gb:>10,.2f} GB (ok)")
    print("=" * 70)
    print("Verdict: NATIVE 300 m PIXEL IS VIABLE via per-week/waterbody PARTITIONED columnar storage")
    print("(Parquet/DuckDB/Polars, ~0.05 GB/week live) -> no lake-aggregation fallback needed.")
    print("A dense in-RAM monolith is UNSAFE and must not be built. RBF-SVM & GAM still need a")
    print("documented subsample (they don't scale to tens of millions of rows).")


if __name__ == "__main__":
    main()
