# HAB Research — Foundational Landscape

**What this is.** A defensible, traceable baseline of the current scientific and operational understanding of **harmful algal blooms (HABs)**, with a center of gravity on **freshwater cyanobacterial HABs** (the SePRO case-study focus). It answers *what is known, what is contested, what data/models/methods exist, and where they work or fail* — deliberately **not** "how do we build the PoC" (that is downstream). Everything here traces to real, public, cited sources.

**How to read it.** Five category collations hold the synthesis; each claim carries a citation key `[KEY]` that resolves in [`REFERENCES.md`](REFERENCES.md). Each category README has a **"What's well-established"** section and — importantly — an explicit **"Contested / uncertain / poorly-established"** section, because a great deal of this field is genuinely unsettled.

## The five categories

| Category | Sources cited | What it covers | Contested points |
|---|---|---|---|
| [basic-science](basic-science/README.md) | 70 | Bloom biology & taxa; nutrient (N-vs-P) drivers; temperature/stratification/hydrology; cyanotoxins & health; climate-change trends & attribution; succession/physiology | 6 |
| [remote-sensing](remote-sensing/README.md) | 43 | Satellite detection (Cyanobacteria Index, phycocyanin, chlorophyll-a); sensors & missions (MERIS→OLCI→Sentinel-2/Landsat→PACE); atmospheric correction; validation, resolution & revisit limits | 7 |
| [in-situ-and-weather-data](in-situ-and-weather-data/README.md) | 46 | In-situ data infrastructure (Water Quality Portal, NWIS, NARS/NLA); harmonized chlorophyll & cyanotoxin datasets; weather/climate covariates; sampling design, biases, detection limits; **data-feasibility & satellite↔in-situ join** | 7 |
| [models-and-methods](models-and-methods/README.md) | 43 | Statistical/ML forecast & risk models; mechanistic/process-based models; satellite+in-situ+weather fusion & early warning; validation, skill metrics, leakage, spatiotemporal CV | 8 |
| [treatment-and-management](treatment-and-management/README.md) | 60 | Copper & hydrogen-peroxide algaecides; nutrient/watershed management (P & N, TMDLs, BMPs, alum, biomanipulation); in-lake physical controls; guideline values & advisory frameworks; **data-feasibility** | 8 |

## The ten things most worth knowing (each links to where it's substantiated)

1. **Eutrophication + warming are the two agreed catalysts** of rising cyanobacterial blooms, but *which dominates the global trend is explicitly unresolved* in the current literature — case studies point both ways. → [basic-science](basic-science/README.md)
2. **The nitrogen-vs-phosphorus control debate is live, not settled.** The classic P-only paradigm (37-year whole-lake ELA experiment) is directly challenged by a large body of work arguing dual N+P reduction is needed where non-N-fixing genera dominate. → [basic-science](basic-science/README.md)
3. **The reported "global increase" in HABs is itself contested** — one rigorous analysis finds no significant global trend once monitoring effort is adjusted; a *Nature* rebuttal challenges the influential satellite-trend paper on sediment-plume confounding. → [basic-science](basic-science/README.md)
4. **Satellite biomass ≠ toxin.** The operational Cyanobacteria Index detects bloom *presence* reasonably (≈84% accuracy vs. combined ground truth) but has **no signal for toxin identity or concentration**, and proxy indicators (chlorophyll, cell counts) systematically **over-predict** toxin-based risk vs. direct measurement. → [remote-sensing](remote-sensing/README.md), [in-situ](in-situ-and-weather-data/README.md)
5. **A hard physical floor limits satellite cyanoHAB detection**: cyanobacteria-specific (phycocyanin) features only resolve above ~chl-a 20 mg/m³, and the 300 m operational pixel cannot see most small lakes or nearshore scums — ~80% of state-reported events fell on waterbodies too small to resolve. → [remote-sensing](remote-sensing/README.md)
6. **A published satellite+in-situ+weather fusion analog exists at national scale** (INLA over 2,192 U.S. lakes): ~90% accuracy on a true out-of-sample year — *but only ~49% precision*, a base-rate caveat that must travel with the headline. → [models-and-methods](models-and-methods/README.md)
7. **Persistence is a stiff baseline.** Week-to-week bloom state is strongly autocorrelated (AR1 ≈ 0.90); much apparent short-horizon "skill" may be persistence, and fusion authors don't expect accuracy beyond ~2 weeks — any PoC must beat a persistence/climatology baseline to claim value. → [models-and-methods](models-and-methods/README.md)
8. **Simple, explainable models are competitive.** Tree/gradient-boosted methods match or beat deep learning in single-site studies; water temperature is the single most frequent top predictor across ML studies. → [models-and-methods](models-and-methods/README.md)
9. **Every lysis-based treatment carries a suppression-vs-toxin-release trade-off** — copper and H₂O₂ kill cells but release intracellular toxin into the dissolved (more bioavailable) fraction rather than degrading it; this does *not* apply to alum, nutrient management, or biomanipulation. → [treatment-and-management](treatment-and-management/README.md)
10. **The public data plumbing is mature but not seamless.** WQP federates 400+ agencies and 430M+ records, but NWIS/WQX site IDs are unharmonized, refresh on different schedules, and satellite↔in-situ joins are non-trivial in space and time. → [in-situ-and-weather-data](in-situ-and-weather-data/README.md)

## Supporting documents

- [`REFERENCES.md`](REFERENCES.md) — master works-cited; every `[KEY]` resolves here (261 sources; 0 dangling citations).
- [`METHODOLOGY.md`](METHODOLOGY.md) — how this was produced: search sweep, per-source dual-agent summarize→blind-review, synthesis review, tools, dates, and honest limitations.
- [`DECISIONS-LOG.md`](DECISIONS-LOG.md) — assumptions and trade-offs taken along the way.
- [`SOURCE-REGISTRY.md`](SOURCE-REGISTRY.md) — the curated candidate list (tiers, categories, relevance) that seeded the deep read.
- [`_sources/`](_sources/) — the 261 per-source dossiers (one file per source), each with claims tagged by a blind fact-checker's verdict.

## Corpus at a glance

- **261 sources**, tiered by provenance: **ACAD** 148 (peer-reviewed) · **FED** 78 (EPA/USGS/NOAA/NASA/CDC) · **SLG** 13 (state/local) · **NGO** 13 (incl. WHO, IOC-UNESCO) · **PVT** 9 (incl. SePRO & competitors).
- All six brief-listed source families are covered and tiered High (EPA CyAN, Water Quality Portal, USGS NWIS/`dataRetrieval`, EPA NARS/NLA, NOAA/NCEI, state DEQ programs).
- **250** sources are cited in the synthesis; the remaining 11 are peripheral (program landing pages, corporate PR, near-duplicate product pages) and remain documented as dossiers — no source was silently dropped.
- Fidelity posture: real public data only; each dossier's claims were verified against the source by a blind reviewer; unverified claims were excluded from the collations; contested and single-source/abstract-only findings are flagged as such, not smoothed over.

*Scope caveat.* Freshwater cyanobacteria are the focus; marine/coastal HAB science appears only where methods or drivers transfer, and is flagged where it does. This is a literature/landscape orientation — it characterizes real public data and methods but does not itself design a model or select water bodies.
