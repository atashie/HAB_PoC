#!/usr/bin/env python3
"""Deterministically download PDF-URL sources and cache their extracted text.

WebFetch renders pages via a small model and cannot parse some PDFs (e.g. InDesign/
FlateDecode), which led a Phase-3 agent to confabulate content. This script fetches PDF
sources directly (urllib) and extracts a real text layer (pdfplumber, pypdf fallback),
caching to Research/_sources/_rawtext/<KEY>.txt so the summarizer works from faithful
text instead of guessing. Paywalled publisher PDFs may 403; those are recorded as failed
and fall back to the agent's abstract path.

Reproducible: re-running re-fetches only missing/empty caches unless --force is passed.
"""
import io
import json
import os
import sys
import urllib.request

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
SOURCES_JSON = os.path.join(REPO, "Research", "_discovery", "sources.json")
OUT_DIR = os.path.join(REPO, "Research", "_sources", "_rawtext")
MANIFEST = os.path.join(OUT_DIR, "_manifest.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
FORCE = "--force" in sys.argv


def is_pdf_url(u):
    return (u or "").lower().split("?")[0].strip().endswith(".pdf")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def extract_text(pdf_bytes):
    # pdfplumber (pdfminer) first — best text-layer fidelity.
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            txt = "\n".join((p.extract_text() or "") for p in pdf.pages)
        if txt.strip():
            return txt, "pdfplumber", len(pdf.pages) if hasattr(pdf, "pages") else None
    except Exception:
        pass
    try:
        import pypdf
        r = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        txt = "\n".join((pg.extract_text() or "") for pg in r.pages)
        if txt.strip():
            return txt, "pypdf", len(r.pages)
    except Exception:
        pass
    return "", "none", None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sources = json.load(open(SOURCES_JSON, encoding="utf-8"))
    pdfs = [s for s in sources if is_pdf_url(s.get("url"))]
    manifest = {}
    if os.path.exists(MANIFEST) and not FORCE:
        manifest = json.load(open(MANIFEST, encoding="utf-8"))

    ok, failed = 0, 0
    for s in pdfs:
        key = s["key"]
        cache = os.path.join(OUT_DIR, f"{key}.txt")
        if (not FORCE) and os.path.exists(cache) and os.path.getsize(cache) > 200:
            manifest.setdefault(key, {"status": "cached", "chars": os.path.getsize(cache)})
            ok += 1
            continue
        rec = {"key": key, "url": s.get("url")}
        try:
            raw = fetch(s["url"])
            if raw[:5] != b"%PDF-" and b"%PDF-" not in raw[:1024]:
                rec.update(status="not-pdf", note="response did not look like a PDF (likely HTML/403 page)")
                failed += 1
            else:
                txt, engine, pages = extract_text(raw)
                if txt.strip():
                    open(cache, "w", encoding="utf-8", newline="\n").write(txt)
                    rec.update(status="ok", engine=engine, pages=pages, chars=len(txt))
                    ok += 1
                else:
                    rec.update(status="no-text", note="downloaded but no extractable text layer (scanned image?)")
                    failed += 1
        except Exception as e:
            rec.update(status="error", note=f"{type(e).__name__}: {e}")
            failed += 1
        manifest[key] = rec
        print(f"  {key:9s} {rec['status']:9s} {rec.get('chars', '')!s:>8}  {(s.get('title') or '')[:52]}")

    json.dump(manifest, open(MANIFEST, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    print(f"\nPDF sources: {len(pdfs)} | extracted-ok: {ok} | failed: {failed}")
    print(f"cache dir: {OUT_DIR}")


if __name__ == "__main__":
    main()
