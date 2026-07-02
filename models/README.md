# models/ — Florida CyAN bloom forecasting

This directory holds the **modeling layer** of the SePRO HAB PoC: the design, decisions, progress
tracking, and (as they are built) the code, artifacts, and results for forecasting the EPA/NASA
**CyAN cyanobacteria index (CI_cyano)** over the **state of Florida**, fusing four public data
groups — in-situ hydrology (NWIS), in-situ water quality (WQP), weather (ERA5 + ECMWF), and static
hydroclimate basin characteristics (BasinATLAS L12).

The data-acquisition layer lives in [`../data-sources/`](../data-sources/). This layer consumes it.

## What we are (and are not) doing

We **predict the CyAN satellite bloom signal** as the target/ground-truth. We explicitly **defer to
future work**: linking the CyAN signal to cyanobacteria cell counts, fusing local grab samples,
live optical/SAR retrievals, basin-scale hydrologic modeling, a global/general model, and
weather-forecast uncertainty (we assume perfect coincident weather for now). See
[`DESIGN.md` §1](DESIGN.md) for the full framing and scope bounds.

## Document map

| File | Purpose |
|------|---------|
| [`DESIGN.md`](DESIGN.md) | **The authoritative design spec** — problem framing, target, analysis unit, features, splits, models, baselines, metrics, leakage guards. Read this first. |
| [`DECISIONS-LOG.md`](DECISIONS-LOG.md) | Append-only, dated log of every decision + assumption and its rationale. |
| [`PROGRESS.md`](PROGRESS.md) | Living phase-by-phase tracker (define → acquire → prepare → explore → model → evaluate → communicate). Status at a glance. |
| [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) | Decisions still needing resolution or user input, with recommendations. |
| `docs/NN-*.md` | Phase-specific deep-dive docs, created as we reach each phase (see `DESIGN.md` §9 for the planned set). |
| `model-cards/` | One card per trained model: config, metrics-vs-baseline, importances, limits. Created at the modeling phase. |

## Operating principles (inherited, non-negotiable)

Everything here is gated by the project's **claim gate** (`../CLAUDE.md`): every number traces to a
cited real source + the exact code that produced it, regenerates from checked-in code, is reported
**with a baseline and an uncertainty**, and is stated with its limits. Weak or negative results are
deliverables, not failures. No spatial/temporal aggregation of data without explicit sign-off.

## Status

**Phase: ACQUIRE.** Design finalized (v3, 2026-07-02) and Codex-reviewed; **pivoted to match the EPA
CyanoHAB forecast** — resolvable-**lake** unit, **temporal** held-out-year split, **WHO Alert Level 1**
target. Next: FL resolvable-lakes mask + per-lake CyAN aggregation. No model trained yet — see
[`PROGRESS.md`](PROGRESS.md).
