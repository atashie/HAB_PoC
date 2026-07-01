#!/usr/bin/env python
"""Visualize pulled CyAN CI_cyano tiles: interactive HTML map + summary charts.

Outputs (into outputs/):
  * cyan_<tile>_map.html      — Folium map; each date is a toggleable CI overlay
                                 (Albers tiles reprojected to lat/lon; exact DN
                                 categories colorized; land/no-data transparent).
  * cyan_<tile>_summary.html  — Plotly: valid-pixel CI over time + DN-category
                                 composition over time.

Colorization (see METADATA.md §4):
  * DN 1–253  -> CI, 'turbo' colormap on log10(CI)
  * DN 0      -> pale grey, semi-transparent ("below detection" = measured, no bloom)
  * DN 254/255 (land / no-data) -> fully transparent

Usage:  python viz_cyan.py [--raw <dir>] [--outdir <dir>] [--tile 7_2] [--max-overlays N]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from cyan.access import cyan_api as c          # noqa: E402

_CYAN = _DATA_SOURCES / "cyan"
_DEFAULT_RAW = _CYAN / "data" / "raw"
_DEFAULT_OUT = _CYAN / "outputs"


def warp_dn_to_4326(path: Path):
    """Reproject the DN band to EPSG:4326 with NEAREST (preserves category codes).

    Returns (dn_array, (west, south, east, north)).
    """
    dst_crs = "EPSG:4326"
    with rasterio.open(path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        dst = np.full((height, width), 255, dtype="uint8")  # fill with no-data
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=transform, dst_crs=dst_crs,
            resampling=Resampling.nearest, src_nodata=255, dst_nodata=255,
        )
    west = transform.c
    north = transform.f
    east = west + transform.a * width
    south = north + transform.e * height
    return dst, (west, south, east, north)


def crop_to_bbox(dn: np.ndarray, bounds, bbox):
    """Spatially SUBSET (crop) dn to bbox=(lon_w, lat_s, lon_e, lat_n). Returns
    (sub_dn, sub_bounds). This is a crop (a scope choice), NOT aggregation — every
    retained pixel keeps its exact native value. Returns input unchanged if bbox is None
    or doesn't overlap.
    """
    if bbox is None:
        return dn, bounds
    w, s, e, n = bounds
    H, W = dn.shape
    dlon, dlat = (e - w) / W, (s - n) / H          # dlat negative (N->S)
    lons = w + (np.arange(W) + 0.5) * dlon
    lats = n + (np.arange(H) + 0.5) * dlat
    bw, bs, be, bn = bbox
    jc = np.where((lons >= bw) & (lons <= be))[0]
    ir = np.where((lats >= bs) & (lats <= bn))[0]
    if len(jc) == 0 or len(ir) == 0:
        return dn, bounds
    i0, i1, j0, j1 = ir[0], ir[-1] + 1, jc[0], jc[-1] + 1
    sub = dn[i0:i1, j0:j1]
    return sub, (w + j0 * dlon, n + i1 * dlat, w + j1 * dlon, n + i0 * dlat)


def colorize(dn: np.ndarray) -> np.ndarray:
    """DN array -> RGBA uint8 for display."""
    import matplotlib
    turbo = matplotlib.colormaps["turbo"]   # modern API (cm.get_cmap removed in mpl 3.9+)
    masks = c.classify_dn(dn)
    h, w = dn.shape
    rgba = np.zeros((h, w, 4), dtype="uint8")  # transparent by default (land/nodata)

    # below detection: pale grey, semi-transparent
    bd = masks["below_detection"]
    rgba[bd] = (205, 214, 220, 90)

    # valid CI: turbo on log10(CI), scaled across the valid CI dynamic range
    valid = masks["valid"]
    if valid.any():
        ci = c.dn_to_ci(dn[valid])
        logci = np.log10(ci)
        lo = np.log10(c.dn_to_ci(np.array([c.DN_VALID_MIN]))[0])
        hi = np.log10(c.dn_to_ci(np.array([c.DN_VALID_MAX]))[0])
        norm = np.clip((logci - lo) / (hi - lo), 0, 1)
        colors = (turbo(norm)[:, :4] * 255).astype("uint8")
        colors[:, 3] = 220
        rgba[valid] = colors
    return rgba


def hover_features(dn: np.ndarray, bounds, date_label: str, agg: int = 1) -> list[dict]:
    """Build one GeoJSON polygon per valid-CI pixel with its EXACT value.

    ``agg=1`` (DEFAULT) = **native 300 m pixels, NO aggregation** — each feature carries
    that pixel's exact DN, CI, and approx cells/mL. Only valid pixels (DN 1–253) are
    emitted; land / no-data / below-detection are shown by the ImageOverlay + basemap.

    ``agg>1`` **spatially MEAN-aggregates** agg×agg native pixels into one cell. This
    DISTORTS the data and must only be used with explicit user permission (project rule:
    never aggregate without asking). It is opt-in via the CLI ``--agg`` flag.
    """
    import matplotlib
    turbo = matplotlib.colormaps["turbo"]

    w, s, e, n = bounds
    H, W = dn.shape
    lo = c.DN_VALID_MIN * c.CI_SLOPE + c.CI_INTERCEPT          # log10(CI) at DN=1
    hi = c.DN_VALID_MAX * c.CI_SLOPE + c.CI_INTERCEPT          # log10(CI) at DN=253
    dlon = (e - w) / W
    dlat = (s - n) / H                                          # negative (N->S)

    def _feature(lat_s, lon_w, lat_n, lon_e, dn_val, ci_val, npix):
        cells = ci_val * c.CELLS_PER_ML_FACTOR
        norm = float(np.clip((np.log10(ci_val) - lo) / (hi - lo), 0, 1))
        r, g, b, _ = turbo(norm)
        color = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
        rw, re_, rs, rn = round(lon_w, 4), round(lon_e, 4), round(lat_s, 4), round(lat_n, 4)
        return {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [[
                [rw, rs], [re_, rs], [re_, rn], [rw, rn], [rw, rs]]]},
            "properties": {
                "date": date_label, "dn": int(round(dn_val)),
                "ci": f"{ci_val:.4g}", "cells": f"{cells:,.0f}", "npix": int(npix),
                "color": color,
            },
        }

    feats = []
    if agg <= 1:
        # NATIVE: exact per-pixel values, no aggregation.
        valid = (dn >= c.DN_VALID_MIN) & (dn <= c.DN_VALID_MAX)
        for i, j in np.argwhere(valid):
            dn_val = float(dn[i, j])
            ci_val = 10.0 ** (dn_val * c.CI_SLOPE + c.CI_INTERCEPT)
            lat_n = n + i * dlat
            lat_s = n + (i + 1) * dlat
            lon_w = w + j * dlon
            lon_e = w + (j + 1) * dlon
            feats.append(_feature(lat_s, lon_w, lat_n, lon_e, dn_val, ci_val, 1))
        return feats

    # agg>1: EXPLICIT, opt-in mean aggregation (distorts data — user must request it).
    Hb, Wb = H // agg, W // agg
    if Hb == 0 or Wb == 0:
        return []
    dn_t = dn[:Hb * agg, :Wb * agg].astype("float64")
    valid = (dn_t >= c.DN_VALID_MIN) & (dn_t <= c.DN_VALID_MAX)
    ci = np.where(valid, 10.0 ** (dn_t * c.CI_SLOPE + c.CI_INTERCEPT), np.nan)
    nvalid = valid.reshape(Hb, agg, Wb, agg).sum(axis=(1, 3))
    ci_sum = np.nansum(ci.reshape(Hb, agg, Wb, agg), axis=(1, 3))
    dn_sum = np.nansum(np.where(valid, dn_t, np.nan).reshape(Hb, agg, Wb, agg), axis=(1, 3))
    for bi, bj in np.argwhere(nvalid > 0):
        npix = int(nvalid[bi, bj])
        ci_val = float(ci_sum[bi, bj] / npix)
        dn_val = float(dn_sum[bi, bj] / npix)
        lat_n = n + bi * agg * dlat
        lat_s = n + (bi + 1) * agg * dlat
        lon_w = w + bj * agg * dlon
        lon_e = w + (bj + 1) * agg * dlon
        feats.append(_feature(lat_s, lon_w, lat_n, lon_e, dn_val, ci_val, npix))
    return feats


def make_map(files, raw: Path, out: Path, tile: str, max_overlays: int,
             agg: int = 1, bbox=None) -> Path | None:
    import folium
    import branca.colormap as bcm
    from folium.raster_layers import ImageOverlay
    from folium.features import GeoJson, GeoJsonTooltip
    from folium.plugins import MousePosition

    files = sorted(files, key=lambda x: x.start_date)
    if max_overlays and len(files) > max_overlays:
        # Sample EVENLY across the sorted series so the map shows the seasonal
        # progression (winter -> bloom peak -> fall), not just the first N weeks.
        idx = sorted(set(np.linspace(0, len(files) - 1, max_overlays).round().astype(int).tolist()))
        files = [files[i] for i in idx]
    if not files:
        return None

    _dn0, _b0 = warp_dn_to_4326(raw / files[0].filename)
    _dn0, (w0, s0, e0, n0) = crop_to_bbox(_dn0, _b0, bbox)
    m = folium.Map(location=[(s0 + n0) / 2, (w0 + e0) / 2],
                   zoom_start=9 if bbox else 8,
                   tiles="CartoDB positron", control_scale=True)

    native = agg <= 1
    px_km = round(0.3 * max(agg, 1), 1)
    week_groups = []
    total_hover = 0
    for k, f in enumerate(files):
        dn, bounds = warp_dn_to_4326(raw / f.filename)
        dn, bounds = crop_to_bbox(dn, bounds, bbox)   # scope crop only (no aggregation)
        w, s, e, n = bounds
        rgba = colorize(dn)
        label = f"{f.start_date}→{f.end_date} ({f.stream})"
        # One FeatureGroup per week; GroupedLayerControl makes them mutually exclusive
        # (radio) so weeks don't stack, while the basemap stays visible.
        fg = folium.FeatureGroup(name=label, show=(k == 0))
        ImageOverlay(image=rgba, bounds=[[s, w], [n, e]], opacity=1.0,
                     mercator_project=True).add_to(fg)
        feats = hover_features(dn, bounds, f.start_date, agg=agg)
        total_hover += len(feats)
        if feats:
            GeoJson(
                {"type": "FeatureCollection", "features": feats},
                style_function=lambda x: {"fillColor": x["properties"]["color"],
                                          "color": x["properties"]["color"],
                                          "weight": 0, "fillOpacity": 0.35},
                highlight_function=lambda x: {"weight": 1, "color": "#000000",
                                              "fillOpacity": 0.6},
                tooltip=GeoJsonTooltip(
                    fields=["date", "dn", "ci", "cells", "npix"],
                    aliases=["Week start:", "DN:", "CI_cyano (sr⁻¹):",
                             "~cells/mL (approx):", "native px in cell:"],
                    sticky=True, localize=True),
                embed=True,
            ).add_to(fg)
        fg.add_to(m)
        week_groups.append(fg)

    MousePosition(position="topright", separator=" , ", prefix="lat, lon:",
                  num_digits=4, lat_formatter=None, lng_formatter=None).add_to(m)

    grid_note = ("native 300 m pixels (no aggregation)" if native
                 else f"⚠ MEAN-AGGREGATED to ~{px_km} km cells (opt-in --agg {agg})")
    ci_lo = float(c.dn_to_ci(np.array([c.DN_VALID_MIN]))[0])
    ci_hi = float(c.dn_to_ci(np.array([c.DN_VALID_MAX]))[0])
    bcm.LinearColormap(
        colors=["#30123b", "#28bceb", "#a4fc3c", "#fb7e21", "#7a0403"],
        vmin=ci_lo, vmax=ci_hi,
        caption=(f"CyAN CI_cyano (sr⁻¹). Hover a cell for value & ~cells/mL. "
                 f"Grey=below detection; blank=land/no-data. Hover grid: {grid_note}."),
    ).add_to(m)

    # Exclusive (radio) selector over the weeks; falls back to a plain LayerControl
    # if GroupedLayerControl is unavailable in this folium build.
    try:
        from folium.plugins import GroupedLayerControl
        GroupedLayerControl(groups={"CyAN week": week_groups},
                            exclusive_groups=True, collapsed=False).add_to(m)
    except Exception:
        folium.LayerControl(collapsed=False).add_to(m)

    dst = out / f"cyan_{tile}_map.html"
    m.save(str(dst))
    print(f"[viz] map: {len(files)} weeks, {total_hover} hover cells total "
          f"({'native 300 m' if native else f'AGGREGATED ~{px_km} km'})")
    return dst


def make_summary(files, raw: Path, out: Path, tile: str) -> Path | None:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # NOTE: this summary is an EXPLICITLY-AGGREGATED DIAGNOSTIC. Each scene is reduced
    # to per-date spatial statistics (mean CI over valid pixels; DN-category %). That is
    # spatial aggregation — a time-series summary cannot exist without it — so it is
    # labeled as such in the chart and is NOT an input to any model. Native, non-aggregated
    # values live in the map (viz map hover) and the raw GeoTIFFs. (Per the project
    # aggregation rule, aggregation is surfaced, never silent — see METADATA.md §12.)
    rows = []
    for f in sorted(files, key=lambda x: x.start_date):
        with rasterio.open(raw / f.filename) as ds:
            arr = ds.read(1)
        masks = c.classify_dn(arr)
        total = arr.size
        valid = masks["valid"]
        ci_mean = float(np.nanmean(c.dn_to_ci(arr[valid]))) if valid.any() else np.nan
        rows.append({
            "date": f.start_date,
            "ci_mean": ci_mean,
            "pct_valid": 100 * valid.sum() / total,
            "pct_below": 100 * masks["below_detection"].sum() / total,
            "pct_land": 100 * masks["land"].sum() / total,
            "pct_nodata": 100 * masks["nodata"].sum() / total,
        })
    if not rows:
        return None
    dates = [r["date"] for r in rows]

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
        subplot_titles=("Mean CI_cyano over valid pixels — ⚠ SPATIALLY AGGREGATED diagnostic",
                        "DN-category composition over time (% of tile pixels) — aggregated"))

    fig.add_trace(go.Scatter(x=dates, y=[r["ci_mean"] for r in rows],
                             mode="lines+markers", name="mean CI (valid px)"), row=1, col=1)
    for key, label, color in [
        ("pct_valid", "valid (CI)", "#1f9e46"),
        ("pct_below", "below detection", "#b0bcc4"),
        ("pct_land", "land", "#8c6d31"),
        ("pct_nodata", "no-data (cloud/ice)", "#444444"),
    ]:
        fig.add_trace(go.Bar(x=dates, y=[r[key] for r in rows], name=label,
                             marker_color=color), row=2, col=1)
    fig.update_layout(barmode="stack", height=760,
                      title=(f"CyAN CI_cyano — tile {tile} summary (SePRO HAB PoC)<br>"
                             f"<sup>⚠ Aggregated diagnostic (per-date spatial statistics), "
                             f"not model input. Native values: map hover / raw GeoTIFFs.</sup>"),
                      legend=dict(orientation="h"))
    fig.update_yaxes(title_text="CI (sr^-1)", row=1, col=1)
    fig.update_yaxes(title_text="% of pixels", row=2, col=1)

    dst = out / f"cyan_{tile}_summary.html"
    fig.write_html(str(dst), include_plotlyjs="cdn")
    return dst


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", default=str(_DEFAULT_RAW))
    ap.add_argument("--outdir", default=str(_DEFAULT_OUT))
    ap.add_argument("--tile", default=None, help="restrict to one tile, e.g. 7_2")
    ap.add_argument("--max-overlays", type=int, default=8,
                    help="number of weeks shown on the map (evenly sampled); 0 = all")
    ap.add_argument("--agg", type=int, default=1,
                    help="hover-grid aggregation factor. 1 = NATIVE 300 m, no aggregation "
                         "(default). >1 MEAN-aggregates agg×agg pixels (distorts data) — "
                         "opt-in only, per project rule that aggregation needs explicit permission.")
    ap.add_argument("--bbox", type=float, nargs=4, default=None,
                    metavar=("LON_W", "LAT_S", "LON_E", "LAT_N"),
                    help="crop the map to this lon/lat box (scope subset, NOT aggregation) "
                         "to keep native-resolution hover at a usable file size.")
    args = ap.parse_args(argv)
    if args.agg > 1:
        print(f"[viz] ⚠ --agg {args.agg}: hover grid will be MEAN-AGGREGATED to "
              f"~{round(0.3*args.agg,1)} km cells (opt-in; distorts native values).")

    raw, out = Path(args.raw), Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    files = [c.parse_cyan_filename(p.name) for p in sorted(raw.glob("*.tif"))]
    files = [f for f in files if f]
    if args.tile:
        files = [f for f in files if f.tile == args.tile]
    if not files:
        print(f"[viz] no parseable CyAN tiles in {raw}"
              f"{' for tile ' + args.tile if args.tile else ''}. Pull data first.",
              file=sys.stderr)
        return 2

    tiles = sorted({f.tile for f in files})
    for tile in tiles:
        tfiles = sorted([f for f in files if f.tile == tile], key=lambda x: x.start_date)
        mp = make_map(tfiles, raw, out, tile, args.max_overlays, agg=args.agg, bbox=args.bbox)
        sm = make_summary(tfiles, raw, out, tile)
        print(f"[viz] tile {tile}: {len(tfiles)} file(s) -> "
              f"{mp.name if mp else 'no map'}, {sm.name if sm else 'no summary'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
