"""Significance screening: STATIC per-lake features (area + BasinATLAS L12) vs HAB.

Honest unit of analysis = the LAKE (n=132), NOT the lake-week: static features are constant within a
lake, so testing across ~70k lake-weeks would be pseudoreplication (effective n = # lakes). We test
each feature against per-lake bloom PREVALENCE with a Spearman rank correlation (robust, monotone),
Benjamini-Hochberg FDR across the feature set, and report the lake-week univariate AUC only as a
DESCRIPTIVE between-lake effect size (not a significance test).

Depth is NOT included -- no per-lake depth source on disk (HydroLAKES needed); flagged, not faked.

Output: models/outputs/feature_significance_static.md
Run:    python models/model/assess_static_features.py
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
TARGET = os.path.join(DER, "cyan_lake_weekly_fl.parquet")
STATIC = os.path.join(DER, "lake_basinatlas_l12.parquet")
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "feature_significance_static.md"))

# human-readable labels for the curated attrs
LABELS = {
    "AREASQKM": "lake surface area", "lkv_mc_usu": "upstream lake volume (depth proxy)",
    "crp_pc_use": "cropland % (upstream)", "pst_pc_use": "pasture % (upstream)",
    "for_pc_use": "forest % (upstream)", "urb_pc_use": "urban % (upstream)",
    "ire_pc_use": "irrigated % (upstream)", "wet_pc_ug1": "wetland %",
    "ppd_pk_uav": "pop. density (upstream)", "hft_ix_u09": "human footprint 2009",
    "nli_ix_uav": "night lights", "gdp_ud_usu": "GDP (upstream)", "pop_ct_usu": "population (upstream)",
    "tmp_dc_syr": "air temp (annual, x10C)", "pre_mm_syr": "precip (annual mm)",
    "pet_mm_syr": "PET (annual mm)", "ari_ix_sav": "aridity index", "cmi_ix_syr": "moisture index",
    "swc_pc_syr": "soil water %", "ele_mt_uav": "elevation (m, upstream)",
    "slp_dg_uav": "slope (deg, upstream)", "run_mm_syr": "runoff (mm)",
    "lka_pc_use": "lake area % (upstream)", "dor_pc_pva": "degree of regulation",
    "gwt_cm_sav": "groundwater table depth", "inu_pc_umn": "inundation % (min)",
    "kar_pc_use": "karst % (upstream)", "ria_ha_usu": "river area (ha, upstream)",
    "soc_th_uav": "soil organic C", "cly_pc_uav": "clay %", "snd_pc_uav": "sand %",
    "slt_pc_uav": "silt %", "ero_kh_uav": "soil erosion",
}


def bh_fdr(p):
    p = np.asarray(p, dtype=float)
    n = len(p)
    order = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        idx = order[i]
        prev = min(prev, p[idx] * n / (i + 1))
        q[idx] = prev
    return q


def main() -> None:
    tgt = pd.read_parquet(TARGET)
    prev = (tgt.dropna(subset=["bloom"]).groupby("comid")
            .agg(prevalence=("bloom", "mean"), n_weeks=("bloom", "size")).reset_index())
    st = pd.read_parquet(STATIC).rename(columns={"COMID": "comid"})
    feat_cols = [c for c in st.columns if c in LABELS]
    lw = tgt.dropna(subset=["bloom"]).merge(st, left_on="comid", right_on="comid", how="left")
    lw["bloom"] = lw["bloom"].astype(int)

    df = prev.merge(st, on="comid", how="left")
    rows = []
    for c in feat_cols:
        d = df[["prevalence", c]].dropna()
        if d[c].nunique() < 3:
            continue
        rho, p = spearmanr(d[c], d["prevalence"])
        # descriptive between-lake effect size: univariate lake-week AUC (pseudoreplicated -> descriptive)
        s = lw[[c, "bloom"]].dropna()
        auc = roc_auc_score(s["bloom"], s[c]) if s["bloom"].nunique() > 1 else np.nan
        rows.append({"feature": c, "label": LABELS.get(c, c), "n_lakes": len(d),
                     "spearman_rho": round(rho, 3), "p": p, "AUC_lakeweek": round(auc, 3)})
    res = pd.DataFrame(rows)
    res["q_bh"] = bh_fdr(res["p"].values).round(4)
    res["include"] = np.where(res["p"] < 0.1, "YES", "")   # permissive INCLUSION screen (p<0.1, user)
    res["fdr"] = np.where(res["q_bh"] < 0.05, "*", "")      # survives Benjamini-Hochberg FDR
    res["p"] = res["p"].round(4)
    res = res.reindex(res.spearman_rho.abs().sort_values(ascending=False).index).reset_index(drop=True)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wk_min, wk_med = int(prev.n_weeks.min()), int(prev.n_weeks.median())
    md = ["# Static feature significance vs HAB (per-lake, n=132)", "",
          "Unit = LAKE (static features are per-lake; lake-week testing = pseudoreplication). Test = "
          "**Spearman**(feature, per-lake bloom prevalence) -- rank-based, so robust to the skewed, "
          f"[0,1]-bounded prevalence. Every lake has ample weeks (min {wk_min}, median {wk_med} valid "
          "weeks), so prevalence is well-estimated and unweighted Spearman is appropriate (weighting "
          "barely moves rho). **Inclusion screen = raw p<0.1** (permissive; select candidates, narrow "
          "to top-N later) -- NOT a significance claim. **q(BH)** = Benjamini-Hochberg FDR (honest "
          "multiple-comparison context; `*` = survives q<0.05). ",
          "",
          "**Feature extent (BasinATLAS):** lakes are assigned to their **max-overlap L12 sub-basin**; "
          "attributes mix extents by design -- climate/soil/morphology use the **local sub-basin** "
          "(`_s*`), while land-use / anthropogenic **loading** proxies use the **upstream catchment** "
          "(`_u*`, the hydrologically correct extent for what reaches the lake). So this is a "
          "*containing-L12 + upstream-context* screen, not strictly local. `AUC_lakeweek` is a "
          "DESCRIPTIVE between-lake effect size (repeated-week; **<0.5 = inverse association**, per the "
          "rho sign) -- not a significance test. **True per-lake depth omitted** (needs HydroLAKES); "
          "`lkv_mc_usu` is a crude upstream-lake-volume morphology proxy, not lake depth.",
          "", "| feature | meaning | n | Spearman rho | p | q(BH) | incl(p<.1) | FDR | AUC(desc) |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for _, r in res.iterrows():
        md.append(f"| `{r.feature}` | {r.label} | {r.n_lakes} | {r.spearman_rho:+.3f} | {r.p:.4f} | "
                  f"{r.q_bh:.4f} | {r.include} | {r.fdr} | {r.AUC_lakeweek:.3f} |")
    ninc = int((res.include == "YES").sum())
    nfdr = int((res.fdr == "*").sum())
    md += ["", f"**{ninc} of {len(res)} static features pass the p<0.1 inclusion screen** (candidate "
           f"set for modeling); **{nfdr} survive FDR q<0.05**. "
           f"Area (`AREASQKM`): rho={res[res.feature=='AREASQKM'].spearman_rho.iloc[0]:+.3f}, "
           f"p={res[res.feature=='AREASQKM'].p.iloc[0]:.4f} -> included; q={res[res.feature=='AREASQKM'].q_bh.iloc[0]:.3f} "
           f"(does not survive FDR)."]
    open(OUT, "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
