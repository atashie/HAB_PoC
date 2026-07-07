#!/usr/bin/env python
"""Pull the ECMWF open-data ENS forecast (+ an oper gap-fill run) for the HAB feature ensemble.

Stage 2 of the forecast-ensemble pipeline (docs/plans/2026-07-05-forecast-ensemble-features-design.md).

What it does
------------
* Pulls the latest (or a named) **ENS** run — `stream=enfo, type=pf`, the **50 perturbed members**
  (open-data has NO `cf` control → 50 members, not 51; documented deviation from the design).
* Pulls a deterministic **oper (HRES)** gap-fill run to bridge the ERA5→forecast gap (1 member, cheap).
* Fields: `2t, 10u, 10v, tp, ssrd` at 3-hourly to +144 h then 6-hourly to +360 h (15 d), plus
  `mx2t3, mn2t3` (3-hourly max/min temp) to +144 h for proper daily Tmax/Tmin days 1–6.

Why per-param + crop-and-delete
-------------------------------
Open data serves **global** fields (no server-side subsetting) and one ENS field = ~33.5 MB
(50 members). The faithful pull is ~17 GB of transfer. To keep disk small we pull ONE param at a
time (all its steps, all members) → crop to a Florida buffer → save a small NetCDF → **delete the
global GRIB**. Peak disk ≈ one param file (~2.9 GB); final per-run data is a few MB. Resumable:
an existing `<param>_fl.nc` is skipped.

Grid note (verified 2026-07-05): the open-data global 0.25° grid is whole-degree-aligned; our ERA5
daily grid is **offset by ≤0.2°** (CDS `area` registration). We crop here with a buffer and defer the
**nearest-neighbour reindex onto the ERA5 master grid** to aggregate_forecast.py — so the raw pull is
never hand-edited and the regrid is an explicit, traceable derive step.

Usage
-----
python pull_ens.py --dry-run                       # plan only
python pull_ens.py                                 # latest ENS + auto gap-fill oper run
python pull_ens.py --params 2t --max-step 6        # cheap single-param validation
python pull_ens.py --ens-date 20260705 --ens-time 12
"""
from __future__ import annotations

import argparse
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

_WEATHER = _DATA_SOURCES / "weather"
_RAW = _WEATHER / "data" / "raw"
_ENS_DIR = _RAW / "forecast_ens"
_GAP_DIR = _RAW / "forecast_gapfill"
_MANIFEST = _RAW / "forecast_ens_manifest.jsonl"

# Florida bbox (matches the ERA5 pull) + a buffer so every ERA5 cell has a forecast neighbour
# within a quarter-cell for the nearest-neighbour reindex done downstream.
FLORIDA_AREA = (31.0, -87.7, 24.4, -79.9)         # N, W, S, E
CROP_BUFFER_DEG = 0.5

# Faithful step ladder: 3-hourly to +144 h, then 6-hourly to +360 h.
BASE_STEPS = list(range(0, 145, 3)) + list(range(150, 361, 6))      # 85 steps
EXTREME_STEPS = list(range(3, 145, 3))                              # 48 steps (max/min over last 3 h)

BASE_PARAMS = ["2t", "10u", "10v", "tp", "ssrd"]  # instantaneous + accumulations
EXTREME_PARAMS = ["mx2t3", "mn2t3"]               # 3-hourly max/min temp (to +144 h only)

ATTRIBUTION = "Contains ECMWF open data (IFS/ENS forecasts), CC-BY-4.0. Attribute ECMWF."


def _fl_slices(lat, lon, area=FLORIDA_AREA, buffer=CROP_BUFFER_DEG):
    import numpy as np
    N, W, S, E = area
    lat_i = np.where((lat <= N + buffer) & (lat >= S - buffer))[0]
    lon_i = np.where((lon >= W - buffer) & (lon <= E + buffer))[0]
    return (slice(int(lat_i[0]), int(lat_i[-1]) + 1),
            slice(int(lon_i[0]), int(lon_i[-1]) + 1))


def stream_crop_grib(grib_path, area=FLORIDA_AREA, buffer=CROP_BUFFER_DEG):
    """FL crop: single open, stream ONE step at a time.

    ⚠️ KNOWN-BROKEN (2026-07-07) — DO NOT trust for large multi-step globals. See the post-mortem in
    docs/plans/2026-07-05-forecast-ensemble-features-design.md. A *single* per-step
    `ds.isel(step=i, lat, lon).load()` is cheap (~0.22 GB, cfgrib pushes the step index down), but
    **looping over all steps while this one open dataset stays alive LEAKS ~one global step-slab
    (~207 MB) per call** — the per-message eccodes handles are never freed. RSS climbs ~0.21 GB/step,
    reaching the full ~17.6 GB cube by ~step 84 and thrashing to ~53 GB (near-OOM on 64 GB). The
    earlier "~200 MB peak" claim was FALSE across the loop. A viable crop must release the dataset /
    eccodes handles per step (or per small batch), or read messages directly via eccodes/pygrib with
    explicit codes_release. Not fixed here — the forecast pull is paused pending a workflow redesign.

    (Separately: a corrupt GRIB message crashes eccodes natively — a *download* problem; the resume
    reuse-check validates step/member count only, not integrity, so a corrupt global can be reused.)
    """
    import numpy as np
    import xarray as xr
    with _decode(grib_path) as ds:
        lasl, losl = _fl_slices(ds["latitude"].values, ds["longitude"].values, area, buffer)
        if "step" in ds.dims and ds.sizes["step"] > 1:
            parts = [ds.isel(step=i, latitude=lasl, longitude=losl).load()
                     for i in range(ds.sizes["step"])]
            return xr.concat(parts, dim="step")
        return ds.isel(latitude=lasl, longitude=losl).load()


def _decode(grib_path: Path):
    import xarray as xr
    return xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs={"indexpath": ""})


def pull_param(client, run, stream, ftype, param, steps, outdir: Path,
               manifest: Path, keep_global=False):
    """Download one param (all steps, all members) globally → crop FL → save NetCDF → delete global.

    Returns a manifest record dict (also appended to `manifest`). Skips if the FL NetCDF exists.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    fl_path = outdir / f"{param}_fl.nc"
    if fl_path.exists() and fl_path.stat().st_size > 0:
        print(f"  [{param}] cached → {fl_path.name} (skip)")
        return {"param": param, "path": str(fl_path.relative_to(_DATA_SOURCES)), "cached": True}

    global_grib = outdir / f"_{param}_global.grib2"
    # Reuse an existing COMPLETE global (resumability — avoids re-downloading GBs on a slow link);
    # a global with the expected step (and member) count is trusted, otherwise (re)download.
    reuse = False
    if global_grib.exists() and global_grib.stat().st_size > 0:
        try:
            probe = _decode(global_grib)
            steps_ok = int(probe.sizes.get("step", 1)) == len(steps)
            mem_ok = (ftype != "pf") or int(probe.sizes.get("number", 0)) == 50
            probe.close()
            reuse = steps_ok and mem_ok
        except Exception:
            reuse = False
    if reuse:
        print(f"  [{param}] reusing complete global ({global_grib.stat().st_size/1e6:.0f}MB, no re-download)")
    else:
        global_grib.unlink(missing_ok=True)
        client.retrieve(stream=stream, type=ftype, param=param, step=steps, resol="0p25",
                        date=run.strftime("%Y%m%d"), time=run.hour, target=str(global_grib))
    gbytes = global_grib.stat().st_size

    ds_fl = stream_crop_grib(global_grib)          # batched-open + per-step stream; already loaded
    comp = {v: {"zlib": True, "complevel": 4} for v in ds_fl.data_vars}
    ds_fl.to_netcdf(fl_path, encoding=comp)

    if not keep_global:
        global_grib.unlink(missing_ok=True)
        # cfgrib may drop a sidecar .idx despite indexpath="" on some versions
        for extra in outdir.glob(f"_{param}_global.grib2*"):
            extra.unlink(missing_ok=True)

    nmem = int(ds_fl.sizes.get("number", 1))
    rec = {
        "kind": "ecmwf_forecast_crop", "stream": stream, "type": ftype, "param": param,
        "run_datetime": str(run), "n_members": nmem, "n_steps": len(steps),
        "global_bytes": gbytes, "path": str(fl_path.relative_to(_DATA_SOURCES)),
        "bytes": fl_path.stat().st_size, "sha256": net._sha256(fl_path),
        "fl_grid": [int(ds_fl.sizes["latitude"]), int(ds_fl.sizes["longitude"])],
        "crop_area_buffered": [FLORIDA_AREA, CROP_BUFFER_DEG],
        "accessed_utc": net._utc_now_iso(), "license": "CC-BY-4.0 (ECMWF open data)",
    }
    net.append_manifest(manifest, rec)
    print(f"  [{param}] {nmem}m × {len(steps)}s  global {gbytes/1e6:.0f}MB → "
          f"{fl_path.name} {fl_path.stat().st_size/1e3:.0f}KB "
          f"[{rec['fl_grid'][0]}×{rec['fl_grid'][1]}]" + ("" if not keep_global else " (kept global)"))
    return rec


def _resolve_run(client, stream, ftype, date, time, long_range_hours=(0, 12)):
    """Resolve the concrete run datetime.

    If an explicit date is given, honour it. Otherwise take `latest`, but step back to the most
    recent LONG-RANGE cycle: ENS 00/12z reach +360 h (15 d), while 06/18z ENS runs only reach
    +144 h — requesting steps beyond 144 h on a short run fails the index lookup.
    """
    import datetime as _dt
    if date is not None:
        return _dt.datetime.strptime(f"{date}{int(time):02d}", "%Y%m%d%H")
    run = client.latest(stream=stream, type=ftype, param="2t", step=0)
    if long_range_hours and run.hour not in long_range_hours:
        run = run - _dt.timedelta(hours=run.hour % 12)      # 18→12, 06→00
    return run


def find_oldest_retained_oper(client, max_back_hours=96):
    """Probe backward (6-hourly) for the OLDEST still-retained oper run — the gap-fill source.

    Returns a datetime or None. Uses a cheap 1-member 2t/step0 retrieve as the availability test.
    """
    import datetime as _dt
    latest = client.latest(stream="oper", type="fc", param="2t", step=0)
    oldest = None
    tmp = _GAP_DIR / "_probe.grib2"
    _GAP_DIR.mkdir(parents=True, exist_ok=True)
    for back in range(0, max_back_hours + 1, 6):
        cand = latest - _dt.timedelta(hours=back)
        if cand.hour not in (0, 6, 12, 18):
            continue
        try:
            client.retrieve(stream="oper", type="fc", param="2t", step=0, resol="0p25",
                            date=cand.strftime("%Y%m%d"), time=cand.hour, target=str(tmp))
            oldest = cand                       # keep going back until a miss
        except Exception:
            break
    tmp.unlink(missing_ok=True)
    for extra in _GAP_DIR.glob("_probe.grib2*"):
        extra.unlink(missing_ok=True)
    return oldest


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ens-date", default=None, help="ENS run date YYYYMMDD (default: latest)")
    p.add_argument("--ens-time", type=int, default=12, choices=[0, 12], help="ENS run hour (00/12)")
    p.add_argument("--gap-date", default=None, help="oper gap-fill run date (default: auto oldest retained)")
    p.add_argument("--gap-time", type=int, default=None, choices=[0, 6, 12, 18])
    p.add_argument("--params", nargs="+", default=None,
                   help="subset of params to pull (default: all base+extreme)")
    p.add_argument("--max-step", type=int, default=None,
                   help="cap steps at this many hours (for cheap validation)")
    p.add_argument("--skip-gap", action="store_true", help="pull only the ENS run")
    p.add_argument("--keep-global", action="store_true", help="don't delete the global GRIB after crop")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    base = [q for q in BASE_PARAMS if args.params is None or q in args.params]
    extreme = [q for q in EXTREME_PARAMS if args.params is None or q in args.params]

    def cap(steps):
        return [s for s in steps if args.max_step is None or s <= args.max_step]

    plan_base, plan_extr = cap(BASE_STEPS), cap(EXTREME_STEPS)

    if args.dry_run:
        nfields = len(base) * len(plan_base) + len(extreme) * len(plan_extr)
        print("DRY-RUN — ENS pull plan:")
        print(f"  base params {base} × {len(plan_base)} steps")
        print(f"  extreme params {extreme} × {len(plan_extr)} steps")
        print(f"  ~{nfields} fields × ~33.5 MB ≈ {nfields*33.5/1000:.1f} GB global transfer "
              f"(cropped to FL, global deleted)")
        print(f"  {ATTRIBUTION}")
        return 0

    from ecmwf.opendata import Client
    client = Client(source="ecmwf")

    ens_run = _resolve_run(client, "enfo", "pf", args.ens_date, args.ens_time)
    ens_out = _ENS_DIR / ens_run.strftime("%Y%m%d%H")
    print(f"ENS run {ens_run} → {ens_out.relative_to(_DATA_SOURCES)}")
    for param in base:
        pull_param(client, ens_run, "enfo", "pf", param, plan_base, ens_out, _MANIFEST, args.keep_global)
    for param in extreme:
        pull_param(client, ens_run, "enfo", "pf", param, plan_extr, ens_out, _MANIFEST, args.keep_global)

    gap_run, gap_out = None, None
    if not args.skip_gap:
        if args.gap_date is not None:
            import datetime as _dt
            gap_run = _dt.datetime.strptime(f"{args.gap_date}{int(args.gap_time or 0):02d}", "%Y%m%d%H")
        else:
            gap_run = find_oldest_retained_oper(client)
        if gap_run is None:
            print("!! no retained oper run found for gap-fill — skipping (handle gap by interpolation)")
        else:
            gap_out = _GAP_DIR / gap_run.strftime("%Y%m%d%H")
            print(f"gap-fill oper run {gap_run} → {gap_out.relative_to(_DATA_SOURCES)}")
            for param in base:
                pull_param(client, gap_run, "oper", "fc", param, plan_base, gap_out, _MANIFEST, args.keep_global)
            for param in extreme:
                pull_param(client, gap_run, "oper", "fc", param, plan_extr, gap_out, _MANIFEST, args.keep_global)

    # Run manifest — records exactly which dirs downstream stages should consume (traceability +
    # lets run_forecast_features.py chain stages without re-resolving runs).
    import json
    run_manifest = {
        "ens_run": str(ens_run), "ens_dir": str(ens_out.relative_to(_DATA_SOURCES)),
        "gap_run": str(gap_run) if gap_run else None,
        "gap_dir": str(gap_out.relative_to(_DATA_SOURCES)) if gap_out else None,
        "base_params": base, "extreme_params": extreme,
        "base_steps": plan_base, "extreme_steps": plan_extr,
        "accessed_utc": net._utc_now_iso(),
    }
    (ens_out / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2))
    print(f"\nDone. run_manifest.json written to {ens_out.relative_to(_DATA_SOURCES)}. {ATTRIBUTION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
