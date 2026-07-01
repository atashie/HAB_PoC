#!/usr/bin/env python3
"""Turn Phase 3 workflow output into per-source dossiers (Research/_sources/<KEY>-<slug>.md).

Usage: python write_sources.py <workflow_output_file> [<more_output_files> ...]

Each source's blind-review verdict is applied deterministically (Stage C): every claim is
tagged verified / partial / unverified against the reviewer's per-claim judgment, and any
flagged source is marked. A cumulative log (Research/_sources/_processing-log.json + .md)
tracks status across batches. Idempotent: re-running a batch overwrites its files/log rows.
"""
import json
import os
import re
import sys

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
SRC_DIR = os.path.join(REPO, "Research", "_sources")
LOG_JSON = os.path.join(SRC_DIR, "_processing-log.json")
LOG_MD = os.path.join(REPO, "Research", "_sources", "_processing-log.md")
ACCESS_DATE = "2026-07-01"
BADGE = {"yes": "✓ verified", "partial": "⚠ partial", "no": "✗ UNVERIFIED"}


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return (s[:60] or "untitled").rstrip("-")


def norm(s):
    return re.sub(r"\W+", " ", (s or "").lower()).strip()


def esc(s):
    return str(s or "").replace("\r", " ").strip()


def load_results(path):
    data = json.load(open(path, encoding="utf-8"))
    res = data.get("result", data)
    return res.get("results", []) if isinstance(res, dict) else []


def md_frontmatter(d):
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(str(x) for x in v)}]")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def write_source(item):
    key = item.get("key")
    src = item.get("src") or {}
    summ = item.get("summary")
    rev = item.get("review")

    if not summ or summ.get("fetch_status") == "failed" or not summ.get("key_claims"):
        # Fetch failed or nothing extracted — write a stub so the gap is visible, not silent.
        title = (summ or {}).get("title") or src.get("title") or key
        path = os.path.join(SRC_DIR, f"{key}-{slug(title)}.md")
        fm = md_frontmatter({
            "key": key, "title": esc(title), "url": src.get("url"),
            "access_date": ACCESS_DATE, "tier": src.get("tier"),
            "categories": src.get("categories") or [src.get("category")],
            "relevance": src.get("relevance"), "fetch_status": (summ or {}).get("fetch_status", "failed"),
            "full_text_access": (summ or {}).get("full_text_access", "blocked"),
            "review_status": "not-reviewed",
        })
        body = f"\n\n# {esc(title)}\n\n> **Not summarized** — fetch failed or returned no usable content.\n\n" \
               f"- URL: {src.get('url')}\n- Fetch notes: {esc((summ or {}).get('fetch_notes'))}\n"
        open(path, "w", encoding="utf-8", newline="\n").write(fm + body)
        return {"key": key, "title": esc(title), "tier": src.get("tier"), "fetch_status": (summ or {}).get("fetch_status", "failed"),
                "full_text_access": (summ or {}).get("full_text_access", "blocked"), "severity": "fetch-failed", "review": "n/a",
                "n_claims": 0, "n_unverified": 0, "n_partial": 0, "n_hallucinated": 0, "n_dropped": 0, "file": os.path.basename(path)}

    url = summ.get("resolved_url") or summ.get("url_used") or src.get("url")
    title = summ.get("title") or src.get("title") or key
    cats = src.get("categories") or ([summ.get("category")] if summ.get("category") else [])
    rmap = {}
    per_claim = (rev or {}).get("per_claim") or []
    for pc in per_claim:
        rmap[norm(pc.get("claim"))] = pc

    n_unverified = 0
    n_partial = 0
    claim_lines = []
    for i, c in enumerate(summ.get("key_claims", [])):
        pc = rmap.get(norm(c.get("claim"))) or (per_claim[i] if i < len(per_claim) else None)
        sup = (pc or {}).get("supported", "?")
        if sup == "no":
            n_unverified += 1
        elif sup == "partial":
            n_partial += 1
        badge = BADGE.get(sup, "? unreviewed")
        issue = (pc or {}).get("issue")
        claim_lines.append(f"- **[{badge}]** {esc(c.get('claim'))}")
        if c.get("evidence_note"):
            claim_lines.append(f"  - *evidence:* {esc(c.get('evidence_note'))}" + (f" ({esc(c.get('location'))})" if c.get("location") else ""))
        if c.get("quote"):
            claim_lines.append(f"  - *quote:* \"{esc(c.get('quote'))}\"")
        if issue:
            claim_lines.append(f"  - *reviewer:* {esc(issue)}")

    overall = (rev or {}).get("overall", "not-reviewed")
    n_hall = len((rev or {}).get("hallucinated_numbers") or [])
    n_drop = len((rev or {}).get("dropped_caveats") or [])
    # Severity computed from the structured verdict, not Haiku's (stricter, inconsistent) overall:
    #   flagged = real integrity issue (unsupported claim or hallucinated number)
    #   notes   = faithful but reviewer noted partial claims / dropped caveats
    #   clean   = nothing flagged
    if not rev:
        severity = "not-reviewed"
    elif n_unverified > 0 or n_hall > 0:
        severity = "flagged"
    elif n_partial > 0 or n_drop > 0:
        severity = "notes"
    else:
        severity = "clean"
    fm = md_frontmatter({
        "key": key, "title": esc(title),
        "authors_or_org": esc(summ.get("authors_or_org") or src.get("org_or_authors")),
        "year": esc(summ.get("year") or src.get("year")),
        "url": url, "access_date": ACCESS_DATE, "tier": src.get("tier"),
        "source_type": esc(summ.get("source_type") or src.get("source_type")),
        "categories": cats, "relevance": summ.get("relevance") or src.get("relevance"),
        "full_text_access": summ.get("full_text_access"), "fetch_status": summ.get("fetch_status"),
        "review_severity": severity, "review_overall": overall,
    })

    out = [fm, "", f"# {esc(title)}", ""]
    if summ.get("resolved_url") and summ.get("resolved_url") != src.get("url"):
        out.append(f"> Note: provisional URL was resolved to a primary source. Original: {src.get('url')}\n")
    out += [f"**What it is.** {esc(summ.get('what_it_is'))}", ""]
    out += ["## Key claims", "*(each tagged with its blind-review verdict)*", ""] + claim_lines + [""]
    if summ.get("data_numbers"):
        out += ["## Data / numbers"] + [f"- {esc(x)}" for x in summ["data_numbers"]] + [""]
    if summ.get("methods"):
        out += ["## Methods", esc(summ.get("methods")), ""]
    if summ.get("stated_limitations"):
        out += ["## Stated limitations", esc(summ.get("stated_limitations")), ""]
    if summ.get("tensions"):
        out += ["## Tensions with other findings", esc(summ.get("tensions")), ""]

    out += ["## Blind adversarial review", f"- **Overall:** {overall}"]
    if (rev or {}).get("unsupported_count") is not None:
        out.append(f"- **Unsupported claims:** {rev.get('unsupported_count')}")
    if (rev or {}).get("hallucinated_numbers"):
        out += ["- **Possible hallucinated/misattributed numbers:**"] + [f"  - {esc(x)}" for x in rev["hallucinated_numbers"]]
    if (rev or {}).get("dropped_caveats"):
        out += ["- **Dropped caveats:**"] + [f"  - {esc(x)}" for x in rev["dropped_caveats"]]
    if (rev or {}).get("reviewer_notes"):
        out.append(f"- **Reviewer notes:** {esc(rev.get('reviewer_notes'))}")
    out += ["", "## Provenance",
            f"- Canonical URL: {url}",
            f"- Access date: {ACCESS_DATE}",
            f"- Full-text access: {summ.get('full_text_access')} | Fetch status: {summ.get('fetch_status')}"]
    if summ.get("fetch_notes"):
        out.append(f"- Fetch notes: {esc(summ.get('fetch_notes'))}")
    out.append("")

    path = os.path.join(SRC_DIR, f"{key}-{slug(title)}.md")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return {"key": key, "title": esc(title), "tier": src.get("tier"),
            "fetch_status": summ.get("fetch_status"), "full_text_access": summ.get("full_text_access"),
            "severity": severity, "review": overall, "n_claims": len(summ.get("key_claims", [])),
            "n_unverified": n_unverified, "n_partial": n_partial, "n_hallucinated": n_hall, "n_dropped": n_drop,
            "file": os.path.basename(path)}


def main():
    if len(sys.argv) < 2:
        print("usage: write_sources.py <workflow_output_file> [...]")
        sys.exit(1)
    os.makedirs(SRC_DIR, exist_ok=True)
    log = {}
    if os.path.exists(LOG_JSON):
        log = json.load(open(LOG_JSON, encoding="utf-8"))

    n = 0
    for path in sys.argv[1:]:
        for item in load_results(path):
            entry = write_source(item)
            log[entry["key"]] = entry
            n += 1

    json.dump(log, open(LOG_JSON, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)

    rows = sorted(log.values(), key=lambda e: e["key"])
    sev_counts = {}
    for e in rows:
        sev_counts[e.get("severity")] = sev_counts.get(e.get("severity"), 0) + 1
    md = ["# Phase 3 processing log", "",
          f"Sources written: **{len(rows)}**  |  Access date: {ACCESS_DATE}", "",
          "**Severity** (from structured verdict): `flagged` = ≥1 unsupported claim or hallucinated number; "
          "`notes` = faithful, reviewer noted partial claims / dropped caveats; `clean` = nothing flagged.", "",
          "By severity: " + ", ".join(f"{k}={v}" for k, v in sorted(sev_counts.items(), key=lambda x: -x[1])), "",
          "| Key | Tier | Fetch | Access | Severity | Overall | Claims | Unver | Part | HallNum | Dropped | File |",
          "|-----|------|-------|--------|----------|---------|--------|-------|------|---------|---------|------|"]
    for e in rows:
        md.append(f"| {e['key']} | {e.get('tier')} | {e.get('fetch_status')} | {e.get('full_text_access')} | "
                  f"{e.get('severity')} | {e.get('review')} | {e.get('n_claims')} | {e.get('n_unverified')} | "
                  f"{e.get('n_partial')} | {e.get('n_hallucinated')} | {e.get('n_dropped')} | {e.get('file')} |")
    open(LOG_MD, "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")

    flagged = [e for e in rows if e.get("severity") == "flagged"]
    failed = [e for e in rows if e.get("fetch_status") == "failed"]
    print(f"wrote {n} source files this run; log now has {len(rows)} total")
    print(f"severity: {sev_counts}")
    print(f"FLAGGED (real issues): {len(flagged)} {[e['key'] for e in flagged][:30]}")
    print(f"fetch-failed: {len(failed)} {[e['key'] for e in failed][:20]}")


if __name__ == "__main__":
    main()
