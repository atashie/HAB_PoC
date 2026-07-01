#!/usr/bin/env python3
"""Phase 2 curation: dedup + group the discovery-sweep candidates into a draft source registry.

Reads the hab-discovery workflow output, caches the raw candidates in-repo (so this is
reproducible without the ephemeral temp file), dedups by normalized URL, merges cross-lane
hits (keeping the highest relevance and accumulating categories/lanes), groups by source
tier, assigns provisional citation keys, and emits:
  - Research/_discovery/candidates-raw.json   (cached raw pull; never hand-edit)
  - Research/SOURCE-REGISTRY.md                (draft registry for review)

Provisional keys are stable only after Phase 3 begins; until then they may be renumbered.
"""
import json
import os
import re
from urllib.parse import urlparse

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
DISC_DIR = os.path.join(REPO, "Research", "_discovery")
os.makedirs(DISC_DIR, exist_ok=True)
RAW_CACHE = os.path.join(DISC_DIR, "candidates-raw.json")
REGISTRY = os.path.join(REPO, "Research", "SOURCE-REGISTRY.md")

TEMP_OUT = (
    r"C:\Users\arikt\AppData\Local\Temp\claude"
    r"\C--Users-arikt-Documents-GitHub-HAB-PoC"
    r"\d263f364-ff85-4841-bbfb-f2c9e9e81b3e\tasks\wjfvd90c5.output"
)
RUN_ID = "wf_6284bffb-2c5"
ACCESS_DATE = "2026-07-01"

REL_ORDER = {"High": 3, "Medium": 2, "Low": 1}
TIERS = ["ACAD", "FED", "SLG", "NGO", "PVT"]
TIER_NAME = {
    "ACAD": "Academic / peer-reviewed journals",
    "FED": "US federal agencies (EPA/USGS/NOAA/NASA)",
    "SLG": "State & local government",
    "NGO": "NGO / non-profit / academic institute / intergovernmental",
    "PVT": "Private sector",
}
SUSPICIOUS = ("researchgate.net", "wikipedia.org", "academia.edu", "scholar.google", "semanticscholar.org/paper")


def load_lanes():
    if os.path.exists(RAW_CACHE):
        return json.load(open(RAW_CACHE, encoding="utf-8"))["lanes"]
    data = json.load(open(TEMP_OUT, encoding="utf-8"))
    result = data.get("result", data)
    lanes = result["lanes"]
    json.dump(
        {"run_id": RUN_ID, "access_date": ACCESS_DATE, "lanes": lanes},
        open(RAW_CACHE, "w", encoding="utf-8"),
        indent=2,
        ensure_ascii=False,
    )
    return lanes


def norm_url(u):
    u = (u or "").strip()
    try:
        p = urlparse(u)
        host = (p.netloc or "").lower()
        if host.startswith("www."):
            host = host[4:]
        path = (p.path or "").rstrip("/")
        return host + path
    except Exception:
        return u.lower()


def content_id(u):
    """Extract a stable content identifier (PMC/arXiv/bioRxiv/DOI) so the same paper
    reached via different URLs merges to one source."""
    u = u or ""
    m = re.search(r"PMC\d+", u)
    if m:
        return "pmc:" + m.group(0)
    m = re.search(r"arxiv\.org/abs/([\d.]+)", u, re.I)
    if m:
        return "arxiv:" + m.group(1)
    m = re.search(r"(10\.1101/[0-9.]+)", u)  # bioRxiv-style DOI stem (drop version suffix)
    if m:
        return "biorxiv:" + re.split(r"v\d+", m.group(1))[0].rstrip(".")
    m = re.search(r"(10\.\d{4,9}/[^\s/?#]+)", u)  # generic DOI embedded in URL
    if m:
        doi = m.group(1).lower()
        doi = re.sub(r"\.(pdf|full|abstract|xml)$", "", doi).rstrip("/.")
        return "doi:" + doi
    return None


URL_PREF = [
    "doi.org", "nature.com", "science.org", "pnas.org", "sciencedirect.com", "pubs.acs.org",
    "onlinelibrary.wiley.com", "link.springer.com", "academic.oup.com", "iopscience",
    "agupubs", "ametsoc", "aslopubs", "cdnsciencepub", "tandfonline", "mdpi.com",
    "frontiersin", "ascelibrary", "sagepub", "annualreviews", ".gov", "who.int",
    "pmc.ncbi", "ncbi.nlm.nih.gov", "arxiv.org", "biorxiv.org", "github", "researchgate.net",
]


def url_rank(u):
    h = norm_url(u)
    for i, s in enumerate(URL_PREF):
        if s in h:
            return i
    return len(URL_PREF)


def san(s):
    return (str(s or "")
            .replace("&amp;", "&")
            .replace("|", "/")
            .replace("\n", " ")
            .replace("\r", " ")
            .strip())


def main():
    lanes = load_lanes()
    rows = []
    for L in lanes:
        lane = L.get("lane") or "?"
        for c in (L.get("candidates") or []):
            c = dict(c)
            c["_lane"] = lane
            rows.append(c)

    merged = {}
    for c in rows:
        k = norm_url(c.get("url", ""))
        if not k:
            continue
        if k not in merged:
            c["_lanes"] = [c["_lane"]]
            c["_cats"] = [c.get("category")] if c.get("category") else []
            merged[k] = c
        else:
            m = merged[k]
            if c["_lane"] not in m["_lanes"]:
                m["_lanes"].append(c["_lane"])
            if c.get("category") and c["category"] not in m["_cats"]:
                m["_cats"].append(c["category"])
            if REL_ORDER.get(c.get("relevance"), 0) > REL_ORDER.get(m.get("relevance"), 0):
                m["relevance"] = c.get("relevance")
            for f in ("org_or_authors", "year", "source_type"):
                if not m.get(f) and c.get(f):
                    m[f] = c[f]

    cands = list(merged.values())

    # Second pass: merge content-duplicates (same paper via different URLs) by extracted ID.
    cid_map = {}
    deduped = []
    n_content_merged = 0
    for c in cands:
        cid = content_id(c.get("url", ""))
        if cid and cid in cid_map:
            m = cid_map[cid]
            n_content_merged += 1
            for lane in c["_lanes"]:
                if lane not in m["_lanes"]:
                    m["_lanes"].append(lane)
            for cat in c["_cats"]:
                if cat and cat not in m["_cats"]:
                    m["_cats"].append(cat)
            if REL_ORDER.get(c.get("relevance"), 0) > REL_ORDER.get(m.get("relevance"), 0):
                m["relevance"] = c.get("relevance")
            for f in ("org_or_authors", "year", "source_type"):
                if not m.get(f) and c.get(f):
                    m[f] = c[f]
            m.setdefault("_alt_urls", [])
            if url_rank(c.get("url", "")) < url_rank(m.get("url", "")):
                m["_alt_urls"].append(m["url"])
                m["url"] = c["url"]
            else:
                m["_alt_urls"].append(c.get("url", ""))
        else:
            if cid:
                cid_map[cid] = c
            deduped.append(c)
    cands = deduped

    by_tier = {t: [] for t in TIERS}
    untier = []
    for c in cands:
        by_tier.get(c.get("tier"), untier).append(c)
    for t in TIERS:
        by_tier[t].sort(key=lambda x: (-REL_ORDER.get(x.get("relevance"), 0), (x.get("title") or "").lower()))

    for t in TIERS:
        for i, c in enumerate(by_tier[t], 1):
            c["_key"] = f"{t}-{i:03d}"

    # ---- stats ----
    n_raw = len(rows)
    n_uniq = len(cands)
    cat_counts, rel_counts, tier_counts = {}, {}, {}
    for c in cands:
        for cc in (c["_cats"] or ["?"]):
            cat_counts[cc] = cat_counts.get(cc, 0) + 1
        rel_counts[c.get("relevance")] = rel_counts.get(c.get("relevance"), 0) + 1
        tier_counts[c.get("tier")] = tier_counts.get(c.get("tier"), 0) + 1
    multi_cat = [c for c in cands if len(c["_cats"]) > 1]
    flagged = [c for c in cands if any(s in norm_url(c.get("url", "")) for s in SUSPICIOUS)]

    # ---- write registry ----
    out = []
    out.append("# HAB Research — Source Registry (DRAFT, Phase 2)\n")
    out.append(f"**Discovery run:** `{RUN_ID}`  |  **Access date:** {ACCESS_DATE}  |  "
               f"**Source of truth for raw candidates:** `Research/_discovery/candidates-raw.json`\n")
    out.append("> Provisional citation keys — stable once Phase 3 begins; may be renumbered before then. "
               "Generated by `Research/scripts/curate_registry.py` (deterministic dedup by normalized URL).\n")
    out.append("## Summary\n")
    out.append(f"- **Raw candidates (pre-dedup):** {n_raw}")
    out.append(f"- **Merged as content-duplicates (same paper, different URL):** {n_content_merged}")
    out.append(f"- **Unique sources:** {n_uniq}")
    out.append(f"- **By tier:** " + ", ".join(f"{t}={tier_counts.get(t,0)}" for t in TIERS)
               + (f", untiered={len(untier)}" if untier else ""))
    out.append(f"- **By relevance:** " + ", ".join(f"{r}={rel_counts.get(r,0)}" for r in ("High", "Medium", "Low")))
    out.append(f"- **By category (counts each category a source touches):** "
               + ", ".join(f"{k}={v}" for k, v in sorted(cat_counts.items(), key=lambda x: -x[1])))
    out.append(f"- **Multi-category sources:** {len(multi_cat)}  |  **Flagged hosts for manual review:** {len(flagged)}\n")

    for t in TIERS:
        items = by_tier[t]
        if not items:
            continue
        out.append(f"## {t} — {TIER_NAME[t]}  ({len(items)})\n")
        out.append("| Key | Rel | Category | Title | Org/Authors | Year | Why relevant |")
        out.append("|-----|-----|----------|-------|-------------|------|--------------|")
        for c in items:
            title = san(c.get("title"))
            url = (c.get("url") or "").strip()
            cats = ";".join(x for x in c["_cats"] if x)
            out.append("| {key} | {rel} | {cat} | [{title}]({url}) | {org} | {yr} | {why} |".format(
                key=c["_key"], rel=(c.get("relevance") or "?"), cat=san(cats),
                title=title or "(untitled)", url=url or "#",
                org=san(c.get("org_or_authors")), yr=san(c.get("year")),
                why=san(c.get("why_relevant")) + (
                    f" (+{len(c['_alt_urls'])} alt URL merged)" if c.get("_alt_urls") else ""),
            ))
        out.append("")

    if untier:
        out.append(f"## Untiered / needs tier ({len(untier)})\n")
        for c in untier:
            out.append(f"- [{san(c.get('title'))}]({c.get('url')}) — tier={c.get('tier')}")
        out.append("")

    out.append("## ⚑ Flagged for manual review\n")
    out.append("Hosts that are aggregators/tertiary (prefer the primary DOI/publisher/.gov URL instead):\n")
    if flagged:
        for c in flagged:
            out.append(f"- `{c['_key']}` [{san(c.get('title'))}]({c.get('url')})")
    else:
        out.append("- (none)")
    out.append("")
    out.append("Multi-category sources (reviewed once; cited from each relevant collation):\n")
    for c in multi_cat:
        out.append(f"- `{c['_key']}` {san(c.get('title'))} — {';'.join(x for x in c['_cats'] if x)}")

    open(REGISTRY, "w", encoding="utf-8").write("\n".join(out) + "\n")

    # Machine-readable work-list for Phase 3 (per-source pipeline).
    sources_out = []
    for t in TIERS:
        for c in by_tier[t]:
            sources_out.append({
                "key": c["_key"],
                "url": c.get("url"),
                "title": c.get("title"),
                "tier": t,
                "category": c.get("category"),
                "categories": [x for x in c["_cats"] if x],
                "relevance": c.get("relevance"),
                "org_or_authors": c.get("org_or_authors"),
                "year": c.get("year"),
                "source_type": c.get("source_type"),
                "alt_urls": c.get("_alt_urls", []),
                "aggregator": any(s in norm_url(c.get("url", "")) for s in SUSPICIOUS),
            })
    json.dump(sources_out, open(os.path.join(DISC_DIR, "sources.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    print(f"raw={n_raw} url_unique={len(merged)} content_merged={n_content_merged} unique={n_uniq}")
    print("sources.json:", len(sources_out))
    print("tier:", {t: tier_counts.get(t, 0) for t in TIERS}, "untiered:", len(untier))
    print("relevance:", rel_counts)
    print("category:", cat_counts)
    print("flagged_hosts:", len(flagged), "multi_cat:", len(multi_cat))
    print("wrote:", REGISTRY)
    print("cached:", RAW_CACHE)


if __name__ == "__main__":
    main()
