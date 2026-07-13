"""Tests for the trusted core: leakage-safe feature/target alignment, temporal split,
filename parsing, and the metrics. Pure functions, no network, fast.

The alignment tests are the important ones — they assert the antecedent-only and
freshest-available rules that keep the autoregressive model from leaking the future.
"""
import os, sys
from datetime import date
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common  # noqa: E402


def _panel(n_weeks=30, comids=(1, 2), start="2020-01-05", areas=(5.0, 50.0)):
    """Synthetic weekly panel: cyan_median ramps then falls; bloom = median>=130."""
    weeks = pd.date_range(start, periods=n_weeks, freq="7D")
    rows = []
    for ci, comid in enumerate(comids):
        for k, w in enumerate(weeks):
            med = 40 + 12 * k                       # crosses 130 around week ~8
            rows.append(dict(comid=comid, week_start=w, cyan_median=float(med),
                             bloom=int(med >= 130), area_sqkm=areas[ci]))
    return pd.DataFrame(rows)


# --- filename parsing -----------------------------------------------------
def test_parse_week_start_olci():
    d = common.parse_week_start("L20161152016121.L3m_7D_CYAN_CI_cyano_CYAN_CONUS_300m.tif")
    assert d == date(2016, 4, 24)          # 2016 doy 115


def test_parse_week_start_skips_meris():
    assert common.parse_week_start("M20120852012091.L3m_7D_..._300m.tif") is None


# --- alignment: antecedent-only + latency ---------------------------------
def test_feature_week_is_h_plus_1_weeks_before_target():
    panel = _panel()
    for h in range(5):
        f = common.build_horizon_frame(panel, h)
        gap = (f["target_date"] - f["feature_date"]).dt.days
        # No gaps in this synthetic panel -> feature is EXACTLY (h+1) weeks back.
        assert (gap == 7 * (h + 1)).all(), f"h={h}: {sorted(gap.unique())}"
        # And never the target week itself (the circularity guard).
        assert (f["feature_date"] < f["target_date"]).all()


def test_no_feature_within_h_plus_1_weeks_of_target():
    panel = _panel()
    for h in range(5):
        f = common.build_horizon_frame(panel, h)
        newest_allowed = f["target_date"] - pd.Timedelta(weeks=h + 1)
        assert (f["feature_date"] <= newest_allowed).all()


def test_persistence_equals_feature_week_label():
    panel = _panel()
    f = common.build_horizon_frame(panel, 1)
    # persistence is the label carried from the (latency-aware) feature week.
    merged = f.merge(
        panel.rename(columns={"week_start": "feature_date", "bloom": "b_at_feat"}),
        on=["comid", "feature_date"], how="left")
    assert (merged["persistence"] == merged["b_at_feat"]).all()


def test_gap_is_backfilled_not_leaked():
    """Drop one week; the cutoff that lands on it must fall back to an OLDER composite,
    never forward to a newer one."""
    panel = _panel()
    drop = (panel["comid"] == 1) & (panel["week_start"] == pd.Timestamp("2020-02-16"))
    gapped = panel[~drop]
    for h in range(5):
        f = common.build_horizon_frame(gapped, h)
        assert (f["feature_date"] < f["target_date"]).all()
        # feature never equals the removed week for lake 1
        assert not ((f["comid"] == 1) &
                    (f["feature_date"] == pd.Timestamp("2020-02-16"))).any()


# --- temporal split -------------------------------------------------------
def test_temporal_split_boundaries_no_overlap():
    panel = _panel(n_weeks=520, start="2016-01-03")   # ~10 yr, spans all three windows
    f = common.build_horizon_frame(panel, 1)
    tr, va, te = common.temporal_split(f, "2022-07-01", "2024-07-01")
    assert pd.to_datetime(tr["target_date"]).max() < pd.Timestamp("2022-07-01")
    assert pd.to_datetime(va["target_date"]).min() >= pd.Timestamp("2022-07-01")
    assert pd.to_datetime(va["target_date"]).max() < pd.Timestamp("2024-07-01")
    assert pd.to_datetime(te["target_date"]).min() >= pd.Timestamp("2024-07-01")
    assert len(tr) + len(va) + len(te) == len(f)


# --- metrics --------------------------------------------------------------
def test_auc_perfect_and_random():
    y = np.array([0, 0, 1, 1])
    assert common.auc(y, np.array([0.1, 0.2, 0.8, 0.9])) == 1.0
    assert common.auc(y, np.array([0.9, 0.8, 0.2, 0.1])) == 0.0
    assert np.isnan(common.auc(np.array([0, 0, 0]), np.array([1.0, 2.0, 3.0])))  # one class -> nan


def test_onset_auc_uses_only_clear_weeks():
    y =   np.array([1, 1, 0, 1, 0])
    p =   np.array([.9, .8, .2, .7, .1])
    per = np.array([1, 1, 0, 0, 0])     # first two already blooming -> excluded
    # only rows 2,3,4 count: y=[0,1,0], p=[.2,.7,.1] -> perfect ranking
    assert common.onset_auc(y, p, per) == 1.0


def test_mcc_edges():
    # single-class labels -> undefined (nan); constant prediction on mixed labels -> 0.0
    assert np.isnan(common.mcc([1, 1, 1], [1, 0, 1]))
    assert common.mcc([0, 1, 0, 1], [1, 1, 1, 1]) == 0.0
    assert common.mcc([0, 0, 1, 1], [0, 0, 1, 1]) == 1.0


def test_onset_mcc_uses_only_clear_weeks():
    y =   np.array([0, 1, 0, 1, 1])
    p =   np.array([.1, .9, .2, .8, .95])
    per = np.array([0, 0, 0, 1, 1])     # last two already blooming -> excluded
    # clear rows 0,1,2: y=[0,1,0], thr .5 -> pred=[0,1,0] -> perfect
    assert common.onset_mcc(y, p, per, 0.5) == 1.0


# --- optimized lean model: HistGBM fit / score / persist ------------------
def _rich_panel(n_weeks=260, comids=(1, 2, 3, 4), start="2016-01-03"):
    """A seasonal synthetic panel: cyan_median rises and falls each year (so both bloom
    and clear weeks exist for every lake), larger lakes bloom a touch less. Enough rows
    for HistGBM's internal early-stopping holdout."""
    weeks = pd.date_range(start, periods=n_weeks, freq="7D")
    areas = {1: 3.0, 2: 15.0, 3: 60.0, 4: 200.0}
    rows = []
    for comid in comids:
        for k, w in enumerate(weeks):
            season = 100 + 80 * np.sin(2 * np.pi * k / 52.0)      # 20..180, crosses 130
            med = max(0.0, season - 0.02 * areas[comid])
            rows.append(dict(comid=comid, week_start=w, cyan_median=float(med),
                             bloom=int(med >= 130), area_sqkm=areas[comid]))
    return pd.DataFrame(rows)


def test_hgb_fit_score_and_persist(tmp_path):
    import config
    panel = _rich_panel()
    frame = common.build_horizon_frame(panel, 1)
    model = common.fit_hgb(frame, config.FEATURES, config.TARGET, config.HGB_PARAMS, config.SEED)
    p = common.hgb_score(model, frame[config.FEATURES].to_numpy())
    assert p.shape == (len(frame),)
    assert ((p >= 0) & (p <= 1)).all()
    # On this strongly-seasonal signal the model should rank blooms well.
    assert common.auc(frame[config.TARGET].to_numpy(), p) > 0.9
    # persist -> load round-trips to identical scores
    path = tmp_path / "hgb.joblib"
    common.save_model(model, path)
    p2 = common.hgb_score(common.load_model(path), frame[config.FEATURES].to_numpy())
    assert np.allclose(p, p2)


def test_permutation_importance_cyan_dominates():
    import config
    panel = _rich_panel()
    frame = common.build_horizon_frame(panel, 1)
    model = common.fit_hgb(frame, config.FEATURES, config.TARGET, config.HGB_PARAMS, config.SEED)
    base, imp = common.permutation_importance(model, frame, config.FEATURES, config.TARGET,
                                              n_repeats=5, seed=config.SEED)
    # cyan_median carries the signal; shuffling it must hurt AUC more than shuffling area.
    assert imp["cyan_median"][0] > imp["area_sqkm"][0]
