"""Build temporal in-situ features (coincident / aggregated / lagged) and screen each vs HAB.

Source-agnostic (NWIS + WQP). Codex-reconciled screen:
  * VARIABLE CLASS -- `driver` (candidate cause) vs `consequence` (bloom raises turbidity, lowers
    Secchi, raises DO; microcystin is bloom-produced) vs `circular` (WQP chl_a: our AL1 target is
    chl-a-defined). Consequence/circular features are association diagnostics, NOT driver/forecast
    evidence. NOTE (empirical, `chla_leadlag.md`): LAGGED chl-a still carries real independent LEAD
    (AUC ~0.6 conditioned on CyAN-clear) -- weaker than CyAN's own antecedent CI; kept, flagged.
  * TIMING -- `antecedent` reps (lag1/2/4: strictly <= W-1, forecast-eligible) vs `same_week` reps
    (coincident + aggregates that use week W: diagnostic association only, NOT forecast skill).
  * TWO significance gates -- pooled lake-block bootstrap AUC (`incl_assoc`, between+within) AND a
    WITHIN-lake bootstrap of the median per-lake AUC (`incl_within`, the honest temporal test; catches
    within-only signals like TP that pooled misses, and demotes datum/size between-lake artifacts).
  * Fixes: `anomR` baseline is PAST-only (excludes W); `anomC` uses leave-one-out per-lake-month
    climatology; `sum4` only for FLUX variables (discharge) -- a concentration rolling-sum is a
    sampling-frequency artifact.

Output: models/outputs/feature_significance_<source>.md
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
TARGET = os.path.join(DER, "cyan_lake_weekly_fl.parquet")
L12MAP = os.path.join(DER, "lake_basinatlas_l12.parquet")
SEED = 42
NWIS_LABELS = {"00060": "discharge", "00065": "gage_height", "00010": "water_temp"}
# variable class (Codex): what the association can mean
CLASS = {"chl_a": "circular", "turbidity": "consequence", "secchi": "consequence",
         "DO": "consequence", "microcystin": "consequence"}   # default -> "driver"
FLUX_VARS = {"discharge"}                                        # sum4 only meaningful for flux
ANTECEDENT = {"lag1", "lag2", "lag4"}                            # strictly <= W-1 (forecast-eligible)


def bh_fdr(p):
    p = np.asarray(p, dtype=float); n = len(p); order = np.argsort(p)
    q = np.empty(n); prev = 1.0
    for i in range(n - 1, -1, -1):
        idx = order[i]; prev = min(prev, p[idx] * n / (i + 1)); q[idx] = prev
    return q


def lake_week_series(vals, link, labels):
    link = link.copy()
    link["comid"] = pd.to_numeric(link["comid"], errors="coerce")
    link["hybas_id"] = pd.to_numeric(link["hybas_id"], errors="coerce")
    l12 = pd.read_parquet(L12MAP)[["COMID", "HYBAS_ID"]].rename(columns={"COMID": "comid"})
    l12["HYBAS_ID"] = pd.to_numeric(l12["HYBAS_ID"], errors="coerce")
    direct = link[link.tier == "direct"][["site_id", "comid"]].dropna()
    ws = link[link.tier == "watershed"][["site_id", "hybas_id"]].dropna()
    ws_lakes = l12.merge(ws, left_on="HYBAS_ID", right_on="hybas_id")[["comid", "site_id"]]
    ws_lakes = ws_lakes[~ws_lakes.comid.isin(set(direct.comid.unique()))]   # direct suppresses watershed
    lake_site = pd.concat([direct[["comid", "site_id"]], ws_lakes], ignore_index=True).dropna()
    v = vals.merge(lake_site, on="site_id")
    v["date"] = pd.to_datetime(v["date"])
    dow = v["date"].dt.dayofweek
    v["week_start"] = v["date"] - pd.to_timedelta((dow + 1) % 7, unit="D")
    wk = v.groupby(["comid", "parameter_code", "week_start"])["value"].median().reset_index()
    wk["variable"] = wk["parameter_code"].map(labels).fillna(wk["parameter_code"])
    return wk


def build_features(wk, weeks_index):
    out = []
    for (comid, var), g in wk.groupby(["comid", "variable"]):
        s = g.set_index("week_start")["value"].reindex(weeks_index)
        f = pd.DataFrame(index=weeks_index)
        f["coin"] = s
        f["lag1"], f["lag2"], f["lag4"] = s.shift(1), s.shift(2), s.shift(4)
        f["mean4"] = s.rolling(4, min_periods=1).mean()
        f["mean12"] = s.rolling(12, min_periods=2).mean()
        f["sum4"] = s.rolling(4, min_periods=1).sum() if var in FLUX_VARS else np.nan
        f["delta4"] = s - s.shift(4)
        f["anomR"] = s - s.shift(1).rolling(12, min_periods=3).mean()      # baseline = PAST only
        mon = s.index.month
        gs, gc = s.groupby(mon).transform("sum"), s.groupby(mon).transform("count")
        f["anomC"] = s - (gs - s) / (gc - 1)                               # leave-one-out climatology
        f["comid"], f["variable"], f["week_start"] = comid, var, weeks_index
        out.append(f.reset_index(drop=True))
    long = pd.concat(out, ignore_index=True)
    reps = ["coin", "lag1", "lag2", "lag4", "mean4", "mean12", "sum4", "delta4", "anomR", "anomC"]
    wide = long.pivot_table(index=["comid", "week_start"], columns="variable", values=reps)
    wide.columns = [f"{var}__{rep}" for rep, var in wide.columns]
    return wide.reset_index()


def boot_stats(d, feat, n_pool=500, n_within=2000, seed=SEED):
    """One pass -> pooled AUC (between+within) and WITHIN-lake median-AUC, each with 95% CI + a
    two-sided bootstrap p vs 0.5. Per-lake AUCs are precomputed (cheap within resampling)."""
    rng = np.random.default_rng(seed)
    lakes = d["comid"].unique()
    by = {lk: d[d.comid == lk] for lk in lakes}
    lake_auc = {lk: roc_auc_score(g["bloom"], g[feat]) for lk, g in by.items()
                if g["bloom"].nunique() == 2 and len(g) >= 20}
    obs_pool = roc_auc_score(d["bloom"], d[feat])
    wl = list(lake_auc)
    obs_within = float(np.median([lake_auc[l] for l in wl])) if wl else np.nan
    pool_b, within_b = [], []
    for _ in range(n_pool):
        samp = rng.choice(lakes, size=len(lakes), replace=True)
        b = pd.concat([by[lk] for lk in samp], ignore_index=True)
        if b["bloom"].nunique() > 1:
            pool_b.append(roc_auc_score(b["bloom"], b[feat]))
    if wl:
        for _ in range(n_within):
            ws = rng.choice(wl, size=len(wl), replace=True)
            within_b.append(np.median([lake_auc[l] for l in ws]))

    def ci_p(arr, obs):
        if not len(arr) or obs != obs:
            return (np.nan, np.nan, np.nan)
        a = np.array(arr)
        p = 2 * min((a <= 0.5).mean(), (a >= 0.5).mean())
        return round(np.percentile(a, 2.5), 3), round(np.percentile(a, 97.5), 3), min(p, 1.0)
    plo, phi, pp = ci_p(pool_b, obs_pool)
    wlo, whi, wp = ci_p(within_b, obs_within)
    return dict(auc_pool=round(obs_pool, 3), pool_lo=plo, pool_hi=phi, pool_p=pp,
                auc_within=round(obs_within, 3) if obs_within == obs_within else np.nan,
                n_wl=len(wl), within_lo=wlo, within_hi=whi, within_p=wp)


def screen(source, interim_dir, labels):
    tgt = pd.read_parquet(TARGET).dropna(subset=["bloom"]).copy()
    tgt["bloom"] = tgt["bloom"].astype(int)
    tgt["week_start"] = pd.to_datetime(tgt["start_date"])
    weeks_index = pd.Index(sorted(tgt["week_start"].unique()), name="week_start")
    vals = pd.read_parquet(os.path.join(interim_dir, "daily_values.parquet"))
    link = pd.read_parquet(os.path.join(interim_dir, "site_linkage.parquet"))
    feats = build_features(lake_week_series(vals, link, labels), weeks_index)
    df = tgt[["comid", "week_start", "bloom"]].merge(feats, on=["comid", "week_start"], how="left")

    rows = []
    for c in [c for c in df.columns if "__" in c]:
        d = df[["comid", "bloom", c]].dropna()
        if d["comid"].nunique() < 5 or d["bloom"].nunique() < 2 or len(d) < 50:
            continue
        var, rep = c.split("__")
        st = boot_stats(d, c)
        rows.append({"feature": c, "var": var, "rep": rep,
                     "class": CLASS.get(var, "driver"),
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
    out = os.path.abspath(os.path.join(HERE, "..", "outputs", f"feature_significance_{source}.md"))
    md = [f"# {source.upper()} temporal feature significance vs HAB (Codex-reconciled)", "",
          f"Coverage: **{ncov}/133 lakes** (direct in-lake+250m or containing-L12 watershed). Reps: "
          "coincident, lag1/2/4, mean/sum(4/12wk), delta4, anomR(vs past), anomC(LOO climatology).",
          "",
          "**class**: driver (candidate cause) | **consequence** (bloom raises turbidity/DO, lowers "
          "Secchi) | **circular** (WQP chl_a = target proxy). **timing**: antecedent (lag1/2/4, "
          "forecast-eligible) | same_week (diagnostic association only). **Read `AUC_within`** (median "
          "per-lake AUC; removes datum/size between-lake artifacts; <0.5 = inverse). `incl_within` = "
          "within-lake bootstrap p<0.1 & |AUC_within-0.5|>=0.05; `incl_assoc` = pooled p<0.1.", "",
          "| feature | class | timing | n_lk | n_lw | AUC_pool | AUC_within (n) | within_p | incl_within | incl_assoc |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for _, r in res.iterrows():
        wl = f"{r.auc_within:.3f} ({int(r.n_wl)})" if r.auc_within == r.auc_within else "n/a"
        wp = f"{r.within_p:.3f}" if r.within_p == r.within_p else "n/a"
        md.append(f"| `{r.feature}` | {r['class']} | {r.timing} | {r.n_lakes} | {r.n_lw} | "
                  f"{r.auc_pool:.3f} | {wl} | {wp} | {r.incl_within} | {r.incl_assoc} |")

    # per-variable summary among DRIVER-class features, best rep by within signal
    drv = res[res["class"] == "driver"].assign(wsig=(res["auc_within"] - 0.5).abs())
    best = drv.sort_values("wsig", ascending=False).groupby("var", as_index=False).head(1) \
              .sort_values("wsig", ascending=False)
    lines = []
    for _, r in best.iterrows():
        d = "+" if r.auc_within >= 0.5 else "- (inverse)"
        fe = "forecast-eligible" if r.timing == "antecedent" else "same-week"
        g = "within-sig" if r.incl_within == "Y" else "n.s. within"
        lines.append(f"- **{r['var']}**: within AUC **{r.auc_within:.3f}** {d} (`{r.rep}`, {fe}, "
                     f"{int(r.n_wl)} lakes; {g})")
    nwithin = int((res.incl_within == "Y").sum())
    md += ["", f"**{nwithin} reps pass the within-lake gate.** DRIVER-class variables (best rep by "
           f"within-lake signal):"] + lines
    md += ["", "**Caveats (Codex):** (1) **chl_a is CIRCULAR** (target proxy) -- coincident excluded "
           "from driver claims; lagged chl-a is a real but modest INDEPENDENT lead (`chla_leadlag.md`), "
           "weaker than CyAN's own antecedent CI. (2) **turbidity/Secchi/DO are CONSEQUENCES** -- "
           "coincident forms are bloom impacts, not causes. (3) **WQP values NOT unit/fraction-"
           "harmonized** (mixes total/dissolved P, chl-a methods) -- nutrient signals are indicative "
           "only; harmonize before modeling. (4) **TN & pH grossly undercounted** by characteristic-"
           "name misses (need alias/pCode discovery). (5) same_week reps are DIAGNOSTIC, not forecast "
           "skill; only antecedent (lag) reps are forecast-eligible. (6) coverage/linkage: direct tier "
           "suppresses watershed; a few sites fall in >1 lake buffer (kept first) -- minor. (7) WQP "
           "chl-a ~monthly (sparse)."]
    open(out, "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md[:6])); print(f"... {nwithin} within-sig; wrote {out}")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "nwis"
    cfg = {"nwis": (os.path.join(DER, "..", "interim", "nwis_fl"), NWIS_LABELS),
           "wqp": (os.path.join(DER, "..", "interim", "wqp_fl"), {})}
    d, labels = cfg[src]
    screen(src, os.path.abspath(d), labels)
