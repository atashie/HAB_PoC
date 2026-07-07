# Codex Review - Florida HAB Dashboard Accuracy / Claim Gate

Review date: 2026-07-06

Scope reviewed: `dashboard/build_dashboard_data.py`, `dashboard/index.html`, `dashboard/data/dashboard_data.js`, `dashboard/README.md`, plus referenced model/eval docs and source tables as needed.

## Findings

### 1. WQP in-situ values are displayed with concrete units even though the WQP pull is explicitly not unit/fraction/censor harmonized

Verdict: CONFIRMED

File/lines:
- `dashboard/build_dashboard_data.py:68-70` includes WQP raw values in `TRACK_A`.
- `dashboard/build_dashboard_data.py:104-111` labels WQP values as `mg/L`, `ug/L`, `C`, and `ft`.
- `dashboard/build_dashboard_data.py:240-247` and `dashboard/build_dashboard_data.py:315-317` pass WQP daily `value` directly into the dashboard chl-a history.
- `models/prepare/pull_link_wqp_fl.py:8-12` says the consolidated WQP values are "NOT unit/fraction-harmonized".
- `dashboard/data/dashboard_data.js:1` contains the emitted raw feature/history values.

Why it matters:
The UI presents values as physically interpretable measurements, but the source pipeline says they are not harmonized. This violates the claim gate because the numeric value traces to WQP, but the displayed unit/meaning does not. It also affects model input honesty: the fusion model consumes `wqp_TP_val`, `wqp_chl_a_val`, `wqp_ammonia_val`, etc. as numeric features without this caveat in the dashboard.

Concrete failure scenario:
The generated bundle has current "Total phosphorus" values such as Lake Myakka = `312.0 mg/L` and multiple lakes above `10 mg/L`; those are implausible as literal TP mg/L and are likely mixed units or censor artifacts. The chl-a history contains 44 negative chl-a values, e.g. Conway Lake has `-1.0` ug/L samples in `dashboard_data.js`. A user could interpret these as real lab concentrations and make a wrong field-prioritization decision.

### 2. EPA comparator is not an EPA forecast issued at the dashboard cutoff; it is target-week `percent_chance` from a later revisable snapshot

Verdict: CONFIRMED

File/lines:
- `dashboard/build_dashboard_data.py:43-44` hardcodes the EPA snapshot `allweeks_20260702T000000Z.csv`.
- `dashboard/build_dashboard_data.py:227-232` matches EPA by `comid x target_end`.
- `dashboard/index.html:145-147` describes the EPA series as "the EPA CyanoHAB forecast" beside the dashboard forecast.
- `dashboard/index.html:159-160` defines disagreement as "our forecast minus ... the EPA forecast".
- `models/model/eval_epa_headtohead.py:9-21` documents that EPA values are a 2026-07-02 dashboard snapshot, not proven as-issued, and EPA is valid for the current week through Saturday, not a multi-week forecast.
- `models/outputs/epa_headtohead.md:5-11` repeats the same timing/provenance caveats.

Why it matters:
For a dashboard cutoff of 2026-05-17, the EPA values for target weeks ending 2026-05-30, 2026-06-06, ..., 2026-06-27 are not an EPA forecast issued from the 2026-05-17 information set. They are rows from a 2026-07-02 all-weeks dashboard snapshot matched to each target week. The side-by-side bars and deltas therefore compare our model's cutoff-based forecast to EPA current-week/revisable values for future weeks.

Concrete failure scenario:
For h4, the dashboard can show "our forecast vs EPA" for target week ending 2026-06-27 as if both were available at the 2026-05-17 cutoff. The EPA CSV has 132 FL rows for `week_end_date = 2026-06-27`, but those values are from the 2026-07-02 snapshot and are not an as-issued 5-week-ahead EPA forecast. A user could treat a large `fusion - EPA` delta as contemporaneous model disagreement when it is partly an information-set mismatch.

### 3. The dashboard forecast model is not faithful to `eval_fusion.py`'s per-horizon evaluation protocol, and the AUC gate does not validate the emitted model

Verdict: CONFIRMED

File/lines:
- `dashboard/build_dashboard_data.py:213-218` fits one pooled model on all labeled `train`, `val`, and `test` rows across all horizons.
- `dashboard/build_dashboard_data.py:189-200` computes the verification AUC separately for h=1 using train+val -> test.
- `dashboard/build_dashboard_data.py:344-345` runs that separate verification after the dashboard predictions have already been computed.
- `models/model/eval_fusion.py:70-75` fits train, tunes val, refits train+val, and predicts test for a supplied feature set.
- `models/model/eval_fusion.py:103-114` evaluates h=1 specifically.
- `models/model/eval_fusion.py:147-159` fits/evaluates separate models per horizon for the h0-h4 curve.
- `dashboard/README.md:45-61` claims the build reuses the exact estimator code and that the consistency gate reproduces 0.983 and refuses to write if the check fails.

Why it matters:
The dashboard reuses the same feature list and estimator class, but it does not use the same training protocol for emitted predictions. It fits one all-horizon model on all labeled history through 2025, while the eval scripts fit horizon-specific models when reporting horizon behavior. The verification AUC only proves a separate h=1 train+val/test reproduction; it does not test the pooled model used in `window.DASH`.

Concrete failure scenario:
Using the same estimator/features and labeled history, I compared the dashboard's pooled all-horizon fit to horizon-specific fits on the 2026-05-17 snapshot. The pooled-vs-h-specific difference exceeded 5 percentage points on 98 of 641 forecast rows and exceeded 10 points on 51 rows; 35 rows crossed a Watch/Warning boundary. Example: Lake Ocklawaha h2 was 61.5% under the pooled dashboard recipe versus 13.8% under an h-specific recipe. That can change both ranking and tier.

The AUC gate is also loose: `dashboard/build_dashboard_data.py:199` accepts any h1 AUC from 0.950 to 0.995. `models/outputs/fusion_eval.md:31-35` shows ablations such as `-WEATHER` and `-INSITU` still report AUC 0.983, so this gate would not catch important feature-block omissions.

### 4. Forecast figures lack uncertainty intervals even though the governing claim gate requires uncertainty on every figure

Verdict: CONFIRMED

File/lines:
- `dashboard/index.html:404-408` renders the forecast bar chart as point bars only.
- `dashboard/index.html:417-423` renders observed history with threshold lines only.
- `dashboard/index.html:426-430` renders disagreement deltas as point bars only.
- `dashboard/index.html:220-223` prints the AUC point estimate and tier thresholds without confidence intervals.
- `dashboard/README.md:24-28` describes forecast, history, disagreement, and fleet figures, but no uncertainty.

Why it matters:
The dashboard includes baselines in the forecast chart (`ladder`, `clim`, `EPA`) and deltas, but it does not carry uncertainty for the point forecasts, deltas, AUC gate, or observed-history threshold interpretation. That directly misses the stated standard: every figure carries a baseline and uncertainty, and the tool must not imply more certainty than the model supports.

Concrete failure scenario:
A lake at 41% fusion risk is displayed as crossing "Warning >= 40%" with no confidence band or calibration uncertainty. A user can reasonably read that as materially different from 39% or from climatology/EPA, even though the underlying model evaluation reports uncertainty only in separate markdown outputs and not for the dashboard prediction.

### 5. Bloom duration is computed with an `end_date <= cutoff` boundary while bloom state uses the cutoff week's feature row

Verdict: CONFIRMED

File/lines:
- `dashboard/build_dashboard_data.py:175-185` computes duration from rows where `end_date <= cutoff`.
- `dashboard/build_dashboard_data.py:269-294` computes `clear_now` / `blooming_now` from `persistence` in the snapshot row, then computes duration separately.
- `dashboard/build_dashboard_data.py:333` displays `cyan_now` from the cutoff feature row.
- `dashboard/index.html:349` says duration is consecutive observed bloom weeks up to issue.

Why it matters:
For the 2026-05-17 cutoff, the feature row corresponds to the CyAN week starting 2026-05-17, while `end_date <= 2026-05-17` excludes that week because it ends on 2026-05-23. Thus `blooming_now` and `cyan_now` are from the cutoff week, but `duration_wk` is from the previous week.

Concrete failure scenario:
West Lake is `blooming_now=true` with `cyan_now=225.0`, but the emitted duration is 32 weeks. Counting the cutoff week by `start_date <= cutoff` gives 33 weeks. Across the bundle, 46 lakes differ under the cutoff-week-inclusive calculation. Some clear-at-cutoff lakes retain a stale nonzero `duration_wk` from the prior week, although the UI usually hides that value for clear lakes.

### 6. "Latest cutoff carrying a full h0-h4 forecast" is only true globally, not per lake; the UI silently drops missing horizons

Verdict: CONFIRMED

File/lines:
- `dashboard/build_dashboard_data.py:15-17` says `FORECAST_CUTOFF` is the latest cutoff carrying a full h0-h4 forecast.
- `dashboard/build_dashboard_data.py:220-232` selects snapshot rows for the cutoff but does not require each lake to have h0-h4.
- `dashboard/build_dashboard_data.py:274-290` silently skips missing `(comid, horizon)` pairs.
- `dashboard/index.html:226-233` builds the horizon selector from the first lake that has five forecasts.
- `dashboard/index.html:328-330` filters the alert list to lakes that have the selected horizon forecast.
- `dashboard/data/dashboard_data.js:1` emits `n_lakes=131`, not the 133 resolvable lakes described in the UI/README.
- `dashboard/README.md:47-49` says the build scores cutoff 2026-05-17, horizons 0-4.

Why it matters:
The cutoff is the latest date with at least one row for each horizon, but not every lake has all five horizons. The generated bundle has 122 lakes with all five horizons and 9 lakes missing at least one horizon. Six lakes lack h1, the default alert horizon.

Concrete failure scenario:
Mangonia Lake appears in the bundle with horizons `[0,2,3,4]`, no h1. On the default h1 alert view, it is silently excluded from the ranked clear-lake list. A user may interpret absence from the list as low risk rather than missing model output.

### 7. h0 is presented as a forecast option without the documented diagnostic-only caveat

Verdict: CONFIRMED

File/lines:
- `models/docs/02-feature-catalog.md:32-36` says h0 is a coincident nowcast / diagnostic only and excluded from operational forecast claims.
- `dashboard/index.html:123` labels the selector "Forecast target week".
- `dashboard/index.html:145-147` says "Bloom probability (%) for each forecast target week".
- `dashboard/index.html:226-233` includes all horizons from the first full forecast, including h0.
- `dashboard/README.md:18-24` describes the Alerts tab as forecast probability with a forecast-target-week selector.

Why it matters:
The model documentation specifically limits h0. The dashboard makes h0 selectable in the same "forecast" control as h1-h4, without a UI caveat that h0 is diagnostic/nowcast-only under the modeling protocol.

Concrete failure scenario:
A user selects h0 and reads the displayed probability as an operational forecast from the 2026-05-17 cutoff, rather than the special diagnostic horizon described in the model documentation. This can inflate perceived short-lead capability.

### 8. The observed-history panel includes post-cutoff observations without visually separating them from pre-issue observations

Verdict: PLAUSIBLE

File/lines:
- `dashboard/build_dashboard_data.py:310-317` emits observed CyAN and chl-a history from `HISTORY_FROM` forward without truncating at the forecast cutoff.
- `dashboard/build_dashboard_data.py:347-359` sets `obs_last` from the full observed table, which is 2026-06-27 in the generated bundle.
- `dashboard/index.html:150-154` labels the panel "Observed history" but does not mark the forecast cutoff.
- `dashboard/index.html:213-216` states forecasts are issued from data as of 2026-05-17 and observations run through 2026-06-27.

Why it matters:
This may be acceptable for a retrospective demonstration, but the chart mixes pre-cutoff context with observations from the target period and after the issue cutoff. Without a vertical cutoff marker, users can visually inspect realized post-cutoff CyAN values beside forecast bars and mistake them as information that was available at forecast time.

Concrete failure scenario:
For a target week after 2026-05-17, the deep-dive history line can already show CyAN observations through 2026-06-21 / 2026-06-27 while the forecast chart says the forecast was issued from the 2026-05-17 cutoff. A user could overtrust the forecast because the realized future trajectory is visible on the same page.

## Checks With No Negative Finding

- AL1 threshold labeling is consistent with `models/docs/03-target-definition.md:10-26`: median CyAN DN >= 130 is the WHO AL1 operationalization, and the dashboard labels forecasts as probability rather than chlorophyll concentration in `dashboard/index.html:145-154` and `dashboard/README.md:35-41`.
- Forecast-target date algebra is consistent in the table for the selected cutoff: for the 2026-05-17 feature date, `target_date - feature_date = 7*(h+1)` for h0-h4, matching `models/docs/02-feature-catalog.md:20-27`.
- Climatology lookup in the dashboard fit is built from `fit = train+val+test` only (`dashboard/build_dashboard_data.py:213-216`) and does not include the 2026 `oos_partial` snapshot rows. That is temporally clean for a 2026 snapshot, although it differs from the train+val evaluation protocol.
- Onset display logic matches the stated rule: `dashboard/index.html:293-294` returns the first horizon whose fusion risk is at or above `META.tiers.warning`, and the alert list labels it as first h0-h4 reaching Warning in `dashboard/index.html:333-340`.
- Disagreement deltas use the correct sign and scale: `dashboard/build_dashboard_data.py:288-289` computes `(fusion - reference) * 100`, and `dashboard/index.html:159-160` explains positive as more risk than the reference.
- The staleness note is accurate for model inputs: `TRACK_A` includes `cyan_gap_weeks_at_cutoff`, `wqp_TP_stale`, and `wqp_chl_a_stale` (`dashboard/build_dashboard_data.py:60-70`), while the UI displays other WQP/NWIS ages for context (`dashboard/build_dashboard_data.py:104-111`; `dashboard/index.html:165-168`).

---

## Reconciliation (applied 2026-07-06, verified independently)

All 8 findings were independently reproduced before acting (pooled-vs-per-horizon: 98/641 rows >5pts,
Ocklawaha h2 61.5%→13.8%; WQP TP max 312 mg/L, 141 negative chl-a; duration off-by-one; 6 lakes missing h1).

- **F3 (per-horizon):** FIXED — the build now fits a **separate model per horizon** (matching `eval_fusion`).
  Curves vary properly with lead (Ocklawaha h2 now 13.8%). Added **Gate B**: the shipped per-horizon fusion
  is scored on the held-out 2026 period (AUC h0 0.99 → h4 0.98), so the gate now validates the *emitted* model.
  Gate A band tightened to 0.975–0.990.
- **F1 (WQP artifacts):** FIXED — non-physical raw readings dropped (negatives, impossible magnitudes; 0 remain,
  max TP now 0.8 mg/L); in-situ relabelled **raw/unharmonized** (`*`) with a UI caveat.
- **F5 (duration off-by-one):** FIXED — `start_date <= cutoff` includes the cutoff week; clear lakes → 0.
- **F2 (EPA information-set):** FIXED — note corrected; the vs-EPA comparison is flagged fair at 1–2 wk and
  increasingly favourable to EPA at longer leads.
- **F4 (uncertainty, light per user):** FIXED — prominent point-estimate caveat + borderline tiers marked `~`
  (dashed pill) when within 5 pts of a tier line.
- **F6 (missing horizons):** FIXED — banner reports "131 of 133 (122 with all 5 horizons)"; the alert list
  counts lakes with no forecast at the selected horizon; the map shades them distinctly (not as "Low").
- **F7 (h0):** FIXED — h0 labelled "nowcast (diagnostic)" in the selector with an on-view caveat.
- **F8 (post-cutoff observations):** FIXED — observed-history chart draws the issue-cutoff line and shades the
  realized-after-issue region.

Numbers regenerate from `build_dashboard_data.py`; both gates pass. Verified via headless render of both tabs.

## Follow-up: Gate B AUC skepticism (user, 2026-07-06) — investigated, no leakage, presentation corrected

User flagged the Gate B AUC (0.99→0.98) as suspiciously high/flat. Independent audit (scratchpad/audit_auc.py):
- **Persistence baseline alone scores 0.95→0.90 AUC** on the same 2026 rows — the high AUC is autocorrelation /
  between-lake structure (documented AR-dominance), not fusion skill or leakage.
- The recipe **reproduces the published 2025 curve** (fit train+val→predict test 2025: fusion 0.989→0.974; h1 0.984 ≈ published 0.983).
- 2026 is only ~0.004 easier than 2025 (marginally more separable partial year), not leakage.
- **Onset signal (the honest one):** persistence onset-MCC = 0.000 at every horizon (no onset skill by construction);
  fusion onset-MCC = +0.45..+0.53, onset-AUC 0.96→0.93. That gap is fusion's real, modest value.

**Correction applied:** Gate B now reports fusion AUC **beside the persistence baseline** and the onset-AUC in both
the build output and the page footer — a bare AUC without its baseline was itself a claim-gate violation. onset-AUC
is ranking-optimistic (still partly chronic-lake structure); the deployable operating figure is onset-MCC ~0.47 (deck).
