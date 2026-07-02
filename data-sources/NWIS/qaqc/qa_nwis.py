#!/usr/bin/env python
"""QA/QC for pulled NWIS in-situ series (daily / continuous) + the site-metadata table.

Verifies structure and integrity **from the data itself**, and emits:
  * outputs/qa_summary.json  (machine-readable: per-series + cross-cut)
  * outputs/qa_report.md     (human-readable)

What it checks (grounded in METADATA.md):
  * Integrity: sha256 recomputed vs the download manifest; flags files missing from it.
  * Structure: expected columns; single unit_of_measure per series; known parameter code.
  * Values: numeric coercion (flags non-numeric), min/median/max, and a LOOSE plausibility
    range per parameter (encoding-sanity, not scientific judgement) with out-of-range counts.
  * Provisional vs Approved: the count/percent split (the NWIS analogue of CyAN's
    measured-vs-missing distinction — provisional data are subject to revision).
  * Qualifiers: distinct qualifier flags present (e.g. DISCONTINUED, Ice, Estimated).
  * Duplicates / gaps: duplicate timestamps; date span; staleness vs --today.
  * Site table: counts by site type; sites missing lat/lon or HUC.

Usage:  python qa_nwis.py [--raw <dir>] [--outdir <dir>] [--today YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from _common import net                        # noqa: E402
from NWIS.access import nwis_api as nw          # noqa: E402

_NWIS = _DATA_SOURCES / "NWIS"
_DEFAULT_RAW = _NWIS / "data" / "raw"
_DEFAULT_OUT = _NWIS / "outputs"


def qa_series(path: Path, service: str, manifest_by_name: dict, today: str) -> dict:
    rec: dict = {"filename": path.name, "service": service}
    # provenance vs manifest
    m = manifest_by_name.get(path.name)
    if m:
        rec["manifest_sha256"] = m.get("sha256")
        rec["sha256_ok"] = (net._sha256(path) == m.get("sha256"))
    else:
        rec["sha256_ok"] = None

    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    rec["n_rows"] = int(len(df))
    if not len(df):
        rec["flags"] = ["empty file"]
        return rec

    pcode = df["parameter_code"].iloc[0] if "parameter_code" in df else None
    rec["parameter_code"] = pcode
    meta = nw.HAB_PARAMETERS.get(pcode)
    rec["parameter_known"] = meta is not None
    rec["parameter_name"] = meta[0] if meta else None

    # unit consistency
    units = sorted(set(df["unit_of_measure"])) if "unit_of_measure" in df else []
    rec["units"] = units

    # value stats (numeric coercion; count non-numeric)
    vals = pd.to_numeric(df["value"], errors="coerce")
    rec["n_nonnumeric"] = int(vals.isna().sum())
    good = vals.dropna()
    if len(good):
        rec["value_min"], rec["value_max"] = float(good.min()), float(good.max())
        rec["value_median"] = float(good.median())
    else:
        rec["value_min"] = rec["value_max"] = rec["value_median"] = None
    # loose plausibility range
    n_oor = 0
    if meta and len(good):
        lo, hi = meta[3]
        n_oor = int(((good < lo) | (good > hi)).sum())
    rec["n_out_of_range"] = n_oor

    # approval split (provisional vs approved)
    appr = Counter(df["approval_status"]) if "approval_status" in df else Counter()
    rec["approval_counts"] = dict(appr)
    rec["pct_provisional"] = round(100.0 * appr.get(nw.APPROVAL_PROVISIONAL, 0) / len(df), 2)

    # qualifiers present
    quals = Counter()
    if "qualifier" in df:
        for q in df["qualifier"]:
            for tok in str(q).split("|"):
                if tok:
                    quals[tok] += 1
    rec["qualifiers"] = dict(quals)

    # dates / duplicates / staleness
    times = df["time"].astype(str)
    rec["date_min"], rec["date_max"] = times.min(), times.max()
    rec["n_duplicate_timestamps"] = int(len(times) - times.nunique())
    # NB: computed from the PULLED file's latest obs, so it reflects the pulled window — NOT live
    # catalog activity. A historical pull ending 2024 is "not recent" even if the series is active
    # today; for live activity, read `end` from the catalog (time-series-metadata) instead.
    rec["recent_in_pulled_window"] = (
        (rec["date_max"][:10] >= _minus_days(today, 60)) if rec["date_max"] else None)

    # flags
    flags = []
    if rec.get("sha256_ok") is False:
        flags.append("sha256 mismatch vs manifest")
    if rec.get("sha256_ok") is None:
        flags.append("not in download manifest (traceability gap)")
    if not rec["parameter_known"]:
        flags.append(f"unknown parameter code {pcode}")
    if len(units) > 1:
        flags.append(f"multiple units in one series: {units}")
    if rec["n_nonnumeric"]:
        flags.append(f"{rec['n_nonnumeric']} non-numeric value(s)")
    if n_oor:
        flags.append(f"{n_oor} value(s) outside plausible range {meta[3]}")
    if rec["n_duplicate_timestamps"]:
        flags.append(f"{rec['n_duplicate_timestamps']} duplicate timestamp(s)")
    rec["flags"] = flags
    return rec


def _minus_days(today: str, days: int) -> str:
    from datetime import date, timedelta
    y, m, d = (int(x) for x in today[:10].split("-"))
    return (date(y, m, d) - timedelta(days=days)).isoformat()


def qa_sites(raw: Path) -> dict:
    out = {"files": []}
    for csv in sorted((raw / "sites").glob("*_sites.csv")):
        df = pd.read_csv(csv, dtype=str, keep_default_na=False)
        info = {
            "filename": csv.name, "n_sites": int(len(df)),
            "by_site_type": dict(Counter(df["site_type_code"])) if "site_type_code" in df else {},
            "n_missing_latlon": int(((df.get("latitude", "") == "") |
                                     (df.get("longitude", "") == "")).sum()) if len(df) else 0,
            "n_missing_huc": int((df.get("huc", "") == "").sum()) if "huc" in df else None,
            "n_non_usgs_agency": int((df.get("agency_code", "USGS") != "USGS").sum())
                                 if "agency_code" in df else None,
        }
        out["files"].append(info)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", default=str(_DEFAULT_RAW))
    ap.add_argument("--outdir", default=str(_DEFAULT_OUT))
    ap.add_argument("--today", default=None)
    args = ap.parse_args(argv)

    raw, out = Path(args.raw), Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    today = args.today or __import__("time").strftime("%Y-%m-%d", __import__("time").gmtime())

    manifest = net.read_manifest(raw / "manifest.jsonl")
    manifest_by_name = {m["filename"]: m for m in manifest if "filename" in m}

    per_series = []
    for service in ("daily", "continuous"):
        for csv in sorted((raw / service).glob("*.csv")):
            try:
                per_series.append(qa_series(csv, service, manifest_by_name, today))
            except Exception as e:
                per_series.append({"filename": csv.name, "service": service,
                                   "error": repr(e), "flags": ["QA ERROR"]})

    if not per_series:
        print(f"[qa] no series CSVs under {raw}/(daily|continuous). Pull data first "
              f"(access/pull_nwis.py).", file=sys.stderr)

    # cross-cuts
    by_param = {}
    for r in per_series:
        p = r.get("parameter_code")
        if not p:
            continue
        b = by_param.setdefault(p, {"name": r.get("parameter_name"), "n_series": 0, "n_rows": 0})
        b["n_series"] += 1
        b["n_rows"] += r.get("n_rows", 0)

    summary = {
        "generated_utc": net._utc_now_iso(),
        "today": today,
        "raw_dir": str(raw),
        "n_series": len(per_series),
        "n_series_with_flags": sum(1 for r in per_series if r.get("flags")),
        "sites": qa_sites(raw),
        "by_parameter": by_param,
        "per_series": per_series,
    }
    (out / "qa_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    _write_markdown(summary, out / "qa_report.md")
    print(f"[qa] wrote {out/'qa_summary.json'} and {out/'qa_report.md'}")
    print(f"[qa] {summary['n_series_with_flags']}/{summary['n_series']} series carry QA flags")
    return 0


def _write_markdown(s: dict, path: Path) -> None:
    L = ["# NWIS in-situ series — QA/QC report\n",
         f"*Generated {s['generated_utc']} · today={s['today']} · {s['n_series']} series from "
         f"`{s['raw_dir']}`*\n",
         f"**{s['n_series_with_flags']} of {s['n_series']} series carry QA flags.**\n"]

    L.append("\n## Site tables\n")
    L.append("| File | Sites | By type | Missing lat/lon | Missing HUC | Non-USGS agency |")
    L.append("|------|-------|---------|-----------------|-------------|-----------------|")
    for f in s["sites"]["files"]:
        L.append(f"| {f['filename']} | {f['n_sites']} | {f['by_site_type']} | "
                 f"{f['n_missing_latlon']} | {f['n_missing_huc']} | {f['n_non_usgs_agency']} |")

    L.append("\n## By parameter\n")
    L.append("| Parameter | Name | Series | Rows |")
    L.append("|-----------|------|--------|------|")
    for p, b in sorted(s["by_parameter"].items()):
        L.append(f"| {p} | {b['name']} | {b['n_series']} | {b['n_rows']:,} |")

    L.append("\n## Per-series\n")
    L.append("| Series | Svc | Param | Rows | Dates | Value min/med/max | %prov | Qualifiers | Flags |")
    L.append("|--------|-----|-------|------|-------|-------------------|-------|------------|-------|")
    for r in s["per_series"]:
        if "error" in r:
            L.append(f"| {r['filename']} | {r.get('service','')} | | | | | | | ERROR: {r['error']} |")
            continue
        vm = "—" if r.get("value_min") is None else \
            f"{r['value_min']:.3g}/{r['value_median']:.3g}/{r['value_max']:.3g}"
        dates = f"{r.get('date_min','?')[:10]}→{r.get('date_max','?')[:10]}"
        quals = ",".join(r.get("qualifiers", {}).keys()) or "—"
        flags = "; ".join(r.get("flags", [])) or "ok"
        L.append(f"| {r['filename'][:34]} | {r['service'][:4]} | {r.get('parameter_code','?')} "
                 f"| {r.get('n_rows',0):,} | {dates} | {vm} | {r.get('pct_provisional','?')} "
                 f"| {quals} | {flags} |")

    L.append("\n## Notes\n")
    L.append("- **Provisional** data are subject to revision; **Approved** data are final "
             "(but can still change on reprocessing — track `last_modified`). See METADATA.md §4/§5.")
    L.append("- Plausibility ranges are LOOSE encoding-sanity bounds, not scientific limits.")
    L.append("- `recent_in_pulled_window` = latest obs in the *pulled file* is within 60 d of "
             "`today` — it reflects the pulled date window, **not** live catalog activity (for that, "
             "read `end` from time-series-metadata).")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
