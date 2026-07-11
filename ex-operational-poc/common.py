"""Shared, leakage-safe core for the lean operational forecaster.

This module is deliberately small and pure (no I/O, no network) so the one piece of
logic that MUST be correct — how a feature week is aligned to a target week without
leaking the future — lives in one tested place.

The autoregressive-leakage problem, stated plainly
----------------------------------------------------
The target, `bloom(W)`, is a threshold on the CyAN median at week W. The feature,
`cyan_median`, is the CyAN median at an *earlier* week. Because it is the SAME
satellite product, using week W's CyAN as a feature would be circular — you would be
"predicting" a threshold on a number from that same number.

Two rules prevent it, and both are enforced here (and checked in tests/):

1. **Antecedent-only.** For a horizon-`h` forecast of week W, the feature comes from
   `W - (h+1)` weeks — never W. The `+1` is CyAN's ~1-week publication latency: the
   freshest composite actually *available* when the forecast is issued is one week
   behind the nominal lead. This is `feature_cutoff = W - (h+1) weeks`.
2. **Freshest-available (gap-safe).** If that exact week is missing (cloud), we take
   the most recent composite at or before the cutoff — the honest "what you'd really
   have" — via a backward as-of join. We never reach forward.

`build_horizon_frame` returns, for every (lake, target-week) with a known label, the
antecedent `cyan_median`, the static `area_sqkm`, and a latency-aware `persistence`
baseline (= the label at the feature week). It asserts the feature week is strictly
older than the target by at least `(h+1)` weeks, so a leak is a crash, not a silent bug.
"""
from __future__ import annotations
from datetime import date, timedelta
import numpy as np
import pandas as pd


# --- CyAN weekly filename -> composite start date -------------------------
def parse_week_start(filename: str, olci_prefix: str = "L"):
    """Return the 7-day composite's START date, or None if not the OLCI sensor.

    CyAN weekly names look like `L20161152016121.L3m_7D_CYAN_CI_cyano_..._300m.tif`:
    sensor letter + YYYYDDD(start) + YYYYDDD(end). We key each composite by its start
    date and keep only the OLCI ('L') sensor for a single-sensor record.
    """
    stem = filename.split("/")[-1].split("\\")[-1]
    if not stem or stem[0] != olci_prefix:
        return None
    try:
        year = int(stem[1:5])
        doy = int(stem[5:8])
    except ValueError:
        return None
    return date(year, 1, 1) + timedelta(days=doy - 1)


# --- The leakage-safe alignment (the trusted core) ------------------------
def build_horizon_frame(panel: pd.DataFrame, h: int) -> pd.DataFrame:
    """Assemble the (feature, target) table for forecast horizon `h`.

    `panel` = one row per (comid, week_start) with columns:
        comid, week_start (datetime64), cyan_median (float), bloom (0/1), area_sqkm.
    Returns one row per (comid, target week) that has both a label and an available
    antecedent feature, with columns:
        comid, target_date, feature_date, staleness_days, horizon,
        cyan_median, area_sqkm, persistence, bloom (target label).
    """
    p = panel.dropna(subset=["cyan_median", "bloom"]).copy()
    p["week_start"] = pd.to_datetime(p["week_start"])
    p = p.sort_values(["comid", "week_start"])

    # Targets: every labelled lake-week. Feature cutoff = target - (h+1) weeks.
    tgt = p[["comid", "week_start", "bloom", "area_sqkm"]].rename(
        columns={"week_start": "target_date", "bloom": "target_bloom"}
    )
    tgt["cutoff"] = tgt["target_date"] - pd.Timedelta(weeks=h + 1)
    # merge_asof requires each side sorted by its ON key ALONE (not by [comid, key]);
    # the `by="comid"` grouping is handled internally. Keep these sorts single-key.
    tgt = tgt.sort_values("cutoff")

    # Feature source: the antecedent composite (its cyan_median and its own bloom).
    feat = p[["comid", "week_start", "cyan_median", "bloom"]].rename(
        columns={"week_start": "feature_date", "bloom": "persistence"}
    ).sort_values("feature_date")

    # Backward as-of join: freshest feature_date <= cutoff, per lake. Gap-safe, never
    # reaches into the future.
    out = pd.merge_asof(
        tgt, feat,
        left_on="cutoff", right_on="feature_date",
        by="comid", direction="backward",
    )
    out = out.dropna(subset=["cyan_median", "feature_date"])

    # LEAKAGE GUARD (hard): the feature week must be at least (h+1) weeks before the
    # target week. If this ever fails, the pipeline crashes rather than leaking.
    min_gap = pd.Timedelta(weeks=h + 1)
    bad = out["feature_date"] > (out["target_date"] - min_gap)
    if bad.any():
        raise AssertionError(
            f"Leakage: {int(bad.sum())} rows at h={h} have a feature week newer than "
            f"target - {h + 1} weeks."
        )

    out["staleness_days"] = (out["target_date"] - out["feature_date"]).dt.days
    out["horizon"] = h
    return out.rename(columns={"target_bloom": "bloom"})[
        ["comid", "target_date", "feature_date", "staleness_days", "horizon",
         "cyan_median", "area_sqkm", "persistence", "bloom"]
    ].reset_index(drop=True)


# --- Temporal split (no shuffling of autocorrelated weeks) ----------------
def temporal_split(df: pd.DataFrame, train_end: str, val_end: str):
    """Split by target week into train / val / test. Purely temporal — never random,
    because lake-weeks are strongly autocorrelated and a random split would leak
    neighbouring weeks across the boundary."""
    d = pd.to_datetime(df["target_date"])
    tr = df[d < pd.Timestamp(train_end)]
    va = df[(d >= pd.Timestamp(train_end)) & (d < pd.Timestamp(val_end))]
    te = df[d >= pd.Timestamp(val_end)]
    return tr, va, te


# --- Per-lake climatology baseline (fit on labelled history only) ---------
def _woy(dates) -> np.ndarray:
    """Week-of-year 1..52, with ISO week 53 folded into 52 so the seasonal key is stable
    across years (week 53 exists only in some years; without folding, a week-53 target
    would miss the lookup and fall back to the global rate, under-crediting climatology)."""
    w = pd.to_datetime(dates).dt.isocalendar().week.astype(int).to_numpy()
    return np.minimum(w, 52)


def climatology_lookup(fit_df: pd.DataFrame) -> tuple[dict, float]:
    """Per-(comid, week-of-year) bloom rate, learned ONLY from `fit_df` (train[+val]).
    Returns the lookup and a global fallback rate for unseen keys."""
    f = fit_df.copy()
    f["woy"] = _woy(f["target_date"])
    lut = f.groupby(["comid", "woy"])["bloom"].mean().to_dict()
    return lut, float(f["bloom"].mean())


def climatology_scores(df: pd.DataFrame, lut: dict, glob: float) -> np.ndarray:
    woy = _woy(df["target_date"])
    return np.array([lut.get((c, w), glob) for c, w in zip(df["comid"], woy)])


# --- Transparent model scoring --------------------------------------------
# We fit a logistic regression with scikit-learn (03_train) but persist only its
# standardizer stats + coefficients as JSON, and score with this 3-line function.
# The model is small enough to be fully human-readable, and scoring needs no sklearn.
def logreg_score(params: dict, X: np.ndarray) -> np.ndarray:
    """P(bloom) for rows X (columns in params['features'] order)."""
    mean = np.asarray(params["mean"]); scale = np.asarray(params["scale"])
    coef = np.asarray(params["coef"]); b = float(params["intercept"])
    z = ((np.asarray(X, float) - mean) / scale) @ coef + b
    return 1.0 / (1.0 + np.exp(-z))


def fit_logreg(df: pd.DataFrame, features, target: str, seed: int = 42) -> dict:
    """Fit a standardized logistic regression and return its params as a plain dict
    (the same shape `logreg_score` consumes). sklearn is imported here so that merely
    *scoring* a saved model never needs sklearn installed."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    X = df[list(features)].to_numpy(float)
    y = df[target].to_numpy(int)
    sc = StandardScaler().fit(X)
    lr = LogisticRegression(max_iter=1000, random_state=seed).fit(sc.transform(X), y)
    return {"features": list(features), "mean": sc.mean_.tolist(),
            "scale": sc.scale_.tolist(), "coef": lr.coef_[0].tolist(),
            "intercept": float(lr.intercept_[0])}


def best_f1_threshold(y, p) -> float:
    """Operating point that maximizes F1, chosen on VALIDATION only (never test)."""
    from sklearn.metrics import f1_score
    y = np.asarray(y, int)
    best_t, best_f = 0.5, -1.0
    for t in np.linspace(0.05, 0.95, 19):
        f = f1_score(y, (np.asarray(p) >= t).astype(int), zero_division=0)
        if f > best_f:
            best_f, best_t = f, float(t)
    return best_t


# --- Metrics --------------------------------------------------------------
def auc(y, p) -> float:
    """ROC-AUC via the rank identity (no sklearn dependency here). NaN if one class."""
    y = np.asarray(y, float)
    p = np.asarray(p, float)
    n1 = y.sum()
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    # Mann-Whitney U via average ranks (ties get the mean rank, matching roc_auc_score).
    _, inv, counts = np.unique(p, return_inverse=True, return_counts=True)
    csum = np.cumsum(counts)
    avg = {i: (csum[i] - counts[i] + 1 + csum[i]) / 2.0 for i in range(len(counts))}
    ranks = np.array([avg[i] for i in inv])
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def onset_auc(y, p, persistence) -> float:
    """Early-warning AUC: restrict to currently-clear lake-weeks (persistence==0) and
    score which ones BECOME a bloom. This is the decision-relevant metric — persistence
    has zero skill here by construction, so any skill is genuine onset skill."""
    m = np.asarray(persistence) == 0
    if m.sum() == 0:
        return float("nan")
    return auc(np.asarray(y)[m], np.asarray(p)[m])


def block_bootstrap_auc_ci(y, p, groups, metric="auc", persistence=None,
                           n_boot=500, seed=42):
    """95% CI for AUC / onset-AUC by resampling whole lakes (blocks), never rows —
    row-level bootstrap would ignore within-lake autocorrelation and understate the CI."""
    y = np.asarray(y); p = np.asarray(p); groups = np.asarray(groups)
    pers = None if persistence is None else np.asarray(persistence)
    uniq = np.unique(groups)
    idx_by_g = {g: np.where(groups == g)[0] for g in uniq}
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([idx_by_g[g] for g in pick])
        if metric == "onset":
            v = onset_auc(y[idx], p[idx], pers[idx])
        else:
            v = auc(y[idx], p[idx])
        if not np.isnan(v):
            vals.append(v)
    if not vals:
        return (float("nan"), float("nan"))
    return (float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)))
