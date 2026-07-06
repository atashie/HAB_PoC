"""Experiment 3: FEATURE-level greedy backward ablation (user 2026-07-06).

Family-level ablation (`exp_ablation.py`) drops whole BLOCKS; this drops INDIVIDUAL features one at a
time and KEEPS each drop if it does not significantly hurt held-out performance -- greedy backward
elimination, far cheaper than exhaustive 2^44 all-subsets (which the user flagged as burdensome).

Method (honest + leakage-safe):
  * Start from the strongest family, fusion_full+clim (44 features).
  * SELECTION metric = validation AUC at the primary horizon h=1 (val, NOT test, drives selection).
    clim/anomaly pseudo-features are computed from TRAIN only inside Xof (leakage-safe).
  * At each step, try dropping each still-kept feature (one train fit + val score each); the candidate
    removal with the highest val AUC is dropped PERMANENTLY iff the resulting model stays within TOL of
    the ORIGINAL full-model val AUC (fixed baseline => cumulative degradation is bounded by TOL, not
    compounded per step). Stop when even the least-harmful remaining drop would breach the TOL band.
  * The FINAL lean set is then evaluated UNBIASED on held-out test across archs + horizons via the
    standard harness, and a lake-block bootstrap of the full-minus-lean test-AUC gap (h=1) confirms
    whether the trimmed model is significantly worse. Only HistGBM drives selection (arch-robust per
    Exp-1/2); the final table adds XGBoost + logistic.

Run: python models/model/exp_feature_ablation.py
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from experiment_lib import (CYAN, HORIZONS, INSITU, PRIM, SEASON, STATIC, WEATHER, Xof,  # noqa: E402
                            _hgb, fit_predict, load, prep, split)
from experiment_lib import run_experiment  # noqa: E402

# Selection criterion: "pooled" (val AUC over ALL weeks -- collapses to near-persistence, since pooled
# AUC is dominated by persistence-easy weeks) OR "onset" (val AUC over currently-CLEAR weeks only = the
# EARLY-WARNING skill, the decision-relevant objective). Pass as argv[1]; default pooled.
SEL = (sys.argv[1] if len(sys.argv) > 1 else "pooled").lower()
assert SEL in ("pooled", "onset"), f"select metric must be pooled|onset, got {SEL}"
_SFX = "" if SEL == "pooled" else "_onset"
_METLBL = "val AUC (all weeks)" if SEL == "pooled" else "val ONSET AUC (currently-clear weeks)"
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs",
                                   f"exp_feature_ablation{_SFX}.md"))
TRACE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs",
                                     f"exp_feature_ablation{_SFX}_trace.md"))
# onset AUC is a noisier subset metric -> a slightly looser "not significant" band.
TOL = 0.001 if SEL == "pooled" else 0.005
FF_CLIM = CYAN + STATIC + SEASON + WEATHER + INSITU + ["clim"]
BLOCK_OF = {**{c: "CYAN" for c in CYAN}, **{c: "STATIC" for c in STATIC},
            **{c: "SEASON" for c in SEASON}, **{c: "WEATHER" for c in WEATHER},
            **{c: "INSITU" for c in INSITU}, "clim": "clim"}


def val_auc(feats, tr, va):
    """Train-only fit (fast; no refit), score the SELECTION metric on val at h=1. clim/anom train-only.
    pooled = AUC over all val weeks; onset = AUC over currently-clear (persistence==0) val weeks only."""
    Xtr, Xva = Xof(tr, feats, tr), Xof(va, feats, tr)
    p = _hgb().fit(Xtr, tr["target_bloom"]).predict_proba(Xva)[:, 1]
    y = va["target_bloom"].to_numpy()
    if SEL == "onset":
        cl = va["persistence"].to_numpy(float) == 0
        return float(roc_auc_score(y[cl], p[cl]))
    return float(roc_auc_score(y, p))


def greedy_backward(feats0, tr, va, tol=TOL):
    kept = list(feats0)
    base = val_auc(kept, tr, va)               # FIXED baseline = full-model val AUC
    trace = [{"step": 0, "dropped": "(full model)", "block": "", "val_auc": round(base, 5),
              "delta_vs_full": 0.0, "n_kept": len(kept)}]
    print(f"[greedy] full model: val AUC {base:.5f}, {len(kept)} features")
    step = 0
    while len(kept) > 1:
        cand = sorted(((val_auc([x for x in kept if x != f], tr, va), f) for f in kept),
                      key=lambda t: -t[0])
        best_auc, best_f = cand[0]
        if best_auc >= base - tol:             # dropping best_f keeps us within TOL of the FULL model
            kept = [x for x in kept if x != best_f]
            step += 1
            trace.append({"step": step, "dropped": best_f, "block": BLOCK_OF.get(best_f, "?"),
                          "val_auc": round(best_auc, 5), "delta_vs_full": round(best_auc - base, 5),
                          "n_kept": len(kept)})
            print(f"[greedy] step {step}: drop {best_f:28s} ({BLOCK_OF.get(best_f,'?'):6s}) "
                  f"-> val AUC {best_auc:.5f} (dvs_full {best_auc-base:+.5f}); {len(kept)} kept")
        else:
            print(f"[greedy] STOP: least-harmful drop ({best_f}) -> {best_auc:.5f} < {base-tol:.5f}")
            break
    return kept, trace, base


def lakeblock_bootstrap_gap(tr, va, te, feats_full, feats_lean, n=500, seed=42):
    """Full-minus-lean test-AUC gap (h=1) on the SELECTION metric, resampling LAKES with replacement
    (cluster-robust). onset => restrict to currently-clear (persistence==0) test weeks."""
    _, pf, _ = fit_predict("histgbm", feats_full, tr, va, te)
    _, pl, _ = fit_predict("histgbm", feats_lean, tr, va, te)
    y = te["target_bloom"].to_numpy(); comid = te["comid"].to_numpy()
    if SEL == "onset":
        keep = te["persistence"].to_numpy(float) == 0
        y, pf, pl, comid = y[keep], pf[keep], pl[keep], comid[keep]
    lakes = np.unique(comid); idx = {c: np.where(comid == c)[0] for c in lakes}
    rng = np.random.default_rng(seed)
    full_auc, lean_auc = roc_auc_score(y, pf), roc_auc_score(y, pl)
    gaps = []
    for _ in range(n):
        pick = rng.choice(lakes, size=len(lakes), replace=True)
        rows = np.concatenate([idx[c] for c in pick])
        yy = y[rows]
        if len(np.unique(yy)) < 2:
            continue
        gaps.append(roc_auc_score(yy, pf[rows]) - roc_auc_score(yy, pl[rows]))
    q = np.percentile(gaps, [2.5, 50, 97.5])
    return full_auc, lean_auc, q, len(feats_full), len(feats_lean)


def main():
    import gc
    df = prep(load())
    tr, va, te = split(df[(df.horizon == PRIM) & df.persistence.notna()])
    del df; gc.collect()   # free the full 339k-row table; greedy/bootstrap only need the h=1 slices
    kept, trace, full_base = greedy_backward(FF_CLIM, tr, va)
    dropped = [t["dropped"] for t in trace[1:]]
    kept_by_block = {}
    for f in kept:
        kept_by_block.setdefault(BLOCK_OF.get(f, "?"), []).append(f)
    drop_by_block = {}
    for f in dropped:
        drop_by_block.setdefault(BLOCK_OF.get(f, "?"), []).append(f)

    full_auc, lean_auc, q, nfull, nlean = lakeblock_bootstrap_gap(tr, va, te, FF_CLIM, kept)

    with open(TRACE, "w", encoding="utf-8") as fh:
        fh.write(f"# Exp 3 - feature-level greedy backward ablation (selection metric = **{SEL.upper()}**)\n\n")
        fh.write(f"Selection criterion = **{_METLBL}** at h={PRIM}. Start = fusion_full+clim ({nfull} "
                 f"features). Greedy backward: at each step drop the single feature whose removal least "
                 f"hurts that metric, keep it dropped iff the reduced model stays within **TOL={TOL}** of "
                 f"the full-model score (`{full_base:.5f}`). Val (not test) drives selection; clim/anom "
                 "pseudo-features are train-only (leakage-safe). Final lean set evaluated unbiased on "
                 "test below.\n\n")
        if SEL == "pooled":
            fh.write("> **CAVEAT:** pooled AUC is dominated by persistence-easy weeks, so selecting on it "
                     "collapses toward a near-persistence model and discards features that matter for "
                     "ONSET early-warning. See the `_onset` variant for the decision-relevant ablation.\n\n")
        fh.write(f"**Result: dropped {len(dropped)} of {nfull} features with <{TOL} cost on the "
                 f"selection metric; {len(kept)} kept.**\n\n")
        fh.write(f"## Elimination order (score = {_METLBL})\n\n"
                 "| step | dropped feature | block | sel score | delta vs full | n kept |\n")
        fh.write("| --- | --- | --- | --- | --- | --- |\n")
        for t in trace:
            fh.write(f"| {t['step']} | `{t['dropped']}` | {t['block']} | {t['val_auc']:.5f} | "
                     f"{t['delta_vs_full']:+.5f} | {t['n_kept']} |\n")
        fh.write("\n## Kept vs dropped, by block\n\n| block | kept | dropped |\n| --- | --- | --- |\n")
        for blk in ["CYAN", "STATIC", "SEASON", "WEATHER", "INSITU", "clim"]:
            k = kept_by_block.get(blk, []); d = drop_by_block.get(blk, [])
            fh.write(f"| {blk} | {len(k)}: {', '.join(f'`{x}`' for x in k) or '--'} | "
                     f"{len(d)}: {', '.join(f'`{x}`' for x in d) or '--'} |\n")
        _mname = "onset-AUC (currently-clear weeks)" if SEL == "onset" else "pooled AUC"
        fh.write(f"\n## Full vs lean on HELD-OUT TEST (h=1), lake-block bootstrap of the {_mname} gap\n\n")
        fh.write(f"- Full ({nfull} feat) test {_mname} = **{full_auc:.4f}**; Lean ({nlean} feat) = "
                 f"**{lean_auc:.4f}**.\n")
        fh.write(f"- Full - Lean gap (resampling lakes): median **{q[1]:+.4f}**, "
                 f"95% CI [{q[0]:+.4f}, {q[2]:+.4f}].\n")
        verdict = (f"CI includes 0 -> the lean model is NOT significantly worse on held-out test {_mname}."
                   if q[0] <= 0 <= q[2] else
                   f"CI excludes 0 -> the trim DOES cost significant test {_mname}; TOL too loose.")
        fh.write(f"- **{verdict}**\n")
        fh.write("\n> NOTE: this bootstrap tests only the selection metric. Read the full-vs-lean grid "
                 "below for the OTHER metrics (onsetMCC, AUC_within, flipMCC) -- a lean set that ties on "
                 "the selection metric can still lose skill on the others.\n")
    print("wrote", TRACE)
    print(f"KEPT ({len(kept)}): {kept}")
    print(f"DROPPED ({len(dropped)}): {dropped}")

    # Final unbiased comparison across architectures + horizons (full metric suite, both EPA rows)
    suites = {"fusion_full+clim (full)": FF_CLIM, "greedy_lean": kept}
    run_experiment(suites, ["histgbm", "xgboost", "logistic"], OUT,
                   f"Exp 3 - feature-level greedy backward ablation, selection metric = {SEL.upper()} "
                   f"(lean={len(kept)} of {nfull} feats; TOL={TOL})", baselines=True)


if __name__ == "__main__":
    main()
