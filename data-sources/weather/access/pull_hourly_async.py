#!/usr/bin/env python
"""Acquire multi-year HOURLY ERA5 for an AOI by submitting all year-jobs at once.

Why async: the CDS runs each request server-side (queue + on-demand extraction) and **caches
the result even if the client disconnects** (verified 2026-07-02). Sequential per-year
`retrieve()` waits ~15-30 min/job → hours for 11 years. Submitting all years up front lets the
CDS process them in parallel; we then download each as it becomes ready (~7 s / 77 MB year).

Cached + manifested + resumable: a year whose GRIB already exists is sha256-manifested (if not
already) and skipped. Safe to re-run.

Default: Florida, 5 HAB-driver vars, 2016→present (the CyAN OLCI POR), GRIB.
Feeds derive/aggregate_daily.py.

Usage
-----
python pull_hourly_async.py                      # Florida 2016->present, 5 vars
python pull_hourly_async.py --years 2016 2017    # subset
"""
from __future__ import annotations

import argparse
import sys
import time
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
from weather.access import era5_cds as e         # noqa: E402

DRIVER_VARS = ["2m_temperature", "total_precipitation",
               "10m_u_component_of_wind", "10m_v_component_of_wind",
               "surface_solar_radiation_downwards"]
_OUTDIR = e._DEFAULT_RAW                          # weather/data/raw/era5
_MANIFEST = e._MANIFEST                           # weather/data/raw/era5_manifest.jsonl

# ERA5T lag ~5 days → last complete month for the current year. Pass --last-month to override.
CURRENT_YEAR = 2026
CURRENT_LAST_MONTH = 6                            # through June 2026 (today = 2026-07-02)


def _months_for(year, last_month):
    n = last_month if year == CURRENT_YEAR else 12
    return [f"{m:02d}" for m in range(1, n + 1)]


def _manifested_paths(manifest: Path):
    return {r.get("path") for r in net.read_manifest(manifest)}


def _manifest_existing(target: Path, req_meta: dict, manifest: Path, known: set):
    rel = str(target.relative_to(_DATA_SOURCES))
    if rel in known:
        return
    rec = {"kind": "era5_single_levels_hourly", "dataset": e.DATASET,
           "path": rel, "bytes": target.stat().st_size, "sha256": e._sha256(target),
           "accessed_utc": net._utc_now_iso(), "license": "CC-BY-4.0 (Copernicus / ERA5)",
           **req_meta}
    net.append_manifest(manifest, rec)
    known.add(rel)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--years", nargs="+", type=int, default=list(range(2016, CURRENT_YEAR + 1)))
    p.add_argument("--variables", nargs="+", default=DRIVER_VARS)
    p.add_argument("--area", nargs=4, type=float, default=e.FLORIDA_AREA,
                   metavar=("N", "W", "S", "E"))
    p.add_argument("--grid", type=float, default=0.25)
    p.add_argument("--last-month", type=int, default=CURRENT_LAST_MONTH,
                   help=f"last complete month for {CURRENT_YEAR} (default {CURRENT_LAST_MONTH})")
    p.add_argument("--poll", type=int, default=30, help="seconds between readiness polls")
    p.add_argument("--max-active", type=int, default=4,
                   help="max concurrent CDS jobs (the server caps ~5 per user; default 4)")
    p.add_argument("--max-attempts", type=int, default=4,
                   help="resubmit a rejected/failed year up to this many times (default 4)")
    args = p.parse_args(argv)

    e.load_credentials()
    import cdsapi
    inner = cdsapi.Client().client
    _OUTDIR.mkdir(parents=True, exist_ok=True)
    known = _manifested_paths(_MANIFEST)

    def target_for(year):
        ms = _months_for(year, args.last_month)
        return _OUTDIR / f"era5_sl_{year}{ms[0]}-{year}{ms[-1]}.grib"

    def build_req(year):
        ms = _months_for(year, args.last_month)
        return e.build_request(args.variables, [year], [int(m) for m in ms],
                               e.ALL_DAYS, e.ALL_HOURS, args.area, args.grid, "grib")

    def status(remote):
        try:
            return remote.status
        except Exception:
            return "unknown"

    # Work list: skip (and manifest) already-downloaded years.
    pending, attempts = [], {}
    for year in args.years:
        tgt = target_for(year)
        if tgt.is_file() and tgt.stat().st_size > 0:
            _manifest_existing(tgt, {"year": str(year)}, _MANIFEST, known)
            print(f"[{year}] cached {tgt.name} — skip")
        else:
            pending.append(year)
            attempts[year] = 0

    # Sliding window: keep <= max_active jobs in flight (server caps ~5/user).
    active = {}                          # year -> Remote
    while pending or active:
        while pending and len(active) < args.max_active:
            year = pending.pop(0)
            attempts[year] += 1
            r = inner.submit(e.DATASET, build_req(year))
            st = status(r)
            if st in ("rejected", "failed"):
                print(f"[{year}] submit {st} (attempt {attempts[year]}) — requeue, let pool drain")
                if attempts[year] < args.max_attempts:
                    pending.append(year)
                break                    # stop filling; drain active first
            active[year] = r
            print(f"[{year}] submitted ({st})")
            time.sleep(3)
        for year, r in list(active.items()):
            st = status(r)
            if st == "successful":
                tgt = target_for(year)
                r.download(str(tgt))
                _manifest_existing(tgt, {"year": str(year)}, _MANIFEST, known)
                print(f"[{year}] downloaded {tgt.name} ({tgt.stat().st_size:,} B)")
                active.pop(year)
            elif st in ("rejected", "failed"):
                active.pop(year)
                if attempts[year] < args.max_attempts:
                    pending.append(year)
                print(f"[{year}] job {st} — requeue")
        if pending or active:
            print(f"  active={sorted(active)} pending={sorted(pending)} "
                  f"({time.strftime('%H:%M:%SZ', time.gmtime())})")
            time.sleep(args.poll)

    print(f"DONE — years present in {_OUTDIR.relative_to(_DATA_SOURCES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
