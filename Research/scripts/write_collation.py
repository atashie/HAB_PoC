#!/usr/bin/env python3
"""Persist Phase 4 collation-workflow output to Research/<category>/README.md (+ review sidecar).

Usage: python write_collation.py <workflow_output_file> [...]

Writes the collate stage's readme_md to Research/<category>/README.md, and the blind
synthesis-review verdict to Research/<category>/_synthesis-review.md (so any unsupported
cross-source claims are visible and actionable, not silently accepted). A cumulative
Research/_discovery/collation-log.json tracks per-category status. Idempotent per category.
"""
import json
import os
import sys

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
RESEARCH = os.path.join(REPO, "Research")
LOG = os.path.join(RESEARCH, "_discovery", "collation-log.json")


def load_results(path):
    data = json.load(open(path, encoding="utf-8"))
    res = data.get("result", data)
    if isinstance(res, dict) and "category" in res:
        return [res]
    if isinstance(res, dict) and "results" in res:
        return res["results"]
    return res if isinstance(res, list) else []


def esc(s):
    return str(s or "").replace("\r", " ")


def write_one(item):
    cat = item.get("category")
    coll = item.get("collation")
    rev = item.get("review") or {}
    if not cat or not coll or not coll.get("readme_md"):
        return {"category": cat, "status": "failed", "error": item.get("error", "no readme")}

    cat_dir = os.path.join(RESEARCH, cat)
    os.makedirs(cat_dir, exist_ok=True)
    readme = os.path.join(cat_dir, "README.md")
    open(readme, "w", encoding="utf-8", newline="\n").write(coll["readme_md"].rstrip() + "\n")

    unsupported = rev.get("unsupported_synthesis_claims") or []
    bad_keys = rev.get("keys_cited_not_in_pack") or []
    miscited = rev.get("miscited_claims") or []
    overall = rev.get("overall", "n/a")

    side = [f"# Synthesis-review verdict — {cat}", "",
            "Blind synthesis-level review of the category README against the evidence pack "
            "(catches cross-source/aggregate claims the per-source review can't). "
            "Findings here should be reconciled into README.md before final assembly.", "",
            f"- **Overall:** {overall}",
            f"- **Synthesis claims checked:** {rev.get('synthesis_claims_checked', 'n/a')}",
            f"- **Unsupported synthesis claims:** {len(unsupported)}",
            f"- **Keys cited but not in pack:** {len(bad_keys)} {bad_keys if bad_keys else ''}",
            f"- **Miscited claims:** {len(miscited)}", ""]
    if unsupported:
        side.append("## Unsupported synthesis claims")
        for u in unsupported:
            side.append(f"- **Claim:** {esc(u.get('claim'))}")
            side.append(f"  - problem: {esc(u.get('problem'))}")
            if u.get("fix"):
                side.append(f"  - suggested fix: {esc(u.get('fix'))}")
    if miscited:
        side.append("\n## Miscited claims")
        for m in miscited:
            side.append(f"- {esc(m)}")
    if rev.get("reviewer_notes"):
        side += ["", "## Reviewer notes", esc(rev.get("reviewer_notes"))]
    open(os.path.join(cat_dir, "_synthesis-review.md"), "w", encoding="utf-8", newline="\n").write("\n".join(side) + "\n")

    return {"category": cat, "status": "ok", "overall": overall,
            "subtopics": len(coll.get("subtopics_covered") or []),
            "keys_cited": len(coll.get("keys_cited") or []),
            "keys_not_cited": len(coll.get("keys_not_cited") or []),
            "contested_points": coll.get("contested_points_count"),
            "unsupported_synthesis": len(unsupported), "bad_keys": len(bad_keys),
            "readme_chars": len(coll["readme_md"])}


def main():
    if len(sys.argv) < 2:
        print("usage: write_collation.py <workflow_output_file> [...]")
        sys.exit(1)
    log = json.load(open(LOG, encoding="utf-8")) if os.path.exists(LOG) else {}
    for path in sys.argv[1:]:
        for item in load_results(path):
            r = write_one(item)
            if r.get("category"):
                log[r["category"]] = r
            print(r)
    json.dump(log, open(LOG, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    print(f"\ncollation-log: {len(log)} categories")


if __name__ == "__main__":
    main()
