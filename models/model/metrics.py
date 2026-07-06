"""Canonical classification-metric suite for ALL modeling experiments (baselines + fused models).

Single source of truth so every experiment reports the same wide suite (DESIGN §8):
threshold-free — AUC-ROC, AUC-PR, Brier — and operating-point (at `thr`) — MCC, F1, Precision,
Recall, Accuracy. Import this everywhere; do not hand-roll metrics per script.
"""
from __future__ import annotations

import numpy as np
from sklearn.metrics import (accuracy_score, average_precision_score, brier_score_loss,
                             f1_score, matthews_corrcoef, precision_score, recall_score,
                             roc_auc_score)

# canonical display order
METRIC_ORDER = ["AUC-ROC", "AUC-PR", "Brier", "MCC", "F1", "Prec", "Recall", "Acc"]
# higher-is-better for every metric EXCEPT Brier (lower is better)
LOWER_BETTER = {"Brier"}


def best_f1_threshold(y, p, grid=None):
    """Threshold on a probabilistic score that maximizes F1 (tune on train/val only)."""
    y = np.asarray(y).astype(int)
    p = np.asarray(p, dtype=float)
    grid = np.linspace(0.05, 0.95, 19) if grid is None else grid
    return float(max(grid, key=lambda t: f1_score(y, (p >= t).astype(int), zero_division=0)))


def classification_metrics(y, p, thr=0.5, round_to=3):
    """Full suite for binary target `y` and score `p`, thresholded at `thr` for point metrics.

    `p` may be a probability (soft classifier) or a hard 0/1 (e.g. persistence). AUC-ROC/AUC-PR/Brier
    use the score directly; MCC/F1/Prec/Recall/Acc use `(p >= thr)`. AUC-ROC/AUC-PR are NaN if `y` has
    a single class in the slice.
    """
    y = np.asarray(y).astype(int)
    p = np.asarray(p, dtype=float)
    if not np.isfinite(p).all():
        raise ValueError("classification_metrics: scores contain NaN/inf — impute/handle before scoring")
    yhat = (p >= thr).astype(int)
    two = len(np.unique(y)) > 1
    out = {
        "AUC-ROC": roc_auc_score(y, p) if two else float("nan"),
        "AUC-PR": average_precision_score(y, p) if two else float("nan"),
        "Brier": brier_score_loss(y, p),
        "MCC": matthews_corrcoef(y, yhat),
        "F1": f1_score(y, yhat, zero_division=0),
        "Prec": precision_score(y, yhat, zero_division=0),
        "Recall": recall_score(y, yhat, zero_division=0),
        "Acc": accuracy_score(y, yhat),
    }
    if round_to is not None:
        out = {k: (round(v, round_to) if v == v else v) for k, v in out.items()}  # keep NaN as NaN
    return out
