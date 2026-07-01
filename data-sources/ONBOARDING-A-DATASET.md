# Onboarding a new data source — the repeatable workflow

This is the generalized process for adding any public dataset to the PoC, distilled from the
first worked example (**CyAN**, `cyan/`). Follow it in order. The goal is that every dataset
arrives **documented, scripted, cached, QA'd, and visualized** — and that every number we ever
quote from it can be traced back to exact bytes and exact code.

> **The claim gate (from `../CLAUDE.md`) applies to data too.** Before a dataset's numbers enter
> any analysis, slide, or tool, they must: (1) **trace** to a cited real source, (2) **regenerate**
> from checked-in code, (3) carry a **baseline + uncertainty** where a metric is reported, and
> (4) be **bounded** by stated limits. This workflow exists to make that automatic.

Use `cyan/` as the reference implementation and `_template/` as the copy-me skeleton.

---

## The five steps

### 1. Document BEFORE you pull → `<dataset>/METADATA.md`
Know the data before touching it. Fill in `_template/METADATA.template.md`. Answer, with every
fact traced to a **primary source** (agency docs / release notes / data descriptor — not a blog),
and each carrying its access date:

- **What it is** and what each output variable/product actually means.
- **Coverage:** spatial extent + resolution; temporal span, cadence (refresh latency), and **gaps**.
- **Encoding & flags:** the *exact* value scheme, nodata/fill values, detection limits, QA flags
  and their meanings. (CyAN lesson: the DN 0 = "below detection" is **measured**, not missing;
  and a *different* agency's look-alike product used a different encoding — never assume.)
- **Access:** search vs download endpoints, auth, rate limits, formats.
- **Bulk vs subset:** estimate the full-archive size; decide and **justify** whether to mirror or
  subset. (CyAN lesson: full archive ≈ hundreds of GB–TB → subset by space+time.)
- **Known issues / biases:** copy the source's own caveats. These are deliverables.
- **Role in the model:** target / feature / mask / context — state it.
- **Version/reprocessing:** does the provider reprocess (values change over time)? How is version
  recorded? (CyAN lesson: verify version from file *metadata*, not the filename.)

Preserve primary-source docs in `<dataset>/reference/` (e.g. a release-notes PDF + a text
extraction) so the audit trail survives link rot.

**Prefer the primary source over any summary/LLM answer.** If a fact can't be traced, don't state it —
flag it as unresolved and plan to verify empirically (see step 2).

### 2. Script the acquisition (cached + manifested) → `<dataset>/access/`
- **Enumerate then download.** Discovery (listing what exists) is usually auth-free and cheap;
  do it first and log the plan. Downloading may need credentials.
- **Reuse `_common/net.py`:** retrying session (federal endpoints flake — CyAN's search 502s
  intermittently), credential resolution from the gitignored `.env`, and `download_file`
  (cache-if-present, atomic write, sha256) + `append_manifest` (JSONL audit trail: url, bytes,
  sha256, access time, key fields).
- **No silent truncation.** If the source returns families/variants you exclude, **log the counts
  kept vs dropped** and document why. (CyAN lesson: search returned merged *and* per-satellite
  products; we use merged and say so.)
- **Empirically confirm the fuzzy bits** the docs left ambiguous (earliest date, real filenames,
  which auth works). Fold what you learn back into `METADATA.md`.
- **Secrets:** only from `../.env` (gitignored) or env vars. Never commit, never echo.
- Provide a `--dry-run` (plan without auth) and a `--limit` (sample) for cheap iteration.

### 3. QA/QC the pull → `<dataset>/qaqc/` → `outputs/qa_report.md` + `qa_summary.json`
Verify structure and integrity from the data itself, not assumptions:
- **Integrity:** recompute sha256 vs the manifest.
- **Structure:** dtype, bands, CRS, resolution, bounds — check against the documented spec.
- **Distributions:** value/flag composition (per the exact encoding); % valid / nodata / etc.;
  ranges and basic stats on valid data. Distinguish *measured-zero/non-detect* from *missing*.
- **Consistency:** across files that should match (same grid/CRS/shape), and note version tags.
- **Flag anomalies** explicitly; a clean report should still list what was checked.
- Emit both a **machine-readable JSON** (for downstream/CI) and a **human Markdown** report.

### 4. Visualize a summary/sample → `<dataset>/viz/` → `outputs/`
- **Interactive HTML maps** (Folium) for spatial data — reproject to lat/lon, colorize using the
  *exact* categories, land/nodata transparent. Sample across time to show seasonality.
- **Interactive summary charts** (Plotly) — time series + composition, small (`plotlyjs="cdn"`).
- **A small static PNG** of a representative case (visual proof that survives in git and can be
  eyeballed in review). Confirm it looks *scientifically sensible*, not just non-empty.
  (CyAN lesson: the peak-week render showed the known Maumee-Bay bloom — real validation.)

### 5. Register + reflect
- Add/refresh the dataset's row in `DATA-REGISTRY.md`.
- Record notable decisions/assumptions in `DECISIONS-LOG.md`.
- Update this file if you learned a new general lesson.

---

## Repo hygiene (applies to every dataset)

- **Track:** code, `METADATA.md`, `reference/`, QA report + JSON, lightweight summary HTML, small PNGs.
- **Gitignore:** `data/` (raw + derived), the download manifest, and heavy regenerable
  `outputs/*_map.html`. Everything gitignored must **regenerate from checked-in code**.
- **Deterministic:** fixed params, pinned deps (`requirements.txt`), scripted access — no manual steps.

## Cross-cutting lessons from CyAN (things that generalize)

0. **Never aggregate (spatially or temporally) without explicit permission** — analysis *or* viz.
   Aggregation distorts values with hard-to-trace effects. Default to native resolution and the source's
   own composites; if an output is too heavy, reduce **scope** (extent / count), not resolution. Any
   aggregation must be an explicit, opt-in step.
1. **Documentation is step one, not an afterthought** — it prevents wrong assumptions downstream.
2. **Trust the data over the filename/docs for anything ambiguous** — read embedded metadata; probe the API.
3. **Distinguish "measured absence" from "missing"** — they mean different things to a model.
4. **Watch for look-alike products** with different encodings (same phenomenon, different agency).
5. **Cache + sha256 manifest = reproducibility + audit** for free.
6. **Retry transient federal-endpoint errors**; they are common, not fatal.
7. **Subset, don't mirror**, unless the archive is genuinely small.
8. **Visual sanity-check** the output against domain expectation before trusting the pipeline.
