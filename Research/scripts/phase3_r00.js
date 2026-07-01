export const meta = {
  name: 'hab-phase3-r00',
  description: 'Phase 3 REMAINING batch r00: fetch/pre-extract + faithful summary (Sonnet) then blind verify-against-source review (Haiku) for 3 outstanding HAB sources.',
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

const SOURCES = [{"key": "ACAD-113", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7291037/", "title": "Delayed Release of Intracellular Microcystin Following Partial Oxidation of Cultured and Naturally Occurring Cyanobacteria", "tier": "ACAD", "category": "treatment-and-management", "categories": ["treatment-and-management"], "relevance": "Medium", "org_or_authors": "PMC / NCBI (peer-reviewed)", "year": null, "source_type": "peer-reviewed journal article", "alt_urls": [], "aggregator": false}, {"key": "FED-066", "url": "https://catalog.data.gov/dataset/envisat-meris-global-binned-cyanobacteria-index-ci-data-version-5-0-a7b6f", "title": "National Aeronautics and Space Administration - ENVISAT MERIS Global Binned Cyanobacteria Index (CI) Data, version 5.0", "tier": "FED", "category": "remote-sensing", "categories": ["remote-sensing"], "relevance": "Medium", "org_or_authors": "NASA (data.gov catalog)", "year": null, "source_type": "federal dataset catalog record", "alt_urls": [], "aggregator": false}, {"key": "SLG-008", "url": "https://www.oregon.gov/oha/ph/healthyenvironments/recreation/harmfulalgaeblooms/pages/blue-greenalgaeadvisories.aspx", "title": "Current Cyanobacteria Advisories", "tier": "SLG", "category": "treatment-and-management", "categories": ["treatment-and-management"], "relevance": "Medium", "org_or_authors": "Oregon Health Authority", "year": "n.d. (current/ongoing)", "source_type": "state agency advisory page/map", "alt_urls": [], "aggregator": false}]

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
log('Phase 3 r00: ' + done.length + '/' + SOURCES.length + ' processed; ' + flagged + ' review-flagged; ' + failed + ' fetch-failed')
return { batch: 'r00', count: done.length, flagged: flagged, failed: failed, results: done }
