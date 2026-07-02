# cyano-forecasts — EPA experimental cyanoHAB forecast (ingest layer)

Scripted, reproducible acquisition + QA/QC + summary viz for **EPA's experimental weekly 7-day
cyanobacterial-HAB probability forecast** (Schaeffer et al. 2024) — one bloom-probability per
Sentinel-3-resolvable U.S. lake per week. **Read `METADATA.md` first** — it documents what the data
means, its limits, and (critically) the **two-tier, partly-unofficial access model**.

> ⚠️ **The live forecast values have NO official API.** They live only in EPA Qlik Sense dashboards;
> we extract them over the dashboards' anonymous **QIX WebSocket** — a **reverse-engineered,
> not-EPA-supported** path (METADATA §7.2, §12). This is a **research/benchmark** ingest, not a
> production feed. The *official, citeable* artifact is the **model code** at DOI `10.23719/1529140`.

## Why we care (the finding)
The forecast is a **validated federal baseline** (AUC 0.95, acc 0.90 beating 6 ML baselines; but
**precision 0.49 → it deliberately over-predicts**). It is a strong thing to **benchmark our own model
against, or to leverage as a signal** — see `../../docs/plans/2026-07-02-epa-cyano-forecast-as-baseline.md`.
Because it is itself **CyAN-derived**, it must **never** be used as a ground-truth label for our
CyAN-based models (leakage) — see METADATA §9.

## Layout
```
cyano-forecasts/
  METADATA.md                  # 14-section characterization (know-before-you-pull) — START HERE
  reference/                   # preserved primary sources: cached EPA pages, official code README,
                               #   PRIMARY-SOURCES.md (verbatim quotes + probe log), QIX test fixture
  access/
    qlik_public.py             # anonymous-QIX client (fail-closed extraction contract) — UNOFFICIAL
    pull_forecasts.py          # weekly snapshot pull -> immutable snapshots + revision tracking + manifest
    pull_official.py           # official DOI model-code ZIP (HTTP, cached, sha256, manifest)
  qaqc/qa_forecasts.py         # live-snapshot QA + archive QA + integrity -> outputs/qa_report.md
  viz/viz_forecasts.py         # native per-lake map + sentinel-lake curve + PNG proof
  tests/test_qlik_public.py    # OFFLINE parser/normalizer tests (fixture; no network)
  outputs/                     # qa_report.md, qa_summary.json, *.png, sentinel .html (tracked);
                               #   *_map.html (gitignored, heavy)
  data/  raw/ + derived/       # GITIGNORED — regenerate via access/
```

## Quickstart
```bash
cd data-sources
pip install -r requirements.txt          # adds websocket-client==1.9.0

cd cyano-forecasts/access
python pull_forecasts.py --dry-run       # schema + qSize + selection state (fast, no full pull)
python pull_forecasts.py                 # full weekly snapshot -> data/raw/snapshots/ + derived views
python pull_forecasts.py --cross-check   # also pull the sibling app and diff (source-integrity check)
python pull_official.py                  # official model-code ZIP (verified sha256)

cd ../qaqc && python qa_forecasts.py     # -> outputs/qa_report.md + qa_summary.json
cd ../viz  && python viz_forecasts.py    # -> outputs/ map + sentinel curve + peakweek PNG
cd ../tests && python test_qlik_public.py   # or: pytest
```

## Operating notes
- **Run weekly.** The dashboard keeps only a **rolling ~2 seasons** and can revise past weeks; each run
  appends an **immutable, dated snapshot** and rebuilds `data/derived/current.csv` + `revisions.csv`
  (idempotent — `--rebuild-only` rebuilds views without a network pull).
- **Fail-closed.** The extractor reads **exactly** `qSize.qcy` rows and asserts the count; a schema/app
  change fails loudly rather than truncating. If the pinned app IDs / virtual proxy stop working, EPA
  re-published the dashboard — update `access/qlik_public.py` and re-verify (METADATA §7.3, §10).
- **Be a good citizen.** One small read per week, identifying User-Agent. For a supported feed, contact
  **Blake Schaeffer (schaeffer.blake@epa.gov)** (METADATA §12).
- **Verified working** 2026-07-02 (Python 3.13, win32): full pull = 105,168 rows (2,191 lakes × 48
  weeks), 0 QA flags; official ZIP sha256-verified; offline tests green.
