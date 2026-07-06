"""Build the CyAN antecedent feature block (the autoregressive-ladder baseline) for FL lakes.

From the per-lake-week target table (`cyan_lake_weekly_fl.parquet`), derive the ANTECEDENT CyAN
features + the D-26a autoregressive-ladder baseline. Everything here is computed "as of the issue
week t" (freshest = week t); the modeling assembler pairs features(t) with target bloom(t+h) per
horizon (docs/02 §1). NO target-week CyAN, NO interpolation. Per-lake week-of-year climatology is
deferred to split time (train-years only — it is target-derived and would leak).

Output: models/data/derived/cyan_features_fl.parquet
Run:    python models/prepare/build_cyan_features.py
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "data", "derived", "cyan_lake_weekly_fl.parquet"))
OUT = os.path.abspath(os.path.join(HERE, "..", "data", "derived", "cyan_features_fl.parquet"))


def per_lake(g: pd.DataFrame) -> pd.DataFrame:
    g = g.sort_values("start_date").copy()
    med = g["cyan_median"]
    g["cyan_median_lag1"] = med.shift(1)
    g["cyan_median_lag2"] = med.shift(2)
    g["cyan_median_lag4"] = med.shift(4)
    g["cyan_mean_lag1"] = g["cyan_mean"].shift(1)
    g["cyan_sd_lag1"] = g["cyan_sd"].shift(1)

    bloom = g["bloom"].astype("float")           # True/False/NA -> 1/0/NaN
    g["bloom_state"] = bloom                       # bloom at the freshest week t (NaN if cloudy)
    # last-valid bloom at/before t (for PERSISTENCE: carry the last OBSERVED diagnostic forward,
    # rather than treat a cloudy freshest week as no-bloom). Codex M2.
    g["bloom_state_ffill"] = bloom.ffill()
    g["bloom_lag1"] = bloom.shift(1)
    # recent-bloom fraction over the PRIOR 4 weeks (antecedent: t-1..t-4).
    # NOTE (Codex M4): denominator = VALID prior weeks, not 4 calendar weeks; bloom_roll4_n exposes it.
    prior = bloom.shift(1)
    g["bloom_roll4"] = prior.rolling(4, min_periods=1).mean()
    g["bloom_roll4_n"] = prior.rolling(4, min_periods=1).count()

    # CUTOFF-relative data-quality gap: weeks since the last VALID median at/before t (cloud gaps).
    # NOTE (Codex M3): this is NOT target-relative. Target-relative staleness = this + 7*(h+1) days,
    # added by the horizon assembler; named explicitly to avoid the earlier mislabel.
    dt = pd.to_datetime(g["start_date"])
    last_valid = dt.where(med.notna()).ffill()
    g["cyan_gap_weeks_at_cutoff"] = ((dt - last_valid).dt.days / 7).round()
    return g


def main() -> None:
    df = pd.read_parquet(SRC)
    print(f"source: {len(df):,} lake-weeks, {df.comid.nunique()} lakes")
    feats = (df.groupby("comid", group_keys=False)[df.columns.tolist()]
               .apply(per_lake))

    keep = ["comid", "gnis_name", "area_sqkm", "start_date", "end_date", "year",
            "n_inside", "n_valid", "valid_frac", "nodata_frac",
            "cyan_mean", "cyan_median", "cyan_sd", "bloom_state", "bloom_state_ffill",
            "cyan_median_lag1", "cyan_median_lag2", "cyan_median_lag4",
            "cyan_mean_lag1", "cyan_sd_lag1", "bloom_lag1", "bloom_roll4", "bloom_roll4_n",
            "cyan_gap_weeks_at_cutoff"]
    feats = feats[keep]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    feats.to_parquet(OUT, index=False)

    print(f"wrote {OUT}: {len(feats):,} rows x {feats.shape[1]} cols")
    print("\nnull rate per feature (%):")
    print((feats.isna().mean() * 100).round(1).to_string())
    # sanity: Apopka (chronic bloom) vs Okeechobee (patchy) — ladder should reflect persistence
    for name in ("Apopka, Lake",):
        s = feats[feats.gnis_name == name].sort_values("start_date").iloc[10:14]
        print(f"\n{name} sample (t, median, lag1, lag2, bloom_state, roll4, gap_weeks):")
        print(s[["start_date", "cyan_median", "cyan_median_lag1", "cyan_median_lag2",
                 "bloom_state", "bloom_roll4", "cyan_gap_weeks_at_cutoff"]].to_string(index=False))
    # AR(1): pooled vs WITHIN-lake (Codex M6 — pooled is inflated by between-lake baseline differences)
    v = feats.dropna(subset=["cyan_median", "cyan_median_lag1"]).copy()
    pooled = v["cyan_median"].corr(v["cyan_median_lag1"])
    v["md"] = v["cyan_median"] - v.groupby("comid")["cyan_median"].transform("mean")
    v["ld"] = v["cyan_median_lag1"] - v.groupby("comid")["cyan_median_lag1"].transform("mean")
    within = v["md"].corr(v["ld"])
    per = (v.groupby("comid").apply(lambda d: d["cyan_median"].corr(d["cyan_median_lag1"]))
             .dropna())
    print(f"\nAR(1) check (n={len(v):,}): pooled={pooled:.3f} | within-lake(demeaned)={within:.3f} "
          f"| median per-lake={per.median():.3f}")
    print("  (pooled mixes temporal AR with between-lake baseline spread; within-lake is the honest "
          "temporal-persistence number)")


if __name__ == "__main__":
    main()
