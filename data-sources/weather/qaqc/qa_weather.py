#!/usr/bin/env python
"""QA/QC for the weather layer (ERA5 GRIB + ECMWF open-data forecast GRIB2).

Verifies from the data itself, not assumptions (../METADATA.md §4, §11):
  * Integrity   — recompute sha256 vs the manifest; flag missing/mismatched files.
  * Structure   — variables, grid shape + spacing, lat/lon bounds & convention, steps,
                  run/valid times; confirm the 0.25° regular lat/lon grid.
  * Provenance  — ERA5 `expver` (1=final, 5=ERA5T preliminary) when present; forecasts
                  have no expver (note it). Surfaces accumulation variables (tp/ssrd/…).
  * Sanity      — per-variable min/max/mean over the Lake Erie crop, at native resolution.
                  ⚠ These region stats are a *labeled QA diagnostic*, not a model input and
                  NOT a spatial aggregation of the stored data (the GRIB stays native).

Emits outputs/qa_report.md (human) + outputs/qa_summary.json (machine), mirroring the
CyAN/NARS/WQP QA pattern.

Usage
-----
python qa_weather.py                      # scan the forecast + era5 raw dirs & manifests
python qa_weather.py --file <path.grib2>  # QA a single file
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

from _common import net                          # noqa: E402

_WEATHER_DIR = _DATA_SOURCES / "weather"
_RAW = _WEATHER_DIR / "data" / "raw"
_OUT = _WEATHER_DIR / "outputs"
_MANIFESTS = {
    "forecast": _RAW / "forecast_manifest.jsonl",
    "era5": _RAW / "era5_manifest.jsonl",
    "era5_daily": _RAW / "era5_daily_manifest.jsonl",
}
# Western Lake Erie basin (Maumee) — matches CyAN 7_2 / WQP HUC 04100009.
LAKE_ERIE_BBOX = dict(north=42.5, west=-84.5, south=41.0, east=-82.0)


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def _manifest_index(manifest: Path) -> dict:
    """Map absolute file path -> manifest record (last one wins)."""
    idx = {}
    for rec in net.read_manifest(manifest):
        if "path" in rec:
            idx[str((_DATA_SOURCES / rec["path"]).resolve())] = rec
    return idx


def _crop(ds, bbox):
    """Crop to a lat/lon box, native resolution. bbox=None → whole file (already an AOI)."""
    if bbox is None:
        return ds
    lat = ds["latitude"]
    lon = ds["longitude"]
    lat_sel = (lat <= bbox["north"]) & (lat >= bbox["south"])
    lon_sel = (lon <= bbox["east"]) & (lon >= bbox["west"])
    return ds.isel(latitude=lat_sel.values.nonzero()[0],
                   longitude=lon_sel.values.nonzero()[0])


def qa_grib(path: Path, expected_sha: str | None, cli_bbox=None):
    """Return a QA record for one weather file (GRIB/GRIB2 or NetCDF)."""
    import numpy as np

    rec = {"path": str(path.relative_to(_DATA_SOURCES)), "checks": {}, "flags": []}

    # --- integrity ---
    if not path.is_file():
        rec["flags"].append("FILE_MISSING")
        return rec
    have = _sha256(path)
    rec["bytes"] = path.stat().st_size
    rec["sha256"] = have
    if expected_sha is None:
        rec["checks"]["integrity"] = "no_manifest_sha"
        rec["flags"].append("NO_MANIFEST_SHA")
    elif have == expected_sha:
        rec["checks"]["integrity"] = "verified"
    else:
        rec["checks"]["integrity"] = "MISMATCH"
        rec["flags"].append("SHA_MISMATCH")

    # --- structure (NetCDF via xarray, or GRIB via cfgrib multi-hypercube) ---
    try:
        if path.suffix == ".nc":
            import xarray as xr
            datasets = [xr.open_dataset(path)]
        else:
            import cfgrib
            datasets = cfgrib.open_datasets(str(path))
    except Exception as e:  # unreadable — flag, don't crash the run
        rec["flags"].append(f"UNREADABLE ({type(e).__name__})")
        return rec
    variables = {}
    grid = None
    region_bbox = None
    steps = set()
    expvers = set()
    for ds in datasets:
        # grid facts (identical across sub-datasets for one run)
        if grid is None and {"latitude", "longitude"} <= set(ds.coords):
            lat = ds["latitude"].values
            lon = ds["longitude"].values
            grid = {
                "nlat": int(lat.size), "nlon": int(lon.size),
                "lat_min": float(np.min(lat)), "lat_max": float(np.max(lat)),
                "lon_min": float(np.min(lon)), "lon_max": float(np.max(lon)),
                "dlat": float(abs(np.round(np.diff(lat).mean(), 4))) if lat.size > 1 else None,
                "dlon": float(abs(np.round(np.diff(lon).mean(), 4))) if lon.size > 1 else None,
                "lon_convention": "-180..180" if float(np.min(lon)) < 0 else "0..360",
            }
            # sanity-crop region: global files → an AOI (Lake Erie or --bbox);
            # AOI-subset files (ERA5/daily) are already local → whole file.
            is_global = grid["nlat"] >= 300 or (grid["lon_max"] - grid["lon_min"]) >= 350
            region_bbox = cli_bbox if cli_bbox is not None else (
                LAKE_ERIE_BBOX if is_global else None)
        if "step" in ds.coords:
            sv = np.atleast_1d(ds["step"].values)
            for s in sv:
                steps.add(int(np.array(s, dtype="timedelta64[h]").astype(int)))
        if "expver" in ds.coords or "expver" in getattr(ds, "attrs", {}):
            try:
                for e in np.atleast_1d(ds["expver"].values):
                    expvers.add(str(e))
            except Exception:
                pass

        # per-variable region sanity (native crop; labeled diagnostic)
        crop = _crop(ds, region_bbox)
        for name, da in ds.data_vars.items():
            units = da.attrs.get("units", "")
            long_name = da.attrs.get("long_name", da.attrs.get("GRIB_name", name))
            accumulation = da.attrs.get("GRIB_stepType", "") in ("accum", "avgua", "accumul")
            cvals = crop[name].values if name in crop.data_vars else np.array([])
            finite = cvals[np.isfinite(cvals)] if cvals.size else cvals
            variables[name] = {
                "long_name": long_name, "units": units,
                "grib_stepType": da.attrs.get("GRIB_stepType", ""),
                "is_accumulation": bool(accumulation),
                "region_min": float(np.min(finite)) if finite.size else None,
                "region_max": float(np.max(finite)) if finite.size else None,
                "region_mean": float(np.mean(finite)) if finite.size else None,
                "region_cells": int(crop[name].isel({d: 0 for d in crop[name].dims
                                                     if d not in ("latitude", "longitude")}).size)
                                 if name in crop.data_vars else 0,
            }

    rec["grid"] = grid
    rec["sanity_region"] = ("whole file (AOI subset)" if region_bbox is None else region_bbox)
    rec["steps_h"] = sorted(steps)
    rec["expver"] = sorted(expvers) if expvers else ["(none — forecast or single-provenance netCDF)"]
    rec["variables"] = variables

    # --- flags on structure ---
    if grid and (grid["dlat"] not in (0.25, None) or grid["dlon"] not in (0.25, None)):
        rec["flags"].append(f"GRID_NOT_0P25 (dlat={grid['dlat']}, dlon={grid['dlon']})")
    if grid and grid["region_cells" if False else "nlat"] == 0:
        rec["flags"].append("EMPTY_GRID")
    for name, v in variables.items():
        if v["region_cells"] == 0:
            rec["flags"].append(f"{name}:NO_CELLS_IN_BBOX")
    return rec


def discover_files():
    """Yield (path, expected_sha, kind) from manifests, else raw GRIB files on disk."""
    seen = set()
    for kind, manifest in _MANIFESTS.items():
        idx = _manifest_index(manifest)
        for abspath, r in idx.items():
            p = Path(abspath)
            seen.add(p.resolve())
            yield p, r.get("sha256"), kind
    # fallback: any grib/nc on disk not in a manifest (skip cfgrib .idx sidecars)
    for pat in ("*.grib*", "*.nc"):
        for p in sorted(_RAW.rglob(pat)):
            if p.suffix == ".idx" or p.name.endswith(".idx"):
                continue
            if p.resolve() not in seen:
                yield p, None, "unmanifested"


def write_reports(records: list[dict]):
    _OUT.mkdir(parents=True, exist_ok=True)
    (_OUT / "qa_summary.json").write_text(
        json.dumps({"bbox": LAKE_ERIE_BBOX, "files": records}, indent=2), encoding="utf-8")

    lines = ["# Weather layer — QA report",
             "",
             "Region sanity stats are a **labeled diagnostic at native 0.25° resolution** over "
             "each file's AOI (whole file for AOI-subset pulls like ERA5; a Lake Erie crop for the "
             "global forecast files) — not a model input and not a spatial aggregation of the "
             "stored grids (they stay native).",
             ""]
    for r in records:
        lines.append(f"## `{r['path']}`")
        if r.get("flags"):
            lines.append(f"- **FLAGS:** {', '.join(r['flags'])}")
        else:
            lines.append("- flags: none")
        lines.append(f"- integrity: {r['checks'].get('integrity', 'n/a')} "
                     f"({r.get('bytes', 0):,} bytes)")
        g = r.get("grid")
        if g:
            lines.append(f"- grid: {g['nlat']}×{g['nlon']} @ dlat={g['dlat']} dlon={g['dlon']}° "
                         f"({g['lon_convention']}); lat {g['lat_min']}..{g['lat_max']}, "
                         f"lon {g['lon_min']}..{g['lon_max']}")
        lines.append(f"- sanity region: {r.get('sanity_region')}")
        lines.append(f"- steps (h): {r.get('steps_h')}")
        lines.append(f"- expver: {', '.join(r.get('expver', []))}")
        lines.append("")
        lines.append("| variable | long name | units | stepType | accum? | region min | max | mean | cells |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for name, v in r.get("variables", {}).items():
            def _f(x): return "—" if x is None else (f"{x:.3g}" if isinstance(x, float) else x)
            lines.append(f"| `{name}` | {v['long_name']} | {v['units']} | {v['grib_stepType']} | "
                         f"{'yes' if v['is_accumulation'] else 'no'} | {_f(v['region_min'])} | "
                         f"{_f(v['region_max'])} | {_f(v['region_mean'])} | {v['region_cells']} |")
        lines.append("")
    (_OUT / "qa_report.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", type=Path, default=None, help="QA a single GRIB/NetCDF file")
    p.add_argument("--bbox", nargs=4, type=float, default=None, metavar=("N", "W", "S", "E"),
                   help="Override the sanity-crop region (default: whole file for AOI subsets, "
                        "Lake Erie for global forecast files)")
    args = p.parse_args(argv)

    cli_bbox = (dict(north=args.bbox[0], west=args.bbox[1], south=args.bbox[2], east=args.bbox[3])
                if args.bbox else None)
    records = []
    if args.file:
        records.append(qa_grib(args.file, None, cli_bbox))
    else:
        for path, sha, _kind in discover_files():
            records.append(qa_grib(path, sha, cli_bbox))

    if not records:
        print("No GRIB files found under data/raw/. Pull one first "
              "(access/ecmwf_forecast.py or access/era5_cds.py).")
        return 0

    write_reports(records)
    n_flag = sum(1 for r in records if r.get("flags"))
    print(f"QA'd {len(records)} file(s); {n_flag} with flags. "
          f"Reports → weather/outputs/qa_report.md + qa_summary.json")
    for r in records:
        print(f"  {r['path']}: {r['checks'].get('integrity','?')}; "
              f"flags={r.get('flags') or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
