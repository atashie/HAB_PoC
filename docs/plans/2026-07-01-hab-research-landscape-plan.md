# HAB Research Landscape — Execution Plan (DRAFT for review)

**Date:** 2026-07-01
**Author:** Claude (Opus 4.8) with Arik
**Status:** DRAFT — pending Arik's agreement, then codex review, before any research is run.
**Scope of this plan:** Phase 1 of the SePRO HAB PoC — a foundational literature/landscape orientation. This plan governs *research only*. It does **not** touch Part A analysis, Part B tool, or Part C platform.

---

## 1. Objective & framing

Build a **defensible baseline understanding of harmful algal blooms (HABs)** that will underpin every downstream deliverable. The guiding questions at this stage are deliberately *not* "how do we use this for the PoC?" but:

- What is the current scientific understanding of HABs (esp. freshwater cyanobacterial HABs)?
- What causes them / drives them? What is well-established vs. contested?
- Where is the genuine uncertainty in the field?
- What models, tools, and methods exist to detect, describe, or predict them?
- Where and when do those methods work well, and where do they fail?
- What data exist (remote-sensing + in-situ + weather), and what are their known limitations?
- What treatment/management options exist and what does the evidence say about their efficacy?

**Non-goal (this phase):** designing the PoC, choosing a modeling approach, or picking specific lakes. Those come later and will *draw on* this research.

**In-scope, added per review:** a lightweight **data-feasibility characterization** — for the real, public datasets we survey, what is their spatial/temporal coverage, resolution, latency, detection limits, and (critically) do the remote-sensing and in-situ sources actually *join* in space and time? This is baseline data understanding the brief explicitly asks for ("gaps, biases, sampling artifacts, and detection limits") and it keeps the research converging on something buildable — without yet choosing an approach or a water body.

**Scope boundary:** Freshwater cyanobacterial HABs are the center of gravity (matches the brief, CyAN, and SePRO's business). Marine/coastal/brackish HAB science is included **only where its methods or drivers transfer** (e.g., satellite chlorophyll retrieval, nutrient-limitation theory), and is flagged as such.

---

## 2. Locked decisions (from Arik) + proposed defaults

**Locked:**
1. **Breadth: Exhaustive** — chase broad coverage across all five source tiers, including niche and contradictory findings. (~80–120+ sources.)
2. **Categories: Five** — `basic-science`, `remote-sensing`, `in-situ-and-weather-data`, `models-and-methods`, `treatment-and-management`.
3. **Adversarial review: verify-against-source** — a blind Haiku subagent receives the source text + the summary's claims (but *not* the summarizer's reasoning) and hunts for overclaims, misattributed/hallucinated numbers, and dropped caveats.
4. **Time and token cost are explicitly not constraints** (Arik's directive, 2026-07-01). This foundation may seed the *real* production tool, not just the interview deliverable, so we optimize for a great, fit-to-purpose result and accept "over-robust." Codex's proportionality/time concern is noted and deliberately overruled. The only trimming permitted is deduping genuinely redundant sources (quality hygiene, not cost-cutting).

**Proposed defaults (veto any):**
- Retain **per-source review files** (not just category collations) for full traceability.
- **Citation-key system** — every claim in every collation links to a source key; keys resolve in a master `REFERENCES.md`.
- **Relevance tiers: High / Medium / Low**, with a rigor gradient (see §4).
- Each category file has an explicit **"Contested / uncertain / poorly-established"** section.
- **Paywall honesty:** prefer open-access / preprint / agency-hosted full text; when only an abstract is reachable, mark `full_text_access: abstract` and cap the claims we draw from it. Never infer beyond what we can read.
- **Access date = 2026-07-01** for all pulls; every search query logged.
- Correlation-vs-causation flagged inline wherever a driver/treatment implication appears.

---

## 3. Source tiers & citation-key scheme

Sources are keyed by tier prefix + zero-padded number. The prefix encodes the brief's priority ordering, so the key itself carries provenance weight (peer-reviewed vs. vendor white paper).

| Prefix | Tier | Examples |
|--------|------|----------|
| `ACAD` | Academic / peer-reviewed journals | *Harmful Algae*, *Limnology & Oceanography*, *Water Research*, *Remote Sensing of Environment* |
| `FED`  | U.S. federal agencies | EPA (CyAN, NARS), USGS (NWIS, dataRetrieval), NOAA/NCEI, NASA |
| `SLG`  | State & local government | State DEQs, state health departments, regional water authorities, bloom-advisory programs |
| `NGO`  | NGOs / non-profits / non-journal institutes / **intergovernmental** | GLEON, Woods Hole, university centers; WHO & IOC-UNESCO tagged `source_type: intergovernmental` |
| `PVT`  | Private sector | Instrument/algaecide vendors (incl. SePRO), consultancies, commercial data providers |

Example keys: `ACAD-001`, `FED-014`, `SLG-002`, `NGO-005`, `PVT-003`.

**Tier priority is about coverage emphasis and defensibility weighting, not exclusion.** Academic + federal will be the densest, but all five tiers are represented, and every collated claim records the tier of its supporting source(s) so we always know whether a claim rests on peer review or a vendor page. All sources named in the brief are seeded as **High** relevance by fiat.

---

## 4. Relevance taxonomy & rigor gradient

| Relevance | Definition | Treatment |
|-----------|------------|-----------|
| **High** | Provides directly-usable data, a model/method, quantitative findings, or authoritative thresholds — **or** is a brief-listed source. | Full deep-read → structured summary w/ verbatim excerpts → Haiku verify-against-source review. |
| **Medium** | Useful context, background, or synthesis without directly-usable data/method. | Standard summary → Haiku review. |
| **Low** | Tangential, peripheral, or duplicative. | Registry entry + one-line note; **no** full pipeline. Logged explicitly as low so the omission is visible (no silent truncation). |

Relevance is recorded in the source registry and in each review file's frontmatter. A source touching multiple categories is reviewed **once** (single source of truth) and cited by key from every relevant collation.

---

## 5. Folder & file structure

```
Research/
  README.md              # top-level: plain-language summary of all 5 categories + links (the "orient" doc)
  REFERENCES.md          # master works-cited: every key -> full citation (name, org/author, year, URL, access date, tier, relevance, categories)
  METHODOLOGY.md         # how the research was run: queries, tools, dates, the review process, and limitations (reproducibility/audit)
  DECISIONS-LOG.md       # running assumptions & trade-offs
  SOURCE-REGISTRY.md     # candidate -> confirmed source list w/ tier, category(s), relevance, review status
  _sources/              # ONE review file per source, flat, keyed (avoids duplication for multi-category sources)
    ACAD-001-<slug>.md
    FED-003-<slug>.md
    ...
  basic-science/README.md
  remote-sensing/README.md
  in-situ-and-weather-data/README.md
  models-and-methods/README.md
  treatment-and-management/README.md
```

**Why flat `_sources/` instead of per-category source folders:** many sources are relevant to 2+ categories; a flat, keyed store means one review per source (no duplication, no drift), and the category collations reference by key. Category subfolders hold the *synthesis*, which is what the brief's readers actually consume.

---

## 6. Per-source review file schema

Frontmatter:
```yaml
key: ACAD-001
title: ...
authors_or_org: ...
year: ...
url: ...
access_date: 2026-07-01
tier: ACAD            # ACAD|FED|SLG|NGO|PVT
source_type: journal-article   # journal-article|agency-report|dataset|guideline|white-paper|advisory|intergovernmental|...
categories: [basic-science, models-and-methods]
relevance: High       # High|Medium|Low
full_text_access: full   # full|preprint|abstract
review_status: pass   # pass|flagged|corrected
```
Body:
1. **What it is** — one paragraph.
2. **Key claims / findings** — each as a bullet, *each paired with a paraphrased evidence note + exact location (page/section/table)*. Short verbatim quotes only where precision demands it (a specific threshold, a definition, a contested figure) — never bulk-copy copyrighted journal text. The blind reviewer sees the full fetched source text at review time; we store lean, targeted evidence, not the source.
3. **Data / numbers** — with units, and baselines/uncertainties where the source gives them.
4. **Methods / models** (if any) — what, and where it's said to work/fail.
5. **Stated limitations** — the source's own caveats.
6. **Tensions** — where this contradicts or complicates other sources (cross-linked by key).
7. **Blind Haiku adversarial review** — the reviewer's structured verdict (per-claim pass/flag + overall).
8. **Flag resolution** — what we did about any flags (removed claim, softened language, marked contested).

---

## 7. Category collation schema (`<category>/README.md`)

1. **Overview** — what this category covers, in plain language.
2. **What's well-established** — sub-topics with cited claims `[KEY]`.
3. **Contested / uncertain / poorly-established** — explicit, honest; competing claims laid side by side with their sources.
4. **Key data / models / methods** — compact table (name, what it does, where it works/fails, source).
5. **Gaps & open questions.**
6. **Local references** — the subset of the master list cited here, by key.

**Data categories additionally** (`remote-sensing`, `in-situ-and-weather-data`): a **Data-feasibility & coverage** subsection — per surveyed public dataset, its spatial/temporal coverage, resolution, latency, detection limits, access method, and known spatial/temporal overlap with the other modality (do the satellite and in-situ records actually join?). Characterization of real public data, not PoC design.

Rule: **no claim without a key.** If a claim can't be traced to a reviewed source, it doesn't go in.

---

## 8. Orchestration (executes only after approval + codex review)

The heavy fan-out uses the **Workflow** tool (deterministic multi-agent orchestration — matches your ask for per-source subagent review). I scout and curate *inline* between workflow phases to control cost and quality, per Workflow best practice.

**Phase 0 — Preflight (hard gate; must pass before any fan-out).**
Confirm the execution stack actually works before committing to the big run: (a) a workflow subagent can successfully call **WebSearch** and **WebFetch**; (b) the intended **model tiers** (Sonnet 5 summarize, Haiku 4.5 review) are reachable and the schema/structured-output path works on a single trial source end-to-end (fetch → summarize → blind review → structured verdict); (c) confirm effective **concurrency** cap. **Fallback mode:** if workflow subagents cannot use WebSearch/WebFetch, I drive discovery/fetch from the main loop and hand fetched text to review subagents. Preflight runs one real source through the full pipeline as a smoke test; if it fails, we fix the harness before scaling — we never launch 200+ calls on an unproven path.

**Phase 1 — Discovery sweep (Workflow, parallel multi-modal search).**
Fan out search agents across the matrix of {5 categories} × {5 tiers} plus targeted program/topic queries (CyAN, WQP, NWIS, NARS, NOAA/NCEI; and topics like microcystin thresholds, N-vs-P limitation debate, satellite chlorophyll/phycocyanin algorithms, algaecide efficacy). Each returns candidate sources (title, org/author, year, URL, provisional tier + category, one-line why-relevant). Different agents search different angles so coverage is broad. → candidate list.

**Phase 2 — Curation & triage (inline, me).**
Dedup; assign tier + category(s) + provisional relevance; drop non-authoritative junk; ensure tier/category balance; seed all brief sources as High. Produce `SOURCE-REGISTRY.md` — the confirmed work-list with citation keys. **Checkpoint:** I show you the registry before the expensive deep-read (cheap insurance against spending tokens on the wrong sources).

**Phase 3 — Per-source pipeline (Workflow, `pipeline()`).**
For each High/Medium source, independently:
- *Stage A — deep-read & summarize* (Sonnet): WebFetch the source and produce the structured summary + paraphrased evidence + provisional relevance/category, per §6. **For High-relevance sources, WebFetch twice with different extraction prompts and reconcile** — the Phase 0 preflight showed WebFetch renders pages via an intermediate small model that returns *different subsets* on each call, so a single fetch non-deterministically drops content. Stage A returns, alongside its claims, the `source_extract` (the reconciled fetched text) it based them on.
- *Stage B — blind adversarial review* (Haiku): receives Stage A's `source_extract` + the claims (but **not** Stage A's reasoning), and verifies each claim *against that extract*: supported? number matches? caveat present in the extract but dropped from the claims? **It verifies against the returned extract, not an independent re-fetch** — the preflight showed an independent re-fetch produces false "unsupported" flags whenever the reviewer's fetch is less complete than the summarizer's.
- *Stage C — resolution* (conditional): if flagged, reconcile (remove/soften/mark-contested).
Sources flow independently (no barrier). → structured results, which **I** write to `_sources/*.md` (workflow agents can't touch the filesystem; they return data, I persist it). The transient `source_extract` is used only for verification and is **not** persisted in bulk (per §6 / Finding #5).

**Phase 4 — Per-category collation + synthesis review (Workflow, `pipeline`, one chain per category).**
- *Stage A — collate:* an agent reads all reviewed sources tagged to its category and writes the §7 collation, using only passed/contested-flagged claims.
- *Stage B — synthesis review* (the fix for a gap the source-level Haiku pass can't catch): a second, blind agent re-derives every **cross-source / comparative / synthesis** claim in the README (e.g. "most studies find X," "in contrast to Y," "the consensus is Z") and checks it against the cited source keys and their review files. Unsupported synthesis claims are flagged and removed or softened before the README is finalized. Source-level excerpt checking already happened in Phase 3; this pass exists specifically because collation can introduce claims that live *between* sources.

**Phase 5 — Assembly (inline, me).**
Write `README.md` (top-level summary + links), `REFERENCES.md`, `METHODOLOGY.md`, `DECISIONS-LOG.md`. Verify (not merely spot-check) that every citation key in every collation resolves in `REFERENCES.md`, that contested items are represented, and that the synthesis-review flags from Phase 4B were all resolved.

**Model-per-stage (cost control):** discovery = Sonnet/Haiku; summarize = Sonnet 5; review = Haiku 4.5 (as specified); collation = Sonnet 5; curation + final assembly = me (Opus). **Resumability:** the per-source workflow is long; if it dies I resume from its runId (cached prefix returns instantly).

---

## 9. Adversarial review design (the core rigor mechanism)

- **Blind:** the Haiku reviewer never sees the summarizer's reasoning, confidence, or notes — only the source extract and the list of claims to check. It forms an independent judgment.
- **Verify-against-source:** for each claim, the reviewer answers: *Is this supported by the source text? Is any number misattributed or invented? Is a material caveat dropped?* The "source text" is the `source_extract` Stage A fetched and returned (see §8) — **not** an independent re-fetch, because WebFetch's rendering is non-deterministic and re-fetching yields false "unsupported" flags (Phase 0 finding).
- **Structured verdict** (JSON schema): `{ per_claim: [{claim, supported: yes|no|partial, issue}], hallucinated_numbers: [...], dropped_caveats: [...], tier_ok: bool, overall: pass|flag }`.
- **Resolution:** flagged claims are removed, softened, or explicitly marked contested — never silently kept. The verdict is stored *in the source's review file* so the audit trail shows what was challenged and how it resolved.

This directly serves the fidelity standard: it is our automated guard against the failure mode we care about most — a plausible-sounding but unsupported or fabricated claim slipping into the record.

---

## 10. Fidelity & traceability guarantees (the claim gate, applied to research)

Every claim that lands in a collation must:
1. **Trace** to a cited real source (key → `REFERENCES.md` → URL + access date).
2. **Regenerate** — search queries and the workflow script are logged/checked in.
3. Carry its **evidence quality** — tier of source, and whether full text or abstract-only.
4. Be **bounded** — contested/uncertain claims live in the contested section, not stated as settled.

Synthetic data: **none** at this phase (this is literature review). Correlation≠causation flagged wherever a driver/treatment link is asserted.

---

## 11. Scale (for planning, not for trimming)

Rough order of magnitude so we know what we're launching: ~20–30 discovery-search agents; ~90–120 sources × (summarize + review) ≈ 200–260 agent calls; ~5–8 collation + synthesis-review agents. Call it **~230–300 subagent calls**, mostly Sonnet/Haiku, well under the 1000-agent cap. Wall-clock likely a few hours at ~10–16 concurrency (fetch-latency bound).

**Per Arik's directive, we do not trim for time or token cost.** The only reduction applied is **deduplication** of genuinely redundant sources (e.g., five re-hosts of the same press release → one), which is quality hygiene. Any dedup is logged in `SOURCE-REGISTRY.md` so nothing is silently dropped.

---

## 12. Risks & limitations (known now)

- **Paywalls** — some peer-reviewed full texts are inaccessible; we lean on open-access/preprint/agency syntheses and mark abstract-only sources. This biases toward open literature; noted in `METHODOLOGY.md`.
- **Web drift** — search results and pages change over time; our audit trail is the excerpt + access date captured per source, not a guarantee the URL is unchanged later.
- **WebFetch is a rendering, not raw HTML** (confirmed in Phase 0) — WebFetch answers a prompt via an intermediate small model rather than returning raw page text, and returns *different subsets* on repeated calls. So "the source" we verify against is that rendering, with its own omission risk. Mitigations: double-fetch + reconcile on High-relevance sources; verify claims against the summarizer's returned extract (not a noisy re-fetch); and for any specific figure we intend to cite downstream (e.g., a threshold in the tool), fetch/verify with extra care against the primary document (and consider a raw fetch for PDFs).
- **LLM summarization risk** — mitigated by the blind verify-against-source review, but not eliminated; residual risk is logged.
- **Tier mapping edge cases** — intergovernmental bodies (WHO, IOC-UNESCO) are keyed `NGO` but tagged `intergovernmental`; noted so their authority isn't understated.
- **Tool/stack availability** — now handled by the Phase 0 preflight hard gate (§8), not left to chance: if workflow subagents can't use WebSearch/WebFetch, we switch to the documented fallback before scaling.

---

## 13. Deliverables checklist

- [ ] `Research/SOURCE-REGISTRY.md` (checkpointed with Arik)
- [ ] `Research/_sources/*.md` — one reviewed file per High/Medium source
- [ ] `Research/{basic-science,remote-sensing,in-situ-and-weather-data,models-and-methods,treatment-and-management}/README.md`
- [ ] `Research/README.md` — top-level orientation summary + links
- [ ] `Research/REFERENCES.md` — master works-cited
- [ ] `Research/METHODOLOGY.md` — queries, tools, dates, review process, limitations
- [ ] `Research/DECISIONS-LOG.md` — assumptions & trade-offs

---

## 14. Execution sequence & checkpoints

1. Arik agrees this plan (or edits). — **done (approved 2026-07-01, with the time/cost-not-a-constraint directive).**
2. **codex reviews this plan** (gate — no research before this). — **done.**
3. Incorporate codex feedback (Findings #2–#6; #1 overruled by Arik). — **done (this revision).**
4. **Phase 0 preflight (hard gate):** smoke-test one real source end-to-end. — **done (2026-07-01, run wf_899ce392-309): PASS.** WebSearch+WebFetch in subagents, Sonnet summarize, Haiku blind review, and structured output all work. Finding: WebFetch is non-deterministic (§12) → Phase 3 refined to double-fetch High sources + verify against the returned extract (§8, §9).
5. Run **Phase 1** (discovery) → **checkpoint: registry review with Arik**.
6. Run **Phase 3** (per-source pipeline: summarize → blind review → resolve).
7. Run **Phase 4** (collation + synthesis review).
8. **Phase 5** assembly → self-review against the claim gate.
9. Hand off to the next phase (Part A analysis) — out of scope here.
