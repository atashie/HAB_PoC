"""Step 3 - TRAIN / VALIDATE / TEST.  Fit the optimized lean model, one per horizon.

The shipped model is a HistGradientBoostingClassifier on the two lean features
(`cyan_median`, `area_sqkm`) - the architecture the full study selected for this exact
feature set (better held-out early-warning skill than the logistic GLM; see
../models/outputs/exp_feature_ablation.md and the deck's final-model slide).

For each lead time h in {0,1,2,3,4} we follow the study's protocol verbatim:
  * build the leakage-safe (feature, target) table    (common.build_horizon_frame)
  * split by time into train / val / test             (common.temporal_split)
  * fit HistGBM on TRAIN, pick the alert threshold on VALIDATION (never on test)
  * REFIT on TRAIN+VAL (val is used, not wasted) - this is the deployed-for-test model
Each fitted booster is persisted to outputs/models/hgb_h{h}.joblib; a readable metadata
record (hyperparameters, threshold, permutation importance, a CyAN partial-dependence
curve) goes to outputs/models.json. Held-out TEST scoring lives in 04_evaluate.py so
training never sees test metrics.

Run:  python 03_train.py
"""
import json
import pandas as pd

import config
import common


def main():
    panel = pd.read_parquet(config.LAKE_WEEK_PARQUET)
    meta_horizons = {}
    print(f"{'h':>2} {'n_fit':>8} {'n_test':>7} {'thr':>5} {'AUC_fit':>7} "
          f"{'imp(cyan)':>9} {'imp(area)':>9}")
    for h in config.HORIZONS:
        frame = common.build_horizon_frame(panel, h)
        tr, va, te = common.temporal_split(frame, config.TRAIN_END, config.VAL_END)
        trva = pd.concat([tr, va])

        # Threshold: tuned on val (genuinely held out) using a TRAIN-ONLY fit.
        thr_model = common.fit_hgb(tr, config.FEATURES, config.TARGET, config.HGB_PARAMS, config.SEED)
        thr = common.best_f1_threshold(
            va[config.TARGET], common.hgb_score(thr_model, va[config.FEATURES].to_numpy()))
        # Deployed-for-test model: refit on TRAIN+VAL (matches ../models' protocol).
        # 05_predict refits on ALL history for the live forecast.
        model = common.fit_hgb(trva, config.FEATURES, config.TARGET, config.HGB_PARAMS, config.SEED)
        common.save_model(model, config.MODEL_DIR / f"hgb_h{h}.joblib")

        # Transparency (the readable stand-in for GLM coefficients): how hard the model
        # leans on each feature (permutation importance) and how risk responds to CyAN
        # (partial dependence). Computed on train+val, the model's own fit data.
        auc_fit, imp = common.permutation_importance(model, trva, config.FEATURES, config.TARGET,
                                                     seed=config.SEED)
        pd_grid, pd_curve = common.partial_dependence_1d(model, trva, config.FEATURES, "cyan_median")

        meta_horizons[str(h)] = {
            "features": list(config.FEATURES),
            "model_file": f"models/hgb_h{h}.joblib",
            "threshold": thr,
            "n_fit": int(len(trva)),
            "n_test": int(len(te)),
            "auc_fit": round(auc_fit, 3),
            "perm_importance_auc": {f: {"mean": round(m, 4), "std": round(s, 4)}
                                    for f, (m, s) in imp.items()},
            "partial_dependence_cyan_median": {"cyan_median": [round(v, 1) for v in pd_grid],
                                               "p_bloom": [round(v, 4) for v in pd_curve]},
        }
        print(f"{h:>2} {len(trva):>8,} {len(te):>7,} {thr:>5.2f} {round(auc_fit, 3):>7} "
              f"{imp['cyan_median'][0]:>9.3f} {imp['area_sqkm'][0]:>9.3f}")

    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    meta = {"model": "HistGradientBoostingClassifier (lean 2-feature; study-selected architecture)",
            "hyperparameters": config.HGB_PARAMS,
            "features": config.FEATURES,
            "target_rule": f"median CyAN DN >= {config.AL1_THRESHOLD} (WHO AL1)",
            "train_end": config.TRAIN_END, "val_end": config.VAL_END, "seed": config.SEED,
            "protocol": "fit train -> threshold on val -> refit train+val -> (test scored in 04)",
            "horizons": meta_horizons}
    (config.OUTPUTS / "models.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"\nWrote {config.OUTPUTS / 'models.json'} and {len(config.HORIZONS)} boosters "
          f"under {config.MODEL_DIR}")


if __name__ == "__main__":
    main()
