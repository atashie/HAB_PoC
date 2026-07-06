"""Join each FL resolvable lake to its containing BasinATLAS/HydroBASINS L12 sub-basin + attributes.

Two products, both keyed by COMID:
  1. lake -> L12 mapping (HYBAS_ID, PFAF_ID, NEXT_DOWN) -- the prerequisite for the NWIS/WQP
     "watershed tier" linkage (user: containing-L12 only), and
  2. a curated HAB-relevant L12 static-attribute set (climate, land-use / nutrient-loading proxies,
     anthropogenic pressure, morphology incl. lake-volume as a crude depth proxy, karst, soil).

Join = lake centroid within the L12 polygon (simple, robust for screening). BasinATLAS is EPSG:4326.

Output: models/data/derived/lake_basinatlas_l12.parquet
Run:    python models/prepare/join_basinatlas_l12.py
"""
from __future__ import annotations

import os

import geopandas as gpd
from pyogrio import read_dataframe

HERE = os.path.dirname(os.path.abspath(__file__))
LAKES = os.path.abspath(os.path.join(HERE, "..", "data", "derived", "fl_resolvable_lakes.gpkg"))
GDB = "D:/BasinATLAS_Data_v10/BasinATLAS_v10.gdb"
LAYER = "BasinATLAS_v10_lev12"
OUT = os.path.abspath(os.path.join(HERE, "..", "data", "derived", "lake_basinatlas_l12.parquet"))
FL_BBOX = (-88.0, 24.0, -79.5, 31.5)   # (minx, miny, maxx, maxy) covering FL

# curated HAB-relevant L12 attributes (kept if present). suffix: _s=sub-basin, _u=upstream catchment.
CANDIDATES = [
    # climate
    "tmp_dc_syr", "pre_mm_syr", "pet_mm_syr", "ari_ix_sav", "cmi_ix_syr", "swc_pc_syr",
    # land use / nutrient-loading proxies
    "crp_pc_use", "pst_pc_use", "for_pc_use", "wet_pc_ug1", "urb_pc_use", "ire_pc_use",
    # anthropogenic pressure
    "ppd_pk_uav", "urb_pc_use", "hft_ix_u09", "nli_ix_uav", "gdp_ud_usu", "pop_ct_usu",
    # hydrology / morphology  (lkv_mc_usu = upstream lake volume; crude depth/volume proxy)
    "ele_mt_uav", "slp_dg_uav", "run_mm_syr", "lka_pc_use", "lkv_mc_usu", "dor_pc_pva",
    "gwt_cm_sav", "inu_pc_umn", "kar_pc_use", "ria_ha_usu",
    # soil
    "soc_th_uav", "cly_pc_uav", "snd_pc_uav", "slt_pc_uav", "ero_kh_uav",
]


def main() -> None:
    import pandas as pd
    lakes = gpd.read_file(LAKES)[["COMID", "GNIS_NAME", "AREASQKM", "geometry"]].copy()
    if lakes.crs is None:
        raise ValueError("lake layer has no CRS")

    # read only FL-extent L12 polygons (bbox filter -> a few thousand, not the global ~1M)
    l12 = read_dataframe(GDB, layer=LAYER, bbox=FL_BBOX, use_arrow=True)
    keep_attrs = [c for c in dict.fromkeys(CANDIDATES) if c in l12.columns]
    missing = [c for c in dict.fromkeys(CANDIDATES) if c not in l12.columns]
    l12 = l12[["HYBAS_ID", "NEXT_DOWN", "PFAF_ID", "SUB_AREA", "UP_AREA"] + keep_attrs + ["geometry"]]
    if l12.crs is None:
        l12 = l12.set_crs(4326)

    # MAX-OVERLAP assignment (Codex): assign each lake to the L12 it MOSTLY sits in (largest
    # lake-polygon intersection area) -- handles split-basin & coastal lakes better than centroid.
    lk = lakes.to_crs(5070)
    ov = gpd.overlay(lk[["COMID", "GNIS_NAME", "AREASQKM", "geometry"]],
                     l12.to_crs(5070), how="intersection", keep_geom_type=False)
    ov["iarea"] = ov.geometry.area
    split = int((ov.groupby("COMID")["HYBAS_ID"].nunique() > 1).sum())
    best = ov.loc[ov.groupby("COMID")["iarea"].idxmax()].drop(columns=["geometry", "iarea"])
    out = pd.DataFrame(lakes[["COMID", "GNIS_NAME", "AREASQKM"]].merge(
        best.drop(columns=["GNIS_NAME", "AREASQKM"], errors="ignore"), on="COMID", how="left"))
    n_unmatched = out["HYBAS_ID"].isna().sum()
    out.to_parquet(OUT, index=False)

    print(f"lakes: {len(out)} | matched (max-overlap): {int(out['HYBAS_ID'].notna().sum())} | "
          f"unmatched: {int(n_unmatched)} | split-basin (>1 L12): {split}")
    print(f"distinct L12 sub-basins: {out['HYBAS_ID'].nunique()}")
    print(f"kept {len(keep_attrs)} L12 attrs; missing (not in schema): {missing}")
    print(f"wrote {OUT}")
    # peek
    print("\nsample:")
    cols = ["COMID", "GNIS_NAME", "AREASQKM", "HYBAS_ID", "crp_pc_use", "urb_pc_use", "tmp_dc_syr"]
    print(out[[c for c in cols if c in out.columns]].head(6).to_string(index=False))


if __name__ == "__main__":
    main()
