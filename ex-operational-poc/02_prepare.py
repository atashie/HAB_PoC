"""Step 2 - PREPARE.  Turn the CyAN rasters + lake polygons into one tidy table:
one row per (lake, week) with the per-lake median CyAN and the WHO-AL1 bloom label.

Method (fast + faithful to the EPA/Schaeffer recipe):
  1. Rasterize the 133 Florida lake polygons ONCE onto the CyAN grid, restricted to a
     Florida window (all rasters share the same EPSG:5070 grid, so one window fits all).
  2. For each weekly composite, read just that window, keep valid pixels (DN 0..253;
     254=land / 255=cloud are dropped), and take the median DN per lake.
  3. Label: bloom = (median DN >= 130)  ==  WHO Alert Level 1  (~12 ug/L chl-a).

Output: data/lake_week.parquet  (comid, week_start, cyan_median, n_valid, bloom, area_sqkm)
        + a small committed summary in outputs/prepare_summary.md

Run:  python 02_prepare.py [--limit N]      # --limit for a quick smoke test on N weeks
"""
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import from_bounds

import config
from common import parse_week_start


def _olci_rasters():
    # NB: mirrors 01_ingest.list_olci_rasters by design - kept as a tiny local helper so
    # `common.py` stays pure (no filesystem I/O) and the two steps stay file-to-file
    # decoupled. Do not "DRY" this into common without moving I/O there.
    out = []
    for p in sorted(config.CYAN_RAW_DIR.glob("*.tif")):
        ws = parse_week_start(p.name, config.OLCI_PREFIX)
        if ws is not None:
            out.append((p, pd.Timestamp(ws)))
    return sorted(out, key=lambda t: t[1])


def _florida_window(ref_path, lakes, pad=4):
    """Pixel window covering all lakes (+pad) on the shared CyAN grid, plus the matching
    label grid (0 = no lake, k = k-th lake) and the label->(comid, area) map."""
    with rasterio.open(ref_path) as src:
        if lakes.crs != src.crs:                 # align lake CRS to the raster grid, or
            lakes = lakes.to_crs(src.crs)        # medians would come out silently wrong
        minx, miny, maxx, maxy = lakes.total_bounds
        win = from_bounds(minx, miny, maxx, maxy, src.transform).round_offsets().round_lengths()
        win = rasterio.windows.Window(
            max(0, win.col_off - pad), max(0, win.row_off - pad),
            win.width + 2 * pad, win.height + 2 * pad)
        wt = src.window_transform(win)
        shape = (int(win.height), int(win.width))
    shapes = [(geom, i + 1) for i, geom in enumerate(lakes.geometry.values)]
    labels = rasterize(shapes, out_shape=shape, transform=wt, fill=0, dtype="int32")
    meta = {i + 1: (int(r.COMID), float(r.AREASQKM))
            for i, r in enumerate(lakes.itertuples(index=False))}
    return win, labels, meta


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    limit = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else None

    lakes = gpd.read_file(config.FL_LAKES_GPKG)[["COMID", "AREASQKM", "geometry"]]
    rasters = _olci_rasters()
    if limit:
        rasters = rasters[:limit]
    if not rasters:
        sys.exit("No OLCI rasters found - run 01_ingest.py first.")

    win, labels, meta = _florida_window(rasters[0][0], lakes)
    flat = labels.ravel()
    lake_pix = np.where(flat > 0)[0]          # pixel indices that fall in some lake
    lab_at = flat[lake_pix]                    # lake id at each of those pixels
    print(f"Florida window {labels.shape}, {len(lake_pix):,} lake pixels, "
          f"{len(rasters)} weeks -> computing per-lake medians ...")

    rows = []
    for k, (path, ws) in enumerate(rasters):
        with rasterio.open(path) as src:
            dn = src.read(1, window=win).ravel()[lake_pix]
        valid = dn <= config.DN_VALID_MAX
        if not valid.any():
            continue
        g = pd.DataFrame({"lab": lab_at[valid], "dn": dn[valid].astype(np.int16)})
        med = g.groupby("lab")["dn"].median()
        cnt = g.groupby("lab")["dn"].size()
        for lab, m in med.items():
            comid, area = meta[lab]
            rows.append((comid, ws, float(m), int(cnt[lab]),
                         int(m >= config.AL1_THRESHOLD), area))
        if (k + 1) % 100 == 0:
            print(f"  {k + 1}/{len(rasters)} weeks")

    panel = pd.DataFrame(rows, columns=["comid", "week_start", "cyan_median",
                                        "n_valid", "bloom", "area_sqkm"])
    # Coverage floor: a lake-week is labelled from its valid (cloud-free) pixels. We keep
    # the EPA/Schaeffer-parity default (>= 1 pixel) but expose the knob and REPORT how many
    # low-coverage weeks exist, rather than silently thresholding (../models DESIGN sec.4).
    low_frac = float((panel["n_valid"] < 5).mean())          # weeks decided by < 5 pixels
    panel = panel[panel["n_valid"] >= config.MIN_VALID_PIXELS].reset_index(drop=True)
    config.DATA.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(config.LAKE_WEEK_PARQUET, index=False)

    base = panel["bloom"].mean()
    summary = (
        f"# Prepare summary - lake-week panel\n\n"
        f"- Source: {len(rasters)} OLCI weekly CyAN CONUS mosaics "
        f"[{rasters[0][1].date()} -> {rasters[-1][1].date()}]\n"
        f"- Lakes: {panel['comid'].nunique()} of {len(lakes)} Florida resolvable lakes\n"
        f"- Rows (valid lake-weeks, >= {config.MIN_VALID_PIXELS} px): {len(panel):,}\n"
        f"- Bloom base rate (median DN >= {config.AL1_THRESHOLD}): {base:.3f}\n"
        f"- Median valid pixels/lake-week: {int(panel['n_valid'].median())}\n"
        f"- Low-coverage weeks (< 5 valid px, label is noise-prone): {low_frac:.1%}\n"
    )
    (config.OUTPUTS / "prepare_summary.md").write_text(summary, encoding="utf-8")
    print(summary)
    print(f"Wrote {config.LAKE_WEEK_PARQUET}")


if __name__ == "__main__":
    main()
