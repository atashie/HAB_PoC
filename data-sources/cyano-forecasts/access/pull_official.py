#!/usr/bin/env python
"""Download the OFFICIAL, citeable artifact for the EPA cyanoHAB forecast: the archived model CODE.

Unlike the live forecast values (unofficial Qlik extraction, see ``pull_forecasts.py``), this is a
fully official EPA deposit — the source code behind Schaeffer et al. 2024 — at a real DOI. We cache it
with a pinned sha256 so any upstream change is DETECTED (not silently absorbed), matching the CyAN/NARS
acquisition discipline. No authentication.

  DOI      : https://doi.org/10.23719/1529140  (EPA ScienceHub / data.gov `INLA_CONUS_forecast`)
  Resource : https://pasteur.epa.gov/uploads/10.23719/1529140/INLA_CONUS_forecast.zip
  License  : https://pasteur.epa.gov/license/sciencehub-license.html
  Contents : R source only (no input data — inputs are separately, publicly downloadable)

Examples
--------
python pull_official.py --dry-run   # show the pinned artifact + destination, no download
python pull_official.py             # download (or verify cached) + sha256 + manifest
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_MODULE_DIR = _HERE.parent
_DATA_SOURCES = _MODULE_DIR.parents[0]
for _p in (str(_HERE), str(_DATA_SOURCES)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from _common import net              # noqa: E402

OFFICIAL = {
    "doi": "10.23719/1529140",
    "url": "https://pasteur.epa.gov/uploads/10.23719/1529140/INLA_CONUS_forecast.zip",
    "filename": "INLA_CONUS_forecast.zip",
    "license": "https://pasteur.epa.gov/license/sciencehub-license.html",
    "catalog": "https://catalog.data.gov/dataset/inla_conus_forecast",
    "paper_doi": "10.1016/j.jenvman.2023.119518",
    # Verified 2026-07-02 (see reference/PRIMARY-SOURCES.md §5); pinned so drift is detected.
    "expected_sha256": "126f7f3fd9f79bdb36083009f726ecbe2d9047b728b7ac95bb2498545cf84afb",
    "expected_bytes": 33677,
}


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--outdir", default=str(_MODULE_DIR / "data" / "raw" / "official"))
    p.add_argument("--manifest", default=None, help="default: <module>/data/raw/manifest.jsonl")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = parse_args(argv)
    outdir = Path(args.outdir)
    dest = outdir / OFFICIAL["filename"]
    manifest = Path(args.manifest) if args.manifest else _MODULE_DIR / "data" / "raw" / "manifest.jsonl"

    if args.dry_run:
        print(f"[dry-run] would download {OFFICIAL['url']}")
        print(f"[dry-run]   -> {dest}")
        print(f"[dry-run]   expected {OFFICIAL['expected_bytes']:,} B  sha256 {OFFICIAL['expected_sha256'][:12]}…")
        return 0

    session = net.make_session()
    res = net.download_file(session, OFFICIAL["url"], dest,
                            expected_sha256=OFFICIAL["expected_sha256"], min_bytes=1000)
    record = {
        "kind": "official_code", "doi": OFFICIAL["doi"], "paper_doi": OFFICIAL["paper_doi"],
        "url": res.url, "filename": dest.name, "path": str(dest),
        "sha256": res.sha256, "bytes": res.bytes, "cached": res.cached,
        "integrity": res.integrity, "license": OFFICIAL["license"], "catalog": OFFICIAL["catalog"],
        "accessed_utc": res.accessed_utc,
    }
    net.append_manifest(manifest, record)
    status = "cached" if res.cached else "downloaded"
    print(f"[official] {status} {dest.name} ({res.bytes:,} B, sha256 {res.sha256[:12]}…, "
          f"integrity={res.integrity}) -> manifest")
    if res.integrity == "mismatch":
        print("[official] WARNING: bytes differ from the pinned sha256 — EPA re-deposited the artifact; "
              "review before trusting, then update the pin.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
