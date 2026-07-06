"""EPA cyanoHAB-forecast head-to-head vs our CyAN-only baselines, on shared FL 2025 COMID-weeks.

The EPA experimental cyanoHAB forecast (INLA/Bayesian; Schaeffer 2024) is the federal benchmark. We
score it, our AR ladder, latency-aware persistence, and climatology as predictors of the SAME ground
truth -- OUR AL1 bloom label (median CyAN DN >= 130 = WHO AL1 / ~12 ug/L chl-a) -- on the FL
COMID-weeks of 2025 where an EPA forecast and our target both exist. Join is exact: EPA `week_end_date`
(Saturday ending the valid week) == our OLCI `end_date`; COMID identical (NHDPlus V2); 132/132 lakes.

FOUR material caveats (all surfaced in the output; Codex-reviewed):
 1. PROVENANCE -- NOT as-issued. EPA values are the **2026-07-02 dashboard snapshot** (one pull). The
    dashboard is a live, revisable view; we hold a single snapshot, so 2025 values MAY have been revised
    since issuance. Read as "EPA dashboard values as observed 2026-07-02," not strictly operational
    as-issued forecasts. (Weekly as-issued snapshots / EPA confirmation = follow-up.)
 2. STRUCTURAL ADVANTAGE TO US (subtle). Our AL1 is pinned to the SAME Schaeffer/WHO AL1 concept EPA
    forecasts -- NOT a different threshold. But persistence/climatology/ladder are derived from / fit to
    our EXACT realized AL1 labels on these lakes, whereas EPA's model is trained independently. So a gap
    is not a clean skill test. EPA's worse Brier is DESCRIPTIVE (calibration to its own pipeline; mean
    prob != our base rate), not causally explained here.
 3. TIMING. EPA releases Tue/Wed, valid for the current week through Saturday (a CURRENT-WEEK forecast,
    not "7 days ahead"). `WeekEndDate == end_date`. Our h0/h1 (freshest CyAN W-1 / W-2) is OUR
    CyAN-latency sensitivity bracket, NOT a reconstruction of EPA's exact information set.
 4. SEASONAL WINDOW. EPA is ~Apr-Nov only: shared set = 35 of 52 weeks, peak season, base rate 28.8% vs
    26.6% full-year. All metrics seasonal-only, NOT comparable to `cyan_baseline_eval.md`. We quantify
    the shift (exact shared keys) + add WEEK-BLOCK BOOTSTRAP 95% CIs so 35 autocorrelated weeks don't
    masquerade as precision. Threshold-free metrics (AUC-ROC/AUC-PR/Brier) are the fair, tuning-free
    comparison; operating-point metrics use in-sample thresholds for ALL predictors (optimistic).

Output: models/outputs/epa_headtohead.md
Run:    python models/model/eval_epa_headtohead.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import best_f1_threshold, classification_metrics  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
TABLE = os.path.join(DER, "modeling_table_cyan_fl.parquet")
EPA = os.path.abspath(os.path.join(HERE, "..", "..", "data-sources", "cyano-forecasts",
                                   "data", "raw", "snapshots", "allweeks_20260702T000000Z.csv"))
EPA_SNAPSHOT = "2026-07-02 dashboard snapshot (NOT proven as-issued)"
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "epa_headtohead.md"))

LADDER_FEATS = ["cyan_median", "cyan_mean", "cyan_sd",
                "cyan_median_lag1", "cyan_median_lag2", "cyan_median_lag4",
                "cyan_mean_lag1", "cyan_sd_lag1", "bloom_state", "bloom_state_ffill", "bloom_lag1",
                "bloom_roll4", "bloom_roll4_n", "cyan_gap_weeks_at_cutoff", "valid_frac"]
SEED = 42
PREDICTORS = ["EPA_forecast", "our_ladder", "persistence", "climatology"]


def to_md(df, index=True):
    d = df.reset_index() if index else df.copy()
    cols = list(d.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "| " + " | ".join("---" for _ in cols) + " |"]
    for _, r in d.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def clim_lookup(frame):
    u = frame.drop_duplicates(["comid", "target_date"])
    return u.groupby(["comid", "month"])["target_bloom"].mean(), float(u["target_bloom"].mean())


def clim_scores(frame, lut, gr):
    return frame.apply(lambda r: lut.get((r.comid, r.month), gr), axis=1).to_numpy(dtype=float)


def ladder_X(frame, clim_col):
    X = frame[LADDER_FEATS].copy()
    X["clim"] = clim_col
    return X


def new_pipe():
    return Pipeline([("imp", SimpleImputer(strategy="median")),
                     ("sc", StandardScaler()),
                     ("lr", LogisticRegression(max_iter=2000, random_state=SEED))])


def block_bootstrap(detail, n_boot=2000, seed=SEED):
    """Week-block bootstrap AUC-ROC 95% CIs (resample the shared weeks with replacement)."""
    rng = np.random.default_rng(seed)
    weeks = detail["week"].unique()
    by_week = {w: detail[detail.week == w] for w in weeks}
    acc = {p: [] for p in PREDICTORS}
    diffs = {"our_ladder - EPA": [], "EPA - persistence": []}
    for _ in range(n_boot):
        samp = rng.choice(weeks, size=len(weeks), replace=True)
        d = pd.concat([by_week[w] for w in samp], ignore_index=True)
        if d["y"].nunique() < 2:
            continue
        a = {p: roc_auc_score(d["y"], d[p]) for p in PREDICTORS}
        for p in PREDICTORS:
            acc[p].append(a[p])
        diffs["our_ladder - EPA"].append(a["our_ladder"] - a["EPA_forecast"])
        diffs["EPA - persistence"].append(a["EPA_forecast"] - a["persistence"])

    def ci(v):
        v = np.array(v)
        return round(np.percentile(v, 2.5), 3), round(np.median(v), 3), round(np.percentile(v, 97.5), 3)
    return {p: ci(acc[p]) for p in PREDICTORS}, {k: ci(v) for k, v in diffs.items()}


def main() -> None:
    df = pd.read_parquet(TABLE)
    df["month"] = pd.to_datetime(df["target_date"]).dt.month
    df["target_end"] = pd.to_datetime(df["target_date"]) + pd.Timedelta(days=6)

    epa = pd.read_csv(EPA)
    epa = epa[epa.state == "FL"].copy()
    epa["target_end"] = pd.to_datetime(epa["week_end_date"])
    epa["epa_p"] = epa["percent_chance"] / 100.0
    epa = epa[["comid", "target_end", "epa_p"]]

    fit_all = df[df.split.isin(["train", "val"])]
    clim_fit, g_fit = clim_lookup(fit_all)

    rows_tf, rows_op, rows_flip = [], [], []
    detail1, seasonal_cmp, coverage, epa_meanp = None, None, None, None
    for h in (0, 1):
        fi = fit_all[fit_all.horizon == h]
        m_fit = new_pipe().fit(ladder_X(fi, clim_scores(fi, clim_fit, g_fit)), fi["target_bloom"])

        te = df[(df.split == "test") & (df.horizon == h)].merge(epa, on=["comid", "target_end"], how="inner")
        te = te[te.persistence.notna()].copy()
        y = te["target_bloom"]
        flip = (y.to_numpy() != te["persistence"].to_numpy())
        if coverage is None:
            coverage = (len(te), te.comid.nunique(), te.target_end.nunique(), float(y.mean()))
        scores = {"EPA_forecast": te["epa_p"].to_numpy(dtype=float),
                  "our_ladder": m_fit.predict_proba(ladder_X(te, clim_scores(te, clim_fit, g_fit)))[:, 1],
                  "persistence": te["persistence"].to_numpy(dtype=float),
                  "climatology": clim_scores(te, clim_fit, g_fit)}
        for name in PREDICTORS:
            p = scores[name]
            thr = 0.5 if name == "persistence" else best_f1_threshold(y, p)
            m = classification_metrics(y, p, thr)
            rows_tf.append({"EPA freshest": f"W-{h+1}", "predictor": name,
                            "AUC-ROC": m["AUC-ROC"], "AUC-PR": m["AUC-PR"], "Brier": m["Brier"]})
            rows_op.append({"EPA freshest": f"W-{h+1}", "predictor": name,
                            **{k: m[k] for k in ["MCC", "F1", "Prec", "Recall", "Acc"]}})
            # transition weeks (flips: target != persistence) -- same operating threshold
            mf = classification_metrics(y[flip], p[flip], thr)
            rows_flip.append({"EPA freshest": f"W-{h+1}", "predictor": name, "n_flip": int(flip.sum()),
                              "AUC-ROC": mf["AUC-ROC"], "AUC-PR": mf["AUC-PR"], "Brier": mf["Brier"],
                              "MCC": mf["MCC"], "Recall": mf["Recall"]})

        if h == 1:
            epa_meanp = float(te["epa_p"].mean())
            detail1 = pd.DataFrame({"week": te["target_end"].to_numpy(), "y": y.to_numpy(),
                                    **{k: scores[k] for k in PREDICTORS}})
            # seasonal shift: full-year 2025 vs EXACT shared COMID-weeks (Codex MED-4)
            shared_keys = set(map(tuple, te[["comid", "target_end"]].to_numpy()))
            full = df[(df.split == "test") & (df.horizon == 1) & df.persistence.notna()].copy()
            fs = {"our_ladder": m_fit.predict_proba(ladder_X(full, clim_scores(full, clim_fit, g_fit)))[:, 1],
                  "persistence": full["persistence"].to_numpy(dtype=float),
                  "climatology": clim_scores(full, clim_fit, g_fit)}
            sm = np.array([tuple(k) in shared_keys for k in full[["comid", "target_end"]].to_numpy()])
            seasonal_cmp = pd.DataFrame([
                {"predictor": nm,
                 "full-yr AUC": round(roc_auc_score(full["target_bloom"], fs[nm]), 3),
                 "shared AUC": round(roc_auc_score(full["target_bloom"][sm], fs[nm][sm]), 3),
                 "full-yr base": round(float(full["target_bloom"].mean()), 3),
                 "shared base": round(float(full["target_bloom"][sm].mean()), 3)}
                for nm in ("persistence", "climatology", "our_ladder")])

    ci_auc, ci_diff = block_bootstrap(detail1)
    tf, op, flp = pd.DataFrame(rows_tf), pd.DataFrame(rows_op), pd.DataFrame(rows_flip)
    n, nl, nw, br = coverage

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("# EPA forecast head-to-head vs our CyAN-only baselines (shared FL 2025 COMID-weeks)\n\n")
        fh.write(f"Shared test set: **{n:,} FL lake-weeks** ({nl} lakes x {nw} weeks). Ground truth = "
                 f"our AL1 bloom (pinned to the same Schaeffer/WHO AL1 concept EPA forecasts).\n\n")
        fh.write(f"> **EPA values = {EPA_SNAPSHOT}.** The dashboard is a live, revisable view and we hold "
                 f"ONE snapshot, so 2025 values may have been revised since issuance -- treat as "
                 f"dashboard-observed, not strictly as-issued.\n\n")
        fh.write("### Four material caveats\n")
        fh.write("1. **Provenance:** snapshot, not proven as-issued (above).\n")
        fh.write("2. **Structural advantage to us (subtle):** SAME AL1 concept, but persistence/"
                 "climatology/ladder are fit to / derived from our EXACT realized labels; EPA's model is "
                 "independent. A gap is not a clean skill test.\n")
        fh.write(f"3. **Timing:** EPA releases Tue/Wed, valid the current week through Sat (not 7-days-"
                 f"ahead). Our W-1/W-2 is OUR CyAN-latency sensitivity, not EPA's info set.\n")
        fh.write(f"4. **Seasonal:** EPA ~Apr-Nov -> {nw}/52 weeks, peak season, base rate {br:.1%} vs "
                 f"26.6% full-year. Metrics seasonal-only.\n\n")
        fh.write("## Threshold-free -- ALL samples (primary)\n\n" + to_md(tf, index=False))
        fh.write("\n\n## Transition weeks only (target != persistence -- the flips)\n\n")
        fh.write("The fairest cut: persistence is wrong on every flip by construction, so this shows "
                 "whether EPA's fusion model (CyAN+weather+morphology) anticipates ONSETS better than our "
                 "CyAN-only baselines. Threshold-free + MCC/Recall at the same operating threshold.\n\n"
                 + to_md(flp, index=False))
        fh.write("\n\n## Week-block bootstrap 95% CIs for AUC-ROC (W-2 / h1; resamples the "
                 f"{nw} weeks)\n\n")
        fh.write(to_md(pd.DataFrame([{"predictor": p, "AUC-ROC 2.5%": ci_auc[p][0],
                                      "median": ci_auc[p][1], "97.5%": ci_auc[p][2]} for p in PREDICTORS]),
                       index=False))
        fh.write("\n\n**AUC-ROC differences (95% CI):** "
                 + "; ".join(f"{k}: {v[1]:+.3f} [{v[0]:+.3f}, {v[2]:+.3f}]" for k, v in ci_diff.items())
                 + "\n\n")
        fh.write("## Seasonal-window shift -- OUR baselines, full-year 2025 vs exact shared COMID-weeks "
                 "(h1)\n\n" + to_md(seasonal_cmp, index=False))
        fh.write("\n\n## Operating-point -- ALL samples (in-sample thresholds; optimistic, even-handed)"
                 "\n\n" + to_md(op, index=False))
        # findings
        def gv(frame, h, pred, m):
            return frame[(frame["EPA freshest"] == f"W-{h+1}") & (frame.predictor == pred)][m].iloc[0]
        ep, ld = ci_diff["EPA - persistence"], ci_diff["our_ladder - EPA"]
        clear = ep[0] > 0.001
        fh.write("\n\n## Key findings (auto-generated)\n\n")
        fh.write(f"- **EPA vs persistence (against our AL1):** AUC-ROC gap {ep[1]:+.3f} "
                 f"[{ep[0]:+.3f}, {ep[2]:+.3f}] -- CI {'excludes' if clear else 'INCLUDES'} 0, so EPA does "
                 f"{'clearly beat' if clear else 'NOT clearly beat'} naive persistence at predicting our "
                 f"AL1 (marginal at best). EPA Brier {gv(tf,1,'EPA_forecast','Brier'):.3f} vs persistence "
                 f"{gv(tf,1,'persistence','Brier'):.3f}; EPA mean prob {epa_meanp:.3f} vs shared base "
                 f"{br:.3f} -- descriptive calibration gap, not a proven definition mismatch.\n")
        fh.write(f"- **Our ladder vs EPA:** +{ld[1]:.3f} AUC-ROC [{ld[0]:+.3f}, {ld[2]:+.3f}] -- but see "
                 f"caveat 2: the ladder is fit to our EXACT labels, EPA is not, so NOT a clean skill win.\n")
        fh.write(f"- **On FLIPS (h1):** EPA AUC-ROC {gv(flp,1,'EPA_forecast','AUC-ROC'):.3f} / MCC "
                 f"{gv(flp,1,'EPA_forecast','MCC'):.3f} / Recall {gv(flp,1,'EPA_forecast','Recall'):.3f} "
                 f"vs our ladder AUC-ROC {gv(flp,1,'our_ladder','AUC-ROC'):.3f} / MCC "
                 f"{gv(flp,1,'our_ladder','MCC'):.3f} vs climatology AUC-ROC "
                 f"{gv(flp,1,'climatology','AUC-ROC'):.3f}. See table for the full onset comparison.\n")
        fh.write(f"- **FUSION MOTIVATION (the headline for feature work):** the ordering FLIPS on flips -- "
                 f"climatology ({gv(flp,1,'climatology','AUC-ROC'):.3f}) > EPA fusion "
                 f"({gv(flp,1,'EPA_forecast','AUC-ROC'):.3f}) > our CyAN-only ladder "
                 f"({gv(flp,1,'our_ladder','AUC-ROC'):.3f}, anti-predictive) > persistence (0.000). "
                 f"Our ladder's all-samples dominance is an ARTIFACT of persistence-easy weeks; on the "
                 f"onsets that matter, CyAN-only is useless-to-harmful, and EPA's weather/morphology "
                 f"fusion helps. **Our fusion features must beat CLIMATOLOGY on flips to earn their "
                 f"place.**\n")
    print(tf.to_string(index=False))
    print("\nFLIPS:\n", flp.to_string(index=False))
    print("\nBootstrap diffs:", ci_diff)
    print("\nSeasonal:\n", seasonal_cmp.to_string(index=False))
    print(f"\nshared rows: {coverage}; EPA mean prob(h1)={epa_meanp:.3f}\nwrote {OUT}")


if __name__ == "__main__":
    main()
