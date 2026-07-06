"""Assemble the FUSION modeling table: CyAN ladder + static + in-situ (+ weather, when it lands).

Extends `modeling_table_cyan_fl.parquet` (per lake-week x horizon, CyAN antecedent ladder) with the
screened candidate features, each joined **as-of the CyAN cutoff week** (`feature_date` = W-h-1) with a
**(value + staleness)** pair so irregular in-situ sampling is handled without interpolation (D-02).

Feature blocks (selected from the significance screens, `docs/04`):
  * static (by COMID): inundation + top BasinATLAS L12 drivers (area already in base).
  * WQP (as-of cutoff + staleness): TP, water_temp, chl_a (ablation), ammonia, orthoP.
  * NWIS (as-of cutoff + staleness): water_temp, gage_height.
  * WEATHER: added by `add_weather=True` once `weather_features_*.nc` (SPEI rerun) is stable.

Output: models/data/derived/modeling_table_fusion_fl.parquet
Run:    python models/prepare/assemble_fusion_table.py
"""
from __future__ import annotations

import os
import sys

import geopandas as gpd
import pandas as pd
import xarray as xr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "models", "model"))
from screen_insitu_features import lake_week_series  # noqa: E402

DER = os.path.join(ROOT, "models", "data", "derived")
BASE = os.path.join(DER, "modeling_table_cyan_fl.parquet")
L12 = os.path.join(DER, "lake_basinatlas_l12.parquet")
LAKES = os.path.join(DER, "fl_resolvable_lakes.gpkg")
WEATHER = os.path.join(ROOT, "data-sources", "weather", "data", "derived",
                       "weather_features_2016-01-01_2026-06-27.nc")
OUT = os.path.join(DER, "modeling_table_fusion_fl.parquet")
# significant weather drivers (forecast-eligible + key same-week); as-of the cutoff (antecedent track)
WEATHER_FEATS = ["ssrd_trail_14d_mj", "ssrd_trail_30d_mj", "pet_hargreaves_mm", "gdd_trail_30d",
                 "precip_trail_30d_mm", "precip_trail_90d_mm", "spei_1", "spei_4",
                 "wspd_trail_14d_mean_ms", "calm_hours_trail_7d"]

STATIC_COLS = ["inu_pc_umn", "tmp_dc_syr", "pet_mm_syr", "for_pc_use", "crp_pc_use", "hft_ix_u09"]
INSITU = {  # source -> (interim dir, {parameter_code -> label}, [selected variables])
    "wqp": (os.path.join(DER, "..", "interim", "wqp_fl"), {},
            ["TP", "water_temp", "chl_a", "ammonia", "orthoP"]),
    "nwis": (os.path.join(DER, "..", "interim", "nwis_fl"),
             {"00060": "discharge", "00065": "gage_height", "00010": "water_temp"},
             ["water_temp", "gage_height"]),
}


def asof_block(src, interim, labels, variables, weeks_index):
    """Per-(comid, week) as-of value + staleness (weeks since last obs) for each selected variable."""
    vals = pd.read_parquet(os.path.join(interim, "daily_values.parquet"))
    link = pd.read_parquet(os.path.join(interim, "site_linkage.parquet"))
    wk = lake_week_series(vals, link, labels)               # comid, variable, week_start, value
    out = None
    for var in variables:
        g = wk[wk.variable == var]
        pieces = []
        for comid, gg in g.groupby("comid"):
            s = gg.set_index("week_start")["value"].reindex(weeks_index)
            ff = s.ffill()
            last = pd.Series(weeks_index, index=weeks_index).where(s.notna()).ffill()
            stale = ((pd.Series(weeks_index, index=weeks_index) - last).dt.days / 7).round()
            pieces.append(pd.DataFrame({"comid": comid, "week_start": weeks_index,
                                        f"{src}_{var}_val": ff.to_numpy(),
                                        f"{src}_{var}_stale": stale.to_numpy()}))
        blk = pd.concat(pieces, ignore_index=True)
        out = blk if out is None else out.merge(blk, on=["comid", "week_start"], how="outer")
    return out


def weather_block(weeks_index):
    """Per-(comid, week) weather-feature values (nearest 0.25deg cell), as-of the cutoff. Weather is
    dense -> no staleness. Antecedent track (value known by the cutoff week)."""
    if not os.path.exists(WEATHER):
        print("  weather file absent -> skipping weather block"); return None, []
    lakes = gpd.read_file(LAKES)[["COMID", "geometry"]].to_crs(5070)
    cent = lakes.geometry.centroid.to_crs(4326)
    lk = pd.DataFrame({"comid": lakes.COMID.values, "lat": cent.y.values, "lon": cent.x.values})
    ds = xr.open_dataset(WEATHER)[WEATHER_FEATS]
    frames = []
    for r in lk.itertuples():
        d = ds.sel(latitude=r.lat, longitude=r.lon, method="nearest").to_dataframe().reset_index()
        d = d[["date"] + WEATHER_FEATS]; d["comid"] = r.comid
        frames.append(d)
    W = pd.concat(frames, ignore_index=True)
    W["date"] = pd.to_datetime(W["date"])
    dow = W["date"].dt.dayofweek
    W["week_start"] = W["date"] - pd.to_timedelta((dow + 1) % 7, unit="D")
    wk = W.groupby(["comid", "week_start"])[WEATHER_FEATS].mean().reset_index()
    wk = wk[wk["week_start"].isin(set(weeks_index))]
    wk = wk.rename(columns={v: f"wx_{v}" for v in WEATHER_FEATS})
    return wk, [f"wx_{v}" for v in WEATHER_FEATS]


def main() -> None:
    base = pd.read_parquet(BASE)
    base["feature_date"] = pd.to_datetime(base["feature_date"])
    weeks_index = pd.Index(sorted(pd.to_datetime(base["target_date"]).unique()), name="week_start")

    # static (by COMID)
    st = pd.read_parquet(L12).rename(columns={"COMID": "comid"})
    keep = ["comid"] + [c for c in STATIC_COLS if c in st.columns]
    fusion = base.merge(st[keep], on="comid", how="left")

    # in-situ blocks joined as-of the CyAN cutoff (feature_date)
    added = []
    for src, (interim, labels, variables) in INSITU.items():
        blk = asof_block(src, os.path.abspath(interim), labels, variables, weeks_index)
        fusion = fusion.merge(blk.rename(columns={"week_start": "feature_date"}),
                              on=["comid", "feature_date"], how="left")
        added += [c for c in blk.columns if c not in ("comid", "week_start")]

    # weather block (nearest-cell, as-of cutoff)
    wblk, wcols = weather_block(weeks_index)
    if wblk is not None:
        fusion = fusion.merge(wblk.rename(columns={"week_start": "feature_date"}),
                              on=["comid", "feature_date"], how="left")
        added += wcols

    fusion.to_parquet(OUT, index=False)
    newcols = [c for c in keep if c != "comid"] + added
    print(f"wrote {OUT}: {len(fusion):,} rows x {fusion.shape[1]} cols (+{len(newcols)} fusion feats)")
    print(f"  static: {[c for c in keep if c!='comid']}")
    print(f"  in-situ (val+staleness): {added}")
    # coverage: fraction of rows with each in-situ value present
    print("\nin-situ feature coverage (non-null % of rows):")
    for c in [a for a in added if a.endswith('_val')]:
        print(f"  {c}: {100*fusion[c].notna().mean():.1f}%")
    print(f"\n  weather block: {len(wcols)} features (dense, all lakes) as-of cutoff; "
          f"SPEI reflects the 2026-07-05 recompute.")


if __name__ == "__main__":
    main()
