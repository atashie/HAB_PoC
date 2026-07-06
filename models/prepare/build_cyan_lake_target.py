"""Build the per-lake weekly CyAN target table for Florida (Prepare phase).

Replicates Schaeffer et al.'s `cyan_processing_conus.R`: for each FL resolvable lake x OLCI week,
compute mean / median / SD of CyAN DN over pixels FULLY INSIDE the lake polygon
(`coverage_fraction == 1`), excluding masked cells, and set the WHO Alert Level 1 bloom label =
(median DN >= 130). See `../docs/03-target-definition.md` for the pinned definitions + provenance.

Faithful details:
- DN encoding (cyan/METADATA §4): 0 = below-detection (valid), 1..253 = valid detection, 254 = land,
  255 = no-data/cloud. Valid pixels = DN <= 253; 254/255 excluded (NA), matching Schaeffer's masking.
- "coverage_fraction == 1" = pixels wholly within the lake polygon. We compute each lake's fully-inside
  pixel mask ONCE (geometry is static across weeks) via 8x oversampled rasterization, then apply it to
  all 531 weekly mosaics.
- bloom = median DN >= 130 (12 ug/L chl-a, WHO AL1). A lake-week with 0 valid pixels -> median NaN ->
  bloom = missing (NOT imputed; no ice-fill in FL).

Output: models/data/derived/cyan_lake_weekly_fl.parquet  (long: one row per lake-week)

Run:  python models/prepare/build_cyan_lake_target.py [--limit-weeks N]
"""
from __future__ import annotations

import argparse
import glob
import os
import re

import numpy as np
import geopandas as gpd
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import Window, from_bounds
from rasterio.windows import transform as win_transform

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.abspath(os.path.join(HERE, "..", "..", "data-sources", "cyan", "data", "raw",
                                   "conus_mosaic_weekly"))
LAKES = os.path.abspath(os.path.join(HERE, "..", "data", "derived", "fl_resolvable_lakes.gpkg"))
OUT = os.path.abspath(os.path.join(HERE, "..", "data", "derived", "cyan_lake_weekly_fl.parquet"))

DN_LAND, DN_NODATA, DN_VALID_MAX = 254, 255, 253
AL1_DN = 130                 # median DN >= 130  == WHO AL1 (12 ug/L chl-a); Schaeffer cyan_processing:170
OVERSAMPLE = 8               # subpixel factor for coverage_fraction==1
COVER_MIN = 0.999            # "fully inside"


def olci_files():
    out = []
    for p in sorted(glob.glob(os.path.join(RAW, "*.tif"))):
        m = re.match(r"L(\d{4})(\d{3})(\d{4})(\d{3})\.", os.path.basename(p))
        if m and int(m.group(1)) >= 2016:
            out.append((p, m.groups()))
    return out


def doy_to_iso(year, doy):
    return (pd.Timestamp(f"{year}-01-01") + pd.Timedelta(days=int(doy) - 1)).date().isoformat()


def build_lake_masks(lakes, ref_path):
    """Return {comid: (Window, fully_inside_bool_mask)} computed once from geometry."""
    masks = {}
    with rasterio.open(ref_path) as ds:
        transform, H, W = ds.transform, ds.height, ds.width
    for row in lakes.itertuples():
        geom = row.geometry
        minx, miny, maxx, maxy = geom.bounds
        win = from_bounds(minx, miny, maxx, maxy, transform=transform)
        # pad 1 px and clamp to raster
        col0 = max(0, int(np.floor(win.col_off)) - 1)
        row0 = max(0, int(np.floor(win.row_off)) - 1)
        col1 = min(W, int(np.ceil(win.col_off + win.width)) + 1)
        row1 = min(H, int(np.ceil(win.row_off + win.height)) + 1)
        if col1 <= col0 or row1 <= row0:
            continue
        window = Window(col0, row0, col1 - col0, row1 - row0)
        wtr = win_transform(window, transform)
        h, w = int(window.height), int(window.width)
        # oversampled rasterize -> coverage fraction per native pixel
        fine_tr = wtr * wtr.scale(1.0 / OVERSAMPLE, 1.0 / OVERSAMPLE)
        fine = rasterize([(geom, 1)], out_shape=(h * OVERSAMPLE, w * OVERSAMPLE),
                         transform=fine_tr, fill=0, dtype="uint8")
        cover = fine.reshape(h, OVERSAMPLE, w, OVERSAMPLE).mean(axis=(1, 3))
        inside = cover >= COVER_MIN
        if inside.any():
            masks[int(row.COMID)] = (window, inside)
    return masks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-weeks", type=int, default=0, help="process only first N weeks (test)")
    args = ap.parse_args()

    lakes = gpd.read_file(LAKES)
    lakes["COMID"] = lakes["COMID"].astype("int64")
    files = olci_files()
    if args.limit_weeks:
        files = files[: args.limit_weeks]
    print(f"lakes: {len(lakes)}  |  OLCI weeks: {len(files)}")

    print("precomputing fully-inside pixel masks (once)...")
    masks = build_lake_masks(lakes, files[0][0])
    n_inside = {c: int(m.sum()) for c, (w, m) in masks.items()}
    print(f"  lakes with >=1 fully-inside pixel: {len(masks)} / {len(lakes)}")
    print(f"  inside-pixel count min/median/max: {min(n_inside.values())} / "
          f"{int(np.median(list(n_inside.values())))} / {max(n_inside.values())}")
    area = dict(zip(lakes["COMID"], lakes.get("AREASQKM", pd.Series(index=lakes.index))))
    name = dict(zip(lakes["COMID"], lakes.get("GNIS_NAME", pd.Series(index=lakes.index))))

    rows = []
    for i, (path, (y0, d0, y1, d1)) in enumerate(files):
        start, end = doy_to_iso(y0, d0), doy_to_iso(y1, d1)
        with rasterio.open(path) as ds:
            for comid, (window, inside) in masks.items():
                arr = ds.read(1, window=window)
                vals = arr[inside]
                valid = vals[vals <= DN_VALID_MAX]
                nodata = int(np.count_nonzero((vals == DN_NODATA) | (vals == DN_LAND)))
                n_ins = inside.sum()
                if valid.size:
                    med = float(np.median(valid))
                    sd = float(valid.std(ddof=1)) if valid.size > 1 else np.nan  # R sd(): sample, NA if n=1
                    rows.append((comid, start, end, int(y0), int(n_ins), int(valid.size),
                                 valid.size / n_ins, nodata / n_ins, float(valid.mean()), med, sd,
                                 bool(med >= AL1_DN)))
                else:
                    rows.append((comid, start, end, int(y0), int(n_ins), 0,
                                 0.0 if n_ins else np.nan, nodata / n_ins if n_ins else np.nan,
                                 np.nan, np.nan, np.nan, pd.NA))
        if (i + 1) % 50 == 0 or i + 1 == len(files):
            print(f"  {i + 1}/{len(files)} weeks  ({start})")

    df = pd.DataFrame(rows, columns=["comid", "start_date", "end_date", "year", "n_inside",
                                     "n_valid", "valid_frac", "nodata_frac", "cyan_mean",
                                     "cyan_median", "cyan_sd", "bloom"])
    df["gnis_name"] = df["comid"].map(name)
    df["area_sqkm"] = df["comid"].map(area)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    df.to_parquet(OUT, index=False)

    print("\n" + "=" * 60)
    print(f"wrote {OUT}")
    print(f"  rows: {len(df):,}  |  lakes: {df.comid.nunique()}  |  weeks: {df.start_date.nunique()}")
    valid_lw = df["cyan_median"].notna().sum()
    print(f"  lake-weeks with a valid median: {valid_lw:,} "
          f"({100*valid_lw/len(df):.1f}%)  | missing: {len(df)-valid_lw:,}")
    bl = df["bloom"].dropna()
    print(f"  bloom prevalence (of valid): {100*bl.mean():.2f}%  "
          f"({int(bl.sum()):,} bloom lake-weeks)")
    # coverage sensitivity (Codex H3): low-coverage weeks bias prevalence low
    v = df.dropna(subset=["bloom"]).copy()
    lo = v[v["valid_frac"] < 0.5]
    hi = v[v["valid_frac"] >= 0.5]
    print(f"  QA sensitivity — valid_frac<0.5: {len(lo):,} rows ({100*len(lo)/len(v):.1f}%), "
          f"prevalence {100*lo['bloom'].astype(float).mean():.2f}%  |  "
          f">=0.5: prevalence {100*hi['bloom'].astype(float).mean():.2f}%")
    print("  (primary target keeps parity = all-cloud-only missing; >=0.5 filter is a sensitivity)")
    print("=" * 60)


if __name__ == "__main__":
    main()
