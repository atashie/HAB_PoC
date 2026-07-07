# Codex Review - HAB Modeling Workflow Technical Correctness

Scope reviewed: acquire -> prepare -> model -> evaluate, including requested code, derived parquet spot-checks, outputs, docs, and EPA forecast provenance code. Ranked most severe first.

## 1. CONFIRMED - Feature-selection screens use held-out years despite the train-only claim

**Files/lines:** `models/model/assess_static_features.py:63-68`; `models/model/screen_insitu_features.py:130-137`; `models/model/screen_weather_features.py:56-80`; contradicted by `models/DESIGN.md:42-45` and `models/DESIGN.md:210-214`; selected features are then treated as screened candidates in `models/prepare/assemble_fusion_table.py:7-11`.

**Why:** The static, in-situ, and weather screens read the full target table and full feature history, then compute associations over all years. The design explicitly requires feature assessment/statistical inclusion to run on training years only and be frozen before held-out evaluation. This is target-aware feature selection on val/test/oos years, even if the downstream model fitting is temporally split.

**Concrete failure scenario:** A weather or WQP variable has no real training-era association but happens to separate bloom/non-bloom weeks in 2025/2026. It passes the permissive p<0.1 screen, is added to the fusion table, and is later described as a candidate driver or as part of a rigorously tested fusion block. The held-out test is no longer a clean held-out test for feature inclusion.

**Verdict:** CONFIRMED. This is the largest claim-gate violation because it affects feature set construction before modeling.

## 2. CONFIRMED - Non-CyAN temporal predictors are joined one week too stale versus the documented feature-availability matrix

**Files/lines:** `models/prepare/assemble_fusion_table.py:3-5`, `models/prepare/assemble_fusion_table.py:100-120`; documented availability differs in `models/docs/02-feature-catalog.md:37-60`.

**Why:** The fusion assembler joins WQP/NWIS/weather on `feature_date`, which is inherited from the CyAN latency cutoff (`W - h - 1`). The docs say for h>=1 in-situ should be available through `W-h`, and weather should be either oracle `W` or antecedent ablation `W-h`. Current code therefore makes weather/in-situ one week older than the stated information set for h>=1.

**Concrete failure scenario:** For h=1, a TP observation or weather pattern in week `W-1` is available at the issue time under the documented protocol, but the table only permits values through `W-2`. Fusion then looks weaker, and the conclusion that weather/in-situ/morphology add no robust incremental skill may partly reflect an overly stale implementation rather than true lack of signal.

**Verdict:** CONFIRMED. Conservative timing avoids look-ahead, but it invalidates claims that the implemented fusion tested the documented information set.

## 3. CONFIRMED - EPA head-to-head operating-point metrics tune thresholds on the test/shared slice

**Files/lines:** `models/model/eval_epa_headtohead.py:148-151`, `models/model/eval_epa_headtohead.py:156-160`; output caveat appears in `models/outputs/epa_headtohead.md:60-71`.

**Why:** For EPA, ladder, and climatology, the script sets `thr = best_f1_threshold(y, p)` where `y` is the shared 2025 test label vector. The output labels this as "in-sample thresholds; optimistic, even-handed", but the strict claim gate says threshold tuning must be validation-only.

**Concrete failure scenario:** EPA's thresholded MCC/F1/Recall or our ladder's operating metrics look better than a deployable threshold would. A slide using `MCC`, `F1`, or `Recall` from this table could claim alert performance that was selected with hindsight from the test labels.

**Verdict:** CONFIRMED. Threshold-free AUC/Brier rows are still usable; operating-point rows should not support performance claims.

## 4. CONFIRMED - Onset head-to-head leaks validation labels into `clim` during threshold tuning

**Files/lines:** `models/model/eval_headtohead_onset.py:108-138`.

**Why:** `fit_all = train + val` is used to build the climatology lookup (`clim_lut(fit)`) before validation thresholds are selected. Then the validation predictions for climatology and CyAN-ladder-with-clim use that train+val climatology. This embeds validation labels into the feature values used to tune the validation threshold.

**Concrete failure scenario:** A lake-month's 2024 validation outcomes shift its climatology value upward. The validation threshold is then tuned on a feature that already contains the validation target distribution, inflating or stabilizing onset-MCC for climatology and CyAN-ladder. Fusion without `clim` is less affected, but the h1 baseline ordering in `headtohead_onset.md` is not fully clean.

**Verdict:** CONFIRMED. It is not test-label leakage, but it violates the "threshold tuned only on val predictions from train-fitted features" discipline.

## 5. CONFIRMED - In-situ values are forward-filled indefinitely, and most modeled values lack their staleness companion

**Files/lines:** indefinite ffill in `models/prepare/assemble_fusion_table.py:52-70`; feature lists omit many stale columns in `models/model/experiment_lib.py:59-60` and `models/model/eval_fusion.py:44-45`; design requires value + staleness in `models/DESIGN.md:142-143`.

**Why:** The assembler forward-fills last observations without a max-age cutoff. The output table includes stale columns for all selected in-situ variables, but most model feature lists keep only the value columns: `wqp_water_temp_val`, `wqp_ammonia_val`, `wqp_orthoP_val`, `nwis_water_temp_val`, and `nwis_gage_height_val` are used without their stale fields. A parquet spot-check showed max staleness of 464-507 weeks and 95th percentile staleness above 100 weeks for several WQP/NWIS variables.

**Concrete failure scenario:** A single 2016 ammonia, orthophosphate, or NWIS water-temperature measurement is carried into 2025 and used as if it were a current lake covariate. Without the companion stale feature, the model cannot learn that the value is nine years old. This can become a lake-identity proxy or stale historical confounder.

**Verdict:** CONFIRMED. This weakens all in-situ modeling and any "value + staleness" compliance claim.

## 6. PLAUSIBLE - `coverage_fraction == 1` is approximated, not reproduced exactly

**Files/lines:** `models/prepare/build_cyan_lake_target.py:42-45`, `models/prepare/build_cyan_lake_target.py:80-87`; disclosure in `models/docs/03-target-definition.md:42-45`.

**Why:** EPA/Schaeffer's `exact_extract(... coverage_fraction == 1)` is approximated with 8x oversampled rasterization and `coverage >= 0.999`. The documentation honestly discloses this and calls exactextract cross-validation a follow-up, but the implementation is not an exact reproduction.

**Concrete failure scenario:** A small lake has only 7 fully-inside pixels in the derived target table. One borderline edge pixel is included/excluded differently than exactextract, moving the weekly median across DN 130 and flipping the AL1 label for that lake-week.

**Verdict:** PLAUSIBLE. The deviation is documented and probably small for large lakes, but it is a target-fidelity gap for small lakes and label-flip edge cases.

## 7. CONFIRMED - Several headline claims lack uncertainty even when differences are tiny

**Files/lines:** `models/outputs/headtohead_onset.md:9-15`, `models/outputs/headtohead_onset.md:19-45`; claims in `models/RESULTS-SUMMARY.md:49-55`, `models/RESULTS-SUMMARY.md:81-100`; uncertainty requirement in `models/DESIGN.md:216-217`.

**Why:** The onset head-to-head reports point estimates only for onset-AUC and onset-MCC. The summary then says onset-AUC approximately 0.94 beats climatology and EPA, and compares fusion 0.944 vs ladder 0.943. Some wording says "approximately tied", which is good, but the table and summary still lack CIs for the onset metrics that carry the main story.

**Concrete failure scenario:** The 0.001 fusion-vs-ladder onset-AUC difference or the 0.004 ladder-vs-climatology onset-MCC difference is interpreted as an ordering. With only 158 h1 positive onsets in the shared set, that ranking could easily reverse under lake/week block bootstrap.

**Verdict:** CONFIRMED. Baselines are present, but uncertainty is missing for key onset claims.

## 8. CONFIRMED - Generated output is stale/inconsistent with current onset script wording

**Files/lines:** current script writes validation-tuned wording in `models/model/eval_headtohead_onset.py:130-138` and `models/model/eval_headtohead_onset.py:185-190`; checked-in output still says "in-sample F1 thresholds" in `models/outputs/headtohead_onset.md:5`.

**Why:** The current code and the checked-in output do not match. The output text describes the old in-sample/test-threshold convention while the current script text says validation-tuned thresholds. This is a direct reproducibility/documentation mismatch.

**Concrete failure scenario:** A reviewer reads `headtohead_onset.md` and concludes the onset operating metrics are test-tuned and optimistic. Another reviewer reads `RESULTS-SUMMARY.md` and concludes the same numbers were corrected to validation thresholds. Both cannot be true from the checked-in artifacts alone.

**Verdict:** CONFIRMED. I did not regenerate outputs because the instruction was not to modify any files except this review.

## 9. CONFIRMED - `fusion_eval.md` contains a validation/test wording contradiction

**Files/lines:** output text in `models/outputs/fusion_eval.md:3`; code split in `models/model/eval_fusion.py:100-105`.

**Why:** The output says "validation = held-out YEAR 2025" and also says "Threshold tuned on VAL 2024". The code uses `df.split == "val"` and `df.split == "test"`, which correspond to 2024 validation and 2025 test in the assembled table.

**Concrete failure scenario:** A reader may believe the model was validated/tuned on 2025 while also scored on 2025, or that the EPA temporal holdout was used as validation. This undermines the audit trail even if the code itself is using the intended split.

**Verdict:** CONFIRMED. Wording/output reproducibility issue, not a model-code bug.

## 10. PLAUSIBLE - Claims of "generalizable real-time-CyAN" exceed the validation design

**Files/lines:** `models/RESULTS-SUMMARY.md:18-20`, `models/RESULTS-SUMMARY.md:69-75`, `models/RESULTS-SUMMARY.md:178-180`; limitation is correctly stated later in `models/RESULTS-SUMMARY.md:187-188` and design limitation in `models/DESIGN.md:199-207`.

**Why:** The pipeline uses same-lake temporal validation only. It does not run the promised blocked-lake stress test. The summary does state "no unseen-lake transfer claim", but "generalizable" appears repeatedly around the deployable model and could be read as new-lake transfer rather than "not reliant on explicit COMID/clim".

**Concrete failure scenario:** A SePRO audience hears "generalizable real-time-CyAN autoregression" and assumes the model can transfer to lakes without history. The evidence only supports future-week prediction for known CyAN-resolvable lakes under same-lake temporal validation.

**Verdict:** PLAUSIBLE. The caveat exists, but the headline wording is stronger than the validation evidence.

## 11. CONFIRMED - EPA comparison is shared-row for strict head-to-head, but broader experiment EPA rows are only indicative

**Files/lines:** strict shared-row join in `models/model/eval_epa_headtohead.py:138-147`; broader experiment EPA rows in `models/model/experiment_lib.py:237-260`; caveat written in `models/model/experiment_lib.py:275-280`.

**Why:** `eval_epa_headtohead.py` correctly joins exact COMID + target week and reports seasonal/base-rate caveats. The shared harness adds EPA rows into broader experiment tables by merging the EPA snapshot into each horizon's test rows and holding the same EPA current-week probability across h0..h4. The harness labels these "indicative", but these rows should not be treated as horizon-matched head-to-head evidence.

**Concrete failure scenario:** Someone cites an EPA row from `exp_ablation.md` or `exp_change_features.md` as if EPA made a true h=4 forecast. The code is instead reusing EPA's current-week probability for the target week, which the harness itself says flatters EPA at longer leads.

**Verdict:** CONFIRMED. The strict EPA head-to-head is mostly well-caveated; the risk is downstream misuse of the experiment-table EPA rows.

## 12. PLAUSIBLE - Low-coverage target weeks are retained, but model metrics are not stratified by coverage in the reviewed outputs

**Files/lines:** target validity policy in `models/prepare/build_cyan_lake_target.py:122-131`; coverage sensitivity printed only during build at `models/prepare/build_cyan_lake_target.py:152-159`; docs note bias in `models/docs/03-target-definition.md:54-66`.

**Why:** Retaining weeks with at least one valid pixel matches the documented Schaeffer-parity target. However, a parquet spot-check found 5,906 valid target rows with `valid_frac < 0.5`. The build script prints prevalence sensitivity, but the model/evaluation outputs reviewed do not stratify the reported model metrics by target coverage.

**Concrete failure scenario:** A cloudy week with 1-2 clear pixels has median below DN 130 and is labeled no-bloom. If clouds are non-random around bloom conditions, these low-coverage labels bias both training and metrics. The issue is documented, but the headline metrics do not show whether skill changes after applying `target_valid_frac >= 0.5`.

**Verdict:** PLAUSIBLE. Not a target-definition bug under the chosen parity rule, but a missing robustness result for claims based on all rows.

## 13. CONFIRMED - Core CyAN horizon pairing itself is temporally clean in the derived tables

**Files/lines:** `models/prepare/assemble_modeling_table.py:58-82`; eval-time recheck in `models/model/eval_cyan_baselines.py:81-84`.

**Why:** The assembler pairs target week `W` to CyAN feature week `W-(h+1)` and raises on mismatches. A parquet spot-check of both `modeling_table_cyan_fl.parquet` and `modeling_table_fusion_fl.parquet` found zero bad horizon gaps.

**Concrete failure scenario checked:** A h=1 target row accidentally carries CyAN from W-1 or W. The stored `target_date - feature_date == 7*(h+1)` guard prevents this for CyAN features.

**Verdict:** CONFIRMED clean. This is a negative finding: I did not find target-week CyAN leakage in the core modeling table.

## 14. CONFIRMED - `metrics.py` implements the standard classification metrics correctly, with caveats outside the module

**Files/lines:** `models/model/metrics.py:20-25`, `models/model/metrics.py:28-53`.

**Why:** AUC-ROC, AUC-PR, Brier, MCC, F1, precision, recall, and accuracy are delegated to sklearn and thresholded consistently. Single-class AUC slices return NaN, and NaN scores fail closed.

**Concrete failure scenario checked:** Hard persistence scores are passed as 0/1 probabilities. `classification_metrics` treats them as scores for AUC/Brier and thresholds for point metrics, which is technically valid. The main problems are threshold selection in caller scripts and missing CIs, not metric formulas.

**Verdict:** CONFIRMED clean for metric formulas.

## 15. CONFIRMED - CRS/geospatial handling is mostly correct in reviewed workflow

**Files/lines:** FL lake mask CRS alignment in `models/acquire/build_fl_lake_mask.py:64-76`; BasinATLAS max-overlap in equal-area CRS in `models/prepare/join_basinatlas_l12.py:58-67`; weather centroid transform in `models/prepare/assemble_fusion_table.py:79-86`.

**Why:** The reviewed vector operations reproject before spatial predicates/area overlaps. BasinATLAS overlap is performed in EPSG:5070, and weather extraction converts lake centroids back to EPSG:4326 for ERA5 latitude/longitude selection.

**Concrete failure scenario checked:** Assigning L12 basins by centroid in WGS84 or computing overlap area in degrees. Current code avoids that by using EPSG:5070 for overlap area.

**Verdict:** CONFIRMED clean, aside from the target-mask exactextract approximation noted above.
