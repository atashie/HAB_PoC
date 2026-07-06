"""Exp 4b: decompose the dominant C1 cluster -- clim vs real-time CyAN observation (Codex-recommended,
2026-07-06, the #1 honesty check). C1 (from correlation clustering) lumps the real-time CyAN satellite
observation together with `clim` (a per-(comid,month) historical bloom rate = identity/base-rate proxy,
demoted in D-35 as "memorizing lakes"). "C1 = the whole model" therefore cannot say whether skill comes
from the GENERALIZABLE real-time CyAN signal or from PER-LAKE MEMORIZATION via clim.

So we grouped-permute SEMANTIC sub-groups within CyAN+clim in the fitted full model (same protocol as
`exp_perm_importance.py`): clim alone; current-week CyAN obs; CyAN lags; CyAN bloom-state; CyAN data-
quality; all-CyAN-no-clim; and all-CyAN+clim (reference). Caveat (stated in output): sub-groups inside a
correlated cluster UNDER-credit each other via redundancy -- the GROUP totals ("all CyAN no clim" vs
"clim alone") are the honest read; the finer splits are lower bounds.

Run: python models/model/exp_perm_c1_decomp.py
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from experiment_lib import CYAN, PRIM, SEED, load, per_lake_auc, prep, split, transition  # noqa: E402
from exp_perm_importance import ARCHS, FF_CLIM, N_PERM, fit_full, metrics_on  # noqa: E402

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "exp_perm_c1_decomp.md"))

CUR = ["cyan_median", "cyan_mean", "cyan_sd"]
LAGS = ["cyan_median_lag1", "cyan_median_lag2", "cyan_median_lag4", "cyan_mean_lag1", "cyan_sd_lag1"]
STATE = ["bloom_state", "bloom_state_ffill", "bloom_lag1", "bloom_roll4", "bloom_roll4_n"]
QUAL = ["cyan_gap_weeks_at_cutoff", "valid_frac"]
GROUPS = {                                    # ordered; all live inside CyAN+clim
    "clim ONLY (per-lake base rate)": ["clim"],
    "CyAN current-week obs (median/mean/sd)": CUR,
    "CyAN antecedent lags": LAGS,
    "CyAN bloom-state flags": STATE,
    "CyAN data-quality (gap/valid_frac)": QUAL,
    "ALL CyAN, NO clim (15 feat)": list(CYAN),
    "ALL CyAN + clim (reference = C1-ish)": list(CYAN) + ["clim"],
}


def permute_group(model, Xte, y, pers, comid, thr, cols):
    base = metrics_on(model, Xte, y, pers, comid, thr)
    Xnp = Xte.to_numpy(copy=True); colpos = {c: i for i, c in enumerate(Xte.columns)}
    pos = [colpos[c] for c in cols]
    rng = np.random.default_rng(SEED)
    d = {k: [] for k in ("onsetMCC", "AUC_within", "pooled_AUC")}
    for _ in range(N_PERM):
        Xp = Xnp.copy()
        Xp[:, pos] = Xp[rng.permutation(len(Xp))][:, pos]
        mp = metrics_on(model, pd.DataFrame(Xp, columns=Xte.columns, index=Xte.index),
                        y, pers, comid, thr)
        for k in d:
            d[k].append(base[k] - mp[k])
    return {k: (float(np.mean(v)), float(np.std(v))) for k, v in d.items()}


def main():
    df = prep(load())
    tr, va, te = split(df[(df.horizon == PRIM) & df.persistence.notna()])
    y = te["target_bloom"].to_numpy(); pers = te["persistence"].to_numpy(float)
    comid = te["comid"].to_numpy()

    per_arch = {}
    for arch in ARCHS:
        model, thr, Xte = fit_full(arch, FF_CLIM, tr, va, te)
        base = metrics_on(model, Xte, y, pers, comid, thr)
        res = {name: permute_group(model, Xte, y, pers, comid, thr, cols)
               for name, cols in GROUPS.items()}
        per_arch[arch] = (base, thr, res)
        print(f"[{arch}] base onsetMCC={base['onsetMCC']:.3f} | "
              f"noClim d.onsetMCC={res['ALL CyAN, NO clim (15 feat)']['onsetMCC'][0]:+.3f} | "
              f"clim d.onsetMCC={res['clim ONLY (per-lake base rate)']['onsetMCC'][0]:+.3f}")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("# Exp 4b - C1 decomposition: real-time CyAN vs `clim` (per-lake base rate)\n\n")
        fh.write("Grouped permutation (same protocol as `exp_perm_importance.py`) of SEMANTIC sub-groups "
                 "inside the dominant CyAN+clim cluster, in the fitted **fusion_full+clim** model on "
                 f"held-out test, {N_PERM} shuffles. **Δ = baseline − permuted** (mean ± std). The honesty "
                 "question: is the model's skill from the GENERALIZABLE real-time CyAN signal, or from "
                 "PER-LAKE MEMORIZATION via `clim`?\n\n"
                 "> **Read the GROUP TOTALS** — `ALL CyAN NO clim` vs `clim ONLY`. Sub-groups inside a "
                 "correlated cluster under-credit each other (redundancy), so the finer splits (current / "
                 "lags / state) are **lower bounds**, not additive shares. std = shuffle variability only "
                 "(not lake/bootstrap uncertainty).\n\n")
        for arch in ARCHS:
            base, thr, res = per_arch[arch]
            fh.write(f"## {arch} — baseline onsetMCC={base['onsetMCC']:.3f}, AUC_within="
                     f"{base['AUC_within']:.3f}, pooledAUC={base['pooled_AUC']:.3f} (thr={thr:.3f})\n\n")
            fh.write("| sub-group (within CyAN+clim) | Δ onsetMCC | Δ AUC_within | Δ pooled_AUC |\n")
            fh.write("| --- | --- | --- | --- |\n")
            for name in GROUPS:
                om, aw, pa = res[name]["onsetMCC"], res[name]["AUC_within"], res[name]["pooled_AUC"]
                fh.write(f"| {name} | {om[0]:+.3f} ± {om[1]:.3f} | {aw[0]:+.3f} ± {aw[1]:.3f} | "
                         f"{pa[0]:+.4f} ± {pa[1]:.4f} |\n")
            fh.write("\n")
        fh.write("> **Interpretation key:** if `ALL CyAN NO clim` ≈ the full C1 drop while `clim ONLY` is "
                 "small, the model is a **generalizable real-time-CyAN** model and clim is NOT load-bearing "
                 "(cross-check: block ablation `-clim` barely moves onsetMCC). If `clim ONLY` is large, the "
                 "model leans on per-lake base-rate memorization.\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
