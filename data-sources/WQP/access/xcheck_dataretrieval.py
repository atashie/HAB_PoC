#!/usr/bin/env python
"""Cross-validate our raw-REST WQP client against the official USGS `dataretrieval` package.

This is the HYBRID decision's cross-check leg (METADATA §7.4): `dataretrieval` is NOT a
second canonical ingestion path (Codex #13) — it is an independent second implementation we
use to confirm our own `wqp_api` returns the same sites/results for the same query. If the
two disagree, that is a bug (or an upstream change) we want to catch early.

For a bounded scope + one VALID characteristic, it compares, per schema:
  * site count   — our legacy `Total-Site-Count` header  vs  dataretrieval `what_sites`
  * result count — our legacy `Total-Result-Count` header vs dataretrieval `get_results`
(WQX3 has no count headers, so there we compare dataretrieval to our own row counts.)

Writes outputs/xcheck_report.md.

Example:
    python xcheck_dataretrieval.py --countycode US:39:095 --characteristic Phosphorus
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_DATA_SOURCES = Path(__file__).resolve().parents[2]
if str(_DATA_SOURCES) not in sys.path:
    sys.path.insert(0, str(_DATA_SOURCES))

from _common import net                       # noqa: E402
from WQP.access import wqp_api as w            # noqa: E402

_OUT = _DATA_SOURCES / "WQP" / "outputs"
_RAW = _DATA_SOURCES / "WQP" / "data" / "raw"
_MANIFEST = _RAW / "manifest.jsonl"


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--countycode", default="US:39:095", help="default Lucas County OH")
    p.add_argument("--characteristic", default="Phosphorus",
                   help="a VALID WQP characteristicName (default Phosphorus)")
    p.add_argument("--outdir", default=str(_OUT))
    return p.parse_args(argv)


def _our_counts(session, scope, char):
    """Our raw-REST client: legacy header counts + WQX3 verified row counts."""
    params = dict(scope, characteristicName=char)
    out = {}
    leg_station = w.build_query_url("Station", params, schema="legacy")
    out["legacy_sites"] = w.count_headers(session, leg_station).get("site")
    # Result counts via the truncation-guarded fetch (verifies against the legacy header).
    _, out["legacy_results"], _, ok_leg = w.fetch_results_verified(
        session, params, "legacy", _RAW, _MANIFEST)
    _, out["wqx3_results"], _, ok_w3 = w.fetch_results_verified(
        session, params, "wqx3", _RAW, _MANIFEST)
    if not (ok_leg and ok_w3):
        print("  ⚠ a fetch failed truncation verification even after retries")
    return out


def _dr_counts(scope, char):
    """dataretrieval package: what_sites + get_results for legacy and WQX3."""
    import dataretrieval.wqp as wqp
    kw = dict(scope, characteristicName=char)
    out = {}
    sites_leg, _ = wqp.what_sites(legacy=True, **kw)
    out["legacy_sites"] = len(sites_leg)
    res_leg, _ = wqp.get_results(legacy=True, **kw)
    out["legacy_results"] = len(res_leg)
    res_w3, _ = wqp.get_results(legacy=False, **kw)
    out["wqx3_results"] = len(res_w3)
    return out


def _cmp(a, b):
    if a is None or b is None:
        return "n/a"
    return "MATCH" if a == b else f"DIFF ({a} vs {b})"


def run(args) -> int:
    try:
        import dataretrieval  # noqa: F401
    except ImportError:
        print("dataretrieval not installed. `pip install dataretrieval` (see requirements.txt).")
        return 2

    scope = {"countycode": args.countycode}
    char = args.characteristic
    session = net.make_session()
    print(f"Cross-check scope={scope} characteristic={char!r}")
    ours = _our_counts(session, scope, char)
    theirs = _dr_counts(scope, char)

    rows = [("legacy sites", ours["legacy_sites"], theirs["legacy_sites"]),
            ("legacy results", ours["legacy_results"], theirs["legacy_results"]),
            ("wqx3 results", ours["wqx3_results"], theirs["wqx3_results"])]

    lines = [f"# WQP cross-check — raw-REST vs dataretrieval",
             "", f"- **Scope:** `{scope}` · **characteristic:** `{char}`",
             "- dataretrieval is an INDEPENDENT check, not a canonical source (METADATA §7.4).",
             "", "| Metric | ours (wqp_api) | dataretrieval | verdict |",
             "|---|--:|--:|---|"]
    all_ok = True
    for name, a, b in rows:
        verdict = _cmp(a, b)
        all_ok = all_ok and verdict in ("MATCH", "n/a")
        lines.append(f"| {name} | {a} | {b} | {verdict} |")
    lines += ["", ("✅ Our client agrees with dataretrieval." if all_ok
                   else "⚠️ Disagreement — investigate (schema/profile difference or a bug)."),
              "",
              "_Note: small diffs can be legitimate (dataretrieval may request a different default "
              "profile, or counts vs rows differ by dedup); large diffs are a real signal._"]
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    out_path = Path(args.outdir) / "xcheck_report.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")

    for name, a, b in rows:
        print(f"  {name:16s} ours={a}  dataretrieval={b}  -> {_cmp(a, b)}")
    print(f"\nWrote: {out_path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
