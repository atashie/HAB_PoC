---
key: ACAD-104
title: A modular deep learning surrogate model for simulating harmful algal blooms in complex process-based systems
authors_or_org: Kim, Young Woo; Cha, YoonKyung (corresponding); Shin, Jihoon — University of Seoul
year: 2025
url: https://pubmed.ncbi.nlm.nih.gov/40591990/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (Water Research, Elsevier)
categories: [models-and-methods]
relevance: Medium
full_text_access: abstract
fetch_status: ok
review_severity: clean
review_overall: pass
---

# A modular deep learning surrogate model for simulating harmful algal blooms in complex process-based systems

> Note: provisional URL was resolved to a primary source. Original: https://www.sciencedirect.com/science/article/abs/pii/S0043135425009674

**What it is.** A modeling-methods paper (Kim, Cha & Shin, Water Research, 2025) that builds a modular deep-learning surrogate emulating the sequential FLOW (hydrodynamic) → WAQ (water quality) → BLOOM (phytoplankton) modules of a Delft3D process-based model, then uses that surrogate to accelerate and improve parameter calibration and to generate near-real-time, one-day-ahead HAB forecasts, case-studied on Daecheong Lake, South Korea (2022 calibration / 2023 validation).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** Process-based models (PBMs) for simulating HABs are limited for large-scale/operational use by high computational cost and the difficulty of parameter calibration; this is the stated motivation for building a deep-learning surrogate.
  - *evidence:* Stated directly as the opening problem framing in the abstract; no citation or data given for this general claim, it is presented as background motivation. (Abstract (PubMed record 40591990))
  - *quote:* "Process-based models (PBMs) are widely used for simulating harmful algal blooms (HABs) but are constrained by high computational costs and parameter calibration challenges, limiting their efficiency for large-scale applications."
- **[✓ verified]** The authors built a modular deep-learning surrogate that reproduces PBM behavior via a sequential structure (FLOW output feeds WAQ, WAQ output feeds BLOOM), applied to bloom-prone Daecheong Lake, South Korea, with 2022 used for calibration and 2023 for validation.
  - *evidence:* Describes the model architecture and the case-study site/time split as implemented and tested by the authors. (Abstract (PubMed record 40591990))
  - *quote:* "Applied to bloom-prone Daecheong Lake in South Korea during the calibration (2022) and validation (2023) periods, the framework emulates hydrodynamic (FLOW), water quality (WAQ), and phytoplankton dynamics (BLOOM) processes through a sequential structure, where outputs from FLOW serve as inputs for WAQ, and WAQ outputs feed into BLOOM, preserving key environmental interactions while reducing model complexity."
- **[✓ verified]** Surrogate-model-based parameter optimization (SM-PO) produced higher predictive accuracy than trial-and-error calibration (TE-PC) and TE-PC augmented with synthetic data (TE-PC+DA) across all three modules, with total cyanobacteria cell-count NSE rising from 0.644→0.782→0.930 in 2022 and 0.520→0.719→0.867 in 2023.
  - *evidence:* Direct quantitative comparison across three named calibration strategies, reported as Nash-Sutcliffe Efficiency (NSE) values for a single target variable (total cyanobacteria cell counts) in each of the two study years. (Abstract (PubMed record 40591990))
  - *quote:* "Surrogate model-based parameter optimization (SM-PO) achieved higher predictive accuracy than trial-and-error-based calibration (TE-PC) and TE-PC with data augmentation (DA) across all modules. For total cyanobacteria cell counts, SM-PO improved Nash-Sutcliffe Efficiency (NSE) from 0.644 (TE-PC) and 0.782 (TE-PC with DA) to 0.930 in 2022, and from 0.520 to 0.719 to 0.867 in 2023."
- **[✓ verified]** Chlorophyll-a predictions under the surrogate + data-augmentation + probabilistic-optimization approach showed roughly a 40% reduction in RMSE compared to the trial-and-error baseline (TE-PC).
  - *evidence:* Reported as an approximate percentage reduction; abstract does not give the absolute RMSE values or units (e.g., µg/L) underlying the percentage. (Abstract (PubMed record 40591990))
  - *quote:* "Additionally, chlorophyll-a predictions achieved an RMSE reduction of approximately 40% compared to TE-PC, demonstrating the effectiveness of integrating surrogate modeling with data augmentation and probabilistic parameter optimization."
- **[✓ verified]** A temporal dimensionality-reduction technique cut parameter-optimization computation time substantially — 87.5% for the hydrodynamic (FLOW) module and 96.4% for the water-quality/phytoplankton (WAQ/BLOOM) modules — without reducing model accuracy.
  - *evidence:* Direct quantitative efficiency claim tied to a named technique (temporal dimensionality reduction), paired with an explicit no-accuracy-loss claim. (Abstract (PubMed record 40591990))
  - *quote:* "Furthermore, temporal dimensionality reduction significantly accelerated parameter optimization, reducing computation time by 87.5% for hydrodynamic simulations and 96.4% for water quality and phytoplankton modules, without sacrificing model accuracy."
- **[✓ verified]** Because the surrogate is modular, individual modules can be updated/retrained independently, and the trained surrogate can generate near-real-time, one-day-ahead HAB forecasts directly from daily observed environmental inputs without re-running the full Delft3D process-based simulation.
  - *evidence:* States an operational/deployment benefit of the modular design and names Delft3D as the underlying process-based model being emulated — the only place the specific PBM software is identified in the abstract. (Abstract (PubMed record 40591990))
  - *quote:* "The modular structure enables targeted module updates, reducing retraining requirements and enhancing flexibility for different environmental conditions. Beyond accelerating parameter optimization, the trained surrogate model enables near real-time HAB forecasting. By leveraging daily observed environmental inputs, it generates one-day-ahead predictions without requiring full Delft3D simulations."
- **[✓ verified]** The authors frame the overall framework as scalable and computationally efficient, with claimed broad applicability to other aquatic systems and potential integration into operational water-quality management.
  - *evidence:* A forward-looking/generalization claim made by the authors themselves in the abstract's closing statement; not itself supported by cross-site validation data in the abstract (only Daecheong Lake was tested). (Abstract (PubMed record 40591990))
  - *quote:* "The proposed framework provides a scalable and computationally efficient tool for HAB simulation, with broad applicability to various aquatic systems and potential for integration into operational water quality management."

## Data / numbers
- NSE (Nash-Sutcliffe Efficiency, total cyanobacteria cell counts), 2022: TE-PC = 0.644 → TE-PC+DA = 0.782 → SM-PO = 0.930 (unitless index)
- NSE (total cyanobacteria cell counts), 2023: TE-PC = 0.520 → TE-PC+DA = 0.719 → SM-PO = 0.867 (unitless index)
- Chlorophyll-a RMSE: ~40% reduction (SM-PO with data augmentation vs. TE-PC baseline) — percentage only; absolute RMSE value/units not given in abstract
- Parameter-optimization computation-time reduction via temporal dimensionality reduction: 87.5% for hydrodynamic (FLOW) module
- Parameter-optimization computation-time reduction via temporal dimensionality reduction: 96.4% for water-quality (WAQ) and phytoplankton (BLOOM) modules
- Study design: calibration year = 2022; validation year = 2023 (Daecheong Lake, South Korea)
- Publication record: Water Research, Vol. 285, Article 124059; issue date Oct 1, 2025 (Epub Jun 20, 2025); DOI 10.1016/j.watres.2025.124059; PMID 40591990

## Methods
Per the abstract: a modular deep-learning surrogate model is trained to emulate, module-by-module and in sequence, the FLOW (hydrodynamic), WAQ (water quality), and BLOOM (phytoplankton dynamics) components of a Delft3D-based process-based model (Delft3D is named explicitly only in the context of the surrogate replacing "full Delft3D simulations"), with FLOW output feeding WAQ and WAQ output feeding BLOOM. Case study: Daecheong Lake, South Korea (described as "bloom-prone"), 2022 used for calibration and 2023 for validation. The surrogate-generated data are combined with a "probabilistic parameter optimization" method, termed surrogate model-based parameter optimization (SM-PO), and compared against two baselines: trial-and-error-based calibration (TE-PC) and TE-PC augmented with synthetic data (TE-PC+DA). A temporal dimensionality-reduction technique is applied to speed up the optimization step. Per the abstract, SM-PO "works" in the sense of outperforming both baselines across all three modules, with quantified gains for total cyanobacteria cell counts (NSE) and chlorophyll-a (RMSE), and the dimensionality-reduction step cuts optimization compute time sharply "without sacrificing model accuracy." The abstract does not report any scenario, module, or variable for which the surrogate underperforms the baselines or the PBM, nor any accuracy metrics for FLOW or WAQ outputs individually (only total cyanobacteria cell counts and chlorophyll-a are quantified).

## Stated limitations
The abstract — the only text accessible for this entry — does not enumerate explicit limitations, caveats, or failure conditions. It does not address transferability beyond Daecheong Lake, sample size or data-availability constraints, sensitivity of the surrogate to conditions outside the 2022/2023 training-validation window, or computational/data requirements for retraining modules. This should be read as "not stated in the retrievable text," not as evidence that no limitations exist — the full paper's Methods/Discussion/Limitations sections were not reachable (see fetch_notes).

## Tensions with other findings
Not evident from the abstract alone, since no other source's fetched text is available for direct comparison in this pass. Two points are worth flagging for a synthesis pass: (1) the abstract's own framing — that PBMs are constrained by "high computational costs and parameter calibration challenges" — is presented as an uncited, general problem statement rather than a claim traced to specific prior studies, so it should not be repeated as an established fact without its own sourcing; (2) the paper's central mechanism (a deep-learning surrogate wrapped around a proprietary hydrodynamic-water-quality-ecology model, Delft3D) is a heavier and less directly explainable approach than lighter statistical/ML methods reported elsewhere in HAB literature, which may be worth noting if this dossier's synthesis favors simple, transparent, explainable methods. No causal claims about bloom drivers are made in the abstract — all quantitative claims are about model/calibration performance (NSE, RMSE, compute time), not about what causes blooms.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0
- **Reviewer notes:** All seven claims are directly supported by the abstract text retrieved from PubMed (PMID 40591990). Every numeric value (NSE metrics, RMSE reduction %, computation-time savings %) matches the source verbatim. No conflicts between claimed and stated methodology or results. The only limitation is that only the abstract was accessible—the full paper (Methods, Results, Discussion, Limitations) could not be retrieved due to paywall access restriction (Elsevier closed access). Claims remain valid within the scope of what the abstract states, though readers should be aware that full-paper review was not possible."

## Provenance
- Canonical URL: https://pubmed.ncbi.nlm.nih.gov/40591990/
- Access date: 2026-07-01
- Full-text access: abstract | Fetch status: ok
- Fetch notes: Primary URL (https://www.sciencedirect.com/science/article/abs/pii/S0043135425009674) returned HTTP 403 Forbidden on WebFetch (paywalled Elsevier abstract page blocking automated fetch). Following the DOI (10.1016/j.watres.2025.124059) via WebFetch produced a 302 redirect to linkinghub.elsevier.com, which itself redirected back to the same ScienceDirect page and yielded no article text (only a "Redirecting" stub) — a dead end. WebSearch located the PubMed record for this article (PMID 40591990); WebFetch of that PubMed page succeeded and returned the complete, verbatim published abstract, full author list, journal/volume/page/DOI metadata, and keywords — this is the entirety of the article's publicly accessible text. An additional WebFetch of the OpenAlex API record (api.openalex.org/works/doi:10.1016/j.watres.2025.124059) confirmed the article is Closed Access with no open-access PDF location listed (APC $4,350 USD) and gave author affiliations (all three authors at University of Seoul); this was used only to document access status/affiliation, not as a scientific claim. WebSearch for a preprint, PMC copy, ResearchGate PDF, or author-hosted version found none. No full text (Methods/Results/Discussion/Limitations sections) was reachable, so this dossier entry is built strictly from the published abstract.
