"""Screen ERA5-derived WEATHER features vs HAB -- same test as the in-situ screen.

Weather is gridded (0.25deg) and DENSE: extract each derived feature at each lake's nearest grid cell
(a lake << a cell), aggregate to the OLCI week, build coincident + lag1/2/4 + anomaly-vs-LOO-climatology
representations, and screen with the lake-block bootstrap AUC (pooled) + within-lake median-AUC
bootstrap (Codex-reconciled engine, imported). All weather features are `driver` class; coverage = all
133 lakes. The derived vars are already trailing aggregates (7-90d sums, SPEI-1/2/4/6, GDD, PET, solar,
wind, calm-hours), so we do NOT re-aggregate -- we test their coincident value and lags.

Output: models/outputs/feature_significance_weather.md
Run:    python models/model/screen_weather_features.py
"""
from __future__ import annotations

import os
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from screen_insitu_features import bh_fdr, boot_stats  # noqa: E402

DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
LAKES = os.path.join(DER, "fl_resolvable_lakes.gpkg")
TARGET = os.path.join(DER, "cyan_lake_weekly_fl.parquet")
WEATHER = os.path.abspath(os.path.join(DER, "..", "..", "..", "data-sources", "weather", "data",
                                       "derived", "weather_features_2016-01-01_2026-06-27.nc"))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "feature_significance_weather.md"))
ANTECEDENT = {"lag1", "lag2", "lag4"}


def main() -> None:
    lakes = gpd.read_file(LAKES)[["COMID", "geometry"]].to_crs(5070)
    cent = lakes.geometry.centroid.to_crs(4326)
    lk = pd.DataFrame({"comid": lakes.COMID.values, "lat": cent.y.values, "lon": cent.x.values})

    ds = xr.open_dataset(WEATHER)
    wvars = list(ds.data_vars)
    # nearest-cell extraction per lake -> long (comid, date, wvars...)
    frames = []
    for r in lk.itertuples():
        sub = ds.sel(latitude=r.lat, longitude=r.lon, method="nearest")
        d = sub.to_dataframe().reset_index()[["date"] + wvars]
        d["comid"] = r.comid
        frames.append(d)
    W = pd.concat(frames, ignore_index=True)
    W["date"] = pd.to_datetime(W["date"])
    dow = W["date"].dt.dayofweek
    W["week_start"] = W["date"] - pd.to_timedelta((dow + 1) % 7, unit="D")
    wk = W.groupby(["comid", "week_start"])[wvars].mean().reset_index()   # weekly mean per lake

    tgt = pd.read_parquet(TARGET).dropna(subset=["bloom"]).copy()
    tgt["bloom"] = tgt["bloom"].astype(int)
    tgt["week_start"] = pd.to_datetime(tgt["start_date"])
    weeks = pd.Index(sorted(tgt["week_start"].unique()), name="week_start")

    # reps per (comid, var): coin, lag1/2/4, anomC(LOO month climatology)
    feat_frames = []
    for comid, g in wk.groupby("comid"):
        g = g.set_index("week_start").reindex(weeks)
        cols = {}
        for v in wvars:
            s = g[v]
            cols[f"{v}__coin"] = s.to_numpy()
            cols[f"{v}__lag1"] = s.shift(1).to_numpy()
            cols[f"{v}__lag2"] = s.shift(2).to_numpy()
            cols[f"{v}__lag4"] = s.shift(4).to_numpy()
            mon = s.index.month
            gs, gc = s.groupby(mon).transform("sum"), s.groupby(mon).transform("count")
            cols[f"{v}__anomC"] = (s - (gs - s) / (gc - 1)).to_numpy()
        f = pd.DataFrame(cols)                          # build once -> no fragmentation
        f["comid"] = comid
        f["week_start"] = weeks.to_numpy()
        feat_frames.append(f)
    feats = pd.concat(feat_frames, ignore_index=True)
    df = tgt[["comid", "week_start", "bloom"]].merge(feats, on=["comid", "week_start"], how="left")

    rows = []
    for c in [c for c in df.columns if "__" in c]:
        d = df[["comid", "bloom", c]].dropna()
        if d["comid"].nunique() < 5 or d["bloom"].nunique() < 2 or len(d) < 50:
            continue
        var, rep = c.rsplit("__", 1)
        st = boot_stats(d, c)
        rows.append({"feature": c, "var": var, "rep": rep,
                     "timing": "antecedent" if rep in ANTECEDENT else "same_week",
                     "n_lakes": d["comid"].nunique(), "n_lw": len(d), **st})
    res = pd.DataFrame(rows)
    res["q_assoc"] = bh_fdr(res["pool_p"].fillna(1).values).round(4)
    res["incl_assoc"] = np.where(res["pool_p"] < 0.1, "Y", "")
    res["incl_within"] = np.where((res["within_p"] < 0.1) &
                                  (res["auc_within"].sub(0.5).abs() >= 0.05), "Y", "")
    res = res.reindex(res["auc_within"].sub(0.5).abs().sort_values(ascending=False, na_position="last")
                      .index).reset_index(drop=True)

    ncov = int(df.groupby("comid")[[c for c in df.columns if "__" in c]]
               .apply(lambda x: x.notna().any().any()).sum())
    md = ["# WEATHER (ERA5-derived) feature significance vs HAB", "",
          f"Coverage: **{ncov}/133 lakes** (gridded 0.25deg, nearest cell -> every lake). All features "
          "`driver` class. Reps: coincident, lag1/2/4 (antecedent/forecast-eligible), anomC (LOO "
          "climatology). Test = lake-block bootstrap AUC (pooled) + **within-lake** median-AUC bootstrap "
          "(read `AUC_within`; <0.5 = inverse). `incl_within` = within p<0.1 & |AUC_within-0.5|>=0.05.",
          "",
          "| feature | timing | n_lk | n_lw | AUC_pool | AUC_within (n) | within_p | incl_within | incl_assoc |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for _, r in res.iterrows():
        wl = f"{r.auc_within:.3f} ({int(r.n_wl)})" if r.auc_within == r.auc_within else "n/a"
        wp = f"{r.within_p:.3f}" if r.within_p == r.within_p else "n/a"
        md.append(f"| `{r.feature}` | {r.timing} | {r.n_lakes} | {r.n_lw} | {r.auc_pool:.3f} | {wl} | "
                  f"{wp} | {r.incl_within} | {r.incl_assoc} |")
    best = (res.assign(wsig=(res.auc_within - 0.5).abs()).sort_values("wsig", ascending=False)
            .groupby("var", as_index=False).head(1).sort_values("wsig", ascending=False))
    lines = []
    for _, r in best.iterrows():
        d = "+" if r.auc_within >= 0.5 else "- (inverse)"
        fe = "forecast-eligible" if r.timing == "antecedent" else "same-week"
        g = "within-sig" if r.incl_within == "Y" else "n.s. within"
        lines.append(f"- **{r['var']}**: within AUC **{r.auc_within:.3f}** {d} (`{r.rep}`, {fe}, {g})")
    nwithin = int((res.incl_within == "Y").sum())
    md += ["", f"**{nwithin} reps pass the within-lake gate.** Per weather variable (best rep by "
           f"within-lake signal):"] + lines
    md += ["", "**Notes:** weather is a coincident/antecedent DRIVER layer (no consequence/circular "
           "issue). SPEI is already a standardized anomaly; trailing sums are levels (anomC removes "
           "seasonality). same_week reps are diagnostic; lag reps are forecast-eligible. Nearest-cell "
           "extraction (0.25deg ~28km) -- fine for lakes << cell."]
    open(OUT, "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md[:5])); print(f"... {nwithin} within-sig of {len(res)}; wrote {OUT}")


if __name__ == "__main__":
    main()
