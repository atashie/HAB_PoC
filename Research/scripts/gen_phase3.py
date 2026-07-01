#!/usr/bin/env python3
"""Generate Phase 3 per-source pipeline workflow scripts (one per batch).

Reads Research/_discovery/sources.json (+ cached PDF text from fetch_pdftext.py) and writes
self-contained workflow scripts to Research/scripts/phase3_bNN.js. Batch 0 is a diverse ~12
VALIDATION batch; the rest are chunked into ~50s. Each script: Sonnet summarizes, then a
blind Haiku reviewer verifies claims against the source text (Phase-0-validated design).

Fidelity hardening (after b00 validation surfaced a confabulation on an unparseable PDF):
- PDF sources get deterministic pre-extracted text embedded as `pretext` (authoritative;
  agent does not WebFetch them). Long docs are windowed (head + threshold/keyword windows).
- The reviewer verifies against the full pretext (for PDF sources) rather than the agent's
  selected excerpt, removing selection bias.
- The summarizer prompt forbids any non-fetched content ("no Read tool / filesystem", no
  training-knowledge claims) and requires every claim to be backed by the source text.
"""
import json
import os
import re
import sys

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
SOURCES_JSON = os.path.join(REPO, "Research", "_discovery", "sources.json")
SCRIPTS_DIR = os.path.join(REPO, "Research", "scripts")
RAWTEXT_DIR = os.path.join(REPO, "Research", "_sources", "_rawtext")
LOG_JSON = os.path.join(REPO, "Research", "_sources", "_processing-log.json")
BATCH_SIZE = 50
DONE_SEVERITY = {"clean", "notes", "flagged"}  # successfully summarized + reviewed with claims
PRETEXT_CAP = 28000  # chars of PDF text embedded per source (bounds script size <512KB + agent context)
CATS = ["basic-science", "remote-sensing", "in-situ-and-weather-data", "models-and-methods", "treatment-and-management"]
KW = re.compile(
    r"guideline|threshold|µg|ug/l|microgram|mg/l|microcystin|cyanotoxin|cylindrospermopsin|"
    r"anatoxin|saxitoxin|recreational|drinking water|cell count|chlorophyll|alert level|advisor|"
    r"exposure|toxicity|concentration|limit|dose|efficacy|reduction|accuracy|correlation|r2|rmse",
    re.I,
)

JS_TEMPLATE = r'''export const meta = {
  name: '__META_NAME__',
  description: '__META_DESC__',
  phases: [
    { title: 'Summarize', detail: 'faithful structured summary from fetched/pre-extracted text (Sonnet)' },
    { title: 'Review', detail: 'blind verify-against-source (Haiku)' },
  ],
}

const SUMMARY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    key: { type: 'string' },
    url_used: { type: 'string' },
    resolved_url: { type: 'string' },
    fetch_status: { type: 'string', enum: ['ok', 'partial', 'blocked', 'failed'] },
    full_text_access: { type: 'string', enum: ['full', 'preprint', 'abstract', 'landing-only', 'blocked'] },
    title: { type: 'string' },
    authors_or_org: { type: 'string' },
    year: { type: 'string' },
    source_type: { type: 'string' },
    category: { type: 'string', enum: ['basic-science', 'remote-sensing', 'in-situ-and-weather-data', 'models-and-methods', 'treatment-and-management'] },
    relevance: { type: 'string', enum: ['High', 'Medium', 'Low'] },
    what_it_is: { type: 'string' },
    key_claims: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          claim: { type: 'string' },
          evidence_note: { type: 'string' },
          location: { type: 'string' },
          quote: { type: 'string' },
        },
        required: ['claim', 'evidence_note'],
      },
    },
    data_numbers: { type: 'array', items: { type: 'string' } },
    methods: { type: 'string' },
    stated_limitations: { type: 'string' },
    tensions: { type: 'string' },
    source_extract: { type: 'string' },
    fetch_notes: { type: 'string' },
  },
  required: ['key', 'fetch_status', 'full_text_access', 'what_it_is', 'key_claims', 'source_extract'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    per_claim: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          claim: { type: 'string' },
          supported: { type: 'string', enum: ['yes', 'partial', 'no'] },
          issue: { type: 'string' },
        },
        required: ['claim', 'supported'],
      },
    },
    hallucinated_numbers: { type: 'array', items: { type: 'string' } },
    dropped_caveats: { type: 'array', items: { type: 'string' } },
    unsupported_count: { type: 'integer' },
    overall: { type: 'string', enum: ['pass', 'flag'] },
    reviewer_notes: { type: 'string' },
  },
  required: ['per_claim', 'overall'],
}

const SOURCES = __SOURCES_JSON__

const ANTI = 'RULES: You have ONLY WebFetch and WebSearch tools. You have NO Read tool and NO filesystem access - NEVER claim to open, download, or read a file, and never invent a fetch you did not perform. Every claim MUST be supported by text present in your source material; if something is not in the fetched/provided text, do NOT state it, and do NOT draw on prior or training knowledge of this source. Correlation is not causation - phrase any driver or effect claim carefully.'

function summarizePrompt(s) {
  const head = `You are a rigorous research analyst building a source dossier for a foundational literature review on harmful algal blooms (HABs). Summarize ONE source faithfully and defensibly. Set key to exactly ${s.key}.

SOURCE:
- key: ${s.key}
- title: ${s.title}
- provisional category: ${s.category}; provisional relevance: ${s.relevance}`

  const produce = `Produce, using ONLY the source text: what_it_is (1-2 sentences); key_claims (each = a factual claim + evidence_note (paraphrase of the support) + location (section/page/table) + a SHORT verbatim quote ONLY for a precise threshold, number, or definition - never bulk-copy); data_numbers (values WITH UNITS and any baseline/uncertainty the source states); methods (method/model/data used, and where the source says it works or fails); stated_limitations (the caveats the source itself states); tensions (where this source contradicts or complicates other HAB findings, if evident). Reassess category (best single of the five) and relevance (High/Medium/Low) from the ACTUAL content.`

  if (s.pretext) {
    return `${head}
- URL: ${s.url}

PRE-EXTRACTED SOURCE TEXT is provided at the bottom (deterministically extracted from the source document; note: ${s.pretext_note}). This IS your source - do NOT WebFetch this document, it is already extracted. You MAY use WebSearch ONLY to confirm missing bibliographic metadata (year, authors, DOI). Set fetch_status to 'ok'; set full_text_access to 'full' if the note says full extracted text, otherwise 'partial' (windowed).

${produce}

Set source_extract to the portions of the pre-extracted text that support your claims (you need not copy all of it; an independent reviewer will separately verify your claims against the full pre-extracted text).

${ANTI}

===== PRE-EXTRACTED SOURCE TEXT (${s.pretext_note}) =====
${s.pretext}
===== END SOURCE TEXT =====`
  }

  const alt = (s.alt_urls && s.alt_urls.length) ? ('\n- alternate URLs: ' + s.alt_urls.join(', ')) : ''
  const aggNote = s.aggregator
    ? 'This URL is an aggregator (e.g., ResearchGate) that is often blocked or incomplete: FIRST WebSearch for the primary version (title plus DOI or publisher) and prefer the publisher / DOI / .gov / PMC page. Record the URL you used in url_used and any switch in resolved_url.'
    : 'If the fetch is blocked, incomplete, or clearly the wrong page, WebSearch for the primary or DOI version and use it; record url_used and resolved_url.'
  const dbl = (s.relevance === 'High')
    ? 'Because this is a HIGH-relevance source, WebFetch TWICE with different extraction prompts and reconcile the two into one - the fetch tool renders pages via a small model and drops different content each call, so a single fetch is unreliable. Take the union.'
    : 'A single thorough WebFetch is sufficient.'
  return `${head}
- primary URL: ${s.url}${alt}

STEP 1 - FETCH with the WebFetch tool. ${aggNote} ${dbl} Ask the fetch for a COMPREHENSIVE, faithful extraction: what it is; all key findings/claims; every number WITH ITS UNITS; methods, models, and data; and any stated limitations. Do not let the fetch paraphrase numbers.

STEP 2 - ASSESS ACCESS honestly. If WebFetch returns binary, empty, or garbage content (e.g., an unparseable PDF), the fetch FAILED: WebSearch for an HTML, PMC, or abstract version and use that instead. Set full_text_access to full / preprint / abstract / landing-only / blocked, and fetch_status to ok / partial / blocked / failed. If you can only reach an abstract, say so and summarize ONLY the abstract.

STEP 3 - ${produce}

STEP 4 - Build source_extract as the EVIDENCE BASE for review: for EACH key_claim, include the verbatim passage(s) from your fetched text that support it. A reviewer verifies each claim ONLY against source_extract, so any claim whose supporting text you omit WILL be marked unsupported - favor completeness, do not reduce it to a short summary.

${ANTI} If the source cannot be fetched at all, set fetch_status=failed, full_text_access=blocked, key_claims=[], and explain in fetch_notes.`
}

function reviewPrompt(summ, sourceText) {
  return `You are a BLIND adversarial fact-checker. You are given the SOURCE TEXT and the CLAIMS another analyst extracted - but NOT their reasoning. Judge each claim ONLY against the SOURCE TEXT below. Do not use outside knowledge and do not re-fetch anything.

For each claim, set supported to: 'yes' (clearly supported by the source text), 'partial' (loosely supported, overstated, or missing an important qualifier), or 'no' (not present in the source text). For partial or no, name the problem in issue.
Also report: hallucinated_numbers (any figure in the claims not found in the source text); dropped_caveats (caveats present in the source text but omitted from the claims); unsupported_count (how many claims are 'no'). Set overall to 'flag' if any claim is 'no' or any hallucinated number exists, otherwise 'pass'.
Be fair: if the source text clearly supports a claim, mark 'yes'. If the source text is only an abstract or a windowed excerpt, judge against what IS present and note that limitation in reviewer_notes rather than failing everything.

CLAIMS (JSON):
${JSON.stringify(summ.key_claims, null, 2)}

SOURCE TEXT (verify strictly against this):
"""
${sourceText || '(no source text captured)'}
"""`
}

phase('Summarize')

const results = await pipeline(
  SOURCES,
  (s) => agent(summarizePrompt(s), { label: 'sum:' + s.key, phase: 'Summarize', schema: SUMMARY_SCHEMA, model: 'sonnet' }),
  (summ, s) => {
    if (!summ) return { key: s.key, src: s, summary: null, review: null, error: 'summarize_failed' }
    const sourceText = (s.pretext && s.pretext.length) ? s.pretext : (summ.source_extract || '')
    const prompt = reviewPrompt(summ, sourceText)
    const rest = Object.assign({}, summ)
    delete rest.source_extract
    const srcLean = Object.assign({}, s)
    delete srcLean.pretext
    delete srcLean.pretext_note
    return agent(prompt, { label: 'rev:' + s.key, phase: 'Review', schema: REVIEW_SCHEMA, model: 'haiku' })
      .then((rev) => ({ key: s.key, src: srcLean, summary: rest, review: rev }))
  }
)

const done = results.filter(Boolean)
const flagged = done.filter((r) => r.review && r.review.overall === 'flag').length
const failed = done.filter((r) => !r.summary).length
log('Phase 3 __BATCH_ID__: ' + done.length + '/' + SOURCES.length + ' processed; ' + flagged + ' review-flagged; ' + failed + ' fetch-failed')
return { batch: '__BATCH_ID__', count: done.length, flagged: flagged, failed: failed, results: done }
'''


def build_pretext(key):
    path = os.path.join(RAWTEXT_DIR, f"{key}.txt")
    if not os.path.exists(path) or os.path.getsize(path) < 200:
        return None, None
    txt = open(path, encoding="utf-8").read()
    if len(txt) <= PRETEXT_CAP:
        return txt, f"full extracted text ({len(txt)} chars)"
    head = txt[:12000]
    budget = PRETEXT_CAP - len(head)
    windows, last_end, nwin = [], 12000, 0
    for m in KW.finditer(txt):
        if m.start() < last_end:
            continue
        a, b = max(m.start() - 1200, last_end), m.start() + 1800
        seg = txt[a:b]
        if budget - len(seg) < 0:
            break
        windows.append(seg)
        budget -= len(seg)
        last_end = b
        nwin += 1
    pre = head + "\n\n...[long document; head above, threshold/keyword-selected excerpts below]...\n\n" + "\n...\n".join(windows)
    return pre, f"WINDOWED excerpt from {len(txt)} chars total (head + {nwin} keyword windows)"


def attach_pretext(s):
    pre, note = build_pretext(s["key"])
    if pre:
        s["pretext"] = pre
        s["pretext_note"] = note
    return s


def make_validation_batch(sources):
    val, used = [], set()

    def take(pred, n=1):
        c = 0
        for s in sources:
            if s["key"] in used:
                continue
            if pred(s):
                val.append(s); used.add(s["key"]); c += 1
                if c >= n:
                    break

    take(lambda s: s.get("aggregator"))
    take(lambda s: (s.get("url") or "").lower().endswith(".pdf"))
    take(lambda s: s["tier"] == "FED")
    take(lambda s: s["tier"] == "SLG")
    take(lambda s: s["tier"] == "PVT")
    take(lambda s: s["tier"] == "NGO")
    take(lambda s: s["relevance"] == "Medium")
    for cat in CATS:
        take(lambda s, cat=cat: s["tier"] == "ACAD" and s["category"] == cat and s["relevance"] == "High")
    for s in sources:
        if len(val) >= 12:
            break
        if s["key"] not in used:
            val.append(s); used.add(s["key"])
    return val[:12]


def load_done_keys():
    if not os.path.exists(LOG_JSON):
        return set()
    log = json.load(open(LOG_JSON, encoding="utf-8"))
    return {k for k, e in log.items() if e.get("severity") in DONE_SEVERITY}


def main_remaining():
    """Generate batches (phase3_rNN.js) for only the sources not yet successfully done."""
    sources = json.load(open(SOURCES_JSON, encoding="utf-8"))
    done = load_done_keys()
    todo = [s for s in sources if s["key"] not in done]
    n_batches = int(sys.argv[2]) if len(sys.argv) > 2 else 6  # split across N parallel batches
    per = max(1, (len(todo) + n_batches - 1) // n_batches)
    batches = [todo[i:i + per] for i in range(0, len(todo), per)]
    max_bytes = 0
    for i, batch in enumerate(batches):
        bid = f"r{i:02d}"
        emb = [attach_pretext(dict(s)) for s in batch]
        js = (JS_TEMPLATE
              .replace("__META_NAME__", f"hab-phase3-{bid}")
              .replace("__META_DESC__", f"Phase 3 REMAINING batch {bid}: fetch/pre-extract + faithful summary (Sonnet) then blind verify-against-source review (Haiku) for {len(batch)} outstanding HAB sources.")
              .replace("__BATCH_ID__", bid)
              .replace("__SOURCES_JSON__", json.dumps(emb)))
        path = os.path.join(SCRIPTS_DIR, f"phase3_{bid}.js")
        open(path, "w", encoding="utf-8", newline="\n").write(js)
        max_bytes = max(max_bytes, len(js.encode("utf-8")))
    print(f"done={len(done)} todo={len(todo)} -> {len(batches)} batches of ~{per} (phase3_rNN.js)")
    print(f"largest script: {max_bytes/1024:.0f} KB (limit 512 KB)")
    print("todo keys:", ",".join(s["key"] for s in todo))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--remaining":
        return main_remaining()
    sources = json.load(open(SOURCES_JSON, encoding="utf-8"))
    val = make_validation_batch(sources)
    val_keys = {s["key"] for s in val}
    rest = [s for s in sources if s["key"] not in val_keys]
    batches = [val] + [rest[i:i + BATCH_SIZE] for i in range(0, len(rest), BATCH_SIZE)]

    max_bytes = 0
    for i, batch in enumerate(batches):
        bid = f"b{i:02d}"
        emb = [attach_pretext(dict(s)) for s in batch]
        js = (JS_TEMPLATE
              .replace("__META_NAME__", f"hab-phase3-{bid}")
              .replace("__META_DESC__", f"Phase 3 per-source pipeline batch {bid}: fetch/pre-extract + faithful summary (Sonnet) then blind verify-against-source review (Haiku) for {len(batch)} HAB sources.")
              .replace("__BATCH_ID__", bid)
              .replace("__SOURCES_JSON__", json.dumps(emb)))
        path = os.path.join(SCRIPTS_DIR, f"phase3_{bid}.js")
        open(path, "w", encoding="utf-8", newline="\n").write(js)
        max_bytes = max(max_bytes, len(js.encode("utf-8")))

    n_pretext = sum(1 for s in sources if build_pretext(s["key"])[0])
    print(f"sources={len(sources)} batches={len(batches)} sizes={[len(b) for b in batches]}")
    print(f"sources with embedded pretext (cached PDF text): {n_pretext}")
    print(f"largest script: {max_bytes/1024:.0f} KB (limit 512 KB)")
    print("\nVALIDATION BATCH (b00):")
    for s in val:
        pre = "PDF-pretext" if build_pretext(s["key"])[0] else ("AGG" if s.get("aggregator") else "web")
        print(f"  {s['key']:9s} {s['tier']:4s} {s['relevance']:6s} {s['category']:26s} {pre:11s} {(s['title'] or '')[:52]}")
    print("\nscripts written to Research/scripts/phase3_bNN.js")


if __name__ == "__main__":
    main()
