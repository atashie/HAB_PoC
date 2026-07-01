#!/usr/bin/env python
"""One-time (idempotent) backfill: add `processing_version` (+ `is_mosaic`) to an
existing CyAN download manifest whose records predate version-in-manifest.

Metadata-only: opens each GeoTIFF to read its `OBPG_version` tag (no pixel read,
NO re-hashing) and merges it into the matching manifest record. Existing fields
(sha256, bytes, etc.) are preserved untouched. Backs up manifest.jsonl ->
manifest.jsonl.bak before rewriting (atomic replace). Safe to re-run.

Usage:  python backfill_manifest_version.py --dir <folder-with-manifest.jsonl-and-tifs>
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from cyan.access import cyan_api as c   # noqa: E402


def backfill(dir_path: Path) -> int:
    manifest = dir_path / "manifest.jsonl"
    if not manifest.is_file():
        print(f"[backfill] no manifest at {manifest}", file=sys.stderr)
        return 2

    records = [json.loads(ln) for ln in manifest.read_text(encoding="utf-8").splitlines()
               if ln.strip()]
    print(f"[backfill] {manifest}: {len(records)} records")

    added = already = missing_file = no_tag = 0
    versions: Counter = Counter()
    out_lines = []
    for rec in records:
        fn = rec.get("filename")
        fpath = dir_path / fn if fn else None
        # is_mosaic (cheap, from filename) — add if absent
        if "is_mosaic" not in rec and fn:
            parsed = c.parse_cyan_filename(fn)
            if parsed:
                rec["is_mosaic"] = parsed.is_mosaic

        if rec.get("processing_version"):
            already += 1
            versions[rec["processing_version"]] += 1
        elif fpath and fpath.is_file():
            ver = c.read_processing_version(fpath)   # metadata-only
            rec["processing_version"] = ver
            if ver is None:
                no_tag += 1
            else:
                added += 1
                versions[ver] += 1
        else:
            missing_file += 1
            rec["processing_version"] = None
            rec.setdefault("backfill_note", "file not on disk at backfill time")

        rec.setdefault("integrity", "unverified")   # not re-hashed here
        out_lines.append(json.dumps(rec, sort_keys=True))

    # back up once, then atomically replace
    bak = manifest.with_suffix(".jsonl.bak")
    if not bak.exists():
        bak.write_text(manifest.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[backfill] backed up original -> {bak.name}")
    tmp = manifest.with_suffix(".jsonl.tmp")
    tmp.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    tmp.replace(manifest)

    print(f"[backfill] version added={added} already-present={already} "
          f"no-tag={no_tag} missing-file={missing_file}")
    print(f"[backfill] version distribution: {dict(versions)}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True,
                    help="folder containing manifest.jsonl and the .tif files")
    args = ap.parse_args(argv)
    return backfill(Path(args.dir))


if __name__ == "__main__":
    raise SystemExit(main())
