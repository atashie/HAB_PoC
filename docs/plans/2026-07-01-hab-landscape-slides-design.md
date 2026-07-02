# HAB Landscape Slides — Design (Part-A orientation deck, 2 topics)

**Date:** 2026-07-01. **Status:** design for confirmation before build.
**Goal:** two client-orienting slide topics answering "what is currently possible/available in HAB monitoring & forecasting" (Slide 1) and "what does the research frontier look like, and what drives the models" (Slide 2). Jargon-free; counts shown as simple barplots/tables.
**Output location:** `./presentation/` (pptx + reproducible code + data + figures).

> **2026-07-02 update — the EPA 7-day forecast (tool #2 / model #1, `ACAD-050`) is now INGESTED and is
> our baseline.** We reviewed, extracted, and QA'd it into `data-sources/cyano-forecasts/` (2,191 lakes ×
> 48 weeks, validated). It is a **validated federal baseline to judge our Part-A model against, or to
> leverage as a signal** — strategy + leakage caveats in
> [`2026-07-02-epa-cyano-forecast-as-baseline.md`](2026-07-02-epa-cyano-forecast-as-baseline.md). This
> reinforces its "established-operational" quality tier below (H4) and the tool↔model overlap note (M1).

## Locked decisions
- **Layout:** 2 lead slides + 2 appendix slides (full reference tables). ~4 slides.
- **Scope:** freshwater cyanoHAB only (no marine).
- **Quality:** evidence-anchored — show the concrete basis (validation metric, peer-reviewed?, operational vs experimental, year), not a bare badge.
- **Provenance:** every entity/attribute traces to a `./Research` dossier via citation key; unknowns = "not reported (n/r)," never guessed. (Claim gate applies.)

## Slide 1 — "The landscape of HAB tools you can use today" (operational products)
Dimensions per tool: **model type** (empirical remote-sensing / mechanistic / statistical-ML / in-situ-sampling / hybrid), **org type** (federal / state-local / private / academic / NGO / intl-govt), **time horizon** (nowcast / hindcast / forecast + lead time) & **refresh rate**, **spatial resolution**, **access** (free / paid / restricted), **year created**, **quality basis**.
- **Lead slide:** 3 barplots (count by org type; count by access; count by model type) + a timeline strip (year created) + 4-5 headline takeaways + a compact 6-row "representative tools" table.
- **Appendix slide:** full table, all tools × all columns, with citation keys.

## Slide 2 — "The research frontier & what drives the models"
Dimensions per model: **org type**, **algorithm** (random forest / gradient boosting / CNN-LSTM / Bayesian spatiotemporal-INLA / process-based / GLM / ANN / SVM…), **what it forecasts** (occurrence / likelihood / cell density / toxin / severity class), **spatial + temporal resolution**, **nowcast/hindcast/forecast**, and — emphasized — **features/datasets used** + **which are most important**.
- **Lead slide:** the hero is a **feature-frequency figure** (how many flagship models use each feature; water temperature highlighted as the most consistent top predictor) + a "which features are *most important*" callout + a compact 6-row flagship-models table.
- **Appendix slide:** full models table incl. the features/datasets column and reported skill, with citation keys.

## Candidate entities (from the corpus — veto/add welcome)

**Slide 1 — operational tools (~12):**
1. EPA CyAN / CyANWeb — federal, empirical RS (Cyanobacteria Index), 300 m, daily+7-day composites, free, 2015 [FED-008/009/010/048; ACAD-045/006]
2. EPA experimental 7-day cyanoHAB forecast — federal, statistical (Bayesian/INLA), 2,000+ lakes, 7-day forecast/weekly, free, 2024 [FED-060/012/016/017; ACAD-050]
3. NOAA Lake Erie HAB Forecast + bulletin — federal, mechanistic (hydrodynamic+particle) + satellite, nowcast + **≥96-hr (~4-day) bloom-position forecast + seasonal severity outlook**, twice-weekly bulletins (season), free, ~2008 (3-D sub-surface model added 2020); **skill = n/r in corpus** [FED-024/025/064/068; ACAD-024/051] *(ACAD-101 REMOVED — it is the global-trend study, not a Lake Erie model)*
4. NOAA HAB Monitoring System — federal, RS + model, near-real-time, free [FED-061]
5. Florida DEP Algal Bloom Dashboard — state, in-situ sampling + citizen reports, current status, free [SLG-001/007]
6. NY NYHABS notifications/map — state, in-situ + citizen, current status, free [SLG-003]
7. California SWAMP FHAB + satellite screening — state, RS screening + in-situ, free [SLG-012/006]
8. Ohio HAB response (Lake Erie region) — state, in-situ + satellite-supported advisories, free [SLG-004/005]
9. Utah / Oregon advisory systems — state, in-situ, current status, free [SLG-002/008]
10. BlueGreen BGi Water Health Intelligence — private, fusion (satellite+in-situ+weather), 2025, paid [PVT-001]
11. CyanoLakes — private, empirical RS **+ forecast (vendor-stated up to 3 weeks; "80%/70% at 1-/2-week lead" — vendor self-report, no baseline)**, subscription/paid, year n/r (~2015) [PVT-003]
12. EOMAP water quality — private, physics-based RS, paid [PVT-008]

*(Insight this surfaces: operational freshwater forecasting is dominated by US federal + state programs + a few private services; NGO/international-govt operational freshwater tools are essentially absent — worth stating.)*

**Slide 2 — cutting-edge models (~12):**
1. Bayesian spatiotemporal INLA fusion, 2,192 US lakes — occurrence prob., 7-day forecast; features: satellite CI + water temp + precip + lake morphology [ACAD-050]
2. R-INLA SPDE+AR1, 103 FL lakes — exceedance prob., 1-week forecast [ACAD-092/093]
3. Gradient boosting + attention CNN-LSTM ensemble — cell density, weekly; temp/pH/DO/nutrients/precip [ACAD-043]
4. Explainable LSTM + SHAP, 102 sites — bloom/chl, forecast; in-situ + ERA5; water temp top driver [ACAD-048]
5. CatBoost + SHAP (interpretable), Yilong Lake — likelihood, AUC 0.948 [ACAD-060]
6. Intelligible ML (XGBoost/rule-learner vs LSTM), Müggelsee — early warning, high-frequency [ACAD-037]
7. ANN vs SVM reservoir alert-level — occurrence/alert level; **6-7 day = efficient *sampling interval*, not a forecast lead time** [ACAD-001]
8. RF+boosting ensemble vs CNN/ANN — alert level, 78.7% acc [ACAD-117]
9. NOAA Lake Erie mechanistic transport (Lagrangian/Eulerian/property-carrying particle) — Microcystis biomass position, ≥96-hr forecast [ACAD-024]; companion toxin **transport/fate** (7-day, initialized from in-situ microcystin maps — *not* early warning) [ACAD-051]; buoyancy-resolving particle model [ACAD-100/FED-042] *(ACAD-101 REMOVED)*
10. Coupled hydrodynamic-algal biomass, Lake Taihu — short-term forecast [ACAD-052]
11. Multi-source fusion (Sentinel-2 + DEM + NOAA climate) — severity class; **top feature = longitude/geolocation (a regionally-learned, explicitly non-transferable *correlational* proxy — NOT a driver); temperature/precipitation/wind are contributing climate inputs** [ACAD-008]
12. WASP eutrophication process model, Lake Winnipeg — biomass, scenario **[ACAD-108]** *(was mis-keyed ACAD-110, which is a Comment/rebuttal on the Müggelsee ML paper)*
13. *(add)* Frontier synthesis: 168-study cross-review (1997–2025) — DL strongest in aggregate, hybrids highest accuracy [ACAD-068]
14. *(add)* Deep-learning surrogate of a Delft3D process model (hybrid), NSE 0.644→0.930 [ACAD-104]
15. *(add)* NASA PACE hyperspectral cyanoHAB validation (2026, R²=0.84 vs CyAN) — cutting-edge sensor [ACAD-106]

**Feature-importance synthesis (the Slide-2 emphasis):** water temperature = most consistent top predictor; then nutrients (TP/TN/TKN), precipitation, prior/antecedent bloom state (persistence), wind/mixing, light/solar, pH & dissolved oxygen, stratification, hydrology/residence time. Figure = count of flagship models using each feature category.

## Post-review corrections (Claude review, 2026-07-01 — all verified against dossiers & accepted)

**HIGH (fixed in entity lists above):** H1 WASP key ACAD-110→ACAD-108; H2 ACAD-101 removed from both Lake Erie entries (it's the global-trend study); H3 ACAD-008 top feature corrected to longitude/geolocation (non-transferable, correlational).

**H4 — quality tiers & feature-importance need a written, cited rubric (highest fidelity risk).** Encode the tier rule as checked-in code/text and show it on the appendix:
- **Established-operational** = deployed public product with peer-reviewed *and* out-of-sample validation + a baseline (e.g., CyAN CI [ACAD-045/006]; EPA 7-day forecast [ACAD-050]).
- **Operational-unbenchmarked** = deployed but no skill metric in the corpus (e.g., NOAA Lake Erie product [FED-024] → skill n/r; state dashboards).
- **Vendor-self-report** = commercial, validation claimed but no disclosed baseline/peer review (PVT-001/003).
- **Research-grade** = peer-reviewed model, skill reported, not an operational product.
Every quality cell must show its *basis* (metric + status + year + peer-reviewed?), not a bare badge. The feature-frequency figure needs explicit inclusion rules (count a model toward a feature only if its dossier lists that feature) and each model's feature list cited.

**M1 — tool↔model overlap:** the EPA 7-day forecast (tool #2 = model #1, via FED-060→ACAD-050) and NOAA Lake Erie (product FED-024 vs research ACAD-024/051) are single things wearing two hats. Add one explicit sentence; a visual link between the paired entries; and **do not double-count them** in the count barplots (count operational products once on Slide 1; count research models once on Slide 2).

**M2 — add a "data signal" facet (satellite / in-situ / fusion) to the models table.** Surfaces a real insight: most frontier ML is *in-situ-driven and non-US* (Korea/China/Germany dominate: ACAD-043/117 Korea, 048/060/052 China, 037 Germany). Note this skew explicitly.

**M3 — temperature-driver synthesis stated honestly.** Phrase as "most *frequently* the top-ranked predictor — a correlational, model-internal finding," and carry the exceptions (phycocyanin ranks #1 in ACAD-037; nutrients/longitude lead in ACAD-060/008) and the "often a seasonal-cycle proxy; not a causal test" caveat. Hero figure must not imply a settled causal driver.

**M7 — respect the marine exclusion honestly.** FED-061 (NOAA HAB Monitoring System, 13 water bodies incl. coastal) and SLG-001 (FL DEP, prominently red-tide) are freshwater-*inclusive*, not -only. Scope each cell to its freshwater component and footnote that the parent program also covers marine (excluded here).

**LOW:** L3 small-N — show raw counts with N labelled, no percentages; use labelled dot/table where a category has ≤3 (a single reclassification must not visibly swing a chart). L4 — ACAD-050 year = 2023 online / 2024 issue; living program pages (SLG-001/012, FED-060/061) show **n/r** for year, never a guess. L5 — include a model-type taxonomy legend (empirical-RS index vs statistical/INLA vs mechanistic vs ML), noting CyAN CI and the EPA 7-day forecast both trace to the CyAN signal.

## Build approach (reproducible, in ./presentation)
1. `data/tools.json`, `data/models.json` — hand-curated from dossiers, each attribute carrying source key(s); n/r where unstated. I verify each cell against its dossier.
2. `build_figures.py` (matplotlib) → `figures/*.png` (barplots + feature-frequency).
3. `build_deck.py` (python-pptx, per the `pptx` skill) → `HAB_landscape.pptx`.
4. `README.md` — provenance + how to regenerate.
