"""Step 3 - TRAIN / VALIDATE / TEST.  Fit the lean 2-feature model, one per horizon.

For each lead time h in {0,1,2,3,4}:
  * build the leakage-safe (feature, target) table    (common.build_horizon_frame)
  * split by time into train / val / test             (common.temporal_split)
  * fit logistic regression on TRAIN                   (features: cyan_median, area_sqkm)
  * pick the alert threshold on VALIDATION             (never on test)
The fitted, human-readable coefficients + threshold are written to outputs/models.json.
Held-out TEST scoring lives in 04_evaluate.py so training never sees test metrics.

Run:  python 03_train.py
"""
import json
import pandas as pd

import config
import common


def main():
    panel = pd.read_parquet(config.LAKE_WEEK_PARQUET)
    models = {}
    print(f"{'h':>2} {'n_train':>8} {'n_val':>7} {'n_test':>7} "
          f"{'thr':>5} {'AUC_tr':>7} {'AUC_val':>7}")
    for h in config.HORIZONS:
        frame = common.build_horizon_frame(panel, h)
        tr, va, te = common.temporal_split(frame, config.TRAIN_END, config.VAL_END)

        params = common.fit_logreg(tr, config.FEATURES, config.TARGET, config.SEED)
        p_val = common.logreg_score(params, va[config.FEATURES].to_numpy())
        params["threshold"] = common.best_f1_threshold(va[config.TARGET], p_val)

        p_tr = common.logreg_score(params, tr[config.FEATURES].to_numpy())
        params.update(n_train=len(tr), n_val=len(va), n_test=len(te),
                      auc_train=round(common.auc(tr[config.TARGET], p_tr), 3),
                      auc_val=round(common.auc(va[config.TARGET], p_val), 3))
        models[str(h)] = params
        print(f"{h:>2} {len(tr):>8,} {len(va):>7,} {len(te):>7,} "
              f"{params['threshold']:>5.2f} {params['auc_train']:>7} {params['auc_val']:>7}")

    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    meta = {"features": config.FEATURES, "target_rule": f"median CyAN DN >= {config.AL1_THRESHOLD} (WHO AL1)",
            "train_end": config.TRAIN_END, "val_end": config.VAL_END, "seed": config.SEED,
            "horizons": {str(h): models[str(h)] for h in config.HORIZONS}}
    (config.OUTPUTS / "models.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"\nWrote {config.OUTPUTS / 'models.json'}")


if __name__ == "__main__":
    main()
