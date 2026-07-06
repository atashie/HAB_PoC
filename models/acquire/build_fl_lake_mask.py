"""Build the Florida resolvable-lake mask for the CyAN lake-level model (pin #2).

Downloads (caches) the authoritative CyAN MERIS/OLCI resolvable-lakes shapefile
(`updatedValidLakes.shp`, COMID-keyed lake polygons, CyAN Albers ~= EPSG:5070), clips it to the
Florida state polygon, and writes the FL lake mask used for per-lake CyAN aggregation.

Source (cited): NASA Earthdata / CyAN project, "Lake Shapefile for MERIS and OLCI sensors" —
https://www.earthdata.nasa.gov/s3fs-public/2026-01/MERIS_OLCI_Lakes.zip (public, no login;
accessed 2026-07-02). This is the same resolvable-lakes universe Schaeffer et al. 2024 used
(`OLCI_resolvable_lakes_*.shp`, COMID); the file here contains 2,321 valid lakes CONUS.

FL boundary: US Census 2022 cartographic states 1:20M (cached by compute_gate_estimate.py).

Run:  python models/acquire/build_fl_lake_mask.py
Output: models/data/derived/fl_resolvable_lakes.gpkg  (+ printed FL lake count)
"""
from __future__ import annotations

import os
import ssl
import urllib.request
import zipfile

import geopandas as gpd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
LAKES_URL = "https://www.earthdata.nasa.gov/s3fs-public/2026-01/MERIS_OLCI_Lakes.zip"
LAKES_ZIP = os.path.join(CACHE, "MERIS_OLCI_Lakes.zip")
LAKES_DIR = os.path.join(CACHE, "MERIS_OLCI_Lakes")
STATES_ZIP = os.path.join(CACHE, "cb_2022_us_state_20m.zip")   # cached by compute_gate_estimate.py
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
OUT = os.path.join(OUT_DIR, "fl_resolvable_lakes.gpkg")
STATE = "FL"


def fetch(url: str, dest: str) -> None:
    if os.path.exists(dest):
        print(f"cache hit: {dest}")
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "SePRO-HAB-PoC/0.1 (research)"})
    data = urllib.request.urlopen(req, timeout=120, context=ssl.create_default_context()).read()
    with open(dest, "wb") as fh:
        fh.write(data)
    print(f"downloaded {len(data):,} bytes -> {dest}")


def main() -> None:
    fetch(LAKES_URL, LAKES_ZIP)
    if not os.path.isdir(LAKES_DIR):
        with zipfile.ZipFile(LAKES_ZIP) as z:
            z.extractall(LAKES_DIR)
    shp = os.path.join(LAKES_DIR, "updatedValidLakes.shp")

    lakes = gpd.read_file(shp)
    lakes["COMID"] = lakes["COMID"].astype("int64")
    n_total = len(lakes)
    n_comid = lakes["COMID"].nunique()
    print(f"CONUS resolvable lakes: {n_total:,} features, {n_comid:,} distinct COMID")

    if not os.path.exists(STATES_ZIP):
        raise SystemExit("Run compute_gate_estimate.py first to cache the state boundary.")
    fl = gpd.read_file(f"zip://{STATES_ZIP}")
    fl = fl[fl["STUSPS"] == STATE].to_crs(lakes.crs)
    fl_geom = fl.geometry.union_all() if hasattr(fl.geometry, "union_all") else fl.geometry.unary_union

    # Assign a lake to FL if its representative interior point falls inside FL (avoids
    # double-counting border lakes shared with GA/AL).
    inside = lakes.geometry.representative_point().within(fl_geom)
    fl_lakes = lakes[inside].copy()
    n_fl = len(fl_lakes)
    also_intersect = int(lakes.geometry.intersects(fl_geom).sum())

    os.makedirs(OUT_DIR, exist_ok=True)
    fl_lakes.to_file(OUT, driver="GPKG")

    print("\n" + "=" * 64)
    print(f"FLORIDA RESOLVABLE-LAKE MASK  (STATE = {STATE})")
    print("=" * 64)
    print(f"  FL lakes (interior point in FL) : {n_fl:,}")
    print(f"  FL lakes (any intersection)     : {also_intersect:,}  (incl. border-shared)")
    print(f"  distinct COMID (FL)             : {fl_lakes['COMID'].nunique():,}")
    print(f"  area km^2  min/median/max       : {fl_lakes['AREASQKM'].min():.2f} / "
          f"{fl_lakes['AREASQKM'].median():.2f} / {fl_lakes['AREASQKM'].max():.1f}")
    print(f"  CRS                             : {lakes.crs.to_string() if lakes.crs else 'none'}")
    print(f"  -> wrote {OUT}")
    print("  rows for the model = FL lakes x 531 OLCI weeks = "
          f"{n_fl * 531:,} lake-weeks (pre-QA)")
    print("=" * 64)
    print("Named examples:")
    cols = [c for c in ("GNIS_NAME", "COMID", "AREASQKM") if c in fl_lakes.columns]
    top = fl_lakes.sort_values("AREASQKM", ascending=False)[cols].head(8)
    print(top.to_string(index=False))


if __name__ == "__main__":
    main()
