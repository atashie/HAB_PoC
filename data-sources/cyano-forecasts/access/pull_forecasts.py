#!/usr/bin/env python
"""Snapshot EPA's experimental cyanoHAB forecast (the full AllWeeks panel) from its Qlik dashboard.

⚠️ UNOFFICIAL access path — see ``qlik_public.py`` and ``../METADATA.md`` §7.2/§12. This module exists
because the live forecast values have no official API; it is a research/benchmark ingestion, not a
production dependency.

Because the dashboard keeps only a **rolling ~2 seasons** and can **revise** past weeks (§2), this is
an **append-only snapshot** tool designed to be re-run **weekly** to accumulate the history the
dashboard discards:

  1. Extract the full ``AllWeeks_CyanForecasts`` table over QIX (fail-closed: reads exactly
     ``qSize.qcy`` rows — see the extraction contract in ``qlik_public.extract_table``).
  2. Normalize (WeekEndDate dual -> ISO + Saturday assert; Year cross-check; numeric coercions),
     write an **immutable, dated snapshot CSV** (never overwritten), sha256 it, and append a
     **full-provenance** record to the JSONL manifest.
  3. Rebuild two derived views from ALL snapshots (idempotent): ``current.csv`` (newest value per
     ``(COMID, WeekEndDate)``) and ``revisions.csv`` (every past week whose probability CHANGED
     between snapshots) — so revisions are recorded, never silently blessed.

Examples
--------
python pull_forecasts.py --dry-run          # schema + qSize + selection state only (fast, no full pull)
python pull_forecasts.py                     # full weekly snapshot -> data/raw/snapshots/ + views
python pull_forecasts.py --cross-check       # also pull the sibling AllWeeks app and diff it
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

_ACCESS_DIR = Path(__file__).resolve().parent
_MODULE_DIR = _ACCESS_DIR.parent
_DATA_SOURCES = _MODULE_DIR.parent
# make `_common` importable (data-sources on path) and this dir's siblings importable (access on path);
# the module folder name `cyano-forecasts` is hyphenated, so it can't be a Python package.
for _p in (str(_ACCESS_DIR), str(_DATA_SOURCES)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from _common import net              # noqa: E402
import qlik_public as qp             # noqa: E402

CLIENT_VERSION = "qlik_public/0.1"
_QLIK_EPOCH = date(1899, 12, 30)   # Qlik/Excel date serial base (valid for all dates >= 1900-03-01)

# Stable output column order (fixes CSV sha256 across runs).
_SNAPSHOT_COLS = [
    "comid", "lake_name", "state", "epa_region", "week_end_date", "year",
    "percent_chance", "lat_centroid", "lon_centroid", "date_raw", "week_end_raw", "flags",
]


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def _iso_from_serial(num) -> str:
    try:
        return (_QLIK_EPOCH + timedelta(days=int(round(float(num))))).isoformat()
    except Exception:
        return ""


def normalize_row(row: dict) -> dict:
    """Pure: one QIX row (dict[field]->Cell) -> a tidy record + a list of QA flags.

    Never raises — anomalies become ``flags`` so a single odd row can't abort a snapshot; QA
    (``qaqc/qa_forecasts.py``) is where flags are tallied and judged.
    """
    flags: list = []

    def num(field):
        c = row[field]
        if c.num is not None:
            return c.num
        try:
            return float(c.text)
        except Exception:
            flags.append(f"{field}:nonnumeric")
            return None

    comid_c = row["COMID"]
    try:
        comid = int(round(float(comid_c.num if comid_c.num is not None else comid_c.text)))
    except Exception:
        comid = None
        flags.append("COMID:unparseable")

    # WeekEndDate: prefer display text (M/D/Y); cross-check the numeric serial; assert Saturday.
    wk = row["WeekEndDate"]
    iso = ""
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y"):
        try:
            iso = datetime.strptime(wk.text, fmt).date().isoformat()
            break
        except Exception:
            continue
    if not iso:
        iso = _iso_from_serial(wk.num)
        if iso:
            flags.append("WeekEndDate:parsed_from_serial")
        else:
            flags.append("WeekEndDate:unparseable")
    if iso:
        d = date.fromisoformat(iso)
        if d.weekday() != 5:                       # 5 == Saturday
            flags.append(f"WeekEndDate:not_saturday({d.strftime('%A')})")
        if wk.num is not None:
            serial_iso = _iso_from_serial(wk.num)
            if serial_iso and serial_iso != iso:
                flags.append("WeekEndDate:text_serial_mismatch")

    year = None
    try:
        year = int(round(float(row["Year"].num if row["Year"].num is not None else row["Year"].text)))
    except Exception:
        flags.append("Year:unparseable")
    if iso and year is not None and date.fromisoformat(iso).year != year:
        flags.append("Year:disagrees_with_weekenddate")

    pct = num("Percent_chance_of_cyanoHAB")
    if pct is not None and not (0.0 <= pct <= 100.0):
        flags.append(f"percent_chance:out_of_range({pct})")

    return {
        "comid": comid,
        "lake_name": row["Lake_name_for_public"].text,
        "state": row["State"].text,
        "epa_region": row["EPA_region"].text,
        "week_end_date": iso,
        "year": year,
        "percent_chance": pct,
        "lat_centroid": num("Lat_centroid"),
        "lon_centroid": num("Lon_centroid"),
        "date_raw": row["Date"].text,
        "week_end_raw": wk.text,
        "flags": "|".join(flags),
    }


def _write_snapshot(records: list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Deterministic ordering so a re-pull of identical data yields an identical file/sha256.
    records = sorted(records, key=lambda r: (r["week_end_date"], r["comid"] if r["comid"] is not None else -1))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=_SNAPSHOT_COLS)
        w.writeheader()
        w.writerows(records)


def rebuild_views(snapshots_dir: Path, derived_dir: Path) -> dict:
    """Rebuild current.csv + revisions.csv from ALL snapshots (idempotent). Returns a summary."""
    snaps = sorted(glob.glob(str(snapshots_dir / "allweeks_*.csv")))
    current: dict = {}          # (comid, week_end_date) -> (percent, snapshot_tag, record)
    revisions: list = []
    for snap in snaps:
        tag = Path(snap).stem
        with open(snap, encoding="utf-8") as f:
            for rec in csv.DictReader(f):
                key = (rec["comid"], rec["week_end_date"])
                new_pct = rec["percent_chance"]
                prev = current.get(key)
                if prev is not None and prev[0] != new_pct:
                    revisions.append({
                        "comid": rec["comid"], "week_end_date": rec["week_end_date"],
                        "old_percent": prev[0], "new_percent": new_pct,
                        "old_snapshot": prev[1], "new_snapshot": tag,
                    })
                current[key] = (new_pct, tag, rec)
    derived_dir.mkdir(parents=True, exist_ok=True)
    cur_path = derived_dir / "current.csv"
    with cur_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=_SNAPSHOT_COLS + ["source_snapshot"])
        w.writeheader()
        for (comid, wk), (pct, tag, rec) in sorted(current.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            rec = dict(rec); rec["source_snapshot"] = tag
            w.writerow(rec)
    rev_path = derived_dir / "revisions.csv"
    with rev_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["comid", "week_end_date", "old_percent", "new_percent",
                                          "old_snapshot", "new_snapshot"])
        w.writeheader()
        w.writerows(revisions)
    return {"n_snapshots": len(snaps), "n_current_lakeweeks": len(current), "n_revisions": len(revisions)}


def _summarize(records: list) -> dict:
    weeks = sorted({r["week_end_date"] for r in records if r["week_end_date"]})
    comids = {r["comid"] for r in records if r["comid"] is not None}
    flagged = sum(1 for r in records if r["flags"])
    return {
        "n_rows": len(records), "n_distinct_comid": len(comids), "n_distinct_weeks": len(weeks),
        "week_min": weeks[0] if weeks else None, "week_max": weeks[-1] if weeks else None,
        "n_flagged_rows": flagged,
    }


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--app", default=qp.CANONICAL_APP, choices=list(qp.APPS),
                   help="which dashboard app to pull (default: canonical AllWeeks app)")
    p.add_argument("--outdir", default=str(_MODULE_DIR / "data" / "raw"))
    p.add_argument("--manifest", default=None, help="default: <outdir>/manifest.jsonl")
    p.add_argument("--snapshot-utc", default=None,
                   help="override snapshot timestamp tag (YYYYMMDDTHHMMSSZ); default = now (UTC)")
    p.add_argument("--cross-check", action="store_true",
                   help="also pull the sibling AllWeeks app and report schema/rowcount/value agreement")
    p.add_argument("--rebuild-only", action="store_true",
                   help="skip the network pull; just rebuild current.csv/revisions.csv from snapshots")
    p.add_argument("--insecure", action="store_true", help="disable TLS verification (last resort)")
    p.add_argument("--dry-run", action="store_true",
                   help="connect, ClearAll, read schema + qSize + selection state; no full extract")
    return p.parse_args(argv)


def _pull_records(appid: str, insecure: bool):
    with qp.QlikPublicClient(appid, verify_tls=not insecure) as cli:
        rows, meta = cli.extract_table(qp.ALLWEEKS_FIELDS)
    return [normalize_row(r) for r in rows], meta


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = parse_args(argv)
    outdir = Path(args.outdir)
    snapshots_dir = outdir / "snapshots"
    derived_dir = _MODULE_DIR / "data" / "derived"
    manifest = Path(args.manifest) if args.manifest else outdir / "manifest.jsonl"

    if args.rebuild_only:
        summary = rebuild_views(snapshots_dir, derived_dir)
        print(f"[rebuild] {summary}")
        return 0

    appid = qp.APPS[args.app]
    if args.app == "currentweek":
        print("[warn] 'currentweek' app opens with a default single-week selection; ClearAll is applied "
              "but the canonical AllWeeks apps are preferred for a full pull.", file=sys.stderr)

    if args.dry_run:
        with qp.QlikPublicClient(appid, verify_tls=not args.insecure) as cli:
            cli.open_doc()
            sel_before = cli.get_selections()
            cli.clear_all()
            sel_after = cli.get_selections()
            tables = [(t.get("qName"), t.get("qNoOfRows"), [f["qName"] for f in t.get("qFields", [])])
                      for t in cli.data_model()]
            rows, meta = cli.extract_table(qp.ALLWEEKS_FIELDS)  # reads full qSize, but we won't write it
        print(f"[dry-run] app={args.app} ({appid})")
        print(f"[dry-run] selections before ClearAll={sel_before or 'none'} after={sel_after or 'none'}")
        for name, n, fields in tables:
            print(f"[dry-run] table {name}: rows~{n} fields={fields}")
        print(f"[dry-run] qSize={meta.q_size} pages={meta.n_pages} page_rows={meta.page_rows} "
              f"row_count={meta.row_count}")
        return 0

    now = args.snapshot_utc or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    print(f"[pull] app={args.app} ({appid})  snapshot={now}")
    records, meta = _pull_records(appid, args.insecure)
    summary = _summarize(records)
    print(f"[pull] extracted {summary['n_rows']} rows | {summary['n_distinct_comid']} lakes | "
          f"{summary['n_distinct_weeks']} weeks {summary['week_min']}..{summary['week_max']} | "
          f"{summary['n_flagged_rows']} flagged rows | pages={meta.n_pages}")

    snap_path = snapshots_dir / f"allweeks_{now}.csv"
    _write_snapshot(records, snap_path)
    sha = _sha256(snap_path)

    record = {
        "kind": "snapshot", "snapshot_utc": now, "filename": snap_path.name, "path": str(snap_path),
        "sha256": sha, "bytes": snap_path.stat().st_size, "client_version": CLIENT_VERSION,
        "source_page": "https://www.epa.gov/habs/hab-forecasts",
        "app_label": args.app, "appid": meta.appid, "engine_url": meta.engine_url,
        "single_url": meta.single_url, "virtual_proxy": meta.virtual_proxy,
        "xrfkey_present": meta.xrfkey_present, "field_order": meta.field_order,
        "hypercube_def": meta.hypercube_def, "q_size": meta.q_size,
        "page_rows": meta.page_rows, "n_pages": meta.n_pages,
        "selection_before": meta.selection_before, "selection_after": meta.selection_after,
        "row_count": summary["n_rows"], "n_distinct_comid": summary["n_distinct_comid"],
        "n_distinct_weeks": summary["n_distinct_weeks"],
        "week_min": summary["week_min"], "week_max": summary["week_max"],
        "n_flagged_rows": summary["n_flagged_rows"], "accessed_utc": net._utc_now_iso(),
    }
    net.append_manifest(manifest, record)
    print(f"[pull] wrote {snap_path.name} ({record['bytes']:,} B, sha256 {sha[:12]}…) -> manifest")

    if args.cross_check:
        other = "allweeks_b" if args.app != "allweeks_b" else "allweeks_a"
        oth_records, oth_meta = _pull_records(qp.APPS[other], args.insecure)
        a = {(r["comid"], r["week_end_date"]): r["percent_chance"] for r in records}
        b = {(r["comid"], r["week_end_date"]): r["percent_chance"] for r in oth_records}
        common = a.keys() & b.keys()
        disagree = sum(1 for k in common if a[k] != b[k])
        print(f"[cross-check] {other}: rows={len(oth_records)} | shared_keys={len(common)} "
              f"| only_in_{args.app}={len(a.keys()-b.keys())} | only_in_{other}={len(b.keys()-a.keys())} "
              f"| value_disagreements={disagree}")

    views = rebuild_views(snapshots_dir, derived_dir)
    print(f"[views] {views}  -> data/derived/current.csv, revisions.csv")
    return 1 if summary["n_flagged_rows"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
