#!/usr/bin/env python
"""Acquire USGS NWIS in-situ series for an area of interest, via the Water Data OGC API.

Reproducible, cached, and auditable (mirrors the CyAN acquisition discipline):
  1. **Enumerate** monitoring locations for an AOI (HUC / bbox / state / county / site-type /
     explicit ids) — auth-free and cheap. Writes a site-metadata CSV (geotagging + HUC + FIPS).
  2. **Catalog** each site's time-series (period of record + Daily/Points computation) and plan
     only the series that actually exist for the requested parameters — no empty pulls, and the
     plan itself reports which features exist where and whether they're active/stale.
  3. **Download** each planned series (daily and/or continuous) over the date window, cached to
     ``data/raw/<service>/`` as a tidy CSV (row-per-observation — no aggregation), with sha256 +
     a JSONL manifest recording query, counts, date span, provisional/approved split, the OGC
     service build version, and access time. Any figure/metric later traces to these bytes.

Auth is OPTIONAL — the OGC API is public. A free API key (``NWIS_API_KEY`` in ``../.env``) only
raises rate limits; it is sent as the ``X-Api-Key`` header. ``--dry-run`` never downloads data.

Examples
--------
# Plan only (no data pull): what daily series exist for HAB params in one HUC-8?
python pull_nwis.py --huc 02070008 --service daily --dry-run

# Pull daily mean series for two named sites, 2015->present:
python pull_nwis.py --sites USGS-01646500 USGS-01656000 --service daily \
    --start 2015-01-01 --params 00060 00010 00095

# Pull continuous (real-time) data in a bbox, capped to 5 sites for a sample:
python pull_nwis.py --bbox -83.8 41.2 -81.5 43.0 --service continuous --limit 5 --start 2026-06-01
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

# requests.Session is not a safe concurrency boundary, so give each worker thread its own.
_thread_local = threading.local()


def _worker_session():
    s = getattr(_thread_local, "session", None)
    if s is None:
        s = nw.make_nwis_session()
        _thread_local.session = s
    return s

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from _common import net                       # noqa: E402
from NWIS.access import nwis_api as nw         # noqa: E402

_NWIS_DIR = _DATA_SOURCES / "NWIS"
_DEFAULT_RAW = _NWIS_DIR / "data" / "raw"
_DOTENV = _DATA_SOURCES / ".env"

# Column order for the tidy per-series CSVs (kept stable for reproducible sha256).
_SERIES_COLS = ["monitoring_location_id", "parameter_code", "statistic_id", "time",
                "value", "unit_of_measure", "approval_status", "qualifier",
                "last_modified", "time_series_id"]


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def _aoi_tag(args) -> str:
    if args.sites:
        return "sites_" + "_".join(s.replace("USGS-", "") for s in args.sites)[:40]
    if args.huc:
        return f"huc_{args.huc}"
    if args.state:
        return f"state_{args.state}"
    if args.bbox:
        return "bbox_" + "_".join(str(x) for x in args.bbox)
    return "aoi"


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    # --- AOI (at least one required, unless --sites) ---
    p.add_argument("--sites", nargs="+", help="explicit ids, e.g. USGS-01646500 (or bare 01646500)")
    p.add_argument("--huc", help="HUC prefix (HUC-8 matches its HUC-12 children), e.g. 02070008")
    p.add_argument("--bbox", nargs=4, type=float, metavar=("MINLON", "MINLAT", "MAXLON", "MAXLAT"))
    p.add_argument("--state", help="state FIPS code, e.g. 24 (Maryland)")
    p.add_argument("--county", help="county FIPS code (use with --state)")
    p.add_argument("--site-types", help="comma-joined site-type codes, e.g. ST,LK")
    # --- what to pull ---
    p.add_argument("--service", default="daily", choices=["daily", "continuous"],
                   help="daily = DV statistic values (modeling core); continuous = real-time IV")
    p.add_argument("--params", nargs="+", default=list(nw.HAB_PARAMETERS),
                   help=f"parameter codes (default: HAB set {list(nw.HAB_PARAMETERS)})")
    p.add_argument("--stats", nargs="+", default=[nw.DEFAULT_STAT],
                   help="daily statistic codes to keep (default mean 00003); ignored for continuous")
    p.add_argument("--start", default=None, help="start date YYYY-MM-DD (default: series start)")
    p.add_argument("--end", default=None, help="end date YYYY-MM-DD (default: latest)")
    p.add_argument("--active-only", action="store_true",
                   help="skip series whose period-of-record end is > --active-days old")
    p.add_argument("--active-days", type=int, default=60)
    p.add_argument("--today", default=None, help="reference 'today' YYYY-MM-DD for staleness "
                                                 "(default: derived from system clock)")
    # --- run controls ---
    p.add_argument("--outdir", default=str(_DEFAULT_RAW))
    p.add_argument("--manifest", default=None)
    p.add_argument("--limit", type=int, default=0,
                   help="explicitly cap number of SITES to sample (0 = no cap); opts past --max-sites")
    p.add_argument("--max-sites", type=int, default=300,
                   help="safety guard: refuse to fan out per-site catalog requests to more than this "
                        "many sites unless --limit is set. NWIS HUC/bbox AOIs include ALL site types "
                        "(often 1000s of groundwater wells) — narrow with --site-types ST,LK,SP.")
    p.add_argument("--page-size", type=int, default=20000, help="OGC page size (verified up to 20000)")
    p.add_argument("--workers", type=int, default=4,
                   help="concurrent request workers for the per-site catalog + per-series pulls "
                        "(network-bound). Keep modest to respect the keyless 1000/hr limit.")
    p.add_argument("--refresh", action="store_true", help="re-pull even if a cached CSV exists")
    p.add_argument("--allow-partial", action="store_true",
                   help="exit 0 even if some sites failed to catalog (default: exit nonzero so an "
                        "incomplete AOI plan is not mistaken for a complete pull)")
    p.add_argument("--dry-run", action="store_true", help="enumerate + plan only; no data pull")
    return p.parse_args(argv)


def _today_str(args) -> str:
    if args.today:
        return args.today
    import time
    return time.strftime("%Y-%m-%d", time.gmtime())


def main(argv=None) -> int:
    try:                       # force UTF-8 console so stray unicode never crashes a pull
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        return _run(parse_args(argv))
    except nw.RateLimitError as e:
        print(f"[rate-limit] {e}", file=sys.stderr)
        return 3


def _run(args) -> int:
    if not any([args.sites, args.huc, args.bbox, args.state]):
        print("[error] need an AOI: one of --sites / --huc / --bbox / --state.", file=sys.stderr)
        return 2

    outdir = Path(args.outdir)
    manifest = Path(args.manifest) if args.manifest else outdir / "manifest.jsonl"
    session = nw.make_nwis_session()          # retries 5xx only; 429 -> clear RateLimitError
    api_key = nw.resolve_api_key(_DOTENV)
    build = nw.get_response_build_version(session, api_key)
    today = _today_str(args)
    print(f"[api] OGC build {build or '?'} |api_key={'yes' if api_key else 'no (keyless)'} |today={today}")

    # --- 1. enumerate sites -------------------------------------------------- #
    print(f"[enumerate] AOI={_aoi_tag(args)}  service={args.service}  params={args.params}")
    sites = nw.enumerate_sites(
        session,
        huc=args.huc, bbox=args.bbox, state_code=args.state, county_code=args.county,
        site_type_code=args.site_types,
        site_ids=[nw.to_wqp_id(s) for s in args.sites] if args.sites else None,
        api_key=api_key, page_size=args.page_size,
        max_sites=args.limit if args.limit else 0,
    )
    print(f"[enumerate] {len(sites)} monitoring location(s)")
    if not sites:
        print("[enumerate] no sites for this AOI — nothing to do.", file=sys.stderr)
        return 0
    types = pd.Series([s.site_type_code for s in sites]).value_counts()
    print("[enumerate] by site type: " + ", ".join(f"{k}={v}" for k, v in types.items()))

    # write site metadata CSV (geotagging table)
    sites_dir = outdir / "sites"
    sites_dir.mkdir(parents=True, exist_ok=True)
    sites_csv = sites_dir / f"{_aoi_tag(args)}_sites.csv"
    sdf = pd.DataFrame([{
        "id": s.id, "agency_code": s.agency_code, "site_no": s.site_no, "name": s.name,
        "latitude": s.latitude, "longitude": s.longitude, "huc": s.huc, "huc8": s.huc8,
        "state_code": s.state_code, "county_code": s.county_code,
        "site_type_code": s.site_type_code, "site_type": s.site_type,
        "drainage_area": s.drainage_area, "altitude": s.altitude,
        "horizontal_datum": s.horizontal_datum, "vertical_datum": s.vertical_datum,
        "wqp_id": s.wqp_id,
    } for s in sites])
    sdf.to_csv(sites_csv, index=False)
    print(f"[enumerate] wrote {sites_csv}  ({len(sdf)} rows)")

    # Safety guard: a HUC-8/bbox AOI returns ALL site types (often >1000 groundwater wells).
    # Cataloguing every site is slow and blows the keyless 1000/hr budget. Refuse loudly rather
    # than silently fan out — the user narrows the AOI or opts in with --limit.
    if not args.limit and len(sites) > args.max_sites:
        print(f"[stop] AOI returned {len(sites)} sites (> --max-sites={args.max_sites}). NWIS "
              f"HUC/bbox queries include every site type, incl. many groundwater wells. Narrow "
              f"with --site-types (e.g. 'ST,LK,SP' for surface water), use a smaller AOI, or "
              f"opt in with --limit N / raise --max-sites. (The site table above was still "
              f"written to {sites_csv}.)", file=sys.stderr)
        return 2

    # --- 2. catalog + plan --------------------------------------------------- #
    # Deduped by (site_id, parameter_code, statistic_id): fetch_series pulls by that key
    # (not by time_series_id), so several catalog time-series that share the key (e.g. a
    # water-temp sensor swapped over the years) collapse to ONE pull. Merge their spans.
    want_params = set(args.params)
    want_stats = set(args.stats)
    want_service = nw.COLL_DAILY if args.service == "daily" else nw.COLL_CONTINUOUS

    # We catalog per enumerated site (concurrently — it's network-bound). NOTE: the
    # `time-series-metadata` collection DOES accept AOI filters server-side
    # (`hydrologic_unit_code`, `state_name`, `parameter_code`, `monitoring_location_id` —
    # verified 2026-07-02); we still go per-site because the site set is already narrowed by
    # enumeration + the --max-sites guard, so per-site is targeted and uniform across AOI types
    # (HUC/bbox/state/ids). An AOI-wide catalog query is the better path only when pulling
    # (nearly) all sites in a HUC — see METADATA §7.2 for that alternative.
    def _catalog_one(s):
        try:
            return s, nw.catalog_series(_worker_session(), s.id, parameter_codes=want_params,
                                        api_key=api_key), None
        except Exception as e:
            return s, None, e

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        cat_results = list(ex.map(_catalog_one, sites))
    rl = next((e for _, _, e in cat_results if isinstance(e, nw.RateLimitError)), None)
    if rl:
        raise rl

    plan_by_key: dict[tuple, dict] = {}
    catalog_failed: list[str] = []
    for s, cat, err in cat_results:
        if err is not None:
            catalog_failed.append(s.id)
            print(f"  [catalog] {s.id}: FAILED {err}", file=sys.stderr)
            continue
        for ser in cat:
            if nw.series_service(ser) != want_service:
                continue
            stat = ser.get("statistic_id")
            if args.service == "daily" and want_stats and stat not in want_stats:
                continue
            active = nw.series_is_active(ser, today, args.active_days)
            if args.active_only and active is False:
                continue
            key = (s.id, ser.get("parameter_code"), stat)
            begin, end = (ser.get("begin") or "")[:10], (ser.get("end") or "")[:10]
            cur = plan_by_key.get(key)
            if cur is None:
                plan_by_key[key] = {
                    "site_id": s.id, "parameter_code": ser.get("parameter_code"),
                    "statistic_id": stat, "begin": begin, "end": end, "active": bool(active),
                    "param_name": ser.get("parameter_name"), "n_timeseries": 1}
            else:  # merge span across co-keyed time-series
                cur["begin"] = min(x for x in (cur["begin"], begin) if x) or cur["begin"]
                cur["end"] = max(cur["end"], end)
                cur["active"] = cur["active"] or bool(active)
                cur["n_timeseries"] += 1
    plan = list(plan_by_key.values())

    print(f"[plan] {len(plan)} series to pull ({args.service}) across {len(sites)} site(s)")
    if args.dry_run:
        for pl in plan[:200]:
            act = {True: "active", False: "STALE", None: "?"}[pl["active"]]
            print(f"  {pl['site_id']:22s} {pl['parameter_code']} "
                  f"{pl['statistic_id'] or '   '} {pl['begin']}->{pl['end']} {act:6s} {pl['param_name']}")
        if len(plan) > 200:
            print(f"  … and {len(plan) - 200} more")
        print(f"[dry-run] {len(plan)} series would be pulled to {outdir}/{args.service}/")
        return 0

    # --- 3. download each series (parallel fetch, serial write) -------------- #
    prior = {r["filename"]: r for r in net.read_manifest(manifest) if r.get("filename")}
    series_dir = outdir / args.service
    series_dir.mkdir(parents=True, exist_ok=True)

    def _fname(pl):
        stat_tag = f"__{pl['statistic_id']}" if pl["statistic_id"] else ""
        return f"{pl['site_id']}__{pl['parameter_code']}{stat_tag}.csv"

    to_fetch = [pl for pl in plan if args.refresh or not (series_dir / _fname(pl)).exists()]
    cached = len(plan) - len(to_fetch)
    if cached:
        print(f"[download] {cached} series already cached (use --refresh to re-pull)")

    def _fetch_one(pl):
        try:
            return pl, nw.fetch_series(
                _worker_session(), args.service, pl["site_id"], pl["parameter_code"],
                statistic_id=pl["statistic_id"], start=args.start, end=args.end,
                api_key=api_key, page_size=args.page_size), None
        except Exception as e:
            return pl, None, e

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        fetched = list(ex.map(_fetch_one, to_fetch))
    rl = next((e for _, _, e in fetched if isinstance(e, nw.RateLimitError)), None)
    if rl:
        raise rl

    pulled = empty = failed = 0
    for i, (pl, recs, err) in enumerate(fetched, 1):
        fname = _fname(pl)
        if err is not None:
            failed += 1
            print(f"  [{i}/{len(fetched)}] FAILED {fname}: {err}", file=sys.stderr)
            continue
        if not recs:
            empty += 1
            # Record the empty outcome too (reproducibility: the query ran, 0 rows in window).
            net.append_manifest(manifest, {
                "kind": "series_empty", "filename": fname,
                "service": args.service, "site_id": pl["site_id"],
                "parameter_code": pl["parameter_code"], "statistic_id": pl["statistic_id"],
                "n_rows": 0, "requested_start": args.start, "requested_end": args.end,
                "ogc_build_version": build, "accessed_utc": net._utc_now_iso(),
            })
            print(f"  [{i}/{len(fetched)}] empty  {fname} (no observations in window)")
            continue
        df = pd.DataFrame(recs)
        # qualifier is a list -> join for CSV; keep every observation (no aggregation).
        if "qualifier" in df.columns:
            df["qualifier"] = df["qualifier"].apply(
                lambda q: "|".join(q) if isinstance(q, list) else (q or ""))
        for c in _SERIES_COLS:
            if c not in df.columns:
                df[c] = None
        df = df[_SERIES_COLS].sort_values("time")
        dest = series_dir / fname
        df.to_csv(dest, index=False)
        sha = _sha256(dest)
        appr = df["approval_status"].value_counts(dropna=False).to_dict()
        record = {
            "kind": "series", "filename": fname, "path": str(dest),
            "sha256": sha, "bytes": dest.stat().st_size,
            "service": args.service, "site_id": pl["site_id"],
            "parameter_code": pl["parameter_code"], "statistic_id": pl["statistic_id"],
            "n_rows": int(len(df)),
            "date_min": str(df["time"].min()), "date_max": str(df["time"].max()),
            "n_provisional": int(appr.get(nw.APPROVAL_PROVISIONAL, 0)),
            "n_approved": int(appr.get(nw.APPROVAL_APPROVED, 0)),
            "last_modified_max": str(df["last_modified"].max()),
            "requested_start": args.start, "requested_end": args.end,
            "ogc_build_version": build, "accessed_utc": net._utc_now_iso(),
        }
        if not prior.get(fname) or prior[fname].get("sha256") != sha:
            net.append_manifest(manifest, record)
        pulled += 1
        print(f"  [{i}/{len(fetched)}] pulled {fname} ({len(df):,} rows, "
              f"{record['date_min']}->{record['date_max']}, {record['n_provisional']} provisional)")

    if catalog_failed:
        print(f"[warn] {len(catalog_failed)} site(s) failed to catalog and were EXCLUDED from the "
              f"plan (incomplete AOI): {', '.join(catalog_failed[:10])}"
              f"{' …' if len(catalog_failed) > 10 else ''}. Re-run (optionally --refresh), or pass "
              f"--allow-partial to accept an incomplete pull.", file=sys.stderr)
    print(f"[done] pulled={pulled} cached={cached} empty={empty} failed={failed} "
          f"catalog_failed={len(catalog_failed)} total_planned={len(plan)} |manifest={manifest}")
    # Non-zero on any fetch failure OR silently-dropped catalog sites (unless explicitly allowed).
    incomplete = bool(catalog_failed) and not args.allow_partial
    return 1 if (failed or incomplete) else 0


if __name__ == "__main__":
    raise SystemExit(main())
