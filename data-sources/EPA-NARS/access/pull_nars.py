#!/usr/bin/env python
"""Acquire EPA National Lakes Assessment (NLA) data files - cached, manifested, auditable.

NARS has no API; it publishes small, static flat CSVs (+ .txt dictionaries) at stable
epa.gov URLs. This CLI mirrors a selected cycle's indicators locally so all downstream
work is offline, deterministic, and traceable to exact bytes (sha256 in a JSONL manifest).

No authentication is required - these are U.S. public-domain files.

Examples
--------
# Plan only (no download): what would we pull for the default HAB indicator set, 2022?
python pull_nars.py --dry-run

# Pull the default set (siteinfo, waterchem, algaltoxins, secchi, lakes_shp) for NLA 2022:
python pull_nars.py

# Pull every pinned 2022 indicator:
python pull_nars.py --indicators all

# Pull a specific subset:
python pull_nars.py --indicators siteinfo,waterchem,algaltoxins

# Check whether EPA has added/revised files vs our pinned manifest (network; no download):
python pull_nars.py --check-drift
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# --- make `_common` importable, and this dir's modules importable ----------- #
_HERE = Path(__file__).resolve().parent
_DATA_SOURCES = _HERE.parents[1]
for _p in (str(_HERE), str(_DATA_SOURCES)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from _common import net              # noqa: E402
import nars_catalog as cat           # noqa: E402

_NARS_DIR = _HERE.parent
_DEFAULT_RAW = _NARS_DIR / "data" / "raw"


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--cycle", type=int, default=2022, choices=sorted(cat.PINNED),
                   help="NLA survey cycle year (default 2022; only pinned cycles allowed)")
    p.add_argument("--indicators", default=",".join(cat.DEFAULT_INDICATORS),
                   help="comma-separated indicator keys, or 'all'. "
                        f"Default: {','.join(cat.DEFAULT_INDICATORS)}")
    p.add_argument("--outdir", default=str(_DEFAULT_RAW),
                   help="download cache root (a per-cycle subfolder is created)")
    p.add_argument("--limit", type=int, default=0,
                   help="cap number of DATA files (0 = no cap); for sampling")
    p.add_argument("--dry-run", action="store_true",
                   help="list the plan only; no download, no network")
    p.add_argument("--check-drift", action="store_true",
                   help="fetch the live NARS page and diff vs the pinned manifest, then exit")
    p.add_argument("--no-meta", action="store_true",
                   help="skip the companion .txt metadata dictionaries")
    return p.parse_args(argv)


def _resolve_indicators(cycle: int, spec: str) -> list[str]:
    available = cat.PINNED[cycle]
    if spec.strip().lower() == "all":
        return list(available)
    wanted = [s.strip() for s in spec.split(",") if s.strip()]
    unknown = [w for w in wanted if w not in available]
    if unknown:
        raise SystemExit(
            f"Unknown indicator(s) for NLA {cycle}: {unknown}\n"
            f"Available: {sorted(available)}"
        )
    return wanted


def check_drift(cycle: int) -> int:
    session = net.make_session()
    print(f"Fetching {cat.NARS_DATA_PAGE} to check for drift vs pinned NLA {cycle} ...")
    discovered = cat.discover(session)
    rep = cat.reconcile(cycle, discovered)
    print(f"\nDrift report for NLA {cycle}:")
    print(f"  matched (pinned & live): {rep.n_matched}")
    if rep.new_on_page:
        print(f"  NEW on page (not pinned) - review & consider adding: {len(rep.new_on_page)}")
        for n in rep.new_on_page:
            print(f"    + {n}  [{cat.indicator_of(n)}]")
    if rep.missing_from_page:
        print(f"  MISSING from page (pinned URL no longer linked): {len(rep.missing_from_page)}")
        for n in rep.missing_from_page:
            print(f"    - {n}")
    if rep.is_clean:
        print("  OK - clean: pinned manifest matches the live page exactly.")
    return 0


def main(argv=None) -> int:
    args = parse_args(argv)

    if args.check_drift:
        return check_drift(args.cycle)

    indicators = _resolve_indicators(args.cycle, args.indicators)
    files = cat.PINNED[args.cycle]

    # Build the download plan: (url, dest, kind, indicator).
    cycle_dir = Path(args.outdir) / f"nla{args.cycle}"
    plan: list[tuple[str, Path, str, str]] = []
    n_data = 0
    stop = False
    for ind in indicators:
        if stop:
            break
        for ref in files[ind]:
            if args.limit and n_data >= args.limit:
                stop = True
                break
            n_data += 1
            data_name = ref.data_url.rsplit("/", 1)[-1]
            plan.append((ref.data_url, cycle_dir / data_name, cat.kind_of(data_name), ind))
            if ref.meta_url and not args.no_meta:
                meta_name = ref.meta_url.rsplit("/", 1)[-1]
                plan.append((ref.meta_url, cycle_dir / meta_name, "meta", ind))

    print(f"NLA {args.cycle}: {len(indicators)} indicator(s), "
          f"{len(plan)} file(s) planned -> {cycle_dir}")
    for url, dest, kind, ind in plan:
        print(f"  [{ind:>13} | {kind:>7}] {dest.name}")

    if args.dry_run:
        print("\n(dry-run) no files downloaded.")
        return 0

    session = net.make_session()
    manifest = cycle_dir / "manifest.jsonl"
    n_new = n_cached = 0
    for url, dest, kind, ind in plan:
        res = net.download_file(session, url, dest)
        rec = {
            "dataset": "nars_nla",
            "cycle": args.cycle,
            "indicator": ind,
            "kind": kind,
            "url": res.url,
            "path": str(dest.relative_to(_NARS_DIR)),
            "bytes": res.bytes,
            "sha256": res.sha256,
            "cached": res.cached,
            "accessed_utc": res.accessed_utc,
        }
        net.append_manifest(manifest, rec)
        if res.cached:
            n_cached += 1
        else:
            n_new += 1
        flag = "cached" if res.cached else "downloaded"
        print(f"  {flag:>10}  {dest.name}  ({res.bytes:,} B)")

    print(f"\nDone. {n_new} downloaded, {n_cached} cached. Manifest: "
          f"{manifest.relative_to(_NARS_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
