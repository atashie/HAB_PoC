"""Experiment-suite runner: every experiment reports the FEATURE-SUITE x ARCHITECTURE grid.

Standard suites (unless an experiment explicitly tries a new one): baselines (persistence, climatology)
+ the CyAN ladder + full fusion (CyAN+static+season+weather+in-situ) + **cyan-less fusion**
(static+season+weather+in-situ = the anti-persistence model). Architectures: regularized **logistic**
(genuinely-different linear comparator; needs impute+scale+missingness-indicator -> disadvantaged on
sparse in-situ), **HistGBM** and **XGBoost** (GBDTs, native NaN; XGBoost ~ robustness check on HistGBM).

Split (date-based, ~60/20/20, 2-yr test): train < 2022-07-01; val [2022-07-01, 2024-07-01);
test >= 2024-07-01 (covers EPA's 2025-2026 window). Protocol: fit train (early stop where available),
tune threshold on VAL, refit train+val, score TEST. Metrics: canonical suite + within-lake AUC +
transition-week (flips). Climatology is a BASELINE (D-35), not a model feature.

Output: models/outputs/experiments.md
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import best_f1_threshold, classification_metrics  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
TABLE = os.path.join(DER, "modeling_table_fusion_fl.parquet")
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "experiments.md"))
SEED = 42
TRAIN_END, VAL_END = "2022-07-01", "2024-07-01"

CYAN = ["cyan_median", "cyan_mean", "cyan_sd", "cyan_median_lag1", "cyan_median_lag2",
        "cyan_median_lag4", "cyan_mean_lag1", "cyan_sd_lag1", "bloom_state", "bloom_state_ffill",
        "bloom_lag1", "bloom_roll4", "bloom_roll4_n", "cyan_gap_weeks_at_cutoff", "valid_frac"]
STATIC = ["area_sqkm", "inu_pc_umn", "tmp_dc_syr", "pet_mm_syr", "for_pc_use", "crp_pc_use", "hft_ix_u09"]
SEASON = ["woy_sin", "woy_cos"]
WEATHER = ["wx_ssrd_trail_14d_mj", "wx_ssrd_trail_30d_mj", "wx_pet_hargreaves_mm", "wx_gdd_trail_30d",
           "wx_precip_trail_30d_mm", "wx_precip_trail_90d_mm", "wx_spei_1", "wx_spei_4",
           "wx_wspd_trail_14d_mean_ms", "wx_calm_hours_trail_7d"]
INSITU = ["wqp_TP_val", "wqp_TP_stale", "wqp_water_temp_val", "wqp_ammonia_val", "wqp_orthoP_val",
          "wqp_chl_a_val", "wqp_chl_a_stale", "nwis_water_temp_val", "nwis_gage_height_val"]
DRIVERS = STATIC + SEASON + WEATHER + INSITU
SUITES = {"lean": ["cyan_median", "area_sqkm"],   # the greedy-selected 2-feature deployable model (Part 3)
          "cyan_ladder": CYAN, "fusion_full": CYAN + DRIVERS, "fusion_nocyan": DRIVERS,
          # +clim = climatology added as a FEATURE (reintroduces per-lake identity, D-35 -- experiment)
          "cyan_ladder+clim": CYAN + ["clim"], "fusion_full+clim": CYAN + DRIVERS + ["clim"],
          "fusion_nocyan+clim": DRIVERS + ["clim"]}
ARCHS = ["logistic", "histgbm", "xgboost"]


def add_clim(fit, frame):
    u = fit.drop_duplicates(["comid", "target_date"])
    lut = u.groupby(["comid", "month"])["target_bloom"].mean(); g = float(u["target_bloom"].mean())
    return frame.apply(lambda r: lut.get((r.comid, r.month), g), axis=1).to_numpy(dtype=float)


def add_features(frame, feats, fit_source):
    """feature matrix; `clim` is computed train-only from `fit_source` (leakage-safe)."""
    X = frame[[f for f in feats if f != "clim"]].copy()
    if "clim" in feats:
        X["clim"] = add_clim(fit_source, frame)
    return X


def fit_score(arch, feats, tr, va, fit, te):
    """fit train (early stop where available) -> val threshold -> refit train+val -> predict test.
    clim is train-only for the threshold model, train+val for the final model (no leakage)."""
    ytr, yva, yfit = tr["target_bloom"], va["target_bloom"], fit["target_bloom"]
    Xtr, Xva = add_features(tr, feats, tr), add_features(va, feats, tr)          # train-only clim
    Xfit, Xte = add_features(fit, feats, fit), add_features(te, feats, fit)      # train+val clim
    if arch == "logistic":
        pipe = lambda: Pipeline([("imp", SimpleImputer(strategy="median", add_indicator=True)),
                                 ("sc", StandardScaler()),
                                 ("lr", LogisticRegression(C=1.0, max_iter=3000, random_state=SEED))])
        m1 = pipe().fit(Xtr, ytr)
        thr = best_f1_threshold(yva, m1.predict_proba(Xva)[:, 1])
        return pipe().fit(Xfit, yfit).predict_proba(Xte)[:, 1], thr
    if arch == "histgbm":
        def m(): return HistGradientBoostingClassifier(random_state=SEED, max_iter=400,
                                                        learning_rate=0.06, max_leaf_nodes=31,
                                                        l2_regularization=1.0, early_stopping=True,
                                                        validation_fraction=0.1, n_iter_no_change=20)
        m1 = m().fit(Xtr, ytr)
        thr = best_f1_threshold(yva, m1.predict_proba(Xva)[:, 1])
        return m().fit(Xfit, yfit).predict_proba(Xte)[:, 1], thr
    # xgboost: early stop on val -> best_iteration; refit train+val at that n
    x1 = XGBClassifier(n_estimators=600, max_depth=6, learning_rate=0.06, subsample=0.8,
                       colsample_bytree=0.8, reg_lambda=1.0, tree_method="hist", eval_metric="logloss",
                       early_stopping_rounds=30, random_state=SEED)
    x1.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)
    best = x1.best_iteration + 1
    thr = best_f1_threshold(yva, x1.predict_proba(Xva)[:, 1])
    x2 = XGBClassifier(n_estimators=best, max_depth=6, learning_rate=0.06, subsample=0.8,
                       colsample_bytree=0.8, reg_lambda=1.0, tree_method="hist", random_state=SEED)
    x2.fit(Xfit, yfit)
    return x2.predict_proba(Xte)[:, 1], thr


def per_lake_auc(y, p, comid):
    d = pd.DataFrame({"y": y, "p": p, "c": comid})
    a = [roc_auc_score(g.y, g.p) for _, g in d.groupby("c") if g.y.nunique() == 2 and len(g) >= 20]
    return round(float(np.median(a)), 3) if a else np.nan


def row(name, y, p, comid, pers, thr):
    m = classification_metrics(y, p, thr)
    flip = (y.to_numpy() != pers)
    mf = classification_metrics(y[flip], p[flip], thr) if flip.sum() > 30 else {"MCC": np.nan, "AUC-ROC": np.nan}
    # ONSET (positive-flip): restrict to currently-CLEAR weeks (persistence==0) and score which BECOME a
    # bloom, at the same VAL-tuned threshold. Same definition as eval_headtohead_onset.py / headtohead_onset.md.
    onset = (pers == 0)
    mo = (classification_metrics(y[onset], p[onset], thr)
          if onset.sum() > 30 and y[onset].nunique() == 2 else {"MCC": np.nan, "AUC-ROC": np.nan})
    return {"config": name, "AUC-ROC": m["AUC-ROC"], "AUC-PR": m["AUC-PR"], "Brier": m["Brier"],
            "MCC": m["MCC"], "AUC_within": per_lake_auc(y.to_numpy(), p, comid.to_numpy()),
            "flip_MCC": mf["MCC"], "flip_AUC": mf["AUC-ROC"], "n_flip": int(flip.sum()),
            "onset_MCC": mo["MCC"], "onset_AUC": mo["AUC-ROC"]}


def split(df):
    td = pd.to_datetime(df["target_date"])
    return df[td < TRAIN_END], df[(td >= TRAIN_END) & (td < VAL_END)], df[td >= VAL_END]


def prep(df):
    df = df.copy(); df["month"] = pd.to_datetime(df["target_date"]).dt.month
    w = pd.to_datetime(df["target_date"]).dt.isocalendar().week.astype(int)
    df["woy_sin"], df["woy_cos"] = np.sin(2 * np.pi * w / 52.0), np.cos(2 * np.pi * w / 52.0)
    return df


def run_h(df, h, arch_list, suite_list, with_baselines=True):
    d = prep(df[(df.horizon == h) & df.persistence.notna()])
    tr, va, te = split(d); fit = pd.concat([tr, va])
    y, c, pers = te["target_bloom"], te["comid"], te["persistence"].to_numpy(float)
    out = []
    if with_baselines:
        out.append(row("persistence", y, pers, c, pers, 0.5))
        thr = best_f1_threshold(va["target_bloom"], add_clim(tr, va))
        out.append(row("climatology", y, add_clim(fit, te), c, pers, thr))
    for suite in suite_list:
        for arch in arch_list:
            p, thr = fit_score(arch, SUITES[suite], tr, va, fit, te)
            out.append(row(f"{suite} | {arch}", y, p, c, pers, thr))
    return pd.DataFrame(out)


def main() -> None:
    df = pd.read_parquet(TABLE)
    print("=== h=1 grid ===")
    g1 = run_h(df, 1, ARCHS, list(SUITES))
    print(g1.to_string(index=False))
    # horizon curve: headliners (fusion_full, fusion_nocyan, cyan_ladder) on HistGBM + baselines
    curves = []
    for h in range(5):
        gh = run_h(df, h, ["histgbm"], list(SUITES))
        gh["h"] = h; curves.append(gh)
    cur = pd.concat(curves, ignore_index=True)

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("# Experiment suite -- feature-suite x architecture grid (h=1, test = Jul2024-Jun2026)\n\n")
        fh.write("Split: train <2022-07 / val 2022-07..2024-07 / **test >=2024-07 (2 yr)**; ~60/20/20 "
                 "temporal. Threshold tuned on val; early stopping (HistGBM/XGBoost). Climatology = "
                 "BASELINE. `fusion_nocyan` = the anti-persistence model (no antecedent CyAN levels). "
                 "**`+clim` configs add per-lake climatology as a FEATURE** (reintroduces per-lake "
                 "identity, D-35 -- trades generalizability for the seasonal onset signal; experiment). "
                 "**Read AUC_within + flip_MCC** (flips = onsets/offsets, the hard case). Logistic is "
                 "disadvantaged on sparse in-situ (needs imputation); GBDTs handle NaN natively.\n\n")
        fh.write("## h=1 grid\n\n| config | AUC-ROC | AUC-PR | Brier | MCC | AUC_within | flip_MCC | flip_AUC "
                 "| n_flip | onset-MCC | onset-AUC |\n")
        fh.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for _, r in g1.iterrows():
            fh.write(f"| {r.config} | {r['AUC-ROC']:.3f} | {r['AUC-PR']:.3f} | {r.Brier:.3f} | {r.MCC:.3f} "
                     f"| {r.AUC_within:.3f} | {r.flip_MCC:.3f} | {r.flip_AUC:.3f} | {r.n_flip} "
                     f"| {r.onset_MCC:.3f} | {r.onset_AUC:.3f} |\n")
        fh.write("\n## Horizon curve h=0..4 (HistGBM; flip + onset)\n\n"
                 "| h | config | AUC-ROC | AUC_within | flip_MCC | flip_AUC | onset-MCC | onset-AUC |\n"
                 "| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for _, r in cur.iterrows():
            cfg = r.config.replace(" | histgbm", "")   # single-token config (curve is HistGBM-only) -> easy to parse
            fh.write(f"| {int(r.h)} | {cfg} | {r['AUC-ROC']:.3f} | {r.AUC_within:.3f} | "
                     f"{r.flip_MCC:.3f} | {r.flip_AUC:.3f} | {r.onset_MCC:.3f} | {r.onset_AUC:.3f} |\n")
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
