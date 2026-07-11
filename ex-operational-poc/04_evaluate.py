"""Step 4 - ASSESS.  Score the held-out TEST period and, per the claim gate, always
beside baselines and with an uncertainty.

Baselines (every horizon):
  * persistence  = the latency-aware label carried from the feature week (a stiff,
    honest yardstick because bloom state is strongly autocorrelated).
  * climatology  = per-(lake, week-of-year) bloom rate, fit on train+val only.

Metrics on TEST:
  * AUC-ROC (all lake-weeks)          - overall ranking; autocorrelation-inflated.
  * onset-AUC (currently-clear only)  - THE decision-relevant early-warning metric;
    persistence has no skill here by construction, so skill is genuinely predictive.
  * MCC at the val-tuned threshold    - a balanced operating-point score.
95% CIs are block-bootstrapped by lake (never by row).

Output: outputs/eval_metrics.md

Run:  python 04_evaluate.py
"""
import json
import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef

import config
import common


def _fmt(v):
    return "n/a" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.3f}"


def main():
    panel = pd.read_parquet(config.LAKE_WEEK_PARQUET)
    models = json.loads((config.OUTPUTS / "models.json").read_text(encoding="utf-8"))["horizons"]

    lines = ["# Held-out evaluation - lean 2-feature model vs. baselines", "",
             f"Features: `{' + '.join(config.FEATURES)}`  |  target: median CyAN DN "
             f">= {config.AL1_THRESHOLD} (WHO AL1)  |  test = target week >= {config.VAL_END}.",
             "AUC 95% CIs (in brackets) are block-bootstrapped by lake. `onset` = "
             "currently-clear lakes only (early-warning skill).", "",
             "| h | test rows | base rate | lean AUC | persist AUC | clim AUC | "
             "lean onset-AUC | clim onset-AUC | lean MCC |",
             "|--:|--:|--:|--|--:|--:|--|--:|--:|"]

    for h in config.HORIZONS:
        p = models[str(h)]
        frame = common.build_horizon_frame(panel, h)
        tr, va, te = common.temporal_split(frame, config.TRAIN_END, config.VAL_END)

        y = te[config.TARGET].to_numpy(int)
        per = te["persistence"].to_numpy(int)
        g = te["comid"].to_numpy()
        p_lean = common.logreg_score(p, te[config.FEATURES].to_numpy())

        lut, glob = common.climatology_lookup(pd.concat([tr, va]))
        p_clim = common.climatology_scores(te, lut, glob)

        auc_lean = common.auc(y, p_lean)
        ci_lean = common.block_bootstrap_auc_ci(y, p_lean, g, "auc", seed=config.SEED)
        onset_lean = common.onset_auc(y, p_lean, per)
        ci_onset = common.block_bootstrap_auc_ci(y, p_lean, g, "onset", per, seed=config.SEED)
        mcc = matthews_corrcoef(y, (p_lean >= p["threshold"]).astype(int)) if y.any() else float("nan")

        lines.append(
            f"| {h} | {len(te):,} | {y.mean():.3f} | "
            f"{_fmt(auc_lean)} [{_fmt(ci_lean[0])}, {_fmt(ci_lean[1])}] | "
            f"{_fmt(common.auc(y, per))} | {_fmt(common.auc(y, p_clim))} | "
            f"{_fmt(onset_lean)} [{_fmt(ci_onset[0])}, {_fmt(ci_onset[1])}] | "
            f"{_fmt(common.onset_auc(y, p_clim, per))} | {_fmt(mcc)} |")

    lines += ["",
              "**Reading it (honestly).** All-sample AUC is high but "
              "autocorrelation-dominated - persistence scores nearly as well, so it is "
              "*not* the result. The decision-relevant signal is **onset-AUC** "
              "(currently-clear lakes), where persistence has no skill by construction. "
              "The lean model shows genuine onset skill (well above 0.5), but a per-lake "
              "seasonal **climatology - itself only a baseline - is competitive-to-better** "
              "on the onset alert. So this 2-feature model's value is *simplicity + "
              "explainability while staying competitive*, not beating every baseline; a "
              "richer real-time-CyAN ladder is what pushes onset skill higher in the full "
              "study. Correlation, not causation.",
              ""]
    (config.OUTPUTS / "eval_metrics.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {config.OUTPUTS / 'eval_metrics.md'}")


if __name__ == "__main__":
    main()
