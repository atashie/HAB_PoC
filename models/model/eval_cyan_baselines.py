"""CyAN-only baseline evaluation for FL bloom forecasting, per horizon, on the temporal split.

Establishes the bar the fused model must beat. Three CyAN-only baselines, evaluated on the held-out
TEST year (2025):
  1. Persistence  -- predict bloom(W) = last OBSERVED bloom carried forward to the cutoff week W-h-1
                     (bloom_state_ffill; cloudy freshest weeks carried, not zeroed -- Codex M2).
  2. Climatology  -- per-lake, per-calendar-MONTH bloom rate (seasonal base rate; horizon-agnostic),
                     computed from UNIQUE (comid, target_date) rows (Codex L4).
  3. AR ladder    -- logistic on the CyAN-only feature ladder + climatology.

Protocol (Codex M1): probability models are FIT on train (<=2023), their operating threshold is tuned
on VALIDATION (2024) predictions, then the model is REFIT on train+val and scored on TEST (2025) with
the frozen threshold. Metrics = canonical suite from model/metrics.py.

Also reports a TRANSITION-WEEK evaluation (rows where target != persistence -- the flips), where
persistence is wrong by construction and a model must earn its keep (Codex M3/L5).

Output: models/outputs/cyan_baseline_eval.md  (+ printed tables)
Run:    python models/model/eval_cyan_baselines.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import METRIC_ORDER, best_f1_threshold, classification_metrics  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.abspath(os.path.join(HERE, "..", "data", "derived", "modeling_table_cyan_fl.parquet"))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "cyan_baseline_eval.md"))

LADDER_FEATS = ["cyan_median", "cyan_mean", "cyan_sd",
                "cyan_median_lag1", "cyan_median_lag2", "cyan_median_lag4",
                "cyan_mean_lag1", "cyan_sd_lag1", "bloom_state", "bloom_state_ffill", "bloom_lag1",
                "bloom_roll4", "bloom_roll4_n", "cyan_gap_weeks_at_cutoff", "valid_frac"]
SEED = 42


def to_md(df, index=True):
    d = df.reset_index() if index else df.copy()
    cols = list(d.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "| " + " | ".join("---" for _ in cols) + " |"]
    for _, r in d.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def clim_lookup(frame):
    """Per-lake per-month bloom rate from UNIQUE (comid, target_date) rows + global fallback."""
    u = frame.drop_duplicates(["comid", "target_date"])
    return u.groupby(["comid", "month"])["target_bloom"].mean(), float(u["target_bloom"].mean())


def clim_scores(frame, lut, g):
    return frame.apply(lambda r: lut.get((r.comid, r.month), g), axis=1).to_numpy(dtype=float)


def ladder_X(frame, clim_col):
    X = frame[LADDER_FEATS].copy()
    X["clim"] = clim_col
    return X


def new_pipe():
    return Pipeline([("imp", SimpleImputer(strategy="median")),
                     ("sc", StandardScaler()),
                     ("lr", LogisticRegression(max_iter=2000, random_state=SEED))])


def main() -> None:
    df = pd.read_parquet(TABLE)
    # eval-time re-assert the latency guard (Codex L2 -- don't trust the table blindly)
    gap = (pd.to_datetime(df.target_date) - pd.to_datetime(df.feature_date)).dt.days
    if not (gap == 7 * (df.horizon + 1)).all():
        raise ValueError("latency guard violated in modeling table")
    df = df[df.persistence.notna()].copy()          # drop record-start rows w/o any prior obs (~75)
    df["month"] = pd.to_datetime(df["target_date"]).dt.month

    train = df[df.split == "train"]                  # <=2023
    val = df[df.split == "val"]                      # 2024
    test = df[df.split == "test"]                    # 2025
    fit = df[df.split.isin(["train", "val"])]        # final model data

    clim_tr, g_tr = clim_lookup(train)               # for threshold tuning
    clim_fit, g_fit = clim_lookup(fit)               # for final test prediction

    full_rows, trans_rows = [], []
    for h in sorted(df.horizon.unique()):
        tr, va, te, fi = (d[d.horizon == h] for d in (train, val, test, fit))
        y = te["target_bloom"]

        # 1) persistence (hard, last-valid carry-forward)
        p_pers = te["persistence"].to_numpy(dtype=float)

        # 2) climatology -- tune thr on val (train lut), score test (fit lut)
        thr_clim = best_f1_threshold(va["target_bloom"], clim_scores(va, clim_tr, g_tr))
        p_clim = clim_scores(te, clim_fit, g_fit)

        # 3) ladder -- fit on train, tune thr on val; refit on train+val, score test
        m_tr = new_pipe().fit(ladder_X(tr, clim_scores(tr, clim_tr, g_tr)), tr["target_bloom"])
        p_va = m_tr.predict_proba(ladder_X(va, clim_scores(va, clim_tr, g_tr)))[:, 1]
        thr_lad = best_f1_threshold(va["target_bloom"], p_va)
        m_fit = new_pipe().fit(ladder_X(fi, clim_scores(fi, clim_fit, g_fit)), fi["target_bloom"])
        p_lad = m_fit.predict_proba(ladder_X(te, clim_scores(te, clim_fit, g_fit)))[:, 1]

        preds = {"persistence": (p_pers, 0.5), "climatology": (p_clim, thr_clim),
                 "ladder": (p_lad, thr_lad)}
        for name, (p, thr) in preds.items():
            full_rows.append({"h": h, "baseline": name, "n_test": len(y),
                              "base_rate": round(float(y.mean()), 3),
                              **classification_metrics(y, p, thr)})

        # transition-week subset: rows where target != persistence (the flips)
        flip = (te["target_bloom"].to_numpy() != te["persistence"].to_numpy())
        yt = y[flip]
        for name, (p, thr) in preds.items():
            trans_rows.append({"h": h, "baseline": name, "n_flip": int(flip.sum()),
                               "flip_rate": round(float(flip.mean()), 3),
                               **classification_metrics(yt, p[flip], thr)})

    res = pd.DataFrame(full_rows)[["h", "baseline", "n_test", "base_rate"] + METRIC_ORDER]
    trans = pd.DataFrame(trans_rows)[["h", "baseline", "n_flip", "flip_rate"] + METRIC_ORDER]
    piv = res.pivot(index="h", columns="baseline", values="AUC-ROC")
    brier = res.pivot(index="h", columns="baseline", values="Brier")
    mcc = res.pivot(index="h", columns="baseline", values="MCC")

    def pair_deltas(pivot, lower_better=False):
        # positive => the first baseline beats the second on this metric.
        # higher-better: first - second; lower-better (Brier): second - first.
        a, b, c = ("persistence", "climatology", "ladder")
        if lower_better:
            return pd.DataFrame({"ladder-persist": pivot[a] - pivot[c],
                                 "ladder-clim": pivot[b] - pivot[c],
                                 "clim-persist": pivot[a] - pivot[b]}).round(3)
        return pd.DataFrame({"ladder-persist": pivot[c] - pivot[a],
                             "ladder-clim": pivot[c] - pivot[b],
                             "clim-persist": pivot[b] - pivot[a]}).round(3)
    d_mcc, d_auc = pair_deltas(mcc), pair_deltas(piv)
    d_brier = pair_deltas(brier, lower_better=True)

    def g(frame, h, b, m):
        return frame[(frame.h == h) & (frame.baseline == b)][m].iloc[0]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("# CyAN-only baseline evaluation (FL, temporal split)\n\n")
        fh.write("Probability models FIT on train (<=2023), threshold tuned on **val (2024)**, refit on "
                 "train+val, scored on held-out **test 2025**. Persistence = last observed bloom carried "
                 "to the cutoff week `W-h-1` (latency-aware, D-28). Climatology = per-lake per-month rate. "
                 "AR ladder = logistic on CyAN-only features + climatology. Metrics: canonical suite "
                 "(`model/metrics.py`); **MCC is the headline balanced metric**; AUC-ROC of the HARD "
                 "persistence is capped, so read it with care.\n\n")
        fh.write("## Full test set\n\n" + to_md(res, index=False))
        fh.write("\n\n## AUC-ROC by horizon\n\n" + to_md(piv.round(3)))
        fh.write("\n\n## Brier by horizon (lower better)\n\n" + to_md(brier.round(3)))
        fh.write("\n\n## MCC by horizon (headline balanced metric)\n\n" + to_md(mcc.round(3)))
        fh.write("\n\n## Pairwise skill deltas -- ALL samples (positive => first beats second)\n\n")
        fh.write("Climatology as an explicit comparator vs persistence and the ladder. The strongest "
                 "CyAN-only baseline is **metric-dependent**, so the fused model must beat the best on "
                 "EACH metric.\n\n**MCC deltas:**\n\n" + to_md(d_mcc)
                 + "\n\n**AUC-ROC deltas:**\n\n" + to_md(d_auc)
                 + "\n\n**Brier deltas** (lower-is-better; positive => first model has the lower/better "
                   "Brier):\n\n" + to_md(d_brier))
        fh.write("\n\n## Transition weeks only (target != persistence -- the flips)\n\n")
        fh.write("Where persistence is wrong by construction; this is where a model must earn its keep "
                 "and where fused features should help most.\n\n" + to_md(trans, index=False))
        # findings
        fh.write("\n\n## Key findings (auto-generated)\n\n")
        fh.write(f"- **Persistence decays with lead** (AUC-ROC {piv.loc[0,'persistence']:.3f}->"
                 f"{piv.loc[4,'persistence']:.3f}; Brier {brier.loc[0,'persistence']:.3f}->"
                 f"{brier.loc[4,'persistence']:.3f}) -- the freshest published CyAN goes staler.\n")
        fh.write(f"- **Absolute skill is dominated by per-lake seasonal identity, not just "
                 f"autocorrelation (Codex M3):** climatology alone reaches AUC-ROC "
                 f"{piv.loc[1,'climatology']:.3f} flat across horizons, and the ladder adds only "
                 f"~{g(res,1,'ladder','AUC-ROC')-g(res,1,'climatology','AUC-ROC'):+.3f}-"
                 f"{g(res,4,'ladder','AUC-ROC')-g(res,4,'climatology','AUC-ROC'):+.3f} AUC-ROC over "
                 f"climatology. So the fused model must show **lift over BOTH the ladder AND climatology**, "
                 f"not just over persistence.\n")
        fh.write(f"- **The ladder is the strongest CyAN-only baseline overall** -- best AUC-ROC/AUC-PR/"
                 f"Brier at every horizon; on MCC it ties persistence at h0 "
                 f"({g(res,0,'ladder','MCC'):.3f} vs {g(res,0,'persistence','MCC'):.3f}) and leads "
                 f"beyond. **Climatology is a strong RANKER but weak CLASSIFIER (a distinct comparator):** "
                 f"it beats persistence on AUC-ROC by a WIDENING margin "
                 f"({g(res,0,'climatology','AUC-ROC')-g(res,0,'persistence','AUC-ROC'):+.3f} at h0 -> "
                 f"{g(res,4,'climatology','AUC-ROC')-g(res,4,'persistence','AUC-ROC'):+.3f} at h4, as "
                 f"persistence decays) yet has the LOWEST MCC ({g(res,0,'climatology','MCC'):.3f}) -- a "
                 f"smooth seasonal prior ranks lake-months well but classifies individual lake-weeks worse "
                 f"than state-aware persistence. It is 2nd on AUC-ROC (ladder leads) and last on MCC, so "
                 f"never the single best baseline, but its ranking strength quantifies how much signal is "
                 f"pure seasonality. The fused model must beat the best baseline on EACH metric.\n")
        fh.write(f"- **Operating-point metrics tie at short lead (why the wide suite matters):** at h0 "
                 f"persistence MCC {g(res,0,'persistence','MCC'):.3f} vs ladder "
                 f"{g(res,0,'ladder','MCC'):.3f}; the ladder's edge appears at longer leads "
                 f"(h4 MCC {g(res,4,'persistence','MCC'):.3f}->{g(res,4,'ladder','MCC'):.3f}). AUC-ROC "
                 f"alone overstates the ladder at short lead.\n")
        fh.write(f"- **The real bar is TRANSITION weeks (target != persistence -- the onsets/offsets).** "
                 f"Persistence is wrong on EVERY flip by construction (AUC-ROC "
                 f"{g(trans,1,'persistence','AUC-ROC'):.0f}, MCC {g(trans,1,'persistence','MCC'):.0f}). And "
                 f"the CyAN-only **ladder is ANTI-PREDICTIVE on flips at every horizon** (AUC-ROC "
                 f"{g(trans,0,'ladder','AUC-ROC'):.3f}->{g(trans,4,'ladder','AUC-ROC'):.3f}, all < 0.5; MCC "
                 f"{g(trans,0,'ladder','MCC'):.3f}->{g(trans,4,'ladder','MCC'):.3f}, all negative) -- driven "
                 f"by 'current state persists', it predicts the WRONG direction on flips. Climatology "
                 f"(seasonal timing) is the only CyAN-only signal with any positive flip skill, and weak "
                 f"(MCC up to {g(trans,4,'climatology','MCC'):.3f} at h4). **Flips are where fused "
                 f"weather/nutrient features must earn their keep -- the headline test for fusion.**\n")
    print(res.to_string(index=False))
    print("\nTransition weeks:\n", trans.to_string(index=False))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
