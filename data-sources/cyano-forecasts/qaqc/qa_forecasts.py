#!/usr/bin/env python
"""QA/QC for the EPA cyanoHAB forecast snapshots — verify structure & integrity from the data itself.

Two separate QA passes, because the source has two shapes (see ../METADATA.md §2, Codex review):

  * LIVE-SNAPSHOT QA (newest snapshot): compares the current dashboard extract to the documented
    probe baseline WITH TOLERANCE — panel completeness, value range, geotag validity, Saturday
    cadence, distribution — because the live window legitimately advances/drops weeks.
  * ARCHIVE QA (accumulated snapshots -> data/derived): shape-agnostic invariants that must hold no
    matter how many weeks we have accrued — no duplicate current lake-weeks, per-COMID weekly
    continuity, and revision accounting.

Plus INTEGRITY (sha256 of every manifested file vs the manifest, incl. the official code ZIP).

Emits ``outputs/qa_report.md`` (human) + ``outputs/qa_summary.json`` (machine/CI). A clean report
still lists what was checked. Run after ``access/pull_forecasts.py``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
_MODULE_DIR = _HERE.parent
_RAW = _MODULE_DIR / "data" / "raw"
_DERIVED = _MODULE_DIR / "data" / "derived"
_OUT = _MODULE_DIR / "outputs"

# Documented reference values (from the 2026-07-02 probe; METADATA §3/§4/§13). Deviations are
# REPORTED as flags, not treated as hard failures — the live product can legitimately change.
DELIVERED_LAKES = 2191          # distinct COMIDs actually delivered
ADVERTISED_LAKES = 2192         # EPA's advertised count (the 1-lake gap is a known, flagged issue)
CONUS_LAT = (24.0, 50.0)
CONUS_LON = (-125.0, -66.0)
PCT_RANGE = (0.0, 100.0)


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def _read_manifest(path: Path) -> list:
    if not path.is_file():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def check_integrity(manifest: list) -> dict:
    results = []
    for rec in manifest:
        p = Path(rec.get("path", ""))
        if not p.is_file():
            results.append({"filename": rec.get("filename"), "status": "MISSING"})
            continue
        ok = _sha256(p) == rec.get("sha256")
        results.append({"filename": rec.get("filename"), "kind": rec.get("kind"),
                        "status": "ok" if ok else "SHA_MISMATCH"})
    bad = [r for r in results if r["status"] != "ok"]
    return {"n_files": len(results), "n_bad": len(bad), "files": results}


def _newest_snapshot(manifest: list) -> Path | None:
    snaps = [r for r in manifest if r.get("kind") == "snapshot"]
    if not snaps:
        # fall back to files on disk
        found = sorted((_RAW / "snapshots").glob("allweeks_*.csv"))
        return found[-1] if found else None
    newest = sorted(snaps, key=lambda r: r.get("snapshot_utc", ""))[-1]
    return Path(newest["path"])


def qa_live_snapshot(snap_path: Path) -> dict:
    df = pd.read_csv(snap_path, dtype={"comid": "Int64"})
    r: dict = {"snapshot_file": snap_path.name, "n_rows": int(len(df)), "flags": []}

    # -- schema --
    expected_cols = ["comid", "lake_name", "state", "epa_region", "week_end_date", "year",
                     "percent_chance", "lat_centroid", "lon_centroid", "date_raw", "week_end_raw", "flags"]
    r["schema_ok"] = list(df.columns) == expected_cols
    if not r["schema_ok"]:
        r["flags"].append(f"schema mismatch: {list(df.columns)}")

    # -- lakes / weeks --
    n_comid = int(df["comid"].nunique(dropna=True))
    n_null_comid = int(df["comid"].isna().sum())
    weeks = sorted(df["week_end_date"].dropna().unique())
    r.update({"n_distinct_comid": n_comid, "n_null_comid": n_null_comid,
              "n_distinct_weeks": len(weeks), "week_min": weeks[0] if weeks else None,
              "week_max": weeks[-1] if weeks else None})
    if n_comid != DELIVERED_LAKES:
        r["flags"].append(f"lake count {n_comid} != documented {DELIVERED_LAKES} (live change?)")
    r["lake_count_note"] = f"delivered {n_comid}; EPA advertises {ADVERTISED_LAKES} (known 1-lake gap)"
    if n_null_comid:
        r["flags"].append(f"{n_null_comid} null COMID rows")

    # -- panel completeness (rectangular?) --
    expected_cells = n_comid * len(weeks)
    r["panel_complete"] = (len(df) == expected_cells)
    r["n_missing_lakeweeks"] = int(expected_cells - len(df))
    if not r["panel_complete"]:
        r["flags"].append(f"panel not rectangular: {len(df)} rows vs {expected_cells} lake*weeks")

    # -- duplicate lake-weeks --
    dups = int(df.duplicated(subset=["comid", "week_end_date"]).sum())
    r["n_duplicate_lakeweeks"] = dups
    if dups:
        r["flags"].append(f"{dups} duplicate (COMID, week) rows")

    # -- percent_chance range + distribution --
    pct = pd.to_numeric(df["percent_chance"], errors="coerce")
    n_oob = int(((pct < PCT_RANGE[0]) | (pct > PCT_RANGE[1])).sum())
    r["n_percent_out_of_range"] = n_oob
    r["n_percent_null"] = int(pct.isna().sum())
    if n_oob:
        r["flags"].append(f"{n_oob} percent_chance out of [0,100]")
    r["percent_stats"] = {"min": float(pct.min()), "max": float(pct.max()),
                          "mean": round(float(pct.mean()), 3)}
    r["percent_buckets"] = {
        "eq_0": int((pct == 0).sum()),
        "0_10": int(((pct > 0) & (pct < 10)).sum()),
        "10_50": int(((pct >= 10) & (pct < 50)).sum()),
        "ge_50": int((pct >= 50).sum()),
    }

    # -- geotag validity --
    lat = pd.to_numeric(df["lat_centroid"], errors="coerce")
    lon = pd.to_numeric(df["lon_centroid"], errors="coerce")
    n_lat_oob = int(((lat < CONUS_LAT[0]) | (lat > CONUS_LAT[1])).sum())
    n_lon_oob = int(((lon < CONUS_LON[0]) | (lon > CONUS_LON[1])).sum())
    n_lon_pos = int((lon > 0).sum())
    r.update({"n_lat_out_of_conus": n_lat_oob, "n_lon_out_of_conus": n_lon_oob,
              "n_lon_positive": n_lon_pos})
    for label, n in [("lat", n_lat_oob), ("lon", n_lon_oob), ("lon>0", n_lon_pos)]:
        if n:
            r["flags"].append(f"{n} rows with {label} outside CONUS/sign")

    # -- stable coords per COMID (a point can be in-CONUS yet swapped/mislabeled week-to-week) --
    coord_var = df.groupby("comid")[["lat_centroid", "lon_centroid"]].nunique()
    n_unstable = int(((coord_var["lat_centroid"] > 1) | (coord_var["lon_centroid"] > 1)).sum())
    r["n_comid_unstable_coords"] = n_unstable
    if n_unstable:
        r["flags"].append(f"{n_unstable} COMIDs have >1 distinct centroid across weeks")

    # -- Saturday cadence + weekly spacing --
    wk_dates = [date.fromisoformat(w) for w in weeks]
    n_non_sat = sum(1 for d in wk_dates if d.weekday() != 5)
    r["n_non_saturday_weeks"] = n_non_sat
    if n_non_sat:
        r["flags"].append(f"{n_non_sat} week-ending dates are not Saturday")
    # gaps within a season = spacing >7d that also crosses <90d (i.e., not the Nov->Apr off-season)
    gaps = []
    for a, b in zip(wk_dates, wk_dates[1:]):
        delta = (b - a).days
        if delta != 7 and delta < 90:
            gaps.append((a.isoformat(), b.isoformat(), delta))
    r["intra_season_week_gaps"] = gaps
    if gaps:
        r["flags"].append(f"{len(gaps)} intra-season week gaps != 7d")

    # -- carry through the pull-time normalization flags --
    norm_flagged = int((df["flags"].fillna("") != "").sum())
    r["n_pull_flagged_rows"] = norm_flagged
    if norm_flagged:
        r["flags"].append(f"{norm_flagged} rows carried pull-time normalization flags")

    r["clean"] = (len(r["flags"]) == 0)
    return r


def qa_archive() -> dict:
    r: dict = {"flags": []}
    cur = _DERIVED / "current.csv"
    rev = _DERIVED / "revisions.csv"
    if not cur.is_file():
        r["status"] = "no derived views yet (run access/pull_forecasts.py)"
        return r
    dfc = pd.read_csv(cur, dtype={"comid": "Int64"})
    r["n_current_lakeweeks"] = int(len(dfc))
    r["n_distinct_comid"] = int(dfc["comid"].nunique())
    r["n_distinct_weeks"] = int(dfc["week_end_date"].nunique())
    dup = int(dfc.duplicated(subset=["comid", "week_end_date"]).sum())
    r["n_duplicate_current_lakeweeks"] = dup
    if dup:
        r["flags"].append(f"{dup} duplicate (COMID, week) in current view — view build is broken")

    # per-COMID weekly continuity across the accumulated archive
    dfc = dfc.dropna(subset=["comid", "week_end_date"]).copy()
    dfc["d"] = pd.to_datetime(dfc["week_end_date"], errors="coerce")
    gap_lakes = 0
    for _comid, g in dfc.groupby("comid"):
        ds = g["d"].sort_values().to_list()
        if any(0 < (b - a).days != 7 and (b - a).days < 90 for a, b in zip(ds, ds[1:])):
            gap_lakes += 1
    r["n_comid_with_intra_season_gaps"] = gap_lakes

    if rev.is_file():
        dfr = pd.read_csv(rev)
        r["n_revisions"] = int(len(dfr))
        if len(dfr):
            oldv = pd.to_numeric(dfr["old_percent"], errors="coerce")
            newv = pd.to_numeric(dfr["new_percent"], errors="coerce")
            r["revision_abs_delta"] = {"max": float((newv - oldv).abs().max()),
                                       "mean": round(float((newv - oldv).abs().mean()), 3)}
    r["clean"] = (len(r["flags"]) == 0)
    return r


def write_report(summary: dict) -> None:
    _OUT.mkdir(parents=True, exist_ok=True)
    (_OUT / "qa_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    live = summary["live_snapshot"]
    integ = summary["integrity"]
    arch = summary["archive"]
    L = []
    L.append("# cyano-forecasts — QA/QC report\n")
    L.append(f"_Generated by `qaqc/qa_forecasts.py`. Access date of data: {summary['access_note']}._\n")
    L.append("This dataset's live values come from an UNOFFICIAL Qlik extraction (see METADATA §7.2); "
             "QA is split into a live-snapshot pass and a shape-agnostic archive pass.\n")

    L.append("## 1. Integrity (sha256 vs manifest)\n")
    L.append(f"- Files checked: **{integ['n_files']}**; failures: **{integ['n_bad']}**")
    for f in integ["files"]:
        L.append(f"  - `{f['filename']}` ({f.get('kind','?')}) — {f['status']}")
    L.append("")

    L.append("## 2. Live-snapshot QA (newest snapshot)\n")
    L.append(f"- Snapshot: `{live['snapshot_file']}` — **{live['n_rows']:,} rows**")
    L.append(f"- Lakes: **{live['n_distinct_comid']}** distinct COMID "
             f"({live['lake_count_note']}); null COMID: {live['n_null_comid']}")
    L.append(f"- Weeks: **{live['n_distinct_weeks']}** ({live['week_min']} → {live['week_max']}); "
             f"non-Saturday: {live['n_non_saturday_weeks']}; intra-season gaps: {len(live['intra_season_week_gaps'])}")
    L.append(f"- Panel rectangular: **{live['panel_complete']}** (missing lake-weeks: {live['n_missing_lakeweeks']}); "
             f"duplicate lake-weeks: {live['n_duplicate_lakeweeks']}")
    L.append(f"- `percent_chance`: range [{live['percent_stats']['min']}, {live['percent_stats']['max']}], "
             f"mean {live['percent_stats']['mean']}; out-of-range: {live['n_percent_out_of_range']}; "
             f"null: {live['n_percent_null']}")
    b = live["percent_buckets"]
    L.append(f"  - distribution: =0 → {b['eq_0']:,}; (0,10) → {b['0_10']:,}; "
             f"[10,50) → {b['10_50']:,}; ≥50 → {b['ge_50']:,}")
    L.append(f"- Geotag: lat OOB {live['n_lat_out_of_conus']}, lon OOB {live['n_lon_out_of_conus']}, "
             f"lon>0 {live['n_lon_positive']}; COMIDs with unstable centroid: {live['n_comid_unstable_coords']}")
    L.append(f"- Pull-time normalization flags: {live['n_pull_flagged_rows']}")
    L.append(f"- **Live-snapshot clean: {live['clean']}**")
    if live["flags"]:
        L.append("  - flags: " + "; ".join(live["flags"]))
    L.append("")

    L.append("## 3. Archive QA (accumulated snapshots → derived views)\n")
    if "status" in arch:
        L.append(f"- {arch['status']}")
    else:
        L.append(f"- Current view: **{arch['n_current_lakeweeks']:,}** lake-weeks "
                 f"({arch['n_distinct_comid']} lakes × {arch['n_distinct_weeks']} weeks); "
                 f"duplicate current lake-weeks: {arch['n_duplicate_current_lakeweeks']}")
        L.append(f"- COMIDs with intra-season gaps across the archive: {arch['n_comid_with_intra_season_gaps']}")
        L.append(f"- Revisions recorded: {arch.get('n_revisions', 0)}"
                 + (f" (|Δ| max {arch['revision_abs_delta']['max']}, mean {arch['revision_abs_delta']['mean']})"
                    if arch.get("n_revisions") else ""))
        L.append(f"- **Archive clean: {arch['clean']}**")
        if arch["flags"]:
            L.append("  - flags: " + "; ".join(arch["flags"]))
    L.append("")

    L.append("## 4. What this QA does NOT check\n")
    L.append("- COMID existence against a pinned NHDPlus/LakeCat reference (linkage validation — deferred to "
             "the fusion analysis; see METADATA §11).")
    L.append("- Whether the forecast is *correct* — this is a source-integrity/structure QA, not a skill "
             "evaluation. Skill metrics are EPA-reported (METADATA §13), not validated here.")
    (_OUT / "qa_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=str(_RAW / "manifest.jsonl"))
    args = ap.parse_args(argv)

    manifest = _read_manifest(Path(args.manifest))
    integ = check_integrity(manifest)
    snap = _newest_snapshot(manifest)
    if snap is None:
        print("[qa] no snapshot found — run access/pull_forecasts.py first", file=sys.stderr)
        return 2
    live = qa_live_snapshot(snap)
    arch = qa_archive()
    access_note = next((r.get("snapshot_utc") for r in manifest if r.get("kind") == "snapshot"), "unknown")
    summary = {"access_note": access_note, "integrity": integ,
               "live_snapshot": live, "archive": arch}
    write_report(summary)

    clean = (integ["n_bad"] == 0) and live["clean"] and arch.get("clean", True)
    print(f"[qa] integrity: {integ['n_files']} files, {integ['n_bad']} bad")
    print(f"[qa] live-snapshot clean={live['clean']} ({len(live['flags'])} flags); "
          f"archive clean={arch.get('clean', True)}")
    print(f"[qa] wrote outputs/qa_report.md + qa_summary.json")
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
