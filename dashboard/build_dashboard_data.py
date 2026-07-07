"""Precompute the Part B dashboard data bundle (window.DASH) from the REAL modeling pipeline.

Deterministic (seed 42), reuses the EXACT model code from ../models/model/eval_fusion.py and
eval_headtohead_onset.py (same feature blocks, same estimators). Produces a DATED DEMONSTRATION
snapshot -- NOT a live feed. Everything regenerates from checked-in real data (claim gate).

What it emits -> dashboard/data/dashboard_data.js  (assigns window.DASH):
  * meta        : snapshot dates, provenance, thresholds, base rate, data dictionary
  * lakes       : per-lake forecast (risk % by horizon: fusion / ladder / climatology / EPA + deltas),
                  current bloom state + duration, current features by family (+staleness),
                  observed CyAN-index history + in-situ chl-a samples
  * fleet       : disagreement leaderboards (vs climatology, vs EPA)
It also copies fl_lakes.geojson next to it so the page is self-contained.

Snapshot definition (grounded in the table structure -- see docs/plans/2026-07-06-dashboard-design.md):
  at feature cutoff T, horizon h targets week T+(h+1) weeks. FORECAST_CUTOFF is the latest cutoff that
  carries a full h0..h4 forecast. Tab 1 is anchored entirely to that cutoff (coherent single snapshot).

Run:  python dashboard/build_dashboard_data.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# ------------------------------------------------------------------ paths + constants
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
MODELS = os.path.join(ROOT, "models")
DER = os.path.join(MODELS, "data", "derived")
TABLE = os.path.join(DER, "modeling_table_fusion_fl.parquet")
CYAN_WEEKLY = os.path.join(DER, "cyan_lake_weekly_fl.parquet")
EPA_CSV = os.path.join(ROOT, "data-sources", "cyano-forecasts", "data", "raw", "snapshots",
                       "allweeks_20260702T000000Z.csv")
WQP_LINK = os.path.join(MODELS, "data", "interim", "wqp_fl", "site_linkage.parquet")
WQP_VALS = os.path.join(MODELS, "data", "interim", "wqp_fl", "daily_values.parquet")
LAKES_GEO = os.path.join(ROOT, "presentation", "data", "fl_lakes.geojson")
STATES_GEO = os.path.join(ROOT, "presentation", "data", "basemap_states.geojson")
OUT_DIR = os.path.join(HERE, "data")
OUT_JS = os.path.join(OUT_DIR, "dashboard_data.js")
OUT_GEO_JS = os.path.join(OUT_DIR, "geo.js")   # geometry as JS globals -> works from file:// (no fetch)

SEED = 42
FORECAST_CUTOFF = "2026-05-17"     # latest feature cutoff carrying a full h0..h4 forecast
WATCH, WARNING = 0.20, 0.40        # illustrative, tunable risk tiers (base rate ~0.23)
EPA_SNAPSHOT_LABEL = os.path.basename(EPA_CSV)
HISTORY_FROM = "2021-01-01"        # observed-history window shown in the deep dive

# The WQP/NWIS pull is NOT unit/censor-harmonized (see models/prepare/pull_link_wqp_fl.py). Drop clearly
# NON-PHYSICAL raw readings (negatives, impossible magnitudes); the rest are shown labeled "raw / unharmonized".
PHYS_BOUNDS = {
    "wqp_TP_val": (0.0, 10.0), "wqp_orthoP_val": (0.0, 10.0), "wqp_ammonia_val": (0.0, 100.0),
    "wqp_chl_a_val": (0.0, 3000.0), "wqp_water_temp_val": (0.0, 45.0),
    "nwis_water_temp_val": (0.0, 45.0), "nwis_gage_height_val": (-50.0, 100.0),
}


def phys_ok(col, v):
    """True if a raw in-situ value is within a generous physical range for its parameter."""
    if col not in PHYS_BOUNDS or v is None or not np.isfinite(v):
        return True
    lo, hi = PHYS_BOUNDS[col]
    return lo <= v <= hi

# ---- feature blocks: VERBATIM from eval_fusion.py / eval_headtohead_onset.py ----
CYAN = ["cyan_median", "cyan_mean", "cyan_sd", "cyan_median_lag1", "cyan_median_lag2", "cyan_median_lag4",
        "cyan_mean_lag1", "cyan_sd_lag1", "bloom_state", "bloom_state_ffill", "bloom_lag1",
        "bloom_roll4", "bloom_roll4_n", "cyan_gap_weeks_at_cutoff", "valid_frac"]
STATIC = ["area_sqkm", "inu_pc_umn", "tmp_dc_syr", "pet_mm_syr", "for_pc_use", "crp_pc_use", "hft_ix_u09"]
SEASON = ["woy_sin", "woy_cos"]
WEATHER = ["wx_ssrd_trail_14d_mj", "wx_ssrd_trail_30d_mj", "wx_pet_hargreaves_mm", "wx_gdd_trail_30d",
           "wx_precip_trail_30d_mm", "wx_precip_trail_90d_mm", "wx_spei_1", "wx_spei_4",
           "wx_wspd_trail_14d_mean_ms", "wx_calm_hours_trail_7d"]
INSITU = ["wqp_TP_val", "wqp_TP_stale", "wqp_water_temp_val", "wqp_ammonia_val", "wqp_orthoP_val",
          "wqp_chl_a_val", "wqp_chl_a_stale", "nwis_water_temp_val", "nwis_gage_height_val"]
TRACK_A = CYAN + STATIC + SEASON + WEATHER + INSITU
# LEAN = the optimal simple model: greedy backward ablation dropped 42 of 44 features to just these two
# (both the AUC- and onset-selected ablations converged here; not sig. worse than the full model on test).
# See models/outputs/exp_feature_ablation_trace.md / exp_feature_ablation_onset_trace.md.
LEAN = ["cyan_median", "area_sqkm"]

# families shown in the deep-dive "current state of features" panel (human labels + units + stale partner)
FAMILIES = [
    ("CyAN satellite index", [
        ("cyan_median", "CyAN median (index)", None, "cyan_gap_weeks_at_cutoff"),  # cloud-gap staleness
        ("cyan_mean", "CyAN mean (index)", None),
        ("cyan_sd", "CyAN spatial SD", None),
        ("cyan_median_lag1", "CyAN median, 1 wk ago", None),
        ("cyan_median_lag4", "CyAN median, 4 wk ago", None),
        ("bloom_roll4", "Bloom weeks in last 4", None),
        ("valid_frac", "Valid pixel fraction", None),
    ]),
    ("Catchment / morphology (static)", [
        ("area_sqkm", "Lake area", "sq km"),
        ("inu_pc_umn", "Inundation extent", "%"),
        ("tmp_dc_syr", "Mean air temp (catchment)", "0.1 C"),
        ("pet_mm_syr", "Potential ET (annual)", "mm"),
        ("for_pc_use", "Forest cover", "%"),
        ("crp_pc_use", "Cropland cover", "%"),
        ("hft_ix_u09", "Human footprint index", None),
    ]),
    # NOTE: Season (woy_sin/cos) is deliberately NOT shown as a "current feature" -- it encodes the
    # TARGET week's position in the calendar (horizon-dependent), not a current lake condition.
    ("Weather (ERA5)", [
        ("wx_ssrd_trail_14d_mj", "Solar radiation, trailing 14 d", "MJ"),
        ("wx_gdd_trail_30d", "Growing degree days, 30 d", None),
        ("wx_precip_trail_30d_mm", "Precip, trailing 30 d", "mm"),
        ("wx_precip_trail_90d_mm", "Precip, trailing 90 d", "mm"),
        ("wx_spei_1", "Drought index SPEI-1", None),
        ("wx_spei_4", "Drought index SPEI-4", None),
        ("wx_wspd_trail_14d_mean_ms", "Wind speed, trailing 14 d", "m/s"),
        ("wx_calm_hours_trail_7d", "Calm hours, trailing 7 d", "hr"),
    ]),
    # in-situ units carry a trailing * -> "raw / unharmonized" (explained in the UI note); non-physical dropped
    ("In-situ grab samples (WQP / NWIS) - raw, unharmonized", [
        ("wqp_TP_val", "Total phosphorus", "mg/L*", "wqp_TP_stale"),
        ("wqp_orthoP_val", "Orthophosphate", "mg/L*", "wqp_orthoP_stale"),
        ("wqp_ammonia_val", "Ammonia", "mg/L*", "wqp_ammonia_stale"),
        ("wqp_chl_a_val", "Chlorophyll-a (in-situ)", "ug/L*", "wqp_chl_a_stale"),
        ("wqp_water_temp_val", "Water temp (WQP)", "C*", "wqp_water_temp_stale"),
        ("nwis_water_temp_val", "Water temp (NWIS)", "C*", "nwis_water_temp_stale"),
        ("nwis_gage_height_val", "Gage height (NWIS)", "ft*", "nwis_gage_height_stale"),
    ]),
]


# ------------------------------------------------------------------ model helpers (verbatim recipes)
def add_season(df):
    d = pd.to_datetime(df["target_date"])
    df["month"] = d.dt.month
    woy = d.dt.isocalendar().week.astype(int)
    df["woy_sin"] = np.sin(2 * np.pi * woy / 52.0)
    df["woy_cos"] = np.cos(2 * np.pi * woy / 52.0)
    return df


def clim_lut(fit):
    u = fit.drop_duplicates(["comid", "target_date"])
    return u.groupby(["comid", "month"])["target_bloom"].mean(), float(u["target_bloom"].mean())


def clim_scores(frame, lut, g):
    return frame.apply(lambda r: lut.get((r.comid, r.month), g), axis=1).to_numpy(float)


def ladder_pipe():
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                     ("lr", LogisticRegression(max_iter=2000, random_state=SEED))])


def gbm():
    return HistGradientBoostingClassifier(random_state=SEED, max_iter=400, learning_rate=0.06,
                                          max_leaf_nodes=31, l2_regularization=1.0, early_stopping=True,
                                          validation_fraction=0.1, n_iter_no_change=20)


def Xof(frame, feats, lut, g):
    X = frame[[f for f in feats if f != "clim"]].copy()
    if "clim" in feats:
        X["clim"] = clim_scores(frame, lut, g)
    return X


def jnum(x, nd=1):
    """JSON-safe rounded number or None (NaN -> null)."""
    if x is None:
        return None
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(xf):
        return None
    return round(xf, nd)


# ------------------------------------------------------------------ observed history + duration
def chl_param_code(vals):
    codes = vals["parameter_code"].dropna().unique().tolist()
    for c in codes:
        if "chl" in str(c).lower():
            return c
    return None


def bloom_duration_weeks(sub, cutoff):
    """Trailing run of observed bloom==True weeks ending at the cutoff week (the week whose start<=cutoff).

    Uses start_date<=cutoff so the cutoff week itself is included (its end_date is 6 days later); an
    end_date<=cutoff test would drop the cutoff week and undercount by one. A clear cutoff week -> run 0.
    """
    s = sub[sub["start_date"] <= cutoff].sort_values("start_date")
    b = s["bloom"].tolist()
    run = 0
    for v in reversed(b):
        if v is True or v == 1 or v == 1.0:
            run += 1
        else:
            break  # first non-bloom (or missing) week ends the run
    return run


# ------------------------------------------------------------------ verification gate
def verify_against_eval(df, lut_dummy=None):
    """Reproduce eval_fusion protocol (fit train, tune val, refit train+val, predict TEST) and check the
    h=1 fusion Track-A test AUC matches fusion_eval.md (~0.98). Consistency with the published numbers."""
    d1 = df[(df.horizon == 1) & df["persistence"].notna()].copy()
    tr, va, te = d1[d1.split == "train"], d1[d1.split == "val"], d1[d1.split == "test"]
    lut_tr, g_tr = clim_lut(pd.concat([tr, va]))
    fit = pd.concat([tr, va])
    m = gbm().fit(Xof(fit, TRACK_A, lut_tr, g_tr), fit["target_bloom"])
    p = m.predict_proba(Xof(te, TRACK_A, lut_tr, g_tr))[:, 1]
    auc = roc_auc_score(te["target_bloom"], p)
    ok = 0.975 <= auc <= 0.990   # tight band around the published 0.983 (catch regressions)
    return auc, ok


# ------------------------------------------------------------------ main
def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    df = pd.read_parquet(TABLE)
    df = add_season(df)
    df["feature_date"] = pd.to_datetime(df["feature_date"])
    df["target_date"] = pd.to_datetime(df["target_date"])
    df["target_end"] = df["target_date"] + pd.Timedelta(days=6)
    cutoff = pd.Timestamp(FORECAST_CUTOFF)

    # ---- PER-HORIZON models (matches eval_fusion's per-horizon protocol): a separate fusion + ladder +
    #      climatology per lead h, fit on ALL labeled history (train+val+test, <=2025), scoring the
    #      held-out 2026 snapshot. A pooled all-horizon model gives near-flat, sometimes badly-wrong
    #      curves because features at a fixed cutoff are horizon-invariant -- per-horizon fixes that.
    fit_all = df[df.split.isin(["train", "val", "test"])].copy()
    base_rate = float(fit_all["target_bloom"].mean())
    snap = df[(df.feature_date == cutoff) & (df.horizon.isin([0, 1, 2, 3, 4]))].copy()
    if snap.empty:
        sys.exit(f"ERROR: no snapshot rows at feature cutoff {FORECAST_CUTOFF}")
    oos = df[(df.split == "oos_partial") & (df.horizon.isin([0, 1, 2, 3, 4]))].copy()  # 2026 held-out, for skill gate
    for c in ("fusion_p", "lean_p", "clim_p"):
        snap[c] = np.nan
    ship_auc, ship_persist_auc, ship_onset_auc = {}, {}, {}
    for h in range(5):
        fh = fit_all[fit_all.horizon == h]
        luth, gh = clim_lut(fh)
        mFh = gbm().fit(Xof(fh, TRACK_A, luth, gh), fh["target_bloom"])
        mLean = ladder_pipe().fit(fh[LEAN], fh["target_bloom"])   # lean 2-feature simple model (median + area)
        si = (snap.horizon == h).to_numpy()
        if si.any():
            snap.loc[si, "fusion_p"] = mFh.predict_proba(Xof(snap[si], TRACK_A, luth, gh))[:, 1]
            snap.loc[si, "lean_p"] = mLean.predict_proba(snap[si][LEAN])[:, 1]
            snap.loc[si, "clim_p"] = clim_scores(snap[si], luth, gh)
        # GATE B: score the SHIPPED per-horizon model on the held-out 2026 period -- but ALWAYS beside its
        # baseline. Overall AUC is autocorrelation-dominated (persistence alone ~0.90-0.95); the honest
        # signal is ONSET-AUC on currently-clear lakes, where persistence has NO skill by construction.
        sub = oos[(oos.horizon == h) & oos["persistence"].notna()]
        yo = sub["target_bloom"].astype(int).to_numpy()
        if len(sub) and len(np.unique(yo)) > 1:
            po = mFh.predict_proba(Xof(sub, TRACK_A, luth, gh))[:, 1]
            perso = sub["persistence"].to_numpy(float)
            ship_auc[h] = round(float(roc_auc_score(yo, po)), 3)
            ship_persist_auc[h] = round(float(roc_auc_score(yo, perso)), 3)   # baseline the AUC MUST carry
            onset = perso == 0
            if onset.sum() and len(np.unique(yo[onset])) > 1:
                ship_onset_auc[h] = round(float(roc_auc_score(yo[onset], po[onset])), 3)  # fusion skill on NEW blooms

    # ---- EPA forecast (percent_chance, current-week nowcast) matched by comid x target week ----
    epa = pd.read_csv(EPA_CSV)
    epa = epa[epa.state == "FL"].copy()
    epa["target_end"] = pd.to_datetime(epa["week_end_date"])
    epa["epa_p"] = epa["percent_chance"] / 100.0
    snap = snap.merge(epa[["comid", "target_end", "epa_p"]], on=["comid", "target_end"], how="left")

    # ---- observed weekly CyAN + in-situ chl-a ----
    cw = pd.read_parquet(CYAN_WEEKLY)
    cw["start_date"] = pd.to_datetime(cw["start_date"])
    cw["end_date"] = pd.to_datetime(cw["end_date"])
    hist_from = pd.Timestamp(HISTORY_FROM)

    wqp_link = pd.read_parquet(WQP_LINK)[["site_id", "comid"]].dropna()
    wqp_link["comid"] = wqp_link["comid"].astype("int64")
    wqp_vals = pd.read_parquet(WQP_VALS)
    ccode = chl_param_code(wqp_vals)
    chl = pd.DataFrame(columns=["comid", "date", "value"])
    if ccode is not None:
        chl = wqp_vals[wqp_vals.parameter_code == ccode].merge(wqp_link, on="site_id", how="inner")
        chl["date"] = pd.to_datetime(chl["date"])
        chl = chl[chl["date"] >= hist_from]
        chl = chl[(chl["value"] >= 0) & (chl["value"] <= 3000)]   # drop non-physical (negatives / sentinels)

    # ---- lake geometry (names) ----
    with open(LAKES_GEO, "r", encoding="utf-8") as fh:
        geo = json.load(fh)
    name_of = {int(f["properties"]["COMID"]): (f["properties"].get("name") or "") for f in geo["features"]}

    # ---- assemble per-lake records ----
    horizons = [0, 1, 2, 3, 4]
    snap_by = {(int(r.comid), int(r.horizon)): r for r in snap.itertuples(index=False)}
    # feature vector + persistence are as-of the cutoff -> identical across horizons; use h=0 (fallback any)
    cur_row = {}
    for c in snap["comid"].unique():
        rows = snap[snap.comid == c]
        r0 = rows[rows.horizon == 0]
        cur_row[int(c)] = (r0.iloc[0] if len(r0) else rows.iloc[0])

    lakes = []
    for c in sorted(snap["comid"].unique()):
        c = int(c)
        cr = cur_row[c]
        pers = cr["persistence"]
        clear_now = bool(pers == 0)
        blooming_now = bool(pers == 1)

        # forecast by horizon
        fc = []
        for h in horizons:
            key = (c, h)
            if key not in snap_by:
                continue
            rr = snap_by[key]
            fus = float(rr.fusion_p)
            fc.append({
                "h": h,
                "target_end": pd.Timestamp(rr.target_end).strftime("%Y-%m-%d"),
                "fusion": jnum(fus * 100, 1),
                "lean": jnum(float(rr.lean_p) * 100, 1),
                "clim": jnum(float(rr.clim_p) * 100, 1),
                "epa": jnum(float(rr.epa_p) * 100, 1) if pd.notna(rr.epa_p) else None,
                "d_clim": jnum((fus - float(rr.clim_p)) * 100, 1),
                "d_epa": jnum((fus - float(rr.epa_p)) * 100, 1) if pd.notna(rr.epa_p) else None,
            })

        # current-state duration (observed weekly, run of bloom weeks up to cutoff)
        sub = cw[cw.comid == c]
        dur = bloom_duration_weeks(sub, cutoff) if len(sub) else 0

        # current features by family (as-of cutoff)
        fam = []
        for fam_name, items in FAMILIES:
            feats_out = []
            for it in items:
                col, label, unit = it[0], it[1], it[2]
                stale_col = it[3] if len(it) > 3 else None
                val = cr[col] if col in cr.index else None
                if val is not None and pd.notna(val) and not phys_ok(col, float(val)):
                    val = None            # drop clearly non-physical raw in-situ reading (unit/censor artifact)
                stale = None
                if stale_col and stale_col in cr.index and pd.notna(cr[stale_col]):
                    stale = int(round(float(cr[stale_col])))  # weeks since last sample (CyAN: cloud-gap)
                feats_out.append({"label": label, "unit": unit, "val": jnum(val, 3), "stale_wk": stale})
            fam.append({"family": fam_name, "features": feats_out})

        # observed history: weekly CyAN index (dense) since HISTORY_FROM
        h_obs = sub[(sub.start_date >= hist_from)].sort_values("start_date")
        obs_d = [d.strftime("%Y-%m-%d") for d in h_obs["start_date"]]
        obs_cyan = [jnum(v, 1) for v in h_obs["cyan_median"]]
        # in-situ chl-a samples (real, sparse)
        cc = chl[chl.comid == c].sort_values("date") if len(chl) else chl
        chl_d = [d.strftime("%Y-%m-%d") for d in cc["date"]] if len(cc) else []
        chl_v = [jnum(v, 1) for v in cc["value"]] if len(cc) else []

        # forecast @ default horizon 1 for the alert board
        f1 = next((x for x in fc if x["h"] == 1), None)
        risk1 = f1["fusion"] if f1 else None
        tier = None
        if risk1 is not None:
            p = risk1 / 100.0
            tier = "Warning" if p >= WARNING else ("Watch" if p >= WATCH else "Low")

        lakes.append({
            "comid": c,
            "name": name_of.get(c, "") or (cr["gnis_name"] if "gnis_name" in cr.index and pd.notna(cr["gnis_name"]) else ""),
            "clear_now": clear_now,
            "blooming_now": blooming_now,
            "duration_wk": dur,
            "cyan_now": jnum(cr["cyan_median"], 1) if "cyan_median" in cr.index else None,
            "risk1": risk1,
            "tier": tier,
            "forecast": fc,
            "families": fam,
            "obs": {"d": obs_d, "cyan": obs_cyan},
            "chl": {"d": chl_d, "v": chl_v},
        })

    # (the fleet disagreement table is built client-side from every lake's h=1 forecast — no server-side list)

    # ---- verification gate ----
    auc, ok = verify_against_eval(df)

    # ---- snapshot dates ----
    forecast_target_last = snap[snap.horizon == 4]["target_end"].max()
    obs_last = cw["end_date"].max()

    n_clear = sum(1 for lk in lakes if lk["clear_now"])
    n_bloom = sum(1 for lk in lakes if lk["blooming_now"])
    n_epa = sum(1 for lk in lakes if any(x.get("epa") is not None for x in lk["forecast"]))
    n_full = sum(1 for lk in lakes if len(lk["forecast"]) == 5)

    meta = {
        "generated_note": "Dated demonstration on a FIXED real snapshot. NOT a live feed.",
        "forecast_cutoff": FORECAST_CUTOFF,
        "forecast_target_last": pd.Timestamp(forecast_target_last).strftime("%Y-%m-%d"),
        "obs_last": pd.Timestamp(obs_last).strftime("%Y-%m-%d"),
        "n_lakes": len(lakes),
        "n_lakes_full": n_full,                 # lakes with all 5 horizons (rest miss >=1)
        "n_resolvable": 133,                    # CyAN-resolvable universe; this snapshot has n_lakes of them
        "n_clear_now": n_clear,
        "n_blooming_now": n_bloom,
        "n_with_epa": n_epa,
        "base_rate": round(base_rate, 3),
        "tiers": {"watch": WATCH, "warning": WARNING},
        "epa_snapshot": EPA_SNAPSHOT_LABEL,
        "chl_param_code": str(ccode),
        "verify_fusion_h1_test_auc": round(float(auc), 3),   # gate A: reproduces published 0.983 (train+val->test)
        "verify_pass": bool(ok),
        "shipped_oos_auc": ship_auc,            # gate B: SHIPPED per-horizon fusion, AUC on 2026 held-out (oos_partial)
        "shipped_oos_persist_auc": ship_persist_auc,  # the persistence baseline the AUC MUST be read against
        "shipped_oos_onset_auc": ship_onset_auc,      # fusion skill on NEW blooms (persistence has none here)
        "per_horizon": True,
        "horizon_note": "At cutoff T, horizon h targets week T+(h+1) wk. h0 is a coincident nowcast (diagnostic), "
                        "not an operational forecast. Forecasts are separate per-horizon models. CyAN carries ~2 wk latency.",
        "insitu_note": "In-situ WQP/NWIS values (marked *) are RAW and not unit/censor-harmonized; non-physical "
                       "readings are dropped and the rest are indicative only.",
        "provenance": {
            "table": "models/data/derived/modeling_table_fusion_fl.parquet",
            "observed": "models/data/derived/cyan_lake_weekly_fl.parquet",
            "epa": "data-sources/cyano-forecasts/.../%s" % EPA_SNAPSHOT_LABEL,
            "wqp_chl": "models/data/interim/wqp_fl/daily_values.parquet",
            "models": "per-horizon fusion=HistGradientBoosting (TRACK_A); lean=LogReg (cyan_median+area_sqkm); climatology=per-lake-month mean; EPA=percent_chance",
        },
    }

    bundle = {"meta": meta, "lakes": lakes}
    payload = "window.DASH = " + json.dumps(bundle, separators=(",", ":")) + ";\n"
    with open(OUT_JS, "w", encoding="utf-8") as fh:
        fh.write(payload)
    # geometry as JS globals (loaded via <script src> so the page works from file:// with no fetch)
    with open(STATES_GEO, "r", encoding="utf-8") as fh:
        states = json.load(fh)
    with open(OUT_GEO_JS, "w", encoding="utf-8") as fh:
        fh.write("window.FL_LAKES = " + json.dumps(geo, separators=(",", ":")) + ";\n")
        fh.write("window.FL_STATES = " + json.dumps(states, separators=(",", ":")) + ";\n")

    # ASCII-only console summary (Windows cp1252-safe)
    kb = os.path.getsize(OUT_JS) / 1024.0
    print("VERIFY fusion h=1 test AUC = %.3f  ->  %s (expect ~0.98 per fusion_eval.md)"
          % (auc, "PASS" if ok else "FAIL"))
    print("snapshot: forecast cutoff %s (targets to %s); observations to %s"
          % (FORECAST_CUTOFF, meta["forecast_target_last"], meta["obs_last"]))
    print("lakes=%d (full-h0-4=%d)  clear_now=%d  blooming_now=%d  with_EPA=%d  base_rate=%.3f  chl_code=%s"
          % (len(lakes), n_full, n_clear, n_bloom, n_epa, base_rate, ccode))
    print("GATE B 2026 held-out: fusion AUC %s vs PERSISTENCE %s (AUC is autocorrelation-dominated)" % (ship_auc, ship_persist_auc))
    print("         fusion ONSET-AUC (new blooms; persistence has none): %s" % ship_onset_auc)
    print("wrote %s (%.0f KB) and geo.js" % (OUT_JS, kb))
    if not ok:
        sys.exit("VERIFICATION FAILED: fusion h=1 test AUC outside expected band; investigate before use.")


if __name__ == "__main__":
    main()
