# Decisions & Trade-offs Log — Research Phase

A running record of the substantive choices, assumptions, and trade-offs made during the foundational research phase. The brief asks for both assumptions and trade-offs to be surfaced rather than buried; this is that record. Dated 2026-07-01 unless noted.

## Framing & scope

- **Landscape-first, not PoC-first.** We treated this phase as building baseline understanding ("what is known / contested / available"), explicitly deferring "how do we build the tool." *Trade-off:* slower path to a demo, but it grounds every downstream claim in cited evidence and surfaces the field's genuine uncertainty before we commit to a modeling frame. A data-feasibility lens was added to the two data categories (per external review) so the research still converges on something buildable.
- **Freshwater cyanobacteria as the center of gravity.** Matches the brief, EPA CyAN, and SePRO's business. *Assumption/trade-off:* marine/coastal HAB science is included only where methods or drivers transfer (e.g., satellite chlorophyll retrieval, nutrient theory) and flagged as such — so some marine-only findings (e.g., the effort-adjusted global-trend analysis) are noted as not established for freshwater.
- **Exhaustive breadth, and time/cost explicitly not a constraint** (lead's directive, overriding the brief's 6–8h research timebox for this phase) — because this foundation may seed the real production tool. *Trade-off:* substantially more sources and agent calls than a minimal pass; justified by the directive and the fidelity standard. The only reduction applied was deduping genuinely redundant sources (logged, never silent).

## Sourcing & curation

- **Five categories** (`basic-science`, `remote-sensing`, `in-situ-and-weather-data`, `models-and-methods`, `treatment-and-management`) rather than the looser three originally sketched — splitting the spectral signal and the treatment/recommendation half into first-class buckets, matching the brief's spectral-plus-aquatic, claims-defensible spirit.
- **Provenance-tiered citation keys** (ACAD›FED›SLG›NGO›PVT). *Assumption:* peer-reviewed and federal sources carry more defensibility weight, but tiers drive emphasis, not exclusion — vendor and state sources are retained and every claim records its support's tier.
- **All brief-listed sources seeded as High relevance** by fiat, and all six families confirmed present (EPA CyAN, Water Quality Portal, USGS NWIS/`dataRetrieval`, EPA NARS/NLA, NOAA/NCEI, state DEQ programs).
- **Flat, keyed `_sources/` store** (one dossier per source) rather than per-category source folders, because ~12 sources span multiple categories; the category READMEs cite by key so there is a single source of truth per source and no duplication/drift.
- **11 of 261 sources are uncited in the synthesis.** These are peripheral (program landing pages, corporate PR, near-duplicate product pages). *Trade-off:* kept as documented dossiers rather than deleted, so the omission is visible and auditable, not silent.

## Rigor mechanisms

- **Blind verify-against-source review on every source** (Haiku sees the source text + claims, not the summarizer's reasoning). *Trade-off:* ~2× the agent calls per source, but it is our primary guard against fabrication and the reason we can stand behind the claims.
- **Unverified claims excluded from collations.** Claims a reviewer marked unsupported are dropped from the synthesis (still visible in dossiers). *Assumption:* better to under-claim than to carry an unsupported statement into a document that feeds a product claim.
- **Synthesis-level review added** (per external review) — a second blind pass over each category README's cross-source claims, because per-source review cannot catch claims that live between sources. It flagged 4 issues across 5 categories; all were reconciled.
- **Contested/uncertain is a required section** in every category README, with competing positions laid side by side and single-source/abstract-only claims flagged. *Rationale:* the fidelity standard treats an honest negative/uncertain result as a deliverable, not a failure.

## Technical trade-offs discovered during execution

- **WebFetch is non-deterministic** (returns different subsets per call) and is a rendering, not raw HTML. Mitigations: double-fetch + reconcile on High sources; verify against the returned extract, not a re-fetch; deterministic PDF pre-extraction for 29 PDF sources. *Residual risk:* omission, disclosed in `METHODOLOGY.md`.
- **One confabulation was caught and fixed.** An unparseable *Nature Reviews* PDF led an early agent to invent regional statistics; the blind reviewer caught it, and we responded with deterministic PDF text extraction + a hardened anti-confabulation prompt (no filesystem/Read claims; every claim must trace to fetched text). *This is exactly the failure mode the review layer exists to catch.*
- **Sequential vs. parallel batching.** Launching many workflow batches at once tripped both a session limit and a server-side throttle; we converged on running batches largely one-at-a-time. *Trade-off:* slower wall-clock, higher reliability — acceptable given time is not the binding constraint. A self-healing "remaining-work" generator (recompute the outstanding set from the processing log each round) made the process robust to partial failures.
- **Two sources finalized manually** (ACAD-113 paywalled/abstract-elided → metadata-only; SLG-008 transient drop → single fetch). Labeled `manual`, bounded explicitly, and noted as not having passed the dual-agent path.

## Explicitly deferred to later phases

- Choosing the PoC framing (risk forecasting vs. early-warning anomaly detection vs. driver/treatment analysis).
- Selecting specific lakes/regions and the modeling approach and stack.
- Building the satellite↔in-situ join in practice (the research characterizes its feasibility and pitfalls but does not implement it).
- Any product-claim language — the research supplies the evidence base and its uncertainty bounds; claims are constructed downstream against the claim gate.

## Post-research additions

- **EPA-forecast supplemental appendices reviewed (2026-07-06).** Obtained and reviewed the two publisher
  supplements to ACAD-050/FED-017 (Schaeffer et al. 2024): `mmc1.docx` (Supplemental Material & Methods) and
  `mmc2.xlsx` (Table S1 — Florida-vs-CONUS metrics for the six comparison models). Review dossier:
  `epa-forecast/README.md`; addendum on the source note `_sources/ACAD-050-*.md`. *Why it matters:* it lets us
  **check that our own head-to-head represents the federal baseline faithfully.** Our out-of-sample FL 2025
  evaluation of the *deployed* forecast (`../models/outputs/epa_headtohead.md`: AUC-ROC 0.928, precision ≈0.73)
  **brackets** between EPA's CONUS INLA (precision 0.49, ~9% base rate) and their in-sample FL comparison
  models (precision 0.79–0.93, high FL base rate) — coherent once the base-rate and in-sample/out-of-sample
  differences are accounted for. *Conclusion:* baseline faithfully represented — neither flattered nor
  understated. *Trade-off/limit:* Table S1 reports the **comparison** models, not the INLA forecast (no
  published INLA-in-Florida number exists), so this is a consistency bracket, not a like-for-like identity.
  *Carry-forward:* (a) EPA's own cutoff is **0.10** (Youden) — score our EPA head-to-head at 0.10 for an
  apples-to-apples confusion matrix; (b) plain SVC collapses on the imbalanced CONUS set (precision 0.03) —
  our SVC family needs explicit imbalance handling; (c) the CONUS-trained model **dampens Florida's Nov–Dec
  secondary bloom peak** — a concrete place a FL-tuned model could add value (a hypothesis to test, not a claim).
