# <DATASET NAME> — Dataset Metadata

**Dataset short name:** <id>
**Product this file describes:** <specific product/variable>
**Version / processing level documented:** <version + date>
**Compiled:** <YYYY-MM-DD> · **Access date for all checks below:** <YYYY-MM-DD>
**Compiled by:** <who>. Every quantitative claim traces to a cited primary source or an empirical
check we ran (script noted). Ambiguities are flagged, not smoothed over.

---

## 0. TL;DR for the modeler

| Question | Answer |
|---|---|
| What is it? | |
| Native form / format | |
| Spatial resolution & extent | |
| Temporal span, cadence, gaps | |
| The value in a cell/record | |
| Encoding / how to read a value | |
| Nodata / fill / detection limit | |
| Access (search / download / auth) | |
| Bulk or subset? (with size estimate) | |
| Likely role (target / feature / mask / context) | |

## 1. What it is
<one-para description; what each output variable means; who produces it; maturity/validation status.>

## 2. Temporal coverage, cadence & gaps
<table of sensors/sources × period × cadence; refresh latency; reprocessing/version churn; KNOWN GAPS.>

## 3. Spatial characteristics
<resolution (verify from a real file), CRS/projection, tiling/grid, extent, minimum reliable unit.>

## 4. Encoding & quality flags — EXACT values (authoritative)
<the exact value scheme / units; nodata & fill; detection limits; every QA flag + meaning.
Beware look-alike products with different encodings. Note what is/ isn't in the primary file
vs separate flag layers.>

## 5. Known issues & limitations (from the source — the honest list)
<copy the provider's own caveats; add biases relevant to prep: non-random gaps, sampling bias, etc.>

## 6. Bulk-download vs on-the-fly — the feasibility call
<order-of-magnitude size estimate of the full archive; the chosen subset strategy + justification.>

## 7. How to access it (verified <date>)
### 7.1 Search / enumerate (auth?)  — endpoint, params, returns, reliability notes
### 7.2 Download (auth?)            — endpoint/pattern, auth method, where creds live (.env)
### 7.3 Alternative/convenience access (documented, secondary)
### 7.4 Ancillary (grids/shapefiles/DOIs)

## 8. Sources (all accessed <date>)
1. <primary source> — URL. Local cache: `reference/<file>`.
2. <secondary> — URL.
N. <empirical checks we ran> — reproducible via `access/` scripts.

## 9. Likely role in the SePRO HAB analysis
<target / feature / mask / context; what it is NOT; correlation-vs-causation caveats.>

## 10. Reproducibility & version pinning (rules for this dataset)
<how version is recorded & verified; default stream/selection; cache + manifest; access date.>
