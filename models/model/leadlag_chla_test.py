"""Does WQP in-situ chl-a LEAD the CyAN bloom (genuine early warning), or is it just shared persistence?

The test that isolates LEAD from persistence: restrict to lake-weeks where CyAN is currently NOT
blooming at the cutoff (bloom(W-h)=0), then ask whether antecedent WQP chl-a as-of W-h predicts a CyAN
bloom h weeks later (bloom(W)=1). If AUC>0.5 there, in-situ chl-a saw biomass BEFORE CyAN's lake-median
crossed threshold -> real lead. We compare against CyAN's own sub-threshold median value at W-h (does
the satellite's own rising-but-not-yet-blooming signal lead too?).

WQP chl-a is sparse (~monthly), so we use the freshest chl-a on/before W-h (staleness-aware, <=8 wk).
Reported per horizon with within-lake median AUC (removes between-lake baseline).
Output: printed + models/outputs/chla_leadlag.md
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
WQP = os.path.abspath(os.path.join(DER, "..", "interim", "wqp_fl"))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "chla_leadlag.md"))
MAX_STALE = 8


def within_auc(d, fcol):
    a = [roc_auc_score(g["bloom"], g[fcol]) for _, g in d.groupby("comid")
         if g["bloom"].nunique() == 2 and len(g) >= 20]
    return (float(np.median(a)) if a else np.nan), len(a)


def main() -> None:
    tgt = pd.read_parquet(os.path.join(DER, "cyan_lake_weekly_fl.parquet")).dropna(subset=["bloom"])
    tgt = tgt[["comid", "start_date", "bloom", "cyan_median"]].copy()
    tgt["week"] = pd.to_datetime(tgt["start_date"])
    tgt["bloom"] = tgt["bloom"].astype(int)

    # WQP chl-a -> per-(comid, week) weekly median (direct sites; else watershed)
    v = pd.read_parquet(os.path.join(WQP, "daily_values.parquet"))
    v = v[v.parameter_code == "chl_a"]
    link = pd.read_parquet(os.path.join(WQP, "site_linkage.parquet"))
    link["comid"] = pd.to_numeric(link["comid"], errors="coerce")
    link["hybas_id"] = pd.to_numeric(link["hybas_id"], errors="coerce")
    l12 = pd.read_parquet(os.path.join(DER, "lake_basinatlas_l12.parquet"))[["COMID", "HYBAS_ID"]]
    l12["HYBAS_ID"] = pd.to_numeric(l12["HYBAS_ID"], errors="coerce")
    direct = link[link.tier == "direct"][["site_id", "comid"]].dropna()
    ws = link[link.tier == "watershed"][["site_id", "hybas_id"]].dropna().merge(
        l12, left_on="hybas_id", right_on="HYBAS_ID").rename(columns={"COMID": "comid"})[["site_id", "comid"]]
    ws = ws[~ws.comid.isin(set(direct.comid))]
    ls = pd.concat([direct, ws], ignore_index=True)
    vv = v.merge(ls, on="site_id")
    vv["date"] = pd.to_datetime(vv["date"])
    dow = vv["date"].dt.dayofweek
    vv["week"] = vv["date"] - pd.to_timedelta((dow + 1) % 7, unit="D")
    chla = vv.groupby(["comid", "week"])["value"].median().reset_index().rename(columns={"value": "chla"})

    df = tgt.merge(chla, on=["comid", "week"], how="left").sort_values(["comid", "week"])
    rows = []
    for comid, g in df.groupby("comid"):
        g = g.sort_values("week").copy()
        # staleness-aware freshest chl-a on/before each week
        g["chla_ff"] = g["chla"].ffill()
        last_wk = g["week"].where(g["chla"].notna()).ffill()
        g["stale"] = ((g["week"] - last_wk).dt.days / 7).round()
        rows.append(g)
    df = pd.concat(rows, ignore_index=True)

    md = ["# Does WQP chl-a LEAD CyAN? (isolating lead from shared persistence)", "",
          "Test: restrict to weeks where **CyAN is NOT blooming at the cutoff** (`bloom(W-h)=0`), then "
          "measure whether antecedent in-situ chl-a (freshest on/before W-h, staleness<=8wk) predicts a "
          "CyAN bloom h weeks later. AUC>0.5 there = genuine lead (chl-a saw it before CyAN). Within-lake "
          "median AUC. Compared to CyAN's own sub-threshold median at W-h.", "",
          "| h (wk) | n lake-wks | n lakes | chl-a AUC_within | CyAN-median AUC_within | onset rate |",
          "| --- | --- | --- | --- | --- | --- |"]
    print("horizon | n | lakes | chla_AUC_within | cyan_AUC_within | onset_rate")
    for h in (1, 2, 3, 4):
        g = df.groupby("comid", group_keys=False).apply(
            lambda x: x.assign(bloom_cut=x["bloom"].shift(h), cyan_cut=x["cyan_median"].shift(h),
                               chla_cut=x["chla_ff"].shift(h), stale_cut=x["stale"].shift(h)))
        d = g[(g.bloom_cut == 0) & g.chla_cut.notna() & (g.stale_cut <= MAX_STALE)
              & g.cyan_cut.notna()].copy()
        if len(d) < 50:
            md.append(f"| {h} | {len(d)} | - | (too few) | | |"); continue
        ca, nl = within_auc(d, "chla_cut")
        cy, _ = within_auc(d, "cyan_cut")
        onset = d["bloom"].mean()
        md.append(f"| {h} | {len(d):,} | {nl} | {ca:.3f} | {cy:.3f} | {onset:.3f} |")
        print(f"  {h}    | {len(d):,} | {nl} | {ca:.3f} | {cy:.3f} | {onset:.3f}")

    md += ["", "**Reading:** if chl-a AUC_within > 0.5 (and > CyAN-median's), in-situ chl-a carries "
           "early-warning signal the satellite's own sub-threshold value does not -- quantifying the "
           "lead. If ~0.5 or <= CyAN, the apparent lag skill was shared persistence, not independent "
           "lead. Caveat: WQP chl-a ~monthly (staleness up to 8wk), so lead resolution is coarse; "
           "coincident chl-a remains redundant with the CyAN-defined target (D-15)."]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(md))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
