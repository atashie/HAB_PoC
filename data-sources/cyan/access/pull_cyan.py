#!/usr/bin/env python
"""Acquire CyAN CI_cyano merged GeoTIFF tiles for a region / period / tile-set / date-range.

Reproducible, cached, and auditable:
  * Enumerates files via the (no-auth) cyan_file_search API.
  * Reports the merged vs per-satellite split explicitly (no silent drops).
  * Defaults to the CYAN (version 6.0) stream for a consistent series (override with --stream).
  * Downloads only what's missing; every file is recorded in a JSONL manifest with
    sha256, byte size, source URL, stream, dates, tile, and access timestamp.

Auth: downloading requires a free NASA Earthdata Login AppKey (see
data-sources/cyan/METADATA.md §7.2). Put OB_DAAC_APPKEY in data-sources/.env
(gitignored) or the environment. --dry-run needs no auth.

Examples
--------
# Plan only (no download, no auth): what would we pull for Lake Erie tile, Aug 2022?
python pull_cyan.py --tiles 7_2 --sdate 2022-08-01 --edate 2022-08-31 --dry-run

# Download a small sample (needs AppKey):
python pull_cyan.py --tiles 7_2 --sdate 2022-08-08 --edate 2022-08-14 --period weekly
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# --- make `_common` and `cyan` importable when run as a script -------------- #
_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from _common import net                      # noqa: E402
from cyan.access import cyan_api as c         # noqa: E402

_CYAN_DIR = _DATA_SOURCES / "cyan"
_DEFAULT_RAW = _CYAN_DIR / "data" / "raw"
_DOTENV = _DATA_SOURCES / ".env"


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--region", default="conus", choices=["conus", "alaska", "ak"])
    p.add_argument("--period", default="weekly", choices=["daily", "weekly"],
                   help="weekly == 7-day max composite (default; soft preference over daily)")
    p.add_argument("--product", default="ci", choices=["ci", "truecolor"])
    p.add_argument("--tiles", default="7_2",
                   help="'all', a single tile '7_2', or several joined with '+': '7_2+6_2'")
    p.add_argument("--sdate", required=True, help="start date YYYY-MM-DD")
    p.add_argument("--edate", required=True, help="end date YYYY-MM-DD")
    p.add_argument("--stream", default="CYAN",
                   help="preferred processing stream. Default 'CYAN' (OBPG_version 6.0) is "
                        "available across the whole record -> a CONSISTENT series. 'CYANV6T' "
                        "(6T) exists only for a subset of dates; preferring it mixes batches.")
    p.add_argument("--outdir", default=str(_DEFAULT_RAW), help="download cache dir")
    p.add_argument("--manifest", default=None, help="manifest path (default <outdir>/manifest.jsonl)")
    p.add_argument("--limit", type=int, default=0, help="cap number of files (0 = no cap); for sampling")
    p.add_argument("--dry-run", action="store_true", help="enumerate & plan only; no download, no auth")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    outdir = Path(args.outdir)
    manifest = Path(args.manifest) if args.manifest else outdir / "manifest.jsonl"

    session = net.make_session()

    print(f"[search] region={args.region} period={args.period} product={args.product} "
          f"tiles={args.tiles} {args.sdate}..{args.edate}")
    urls = c.search_files(session, args.region, args.period, args.product,
                          args.tiles, args.sdate, args.edate)
    cats = c.categorize_search_results(urls)
    merged, per_sat, other = cats["merged"], cats["per_satellite"], cats["other"]
    print(f"[search] {len(urls)} URLs -> merged CI tiles={len(merged)}, "
          f"per-satellite (excluded)={len(per_sat)}, other (excluded)={len(other)}")
    if other:
        for o in other[:5]:
            print(f"         [other] {o.rsplit('/',1)[-1]}")

    plan = c.prefer_stream(merged, preferred=args.stream)
    n_v6 = sum(1 for f in plan if f.stream == args.stream)
    print(f"[plan]   {len(plan)} files after collapsing streams "
          f"({n_v6} {args.stream}, {len(plan) - n_v6} fallback)")

    if args.limit and len(plan) > args.limit:
        print(f"[plan]   LIMIT: sampling first {args.limit} of {len(plan)} files (sorted by date)")
        plan = plan[:args.limit]

    if args.dry_run:
        print("[dry-run] planned files (not downloaded):")
        for f in plan:
            print(f"          {f.start_date}..{f.end_date} {f.temporal:3s} {f.stream:8s} {f.tile}  {f.filename}")
        print(f"[dry-run] {len(plan)} files would be downloaded to {outdir}")
        return 0

    bearer = net.resolve_edl_token(_DOTENV)
    appkey = net.resolve_appkey(_DOTENV)
    if not (bearer or appkey):
        print("[error] No credentials found (env or data-sources/.env). Downloads need "
              "either OB_DAAC_EDL_TOKEN (Earthdata bearer token) or OB_DAAC_APPKEY — "
              "see METADATA.md §7.2. Use --dry-run to plan without auth.", file=sys.stderr)
        return 2
    auth_kind = "EDL bearer token" if bearer else "AppKey"
    print(f"[auth] using {auth_kind}")

    # Prior manifest -> latest sha256 per filename (for cache-hit validation & dedupe).
    prior = {}
    for rec in net.read_manifest(manifest):
        if rec.get("filename"):
            prior[rec["filename"]] = rec

    print(f"[download] -> {outdir}  (manifest: {manifest})")
    ok = skipped = failed = mismatched = 0
    for i, f in enumerate(plan, 1):
        dest = outdir / f.filename
        try:
            prior_rec = prior.get(f.filename)
            res = net.download_file(session, f.url, dest, appkey=appkey, bearer_token=bearer,
                                    expected_sha256=(prior_rec or {}).get("sha256"))
            # Processing version verified FROM the GeoTIFF metadata (METADATA.md §10).
            version = c.read_processing_version(dest)
            record = {
                "filename": f.filename, "url": f.url, "bytes": res.bytes,
                "sha256": res.sha256, "cached": res.cached, "integrity": res.integrity,
                "processing_version": version, "accessed_utc": res.accessed_utc,
                "sensor": f.sensor_code, "temporal": f.temporal, "stream": f.stream,
                "region": f.region, "tile": f.tile,
                "start_date": f.start_date, "end_date": f.end_date,
                "is_mosaic": f.is_mosaic,
            }
            # Dedupe: only (re)write a manifest line when this is a new file, the bytes
            # changed vs the prior record, or a stale cache was healed — so re-runs don't
            # bloat the audit trail but real events are always recorded.
            if (not prior_rec or prior_rec.get("sha256") != res.sha256
                    or res.integrity == "refetched_stale_cache"):
                net.append_manifest(manifest, record)
            if res.integrity in ("mismatch", "refetched_stale_cache"):
                mismatched += 1
                if res.integrity == "refetched_stale_cache":
                    print(f"  [{i}/{len(plan)}] ⚠ stale/corrupt cache for {f.filename} "
                          f"— refetched, now matches manifest sha.", file=sys.stderr)
                else:
                    print(f"  [{i}/{len(plan)}] ⚠ MISMATCH: fresh bytes for {f.filename} differ "
                          f"from manifest sha — upstream reprocessing? (recorded new sha).",
                          file=sys.stderr)
            if res.cached:
                skipped += 1
            else:
                ok += 1
            tag = "cached" if res.cached else "fetched"
            print(f"  [{i}/{len(plan)}] {tag} {f.filename} ({res.bytes:,} B, v{version})")
        except Exception as e:
            failed += 1
            print(f"  [{i}/{len(plan)}] FAILED {f.filename}: {e}", file=sys.stderr)

    print(f"[done] fetched={ok} cached={skipped} failed={failed} "
          f"integrity_mismatch={mismatched} total_planned={len(plan)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
