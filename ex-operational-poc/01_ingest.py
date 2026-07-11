"""Step 1 - INGEST.  Make sure the only two inputs the lean model needs are present:

  (a) CyAN weekly CONUS mosaics (the satellite signal), OLCI sensor only, and
  (b) the Florida resolvable-lakes layer (the lake universe + the `area_sqkm` feature).

CyAN publishes weekly 7-day CONUS mosaics on NASA's Ocean Biology DAAC. The real
"download from source" path (enumerate via cyan_file_search -> getfile with an
Earthdata bearer token) is delegated to the repo's already-tested CyAN client rather
than re-implemented here, and every file is content-addressed (sha256) so a re-run is a
cache check, not a re-download. With the cache already populated this step just
verifies and summarizes it.

Run:  python 01_ingest.py    # verify the cache (download the full set from source if it is empty)
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


def download_from_source():
    """Enumerate + fetch missing weekly OLCI mosaics from OB.DAAC using the repo's
    verified CyAN client (needs OB_DAAC_EDL_TOKEN in data-sources/.env). We reuse that
    client instead of duplicating a fragile API so there is one source of truth for how
    CyAN bytes are pulled and checksummed."""
    sys.path.insert(0, str(config.REPO / "data-sources"))
    from cyan.access import pull_cyan  # noqa: E402  (tested client in the repo)
    print("Downloading weekly OLCI CONUS mosaics via the repo CyAN client "
          "(cached + sha256-verified; skips files already present) ...")
    pull_cyan.main(["--region", "conus", "--period", "weekly",
                    "--dest", str(config.CYAN_RAW_DIR)])


def main():
    if not config.FL_LAKES_GPKG.exists():
        sys.exit(f"ERROR: FL lakes layer missing: {config.FL_LAKES_GPKG}\n"
                 f"It is the CyAN resolvable-lakes set clipped to Florida (COMID + "
                 f"AREASQKM). Produce it via the repo acquire step (build_fl_lake_mask).")

    rasters = list_olci_rasters()
    if not rasters:
        print("No CyAN OLCI mosaics in the cache - downloading the full set from source.")
        try:
            download_from_source()
            rasters = list_olci_rasters()
        except Exception as e:  # noqa: BLE001 - surface the reason plainly
            sys.exit(f"ERROR: could not download CyAN ({e}).\n"
                     f"Set OB_DAAC_EDL_TOKEN in data-sources/.env (free NASA Earthdata "
                     f"login) or point config.CYAN_RAW_DIR at an existing cache.")

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
