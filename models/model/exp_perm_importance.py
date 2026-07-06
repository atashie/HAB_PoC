"""Exp 4: correlation-CLUSTERED permutation importance (user 2026-07-06).

Why clustered: the fusion features are heavily collinear (47 pairs |r|>0.8, mostly CyAN-internal; see
`exp_collinearity.md`). Plain per-feature permutation importance UNDER-credits correlated features
(permuting `cyan_mean` while `cyan_median` stays reads ~0), and the greedy-ablation order is only a
*conditional* dispensability path, not marginal importance. So we (1) hierarchically cluster features
by |Pearson r| on TRAIN (complete linkage, cut so within-cluster |r| >= CLUST_RMIN), then (2) GROUPED-
permute each cluster together in the fitted full model (fusion_full+clim) on the held-out TEST set and
measure the drop on each metric. Grouped permutation credits the *signal* (the cluster), not an
arbitrary split among redundant twins.

Reported per architecture (histgbm/xgboost/logistic), on THREE metrics (user):
  * pooled AUC-ROC   -- overall ranking (dominated by persistence-easy weeks)
  * AUC_within       -- median within-lake AUC (within-lake temporal skill)
  * onsetMCC (h=1)   -- the ALERT-decision metric (classify bloom-next among currently-CLEAR weeks,
                        at the model's val-tuned F1 threshold, held FIXED across permutations)
onsetAUC also shown for context. Importance = baseline_metric - permuted_metric (mean +/- std over
N_PERM shuffles); higher = the cluster matters more for that metric.

Model = fusion_full+clim, refit on train+val (D-36 protocol). Split as elsewhere (test >= 2024-07).
Run: python models/model/exp_perm_importance.py
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from experiment_lib import (CYAN, INSITU, PRIM, SEASON, SEED, STATIC, WEATHER, Xof,  # noqa: E402
                            _hgb, _lr, best_f1_threshold, load, per_lake_auc, prep, split, transition)

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "exp_perm_importance.md"))
FF_CLIM = CYAN + STATIC + SEASON + WEATHER + INSITU + ["clim"]
BLOCK_OF = {**{c: "CYAN" for c in CYAN}, **{c: "STATIC" for c in STATIC},
            **{c: "SEASON" for c in SEASON}, **{c: "WEATHER" for c in WEATHER},
            **{c: "INSITU" for c in INSITU}, "clim": "clim"}
N_PERM = 20
CLUST_RMIN = 0.7   # complete-linkage cut: every within-cluster pair has |r| >= 0.7
ARCHS = ["histgbm", "xgboost", "logistic"]


def cluster_features(Xtr):
    """Complete-linkage clusters on |Pearson r|; cut so within-cluster min |r| >= CLUST_RMIN."""
    corr = Xtr.corr().abs().to_numpy()
    corr = np.nan_to_num(corr, nan=0.0)              # constant/all-NaN cols -> uncorrelated
    d = np.clip(1.0 - corr, 0.0, None)
    d = (d + d.T) / 2.0
    np.fill_diagonal(d, 0.0)
    Z = linkage(squareform(d, checks=False), method="complete")
    labels = fcluster(Z, t=1.0 - CLUST_RMIN, criterion="distance")
    clusters = {}
    for f, lab in zip(Xtr.columns, labels):
        clusters.setdefault(int(lab), []).append(f)
    # order clusters biggest-first for stable display
    return sorted(clusters.values(), key=lambda c: (-len(c), c[0]))


def fit_full(arch, feats, tr, va, te):
    """Refit-on-train+val model (matches fit_predict) + val-tuned F1 threshold; returns (model, thr, Xte)."""
    ytr = tr["target_bloom"]; fit = pd.concat([tr, va]); yfit = fit["target_bloom"]
    Xtr, Xva_tr = Xof(tr, feats, tr), Xof(va, feats, tr)
    Xfit, Xte = Xof(fit, feats, fit), Xof(te, feats, fit)
    if arch == "histgbm":
        thr = best_f1_threshold(va["target_bloom"], _hgb().fit(Xtr, ytr).predict_proba(Xva_tr)[:, 1])
        m = _hgb().fit(Xfit, yfit)
    elif arch == "logistic":
        thr = best_f1_threshold(va["target_bloom"], _lr().fit(Xtr, ytr).predict_proba(Xva_tr)[:, 1])
        m = _lr().fit(Xfit, yfit)
    else:
        x1 = XGBClassifier(n_estimators=600, max_depth=6, learning_rate=0.06, subsample=0.8,
                           colsample_bytree=0.8, reg_lambda=1.0, tree_method="hist", eval_metric="logloss",
                           early_stopping_rounds=30, random_state=SEED)
        x1.fit(Xtr, ytr, eval_set=[(Xva_tr, va["target_bloom"])], verbose=False)
        thr = best_f1_threshold(va["target_bloom"], x1.predict_proba(Xva_tr)[:, 1])
        m = XGBClassifier(n_estimators=x1.best_iteration + 1, max_depth=6, learning_rate=0.06,
                          subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0, tree_method="hist",
                          random_state=SEED).fit(Xfit, yfit)
    return m, thr, Xte


def metrics_on(model, X, y, pers, comid, thr):
    p = model.predict_proba(X)[:, 1]
    within, _ = per_lake_auc(y, p, comid)
    tr_ = transition(y, p, pers, thr)
    return {"pooled_AUC": float(roc_auc_score(y, p)), "AUC_within": within,
            "onsetMCC": tr_["onset_MCC"], "onsetAUC": tr_["onset_AUC"]}


def perm_importance(arch, feats, clusters, tr, va, te):
    m, thr, Xte = fit_full(arch, feats, tr, va, te)
    y = te["target_bloom"].to_numpy(); pers = te["persistence"].to_numpy(float)
    comid = te["comid"].to_numpy()
    base = metrics_on(m, Xte, y, pers, comid, thr)
    rng = np.random.default_rng(SEED)
    Xnp = Xte.to_numpy(copy=True); colpos = {c: i for i, c in enumerate(Xte.columns)}
    rows = []
    for cl in clusters:
        pos = [colpos[c] for c in cl]
        drops = {k: [] for k in ("pooled_AUC", "AUC_within", "onsetMCC")}
        for _ in range(N_PERM):
            Xp = Xnp.copy()
            Xp[:, pos] = Xp[rng.permutation(len(Xp))][:, pos]   # grouped row-shuffle of the cluster
            mp = metrics_on(m, pd.DataFrame(Xp, columns=Xte.columns, index=Xte.index),
                            y, pers, comid, thr)
            for k in drops:
                drops[k].append(base[k] - mp[k])
        r = {"cluster": cl, "n": len(cl)}
        for k in drops:
            r[f"{k}_mean"] = float(np.mean(drops[k])); r[f"{k}_std"] = float(np.std(drops[k]))
        rows.append(r)
    return base, thr, rows


def fmt_members(cl):
    return ", ".join(f"`{c}`" for c in cl) if len(cl) <= 6 else \
        ", ".join(f"`{c}`" for c in cl[:6]) + f", (+{len(cl)-6} more)"


def main():
    df = prep(load())
    tr, va, te = split(df[(df.horizon == PRIM) & df.persistence.notna()])
    clusters = cluster_features(Xof(tr, FF_CLIM, tr))
    print(f"{len(clusters)} clusters from {len(FF_CLIM)} features (within-cluster |r|>={CLUST_RMIN})")

    per_arch = {}
    for arch in ARCHS:
        base, thr, rows = perm_importance(arch, FF_CLIM, clusters, tr, va, te)
        per_arch[arch] = (base, thr, rows)
        print(f"[{arch}] baseline onsetMCC={base['onsetMCC']:.3f} AUC_within={base['AUC_within']:.3f} "
              f"pooledAUC={base['pooled_AUC']:.3f}")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("# Exp 4 - correlation-clustered permutation importance (fusion_full+clim)\n\n")
        fh.write(f"Features grouped into **{len(clusters)} clusters** by |Pearson r| on TRAIN (complete "
                 f"linkage, within-cluster |r| >= **{CLUST_RMIN}**), then each cluster is GROUPED-permuted "
                 f"together in the refit full model on **held-out test (>=2024-07)**, {N_PERM} shuffles. "
                 "**Importance = baseline - permuted** (mean +/- std); higher = the cluster matters more. "
                 "Clustering handles the heavy collinearity (per-feature importance would under-credit "
                 "redundant twins). onsetMCC uses the model's val-tuned F1 threshold, held FIXED across "
                 "permutations. Sorted by **onsetMCC importance** (the alert-decision metric).\n\n")

        fh.write("## Clusters (from train correlation)\n\n| # | n | block(s) | members |\n| --- | --- | --- | --- |\n")
        for i, cl in enumerate(clusters, 1):
            blks = "/".join(sorted({BLOCK_OF.get(c, "?") for c in cl}))
            fh.write(f"| C{i} | {len(cl)} | {blks} | {fmt_members(cl)} |\n")

        cid = {tuple(cl): f"C{i}" for i, cl in enumerate(clusters, 1)}
        for arch in ARCHS:
            base, thr, rows = per_arch[arch]
            rows_sorted = sorted(rows, key=lambda r: -r["onsetMCC_mean"])
            fh.write(f"\n## {arch} — baseline: onsetMCC={base['onsetMCC']:.3f}, "
                     f"AUC_within={base['AUC_within']:.3f}, pooledAUC={base['pooled_AUC']:.3f}, "
                     f"onsetAUC={base['onsetAUC']:.3f} (thr={thr:.3f})\n\n")
            fh.write("| cluster | n | block(s) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |\n")
            fh.write("| --- | --- | --- | --- | --- | --- |\n")
            for r in rows_sorted:
                cl = r["cluster"]; blks = "/".join(sorted({BLOCK_OF.get(c, "?") for c in cl}))
                fh.write(f"| {cid[tuple(cl)]} | {r['n']} | {blks} | "
                         f"{r['onsetMCC_mean']:+.3f} ± {r['onsetMCC_std']:.3f} | "
                         f"{r['AUC_within_mean']:+.3f} ± {r['AUC_within_std']:.3f} | "
                         f"{r['pooled_AUC_mean']:+.4f} ± {r['pooled_AUC_std']:.4f} |\n")
        fh.write("\n> Δ is the metric drop when the cluster is scrambled. ~0 or negative = the cluster "
                 "adds nothing (or noise) to that metric in the full model. A cluster important for "
                 "onsetMCC but ~0 for pooled_AUC = it helps the ALERT decision but not overall ranking.\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
