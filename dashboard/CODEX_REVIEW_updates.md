# Codex Review - Florida HAB Dashboard Latest Updates

Review date: 2026-07-07

Scope reviewed: `dashboard/build_dashboard_data.py`, `dashboard/index.html`, `dashboard/data/dashboard_data.js`,
`dashboard/README.md`, `models/model/eval_fusion.py`, `models/outputs/exp_feature_ablation_trace.md`,
`models/outputs/exp_feature_ablation_onset_trace.md`, and `models/data/derived/modeling_table_fusion_fl.parquet`.
Prior reconciliation in `dashboard/CODEX_REVIEW_dashboard.md` was read first.

## Findings

### 1. README claims borderline tiers are marked with `~`, but the UI never renders that uncertainty marker

Verdict: CONFIRMED

File/lines:
- `dashboard/README.md:71-72` says forecasts are point estimates and "tiers near a boundary marked `~`".
- `dashboard/index.html:358-360` only puts "tiers near a threshold are not sharply separable" in the info tooltip.
- `dashboard/index.html:367-373` renders the alert row tier and probability without any borderline marker.
- `dashboard/index.html:436-440` renders forecast bars as point estimates only.

Why it matters:
The latest text claims a visible uncertainty affordance that does not exist. The dashboard still has a verbal
point-estimate caveat, but near-threshold lakes are displayed as clean Low/Watch/Warning categories.

Concrete failure scenario:
The generated bundle has multiple risks within 5 points of a tier boundary, including Lake Weohyakapka h3 = 40.4%
and Lake Eloise h3 = 39.5%. The former is rendered as an ordinary Warning and the latter as an ordinary Watch/Low
boundary case, with no `~` or dashed/borderline styling. A user can read a 40.4% lake as materially different from
a 39.5% lake even though the README says borderline uncertainty is marked.

### 2. "Weeks to Bloom" displays the horizon index, not literal calendar weeks to bloom

Verdict: CONFIRMED

File/lines:
- `dashboard/index.html:358` defines Weeks to Bloom as the first lead h in 0-4 reaching Warning.
- `dashboard/index.html:367` labels the column "Weeks to Bloom".
- `dashboard/index.html:372` renders the horizon index directly.
- `dashboard/build_dashboard_data.py:428-429` correctly notes that h targets week `T+(h+1)` and that CyAN has about 2 weeks latency.

Why it matters:
The tooltip partially mitigates this by saying "first lead (0-4)", but the visible column header says literal weeks.
Under the table definition, h0 is the target week after the cutoff week, h1 is two target weeks out, and h0 is also
diagnostic/nowcast-only. CyAN latency makes literal timing even less direct.

Concrete failure scenario:
For COMID 86758, the first Warning horizon in the generated bundle is h0 with target_end 2026-05-30 and risk 47.9%.
The alert list would show "0" under "Weeks to Bloom", although the target week is not zero calendar weeks after the
2026-05-17 cutoff and h0 is not an operational forecast. A field user could understate response timing.

### 3. Footer/provenance documentation drift: the README says gate/provenance details are printed in the footer, but the shipped footer is high-level only

Verdict: CONFIRMED

File/lines:
- `dashboard/index.html:230-235` sets the footer to a high-level provisional PoC description with no source paths, Gate A, or Gate B values.
- `dashboard/README.md:106-111` still says provenance and the consistency-gate result are printed in the page footer.
- `dashboard/build_dashboard_data.py:407-438` preserves traceability in `window.DASH.meta`, including source paths and gate values.

Why it matters:
The high-level footer replacement is acceptable, but the README is now inaccurate about where traceability appears.
Claim-gate traceability is preserved in `build_dashboard_data.py`, `dashboard/data/dashboard_data.js`, and the README
method section, not in the visible footer.

Concrete failure scenario:
A reviewer opening only `index.html` sees "Methods, data sources, and validation are documented in the project repository"
but no Gate A h1 AUC, Gate B AUC/baseline/onset-AUC, or data-source paths. The README says those details are printed
in the footer, so the documented audit path and the shipped page disagree.

### 4. Missing-horizon lakes are shaded distinctly but the alert legend does not explain the no-forecast color, and the count is hidden in a tooltip

Verdict: PLAUSIBLE

File/lines:
- `dashboard/index.html:315-319` builds the risk legend for Warning, Watch, Low, and Active HAB only.
- `dashboard/index.html:334` shades clear lakes with no forecast at the selected horizon using a tan fill.
- `dashboard/index.html:357-362` computes the missing count, but only appends it inside the info-tooltip text.
- `dashboard/data/dashboard_data.js:1` emits 131 lakes, 122 with all five horizons; 5 clear lakes are missing h1.

Why it matters:
This is much better than silently treating missing horizons as Low, but it is still easy to miss. The tan no-forecast
state is not in the visible legend, and the selected-horizon missing count is not visible unless the user hovers the
info icon.

Concrete failure scenario:
At the default h1 view, five clear lakes have no h1 forecast and are omitted from the ranked alert list. They appear
on the map in an unexplained tan color. A user who does not hover the info icon can interpret absence from the list as
low risk rather than missing model output.

### 5. README still uses "DN" terminology after the UI standardization to "CyAN index"

Verdict: PLAUSIBLE

File/lines:
- `dashboard/README.md:37-40` refers to observed levels as "satellite CyAN index (DN)" and "median CyAN DN".
- `dashboard/index.html:161`, `dashboard/index.html:388`, and `dashboard/index.html:443-454` use "CyAN index" on screen.

Why it matters:
The on-screen terminology is standardized, but the README is not. This is minor technically, but it conflicts with the
stated cleanup of avoiding "DN" in favor of "CyAN index".

Concrete failure scenario:
A non-technical reviewer reading the README sees both "CyAN index" and "DN" for the same quantity, while the UI uses
only "CyAN index". That weakens the terminology cleanup and may reintroduce the older measurement-label ambiguity.

## Verified Checks With No Negative Finding

- Per-horizon models: confirmed. `dashboard/build_dashboard_data.py:242-260` fits separate fusion, lean, and
  climatology models per h=0..4 on `train+val+test`, then scores the 2026 snapshot. The scored snapshot rows are
  `oos_partial`, not in the fit. The generated full-horizon lakes are not flat: 122 lakes have all 5 horizons, none
  had a max-min fusion range below 0.05 points, median range was 2.2 points, and max range was 75.3 points.
- Eval protocol sanity: confirmed. `models/model/eval_fusion.py:174-185` evaluates the h0-h4 curve per horizon.
  Recomputing in memory reproduced the 2025 fusion curve 0.989, 0.983, 0.979, 0.976, 0.973 and h1 Gate A =
  0.983464, within the 0.975-0.990 band.
- Gate B: confirmed leakage-free at the split/target level. `train+val+test` target labels end 2025-12-28;
  `oos_partial` target labels start 2026-01-04. Recomputed Gate B matched `dashboard_data.js`: fusion AUC
  0.993, 0.987, 0.985, 0.979, 0.979; persistence AUC 0.952, 0.930, 0.920, 0.907, 0.899; onset-AUC
  0.956, 0.942, 0.941, 0.920, 0.932. The high AUC is honestly framed as autocorrelation-dominated.
- Lean model: confirmed. Both ablation traces keep exactly `cyan_median` and `area_sqkm`
  (`models/outputs/exp_feature_ablation_trace.md:66-70`,
  `models/outputs/exp_feature_ablation_onset_trace.md:66-72`). The dashboard uses
  `SimpleImputer + StandardScaler + LogisticRegression` on exactly those two features
  (`dashboard/build_dashboard_data.py:156-158`, `dashboard/build_dashboard_data.py:255`).
- WQP filtering: confirmed for displayed features and chl-a history. `PHYS_BOUNDS` are generous
  (`dashboard/build_dashboard_data.py:61-65`), displayed feature values outside those bounds are nulled
  (`dashboard/build_dashboard_data.py:352-358`), and chl-a history drops negatives/sentinels
  (`dashboard/build_dashboard_data.py:293-297`). In the current bundle there are no displayed out-of-bound
  in-situ values and no negative chl-a samples.
- Duration fix: confirmed. `dashboard/build_dashboard_data.py:196-210` uses `start_date <= cutoff`; all clear
  lakes in the generated bundle have `duration_wk = 0`, all blooming lakes have positive duration, and emitted
  durations match the function.
- EPA, h0, cutoff-line, and raw in-situ caveats: confirmed materially accurate. The EPA later-snapshot caveat is
  on the forecast and disagreement panels (`dashboard/index.html:152-156`, `dashboard/index.html:169-171`), h0 is
  labeled nowcast in the selector (`dashboard/index.html:244-246`), the observed-history cutoff line and post-issue
  shading are implemented (`dashboard/index.html:457-461`), and raw/unharmonized in-situ caveats are visible
  (`dashboard/index.html:176-180`).
- Four risk states: confirmed on screen. The risk map/list distinguish Warning, Watch, Low, and Active HAB
  (`dashboard/index.html:315-319`, `dashboard/index.html:331-335`).

---

## Reconciliation (applied 2026-07-07)

Codex independently VERIFIED all substantive changes as correct — per-horizon models (leakage-free, not flat),
Gate A/B (reproduced the numbers; AUC confirmed autocorrelation-dominated, no leakage), the lean model
(exactly cyan_median+area_sqkm), WQP filtering, duration fix, and all caveats. The 5 findings were minor:

- **F1 (README `~` claim):** FIXED — README no longer claims a `~` borderline marker (removed per user request).
- **F3 (README "printed in footer"):** FIXED — README now states the footer is high-level and full provenance/gates
  live in `window.DASH.meta` + README.
- **F5 (README "DN"):** FIXED — README standardized to "CyAN index" (0–255).
- **F4 (missing-horizon legend):** FIXED — added a muted "no forecast this week" swatch to the risk legend
  (a data-availability note, kept visually distinct from the 4 risk levels).
- **F2 (Weeks to Bloom = onset horizon, not literal weeks):** FIXED — the user chose to relabel. The column is now
  **"Onset lead"** (column header, cell tooltip, ⓘ tooltip, README), and the ⓘ tooltip + README now explicitly state
  it is a *horizon index* (lead `h` targets week `T+(h+1)`; CyAN carries ~2 weeks latency), not a literal week count.
  Values unchanged (still the first forecast horizon 0–4 reaching Warning, "–" if none).
