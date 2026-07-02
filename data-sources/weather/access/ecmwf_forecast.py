#!/usr/bin/env python
"""Acquire ECMWF **medium-range open-data forecasts** (IFS) for the HAB action-window.

The operational half of the weather layer. Fetches the latest (or a named) IFS
forecast run from ECMWF's free, **no-auth**, CC-BY-4.0 open-data service and records
it in a JSONL manifest with sha256 + byte size, so any forecast-driven figure or tool
readout traces to exact bytes.

Why this exists (see ../METADATA.md §3, §7, §11):
  * Open data is the operational feed that *extends ERA5 history into the future* on the
    SAME 0.25° regular lat/lon grid ERA5 uses — the two align cell-for-cell.
  * ⚠ The open-data portal is a **rolling archive of only the most recent ~12 runs
    (~2–3 days)**. There is NO history here. To build a forecast archive for later
    skill verification we must capture runs as they publish — run this on a schedule.
  * One `retrieve()` writes ALL requested (param × step) fields into ONE concatenated
    GRIB2 file per run (that is how ecmwf-opendata works), so the manifest records one
    file per (run, request), not one per field.

Grid / encoding facts (probe-verified 2026-07-02, see ../reference/PRIMARY-SOURCES.md):
  * `resol="0p25"` → global 721×1440 grid, latitude 90..-90, **longitude -180..179.75**
    (NOT 0..360). Crop to a bbox AFTER download (qaqc/qa_weather.py) — the client serves
    global fields.
  * `tp` (total precipitation) is **accumulated from forecast start** (step 0 = 0). It must
    be de-accumulated to per-interval increments before comparing with ERA5 hourly precip.
  * `2t`,`10u`,`10v`,`msl` are instantaneous.

License: ECMWF real-time open data is CC-BY-4.0. The client prints, on every download,
"By downloading data from the ECMWF open data dataset, you agree to the terms:
Attribution 4.0 International (CC BY 4.0). Please attribute ECMWF when downloading this
data." Carry that attribution wherever the data appears.

Access is auth-free, so --dry-run is only for planning/CI; the live pull needs no key.

Examples
--------
# Plan only (no download): what run/params/steps would we pull?
python ecmwf_forecast.py --dry-run

# Pull the latest oper (IFS control, ex-HRES) run, core drivers, 3-day window:
python ecmwf_forecast.py --params 2t tp 10u 10v msl --steps 0 24 48 72

# Pull a specific run:
python ecmwf_forecast.py --date 20260702 --time 0 --steps 0 6 12 24
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

# --- make `_common` importable when run as a script ------------------------- #
_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

# Windows consoles default to cp1252; keep Unicode in help/prints from crashing.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

from _common import net                          # noqa: E402  (shared manifest helpers)

_WEATHER_DIR = _DATA_SOURCES / "weather"
_DEFAULT_RAW = _WEATHER_DIR / "data" / "raw" / "forecast"
_MANIFEST = _WEATHER_DIR / "data" / "raw" / "forecast_manifest.jsonl"

# CC-BY-4.0 attribution string the ECMWF client itself emits on download.
ATTRIBUTION = ("Contains ECMWF open data (IFS forecasts), CC-BY-4.0. "
               "Attribute ECMWF when redistributing.")

# Conservative default: core near-surface HAB drivers, all standard oper fields.
DEFAULT_PARAMS = ["2t", "tp", "10u", "10v", "msl"]
# A 3-day window valid for every run (00/06/12/18); 06/18 runs only reach step 144.
DEFAULT_STEPS = [0, 24, 48, 72]


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def build_request(params, steps, stream, ftype, resol, date=None, time=None):
    """Assemble the ecmwf-opendata request dict (pure — safe to unit-test / dry-run)."""
    req = {
        "type": ftype,          # fc = forecast (deterministic oper / control)
        "stream": stream,       # oper = IFS medium-range control (ex-HRES)
        "param": list(params),
        "step": list(steps),
        "resol": resol,         # 0p25 = 0.25 degree (the ERA5-matched grid)
    }
    if date is not None:
        req["date"] = date      # e.g. 20260702 or -1 for "yesterday"
    if time is not None:
        req["time"] = time      # run hour: 0, 6, 12, 18
    return req


def plan(req, source):
    n_fields = len(req["param"]) * len(req["step"])
    return {
        "source": source,
        "request": req,
        "n_fields": n_fields,
        "note": "One concatenated GRIB2 file per run; global 0.25 deg served, crop after.",
    }


def pull(req, source, outdir: Path, manifest: Path):
    """Download one run's fields into a single GRIB2 file; sha256 + manifest it."""
    from ecmwf.opendata import Client  # imported here so --dry-run needs no package

    client = Client(source=source)
    # Resolve the concrete run datetime (also validates availability) before downloading.
    run_dt = client.latest(**req) if "date" not in req else None

    outdir.mkdir(parents=True, exist_ok=True)
    # Stable, run-stamped filename. If run_dt is None (explicit date/time) name from request.
    stamp = (run_dt.strftime("%Y%m%d%H%M%S") if run_dt is not None
             else f"{req.get('date')}_{str(req.get('time','')).zfill(2)}")
    target = outdir / f"{stamp}-{req['stream']}-{req['type']}-0p25.grib2"

    result = client.retrieve(target=str(target), **req)
    size = target.stat().st_size
    sha = _sha256(target)
    record = {
        "kind": "ecmwf_open_forecast",
        "run_datetime": str(getattr(result, "datetime", run_dt)),
        "stream": req["stream"], "type": req["type"], "resol": req["resol"],
        "params": req["param"], "steps": req["step"],
        "source": source, "path": str(target.relative_to(_DATA_SOURCES)),
        "bytes": size, "sha256": sha,
        "accessed_utc": net._utc_now_iso(),
        "license": "CC-BY-4.0 (ECMWF open data)",
    }
    net.append_manifest(manifest, record)
    return record


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--params", nargs="+", default=DEFAULT_PARAMS,
                   help=f"ECMWF open-data short names (default: {DEFAULT_PARAMS})")
    p.add_argument("--steps", nargs="+", type=int, default=DEFAULT_STEPS,
                   help=f"Forecast steps in hours (default: {DEFAULT_STEPS})")
    p.add_argument("--stream", default="oper",
                   help="oper=IFS control (ex-HRES); enfo=ENS; waef/scwv=waves (default oper)")
    p.add_argument("--type", dest="ftype", default="fc",
                   help="fc=forecast, cf=control, pf=perturbed (default fc)")
    p.add_argument("--resol", default="0p25", help="0p25 = 0.25 deg (default; ERA5-matched)")
    p.add_argument("--date", default=None, help="Run date YYYYMMDD or -1 (default: latest)")
    p.add_argument("--time", type=int, default=None, choices=[0, 6, 12, 18],
                   help="Run hour UTC (default: resolved with latest)")
    p.add_argument("--source", default="ecmwf",
                   help="ecmwf|aws|azure|gcp (default ecmwf; clouds are replicas)")
    p.add_argument("--outdir", type=Path, default=_DEFAULT_RAW)
    p.add_argument("--manifest", type=Path, default=_MANIFEST)
    p.add_argument("--dry-run", action="store_true", help="Plan only; no download, no package import")
    args = p.parse_args(argv)

    req = build_request(args.params, args.steps, args.stream, args.ftype,
                        args.resol, args.date, args.time)
    if args.dry_run:
        info = plan(req, args.source)
        print("DRY-RUN — would retrieve:")
        for k, v in info.items():
            print(f"  {k}: {v}")
        print(f"  attribution: {ATTRIBUTION}")
        return 0

    rec = pull(req, args.source, args.outdir, args.manifest)
    print(f"Pulled run {rec['run_datetime']} → {rec['path']} "
          f"({rec['bytes']:,} bytes, sha256 {rec['sha256'][:12]}…)")
    print(f"  {len(rec['params'])} params × {len(rec['steps'])} steps; {ATTRIBUTION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
