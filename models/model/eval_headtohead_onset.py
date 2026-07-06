"""Positive-flip (ONSET) head-to-head across horizons 0-4, on the shared FL 2025 EPA COMID-weeks.

Extends `eval_epa_headtohead.py` with the metric the DECISION actually needs -- ONSET (positive-flip)
skill -- and puts all five predictor classes on the SAME shared weeks so slides 15 & 17 are consistent:

  * ONSET / positive-flip = restrict to currently-CLEAR weeks (persistence == 0) and score how well each
    predictor flags the ones that BECOME a bloom next week. This is DISTINCT from the both-direction
    "transition / flip" metric (target != persistence) in `epa_headtohead.md`, which mixes onsets AND
    offsets. (Matches the `onsetAUC/onsetMCC` definition in exp_ablation.md.)
  * the FUSION model (HistGBM, all features -- Track A) alongside persistence / climatology / CyAN-ladder / EPA.
  * EPA at BOTH cutoffs (0.10 deployed / 0.50 accuracy-optimal) for operating + onset metrics.
  * horizons 0-4. EPA's probability is a fixed current-week nowcast, held constant across h (this flatters
    EPA at longer leads -- stated).

Threshold-free metrics are cutoff-independent and reproduce the `epa_headtohead.md` W-2/h1 numbers (same
ladder, same exact join) -- a built-in consistency check. Operating thresholds are in-sample F1-tuned on
the test slice (optimistic, even-handed -- same convention as epa_headtohead.md); EPA uses fixed 0.10/0.50.

Output: models/outputs/headtohead_onset.md      Run: python models/model/eval_headtohead_onset.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import best_f1_threshold, classification_metrics  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
TABLE = os.path.join(DER, "modeling_table_fusion_fl.parquet")   # extends the cyan table with fusion feats
EPA = os.path.abspath(os.path.join(HERE, "..", "..", "data-sources", "cyano-forecasts",
                                   "data", "raw", "snapshots", "allweeks_20260702T000000Z.csv"))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "headtohead_onset.md"))
SEED = 42

# CyAN autoregressive ladder = exactly eval_epa_headtohead.LADDER_FEATS (+ per-lake-month clim column)
CYAN = ["cyan_median", "cyan_mean", "cyan_sd", "cyan_median_lag1", "cyan_median_lag2", "cyan_median_lag4",
        "cyan_mean_lag1", "cyan_sd_lag1", "bloom_state", "bloom_state_ffill", "bloom_lag1",
        "bloom_roll4", "bloom_roll4_n", "cyan_gap_weeks_at_cutoff", "valid_frac"]
STATIC = ["area_sqkm", "inu_pc_umn", "tmp_dc_syr", "pet_mm_syr", "for_pc_use", "crp_pc_use", "hft_ix_u09"]
SEASON = ["woy_sin", "woy_cos"]
WEATHER = ["wx_ssrd_trail_14d_mj", "wx_ssrd_trail_30d_mj", "wx_pet_hargreaves_mm", "wx_gdd_trail_30d",
           "wx_precip_trail_30d_mm", "wx_precip_trail_90d_mm", "wx_spei_1", "wx_spei_4",
           "wx_wspd_trail_14d_mean_ms", "wx_calm_hours_trail_7d"]
INSITU = ["wqp_TP_val", "wqp_TP_stale", "wqp_water_temp_val", "wqp_ammonia_val", "wqp_orthoP_val",
          "wqp_chl_a_val", "wqp_chl_a_stale", "nwis_water_temp_val", "nwis_gage_height_val"]
TRACK_A = CYAN + STATIC + SEASON + WEATHER + INSITU


def clim_lut(fit):
    u = fit.drop_duplicates(["comid", "target_date"])
    return u.groupby(["comid", "month"])["target_bloom"].mean(), float(u["target_bloom"].mean())


def clim_scores(frame, lut, g):
    return frame.apply(lambda r: lut.get((r.comid, r.month), g), axis=1).to_numpy(float)


def ladder_pipe():
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                     ("lr", LogisticRegression(max_iter=2000, random_state=SEED))])


def gbm():
    return HistGradientBoostingClassifier(random_state=SEED, max_iter=400, learning_rate=0.06,
                                          max_leaf_nodes=31, l2_regularization=1.0, early_stopping=True,
                                          validation_fraction=0.1, n_iter_no_change=20)


def Xof(frame, feats, fit, lut, g):
    X = frame[[f for f in feats if f != "clim"]].copy()
    if "clim" in feats:
        X["clim"] = clim_scores(frame, lut, g)
    return X


def onset_metrics(y, p, thr, onset_mask):
    """Positive-flip skill: metrics on the currently-CLEAR subset (persistence==0)."""
    ys, ps = y[onset_mask], p[onset_mask]
    if len(ys) == 0 or not np.isfinite(ps).all():
        return {"AUC-ROC": np.nan, "MCC": np.nan, "Acc": np.nan, "Recall": np.nan}, 0
    m = classification_metrics(ys, ps, thr)
    return m, int((ys == 1).sum())


def main() -> None:
    df = pd.read_parquet(TABLE)
    df["month"] = pd.to_datetime(df["target_date"]).dt.month
    woy = pd.to_datetime(df["target_date"]).dt.isocalendar().week.astype(int)
    df["woy_sin"], df["woy_cos"] = np.sin(2 * np.pi * woy / 52.0), np.cos(2 * np.pi * woy / 52.0)
    df["target_end"] = pd.to_datetime(df["target_date"]) + pd.Timedelta(days=6)

    epa = pd.read_csv(EPA)
    epa = epa[epa.state == "FL"].copy()
    epa["target_end"] = pd.to_datetime(epa["week_end_date"])
    epa["epa_p"] = epa["percent_chance"] / 100.0
    epa = epa[["comid", "target_end", "epa_p"]]

    fit_all = df[df.split.isin(["train", "val"])]

    base_rows, horizon_rows = [], []
    for h in range(5):
        fit = fit_all[fit_all.horizon == h]
        lut, g = clim_lut(fit)
        te = df[(df.split == "test") & (df.horizon == h)].merge(epa, on=["comid", "target_end"], how="inner")
        te = te[te.persistence.notna()].copy()
        y = te["target_bloom"].astype(int).reset_index(drop=True)
        pers = te["persistence"].to_numpy(float)
        onset_mask = (pers == 0)

        tr, va = fit[fit.split == "train"], fit[fit.split == "val"]
        mL = ladder_pipe().fit(Xof(fit, CYAN + ["clim"], fit, lut, g), fit["target_bloom"])
        mF = gbm().fit(Xof(fit, TRACK_A, fit, lut, g), fit["target_bloom"])
        scores = {
            "persistence": pers,
            "climatology": clim_scores(te, lut, g),
            "CyAN-ladder": mL.predict_proba(Xof(te, CYAN + ["clim"], fit, lut, g))[:, 1],
            "fusion": mF.predict_proba(Xof(te, TRACK_A, fit, lut, g))[:, 1],
            "EPA": te["epa_p"].to_numpy(float),
        }
        # operating thresholds tuned on VALIDATION (never on test labels): fit thr-models on TRAIN, pick
        # the F1 threshold on VAL predictions. persistence = 0.5; EPA at fixed 0.10/0.50 below.
        mL_tr = ladder_pipe().fit(Xof(tr, CYAN + ["clim"], fit, lut, g), tr["target_bloom"])
        mF_tr = gbm().fit(Xof(tr, TRACK_A, fit, lut, g), tr["target_bloom"])
        yv = va["target_bloom"].astype(int).to_numpy()
        thr = {"persistence": 0.5,
               "climatology": best_f1_threshold(yv, clim_scores(va, lut, g)),
               "CyAN-ladder": best_f1_threshold(yv, mL_tr.predict_proba(Xof(va, CYAN + ["clim"], fit, lut, g))[:, 1]),
               "fusion": best_f1_threshold(yv, mF_tr.predict_proba(Xof(va, TRACK_A, fit, lut, g))[:, 1])}

        # horizon curve: AUC + onset-MCC for the 5 model classes (EPA at its deployed 0.10 cutoff)
        for name in ["persistence", "climatology", "CyAN-ladder", "fusion", "EPA"]:
            p = scores[name]
            t = 0.10 if name == "EPA" else thr[name]
            allm = classification_metrics(y, p, t)
            om, n_on = onset_metrics(y, p, t, onset_mask)
            horizon_rows.append({"h": h, "model": name, "AUC-ROC": allm["AUC-ROC"],
                                 "onset-MCC": om["MCC"], "onset-AUC": om["AUC-ROC"], "n_onset": n_on})

        # baselines table (h=1 only): persistence/climatology/ladder + EPA @0.10 and @0.50
        if h == 1:
            for name in ["persistence", "climatology", "CyAN-ladder"]:
                p, t = scores[name], thr[name]
                allm = classification_metrics(y, p, t)
                om, n_on = onset_metrics(y, p, t, onset_mask)
                base_rows.append({"predictor": name, "AUC-ROC": allm["AUC-ROC"], "AUC-PR": allm["AUC-PR"],
                                  "Brier": allm["Brier"], "MCC": allm["MCC"], "Acc": allm["Acc"],
                                  "onset-AUC": om["AUC-ROC"], "onset-MCC": om["MCC"], "onset-Recall": om["Recall"],
                                  "n_onset": n_on})
            for cut in (0.10, 0.50):
                p = scores["EPA"]
                allm = classification_metrics(y, p, cut)
                om, n_on = onset_metrics(y, p, cut, onset_mask)
                base_rows.append({"predictor": f"EPA @{cut:.2f}", "AUC-ROC": allm["AUC-ROC"], "AUC-PR": allm["AUC-PR"],
                                  "Brier": allm["Brier"], "MCC": allm["MCC"], "Acc": allm["Acc"],
                                  "onset-AUC": om["AUC-ROC"], "onset-MCC": om["MCC"], "onset-Recall": om["Recall"],
                                  "n_onset": n_on})
            shared_n, shared_lakes, shared_weeks, base_rate = len(te), te.comid.nunique(), te.target_end.nunique(), float(y.mean())
            n_clear = int(onset_mask.sum())

    bt = pd.DataFrame(base_rows).round(3)
    ht = pd.DataFrame(horizon_rows).round(3)

    def md(df):
        cols = list(df.columns)
        out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
        for _, r in df.iterrows():
            out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
        return "\n".join(out)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("# Positive-flip (ONSET) head-to-head -- shared FL 2025 EPA COMID-weeks, horizons 0-4\n\n")
        fh.write(f"Shared test set (h=1): **{shared_n:,} lake-weeks** ({shared_lakes} lakes x {shared_weeks} weeks); "
                 f"base rate {base_rate:.1%}; **{n_clear:,} currently-clear** weeks carry the onset test.\n\n")
        fh.write("**ONSET / positive-flip** = restrict to currently-CLEAR weeks (persistence==0); score flagging the "
                 "ones that BECOME a bloom. Distinct from the both-direction transition/flip metric (target != "
                 "persistence) in `epa_headtohead.md`. Threshold-free cols reproduce the epa_headtohead W-2/h1 "
                 "values (consistency check). Operating: F1 thresholds tuned on VALIDATION (never test) — models "
                 "fit on train, threshold picked on val — / fixed 0.10 & 0.50 (EPA). "
                 "EPA prob is a fixed current-week nowcast held constant across h (flatters EPA at longer leads).\n\n")
        fh.write("## Baselines @ h=1 (the bar to clear) -- all-sample + ONSET\n\n" + md(bt) + "\n\n")
        fh.write("## Horizon curve h=0..4 -- AUC-ROC (all weeks) + ONSET-MCC (positive flips), 5 model classes\n\n"
                 + md(ht) + "\n")
    print(bt.to_string(index=False))
    print()
    print(ht.to_string(index=False))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
