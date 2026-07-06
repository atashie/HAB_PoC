"""Fusion model evaluation (Codex-reconciled, critical). Does fusing weather/in-situ/static beat the
CyAN-only ladder on the SAME-LAKE held-out-time split (matching EPA's temporal-holdout methodology)?

Honest scope (Codex): this tests same-lake future prediction ONLY. It does NOT test transfer to unseen
lakes (leave-lakes-out is a deferred secondary diagnostic). "No explicit lake ID / lat-lon" is true, but
static morphology + nearest-cell weather can still fingerprint place under a same-lake split -- so this
is NOT a generalizability-to-new-lakes claim. Climatology is DEMOTED to a baseline (D-35), not a Track-A
feature (matches EPA, avoids per-lake identity).

Protocol (Codex fixes): fit on train(<=2023) with early stopping; **tune threshold on VAL (2024)**;
refit on train+val; score TEST (2025). Reported: canonical suite + within-lake AUC (with **paired
lake-level delta + lake-block bootstrap CI** vs the ladder) + transition-week (flips) + **block ablation
+ block permutation importance** (to expose how little the fused blocks contribute) + a h=0..4 curve.

Model = HistGradientBoosting (native NaN handling; nonlinear). Output: models/outputs/fusion_eval.md
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import best_f1_threshold, classification_metrics  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
TABLE = os.path.join(DER, "modeling_table_fusion_fl.parquet")
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs", "fusion_eval.md"))
SEED = 42

CYAN = ["cyan_median", "cyan_mean", "cyan_sd", "cyan_median_lag1", "cyan_median_lag2",
        "cyan_median_lag4", "cyan_mean_lag1", "cyan_sd_lag1", "bloom_state", "bloom_state_ffill",
        "bloom_lag1", "bloom_roll4", "bloom_roll4_n", "cyan_gap_weeks_at_cutoff", "valid_frac"]
STATIC = ["area_sqkm", "inu_pc_umn", "tmp_dc_syr", "pet_mm_syr", "for_pc_use", "crp_pc_use", "hft_ix_u09"]
SEASON = ["woy_sin", "woy_cos"]
WEATHER = ["wx_ssrd_trail_14d_mj", "wx_ssrd_trail_30d_mj", "wx_pet_hargreaves_mm", "wx_gdd_trail_30d",
           "wx_precip_trail_30d_mm", "wx_precip_trail_90d_mm", "wx_spei_1", "wx_spei_4",
           "wx_wspd_trail_14d_mean_ms", "wx_calm_hours_trail_7d"]
INSITU = ["wqp_TP_val", "wqp_TP_stale", "wqp_water_temp_val", "wqp_ammonia_val", "wqp_orthoP_val",
          "wqp_chl_a_val", "wqp_chl_a_stale", "nwis_water_temp_val", "nwis_gage_height_val"]
BLOCKS = {"CYAN": CYAN, "STATIC": STATIC, "SEASON": SEASON, "WEATHER": WEATHER, "INSITU": INSITU}
TRACK_A = CYAN + STATIC + SEASON + WEATHER + INSITU


def add_clim(fit, frame):
    u = fit.drop_duplicates(["comid", "target_date"])
    lut = u.groupby(["comid", "month"])["target_bloom"].mean(); g = float(u["target_bloom"].mean())
    return frame.apply(lambda r: lut.get((r.comid, r.month), g), axis=1).to_numpy(dtype=float)


def gbm():
    return HistGradientBoostingClassifier(random_state=SEED, max_iter=400, learning_rate=0.06,
                                          max_leaf_nodes=31, l2_regularization=1.0,
                                          early_stopping=True, validation_fraction=0.1,
                                          n_iter_no_change=20)


def Xof(frame, feats, fitframe):
    X = frame[[f for f in feats if f != "clim"]].copy()
    if "clim" in feats:
        X["clim"] = add_clim(fitframe, frame)
    return X


def run(feats, tr, va, te):
    """fit train -> val threshold -> refit train+val -> predict test."""
    m1 = gbm().fit(Xof(tr, feats, tr), tr["target_bloom"])
    thr = best_f1_threshold(va["target_bloom"], m1.predict_proba(Xof(va, feats, tr))[:, 1])
    fit = pd.concat([tr, va]); m2 = gbm().fit(Xof(fit, feats, fit), fit["target_bloom"])
    return m2.predict_proba(Xof(te, feats, fit))[:, 1], thr, m2, fit


def per_lake_auc(y, p, comid):
    d = pd.DataFrame({"y": y, "p": p, "c": comid})
    return {c: roc_auc_score(g.y, g.p) for c, g in d.groupby("c") if g.y.nunique() == 2 and len(g) >= 20}


def evalrow(track, y, p, comid, pers, thr):
    m = classification_metrics(y, p, thr)
    la = per_lake_auc(y.to_numpy(), p, comid.to_numpy())
    wa = round(float(np.median(list(la.values()))), 3) if la else np.nan
    flip = (y.to_numpy() != pers)
    mf = classification_metrics(y[flip], p[flip], thr) if flip.sum() > 30 else {"MCC": np.nan, "AUC-ROC": np.nan}
    onset = (pers == 0)  # positive-flip subset (currently-clear weeks that become blooms), at the val-tuned thr
    mo = (classification_metrics(y[onset], p[onset], thr)
          if onset.sum() > 30 and y[onset].nunique() == 2 else {"MCC": np.nan, "AUC-ROC": np.nan})
    return {"track": track, **{k: m[k] for k in ["AUC-ROC", "AUC-PR", "Brier", "MCC"]},
            "AUC_within": wa, "n_wl": len(la), "flip_MCC": mf["MCC"], "flip_AUC": mf["AUC-ROC"],
            "n_flip": int(flip.sum()), "onset_MCC": mo["MCC"], "onset_AUC": mo["AUC-ROC"]}, la


def main() -> None:
    df0 = pd.read_parquet(TABLE)
    df0["month"] = pd.to_datetime(df0["target_date"]).dt.month
    woy = pd.to_datetime(df0["target_date"]).dt.isocalendar().week.astype(int)
    df0["woy_sin"], df0["woy_cos"] = np.sin(2 * np.pi * woy / 52.0), np.cos(2 * np.pi * woy / 52.0)

    def split(df):
        return (df[df.split == "train"], df[df.split == "val"], df[df.split == "test"])

    # ---------- detailed h=1 ----------
    d1 = df0[(df0.horizon == 1) & df0.persistence.notna()].copy()
    tr, va, te = split(d1)
    yte, cte, pte = te["target_bloom"], te["comid"], te["persistence"].to_numpy(float)
    rows, lakeaucs = [], {}
    r, _ = evalrow("persistence", yte, pte, cte, pte, 0.5); rows.append(r)
    clim_te = add_clim(pd.concat([tr, va]), te)
    thr_c = best_f1_threshold(va["target_bloom"], add_clim(tr, va))
    r, _ = evalrow("climatology (baseline)", yte, clim_te, cte, pte, thr_c); rows.append(r)
    for name, feats in [("CyAN-ladder (bar)", CYAN), ("Track A (fusion, no clim)", TRACK_A),
                        ("Track B (+clim)", TRACK_A + ["clim"])]:
        p, thr, mdl, fit = run(feats, tr, va, te)
        r, la = evalrow(name, yte, p, cte, pte, thr); rows.append(r)
        lakeaucs[name] = la
        if name == "Track A (fusion, no clim)":
            trackA_p, trackA_fit, trackA_feats, trackA_thr = p, fit, feats, thr
    res = pd.DataFrame(rows)

    # paired within-lake delta (Track A - ladder) + lake-block bootstrap CI
    la_A, la_L = lakeaucs["Track A (fusion, no clim)"], lakeaucs["CyAN-ladder (bar)"]
    common = sorted(set(la_A) & set(la_L))
    deltas = np.array([la_A[c] - la_L[c] for c in common])
    rng = np.random.default_rng(SEED)
    boot = [np.median(rng.choice(deltas, len(deltas), replace=True)) for _ in range(2000)]
    dmed, dlo, dhi = np.median(deltas), np.percentile(boot, 2.5), np.percentile(boot, 97.5)
    pos_frac = (deltas > 0).mean()

    # block ablation (Track A minus each block) + block permutation importance
    ablate = []
    for blk in BLOCKS:
        feats = [f for f in TRACK_A if f not in BLOCKS[blk]]
        p, thr, _, _ = run(feats, tr, va, te)
        ablate.append((f"-{blk}", round(roc_auc_score(yte, p), 3),
                       round(float(np.median(list(per_lake_auc(yte.to_numpy(), p, cte.to_numpy()).values()))), 3)))
    mdlA = gbm().fit(Xof(trackA_fit, trackA_feats, trackA_fit), trackA_fit["target_bloom"])
    predA = mdlA.predict_proba(Xof(te, trackA_feats, trackA_fit))[:, 1]
    baseA = roc_auc_score(yte, predA)
    # onset-MCC drop uses the SAME single shuffle per block as the AUC drop, at Track A's VAL-tuned threshold,
    # on the currently-clear (persistence==0) subset -- so the onset-MCC bars mirror the AUC bars exactly.
    onset_te = (pte == 0)

    def onset_mcc_of(pred):
        yo, po = yte.to_numpy()[onset_te], pred[onset_te]
        if len(yo) == 0 or len(np.unique(yo)) < 2:
            return np.nan
        return classification_metrics(yo, po, trackA_thr)["MCC"]

    base_onsetMCC = onset_mcc_of(predA)
    # Average the drops over N shuffles: onset-MCC on the small currently-clear subset is noisy under a
    # single shuffle, so a one-shot block drop overstates non-CyAN blocks. Mean over 20 shuffles matches
    # exp_perm_importance.py's rigor; AUC drops (large, stable test set) are essentially unchanged by it.
    N_PERM = 20
    perm = []
    XteA = Xof(te, trackA_feats, trackA_fit)
    for blk, cols in BLOCKS.items():
        blk_cols = [c for c in cols if c in XteA.columns]
        auc_d, on_d = [], []
        for _ in range(N_PERM):
            Xp = XteA.copy()
            for c in blk_cols:
                Xp[c] = rng.permutation(Xp[c].to_numpy())
            pp = mdlA.predict_proba(Xp)[:, 1]
            auc_d.append(baseA - roc_auc_score(yte, pp))
            on_d.append(base_onsetMCC - onset_mcc_of(pp))
        perm.append((blk, round(float(np.mean(auc_d)), 4), round(float(np.mean(on_d)), 4),
                     round(float(np.std(on_d)), 4)))

    # ---------- h=0..4 curve (AUC-ROC + flip_MCC) ----------
    curve = []
    for h in range(5):
        dh = df0[(df0.horizon == h) & df0.persistence.notna()].copy()
        trh, vah, teh = split(dh)
        yh, ch, ph = teh["target_bloom"], teh["comid"], teh["persistence"].to_numpy(float)
        row = {"h": h}
        rr, _ = evalrow("p", yh, ph, ch, ph, 0.5); row["persist_AUC"] = rr["AUC-ROC"]
        rr, _ = evalrow("c", yh, add_clim(pd.concat([trh, vah]), teh), ch, ph, 0.5); row["clim_AUC"] = rr["AUC-ROC"]
        pL, tL, _, _ = run(CYAN, trh, vah, teh); rr, _ = evalrow("L", yh, pL, ch, ph, tL)
        row["ladder_AUC"], row["ladder_flipMCC"] = rr["AUC-ROC"], rr["flip_MCC"]
        pA, tA, _, _ = run(TRACK_A, trh, vah, teh); rr, _ = evalrow("A", yh, pA, ch, ph, tA)
        row["fusion_AUC"], row["fusion_flipMCC"] = rr["AUC-ROC"], rr["flip_MCC"]
        curve.append(row)
    cur = pd.DataFrame(curve)

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("# Fusion model evaluation -- SAME-LAKE held-out time (Codex-reconciled, critical)\n\n")
        fh.write("HistGradientBoosting; **no explicit lake ID / lat-lon**; validation = held-out YEAR "
                 "2025 (matches EPA temporal holdout). **Scope caveat:** this is same-lake future "
                 "prediction only -- NOT transfer to unseen lakes; static morphology + nearest-cell "
                 "weather can still fingerprint place under a same-lake split. Climatology is a BASELINE "
                 "(D-35). Threshold tuned on VAL 2024; early stopping on.\n\n")
        fh.write("## h=1 (EPA-comparable)\n\n")
        fh.write("| track | AUC-ROC | AUC-PR | Brier | MCC | AUC_within(n) | flip_MCC | flip_AUC | n_flip "
                 "| onset-MCC | onset-AUC |\n")
        fh.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for _, r in res.iterrows():
            fh.write(f"| {r.track} | {r['AUC-ROC']:.3f} | {r['AUC-PR']:.3f} | {r.Brier:.3f} | {r.MCC:.3f} "
                     f"| {r.AUC_within:.3f} ({int(r.n_wl)}) | {r.flip_MCC:.3f} | {r.flip_AUC:.3f} | {r.n_flip} "
                     f"| {r.onset_MCC:.3f} | {r.onset_AUC:.3f} |\n")
        fh.write(f"\n**Fusion lift over the CyAN ladder is small and CyAN-dominated.** Paired within-lake "
                 f"AUC delta (Track A - ladder), per lake, lake-block bootstrap: median **{dmed:+.3f}** "
                 f"[{dlo:+.3f}, {dhi:+.3f}], positive in {pos_frac:.0%} of {len(common)} lakes "
                 f"(the headline 0.843->0.891 was difference-of-medians, not paired -- the honest paired "
                 f"lift is ~{dmed:+.3f}).\n\n")
        fh.write(f"### Block permutation importance (Track A, mean test drop over 20 shuffles when a block "
                 f"is shuffled; baseline AUC {baseA:.3f}, baseline onset-MCC {base_onsetMCC:.3f})\n\n")
        fh.write("| block | AUC drop | onsetMCC drop | onsetMCC std |\n| --- | --- | --- | --- |\n")
        for blk, d, od, ostd in sorted(perm, key=lambda x: -x[1]):
            fh.write(f"| {blk} | {d:+.4f} | {od:+.4f} | {ostd:.4f} |\n")
        fh.write("\n### Block ablation (Track A minus a block)\n\n| removed | AUC-ROC | AUC_within |\n| --- | --- | --- |\n")
        for nm, a, w in ablate:
            fh.write(f"| {nm} | {a:.3f} | {w:.3f} |\n")
        fh.write("\n## Horizon curve h=0..4 (AUC-ROC; flip_MCC)\n\n")
        fh.write("| h | persist AUC | clim AUC | ladder AUC | fusion AUC | ladder flip_MCC | fusion flip_MCC |\n")
        fh.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        for _, r in cur.iterrows():
            fh.write(f"| {int(r.h)} | {r.persist_AUC:.3f} | {r.clim_AUC:.3f} | {r.ladder_AUC:.3f} | "
                     f"{r.fusion_AUC:.3f} | {r.ladder_flipMCC:.3f} | {r.fusion_flipMCC:.3f} |\n")
        fh.write("\n## Honest verdict\n\n"
                 "- **Fusion adds a tiny, real ranking lift** over the CyAN ladder (paired within-lake "
                 f"{dmed:+.3f} [{dlo:+.3f}, {dhi:+.3f}]), but it is **overwhelmingly CyAN autoregression** "
                 "(permutation: CYAN dominates; weather/in-situ/static each add ~thousandths of AUC; "
                 "removing weather or in-situ barely moves pooled AUC).\n"
                 "- **Still anti-predictive on transition weeks** (flip_MCC negative): the model mostly "
                 "predicts the previous state -- calling offsets positive and onsets negative. **Plain "
                 "climatology beats the fusion GBM on flips.** Fusion polishes easy next-state ranking; "
                 "it has NOT solved the scientifically important ONSET/OFFSET problem.\n"
                 "- Same-lake temporal validation only; not a generalization-to-new-lakes claim.\n")
    print(res.to_string(index=False))
    print("\nperm importance:", perm)
    print(f"paired within delta: {dmed:+.3f} [{dlo:+.3f},{dhi:+.3f}], pos {pos_frac:.0%}")
    print(cur.to_string(index=False))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
