"""Step 1 - INGEST.  Make sure the only two inputs the lean model needs are present:

  (a) CyAN weekly CONUS mosaics (the satellite signal), OLCI sensor only, and
  (b) the Florida resolvable-lakes layer (the lake universe + the `area_sqkm` feature).

CyAN publishes weekly 7-day CONUS mosaics on NASA's Ocean Biology DAAC. This PoC reads
that cached, checksummed product; the from-source pull itself (OB.DAAC cyan_file_search
-> getfile with an Earthdata bearer token) is the repo's cited CyAN acquisition layer
(`data-sources/cyan/`), not re-implemented here. This step VERIFIES the cache is present
and complete and summarizes it; if it is empty it points you at that pull rather than
pretending to fetch the multi-GB series from a two-line call.

Run:  python 01_ingest.py    # verify the CyAN weekly-CONUS-mosaic cache + the FL lakes layer
"""
import sys
import config
from common import parse_week_start


def list_olci_rasters():
    """(path, week_start) for every OLCI weekly mosaic in the cache, sorted by date."""
    out = []
    for p in sorted(config.CYAN_RAW_DIR.glob("*.tif")):
        ws = parse_week_start(p.name, config.OLCI_PREFIX)
        if ws is not None:
            out.append((p, ws))
    return sorted(out, key=lambda t: t[1])


def main():
    if not config.FL_LAKES_GPKG.exists():
        sys.exit(f"ERROR: FL lakes layer missing: {config.FL_LAKES_GPKG}\n"
                 f"It is the CyAN resolvable-lakes set clipped to Florida (COMID + "
                 f"AREASQKM). Produce it via the repo acquire step (build_fl_lake_mask).")

    rasters = list_olci_rasters()
    if not rasters:
        sys.exit(
            f"ERROR: no CyAN OLCI weekly CONUS mosaics in {config.CYAN_RAW_DIR}\n"
            f"This PoC reads the weekly-CONUS-mosaic CyAN product. Populate the cache from\n"
            f"source with the repo's cited CyAN pull (needs a free NASA Earthdata token in\n"
            f"data-sources/.env):  python data-sources/cyan/access/pull_cyan.py --help\n"
            f"or point config.CYAN_RAW_DIR at an existing cache.")

    # Completeness check: OLCI weekly composites are a strict 7-day grid, so any non-7-day
    # step means the cache is missing week(s). Flag it rather than silently modelling a
    # gappy series (we do not auto-fill single missing weeks - a clean re-pull does that).
    dates = [ws for _, ws in rasters]
    gaps = [(a, b) for a, b in zip(dates, dates[1:]) if (b - a).days != 7]

    print(f"OK  FL lakes layer:   {config.FL_LAKES_GPKG.name}")
    print(f"OK  CyAN OLCI weeks:  {len(rasters)} composites "
          f"[{dates[0]} -> {dates[-1]}]")
    if gaps:
        print(f"WARNING: {len(gaps)} gap(s) in the weekly series - cache may be incomplete "
              f"(e.g. {gaps[0][0]} -> {gaps[0][1]}). Re-run against a fresh/complete pull.")
    print("Ingest complete." if not gaps else "Ingest complete (with gaps flagged above).")


if __name__ == "__main__":
    main()
