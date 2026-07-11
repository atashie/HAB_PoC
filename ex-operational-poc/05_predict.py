"""Step 5 - RUN & STORE.  Produce the current operational forecast and save it.

This is the deployable step. For each horizon it refits the lean model on ALL labelled
history (more data -> better deployed model; still leakage-safe, since every row's
feature already sits (h+1) weeks before its target). It then takes each lake's freshest
CyAN median and predicts P(WHO-AL1 bloom) at target week = latest week + (h+1).

Outputs (committed):
  outputs/predictions.csv          one row per lake: latest CyAN + risk_h0..h4 (%)
  outputs/predictions_summary.md   issue date, target weeks, and the top new-bloom risks

Run:  python 05_predict.py
"""
import json
import pandas as pd
import geopandas as gpd

import config
import common


def main():
    panel = pd.read_parquet(config.LAKE_WEEK_PARQUET)
    panel["week_start"] = pd.to_datetime(panel["week_start"])
    names = (gpd.read_file(config.FL_LAKES_GPKG)[["COMID", "GNIS_NAME"]]
             .rename(columns={"COMID": "comid", "GNIS_NAME": "name"}))
    tuned = json.loads((config.OUTPUTS / "models.json").read_text(encoding="utf-8"))["horizons"]

    # Deployed model = refit on ALL labelled history, per horizon.
    deployed = {h: common.fit_logreg(common.build_horizon_frame(panel, h),
                                     config.FEATURES, config.TARGET, config.SEED)
                for h in config.HORIZONS}

    # Freshest valid CyAN per lake (the operational feature "as of now").
    latest = (panel.dropna(subset=["cyan_median"])
              .sort_values("week_start").groupby("comid").tail(1)
              .rename(columns={"week_start": "feature_date"}))
    issue_week = latest["feature_date"].max()

    X = latest[config.FEATURES].to_numpy()
    out = latest[["comid", "feature_date", "cyan_median", "area_sqkm"]].copy()
    out["blooming_now"] = latest["bloom"].astype(int).to_numpy()
    for h in config.HORIZONS:
        out[f"risk_h{h}"] = (common.logreg_score(deployed[h], X) * 100).round(1)
    out = out.merge(names, on="comid", how="left").sort_values("risk_h1", ascending=False)

    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    cols = (["comid", "name", "feature_date", "cyan_median", "area_sqkm", "blooming_now"]
            + [f"risk_h{h}" for h in config.HORIZONS])
    out[cols].to_csv(config.OUTPUTS / "predictions.csv", index=False)

    targets = {f"h{h}": str((issue_week + pd.Timedelta(weeks=h + 1)).date()) for h in config.HORIZONS}
    new_risk = out[out["blooming_now"] == 0].head(10)
    thr = tuned["1"]["threshold"] * 100
    md = [f"# Operational forecast - issued from CyAN week {issue_week.date()}", "",
          f"- Model: lean logistic regression on `{' + '.join(config.FEATURES)}`, one per horizon, "
          f"refit on all labelled history.", f"- Target weeks: {targets}",
          f"- Lakes forecast: {len(out)}   |   currently blooming: {int(out['blooming_now'].sum())}",
          f"- h1 alert threshold (val-tuned): {thr:.0f}%", "",
          "## Top-10 new-bloom risk (currently clear, ranked by 1-week risk)", "",
          "| lake | comid | CyAN now | 1-wk risk | 2-wk | 3-wk | 4-wk |",
          "|--|--:|--:|--:|--:|--:|--:|"]
    for _, r in new_risk.iterrows():
        md.append(f"| {r['name'] or '(unnamed)'} | {r['comid']} | {r['cyan_median']:.0f} | "
                  f"{r['risk_h1']:.0f}% | {r['risk_h2']:.0f}% | {r['risk_h3']:.0f}% | {r['risk_h4']:.0f}% |")
    md += ["", "Risks are probabilities of a WHO-AL1 bloom, not chlorophyll values; tiers "
           "near the threshold are not sharply separable. Risk is nearly flat across h0-h4 "
           "by design - all horizons are scored from the same freshest antecedent CyAN, so a "
           "2-feature snapshot barely separates 1-week from 4-week lead. Correlation, not causation."]
    (config.OUTPUTS / "predictions_summary.md").write_text("\n".join(md), encoding="utf-8")

    print("\n".join(md))
    print(f"\nWrote {config.OUTPUTS / 'predictions.csv'} and predictions_summary.md")


if __name__ == "__main__":
    main()
