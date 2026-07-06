"""Pull FL NWIS daily hydrology (discharge/stage/water-temp) and link to our lakes -- efficiently.

Enumerate NWIS sites in the lake bbox, then SPATIALLY FILTER to (lake polygon + 250 m) union (our 94
containing L12 sub-basins) BEFORE fetching any series -- so we only download data relevant to a lake's
direct or watershed tier (D-33 linkage). Then catalog + fetch daily means (2016->present) for the HAB
hydrology params and save the site->lake linkage + long-format daily values.

Params: 00060 discharge, 00065 gage height, 00010 water temp. Daily mean (stat 00003).
Outputs (models/data/interim/nwis_fl/):
  site_linkage.parquet  -- site_id, site_no, lat, lon, tier(direct|watershed), comid, hybas_id
  daily_values.parquet  -- site_id, parameter_code, date, value
Run: python models/prepare/pull_link_nwis_fl.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyogrio import read_dataframe
from shapely.geometry import Point

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "data-sources", "NWIS", "access"))
import nwis_api as nw  # noqa: E402

LAKES = os.path.join(ROOT, "models", "data", "derived", "fl_resolvable_lakes.gpkg")
L12MAP = os.path.join(ROOT, "models", "data", "derived", "lake_basinatlas_l12.parquet")
GDB = "D:/BasinATLAS_Data_v10/BasinATLAS_v10.gdb"
LAYER = "BasinATLAS_v10_lev12"
FL_BBOX = (-88.0, 24.0, -79.5, 31.5)
OUTDIR = os.path.join(ROOT, "models", "data", "interim", "nwis_fl")
PARAMS = ["00060", "00065", "00010"]
START = "2016-01-01"
BUFFER_M = 250.0


def main() -> None:
    os.makedirs(OUTDIR, exist_ok=True)
    lakes = gpd.read_file(LAKES)[["COMID", "geometry"]].to_crs(5070)
    lakes_buf = lakes.copy()
    lakes_buf["geometry"] = lakes.buffer(BUFFER_M)

    l12map = pd.read_parquet(L12MAP)
    our_hybas = set(pd.to_numeric(l12map["HYBAS_ID"], errors="coerce").dropna().astype("int64"))
    l12 = read_dataframe(GDB, layer=LAYER, bbox=FL_BBOX)[["HYBAS_ID", "geometry"]]
    l12 = l12[l12["HYBAS_ID"].astype("int64").isin(our_hybas)].to_crs(5070)

    session = nw.make_nwis_session()
    key = nw.resolve_api_key(Path(ROOT) / "data-sources" / ".env")
    bbox4326 = tuple(float(x) for x in lakes.to_crs(4326).total_bounds)  # (W,S,E,N)
    print(f"enumerating NWIS sites in bbox {tuple(round(x,2) for x in bbox4326)} ...")
    # comma-joined site_type returns 0 (API quirk) -> loop single surface-water types, union.
    # (excludes groundwater wells -> avoids wasted catalog calls.)
    site_by_id = {}
    for st in ["ST", "ST-CA", "ST-DCH", "LK", "SP", "ES"]:
        try:
            got = nw.enumerate_sites(session, bbox=bbox4326, site_type_code=st, api_key=key)
            for s in got:
                if s.latitude is not None and s.longitude is not None:
                    site_by_id[s.id] = s
            print(f"  site_type {st}: {len(got)}")
        except Exception as e:  # noqa: BLE001
            print(f"  site_type {st} fail: {str(e)[:50]}")
    recs = [(s.id, s.site_no, s.latitude, s.longitude) for s in site_by_id.values()]
    print(f"  enumerated {len(recs)} geolocated surface-water sites")
    sg = gpd.GeoDataFrame(pd.DataFrame(recs, columns=["site_id", "site_no", "lat", "lon"]),
                          geometry=[Point(lon, lat) for _, _, lat, lon in recs], crs=4326).to_crs(5070)

    # tier 1: direct (within lake+250m) -> COMID (keep first if multiple)
    d = gpd.sjoin(sg, lakes_buf, how="left", predicate="within").drop(columns="index_right")
    d = d.rename(columns={"COMID": "comid"}).drop_duplicates("site_id")
    # tier 2: for sites without a direct lake, assign the containing L12
    nd = d[d["comid"].isna()].drop(columns=["comid"])
    w = gpd.sjoin(nd, l12, how="left", predicate="within").drop(columns="index_right")
    w = w.rename(columns={"HYBAS_ID": "hybas_id"}).drop_duplicates("site_id")
    link = d[d["comid"].notna()][["site_id", "site_no", "lat", "lon", "comid"]].copy()
    link["tier"] = "direct"; link["hybas_id"] = pd.NA
    wk = w[w["hybas_id"].notna()][["site_id", "site_no", "lat", "lon", "hybas_id"]].copy()
    wk["tier"] = "watershed"; wk["comid"] = pd.NA
    link = pd.concat([link, wk], ignore_index=True)
    print(f"  retained {len(link)} sites: direct={int((link.tier=='direct').sum())}, "
          f"watershed={int((link.tier=='watershed').sum())}")

    # catalog + fetch daily means for retained sites
    rows, n_series = [], 0
    for i, sid in enumerate(link["site_id"].tolist()):
        try:
            series = nw.catalog_series(session, sid, parameter_codes=PARAMS, api_key=key)
        except Exception as e:  # noqa: BLE001
            print(f"  [{sid}] catalog fail: {str(e)[:50]}"); continue
        for s in series:
            if nw.series_service(s) != nw.COLL_DAILY:
                continue
            pc = s.get("parameter_code")
            if pc not in PARAMS:
                continue
            try:
                recs = nw.fetch_series(session, nw.COLL_DAILY, sid, pc,
                                       statistic_id=nw.DEFAULT_STAT, start=START, api_key=key)
            except Exception as e:  # noqa: BLE001
                print(f"  [{sid}/{pc}] fetch fail: {str(e)[:50]}"); continue
            n_series += 1
            for r in recs:
                rows.append((sid, pc, r.get("time"), r.get("value")))
        if (i + 1) % 25 == 0:
            print(f"  ...{i+1}/{len(link)} sites, {n_series} series, {len(rows):,} values")

    vals = pd.DataFrame(rows, columns=["site_id", "parameter_code", "date", "value"])
    vals["value"] = pd.to_numeric(vals["value"], errors="coerce")
    vals = vals.dropna(subset=["date", "value"])
    link.to_parquet(os.path.join(OUTDIR, "site_linkage.parquet"), index=False)
    vals.to_parquet(os.path.join(OUTDIR, "daily_values.parquet"), index=False)
    print(f"\nDONE: {len(link)} sites, {n_series} series, {len(vals):,} daily values")
    print("  by param:", vals.groupby("parameter_code").size().to_dict())
    print(f"  wrote {OUTDIR}/site_linkage.parquet + daily_values.parquet")


if __name__ == "__main__":
    main()
