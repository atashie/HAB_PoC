#!/usr/bin/env python
"""QA/QC for pulled CyAN CI_cyano GeoTIFF tiles.

Checks every raster in data/raw and emits:
  * outputs/qa_summary.json  (machine-readable, per-file + cross-file)
  * outputs/qa_report.md     (human-readable)

What it verifies / reports (grounded in METADATA.md):
  * File integrity: sha256 recomputed vs the download manifest.
  * Structure: single band, uint8, CRS (expect Albers Equal Area), pixel size ~300 m.
  * Processing version read *from the GeoTIFF metadata* (resolves the CYANV6T/CYAN
    filename ambiguity from the data itself).
  * DN distribution across the exact CyAN categories: below-detection(0) / valid(1-253)
    / land(254) / no-data(255) — with % of each, and valid-pixel CI stats.
  * Cross-file consistency for a tile (same CRS/shape/transform), and any anomalies
    (unexpected DN values, all-nodata scenes, CRS mismatch).

Usage:  python qa_cyan.py [--raw <dir>] [--outdir <dir>]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import rasterio

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from _common import net                       # noqa: E402
from cyan.access import cyan_api as c          # noqa: E402

_CYAN = _DATA_SOURCES / "cyan"
_DEFAULT_RAW = _CYAN / "data" / "raw"
_DEFAULT_OUT = _CYAN / "outputs"


def _find_version_tag(tags: dict) -> str | None:
    for k, v in tags.items():
        if "version" in k.lower():
            return f"{k}={v}"
    # some products stash it in the value text
    for k, v in tags.items():
        if isinstance(v, str) and ("CYAN" in v.upper() and "V" in v.upper()):
            return f"{k}={v}"
    return None


def qa_one(path: Path, manifest_by_name: dict) -> dict:
    rec: dict = {"filename": path.name}
    parsed = c.parse_cyan_filename(path.name)
    if parsed:
        rec["parsed"] = {"stream": parsed.stream, "temporal": parsed.temporal,
                         "tile": parsed.tile, "region": parsed.region,
                         "start_date": parsed.start_date, "end_date": parsed.end_date}

    # integrity vs manifest
    m = manifest_by_name.get(path.name)
    if m:
        rec["manifest_sha256"] = m.get("sha256")
        rec["sha256_ok"] = (net._sha256(path) == m.get("sha256"))
    else:
        rec["sha256_ok"] = None  # not in manifest

    with rasterio.open(path) as ds:
        rec["band_count"] = ds.count
        rec["dtype"] = ds.dtypes[0]
        rec["width"], rec["height"] = ds.width, ds.height
        rec["crs"] = str(ds.crs)
        rec["transform"] = [round(v, 6) for v in tuple(ds.transform)[:6]]
        rec["nodata_tag"] = ds.nodata
        res = ds.res
        rec["pixel_size_m"] = [round(res[0], 4), round(res[1], 4)]
        b = ds.bounds
        rec["bounds"] = [b.left, b.bottom, b.right, b.top]
        rec["gtiff_tags"] = ds.tags()
        rec["processing_version_tag"] = _find_version_tag(ds.tags())

        arr = ds.read(1)

    # structural checks
    rec["is_single_band_uint8"] = (ds.count == 1 and rec["dtype"] == "uint8")
    crs_up = rec["crs"].upper()
    rec["crs_is_albers"] = ("ALBERS" in crs_up) or ("5070" in crs_up)

    # DN distribution over exact CyAN categories
    total = int(arr.size)
    masks = c.classify_dn(arr)
    counts = {k: int(v.sum()) for k, v in masks.items()}
    rec["dn_counts"] = counts
    rec["dn_pct"] = {k: round(100.0 * v / total, 4) for k, v in counts.items()}
    rec["total_pixels"] = total

    # any DN outside the defined scheme? (should be impossible for uint8, but verify logic)
    accounted = sum(counts.values())
    rec["unaccounted_pixels"] = int(total - accounted)

    # valid-pixel CI stats
    valid = masks["valid"]
    rec["valid_pixel_count"] = int(valid.sum())
    if valid.any():
        dn_valid = arr[valid]
        ci = c.dn_to_ci(dn_valid)
        rec["dn_valid_min"], rec["dn_valid_max"] = int(dn_valid.min()), int(dn_valid.max())
        rec["ci_min"] = float(np.nanmin(ci))
        rec["ci_max"] = float(np.nanmax(ci))
        rec["ci_mean"] = float(np.nanmean(ci))
        rec["ci_median"] = float(np.nanmedian(ci))
    else:
        rec["dn_valid_min"] = rec["dn_valid_max"] = None
        rec["ci_min"] = rec["ci_max"] = rec["ci_mean"] = rec["ci_median"] = None

    # anomaly flags
    flags = []
    if not rec["is_single_band_uint8"]:
        flags.append("not single-band uint8")
    if not rec["crs_is_albers"]:
        flags.append(f"CRS not Albers ({rec['crs']})")
    if rec["dn_pct"]["nodata"] >= 99.0:
        flags.append("scene ~entirely no-data (cloud/ice?)")
    if rec["valid_pixel_count"] == 0:
        flags.append("no valid CI pixels")
    if rec["unaccounted_pixels"] != 0:
        flags.append("DN values outside 0/1-253/254/255 scheme")
    if rec.get("sha256_ok") is False:
        flags.append("sha256 mismatch vs manifest")
    if rec.get("sha256_ok") is None:
        flags.append("not in download manifest (no provenance / traceability gap)")
    if rec["processing_version_tag"] is None:
        flags.append("no processing-version tag found in GeoTIFF metadata")
    rec["flags"] = flags
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", default=str(_DEFAULT_RAW))
    ap.add_argument("--outdir", default=str(_DEFAULT_OUT))
    args = ap.parse_args(argv)

    raw = Path(args.raw)
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    tifs = sorted(raw.glob("*.tif"))
    if not tifs:
        print(f"[qa] no .tif files in {raw}. Pull data first (access/pull_cyan.py).",
              file=sys.stderr)
        return 2

    manifest = net.read_manifest(raw / "manifest.jsonl")
    manifest_by_name = {m["filename"]: m for m in manifest if "filename" in m}

    print(f"[qa] checking {len(tifs)} raster(s) in {raw}")
    per_file = []
    for t in tifs:
        try:
            per_file.append(qa_one(t, manifest_by_name))
        except Exception as e:
            per_file.append({"filename": t.name, "error": repr(e), "flags": ["QA ERROR"]})

    # cross-file consistency (per tile)
    by_tile: dict[str, list[dict]] = {}
    for r in per_file:
        tile = r.get("parsed", {}).get("tile", "?")
        by_tile.setdefault(tile, []).append(r)
    cross = {}
    for tile, recs in by_tile.items():
        crss = {r.get("crs") for r in recs if "crs" in r}
        shapes = {(r.get("width"), r.get("height")) for r in recs if "width" in r}
        transforms = {tuple(r["transform"]) for r in recs if "transform" in r}
        versions = Counter(r.get("processing_version_tag") for r in recs)
        streams = Counter(r.get("parsed", {}).get("stream") for r in recs)
        cross[tile] = {
            "n_files": len(recs),
            "crs_consistent": len(crss) == 1,
            "shape_consistent": len(shapes) == 1,
            "transform_consistent": len(transforms) == 1,
            "crs_values": sorted(str(x) for x in crss),
            "shapes": sorted(str(x) for x in shapes),
            "transforms": sorted(str(list(x)) for x in transforms),
            "processing_version_tags": dict(versions),
            "streams": dict(streams),
        }

    summary = {
        "generated_utc": net._utc_now_iso(),
        "raw_dir": str(raw),
        "n_files": len(per_file),
        "n_files_with_flags": sum(1 for r in per_file if r.get("flags")),
        "cross_file_by_tile": cross,
        "per_file": per_file,
    }
    (out / "qa_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    _write_markdown(summary, out / "qa_report.md")
    print(f"[qa] wrote {out/'qa_summary.json'} and {out/'qa_report.md'}")
    print(f"[qa] {summary['n_files_with_flags']}/{summary['n_files']} file(s) carry QA flags")
    return 0


def _write_markdown(summary: dict, path: Path) -> None:
    L = []
    L.append("# CyAN CI_cyano — QA/QC report\n")
    L.append(f"*Generated {summary['generated_utc']} · {summary['n_files']} file(s) from "
             f"`{summary['raw_dir']}`*\n")
    L.append(f"**{summary['n_files_with_flags']} of {summary['n_files']} files carry QA flags.**\n")

    L.append("\n## Cross-file consistency (per tile)\n")
    L.append("| Tile | Files | CRS consistent | Shape consistent | Transform consistent | Processing-version tag(s) | Stream(s) |")
    L.append("|------|-------|----------------|------------------|----------------------|---------------------------|-----------|")
    for tile, x in summary["cross_file_by_tile"].items():
        L.append(f"| {tile} | {x['n_files']} | {x['crs_consistent']} | {x['shape_consistent']} "
                 f"| {x.get('transform_consistent')} | {x['processing_version_tags']} | {x['streams']} |")

    L.append("\n## Per-file summary\n")
    L.append("| File | Stream | Dates | %valid | %below-det | %land | %nodata | CI mean | Ver tag | Flags |")
    L.append("|------|--------|-------|--------|-----------|-------|---------|---------|---------|-------|")
    for r in summary["per_file"]:
        if "error" in r:
            L.append(f"| {r['filename']} | | | | | | | | | ERROR: {r['error']} |")
            continue
        p = r.get("parsed", {})
        dn = r.get("dn_pct", {})
        dates = f"{p.get('start_date','?')}→{p.get('end_date','?')}"
        cim = r.get("ci_mean")
        cim_s = "—" if cim is None else f"{cim:.4g}"
        ver = r.get("processing_version_tag") or "—"
        flags = "; ".join(r.get("flags", [])) or "ok"
        L.append(f"| {r['filename'][:40]} | {p.get('stream','?')} | {dates} "
                 f"| {dn.get('valid','?')} | {dn.get('below_detection','?')} "
                 f"| {dn.get('land','?')} | {dn.get('nodata','?')} | {cim_s} | {ver} | {flags} |")

    L.append("\n## Notes\n")
    L.append("- DN categories are the exact CyAN encoding: 0=below detection, 1–253=valid CI, "
             "254=land, 255=no-data (see `METADATA.md` §4).")
    L.append("- `%below-det` (DN 0) is *measured non-detect*, not missing — reported separately from `%nodata`.")
    L.append("- Processing version is read from the GeoTIFF metadata, not inferred from the filename.")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
