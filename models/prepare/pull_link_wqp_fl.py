"""Pull FL WQP water-quality (HAB analytes) and link to our lakes -- station-first & efficient.

WQP statewide result queries are huge and time out; the bBox count 500s. So: fetch the FL STATION list
once (statecode US:12 -- lightweight), SPATIALLY FILTER to (lake+250m) [direct] or the containing-L12
[watershed] (D-33), then pull Result rows only for the retained station IDs in small siteid chunks
(small queries also dodge the many-characteristic 500). WQX3 profile carries inline coords.

Characteristics consolidated to clean variable labels (chl_a, TP, TN, ammonia, orthoP, water_temp,
turbidity, secchi, DO, pH, microcystin). NOTE: values are NOT unit/fraction-harmonized here -- this is
a SCREEN; the within-lake rank test tolerates per-lake-consistent noise. Harmonize for production.

Outputs (models/data/interim/wqp_fl/): site_linkage.parquet, daily_values.parquet (schema matches NWIS).
Run: python models/prepare/pull_link_wqp_fl.py
"""
from __future__ import annotations

import io
import os
import sys
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from pyogrio import read_dataframe
from shapely.geometry import Point

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "data-sources", "WQP", "access"))
import wqp_api as wq  # noqa: E402

LAKES = os.path.join(ROOT, "models", "data", "derived", "fl_resolvable_lakes.gpkg")
L12MAP = os.path.join(ROOT, "models", "data", "derived", "lake_basinatlas_l12.parquet")
GDB = "D:/BasinATLAS_Data_v10/BasinATLAS_v10.gdb"
LAYER = "BasinATLAS_v10_lev12"
FL_BBOX = (-88.0, 24.0, -79.5, 31.5)
OUTDIR = os.path.join(ROOT, "models", "data", "interim", "wqp_fl")
START, END = "01-01-2016", "07-01-2026"
BUFFER_M = 250.0
CHAR_LABEL = {
    "Chlorophyll a": "chl_a", "Chlorophyll a, corrected for pheophytin": "chl_a",
    "Phosphorus": "TP", "Total Phosphorus, mixed forms": "TP", "Orthophosphate": "orthoP",
    "Nitrogen": "TN", "Inorganic nitrogen (nitrate and nitrite)": "TN", "Ammonia": "ammonia",
    "Temperature, water": "water_temp", "Dissolved oxygen (DO)": "DO", "Oxygen": "DO",
    "pH": "pH", "Turbidity": "turbidity", "Depth, Secchi disk depth": "secchi",
    "Microcystin": "microcystin",
}


def fetch_stations(session) -> pd.DataFrame:
    url = wq.build_query_url("Station", {"statecode": "US:12"}, schema="legacy")
    r = session.get(url, timeout=180); r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), low_memory=False)
    df = df.rename(columns={"MonitoringLocationIdentifier": "site_id",
                            "LatitudeMeasure": "lat", "LongitudeMeasure": "lon"})
    return df[["site_id", "lat", "lon"]].dropna(subset=["lat", "lon"]).drop_duplicates("site_id")


def link_stations(stations: pd.DataFrame) -> pd.DataFrame:
    lakes = gpd.read_file(LAKES)[["COMID", "geometry"]].to_crs(5070)
    lakes_buf = lakes.copy(); lakes_buf["geometry"] = lakes.buffer(BUFFER_M)
    l12map = pd.read_parquet(L12MAP)
    our = set(pd.to_numeric(l12map["HYBAS_ID"], errors="coerce").dropna().astype("int64"))
    l12 = read_dataframe(GDB, layer=LAYER, bbox=FL_BBOX)[["HYBAS_ID", "geometry"]]
    l12 = l12[l12["HYBAS_ID"].astype("int64").isin(our)].to_crs(5070)

    sg = gpd.GeoDataFrame(stations.copy(),
                          geometry=[Point(x, y) for x, y in zip(stations.lon, stations.lat)],
                          crs=4326).to_crs(5070)
    d = gpd.sjoin(sg, lakes_buf, how="left", predicate="within").drop(columns="index_right")
    d = d.rename(columns={"COMID": "comid"}).drop_duplicates("site_id")
    nd = d[d["comid"].isna()].drop(columns=["comid"])
    w = gpd.sjoin(nd, l12, how="left", predicate="within").drop(columns="index_right")
    w = w.rename(columns={"HYBAS_ID": "hybas_id"}).drop_duplicates("site_id")
    direct = d[d["comid"].notna()][["site_id", "lat", "lon", "comid"]].assign(tier="direct", hybas_id=pd.NA)
    ws = w[w["hybas_id"].notna()][["site_id", "lat", "lon", "hybas_id"]].assign(tier="watershed", comid=pd.NA)
    return pd.concat([direct, ws], ignore_index=True)


def pull_results(session, site_ids, chunk=80) -> pd.DataFrame:
    rows = []
    chars = list(CHAR_LABEL)
    for i in range(0, len(site_ids), chunk):
        ids = site_ids[i:i + chunk]
        params = wq.hab_query_params({"siteid": ids, "startDateLo": START, "startDateHi": END}, chars)
        url = wq.build_query_url("Result", params, schema="wqx3", dataProfile="narrow")
        ok = False
        for attempt in range(3):
            try:
                r = session.get(url, timeout=240)
                if r.status_code == 200:
                    ok = True; break
                time.sleep(4)
            except Exception:  # noqa: BLE001
                time.sleep(4)
        if not ok:
            print(f"  chunk {i//chunk}: FAILED"); continue
        try:
            df = pd.read_csv(io.StringIO(r.text), low_memory=False)
        except Exception:  # noqa: BLE001
            continue
        if len(df):
            for _, x in df.iterrows():
                rows.append((x.get("Location_Identifier"), x.get("Result_Characteristic"),
                             x.get("Activity_StartDate"), x.get("Result_Measure")))
        if (i // chunk + 1) % 5 == 0:
            print(f"  ...{i+len(ids)}/{len(site_ids)} sites, {len(rows):,} rows")
    v = pd.DataFrame(rows, columns=["site_id", "characteristic", "date", "value"])
    v["parameter_code"] = v["characteristic"].map(CHAR_LABEL)
    v["value"] = pd.to_numeric(v["value"], errors="coerce")
    return v.dropna(subset=["parameter_code", "date", "value"])[["site_id", "parameter_code", "date", "value"]]


def main() -> None:
    os.makedirs(OUTDIR, exist_ok=True)
    session = requests.Session()
    print("fetching FL station list ...")
    stations = fetch_stations(session)
    print(f"  {len(stations)} FL stations")
    link = link_stations(stations)
    print(f"  linked {len(link)}: direct={int((link.tier=='direct').sum())}, "
          f"watershed={int((link.tier=='watershed').sum())}")
    vals = pull_results(session, link["site_id"].tolist())
    vals = vals[vals["site_id"].isin(set(link["site_id"]))]
    link.to_parquet(os.path.join(OUTDIR, "site_linkage.parquet"), index=False)
    vals.to_parquet(os.path.join(OUTDIR, "daily_values.parquet"), index=False)
    print(f"\nDONE: {link.site_id.nunique()} linked sites, {len(vals):,} values")
    print("  by variable:", vals.groupby("parameter_code").size().sort_values(ascending=False).to_dict())
    print(f"  wrote {OUTDIR}")


if __name__ == "__main__":
    main()
