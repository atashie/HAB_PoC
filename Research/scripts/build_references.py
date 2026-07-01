#!/usr/bin/env python3
"""Build Research/REFERENCES.md — the master works-cited resolving every citation key.

Reads each per-source dossier's frontmatter (Research/_sources/*.md) so every [KEY] used in
the category READMEs resolves to: title, author/org, year, URL, access date, tier, source
type, categories, relevance, access level, and review status. Deterministic and reproducible.
Also cross-checks that every key cited in the five category READMEs exists here (and reports
any dangling citation), and lists the keys each README cites.
"""
import glob
import os
import re

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
SRC_DIR = os.path.join(REPO, "Research", "_sources")
RESEARCH = os.path.join(REPO, "Research")
OUT = os.path.join(RESEARCH, "REFERENCES.md")
ACCESS_DATE = "2026-07-01"
TIERS = ["ACAD", "FED", "SLG", "NGO", "PVT"]
TIER_NAME = {
    "ACAD": "Academic / peer-reviewed journals",
    "FED": "US federal agencies (EPA / USGS / NOAA / NASA / CDC)",
    "SLG": "State & local government",
    "NGO": "NGO / non-profit / academic institute / intergovernmental (incl. WHO, IOC-UNESCO)",
    "PVT": "Private sector (incl. SePRO and competitors)",
}
CATS = ["basic-science", "remote-sensing", "in-situ-and-weather-data", "models-and-methods", "treatment-and-management"]


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        fm[k] = v
    return fm


def esc(s):
    return str(s or "").replace("|", "/").replace("\r", " ").replace("\n", " ").strip()


def key_num(k):
    m = re.match(r"([A-Z]+)-(\d+)", k)
    return (m.group(1), int(m.group(2))) if m else (k, 0)


def load_refs():
    refs = {}
    for path in sorted(glob.glob(os.path.join(SRC_DIR, "*.md"))):
        if os.path.basename(path).startswith("_"):
            continue
        fm = parse_frontmatter(open(path, encoding="utf-8").read())
        key = fm.get("key")
        if not key:
            continue
        cats = fm.get("categories") or []
        if isinstance(cats, str):
            cats = [cats]
        review = fm.get("review_severity") or fm.get("review_status") or "n/a"
        refs[key] = {
            "key": key,
            "title": esc(fm.get("title")),
            "authors": esc(fm.get("authors_or_org") or fm.get("org_or_authors")),
            "year": esc(fm.get("year")),
            "url": esc(fm.get("url")),
            "access_date": esc(fm.get("access_date") or ACCESS_DATE),
            "tier": fm.get("tier"),
            "source_type": esc(fm.get("source_type")),
            "categories": cats,
            "relevance": esc(fm.get("relevance")),
            "access": esc(fm.get("full_text_access")),
            "review": esc(review),
        }
    return refs


def cited_keys_by_readme():
    out = {}
    for cat in CATS:
        p = os.path.join(RESEARCH, cat, "README.md")
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8").read()
        out[cat] = sorted(set(re.findall(r"\b([A-Z]{3,4}-\d{3})\b", text)), key=key_num)
    return out


def main():
    refs = load_refs()
    cited = cited_keys_by_readme()
    all_cited = sorted({k for ks in cited.values() for k in ks}, key=key_num)
    dangling = [k for k in all_cited if k not in refs]

    by_tier = {t: [] for t in TIERS}
    for r in refs.values():
        by_tier.get(r["tier"], by_tier.setdefault("?", [])).append(r)
    for t in by_tier:
        by_tier[t].sort(key=lambda r: key_num(r["key"]))

    out = []
    out.append("# HAB Research — Master References\n")
    out.append(f"Every citation key `[KEY]` used in the category collations resolves here. "
               f"Generated deterministically from the per-source dossiers in `_sources/` by "
               f"`scripts/build_references.py`. Default access date: {ACCESS_DATE}.\n")
    out.append(f"**Total sources:** {len(refs)}  |  "
               + "  ".join(f"{t}={len(by_tier.get(t, []))}" for t in TIERS) + "\n")
    out.append("**Legend.** Tier = provenance (ACAD peer-reviewed › FED federal › SLG state/local › "
               "NGO non-profit/intergovernmental › PVT private). Access = full / preprint / abstract / "
               "landing-only / blocked. Review = per-source blind-review outcome "
               "(clean / notes / flagged / manual); see the source dossier for the full verdict.\n")

    # dangling-citation check
    out.append("## Citation integrity check\n")
    if dangling:
        out.append(f"⚠ **{len(dangling)} cited key(s) do not resolve to a dossier:** " + ", ".join(dangling) + "\n")
    else:
        out.append(f"✓ All **{len(all_cited)}** keys cited across the five category READMEs resolve to a dossier below. No dangling citations.\n")
    uncited = sorted([k for k in refs if k not in set(all_cited)], key=key_num)
    out.append(f"Sources in the corpus but not cited in any category README: **{len(uncited)}** "
               f"({'none' if not uncited else ', '.join(uncited)}). These remain fully documented as dossiers in `_sources/`.\n")

    # master list by tier
    for t in TIERS:
        items = by_tier.get(t, [])
        if not items:
            continue
        out.append(f"## {t} — {TIER_NAME[t]}  ({len(items)})\n")
        out.append("| Key | Title | Author / Org | Year | Categories | Rel | Access | Review | URL |")
        out.append("|-----|-------|--------------|------|------------|-----|--------|--------|-----|")
        for r in items:
            out.append("| {key} | {title} | {au} | {yr} | {cats} | {rel} | {acc} | {rev} | {url} |".format(
                key=r["key"], title=r["title"] or "(untitled)", au=r["authors"], yr=r["year"],
                cats=";".join(r["categories"]), rel=r["relevance"], acc=r["access"],
                rev=r["review"], url=f"[link]({r['url']})" if r["url"] else ""))
        out.append("")

    # per-README cited-key index
    out.append("## Keys cited per category README\n")
    for cat in CATS:
        ks = cited.get(cat, [])
        out.append(f"- **{cat}** ({len(ks)}): {', '.join(ks) if ks else '(none)'}")
    out.append("")

    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"wrote {OUT}")
    print(f"refs={len(refs)} cited_unique={len(all_cited)} dangling={len(dangling)} uncited={len(uncited)}")
    print("by tier:", {t: len(by_tier.get(t, [])) for t in TIERS})
    if dangling:
        print("DANGLING:", dangling)


if __name__ == "__main__":
    main()
