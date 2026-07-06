"""Shared experiment harness: feature suites x architectures, standard reporting contract.

Every table via `run_experiment()` includes (per user + Codex/audit reconciliation, 2026-07-06):
  * **TWO EPA-forecast rows** (EPA percent_chance on shared FL test weeks) at BOTH operating points:
    **@0.50** (symmetric-loss / accuracy-optimal default for calibrated probs) and **@0.10** (EPA's
    PUBLISHED health-protective cutoff, Schaeffer 2024; deliberately over-predicts positives). Neither
    is tuned to our test. Threshold-free cols (AUC-ROC/PR/Brier/AUC_within/onsetAUC) are IDENTICAL
    across the two; only MCC/onset/offset/flipMCC differ. Caveats: seasonal shared subset, indicative
    vs full-test model rows; EPA prob is a fixed current-week nowcast held constant across h0..4
    (flatters EPA at longer leads). NOTE: our target IS EPA's own event -- median CyAN DN>=130 == WHO
    AL1, pinned verbatim from Schaeffer's deposited code, so the comparison is apples-to-apples.
  * a **valAUC-testAUC** column = in-sample(val, from the train+val REFIT) optimism vs held-out test
    -- NOT a clean val->test generalization gap (val is in-sample for the refit model),
  * **flipMCC at each horizon h=0..4** (all transitions), and at the primary horizon the **onset/offset
    decomposition** (onsetAUC/onsetMCC on the currently-CLEAR subset = the early-warning skill; offset
    on the currently-BLOOM subset) -- Codex: "flips" conflate onsets and offsets.

Procedure (D-36, standard): fit train -> threshold + early-stop on VAL -> **refit on train+val** ->
predict test. Split: train<2022-07 / val[2022-07,2024-07) / test>=2024-07 (~60/20/20, 2-yr test).

`clim` and weather ANOMALY features are train-only (leakage-safe). CHANGE features are NON-REDUNDANT
(Codex): non-overlapping recent-vs-prior weather trends + weather anomalies vs train seasonal
climatology (NOT linear combos of columns already in DRIVERS).
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import matthews_corrcoef, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from metrics import best_f1_threshold, classification_metrics  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DER = os.path.join(ROOT, "models", "data", "derived")
TABLE = os.path.join(DER, "modeling_table_fusion_fl.parquet")
EPA_CSV = os.path.join(ROOT, "data-sources", "cyano-forecasts", "data", "raw", "snapshots",
                       "allweeks_20260702T000000Z.csv")
SEED = 42
TRAIN_END, VAL_END = "2022-07-01", "2024-07-01"
HORIZONS = [0, 1, 2, 3, 4]
PRIM = 1

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
# NON-REDUNDANT change block (Codex): non-overlapping recent-vs-prior trends (in prep) +
# weather anomalies vs TRAIN seasonal climatology (train-only pseudo-features, in Xof).
ANOM = {"wx_ssrd_anom": "wx_ssrd_trail_30d_mj", "wx_precip_anom": "wx_precip_trail_30d_mm",
        "wx_gdd_anom": "wx_gdd_trail_30d"}
CHANGE = ["wx_precip_trend", "wx_solar_trend"] + list(ANOM)
PSEUDO = {"clim", *ANOM}


def load():
    return pd.read_parquet(TABLE)


def prep(df):
    df = df.copy()
    td = pd.to_datetime(df["target_date"])
    df["month"] = td.dt.month
    w = td.dt.isocalendar().week.astype(int)
    df["woy_sin"], df["woy_cos"] = np.sin(2 * np.pi * w / 52.0), np.cos(2 * np.pi * w / 52.0)
    df["target_end"] = td + pd.Timedelta(days=6)
    # non-overlapping recent-vs-strictly-prior trends (mm/day, MJ/day) -- genuinely new vs the levels
    df["wx_precip_trend"] = (df["wx_precip_trail_30d_mm"] / 30
                             - (df["wx_precip_trail_90d_mm"] - df["wx_precip_trail_30d_mm"]) / 60)
    df["wx_solar_trend"] = (df["wx_ssrd_trail_14d_mj"] / 14
                            - (df["wx_ssrd_trail_30d_mj"] - df["wx_ssrd_trail_14d_mj"]) / 16)
    return df


def split(df):
    td = pd.to_datetime(df["target_date"])
    return df[td < TRAIN_END], df[(td >= TRAIN_END) & (td < VAL_END)], df[td >= VAL_END]


def _lut(fit, col):
    u = fit.drop_duplicates(["comid", "target_date"])
    return u.groupby(["comid", "month"])[col].mean(), float(u[col].mean())


def _lookup(frame, lut, g):
    """Vectorized per-(comid,month) lookup with global fallback (fast; avoids row-wise apply)."""
    v = np.asarray(frame.set_index(["comid", "month"]).index.map(lut), dtype=float)
    v[np.isnan(v)] = g
    return v


def add_clim(fit, frame):
    lut, g = _lut(fit, "target_bloom")
    return _lookup(frame, lut, g)


def Xof(frame, feats, fit_source):
    """Feature matrix. clim + weather anomalies are train-only (fit on `fit_source`), leakage-safe."""
    X = frame[[f for f in feats if f not in PSEUDO]].copy()
    if "clim" in feats:
        X["clim"] = add_clim(fit_source, frame)
    for a in feats:
        if a in ANOM:
            lut, g = _lut(fit_source, ANOM[a])
            X[a] = frame[ANOM[a]].to_numpy() - _lookup(frame, lut, g)
    return X


def _hgb():
    return HistGradientBoostingClassifier(random_state=SEED, max_iter=400, learning_rate=0.06,
                                          max_leaf_nodes=31, l2_regularization=1.0, early_stopping=True,
                                          validation_fraction=0.1, n_iter_no_change=20)


def _lr():
    return Pipeline([("imp", SimpleImputer(strategy="median", add_indicator=True)),
                     ("sc", StandardScaler()),
                     ("lr", LogisticRegression(C=1.0, max_iter=3000, random_state=SEED))])


def fit_predict(arch, feats, tr, va, te):
    """fit train -> threshold + early-stop on VAL -> refit train+val -> predict. Returns (p_val,p_test,thr)
    from the REFIT model (val in-sample). clim/anom train-only for threshold model, train+val for refit."""
    ytr = tr["target_bloom"]; fit = pd.concat([tr, va]); yfit = fit["target_bloom"]
    Xtr, Xva_tr = Xof(tr, feats, tr), Xof(va, feats, tr)
    Xfit, Xva_f, Xte_f = Xof(fit, feats, fit), Xof(va, feats, fit), Xof(te, feats, fit)
    if arch == "logistic":
        thr = best_f1_threshold(va["target_bloom"], _lr().fit(Xtr, ytr).predict_proba(Xva_tr)[:, 1])
        m2 = _lr().fit(Xfit, yfit)
    elif arch == "histgbm":
        thr = best_f1_threshold(va["target_bloom"], _hgb().fit(Xtr, ytr).predict_proba(Xva_tr)[:, 1])
        m2 = _hgb().fit(Xfit, yfit)
    else:
        x1 = XGBClassifier(n_estimators=600, max_depth=6, learning_rate=0.06, subsample=0.8,
                           colsample_bytree=0.8, reg_lambda=1.0, tree_method="hist", eval_metric="logloss",
                           early_stopping_rounds=30, random_state=SEED)
        x1.fit(Xtr, ytr, eval_set=[(Xva_tr, va["target_bloom"])], verbose=False)
        thr = best_f1_threshold(va["target_bloom"], x1.predict_proba(Xva_tr)[:, 1])
        m2 = XGBClassifier(n_estimators=x1.best_iteration + 1, max_depth=6, learning_rate=0.06,
                           subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0, tree_method="hist",
                           random_state=SEED).fit(Xfit, yfit)
    return m2.predict_proba(Xva_f)[:, 1], m2.predict_proba(Xte_f)[:, 1], thr


def per_lake_auc(y, p, comid):
    """Median per-lake AUC (within-lake temporal discrimination) AND the # of qualifying lakes
    (both classes present, >=20 samples). The count matters: a median over few noisy per-lake AUCs
    is unstable (Codex) -- e.g. EPA's shared subset qualifies ~64 lakes with per-lake AUC spanning
    0-1, so its 0.498 is descriptive, not a strong contradiction of pooled AUC. Returns (median, n)."""
    d = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p), "c": np.asarray(comid)})
    a = [roc_auc_score(g.y, g.p) for _, g in d.groupby("c") if g.y.nunique() == 2 and len(g) >= 20]
    return (round(float(np.median(a)), 3) if a else np.nan), len(a)


def _mcc(y, p, thr):
    return round(matthews_corrcoef(y, (p >= thr).astype(int)), 3) if len(np.unique(y)) > 1 else np.nan


def transition(y, p, pers, thr):
    """flip = target!=persistence; onset = currently-clear (pers=0) -> bloom; offset = pers=1 -> clear."""
    y, p, pers = np.asarray(y), np.asarray(p), np.asarray(pers)
    out = {}
    fl = (y != pers)
    out["flip_MCC"] = _mcc(y[fl], p[fl], thr) if fl.sum() >= 30 and len(np.unique(y[fl])) > 1 else np.nan
    cl = (pers == 0)
    if cl.sum() >= 30 and len(np.unique(y[cl])) > 1:
        out["onset_AUC"] = round(roc_auc_score(y[cl], p[cl]), 3); out["onset_MCC"] = _mcc(y[cl], p[cl], thr)
    else:
        out["onset_AUC"] = out["onset_MCC"] = np.nan
    bl = (pers == 1)
    out["offset_MCC"] = _mcc(y[bl], p[bl], thr) if bl.sum() >= 30 and len(np.unique(y[bl])) > 1 else np.nan
    return out


def epa_pred():
    epa = pd.read_csv(EPA_CSV)
    epa = epa[epa.state == "FL"].copy()
    epa["target_end"] = pd.to_datetime(epa["week_end_date"])
    epa["epa_p"] = epa["percent_chance"] / 100.0
    return epa[["comid", "target_end", "epa_p"]]


def run_experiment(suites, archs, out_path, title, df=None, baselines=True):
    df = prep(load() if df is None else df)
    epa = epa_pred()
    Hs = {h: split(df[(df.horizon == h) & df.persistence.notna()]) for h in HORIZONS}
    rows = []

    def assemble(name, preds):  # preds[h] = (p_test, thr); primary metrics at PRIM
        teh = Hs[PRIM][2]; y, c, pers = teh["target_bloom"], teh["comid"], teh["persistence"].to_numpy(float)
        p, thr = preds[PRIM]
        m = classification_metrics(y, p, thr); tr_ = transition(y.to_numpy(), p, pers, thr)
        awn, awn_n = per_lake_auc(y.to_numpy(), p, c.to_numpy())
        r = {"config": name, "AUC-ROC": m["AUC-ROC"], "AUC-PR": m["AUC-PR"], "Brier": m["Brier"],
             "MCC": m["MCC"], "AUC_within": awn, "AUC_within_n": awn_n,
             "onsetAUC_h1": tr_["onset_AUC"], "onsetMCC_h1": tr_["onset_MCC"], "offsetMCC_h1": tr_["offset_MCC"]}
        for h in HORIZONS:
            th = Hs[h][2]; ph, thh = preds[h]
            r[f"flipMCC_h{h}"] = transition(th["target_bloom"].to_numpy(), ph,
                                            th["persistence"].to_numpy(float), thh)["flip_MCC"]
        return r

    if baselines:
        rows.append(assemble("persistence", {h: (Hs[h][2]["persistence"].to_numpy(float), 0.5) for h in HORIZONS}))
        cp = {}
        for h in HORIZONS:
            trh, vah, teh = Hs[h]
            cp[h] = (add_clim(trh, teh), best_f1_threshold(vah["target_bloom"], add_clim(trh, vah)))
        r = assemble("climatology", cp); r["valAUC-testAUC"] = np.nan; rows.append(r)

    for suite, feats in suites.items():
        for arch in archs:
            preds, vA = {}, None
            for h in HORIZONS:
                pv, pe, thr = fit_predict(arch, feats, *Hs[h])
                preds[h] = (pe, thr)
                if h == PRIM:
                    vA = roc_auc_score(Hs[h][1]["target_bloom"], pv)
            r = assemble(f"{suite} | {arch}", preds)
            r["valAUC-testAUC"] = round(vA - r["AUC-ROC"], 3)
            rows.append(r)

    # EPA rows: shared FL test weeks. Report BOTH operating points (user 2026-07-06):
    #   0.50 = symmetric-loss / accuracy-optimal default for calibrated probs;
    #   0.10 = EPA's PUBLISHED health-protective cutoff (Schaeffer 2024, over-predicts positives).
    # Neither is tuned to our test. Threshold-free cols identical across the two.
    emerge = {}
    for h in HORIZONS:
        me = Hs[h][2].merge(epa, on=["comid", "target_end"], how="inner")
        emerge[h] = me[me.persistence.notna()]
    for thr, lab in [(0.50, "EPA_forecast @0.50 (acc-opt)"), (0.10, "EPA_forecast @0.10 (deployed)")]:
        erow = {"config": lab}
        for h in HORIZONS:
            me = emerge[h]
            if not len(me):
                continue
            y = me["target_bloom"]; p = me["epa_p"].to_numpy(); pers = me["persistence"].to_numpy(float)
            if h == PRIM:
                m = classification_metrics(y, p, thr); tr_ = transition(y.to_numpy(), p, pers, thr)
                awn, awn_n = per_lake_auc(y.to_numpy(), p, me["comid"].to_numpy())
                erow.update({"AUC-ROC": m["AUC-ROC"], "AUC-PR": m["AUC-PR"], "Brier": m["Brier"],
                             "MCC": m["MCC"], "AUC_within": awn, "AUC_within_n": awn_n,
                             "onsetAUC_h1": tr_["onset_AUC"], "onsetMCC_h1": tr_["onset_MCC"],
                             "offsetMCC_h1": tr_["offset_MCC"], "n_shared": int(len(me))})
            erow[f"flipMCC_h{h}"] = transition(y.to_numpy(), p, pers, thr)["flip_MCC"]
        rows.append(erow)

    res = pd.DataFrame(rows)
    cols = (["config", "AUC-ROC", "AUC-PR", "Brier", "MCC", "AUC_within", "AUC_within_n", "valAUC-testAUC"]
            + [f"flipMCC_h{h}" for h in HORIZONS] + ["onsetAUC_h1", "onsetMCC_h1", "offsetMCC_h1", "n_shared"])
    res = res.reindex(columns=cols)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(f"# {title}\n\n")
        fh.write("Split train<2022-07 / val[2022-07,2024-07) / **test>=2024-07** (~60/20/20, 2yr); "
                 "fit train, threshold+early-stop on val, **refit train+val**, predict test. "
                 "`valAUC-testAUC` = in-sample(val, from the refit) minus held-out(test) -- an optimism "
                 "gap, NOT a clean val->test generalization gap. `AUC_within` = median per-lake AUC "
                 "(within-lake temporal skill); `AUC_within_n` = # qualifying lakes (small n => unstable). "
                 "`flipMCC_h0..4` = all transitions per lead. **onsetAUC/onsetMCC_h1 = the EARLY-WARNING "
                 "skill** (among currently-CLEAR lake-weeks, predict bloom next); offsetMCC = pers=1->clear. "
                 "**EPA rows: shared FL test weeks, at BOTH @0.50 (acc-opt default) and @0.10 (EPA's "
                 "published health-protective cutoff); threshold-free cols identical across the two; "
                 "indicative** vs full-test rows (n_shared) -- strict head-to-head in `epa_headtohead.md`. "
                 "Our target IS EPA's own event (median CyAN DN>=130 == WHO AL1, pinned from Schaeffer's "
                 "deposited code) -> apples-to-apples. EPA prob is a fixed current-week nowcast held "
                 "constant across h0..4 (flatters EPA at longer leads).\n\n")
        fh.write("| " + " | ".join(cols) + " |\n| " + " | ".join(["---"] * len(cols)) + " |\n")
        for _, r in res.iterrows():
            fh.write("| " + " | ".join(
                (f"{r[c]:.3f}" if isinstance(r[c], float) and r[c] == r[c]
                 else ("" if (isinstance(r[c], float) and r[c] != r[c]) else str(r[c]))) for c in cols) + " |\n")
    print(res.to_string(index=False)); print("wrote", out_path)
    return res
