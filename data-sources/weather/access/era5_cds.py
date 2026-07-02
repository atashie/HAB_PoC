#!/usr/bin/env python
"""Acquire **ERA5 hourly single-level** reanalysis (the historical weather truth) via the CDS API.

The historical half of the weather layer. Pulls bounded ERA5 subsets (region × variables ×
time) from the Copernicus Climate Data Store and records each in a JSONL manifest with
sha256 + byte size. Subset, never mirror — global ERA5 is petabyte-scale (../METADATA.md §6).

Design (see ../METADATA.md §7, §11):
  * Dataset id: `reanalysis-era5-single-levels`, product_type `reanalysis`, grid 0.25°,
    regular lat/lon — the SAME mesh as the ECMWF open-data forecasts, so history and forecast
    align cell-for-cell (that is why we chose single-levels over ERA5-Land 0.1°).
  * Default format is **GRIB** so the `expver` header survives: expver=1 = final ERA5,
    expver=5 = **ERA5T** (preliminary, last ~5 days→~3 months, revisable). Requesting a recent
    window can return a MIX of expver 1 and 5. NetCDF from CDS *cannot* distinguish them unless
    the request straddles both. Log expver at QA; treat the ERA5T tail as provisional.
  * `total_precipitation`, `runoff`, `evaporation` are **accumulations** (hourly, de-accumulated
    to the hour ending at the valid time). Reconcile carefully with forecast `tp`, which is
    accumulated from forecast start (../METADATA.md §5).

⚠ Auth + one-time manual step (unlike the no-auth forecast path):
  1. Free CDS account → copy your API key from https://cds.climate.copernicus.eu/how-to-api
  2. Put it in `~/.cdsapirc` OR set CDSAPI_URL / CDSAPI_KEY in data-sources/.env (gitignored).
  3. **Accept the dataset licence ONCE, manually**, on the dataset page, or retrieve() 403s.
  --dry-run builds and prints the request and needs NONE of the above.

⚠ The CDS **queues and throttles** requests; large/heavy requests are penalised. Keep each
request bounded (small area, a few variables, a year or two) and loop, rather than one huge pull.

Examples
--------
# Plan only (no account, no download): show the exact CDS request for a sample month.
python era5_cds.py --years 2022 --months 8 --dry-run

# Live pull (needs .cdsapirc + accepted licence): Aug 2022, western Lake Erie, core drivers.
python era5_cds.py --years 2022 --months 8
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

from _common import net                          # noqa: E402

_WEATHER_DIR = _DATA_SOURCES / "weather"
_DEFAULT_RAW = _WEATHER_DIR / "data" / "raw" / "era5"
_MANIFEST = _WEATHER_DIR / "data" / "raw" / "era5_manifest.jsonl"
_DEFAULT_DAILY_RAW = _WEATHER_DIR / "data" / "raw" / "era5_daily"
_DAILY_MANIFEST = _WEATHER_DIR / "data" / "raw" / "era5_daily_manifest.jsonl"
_DOTENV = _DATA_SOURCES / ".env"

DATASET = "reanalysis-era5-single-levels"

# CDS long-name variables ↔ the forecast short-names they reconcile with (see METADATA §5).
#   era5 long name                       ~ forecast short name
CORE_VARIABLES = [
    "2m_temperature",                    # ~ 2t   (instantaneous)
    "total_precipitation",               # ~ tp   (ACCUMULATION — de-accumulate to compare)
    "10m_u_component_of_wind",           # ~ 10u  (instantaneous)
    "10m_v_component_of_wind",           # ~ 10v  (instantaneous)
    "mean_sea_level_pressure",           # ~ msl  (instantaneous)
    "surface_solar_radiation_downwards", # ~ ssrd (ACCUMULATION)
    "2m_dewpoint_temperature",           # ~ 2d   (instantaneous)
]

# Western Lake Erie basin (Maumee) bbox — matches the CyAN 7_2 / WQP HUC 04100009 scope.
# CDS 'area' order is [North, West, South, East].
LAKE_ERIE_AREA = [42.5, -84.5, 41.0, -82.0]
FLORIDA_AREA = [31.0, -87.7, 24.4, -79.9]   # [N, W, S, E] — whole state incl. panhandle + keys

ALL_HOURS = [f"{h:02d}:00" for h in range(24)]
ALL_DAYS = [f"{d:02d}" for d in range(1, 32)]
ALL_MONTHS = [f"{m:02d}" for m in range(1, 13)]

# --- Daily statistics (derived dataset) --------------------------------------- #
# Native daily aggregates, far smaller than pulling all hours. NetCDF output
# (single .nc per request, or a .zip of .nc for multi-variable). NOTE: the server
# computes on demand and is SLOW (minutes/year) — loop per year, prefer background.
DAILY_DATASET = "derived-era5-single-levels-daily-statistics"
# Accumulated fields must use daily_sum (the only valid daily stat for them);
# instantaneous fields use daily_mean. (Per CDS daily-stats docs.)
ACCUMULATED_VARS = {
    "total_precipitation", "surface_solar_radiation_downwards",
    "surface_net_solar_radiation", "surface_thermal_radiation_downwards",
    "surface_net_thermal_radiation", "runoff", "surface_runoff",
    "sub_surface_runoff", "evaporation", "potential_evaporation", "snowfall",
    "snowmelt",
}


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def build_request(variables, years, months, days, hours, area, grid, data_format):
    """Assemble the cdsapi request dict (pure — safe to unit-test / dry-run)."""
    return {
        "product_type": ["reanalysis"],
        "variable": list(variables),
        "year": [str(y) for y in years],
        "month": [f"{int(m):02d}" for m in months],
        "day": list(days),
        "time": list(hours),
        "area": list(area),                 # [N, W, S, E]
        "grid": [grid, grid],               # 0.25 x 0.25
        "data_format": data_format,         # 'grib' (default; keeps expver) or 'netcdf'
        "download_format": "unarchived",
    }


def _target_name(req, outdir: Path) -> Path:
    ys, ye = req["year"][0], req["year"][-1]
    ms, me = req["month"][0], req["month"][-1]
    ext = "grib" if req["data_format"] == "grib" else "nc"
    return outdir / f"era5_sl_{ys}{ms}-{ye}{me}.{ext}"


def load_credentials():
    """Surface CDS creds from data-sources/.env into the env so cdsapi picks them up."""
    net.load_dotenv(_DOTENV)  # sets CDSAPI_URL / CDSAPI_KEY if present and unset


def pull(req, outdir: Path, manifest: Path):
    import cdsapi  # imported here so --dry-run needs no package/creds

    load_credentials()
    outdir.mkdir(parents=True, exist_ok=True)
    target = _target_name(req, outdir)
    client = cdsapi.Client()  # reads ~/.cdsapirc or CDSAPI_URL/CDSAPI_KEY
    client.retrieve(DATASET, req, str(target))

    sha = _sha256(target)
    record = {
        "kind": "era5_single_levels",
        "dataset": DATASET,
        "variables": req["variable"],
        "years": req["year"], "months": req["month"],
        "area": req["area"], "grid": req["grid"],
        "data_format": req["data_format"],
        "path": str(target.relative_to(_DATA_SOURCES)),
        "bytes": target.stat().st_size, "sha256": sha,
        "accessed_utc": net._utc_now_iso(),
        "license": "CC-BY-4.0 (Copernicus / ERA5)",
        "note": "expver 1=final ERA5, 5=ERA5T (preliminary). Verify at QA.",
    }
    net.append_manifest(manifest, record)
    return record


# --------------------------------------------------------------------------- #
# Daily statistics path (derived-era5-single-levels-daily-statistics)
# --------------------------------------------------------------------------- #
def split_by_statistic(variables):
    """Group variables by the daily statistic they require (pure)."""
    mean_vars = [v for v in variables if v not in ACCUMULATED_VARS]
    sum_vars = [v for v in variables if v in ACCUMULATED_VARS]
    groups = {}
    if mean_vars:
        groups["daily_mean"] = mean_vars
    if sum_vars:
        groups["daily_sum"] = sum_vars   # only valid stat for accumulated fields
    return groups


def build_daily_request(variables, year, daily_statistic, area,
                        months=ALL_MONTHS, days=ALL_DAYS,
                        frequency="1_hourly", time_zone="utc+00:00"):
    """Assemble a daily-statistics request dict (pure — safe to unit-test / dry-run)."""
    return {
        "product_type": "reanalysis",
        "variable": list(variables),
        "year": str(year),
        "month": list(months),
        "day": list(days),
        "daily_statistic": daily_statistic,
        "time_zone": time_zone,
        "frequency": frequency,
        "area": list(area),          # [N, W, S, E]
        "data_format": "netcdf",     # this dataset is NetCDF-only
    }


def _finalize_daily_download(raw_path: Path, stat: str, year, outdir: Path):
    """Return the resulting .nc path(s). Single .nc → renamed; .zip → extracted."""
    import zipfile
    with open(raw_path, "rb") as f:
        magic = f.read(4)
    results = []
    if magic[:2] == b"PK":                                   # zip of per-variable .nc
        subdir = outdir / f"era5_daily_{stat}_{year}"
        subdir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(raw_path) as z:
            for member in z.namelist():
                if member.endswith(".nc"):
                    z.extract(member, subdir)
                    results.append(subdir / member)
        raw_path.unlink(missing_ok=True)
    else:                                                    # bare NetCDF (HDF5 magic)
        dest = outdir / f"era5_daily_{stat}_{year}.nc"
        raw_path.replace(dest)
        results.append(dest)
    return results


def pull_daily(variables, years, area, outdir: Path, manifest: Path,
               months=ALL_MONTHS, days=ALL_DAYS,
               frequency="1_hourly", time_zone="utc+00:00", client=None):
    """Pull ERA5 daily statistics per (year, statistic-group). Cached + manifested.

    Accumulated vars → daily_sum; instantaneous → daily_mean (separate requests).
    One CDS request per (year, group); the server aggregates on demand (slow).
    """
    import cdsapi
    load_credentials()
    outdir.mkdir(parents=True, exist_ok=True)
    client = client or cdsapi.Client()
    groups = split_by_statistic(variables)
    records = []
    for year in years:
        for stat, vs in groups.items():
            req = build_daily_request(vs, year, stat, area, months, days, frequency, time_zone)
            raw = outdir / f"era5_daily_{stat}_{year}.download"
            client.retrieve(DAILY_DATASET, req, str(raw))
            for ncpath in _finalize_daily_download(raw, stat, year, outdir):
                rec = {
                    "kind": "era5_daily_statistics",
                    "dataset": DAILY_DATASET,
                    "daily_statistic": stat,
                    "variables": vs,
                    "year": str(year),
                    "area": list(area),
                    "frequency": frequency, "time_zone": time_zone,
                    "path": str(ncpath.relative_to(_DATA_SOURCES)),
                    "bytes": ncpath.stat().st_size, "sha256": _sha256(ncpath),
                    "accessed_utc": net._utc_now_iso(),
                    "license": "CC-BY-4.0 (Copernicus / ERA5)",
                }
                net.append_manifest(manifest, rec)
                records.append(rec)
                print(f"  {stat} {year}: {ncpath.name} ({ncpath.stat().st_size:,} B)")
    return records


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--variables", nargs="+", default=CORE_VARIABLES,
                   help="CDS long-name variables (default: core HAB drivers)")
    p.add_argument("--years", nargs="+", type=int, required=True, help="e.g. 2021 2022")
    p.add_argument("--months", nargs="+", type=int, default=list(range(1, 13)),
                   help="1..12 (default: all)")
    p.add_argument("--days", nargs="+", default=ALL_DAYS, help="(default: all valid days)")
    p.add_argument("--hours", nargs="+", default=ALL_HOURS,
                   help="HH:00 (default: all 24). Reduce to lighten the request.")
    p.add_argument("--area", nargs=4, type=float, default=LAKE_ERIE_AREA,
                   metavar=("N", "W", "S", "E"), help="Bounding box (default: W. Lake Erie)")
    p.add_argument("--grid", type=float, default=0.25, help="Grid spacing deg (default 0.25)")
    p.add_argument("--format", dest="data_format", default="grib",
                   choices=["grib", "netcdf"], help="default grib (keeps expver header)")
    p.add_argument("--daily", action="store_true",
                   help="Use the derived DAILY-statistics dataset (NetCDF; sum for accumulated "
                        "vars, mean for instantaneous). Ignores --hours/--grid/--format.")
    p.add_argument("--frequency", default="1_hourly",
                   choices=["1_hourly", "3_hourly", "6_hourly"],
                   help="(daily) sub-daily sampling used to compute the stat (default 1_hourly)")
    p.add_argument("--time-zone", dest="time_zone", default="utc+00:00",
                   help="(daily) time zone for day boundaries (default utc+00:00)")
    p.add_argument("--outdir", type=Path, default=None)
    p.add_argument("--manifest", type=Path, default=None)
    p.add_argument("--dry-run", action="store_true",
                   help="Build + print the request; no account, no download.")
    args = p.parse_args(argv)

    # ---- Daily-statistics path -------------------------------------------- #
    if args.daily:
        outdir = args.outdir or _DEFAULT_DAILY_RAW
        manifest = args.manifest or _DAILY_MANIFEST
        months = [f"{int(m):02d}" for m in args.months]
        groups = split_by_statistic(args.variables)
        if args.dry_run:
            print("DRY-RUN (daily) — would retrieve per (year, statistic):")
            print(f"  dataset: {DAILY_DATASET}")
            for stat, vs in groups.items():
                print(f"  {stat}: {vs}")
            print(f"  years: {args.years}  months: {months}  area[N,W,S,E]: {args.area}")
            print(f"  frequency: {args.frequency}  time_zone: {args.time_zone}")
            print(f"  → {len(args.years) * len(groups)} requests (NetCDF; server aggregates on demand).")
            print("  Reminder: accept the DAILY-stats dataset licence ONCE on its CDS page first.")
            return 0
        recs = pull_daily(args.variables, args.years, args.area, outdir, manifest,
                          months=months, days=args.days,
                          frequency=args.frequency, time_zone=args.time_zone)
        total = sum(r["bytes"] for r in recs)
        print(f"Pulled {len(recs)} daily file(s), {total:,} bytes total "
              f"→ {outdir.relative_to(_DATA_SOURCES)}")
        return 0

    # ---- Hourly path (default) -------------------------------------------- #
    args.outdir = args.outdir or _DEFAULT_RAW
    args.manifest = args.manifest or _MANIFEST

    req = build_request(args.variables, args.years, args.months, args.days,
                        args.hours, args.area, args.grid, args.data_format)
    if args.dry_run:
        import json
        n = (len(req["variable"]) * len(req["year"]) * len(req["month"])
             * len(req["day"]) * len(req["time"]))
        print("DRY-RUN — CDS request (no auth needed to build this):")
        print(f"  dataset: {DATASET}")
        print(json.dumps(req, indent=2))
        print(f"  → up to {n:,} field-hours requested (area-cropped). "
              f"Keep bounded; the CDS queues heavy requests.")
        print("  Reminder: accept the dataset licence ONCE on the CDS dataset page first.")
        return 0

    rec = pull(req, args.outdir, args.manifest)
    print(f"Pulled ERA5 {rec['years']} m{rec['months']} → {rec['path']} "
          f"({rec['bytes']:,} bytes, sha256 {rec['sha256'][:12]}…)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
