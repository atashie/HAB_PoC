"""Experiment 2: rigorous feature ABLATION + collinearity (Codex/user: excess covarying features +
limited targets -> overfitting risk). Drop-one-block from fusion_full, fusion_full+clim, and
fusion_nocyan+clim; report the standard grid (onsetAUC/onsetMCC = early-warning skill; valAUC-testAUC =
overfit). HistGBM (arch-robust per Exp-1; XGBoost ~ HistGBM, logistic reported for the base families).
Also writes a collinearity summary (|corr|>0.8 feature pairs on train).
Run: python models/model/exp_ablation.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from experiment_lib import (CYAN, INSITU, SEASON, STATIC, WEATHER, load, prep, run_experiment,  # noqa: E402
                            split)

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "exp_ablation.md"))
COLLIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "exp_collinearity.md"))
BLOCKS = {"CYAN": CYAN, "STATIC": STATIC, "SEASON": SEASON, "WEATHER": WEATHER, "INSITU": INSITU}


def drop_one(name, feats):
    """full model + each block removed (only blocks the model contains)."""
    out = {f"{name} (all)": list(feats)}
    for blk, cols in BLOCKS.items():
        present = [c for c in cols if c in feats]
        if present and any(c in feats for c in cols):
            out[f"{name} -{blk}"] = [f for f in feats if f not in cols]
    if "clim" in feats:
        out[f"{name} -clim"] = [f for f in feats if f != "clim"]
    return out


def collinearity():
    df = prep(load()); tr = split(df[(df.horizon == 1) & df.persistence.notna()])[0]
    feats = CYAN + STATIC + SEASON + WEATHER + INSITU
    X = tr[feats].select_dtypes("number")
    corr = X.corr().abs()
    pairs = [(a, b, round(corr.loc[a, b], 3)) for i, a in enumerate(corr.columns)
             for b in corr.columns[i + 1:] if corr.loc[a, b] > 0.8]
    pairs.sort(key=lambda t: -t[2])
    with open(COLLIN, "w", encoding="utf-8") as fh:
        fh.write("# Feature collinearity (train, h=1) -- |Pearson r| > 0.8\n\n")
        fh.write(f"{len(pairs)} highly-collinear pairs among {len(feats)} fusion features -- excess "
                 "covariance inflates overfitting risk (motivates the ablation).\n\n| feat A | feat B | |r| |\n| --- | --- | --- |\n")
        for a, b, r in pairs[:40]:
            fh.write(f"| `{a}` | `{b}` | {r:.3f} |\n")
    print(f"collinearity: {len(pairs)} pairs |r|>0.8; wrote {COLLIN}")


def main():
    FF = CYAN + STATIC + SEASON + WEATHER + INSITU
    families = {"fusion_full": FF, "fusion_full+clim": FF + ["clim"],
                "fusion_nocyan+clim": STATIC + SEASON + WEATHER + INSITU + ["clim"]}
    suites = {}
    for nm, feats in families.items():
        suites.update(drop_one(nm, feats))
    collinearity()
    run_experiment(suites, ["histgbm"], OUT,
                   "Exp 2 - feature ablation (drop-one block) + overfitting focus (HistGBM)",
                   baselines=True)


if __name__ == "__main__":
    main()
