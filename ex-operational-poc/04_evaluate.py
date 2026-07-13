"""Step 4 - ASSESS.  Score the held-out TEST period and, per the claim gate, always
beside baselines and with an uncertainty.

Model = the deployed HistGBM boosters from 03_train (refit on train+val), one per horizon.

Baselines (every horizon, every metric):
  * persistence  = the latency-aware label carried from the feature week (a stiff,
    honest yardstick because bloom state is strongly autocorrelated).
  * climatology  = per-(lake, week-of-year) bloom rate; alert threshold tuned on val (from
    a train-only fit), then refit on TRAIN+VAL for test scoring - the same fair fit the lean
    model uses (03_train refits on train+val), so the comparison is apples-to-apples.

Four metric families, each with its baselines:
  A. all-sample AUC-ROC   - overall ranking; autocorrelation-inflated, NOT the result.
  B. onset-AUC            - currently-clear lakes only; THE decision-relevant ranking metric.
  C. MCC @ val-tuned thr  - a balanced all-sample operating-point score.
  D. onset-MCC @ val thr  - the thresholded early-warning alert the deck headlines.
95% CIs are block-bootstrapped by lake (never by row). Both the lean model AND the
climatology baseline carry CIs on the onset-AUC metric, since that comparison is load-bearing.

Output: outputs/eval_metrics.md

Run:  python 04_evaluate.py
"""
import json
import numpy as np
import pandas as pd

import config
import common


def _f(v):
    return "n/a" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.3f}"


def _ci(lo, hi):
    return f"[{_f(lo)}, {_f(hi)}]"


def main():
    panel = pd.read_parquet(config.LAKE_WEEK_PARQUET)
    tuned = json.loads((config.OUTPUTS / "models.json").read_text(encoding="utf-8"))["horizons"]

    rows = []  # per-horizon computed numbers
    for h in config.HORIZONS:
        meta = tuned[str(h)]
        thr = meta["threshold"]
        model = common.load_model(config.MODEL_DIR / f"hgb_h{h}.joblib")
        frame = common.build_horizon_frame(panel, h)
        tr, va, te = common.temporal_split(frame, config.TRAIN_END, config.VAL_END)
        y = te[config.TARGET].to_numpy(int)
        per = te["persistence"].to_numpy(int)
        g = te["comid"].to_numpy()

        # lean HistGBM (val-tuned threshold from 03_train)
        p_lean = common.hgb_score(model, te[config.FEATURES].to_numpy())
        # climatology mirrors the lean model's fair fit: threshold tuned on val (train-only
        # rate), then refit on train+val for test scoring.
        lut_tr, gl_tr = common.climatology_lookup(tr)
        clim_thr = common.best_f1_threshold(va[config.TARGET],
                                            common.climatology_scores(va, lut_tr, gl_tr))
        lut, gl = common.climatology_lookup(pd.concat([tr, va]))
        p_clim = common.climatology_scores(te, lut, gl)

        rows.append(dict(
            h=h, base=y.mean(), onset_base=(y[per == 0].mean() if (per == 0).any() else np.nan),
            auc_lean=common.auc(y, p_lean), ci_lean=common.block_bootstrap_auc_ci(y, p_lean, g, "auc", seed=config.SEED),
            auc_per=common.auc(y, per), auc_clim=common.auc(y, p_clim),
            on_lean=common.onset_auc(y, p_lean, per), on_lean_ci=common.block_bootstrap_auc_ci(y, p_lean, g, "onset", per, seed=config.SEED),
            on_clim=common.onset_auc(y, p_clim, per), on_clim_ci=common.block_bootstrap_auc_ci(y, p_clim, g, "onset", per, seed=config.SEED),
            mcc_lean=common.mcc(y, (p_lean >= thr).astype(int)),
            mcc_per=common.mcc(y, per),
            mcc_clim=common.mcc(y, (p_clim >= clim_thr).astype(int)),
            onmcc_lean=common.onset_mcc(y, p_lean, per, thr),
            onmcc_clim=common.onset_mcc(y, p_clim, per, clim_thr),
        ))

    L = ["# Held-out evaluation - optimized lean model (HistGBM, 2 features) vs. baselines", "",
         f"Model: **HistGradientBoostingClassifier** on `{' + '.join(config.FEATURES)}` "
         f"(study-selected architecture) | target: median CyAN DN "
         f">= {config.AL1_THRESHOLD} (WHO AL1) | test = target week >= {config.VAL_END}.",
         "AUC 95% CIs (brackets) are block-bootstrapped by lake.", "",
         "### A. Ranking - all-sample AUC-ROC", "",
         "| h | test base rate | lean AUC [95% CI] | persistence | climatology |",
         "|--:|--:|--|--:|--:|"]
    for r in rows:
        L.append(f"| {r['h']} | {r['base']:.3f} | {_f(r['auc_lean'])} {_ci(*r['ci_lean'])} "
                 f"| {_f(r['auc_per'])} | {_f(r['auc_clim'])} |")

    L += ["", "### B. Early warning - onset-AUC (currently-clear lakes only)", "",
          "| h | onset base rate | lean onset-AUC [95% CI] | climatology onset-AUC [95% CI] |",
          "|--:|--:|--|--|"]
    for r in rows:
        L.append(f"| {r['h']} | {_f(r['onset_base'])} | {_f(r['on_lean'])} {_ci(*r['on_lean_ci'])} "
                 f"| {_f(r['on_clim'])} {_ci(*r['on_clim_ci'])} |")

    L += ["", "### C. Operating point - all-sample MCC at the val-tuned threshold", "",
          "| h | lean MCC | persistence MCC | climatology MCC |",
          "|--:|--:|--:|--:|"]
    for r in rows:
        L.append(f"| {r['h']} | {_f(r['mcc_lean'])} | {_f(r['mcc_per'])} | {_f(r['mcc_clim'])} |")

    L += ["", "### D. Onset alert - onset-MCC at the val-tuned threshold (currently-clear only)", "",
          "| h | lean onset-MCC | climatology onset-MCC |",
          "|--:|--:|--:|"]
    for r in rows:
        L.append(f"| {r['h']} | {_f(r['onmcc_lean'])} | {_f(r['onmcc_clim'])} |")

    L += ["",
          "**Reading it (honestly).**",
          "- **All-sample AUC (A) is autocorrelation-dominated** - persistence scores nearly "
          "as well, so it is *not* the result.",
          "- **onset-AUC (B) is the decision-relevant ranking metric** (persistence has no skill "
          "on currently-clear lakes by construction). The gradient-boosted trees lift onset skill "
          "over the logistic GLM this pipeline used to ship (the non-linear cyan_median x area "
          "interaction), which is exactly why the study selected this architecture for the lean "
          "set. A per-lake seasonal **climatology - itself only a baseline - remains "
          "competitive**, especially at longer lead where the real-time feature goes stale while "
          "climatology (calendar-only) pays no lead-time penalty.",
          "- **onset-MCC (D)** is the thresholded early-warning alert the deck headlines; it is the "
          "metric where trees separate most from a linear fit and from climatology.",
          "- The target **base rate drifts up** over the record (train ~0.22 -> test ~0.27); "
          "reported as a limitation, not corrected for.",
          "",
          "This lean model's value is **a cheap, deployable early-warning forecaster that extends "
          "EPA's single 1-week nowcast to a 0-4 week horizon** while staying competitive with the "
          "baselines; the richer real-time-CyAN + fusion ladder in `../models/` is the "
          "tantalizing-but-unproven avenue for pushing onset skill higher. The label is a satellite "
          "realization, not toxin. Correlation, not causation.", ""]

    (config.OUTPUTS / "eval_metrics.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\nWrote {config.OUTPUTS / 'eval_metrics.md'}")


if __name__ == "__main__":
    main()
