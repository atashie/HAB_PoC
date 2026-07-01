#!/usr/bin/env python3
"""Parse per-source dossiers (Research/_sources/*.md) into compact per-category evidence packs.

Phase 4 collation agents can't read the filesystem, so their raw material must be embedded in
the workflow script. Full dossiers (median 16 KB) are too large to bundle 67 at once, so this
extracts a COMPACT pack per source — frontmatter + what-it-is + claims (verdict + text only,
sub-bullets/quotes stripped) + key numbers + tensions — and groups packs by category into
Research/_discovery/evidence/<category>.json. Deterministic; re-run after any dossier changes.
"""
import glob
import json
import os
import re

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
SRC_DIR = os.path.join(REPO, "Research", "_sources")
OUT_DIR = os.path.join(REPO, "Research", "_discovery", "evidence")
CATS = ["basic-science", "remote-sensing", "in-situ-and-weather-data", "models-and-methods", "treatment-and-management"]
VMAP = {"✓ verified": "Y", "⚠ partial": "P", "✗ UNVERIFIED": "N", "? unreviewed": "?"}
NUM_CAP = 12          # max data_numbers kept per source
NUM_CHARS = 220       # max chars per number line
TENS_CHARS = 550      # max chars of tensions kept
WHAT_CHARS = 320      # max chars of what-it-is kept
# N-verdict claims (blind reviewer judged unsupported by the source) are EXCLUDED from
# collation input — they remain in the dossiers for audit, but must not feed synthesis.
DROP_VERDICTS = {"N"}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if not m:
        return fm, text
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        fm[k] = v
    return fm, text[m.end():]


def section(body, title):
    """Return the text of a '## title' section up to the next '## '."""
    m = re.search(r"^## " + re.escape(title) + r"\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def parse_claims(body):
    sec = section(body, "Key claims")
    claims = []
    for line in sec.splitlines():
        m = re.match(r"^- \*\*\[(.+?)\]\*\*\s*(.*)$", line)  # top-level claim bullets only
        if m:
            claims.append({"v": VMAP.get(m.group(1).strip(), "?"), "c": m.group(2).strip()})
    return claims


def parse_bullets(body, title, cap, charcap):
    sec = section(body, title)
    out = []
    for line in sec.splitlines():
        m = re.match(r"^- (.*)$", line)
        if m and not line.startswith("  "):
            out.append(m.group(1).strip()[:charcap])
        if len(out) >= cap:
            break
    return out


def what_it_is(body):
    m = re.search(r"\*\*What it is\.\*\*\s*(.*?)(?=\n\n|\n## )", body, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    packs = {c: [] for c in CATS}
    all_packs = []
    skipped = []
    for path in sorted(glob.glob(os.path.join(SRC_DIR, "*.md"))):
        if os.path.basename(path).startswith("_"):
            continue
        text = open(path, encoding="utf-8").read()
        fm, body = parse_frontmatter(text)
        if not fm.get("key"):
            continue
        all_claims = parse_claims(body)
        if not all_claims:
            skipped.append(fm.get("key"))  # fetch-failed stub or empty
            continue
        claims = [c for c in all_claims if c["v"] not in DROP_VERDICTS]
        n_dropped = len(all_claims) - len(claims)
        tensions = re.sub(r"\s+", " ", section(body, "Tensions with other findings")).strip()[:TENS_CHARS]
        cats = fm.get("categories") or []
        if isinstance(cats, str):
            cats = [cats]
        rec = {
            "key": fm.get("key"),
            "title": fm.get("title"),
            "tier": fm.get("tier"),
            "relevance": fm.get("relevance"),
            "year": fm.get("year"),
            "access": fm.get("full_text_access"),
            "severity": fm.get("review_severity"),
            "what": what_it_is(body)[:WHAT_CHARS],
            "claims": claims,
            "n_excluded_unverified": n_dropped,
            "numbers": parse_bullets(body, "Data / numbers", NUM_CAP, NUM_CHARS),
            "tensions": tensions,
        }
        all_packs.append(rec)
        for c in cats:
            if c in packs:
                packs[c].append(rec)

    for c in CATS:
        json.dump(packs[c], open(os.path.join(OUT_DIR, f"{c}.json"), "w", encoding="utf-8", newline="\n"),
                  ensure_ascii=False, indent=1)
    json.dump(all_packs, open(os.path.join(OUT_DIR, "_all.json"), "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=1)

    print(f"parsed {len(all_packs)} dossiers; skipped {len(skipped)} (no claims): {skipped}")
    for c in CATS:
        recs = packs[c]
        size = len(json.dumps(recs, ensure_ascii=False))
        nclaims = sum(len(r["claims"]) for r in recs)
        print(f"  {c:26s} sources={len(recs):3d}  claims={nclaims:4d}  packKB={size/1024:5.0f}")


if __name__ == "__main__":
    build()
