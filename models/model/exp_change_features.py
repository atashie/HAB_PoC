"""Experiment 1: does adding weather TREND/CHANGE features let the anti-persistence model predict
ONSETS (flips)? Change = recent-vs-longer precip & solar rate + short-minus-long SPEI (a flip is a
change event, not a level). Compares fusion_nocyan+clim (+chg) and fusion_full (+clim,+chg) with the
standard reporting contract (EPA row, overfitting gaps, flipMCC by horizon).
Run: python models/model/exp_change_features.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from experiment_lib import CHANGE, CYAN, DRIVERS, run_experiment  # noqa: E402

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "exp_change_features.md"))
SUITES = {
    "fusion_full": CYAN + DRIVERS,
    "fusion_full+clim": CYAN + DRIVERS + ["clim"],
    "fusion_full+clim+chg": CYAN + DRIVERS + ["clim"] + CHANGE,
    "fusion_nocyan+clim": DRIVERS + ["clim"],
    "fusion_nocyan+clim+chg": DRIVERS + ["clim"] + CHANGE,
}

if __name__ == "__main__":
    run_experiment(SUITES, ["histgbm", "xgboost", "logistic"], OUT,
                   "Exp 1 - weather change/trend features vs onsets (flips)")
