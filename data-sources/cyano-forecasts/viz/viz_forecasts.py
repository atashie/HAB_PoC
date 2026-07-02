#!/usr/bin/env python
"""Summary visualizations for the EPA cyanoHAB forecast — native per-lake, no aggregation.

Three artifacts (mirrors the cyan/NARS viz discipline; onboarding rule: never aggregate spatially/
temporally without explicit permission — everything here is per-lake native):

  1. Interactive **native per-lake map** of one forecast week (Folium) -> outputs/forecast_map_*.html
     (heavy; gitignored, regenerates from code). Each lake is one point coloured by probability.
  2. Interactive **sentinel-lake seasonal curve** (Plotly) -> outputs/forecast_sentinel_*.html
     — a single lake's own weekly probabilities across the record (native; no aggregation).
  3. Static **PNG proof** of the representative-week national pattern (matplotlib scatter) ->
     outputs/forecast_peakweek_map.png (small; tracked in git for review).

Pre-declared, non-cherry-picked choices (Codex review):
  * **Sentinel = Grand Lake St Marys, OH (COMID 120052700)** — a *documented, chronic* cyanoHAB lake
    (the 2010 Ohio bloom crisis). Chosen for its notoriety, not its value; we plot its actual curve
    whatever it shows. (It happens to peak ~99% — a real sanity check that a known HAB lake scores high.)
  * **Map week = the peak-season week by rule:** the week with the highest *national mean* probability
    in the most recent complete season (computed, not hand-picked). The national mean is used only to
    SELECT the week; the map itself shows native per-lake values. Override with --week.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
_MODULE_DIR = _HERE.parent
_OUT = _MODULE_DIR / "outputs"
_DEFAULT_INPUT = _MODULE_DIR / "data" / "derived" / "current.csv"

SENTINEL_COMID = 120052700          # Grand Lake St Marys, OH — documented chronic cyanoHAB lake
SENTINEL_LABEL = "Grand Lake St Marys, OH"


def _load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"comid": "Int64"})
    df["pct"] = pd.to_numeric(df["percent_chance"], errors="coerce")
    df["lat"] = pd.to_numeric(df["lat_centroid"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon_centroid"], errors="coerce")
    return df


def _representative_week(df: pd.DataFrame) -> str:
    """Peak-season week = highest national MEAN probability in the most recent complete season.

    (Selection diagnostic only — an aggregate used to pick the week, never displayed as data.)
    """
    seasons = sorted({w[:4] for w in df["week_end_date"].dropna()})
    latest_season = seasons[-2] if len(seasons) > 1 else seasons[-1]  # most recent COMPLETE season
    sub = df[df["week_end_date"].str.startswith(latest_season)]
    wk_mean = sub.groupby("week_end_date")["pct"].mean()
    return wk_mean.idxmax()


def map_week(df: pd.DataFrame, week: str) -> Path:
    import folium
    from branca.colormap import LinearColormap
    d = df[df["week_end_date"] == week].dropna(subset=["lat", "lon", "pct"])
    cmap = LinearColormap(["#2c7bb6", "#ffffbf", "#d7191c"], vmin=0, vmax=100,
                          caption=f"P(cyanoHAB next 7 days), % — week ending {week}")
    m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="CartoDB positron")
    for _, r in d.iterrows():
        folium.CircleMarker(
            [r["lat"], r["lon"]], radius=3, weight=0, fill=True,
            fill_color=cmap(r["pct"]), fill_opacity=0.85,
            tooltip=(f"{r['lake_name']} ({r['state']})<br>COMID {r['comid']}<br>"
                     f"{r['pct']:.1f}% — week ending {week}"),
        ).add_to(m)
    cmap.add_to(m)
    title = (f'<div style="position:fixed;top:8px;left:50px;z-index:9999;background:white;'
             f'padding:6px 10px;border:1px solid #888;font-family:sans-serif;font-size:13px">'
             f'<b>EPA experimental cyanoHAB forecast</b> — week ending {week}<br>'
             f'{len(d):,} lakes, native per-lake (no aggregation). '
             f'<i>Experimental; over-predicts positives (precision≈0.49).</i></div>')
    m.get_root().html.add_child(folium.Element(title))
    _OUT.mkdir(parents=True, exist_ok=True)
    out = _OUT / f"forecast_{week}_map.html"   # '*_map.html' -> gitignored (heavy; regenerates from code)
    m.save(str(out))
    return out


def sentinel_curve(df: pd.DataFrame) -> Path:
    import plotly.graph_objects as go
    d = df[df["comid"] == SENTINEL_COMID].sort_values("week_end_date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["week_end_date"], y=d["pct"], mode="lines+markers",
                             line=dict(color="#d7191c"), name="P(bloom)"))
    fig.add_hline(y=50, line_dash="dot", line_color="grey",
                  annotation_text="50%", annotation_position="right")
    fig.update_layout(
        title=(f"Sentinel lake — {SENTINEL_LABEL} (COMID {SENTINEL_COMID})<br>"
               f"<sub>Weekly 7-day cyanoHAB probability, native (one lake, no aggregation). "
               f"Pre-declared documented HAB lake.</sub>"),
        xaxis_title="week ending", yaxis_title="P(cyanoHAB next 7 days), %",
        yaxis_range=[0, 100], template="plotly_white", height=430)
    _OUT.mkdir(parents=True, exist_ok=True)
    out = _OUT / "forecast_sentinel_grand_lake_st_marys.html"
    fig.write_html(str(out), include_plotlyjs="cdn")
    return out, d


def peakweek_png(df: pd.DataFrame, week: str, sentinel: pd.DataFrame) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = df[df["week_end_date"] == week].dropna(subset=["lat", "lon", "pct"]).sort_values("pct")
    fig, ax = plt.subplots(figsize=(10, 6.2))
    sc = ax.scatter(d["lon"], d["lat"], c=d["pct"], cmap="YlOrRd", vmin=0, vmax=100,
                    s=14, edgecolors="none", alpha=0.9)
    # mark the sentinel
    if len(sentinel):
        s = sentinel[sentinel["week_end_date"] == week]
        if len(s):
            ax.scatter(s["lon"], s["lat"], s=120, facecolors="none", edgecolors="black",
                       linewidths=1.4, zorder=5)
            ax.annotate(f"{SENTINEL_LABEL}\n({float(s['pct'].iloc[0]):.0f}%)",
                        (float(s["lon"].iloc[0]), float(s["lat"].iloc[0])),
                        textcoords="offset points", xytext=(8, 6), fontsize=8)
    ax.set_xlim(-125, -66); ax.set_ylim(24, 50)
    ax.set_xlabel("longitude"); ax.set_ylabel("latitude")
    ax.set_title(f"EPA experimental cyanoHAB forecast — week ending {week}\n"
                 f"{len(d):,} lakes, native per-lake (no aggregation); experimental, over-predicts positives",
                 fontsize=10)
    cb = fig.colorbar(sc, ax=ax, shrink=0.85); cb.set_label("P(cyanoHAB next 7 days), %")
    fig.tight_layout()
    _OUT.mkdir(parents=True, exist_ok=True)
    out = _OUT / "forecast_peakweek_map.png"
    fig.savefig(out, dpi=130); plt.close(fig)
    return out


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default=str(_DEFAULT_INPUT), help="current.csv or a snapshot CSV")
    ap.add_argument("--week", default=None, help="forecast week (YYYY-MM-DD); default = peak-season rule")
    args = ap.parse_args(argv)

    df = _load(Path(args.input))
    week = args.week or _representative_week(df)
    print(f"[viz] input={Path(args.input).name} rows={len(df):,} representative week={week}")

    m = map_week(df, week)
    print(f"[viz] wrote {m.relative_to(_MODULE_DIR)} (interactive native map; gitignored)")
    sc_out, sd = sentinel_curve(df)
    peak = float(sd["pct"].max()) if len(sd) else float("nan")
    print(f"[viz] wrote {sc_out.relative_to(_MODULE_DIR)} — {SENTINEL_LABEL}: "
          f"peak {peak:.0f}%, mean {sd['pct'].mean():.1f}% over {len(sd)} weeks")
    png = peakweek_png(df, week, sd)
    hot = df[(df['week_end_date'] == week) & (df['pct'] >= 50)]
    print(f"[viz] wrote {png.relative_to(_MODULE_DIR)} — {len(hot):,} lakes ≥50% that week "
          f"(visual sanity check: HAB hotspots should stand out)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
