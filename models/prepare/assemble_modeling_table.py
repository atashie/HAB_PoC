"""Assemble the horizon-paired modeling table for FL CyAN bloom forecasting.

Pairs the antecedent CyAN feature block (as-of a cutoff week) with the target bloom at week W, for
each horizon h in {0..4}, enforcing the latency-aware cutoff `feature_week = W − (h+1) weeks`
(D-28; docs/02 §1). Emits one row per (lake, target_week, horizon) with the target, the CyAN-only
features as-of the cutoff, the persistence prediction, the target-relative staleness, the resolved
cutoff week (for audit), and a temporal train/test split flag.

Enforces the H4 leakage guard as hard asserts: for every row, `target_date − feature_date == 7·(h+1)`.

Output: models/data/derived/modeling_table_cyan_fl.parquet
Run:    python models/prepare/assemble_modeling_table.py
"""
from __future__ import annotations

import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.abspath(os.path.join(HERE, "..", "data", "derived"))
FEATS = os.path.join(DER, "cyan_features_fl.parquet")
TARGET = os.path.join(DER, "cyan_lake_weekly_fl.parquet")
OUT = os.path.join(DER, "modeling_table_cyan_fl.parquet")

HORIZONS = [0, 1, 2, 3, 4]
TEST_YEAR = 2025            # held-out year (last complete season); 2026 is partial -> separate split
VAL_YEAR = 2024            # validation year for tuning (train = <=2023)


def split_of(year: int) -> str:
    if year <= VAL_YEAR - 1:
        return "train"
    if year == VAL_YEAR:
        return "val"
    if year == TEST_YEAR:
        return "test"
    return "oos_partial"    # 2026 partial season


def main() -> None:
    feats = pd.read_parquet(FEATS)
    feats["start_date"] = pd.to_datetime(feats["start_date"])
    tgt = pd.read_parquet(TARGET)[["comid", "start_date", "year", "bloom", "valid_frac"]].copy()
    tgt["start_date"] = pd.to_datetime(tgt["start_date"])
    tgt = tgt.rename(columns={"start_date": "target_date", "bloom": "target_bloom",
                              "year": "target_year", "valid_frac": "target_valid_frac"})
    tgt = tgt.dropna(subset=["target_bloom"]).copy()   # can't score a missing target
    tgt["target_bloom"] = tgt["target_bloom"].astype(int)

    # CyAN-only feature columns carried into the model (antecedent, as-of the cutoff week)
    feat_cols = ["cyan_median", "cyan_mean", "cyan_sd", "bloom_state", "bloom_state_ffill",
                 "cyan_median_lag1", "cyan_median_lag2", "cyan_median_lag4",
                 "cyan_mean_lag1", "cyan_sd_lag1", "bloom_lag1", "bloom_roll4", "bloom_roll4_n",
                 "cyan_gap_weeks_at_cutoff", "valid_frac", "area_sqkm", "gnis_name"]
    feats_j = feats[["comid", "start_date"] + feat_cols].rename(columns={"start_date": "feature_date"})

    frames = []
    for h in HORIZONS:
        t = tgt.copy()
        t["horizon"] = h
        t["feature_date"] = t["target_date"] - pd.Timedelta(weeks=h + 1)
        m = t.merge(feats_j, on=["comid", "feature_date"], how="inner")
        frames.append(m)
    df = pd.concat(frames, ignore_index=True)

    # persistence = last OBSERVED bloom diagnostic carried forward to the cutoff week (bloom_state_ffill),
    # NOT fill-0 of a cloudy freshest week (Codex M2). flag rows where the freshest week was cloudy.
    df["persistence"] = df["bloom_state_ffill"].astype("Int64")
    df["persistence_from_cloudy_cutoff"] = df["bloom_state"].isna()
    # target-relative CyAN staleness = cutoff gap + the (h+1)-week latency gap
    df["cyan_staleness_weeks_vs_target"] = df["cyan_gap_weeks_at_cutoff"] + (df["horizon"] + 1)
    df["split"] = df["target_year"].map(split_of)

    # ---- H4 leakage guard (explicit raises; asserts can be disabled under python -O, Codex L3) ----
    gap_days = (df["target_date"] - df["feature_date"]).dt.days
    expected = 7 * (df["horizon"] + 1)
    if not (gap_days == expected).all():
        raise ValueError("LEAKAGE: feature_date != target_date - 7*(h+1)")
    if not df["feature_date"].lt(df["target_date"]).all():
        raise ValueError("LEAKAGE: feature_date >= target_date (not strictly antecedent)")
    print("LEAKAGE GUARD PASSED: feature_date == target_date - 7*(h+1) for all rows; strictly antecedent.")

    keep = (["comid", "gnis_name", "target_date", "feature_date", "target_year", "horizon",
             "split", "target_bloom", "persistence", "persistence_from_cloudy_cutoff",
             "target_valid_frac", "cyan_staleness_weeks_vs_target"] + feat_cols)
    keep = [c for c in dict.fromkeys(keep)]     # dedupe, preserve order
    df = df[keep]
    os.makedirs(DER, exist_ok=True)
    df.to_parquet(OUT, index=False)

    print(f"\nwrote {OUT}: {len(df):,} rows")
    print(f"  per horizon: {df.groupby('horizon').size().to_dict()}")
    print("  split x horizon (rows):")
    print(df.pivot_table(index="split", columns="horizon", values="comid",
                         aggfunc="size", fill_value=0).to_string())
    print("\n  target bloom prevalence by split (h=1):")
    h1 = df[df.horizon == 1]
    print((h1.groupby("split")["target_bloom"].mean() * 100).round(2).to_string())
    print("\n  rows dropped vs naive (no feature at cutoff week — near record start / week gaps):")
    naive = len(tgt) * len(HORIZONS)
    print(f"    {naive - len(df):,} of {naive:,} ({100*(naive-len(df))/naive:.1f}%)")


if __name__ == "__main__":
    main()
