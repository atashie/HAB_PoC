# Research Methodology

How this foundational HAB research landscape was produced, in enough detail to audit and reproduce. The governing standard is the project's fidelity/transparency rule: **real, public, cited data only; every claim traceable to a source and to the code that produced it; contested and weak findings reported honestly.**

**Access date for all web pulls:** 2026-07-01. **Plan of record:** [`../docs/plans/2026-07-01-hab-research-landscape-plan.md`](../docs/plans/2026-07-01-hab-research-landscape-plan.md) (agreed with the lead, reviewed by an external tool before execution).

## Pipeline overview

The work ran in six phases. Fan-out used a deterministic multi-agent workflow harness; between phases the lead curated inline and checkpointed. All orchestration and post-processing scripts are checked in under [`scripts/`](scripts/).

| Phase | What happened | Model(s) | Artifact |
|---|---|---|---|
| 0 — Preflight | End-to-end smoke test on one real source (EPA CyAN) before scaling | Sonnet + Haiku | proved tools/models/schemas; found WebFetch non-determinism |
| 1 — Discovery | ~17 parallel search lanes across {5 categories}×{5 tiers} + targeted program/topic queries | Sonnet | 299 raw candidates |
| 2 — Curation | Dedup (URL + content-ID), tier/category/relevance assignment, citation keys | deterministic (Python) + lead | [`SOURCE-REGISTRY.md`](SOURCE-REGISTRY.md), 261 unique |
| 3 — Per-source | For each source: fetch/pre-extract → structured summary → blind verify-against-source review → resolve | Sonnet (summary), Haiku (review) | 261 dossiers in [`_sources/`](_sources/) |
| 4 — Collation | One agent per category: collate verified claims into a keyed README, then blind synthesis-review of cross-source claims | Sonnet (collate), Haiku (review) | 5 category READMEs |
| 5 — Assembly | Master references (deterministic), top-level orientation, this file, decisions log | deterministic (Python) + lead | this document set |

## Discovery (Phase 1)

Search was intentionally multi-modal to reduce blind spots: ~17 independent lanes, each searching a different slice of the matrix of five categories × five source tiers, plus dedicated lanes for federal programs/data portals, guideline values & state/local programs, NGO/intergovernmental & private sector, and a lane explicitly hunting **reviews and stated knowledge gaps** (so the contested sections would have material). Each lane logged its queries and returned candidate sources with a provisional tier, category, and relevance. Raw candidates are cached at [`_discovery/candidates-raw.json`](_discovery/candidates-raw.json).

## Source tiers & citation keys

Every source has a key whose prefix encodes provenance priority (used for coverage emphasis and defensibility weighting, **not** exclusion — all tiers are represented and every collated claim records the tier of its support):

`ACAD` peer-reviewed journals › `FED` US federal agencies › `SLG` state/local government › `NGO` non-profit / academic institute / intergovernmental (WHO, IOC-UNESCO) › `PVT` private sector (incl. SePRO and competitors).

Dedup was two-stage and deterministic: by normalized URL, then by extracted content ID (PMC / arXiv / bioRxiv / DOI) so the same paper reached via different URLs merged to one source, preferring the primary publisher/DOI/.gov URL. 299 raw → 261 unique.

## Per-source dual-agent review (Phase 3) — the core rigor mechanism

Each source went through **summarize → blind verify-against-source**:

1. **Summarize (Sonnet).** Fetch the source and produce a structured dossier: what it is, key claims (each with a paraphrased evidence note + exact location, and a short verbatim quote only for a precise threshold/number/definition), data/numbers with units, methods, stated limitations, and cross-source tensions. The prompt forbids fabrication and forbids drawing on training knowledge: **every claim must be supported by the fetched text**; if only an abstract is reachable, that is declared and claims are limited to it.
2. **Blind review (Haiku).** A separate agent receives the **source text and the list of claims — but not the summarizer's reasoning** — and judges each claim against the source: supported (yes / partial / no), any hallucinated/misattributed number, any dropped caveat. This is the automated guard against the failure mode we care about most: a plausible-but-unsupported claim.
3. **Resolution.** Verdicts are stored *in each dossier* (every claim is tagged ✓ verified / ⚠ partial / ✗ UNVERIFIED), so the audit trail shows what was challenged. Claims the reviewer marked unsupported are **excluded from the category collations** (they remain in the dossiers for audit).

**Severity accounting across the 261 sources:** the large majority are "clean" or "notes" (faithful; reviewer noted a partial claim or a dropped caveat); a minority are "flagged" (≥1 claim the reviewer judged unsupported by the captured extract — typically a sub-claim inferred beyond the fetched text, which is then dropped from synthesis); two are "manual" (finalized by the lead — see Limitations). Per-source outcomes are in [`_sources/_processing-log.md`](_sources/_processing-log.md).

## Handling WebFetch non-determinism (a Phase-0 finding)

The preflight showed WebFetch renders pages via an intermediate model and returns **different subsets on repeated calls**. Consequences and mitigations, baked into the pipeline:
- **High-relevance sources were fetched twice** with different extraction prompts and reconciled (union), reducing single-fetch omission.
- **The blind reviewer verifies against the summarizer's returned source extract**, not an independent re-fetch — because an independent re-fetch produces false "unsupported" flags whenever the reviewer's fetch is thinner than the summarizer's.
- **PDFs were pre-extracted deterministically.** 29 sources were PDF URLs; a checked-in script ([`fetch_pdftext.py`](scripts/fetch_pdftext.py)) downloaded and extracted their text (pdfplumber/pypdf) to a local cache, which was fed to the summarizer as authoritative text. This was prompted by a real Phase-3 finding: an unparseable PDF (a *Nature Reviews* review) had caused one agent to confabulate regional statistics; deterministic pre-extraction plus a hardened anti-confabulation prompt fixed it, and the blind reviewer had caught it. 25/29 PDFs extracted cleanly; the other 4 fell back to the abstract path.

## Collation & synthesis review (Phase 4)

Per-source dossiers were compacted into per-category **evidence packs** (verified/partial claims + numbers + tensions; unverified claims excluded) by a checked-in script. For each category, one **collation agent** organized the pack into a README (well-established sub-topics + a required contested/uncertain section + a data/models/methods table + gaps; every claim keyed), and a **blind synthesis-review agent** then re-derived the cross-source / aggregate / "most studies" claims and verified them against the pack. This synthesis-level check exists because the per-source review cannot catch a claim that lives *between* sources. Four synthesis flags were raised across the five categories; all four were reconciled into the READMEs (attributions narrowed to the single supporting source, an over-broad headline softened, and a source's internal arithmetic discrepancy surfaced inline) — the verdicts and their resolutions are recorded in each category's `_synthesis-review.md`.

## Reproducibility

- **Data acquisition and post-processing are scripted** and checked in ([`scripts/`](scripts/)): curation/dedup, PDF text extraction, batch-workflow generation, dossier writing, evidence-pack extraction, collation writing, and this reference builder.
- **Citation integrity is machine-checked:** [`build_references.py`](scripts/build_references.py) confirms every `[KEY]` cited in the five READMEs resolves to a dossier (0 dangling at build time).
- Raw discovery candidates, the source registry, per-source processing log, and per-category synthesis-review verdicts are all retained.

## Limitations (known and disclosed)

- **Paywalls bias toward open literature.** Some peer-reviewed full texts were inaccessible; those sources were summarized from abstract/preprint/agency versions and are marked `access: abstract` (or `landing-only`/`blocked`) in [`REFERENCES.md`](REFERENCES.md), with claims limited accordingly. This under-weights closed-access findings.
- **WebFetch is a rendering, not raw HTML** (above) — residual omission risk remains despite double-fetch and PDF pre-extraction.
- **LLM summarization risk** is mitigated by the blind verify-against-source review but not eliminated; the review itself is an LLM and can err. Verdicts are transparent in the dossiers so a human can spot-check.
- **Two sources were finalized manually by the lead** (ACAD-113, paywalled with an elided abstract → metadata-only dossier, explicitly bounded; SLG-008, a transient pipeline drop → single main-loop fetch). Both are labeled `manual` and note they did not pass the dual-agent path.
- **Search/web drift:** results and pages change over time; the audit trail is the captured evidence + access date per source, not a guarantee a URL is unchanged later.
- **Correlation vs. causation:** most driver/treatment relationships in this literature are associational; the collations flag this inline wherever a causal reading might be inferred.
- **This is a landscape orientation,** not a modeling study: it characterizes real public data and methods (including a data-feasibility view) but does not fit a model or select water bodies — those are downstream.

## AI-assisted-work disclosure

This research was produced with heavy AI assistance under human direction, per the brief's allowance and its request to note where tools shaped the result. Search, fetching, per-source summarization, blind review, and category collation were performed by orchestrated LLM agents (Sonnet and Haiku tiers); curation, dedup, references, and integrity checks are deterministic Python; the lead (Opus tier) set the design, checkpointed at the registry, reconciled the synthesis-review flags, and authored the orientation/methodology/decisions documents. The blind-review and synthesis-review layers exist specifically so that AI-generated claims are checked against sources rather than trusted, and so a human can audit any claim via its dossier.
