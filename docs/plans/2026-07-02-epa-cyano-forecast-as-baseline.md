# EPA's cyanoHAB forecast as our baseline (and/or leveraged signal)

**Date:** 2026-07-02 · **Status:** finding + strategy, to carry into the Parts A/B/C deliverable.
**Owner doc for the data:** `../../data-sources/cyano-forecasts/METADATA.md` (14-section) ·
registry row `cyano_forecasts` · decisions log 2026-07-02 (session 9).

## The finding (one line)
EPA already publishes a **peer-reviewed, out-of-sample-validated, operational 7-day cyanoHAB
probability forecast** for **2,191 Sentinel-3-resolvable U.S. lakes** — so we have a **validated
federal baseline to judge our own work against, or to leverage as a signal.** We have it ingested,
QA'd, and reproducible.

## Why it's a *strong* baseline (not just any comparator)
- **Established-operational** by the deck's own quality rubric
  (`2026-07-01-hab-landscape-slides-design.md`, tool #2 / model #1, key `ACAD-050`): a deployed public
  product with peer-reviewed **and** out-of-sample validation and stated skill.
- **Method:** hierarchical Bayesian spatiotemporal (INLA; AR1 + spatial SPDE). Predictors are exactly
  the fusion the brief asks us to demonstrate — **satellite (CyAN) + weather (precip, modeled water
  temperature) + lake morphology.**
- **EPA-reported skill (2021 test year; point estimates, NO CIs — cite as EPA's, not ours):** AUC 0.95;
  accuracy **0.90** (beating SVC/RF/DNN/LSTM/RNN/GRU at 0.84–0.85); sensitivity 0.88; specificity 0.91;
  **precision 0.49**; false-omission 0.01; base rate ~9–10%.
- **The precision 0.49 is the headline caveat and an opportunity:** the model **deliberately
  over-predicts** (health-protective). "Keep the sensitivity, cut the false alarms" is a concrete,
  defensible thing an explainable model could try to improve on — with the base rate stated so the
  metrics are honest.

## How we use it (pick per Part; all defensible)
1. **Benchmark to beat / match (default, strongest story).** Any risk/early-warning model we build is
   scored against **(a)** naïve persistence/climatology **and (b)** this EPA forecast. "As explainable
   as, and competitive with, a federal product" is a credible **product claim** for the panel.
2. **Leverage as a signal / ensemble input.** Use the published probability as a covariate or
   corroborating overlay — **only as an as-of operational value** (the probability published *before*
   the target time), never a current/future value.
3. **Framing for a non-technical user (Part B).** The tool can show our readout **next to** EPA's number
   for the same lake/week — instant credibility and a sanity check for a field specialist.
4. **Part C (platform).** It is a ready-made **drift/monitoring reference** and a business talking point
   (we interoperate with the federal system on the same `COMID` lakes).

## The load-bearing caveat — leakage (do NOT skip)
The EPA forecast is **itself CyAN-derived.** Therefore:
- **Never use it as a ground-truth label** for any model of ours that uses CyAN features — that is
  **circular** and leaks the target. Ground truth for bloom presence must come from **independent
  in-situ** data (WQP/NARS chl-a & cyanotoxins) or the **raw CyAN observation treated as observation**.
- When used as a feature, join **as-of** and **block splits by space and time** (no random shuffles on
  autocorrelated lake-weeks).
- It forecasts a **chl-a/dominance threshold, not toxin** — pair with the CyAN↔NLA matchup finding
  (`../../analysis/cyan_nla_matchup/`) that biomass/CI is **not** a trustworthy toxin screen.
- **Correlation ≠ causation** for any driver/treatment implication.

## Access reality (so the claim is bounded)
- **Official & citeable:** the model **code** (DOI `10.23719/1529140`, ScienceHub) + the **paper**
  (`10.1016/j.jenvman.2023.119518`, open access PMC10842250). Anchor scientific/method claims here.
- **Live values are UNOFFICIAL:** published only via EPA Qlik dashboards; we extract over the anonymous
  Qlik **QIX WebSocket** (reverse-engineered, not an EPA-supported API). Present the live-values use as
  **research/benchmark, not a production dependency**; escalation for a supported feed:
  **Blake Schaeffer, schaeffer.blake@epa.gov**. Full detail: `cyano-forecasts/METADATA.md` §7/§12.

## Linkage (why fusion is cheap here)
Every forecast lake carries a **`COMID` (NHDPlus V2)** — the same key as our `EPA-NARS`, `WQP`, `NWIS`,
and LakeCat layers — so the forecast joins to in-situ chemistry/toxins, streamflow, and watershed
drivers **by identity**, and to CyAN pixels spatially (`cyano-forecasts/METADATA.md` §11).

## Concrete next steps
- Build the **as-of join** of the forecast probability to our CyAN + weather + NARS/WQP features on
  `COMID`, with temporal blocking (reuse the leakage policy above).
- Compute the **honest benchmark table**: our model vs persistence/climatology vs EPA forecast, on a
  held-out season, reporting the confusion matrix at a chosen cutoff (mirroring EPA's precision/recall
  trade-off so the comparison is apples-to-apples).
- Snapshot the dashboard **weekly** (`cyano-forecasts/access/pull_forecasts.py`) to accrue the multi-
  season history the live dashboard discards — needed before any temporal evaluation.
