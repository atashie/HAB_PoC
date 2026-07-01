# _template — copy-me skeleton for a new dataset

To onboard a new source (follow `../ONBOARDING-A-DATASET.md`):

1. `mkdir ../<dataset>` and create subfolders: `reference/ access/ qaqc/ viz/ outputs/ data/raw data/derived`.
2. Copy `METADATA.template.md` → `../<dataset>/METADATA.md` and fill every section from primary sources.
3. Write acquisition/QA/viz code in the subfolders, **reusing `../_common/`** (retrying HTTP
   session, credential resolution, cached+manifested downloads).
4. Use `../cyan/` as the reference implementation to adapt — it is a complete, working example
   (documentation → scripted pull → QA report → interactive map/plots + static proof).
5. Add a row to `../DATA-REGISTRY.md` and note decisions in `../DECISIONS-LOG.md`.

Keep raw data and heavy regenerable maps out of git (see `../../.gitignore`); track the docs,
code, QA report/JSON, lightweight summary HTML, and small PNGs.
