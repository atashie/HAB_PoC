#!/usr/bin/env python
"""One-command orchestrator for the forecast feature ensemble — REPEAT A RUN WITH NO NEW CODE.

Chains the pipeline stages so a new forecast = one command:

    python run_forecast_features.py                        # latest 00/12z ENS run, full pipeline
    python run_forecast_features.py --ens-date 20260705 --ens-time 12   # a specific run (reproducible)
    python run_forecast_features.py --refresh-era5         # also advance the ERA5 history frontier first
    python run_forecast_features.py --skip-pull            # re-aggregate/rebuild from already-pulled dirs

Stages (see docs/plans/2026-07-05-forecast-ensemble-features-design.md):
  1. (optional) refresh ERA5T + re-aggregate → advances the history frontier (shrinks the gap).
  2. pull_ens.py            → ENS (50 members) + oper gap-fill run, cropped to FL; writes run_manifest.json.
  3. aggregate_forecast.py  → each run's GRIBs → daily base fields on the ERA5 grid (+ quality flags).
  4-6. build_feature_ensemble.py → stitch history+forecast per member, apply the FROZEN climatology,
       store the 22-feature ensemble + effective_member_days + provenance.

Everything is scripted, cached, and manifested — re-running is idempotent (completed steps are skipped).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent           # weather/forecast
_WEATHER = _HERE.parent                            # weather
_DATA_SOURCES = _WEATHER.parent                    # data-sources
_ENS_ROOT = _WEATHER / "data" / "raw" / "forecast_ens"


def _run(script: Path, *args, cwd: Path = _HERE):
    cmd = [sys.executable, "-u", str(script), *[str(a) for a in args]]
    print(f"\n$ {script.name} {' '.join(str(a) for a in args)}", flush=True)
    subprocess.run(cmd, check=True, cwd=str(cwd))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ens-date", default=None, help="ENS run date YYYYMMDD (default: latest 00/12z)")
    p.add_argument("--ens-time", type=int, default=12, choices=[0, 12])
    p.add_argument("--refresh-era5", action="store_true",
                   help="pull the current year's ERA5 + re-aggregate before building (advances the frontier)")
    p.add_argument("--skip-pull", action="store_true",
                   help="skip stages 1-2; re-aggregate + rebuild from the most recent pulled run dir")
    args = p.parse_args(argv)

    # Stage 1 — optional ERA5 history refresh.
    if args.refresh_era5 and not args.skip_pull:
        _run(_WEATHER / "access" / "pull_hourly_async.py", "--years", "2026", cwd=_WEATHER / "access")
        _run(_WEATHER / "derive" / "aggregate_daily.py", cwd=_WEATHER / "derive")

    # Stage 2 — pull ENS + gap-fill.
    if not args.skip_pull:
        extra = ["--ens-date", args.ens_date, "--ens-time", str(args.ens_time)] if args.ens_date else []
        _run(_HERE / "pull_ens.py", *extra)

    # Locate the run to process (newest run_manifest.json).
    manifests = sorted(_ENS_ROOT.glob("*/run_manifest.json"), key=lambda x: x.stat().st_mtime)
    if not manifests:
        raise SystemExit("No run_manifest.json found — run without --skip-pull first.")
    rm = json.loads(manifests[-1].read_text())
    ens_dir = _DATA_SOURCES / rm["ens_dir"]
    gap_dir = _DATA_SOURCES / rm["gap_dir"] if rm.get("gap_dir") else None
    print(f"\nProcessing run {rm['ens_run']}  (ens_dir={rm['ens_dir']}, gap_dir={rm.get('gap_dir')})")

    # Stage 3 — forecast → daily base fields.
    ens_daily = ens_dir / "daily_forecast.nc"
    _run(_HERE / "aggregate_forecast.py", "--run-dir", ens_dir,
         "--source-class", "member_forecast", "--out", ens_daily)
    gap_daily = None
    if gap_dir and gap_dir.exists():
        gap_daily = gap_dir / "daily_forecast.nc"
        _run(_HERE / "aggregate_forecast.py", "--run-dir", gap_dir,
             "--source-class", "gapfill_forecast", "--out", gap_daily)

    # Stages 4-6 — stitch + apply frozen climatology + store ensemble.
    build_args = ["--ens-daily", ens_daily]
    if gap_daily:
        build_args += ["--gap-daily", gap_daily]
    _run(_HERE / "build_feature_ensemble.py", *build_args)

    print("\n[DONE] forecast feature ensemble built — see weather/data/derived/forecast_feature_ensemble_*.nc")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
