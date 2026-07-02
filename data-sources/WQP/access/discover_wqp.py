#!/usr/bin/env python
"""Discovery-first step for the Water Quality Portal (no auth required).

Answers "what HAB-relevant data exists here, and how fresh is it?" BEFORE we commit to
pulling results — so the characteristic set is chosen from real availability, not guessed
(the DISCOVERY-FIRST decision; METADATA §7.2).

It runs the two-part discovery the WQX3 404 forces on us:
  1. BROAD availability + recency via the **legacy** Summary service (periodOfRecord) —
     per site x year x characteristic counts + last-submitted dates. (Legacy omits USGS
     data added/modified after 2024-03-11.)
  2. POST-SPLIT USGS freshness via a bounded **legacy vs WQX3** Result count over the same
     scope — shows how much recent USGS data is visible ONLY in WQX3.

Outputs (tracked, small): outputs/discovery_report.md + outputs/discovery_hab_availability.csv.
The native per-site x year x characteristic Summary CSV is cached under data/raw/ (gitignored,
regenerates) and is the source of truth; the roll-ups here are AVAILABILITY COUNTS (inventory),
never aggregated measurement values.

Examples
--------
# Plan only (print the URLs it would hit, no fetch):
python discover_wqp.py --countycode US:39:095 --dry-run

# Run discovery for the western Lake Erie start scope (Lucas County OH):
python discover_wqp.py --countycode US:39:095

# Widen scope (Maumee HUC8, or a bbox, or a whole state):
python discover_wqp.py --huc 04100009
python discover_wqp.py --statecode US:39 --summary-years 10
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from _common import net                       # noqa: E402
from WQP.access import wqp_api as w            # noqa: E402

_WQP_DIR = _DATA_SOURCES / "WQP"
_RAW = _WQP_DIR / "data" / "raw"
_MANIFEST = _RAW / "manifest.jsonl"
_OUT = _WQP_DIR / "outputs"

# The 2024-03-11 USGS split: data collected/modified AFTER this date is WQX3-only.
DEFAULT_SPLIT_DATE = "2024-03-12"


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_argument_group("scope (pick one or more; combined by the API)")
    g.add_argument("--bbox", nargs=4, type=float, metavar=("W", "S", "E", "N"),
                   help="west south east north (WGS84 decimal degrees)")
    g.add_argument("--statecode", help="e.g. US:39 (Ohio)")
    g.add_argument("--countycode", help="e.g. US:39:095 (Lucas County OH)")
    g.add_argument("--huc", help="8-digit HUC(s), ';'-delimited, e.g. 04100009")
    g.add_argument("--siteid", help="e.g. USGS-04193500")
    p.add_argument("--summary-years", type=int, default=5,
                   help="periodOfRecord look-back for the Summary service (default 5)")
    p.add_argument("--split-date", default=DEFAULT_SPLIT_DATE,
                   help=f"post-split freshness cutoff (default {DEFAULT_SPLIT_DATE})")
    p.add_argument("--no-wqx3", action="store_true",
                   help="skip the WQX3 post-split freshness probe")
    p.add_argument("--dry-run", action="store_true", help="print planned URLs, do not fetch")
    p.add_argument("--outdir", default=str(_OUT))
    return p.parse_args(argv)


def scope_params(args) -> tuple[dict, str]:
    """Build the spatial-scope param dict + a short label for filenames/report."""
    s: dict = {}
    label_bits = []
    if args.bbox:
        s["bBox"] = ",".join(str(x) for x in args.bbox)
        label_bits.append("bbox")
    if args.statecode:
        s["statecode"] = args.statecode
        label_bits.append(args.statecode.replace(":", ""))
    if args.countycode:
        s["countycode"] = args.countycode
        label_bits.append(args.countycode.replace(":", ""))
    if args.huc:
        s["huc"] = args.huc
        label_bits.append(f"huc{args.huc.split(';')[0]}")
    if args.siteid:
        s["siteid"] = args.siteid
        label_bits.append(args.siteid.replace(":", ""))
    if not s:
        raise SystemExit("Provide a scope: --bbox / --statecode / --countycode / --huc / --siteid")
    return s, "_".join(label_bits) or "scope"


def _result_count(session, scope: dict, schema: str, split_date: str,
                  fetch_dir: Path) -> tuple[int, str]:
    """Count post-split USGS Result rows for a scope in one schema.

    Legacy: cheap Total-Result-Count header. WQX3: no count header -> fetch the (bounded)
    narrow CSV and count data rows. Returns (count, how) where how in {'header','rowcount'}.
    """
    # No characteristicName filter: count ALL post-split USGS results (any characteristic).
    # Filtering here is both unnecessary for the freshness question and a 400 risk (an
    # unrecognized name would fail the whole query).
    params = dict(scope)
    params["startDateLo"] = split_date
    params["providers"] = "NWIS"                 # USGS specifically (the split's subject)
    if schema == "legacy":
        url = w.build_query_url("Result", params, schema="legacy")
        counts = w.count_headers(session, url)
        return int(counts.get("result", 0)), "header"
    url = w.build_query_url("Result", params, schema="wqx3", dataProfile="narrow")
    dest = w.query_dest(fetch_dir, "Result", "wqx3", url)
    res = w.fetch_csv_to_cache(session, url, dest, _MANIFEST, endpoint="Result", schema="wqx3")
    n = max(0, sum(1 for _ in Path(res.path).open(encoding="utf-8", errors="replace")) - 1)
    return n, "rowcount"


def run(args) -> int:
    scope, label = scope_params(args)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    summary_params = dict(scope)
    summary_params["dataProfile"] = "periodOfRecord"
    summary_params["summaryYears"] = args.summary_years
    summary_url = w.build_query_url("summary", summary_params, schema="legacy")

    if args.dry_run:
        print("[dry-run] would fetch legacy Summary:\n  " + summary_url)
        if not args.no_wqx3:
            for schema in ("legacy", "wqx3"):
                pp = dict(scope, startDateLo=args.split_date, providers="NWIS")
                extra = {} if schema == "legacy" else {"dataProfile": "narrow"}
                print(f"[dry-run] would count post-split USGS Results ({schema}):\n  "
                      + w.build_query_url("Result", pp, schema=schema, **extra))
        return 0

    session = net.make_session()
    print(f"Discovery scope: {scope}  (label={label})")
    print("Fetching legacy Summary (periodOfRecord) ...")
    dest = w.query_dest(_RAW, "summary", "legacy", summary_url)
    res = w.fetch_csv_to_cache(session, summary_url, dest, _MANIFEST,
                               endpoint="summary", schema="legacy")
    df = pd.read_csv(res.path, dtype=str, low_memory=False)
    for col in ("ActivityCount", "ResultCount", "YearSummarized"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # object-dtype text columns: NaN -> "" so string max()/join don't hit mixed types.
    for col in ("LastResultSubmittedDate", "Provider", "ResolvedMonitoringLocationTypeName"):
        if col in df.columns:
            df[col] = df[col].fillna("")

    n_rows = len(df)
    n_sites = df["MonitoringLocationIdentifier"].nunique() if n_rows else 0
    n_chars = df["CharacteristicName"].nunique() if n_rows else 0

    # HAB-relevant availability inventory (COUNTS, not measured values).
    hab_lc = {c.lower() for c in w.HAB_CHARACTERISTICS}
    # Keep keywords specific: bare "ph" false-matches "biPHenyl" (PCBs). "pH" itself is
    # covered by the exact-match set (hab_lc) below.
    hab_keywords = ("chlorophyll", "microcystin", "cyano", "phosph", "nitrogen",
                    "nitrate", "nitrite", "ammoni", "temperature", "oxygen",
                    "turbid", "secchi")
    def is_hab(name: str) -> bool:
        nl = str(name).lower()
        return nl in hab_lc or any(k in nl for k in hab_keywords)

    hab_avail = pd.DataFrame()
    if n_rows:
        hab = df[df["CharacteristicName"].map(is_hab)].copy()
        if len(hab):
            hab_avail = (hab.groupby("CharacteristicName")
                         .agg(sites=("MonitoringLocationIdentifier", "nunique"),
                              results=("ResultCount", "sum"),
                              latest_year=("YearSummarized", "max"),
                              last_submitted=("LastResultSubmittedDate", "max"),
                              providers=("Provider", lambda s: ",".join(sorted(set(s.dropna())))))
                         .reset_index()
                         .sort_values(["sites", "results"], ascending=False))
        hab_csv = outdir / "discovery_hab_availability.csv"
        hab_avail.to_csv(hab_csv, index=False)

    # provider + site-type inventory
    prov = (df.groupby("Provider")["MonitoringLocationIdentifier"].nunique()
            if n_rows else pd.Series(dtype=int))
    stype_col = "ResolvedMonitoringLocationTypeName"
    stype = (df.groupby(stype_col)["MonitoringLocationIdentifier"].nunique()
             if n_rows and stype_col in df.columns else pd.Series(dtype=int))

    # WQX3 post-split USGS freshness probe (bounded)
    freshness = None
    if not args.no_wqx3:
        print("Probing post-split USGS freshness (legacy vs WQX3) ...")
        try:
            leg_n, leg_how = _result_count(session, scope, "legacy", args.split_date, _RAW)
            wqx_n, wqx_how = _result_count(session, scope, "wqx3", args.split_date, _RAW)
            freshness = {"split_date": args.split_date,
                         "legacy": (leg_n, leg_how), "wqx3": (wqx_n, wqx_how)}
        except Exception as e:  # noqa: BLE001 — report, don't crash discovery
            freshness = {"error": f"{type(e).__name__}: {e}"}

    report = _render_report(scope, label, res, df, n_rows, n_sites, n_chars,
                            hab_avail, prov, stype, freshness, args)
    report_path = outdir / "discovery_report.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"\n{n_sites} sites, {n_chars} characteristics, {n_rows} summary rows.")
    if len(hab_avail):
        print("Top HAB-relevant characteristics by site coverage:")
        print(hab_avail.head(10).to_string(index=False))
    if freshness and "error" not in freshness:
        print(f"\nPost-split USGS Results (since {freshness['split_date']}): "
              f"legacy={freshness['legacy'][0]}  wqx3={freshness['wqx3'][0]}")
    print(f"\nWrote: {report_path}")
    if len(hab_avail):
        print(f"Wrote: {outdir / 'discovery_hab_availability.csv'}")
    return 0


def _render_report(scope, label, res, df, n_rows, n_sites, n_chars,
                   hab_avail, prov, stype, freshness, args) -> str:
    lines = [
        f"# WQP discovery — {label}",
        "",
        f"- **Scope:** `{scope}`",
        f"- **Legacy Summary (periodOfRecord), summaryYears={args.summary_years}** — "
        f"source-provided per site×year×characteristic inventory (NOT our aggregation).",
        f"- **Cached source of truth:** `{Path(res.path).relative_to(_DATA_SOURCES)}` "
        f"(sha256 `{res.sha256[:12]}…`, {res.bytes:,} bytes, accessed {res.accessed_utc}).",
        f"- **Inventory:** {n_sites:,} monitoring locations · {n_chars:,} distinct "
        f"characteristics · {n_rows:,} summary rows.",
        "",
        "> ⚠ Legacy Summary omits USGS data added/modified after 2024-03-11. See the "
        "freshness probe below for what WQX3 adds.",
        "",
        "## HAB-relevant availability (counts, not values)",
    ]
    if len(hab_avail):
        lines.append("")
        lines.append("| Characteristic | Sites | Results | Latest yr | Last submitted | Providers |")
        lines.append("|---|--:|--:|--:|---|---|")
        for _, r in hab_avail.head(25).iterrows():
            results = int(r["results"]) if pd.notna(r["results"]) else 0
            yr = int(r["latest_year"]) if pd.notna(r["latest_year"]) else "—"
            lines.append(f"| {r['CharacteristicName']} | {int(r['sites'])} | {results} | "
                         f"{yr} | {r['last_submitted'] or '—'} | {r['providers']} |")
    else:
        lines.append("\n_No HAB-relevant characteristics found in this scope._")

    lines += ["", "## Provider inventory (distinct sites)", ""]
    for name, cnt in prov.sort_values(ascending=False).items():
        lines.append(f"- **{name}**: {int(cnt):,}")
    lines += ["", "## Site-type inventory (distinct sites)", ""]
    for name, cnt in stype.sort_values(ascending=False).head(12).items():
        lines.append(f"- {name}: {int(cnt):,}")

    lines += ["", "## Post-2024-03-11 USGS freshness (legacy vs WQX3)", ""]
    if freshness is None:
        lines.append("_Skipped (--no-wqx3)._")
    elif "error" in freshness:
        lines.append(f"_Probe failed: {freshness['error']}_")
    else:
        leg_n, leg_how = freshness["legacy"]
        wqx_n, wqx_how = freshness["wqx3"]
        lines += [
            f"Bounded probe: USGS (`providers=NWIS`) Results (any characteristic) with "
            f"`startDateLo={freshness['split_date']}`, this scope.",
            "",
            f"- **legacy WQX 2.2:** {leg_n} results (via {leg_how})",
            f"- **WQX 3.0 beta:** {wqx_n} results (via {wqx_how})",
            "",
            "If WQX3 > legacy, that gap is recent USGS data reachable **only** via WQX3 "
            "— the operational reason to prefer WQX3 for USGS (METADATA §2, §10).",
        ]
    lines += ["", "---", "*Regenerate: "
              "`python data-sources/WQP/access/discover_wqp.py " +
              " ".join(f"--{k} {v}" for k, v in _scope_flags(args)) + "`*", ""]
    return "\n".join(lines)


def _scope_flags(args):
    for k in ("bbox", "statecode", "countycode", "huc", "siteid"):
        v = getattr(args, k, None)
        if v:
            yield k, (" ".join(map(str, v)) if isinstance(v, list) else v)


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
