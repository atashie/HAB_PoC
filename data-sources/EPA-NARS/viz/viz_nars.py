#!/usr/bin/env python
"""Summary visualizations for NLA 2022 - per-lake, native resolution, UNWEIGHTED.

Design constraints (from ../../ONBOARDING-A-DATASET.md and CLAUDE.md):
  * NO spatial/temporal aggregation - every lake is its own point at its own
    sampled coordinate. We reduce SCOPE, never resolution.
  * These are the ~1,225 sampled site-visits as-measured. They are NOT survey-weighted,
    so nothing here is a national/regional estimate - every artifact says so.

Outputs (into ../outputs/):
  * nla2022_microcystin_map.html  - interactive Folium map, points colored by microcystin
    relative to EPA's 8 ug/L recreational criterion (heavy; gitignored).
  * nla2022_summary.html          - interactive Plotly summary charts (small; tracked).
  * nla2022_microcystin_map.png   - static national scatter (small; tracked visual proof).

Run:  cd data-sources/EPA-NARS/viz && python viz_nars.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

_HERE = Path(__file__).resolve().parent
_NARS_DIR = _HERE.parent
_DEFAULT_RAW = _NARS_DIR / "data" / "raw" / "nla2022"
_OUTPUTS = _NARS_DIR / "outputs"

# EPA recreational criterion for microcystin (ug/L). Below, we categorize each lake
# against it - a per-lake category, not an aggregate.
MICX_REC_CRITERION = 8.0

# (label, color, predicate on (is_nondetect, value))
MICX_BINS = [
    ("Non-detect",              "#c7c7c7"),
    ("Detected < 1 ug/L",       "#2c7fb8"),
    ("1 to < 8 ug/L",           "#fe9929"),
    (">= 8 ug/L (EPA rec.)",    "#d7191c"),
]


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def _read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""])


def _find(rawdir: Path, needle: str) -> Path:
    hits = sorted(rawdir.glob(f"*{needle}*.csv"))
    if not hits:
        raise SystemExit(f"missing *{needle}*.csv in {rawdir}; run access/pull_nars.py")
    return hits[0]


def build_frame(rawdir: Path) -> pd.DataFrame:
    """One row per sampled lake-visit: coords + microcystin (+ flag) + chla + TP."""
    site = _read(_find(rawdir, "siteinfo"))
    tox = _read(_find(rawdir, "algaltoxins"))
    chem = _read(_find(rawdir, "waterchem_wide"))

    micx = tox[tox["ANALYTE"] == "MICX"].copy()
    micx["MICX"] = _num(micx["RESULT"])
    micx["MICX_ND"] = micx["NARS_FLAG"].fillna("").str.contains("ND")
    micx = micx[["UID", "MICX", "MICX_ND"]]

    keep_site = ["UID", "NARS_NAME", "PSTL_CODE", "US_L3NAME",
                 "INDEX_LAT_DD", "INDEX_LON_DD", "LAT_DD83", "LON_DD83"]
    site = site[[c for c in keep_site if c in site.columns]].copy()
    chem = chem[["UID", "CHLA_RESULT", "PTL_RESULT"]].copy()

    df = site.merge(micx, on="UID", how="inner").merge(chem, on="UID", how="left")
    # Prefer the actual sampled index point; fall back to lake centroid.
    df["lat"] = _num(df["INDEX_LAT_DD"]).fillna(_num(df["LAT_DD83"]))
    df["lon"] = _num(df["INDEX_LON_DD"]).fillna(_num(df["LON_DD83"]))
    df["CHLA"] = _num(df["CHLA_RESULT"])
    df["PTL"] = _num(df["PTL_RESULT"])
    df = df.dropna(subset=["lat", "lon"])
    df["micx_bin"] = [_bin_micx(nd, v) for nd, v in zip(df["MICX_ND"], df["MICX"])]
    return df


def _bin_micx(is_nd: bool, val: float) -> int:
    if is_nd or pd.isna(val) or val <= 0:
        return 0
    if val < 1:
        return 1
    if val < MICX_REC_CRITERION:
        return 2
    return 3


# --------------------------------------------------------------------------- #
# Folium interactive map
# --------------------------------------------------------------------------- #
def make_map(df: pd.DataFrame, out: Path) -> None:
    import folium

    m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="CartoDB positron")
    title = ("NLA 2022 sampled lakes - microcystin vs EPA 8 ug/L recreational criterion "
             "(per-lake, UNWEIGHTED - not a national estimate)")
    folium.map.Marker(
        [49.5, -124], icon=folium.DivIcon(html=f'<div style="font-size:12px;'
        f'background:white;padding:3px;border:1px solid #888">{title}</div>')
    ).add_to(m)

    for _, r in df.iterrows():
        label, color = MICX_BINS[r["micx_bin"]][0], MICX_BINS[r["micx_bin"]][1]
        micx_txt = "ND" if r["micx_bin"] == 0 else f"{r['MICX']:.3g} ug/L"
        popup = (f"<b>{r.get('NARS_NAME','(unnamed)')}</b> ({r.get('PSTL_CODE','')})<br>"
                 f"Ecoregion: {r.get('US_L3NAME','')}<br>"
                 f"Microcystin: {micx_txt} ({label})<br>"
                 f"Chlorophyll-a: {r['CHLA']:.3g} ug/L<br>"
                 f"Total P: {r['PTL']:.3g} ug/L" if pd.notna(r['CHLA']) else
                 f"<b>{r.get('NARS_NAME','(unnamed)')}</b><br>Microcystin: {micx_txt}")
        folium.CircleMarker(
            [r["lat"], r["lon"]], radius=3 if r["micx_bin"] == 0 else 5,
            color=color, fill=True, fill_color=color,
            fill_opacity=0.35 if r["micx_bin"] == 0 else 0.85, weight=0.5,
            popup=folium.Popup(popup, max_width=280),
        ).add_to(m)

    legend = '<div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;' \
             'padding:8px;border:1px solid #888;font-size:12px">' \
             '<b>Microcystin</b><br>'
    for label, color in MICX_BINS:
        legend += f'<span style="color:{color}">&#9679;</span> {label}<br>'
    legend += '</div>'
    m.get_root().html.add_child(folium.Element(legend))
    m.save(str(out))


# --------------------------------------------------------------------------- #
# Plotly summary charts (small, tracked)
# --------------------------------------------------------------------------- #
def make_summary(df: pd.DataFrame, out: Path) -> None:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=(
            "Microcystin category (n lakes)",
            "Chlorophyll-a (ug/L, log)",
            "Chl-a vs microcystin (detects; log-log)",
        ),
    )
    # (1) microcystin category counts
    counts = df["micx_bin"].value_counts().sort_index()
    fig.add_trace(go.Bar(
        x=[MICX_BINS[i][0] for i in counts.index],
        y=counts.values, marker_color=[MICX_BINS[i][1] for i in counts.index],
        showlegend=False), row=1, col=1)
    # (2) chla histogram
    chla = df["CHLA"].dropna()
    fig.add_trace(go.Histogram(x=chla[chla > 0], nbinsx=50, marker_color="#238b45",
                               showlegend=False), row=1, col=2)
    fig.update_xaxes(type="log", row=1, col=2)
    # (3) chla vs microcystin among detects
    d = df[(df["micx_bin"] > 0) & (df["CHLA"] > 0) & (df["MICX"] > 0)]
    fig.add_trace(go.Scatter(x=d["CHLA"], y=d["MICX"], mode="markers",
                             marker=dict(size=5, color="#d7191c", opacity=0.5),
                             showlegend=False), row=1, col=3)
    fig.add_hline(y=MICX_REC_CRITERION, line_dash="dash", line_color="black", row=1, col=3)
    fig.update_xaxes(type="log", title_text="chl-a", row=1, col=3)
    fig.update_yaxes(type="log", title_text="microcystin", row=1, col=3)

    fig.update_layout(
        title_text=f"NLA 2022 sampled lakes (n={len(df)}) - UNWEIGHTED, not a national estimate. "
                   "Chl-a~microcystin is cross-sectional (correlation, not causation).",
        height=430, font=dict(size=11),
    )
    fig.write_html(str(out), include_plotlyjs="cdn")


# --------------------------------------------------------------------------- #
# Static PNG (visual proof for git)
# --------------------------------------------------------------------------- #
def make_png(df: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, (label, color) in enumerate(MICX_BINS):
        sub = df[df["micx_bin"] == i]
        ax.scatter(sub["lon"], sub["lat"], s=8 if i == 0 else 16, c=color,
                   label=f"{label} (n={len(sub)})", alpha=0.4 if i == 0 else 0.85,
                   edgecolors="none")
    ax.set_xlim(-125, -66)
    ax.set_ylim(24, 50)
    ax.set_xlabel("Longitude (NAD83)")
    ax.set_ylabel("Latitude (NAD83)")
    ax.set_title(f"NLA 2022 sampled lakes - microcystin (n={len(df)}, UNWEIGHTED)\n"
                 "per-lake at native coordinates; not a national estimate")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=110)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# State-scoped, multi-variable LAYERED map (toggle value-type per feature)
# --------------------------------------------------------------------------- #
# Each variable is a togglable layer; every lake keeps its exact sampled point
# (no aggregation). "more = more concerning" -> darker/red; Secchi is inverted
# (low clarity = red) so the red==concern semantics stay consistent.
# (key, label, units, source, column, log?, invert?, reference note)
LAYER_VARS = [
    ("CHLA",    "Chlorophyll-a",       "ug/L",  "chem", "CHLA_RESULT", True,  False, None),
    ("PTL",     "Total phosphorus",    "ug/L",  "chem", "PTL_RESULT",  True,  False, None),
    ("NTL",     "Total nitrogen",      "mg/L",  "chem", "NTL_RESULT",  True,  False, None),
    ("MICX",    "Microcystin",         "ug/L",  "tox",  "MICX",        True,  False, "EPA rec. 8 ug/L"),
    ("CYLSPER", "Cylindrospermopsin",  "ug/L",  "tox",  "CYLSPER",     True,  False, None),
    ("SECCHI",  "Secchi depth",        "m",     "sec",  "SECCHI",      False, True,  "higher = clearer"),
    ("TURB",    "Turbidity",           "NTU",   "chem", "TURB_RESULT", True,  False, None),
    ("PH",      "pH",                  "",      "chem", "PH_RESULT",   False, False, None),
    ("COND",    "Conductivity",        "uS/cm", "chem", "COND_RESULT", True,  False, None),
]
_RAMP = ["#ffffb2", "#fecc5c", "#fd8d3c", "#f03b20", "#bd0026"]  # light->dark red (YlOrRd)


def build_state_layer_frame(rawdir: Path, state: str):
    """Return (lakes, evaluated_not_sampled) DataFrames for one state.

    `lakes`: one row per SAMPLED lake (deduped by SITE_ID, primary visit preferred)
    with all LAYER_VARS values (+ toxin ND flags) and per-visit detail for popups.
    `evaluated_not_sampled`: frame sites drawn but not sampled (design coords only).
    """
    site = _read(_find(rawdir, "siteinfo"))
    chem = _read(_find(rawdir, "waterchem_wide"))
    tox = _read(_find(rawdir, "algaltoxins"))
    sec = _read(_find(rawdir, "secchi"))

    site = site[site["PSTL_CODE"] == state].copy()
    if site.empty:
        return site, site

    # toxins long -> wide per UID (value + ND flag)
    tw = {}
    for an in ("MICX", "CYLSPER"):
        sub = tox[tox["ANALYTE"] == an]
        for _, r in sub.iterrows():
            d = tw.setdefault(r["UID"], {})
            d[an] = _num(pd.Series([r["RESULT"]])).iloc[0]
            d[f"{an}_ND"] = "ND" in str(r.get("NARS_FLAG", "") or "")
    # secchi depth per UID = mean(disappear, reappear) when both present
    secd = {}
    for _, r in sec.iterrows():
        dis, rea = _num(pd.Series([r.get("DISAPPEARS")])).iloc[0], _num(pd.Series([r.get("REAPPEARS")])).iloc[0]
        vals = [v for v in (dis, rea) if pd.notna(v)]
        secd[r["UID"]] = (sum(vals) / len(vals)) if vals else float("nan")

    chem_cols = ["UID"] + [c for _, _, _, s, c, *_ in LAYER_VARS if s == "chem"]
    chem = chem[[c for c in chem_cols if c in chem.columns]].copy()

    # per site-visit wide row
    rows = []
    for _, s in site.iterrows():
        uid = s["UID"]
        lat = _num(pd.Series([s.get("INDEX_LAT_DD")])).iloc[0]
        if pd.isna(lat):
            lat = _num(pd.Series([s.get("LAT_DD83")])).iloc[0]
        lon = _num(pd.Series([s.get("INDEX_LON_DD")])).iloc[0]
        if pd.isna(lon):
            lon = _num(pd.Series([s.get("LON_DD83")])).iloc[0]
        crow = chem[chem["UID"] == uid]
        rec = {
            "SITE_ID": s["SITE_ID"], "UID": uid, "VISIT_NO": s.get("VISIT_NO"),
            "DATE_COL": s.get("DATE_COL"), "sampled": pd.notna(_num(pd.Series([s.get("INDEX_LAT_DD")])).iloc[0]),
            "name": s.get("GNIS_NAME") or s.get("NARS_NAME") or "(unnamed)",
            "county": s.get("CNTYNAME", ""), "ecoregion": s.get("US_L3NAME", ""),
            "comid": s.get("COMID", ""), "huc8": s.get("HUC8", ""),
            "area_ha": s.get("AREA_HA", ""), "lat": lat, "lon": lon,
        }
        for key, _, _, src, col, *_ in LAYER_VARS:
            if src == "chem":
                rec[key] = _num(crow[col]).iloc[0] if (col in crow.columns and len(crow)) else float("nan")
            elif src == "tox":
                rec[key] = tw.get(uid, {}).get(col, float("nan"))
                rec[f"{key}_ND"] = tw.get(uid, {}).get(f"{col}_ND", False)
            elif src == "sec":
                rec[key] = secd.get(uid, float("nan"))
        rows.append(rec)
    allv = pd.DataFrame(rows)

    sampled = allv[allv["sampled"]].dropna(subset=["lat", "lon"]).copy()
    not_sampled = allv[~allv["sampled"]].dropna(subset=["lat", "lon"]).copy()

    # one marker per lake: prefer VISIT_NO == '1', else first; attach all visits for popup
    lakes = []
    for sid, g in sampled.groupby("SITE_ID"):
        disp = g[g["VISIT_NO"] == "1"]
        disp = (disp.iloc[0] if len(disp) else g.iloc[0]).to_dict()
        disp["_visits"] = g.to_dict("records")
        lakes.append(disp)
    lakes = pd.DataFrame(lakes)
    return lakes, not_sampled


def _color_for(val, vmin, vmax, log, invert):
    import branca.colormap as bcm
    if pd.isna(val):
        return None
    cmap = bcm.LinearColormap(_RAMP, vmin=0.0, vmax=1.0)
    if log:
        v, lo, hi = _safe_log(val), _safe_log(vmin), _safe_log(vmax)
    else:
        v, lo, hi = float(val), float(vmin), float(vmax)
    t = 0.0 if hi <= lo else (v - lo) / (hi - lo)
    t = min(max(t, 0.0), 1.0)
    if invert:
        t = 1.0 - t
    return cmap(t)


def _safe_log(x):
    import math
    return math.log10(x) if x and x > 0 else math.log10(1e-4)


def make_layered_state_map(lakes: pd.DataFrame, not_sampled: pd.DataFrame,
                           state: str, out: Path) -> None:
    import folium
    from folium.features import GeoJson  # noqa: F401 (ensure folium.features importable)

    if lakes.empty:
        raise SystemExit(f"No sampled lakes for state {state}.")
    clat, clon = lakes["lat"].mean(), lakes["lon"].mean()
    m = folium.Map(location=[clat, clon], zoom_start=7, tiles="CartoDB positron",
                   control_scale=True)

    # per-variable min/max over sampled lakes (finite, and for toxins detected-only)
    ranges = {}
    for key, label, units, src, col, log, invert, ref in LAYER_VARS:
        vals = pd.to_numeric(lakes[key], errors="coerce")
        if src == "tox":  # scale on detections only; ND handled separately
            nd = lakes.get(f"{key}_ND", pd.Series([False] * len(lakes)))
            vals = vals[(~nd.astype(bool)) & vals.notna()]
        vals = vals[vals.notna()]
        ranges[key] = (float(vals.min()), float(vals.max())) if len(vals) else (float("nan"), float("nan"))

    groups = []
    for key, label, units, src, col, log, invert, ref in LAYER_VARS:
        vmin, vmax = ranges[key]
        show = (key == "CHLA")
        fg = folium.FeatureGroup(name=f"{label} ({units})" if units else label, show=show)
        for _, r in lakes.iterrows():
            val = r.get(key)
            is_nd = bool(r.get(f"{key}_ND", False)) if src == "tox" else False
            popup = _lake_popup(r)
            if is_nd or pd.isna(val):
                # measured non-detect (toxins) or not measured -> hollow grey, honest
                txt = "ND (non-detect)" if is_nd else "not measured"
                folium.CircleMarker(
                    [r["lat"], r["lon"]], radius=4, color="#8a8a8a", weight=1,
                    fill=True, fill_color="#d9d9d9", fill_opacity=0.5, dash_array="3",
                    tooltip=f"{r['name']} ({r['county']} Co.) — {label}: {txt}",
                    popup=folium.Popup(popup, max_width=320),
                ).add_to(fg)
            else:
                color = _color_for(val, vmin, vmax, log, invert)
                refnote = f" [{ref}]" if ref else ""
                folium.CircleMarker(
                    [r["lat"], r["lon"]], radius=7, color="#333", weight=0.6,
                    fill=True, fill_color=color, fill_opacity=0.9,
                    tooltip=(f"{r['name']} ({r['county']} Co.) — {label}: "
                             f"{val:.3g} {units}{refnote}"),
                    popup=folium.Popup(popup, max_width=320),
                ).add_to(fg)
        fg.add_to(m)
        groups.append(fg)

    # transparency: sites evaluated but NOT sampled (design coords, no data)
    if len(not_sampled):
        fg_ns = folium.FeatureGroup(name=f"Evaluated, not sampled ({len(not_sampled)})", show=False)
        for _, r in not_sampled.iterrows():
            folium.CircleMarker(
                [r["lat"], r["lon"]], radius=4, color="#666", weight=1, fill=True,
                fill_color="#ffffff", fill_opacity=0.6,
                tooltip=f"{r['name']} ({r['county']} Co.) — frame site evaluated, not sampled (no data)",
            ).add_to(fg_ns)
        fg_ns.add_to(m)
        groups.append(fg_ns)

    _add_legend(m, state, lakes, not_sampled, ranges)

    try:
        from folium.plugins import GroupedLayerControl
        GroupedLayerControl(groups={"NLA 2022 variable": groups},
                            exclusive_groups=True, collapsed=False).add_to(m)
    except Exception:
        folium.LayerControl(collapsed=False).add_to(m)
    m.save(str(out))


def _lake_popup(r: dict) -> str:
    """Full per-lake card: every value type, every visit (the 'multiple values per feature')."""
    head = (f"<b>{r['name']}</b> — {r['county']} Co., {r.get('ecoregion','')}<br>"
            f"<span style='color:#666'>COMID {r.get('comid','')} · HUC8 {r.get('huc8','')} · "
            f"{r.get('area_ha','?')} ha · {r['lat']:.4f}, {r['lon']:.4f}</span><hr style='margin:3px 0'>")
    rows = []
    for rec in r.get("_visits", [r]):
        vdate = rec.get("DATE_COL", "?")
        vno = rec.get("VISIT_NO", "?")
        cells = []
        for key, label, units, src, col, *_ in LAYER_VARS:
            v = rec.get(key)
            nd = bool(rec.get(f"{key}_ND", False)) if src == "tox" else False
            if nd:
                s = "ND"
            elif pd.isna(v):
                s = "—"
            else:
                s = f"{v:.3g} {units}".strip()
            cells.append(f"{label}: <b>{s}</b>")
        rows.append(f"<u>Visit {vno} ({vdate})</u><br>" + " · ".join(cells))
    return head + "<br>".join(rows)


def _add_legend(m, state, lakes, not_sampled, ranges) -> None:
    import folium
    grad = "".join(f'<span style="background:{c};width:14px;display:inline-block">&nbsp;</span>'
                   for c in _RAMP)
    rows = ""
    for key, label, units, src, col, log, invert, ref in LAYER_VARS:
        vmin, vmax = ranges[key]
        rng = "—" if pd.isna(vmin) else f"{vmin:.3g}–{vmax:.3g} {units}".strip()
        note = " (inverted: low=red)" if invert else (f" · {ref}" if ref else "")
        rows += f"<tr><td>{label}</td><td>{rng}{note}</td></tr>"
    html = (
        '<div style="position:fixed;bottom:20px;left:20px;z-index:9999;background:white;'
        'padding:9px 11px;border:1px solid #888;font-size:11px;max-width:340px;'
        'box-shadow:2px 2px 6px rgba(0,0,0,.2)">'
        f'<b>NLA 2022 — {state} sampled lakes (n={len(lakes)})</b><br>'
        '<span style="color:#b00">Per-lake, native coordinates, UNWEIGHTED — '
        'NOT a state/national estimate.</span><br>'
        'Each lake sampled once in summer 2022 (some revisited). '
        'Toggle a variable at top-right; click a lake for all values &amp; visits.<br>'
        f'low&nbsp;{grad}&nbsp;high &nbsp; '
        '<span style="border:1px solid #8a8a8a;border-radius:50%;padding:0 4px;'
        'background:#d9d9d9">ND</span>=non-detect · '
        '<span style="border:1px solid #666;border-radius:50%;padding:0 4px">○</span>=not sampled'
        '<table style="margin-top:4px;border-collapse:collapse">'
        f'{rows}</table></div>'
    )
    m.get_root().html.add_child(folium.Element(html))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rawdir", default=str(_DEFAULT_RAW))
    ap.add_argument("--outdir", default=str(_OUTPUTS))
    ap.add_argument("--state", default=None,
                    help="build the layered multi-variable map for one state (e.g. NC)")
    args = ap.parse_args(argv)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.state:
        lakes, not_sampled = build_state_layer_frame(Path(args.rawdir), args.state.upper())
        out = outdir / f"nla2022_{args.state.lower()}_layered_map.html"
        make_layered_state_map(lakes, not_sampled, args.state.upper(), out)
        print(f"{args.state.upper()}: {len(lakes)} sampled lakes mapped "
              f"({len(not_sampled)} evaluated-not-sampled) -> {out}")
        return 0

    df = build_frame(Path(args.rawdir))
    print(f"Built frame: {len(df)} sampled lakes with coordinates + microcystin.")

    make_map(df, outdir / "nla2022_microcystin_map.html")
    make_summary(df, outdir / "nla2022_summary.html")
    make_png(df, outdir / "nla2022_microcystin_map.png")
    n_exceed = int((df["micx_bin"] == 3).sum())
    print(f"Wrote map/summary/png to {outdir}.")
    print(f"Sanity: {n_exceed} lakes >= {MICX_REC_CRITERION} ug/L microcystin (EPA rec. criterion).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
