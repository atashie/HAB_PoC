# data-sources — the data acquisition & characterization layer

This folder is the **data-engineering layer** of the SePRO HAB PoC: the scripted, reproducible
code + documentation + QA/QC + summary visualizations for every public data source we use.

It is distinct from `../Research/`, which is the **literature/science landscape** (what's known
about HABs). This layer is about **the actual bytes**: where each dataset lives, how we pull it,
what its rough edges are, and whether it's fit for purpose.

## Principles (inherited from `../CLAUDE.md`)

- **Real, public, cited data only.** Every source documented with URL + access date + how accessed.
- **Scripted & cached.** Data access is code, not manual clicks. Raw pulls are cached and
  **never hand-edited**. Everything regenerates from source.
- **Traceable.** Every summary number / figure traces to the exact file (sha256 in a manifest)
  and the exact code that produced it.
- **Honest about limits.** Gaps, biases, detection limits, and version churn are documented,
  not hidden. No silent truncation — exclusions are logged.
- **Secrets never committed.** Credentials live in `data-sources/.env` (gitignored); see
  `.env.example`.

## Layout (per-dataset, self-contained)

```
data-sources/
  README.md            # this file
  DATA-REGISTRY.md     # one row per source: status, access, coverage, citation
  requirements.txt     # pinned deps for all acquisition/QA/viz code
  .env.example         # credential template (copy to .env, gitignored)
  _common/             # dataset-agnostic helpers (HTTP retry, cached downloads, manifest)
  cyan/                # ← first dataset: EPA/NASA CyAN CI_cyano (see cyan/README.md)
    METADATA.md        #   full dataset characterization (the "know before you pull" doc)
    reference/         #   preserved primary-source docs (release notes PDF + text)
    access/            #   scripted, re-runnable pulls (enumerate + download -> data/raw)
    qaqc/              #   QA/QC checks + written QA report
    viz/               #   summary + interactive HTML map/plot generators
    outputs/           #   generated summaries & interactive HTMLs (tracked; small)
    data/              #   raw/ + derived/  (GITIGNORED — regenerate via access/)
```

## Onboarding a new dataset

CyAN is the worked example. Once it's solid, `../docs/` will hold a generalized
onboarding guideline distilled from it (see the project task list). Until then, mirror the
`cyan/` structure: **document first (METADATA.md) → script the pull → QA → visualize.**

## Environment

```
cd data-sources
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
All deps were verified working on Python 3.13 / win32 on 2026-07-01.
