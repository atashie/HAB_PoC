#!/usr/bin/env python3
"""Generate Phase 4 collation workflow scripts — one per category (phase4_<cat>.js).

Each script embeds that category's evidence pack (Research/_discovery/evidence/<cat>.json)
and runs the plan's two stages:
  Stage A (collate, Sonnet): organize the pack's verified/partial claims into a category
    README — well-established sub-topics + an explicit contested/uncertain section + a
    compact data/models/methods table + gaps; every claim cites [KEY]. Data categories
    (remote-sensing, in-situ-and-weather-data) additionally get a data-feasibility subsection.
  Stage B (blind synthesis review, Haiku): re-derive every cross-source / comparative /
    "most studies" claim in the README and verify it against the pack; flag unsupported ones
    and any cited KEY not in the pack. This is the synthesis-level check codex asked for
    (Phase 3's per-claim review can't catch claims that live BETWEEN sources).

One script per category keeps each under the 512 KB script cap and lets them run
individually (rate-limit-friendly). write_collation.py persists {readme, review} to
Research/<cat>/README.md + a review sidecar.
"""
import json
import os
import sys

REPO = r"C:\Users\arikt\Documents\GitHub\HAB_PoC"
EV_DIR = os.path.join(REPO, "Research", "_discovery", "evidence")
SCRIPTS_DIR = os.path.join(REPO, "Research", "scripts")
CATS = ["basic-science", "remote-sensing", "in-situ-and-weather-data", "models-and-methods", "treatment-and-management"]
DATA_CATS = {"remote-sensing", "in-situ-and-weather-data"}

CAT_GUIDE = {
    "basic-science": "bloom biology & dominant taxa; nutrient drivers and the N-vs-P limitation debate; temperature/stratification/hydrology; cyanotoxins & health; climate change & long-term trends (and the attribution debate); succession/physiology (buoyancy, N-fixation).",
    "remote-sensing": "satellite detection algorithms (cyanobacteria index, phycocyanin, chlorophyll-a, spectral shape); sensors & missions (MERIS, Sentinel-3 OLCI, Sentinel-2, Landsat); atmospheric correction; validation, accuracy, and resolution/revisit limits over inland waters.",
    "in-situ-and-weather-data": "in-situ water-quality data & monitoring networks (Water Quality Portal, NWIS, NARS/NLA); cyanotoxin & chlorophyll datasets; weather/climate data for pairing; sampling design, detection limits, gaps and biases.",
    "models-and-methods": "statistical & machine-learning forecast/risk models; mechanistic/process-based models; data fusion & early-warning/anomaly-detection; validation, skill metrics, leakage/overfitting, spatiotemporal cross-validation.",
    "treatment-and-management": "algaecides (copper, hydrogen peroxide) and efficacy/toxin-release trade-offs; nutrient & watershed management (P & N load reduction, TMDLs, BMPs, alum/P-inactivation, biomanipulation); in-lake physical controls; guideline values & advisory frameworks.",
}

JS_TEMPLATE = r'''export const meta = {
  name: 'hab-phase4-__CAT__',
  description: 'Phase 4 collation for the __CAT__ category: collate verified claims into a keyed category README (Sonnet), then blind synthesis-review of cross-source claims against the evidence pack (Haiku).',
  phases: [
    { title: 'Collate', detail: 'organize verified claims into a keyed category README (Sonnet)' },
    { title: 'SynthReview', detail: 'blind verify cross-source/synthesis claims vs pack (Haiku)' },
  ],
}

const COLLATE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    readme_md: { type: 'string' },
    subtopics_covered: { type: 'array', items: { type: 'string' } },
    contested_points_count: { type: 'integer' },
    keys_cited: { type: 'array', items: { type: 'string' } },
    keys_not_cited: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['readme_md', 'subtopics_covered', 'keys_cited'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    synthesis_claims_checked: { type: 'integer' },
    unsupported_synthesis_claims: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          claim: { type: 'string' },
          problem: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['claim', 'problem'],
      },
    },
    keys_cited_not_in_pack: { type: 'array', items: { type: 'string' } },
    miscited_claims: { type: 'array', items: { type: 'string' } },
    overall: { type: 'string', enum: ['pass', 'flag'] },
    reviewer_notes: { type: 'string' },
  },
  required: ['unsupported_synthesis_claims', 'overall'],
}

const CATEGORY = '__CAT__'
const CAT_SCOPE = __CAT_SCOPE__
const IS_DATA_CAT = __IS_DATA__
const PACK = __PACK_JSON__

const dataFeasibilityBlock = IS_DATA_CAT
  ? `\n- A "## Data-feasibility & coverage" section: per surveyed public dataset/sensor, its spatial & temporal coverage, resolution, latency, detection limits, access method, and (critically) how well the remote-sensing and in-situ modalities actually overlap/join in space and time. This characterizes real public data; do NOT design the PoC or pick water bodies.`
  : ''

phase('Collate')

const collatePrompt = `You are a scientific writer building the authoritative internal collation ("category README") for the "${CATEGORY}" category of a foundational literature review on harmful algal blooms (HABs), freshwater cyanobacteria focus.

You are given an EVIDENCE PACK (JSON at the end): an array of sources, each with key, title, tier (ACAD/FED/SLG/NGO/PVT), relevance, year, access level, and a list of already-verified claims (v: "Y" = verified against source, "P" = partial/caveated), plus key numbers and cross-source tensions. These claims already passed a per-source blind fact-check; "N"/unsupported claims were already removed. n_excluded_unverified records how many were dropped per source.

CATEGORY SCOPE: ${CAT_SCOPE}

Write readme_md as a well-structured Markdown document with these sections:
1. "# ${CATEGORY}" title + a 2-4 sentence overview of what this category covers.
2. "## What's well-established" — organized into 4-7 SUB-TOPIC subsections (use the scope above as a guide). State each finding in plain language and cite the supporting source key(s) inline as [KEY] or [KEY1; KEY2]. Where many sources agree, say so and cite the strongest few. Prefer claims marked "Y"; you may use "P" claims but phrase them with appropriate caution.
3. "## Contested / uncertain / poorly-established" — THIS SECTION IS REQUIRED AND IMPORTANT. Lay out, side by side, genuine disagreements and open questions where sources conflict or evidence is weak (e.g., competing positions with their respective source keys). Use the sources' "tensions" notes. Represent disagreement honestly; do not manufacture a false consensus. If a claim rests on a single source or abstract-only access, note that.
4. "## Key data / models / methods" — a compact Markdown table (name | what it does | where it works / fails | source key(s)).
5. "## Gaps & open questions" — what the literature does not yet resolve.${dataFeasibilityBlock}
6. "## Sources cited" — the list of source keys cited in this README.

RULES (fidelity gate):
- EVERY substantive claim must cite at least one [KEY] that exists in the pack. Do NOT invent keys, sources, numbers, or findings not present in the pack.
- Correlation is not causation — phrase driver/treatment/effect claims carefully; flag where a claim is correlational.
- When you state a quantitative value, cite the source key and keep units; do not round away meaning.
- Prefer breadth of coverage: try to draw on most of the pack's sources across the sub-topics, not just a handful. Put every key you cite into keys_cited, and list any pack keys you did NOT cite in keys_not_cited (with the expectation those are genuinely peripheral).

EVIDENCE PACK (JSON):
${JSON.stringify(PACK)}`

const collation = await agent(collatePrompt, { label: 'collate:' + CATEGORY, phase: 'Collate', schema: COLLATE_SCHEMA, model: 'sonnet' })

if (!collation) {
  log('Collate stage failed for ' + CATEGORY)
  return { category: CATEGORY, collation: null, review: null, error: 'collate_failed' }
}
log(CATEGORY + ' collated: ' + (collation.subtopics_covered || []).length + ' sub-topics, ' + (collation.keys_cited || []).length + ' keys cited, ' + (collation.contested_points_count || 0) + ' contested points')

phase('SynthReview')

const reviewPrompt = `You are a BLIND adversarial fact-checker performing SYNTHESIS-LEVEL review of a category README against its evidence pack. The per-source claims were already verified individually; your job is different: catch claims that live BETWEEN sources — comparative/aggregate/"most studies find"/"in contrast to"/"the consensus is" statements — that the README ASSERTS but the pack does NOT support.

Do this:
1. Read the README (below) and extract every cross-source / comparative / aggregate / consensus claim.
2. For each, check it against the EVIDENCE PACK (the same array of source claims the writer had). Is it supported by the cited key(s) and the pack as a whole?
3. Report unsupported_synthesis_claims: each with the problem and a suggested fix (soften / recite / remove).
4. Report keys_cited_not_in_pack: any [KEY] cited in the README that does not exist in the pack.
5. Report miscited_claims: claims attributed to a key whose pack entry does not actually support them.
Set overall to 'flag' if any unsupported synthesis claim or bad key citation exists, else 'pass'. Judge ONLY against the pack; do not use outside knowledge.

README (Markdown):
"""
${collation.readme_md}
"""

EVIDENCE PACK (JSON, ground truth):
${JSON.stringify(PACK)}`

const review = await agent(reviewPrompt, { label: 'synthreview:' + CATEGORY, phase: 'SynthReview', schema: REVIEW_SCHEMA, model: 'haiku' })

return { category: CATEGORY, collation: collation, review: review }
'''


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    max_kb = 0
    for cat in CATS:
        if only and cat != only:
            continue
        pack = json.load(open(os.path.join(EV_DIR, f"{cat}.json"), encoding="utf-8"))
        js = (JS_TEMPLATE
              .replace("__CAT__", cat)
              .replace("__CAT_SCOPE__", json.dumps(CAT_GUIDE[cat]))
              .replace("__IS_DATA__", "true" if cat in DATA_CATS else "false")
              .replace("__PACK_JSON__", json.dumps(pack)))
        path = os.path.join(SCRIPTS_DIR, f"phase4_{cat}.js")
        open(path, "w", encoding="utf-8", newline="\n").write(js)
        kb = len(js.encode("utf-8")) / 1024
        max_kb = max(max_kb, kb)
        print(f"  phase4_{cat}.js  {kb:.0f} KB  ({len(pack)} sources)")
    print(f"largest script: {max_kb:.0f} KB (limit 512 KB)")


if __name__ == "__main__":
    main()
