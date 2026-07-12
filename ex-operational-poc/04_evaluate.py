"""Step 4 - ASSESS.  Score the held-out TEST period and, per the claim gate, always
beside baselines and with an uncertainty.

Baselines (every horizon, every metric):
  * persistence  = the latency-aware label carried from the feature week (a stiff,
    honest yardstick because bloom state is strongly autocorrelated).
  * climatology  = per-(lake, week-of-year) bloom rate; alert threshold tuned on val (from
    a train-only fit), then refit on TRAIN+VAL for test scoring - the same fair fit the lean
    model uses (03_train refits on train+val), so the comparison is apples-to-apples.

Three metric families, each with its baselines:
  A. all-sample AUC-ROC   - overall ranking; autocorrelation-inflated, NOT the result.
  B. onset-AUC            - currently-clear lakes only; THE decision-relevant metric.
  C. MCC @ val-tuned thr  - a balanced operating-point score.
95% CIs are block-bootstrapped by lake (never by row). Both the lean model AND the
climatology baseline carry CIs on the onset metric, since that comparison is load-bearing.

Output: outputs/eval_metrics.md

Run:  python 04_evaluate.py
"""
import json
import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef

import config
import common


def _f(v):
    return "n/a" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.3f}"


def _ci(lo, hi):
    return f"[{_f(lo)}, {_f(hi)}]"


def _mcc(y, pred):
    """MCC. nan only when the LABELS are single-class (genuinely undefined); a constant
    prediction on mixed labels is 0.0 = no skill (matches sklearn, without its 0/0 warning)."""
    if len(np.unique(y)) < 2:
        return float("nan")
    if len(np.unique(pred)) < 2:
        return 0.0
    return matthews_corrcoef(y, pred)


def main():
    panel = pd.read_parquet(config.LAKE_WEEK_PARQUET)
    models = json.loads((config.OUTPUTS / "models.json").read_text(encoding="utf-8"))["horizons"]

    rows = []  # per-horizon computed numbers
    for h in config.HORIZONS:
        p = models[str(h)]
        frame = common.build_horizon_frame(panel, h)
        tr, va, te = common.temporal_split(frame, config.TRAIN_END, config.VAL_END)
        y = te[config.TARGET].to_numpy(int)
        per = te["persistence"].to_numpy(int)
        g = te["comid"].to_numpy()

        # lean (val-tuned threshold from 03_train)
        p_lean = common.logreg_score(p, te[config.FEATURES].to_numpy())
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
            mcc_lean=_mcc(y, (p_lean >= p["threshold"]).astype(int)),
            mcc_per=_mcc(y, per),
            mcc_clim=_mcc(y, (p_clim >= clim_thr).astype(int)),
        ))

    L = ["# Held-out evaluation - lean 2-feature model vs. baselines", "",
         f"Features: `{' + '.join(config.FEATURES)}`  |  target: median CyAN DN "
         f">= {config.AL1_THRESHOLD} (WHO AL1)  |  test = target week >= {config.VAL_END}.",
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

    L += ["", "### C. Operating point - MCC at the val-tuned threshold", "",
          "| h | lean MCC | persistence MCC | climatology MCC |",
          "|--:|--:|--:|--:|"]
    for r in rows:
        L.append(f"| {r['h']} | {_f(r['mcc_lean'])} | {_f(r['mcc_per'])} | {_f(r['mcc_clim'])} |")

    L += ["",
          "**Reading it (honestly).**",
          "- **All-sample AUC (A) is autocorrelation-dominated** - persistence scores nearly "
          "as well, so it is *not* the result.",
          "- **onset-AUC (B) is the decision-relevant metric** (persistence has no skill on "
          "currently-clear lakes by construction). The lean model has genuine onset skill, but "
          "a per-lake seasonal **climatology - itself only a baseline - is competitive-to-better** "
          "(tied at short lead, ahead at longer lead). Note this is partly *structural*: "
          "climatology depends only on the target week's calendar position, so it is "
          "**horizon-invariant and pays no lead-time penalty**, while the lean model's real-time "
          "feature goes stale with lead. The onset subset is also small and imbalanced (base rate "
          "~3-6%, rising with h), so each row scores a slightly different task.",
          "- **At the operating point (C), persistence matches the lean model** on MCC - the "
          "2-feature model earns no unique thresholded edge. Thresholds are tuned on validation "
          "(by F1), never on test.",
          "- The target **base rate drifts up** over the record (train ~0.22 -> test ~0.27); "
          "reported as a limitation, not corrected for.",
          "",
          "This 2-feature model's value is **simplicity + explainability while staying "
          "competitive**, not beating every baseline; the richer real-time-CyAN ladder in "
          "`../models/` is what pushes onset skill higher. The label is a satellite realization, "
          "not toxin. Correlation, not causation.", ""]

    (config.OUTPUTS / "eval_metrics.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\nWrote {config.OUTPUTS / 'eval_metrics.md'}")


if __name__ == "__main__":
    main()
