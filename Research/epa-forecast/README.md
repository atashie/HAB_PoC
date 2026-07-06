# EPA CyanoHAB forecast — supplemental materials review (Schaeffer et al. 2024)

Review of the **supplemental appendices** to the paper behind our federal baseline:

> Schaeffer, B.A., Reynolds, N., Ferriby, H., Salls, W., Smith, D., Johnston, J.M., Myer, M. (2024).
> *Forecasting freshwater cyanobacterial harmful algal blooms for Sentinel-3 satellite resolved U.S.
> lakes and reservoirs.* Journal of Environmental Management 349, 119518.
> DOI [10.1016/j.jenvman.2023.119518](https://doi.org/10.1016/j.jenvman.2023.119518) · source key **ACAD-050 / FED-017**.

**Files in this folder (the raw appendices, as downloaded):**

| File | What it is |
|------|-----------|
| `1-s2.0-S030147972302306X-mmc1.docx` | Supplemental Material and Methods — study area, satellite processing, performance-metric definitions, supplemental discussion, supplemental figures S1–S7, supplemental references |
| `1-s2.0-S030147972302306X-mmc2.xlsx` | **Table S1** — evaluation metrics for the six comparison models, split by **Florida** and **CONUS** |

**Provenance.** Publisher supplementary files for ScienceDirect PII `S030147972302306X` (= the ACAD-050
paper). Obtained 2026-07-05; reviewed 2026-07-06. The `.docx` was text-extracted deterministically with
`python-docx` (`docx.Document(...).paragraphs`); Table S1 was read from the `.xlsx` with `openpyxl`
(`data_only=True`). Everything quoted below traces to those two files.

**Why this review exists.** These appendices (a) give the **Florida-vs-CONUS performance split** we did not
previously have, (b) add **methodological detail** salient to how faithfully we reproduce the baseline, and
(c) let us **cross-check our own head-to-head evaluation** of the deployed forecast in Florida
(`../../models/outputs/epa_headtohead.md`) against EPA's own reported numbers — building confidence we have
represented their work fairly as our benchmark.

> **Read-this-first caveat.** Table S1 reports the **six comparison models** (SVC, Random Forest, DNN, LSTM,
> RNN, GRU) — **not** the deployed INLA forecast. The paper never publishes the INLA model's *Florida-only*
> metrics; its headline metrics (acc 0.90 / precision 0.49) are **CONUS-aggregate for the 2021 test year**.
> So we cannot do a like-for-like "their-INLA-in-FL vs our-eval-of-EPA-in-FL." What we *can* do — and do
> below — is **bracket** our result between EPA's CONUS INLA and their in-sample FL comparison models, and
> show the numbers cohere through the base-rate mechanism the authors themselves invoke.

---

## 1. Table S1 — comparison-model metrics, Florida vs CONUS (verbatim)

"Results of the statistical evaluation metrics obtained from two additional machine learning models
[SVC, Random Forest] and four additional neural network models [DNN, LSTM, RNN, GRU]." Values exactly as in
`mmc2.xlsx`.

### Florida
| Model | Accuracy | Precision | Specificity | Sensitivity | F1 |
|-------|:--------:|:---------:|:-----------:|:-----------:|:--:|
| SVC | 0.9312 | 0.9073 | 0.9460 | 0.8741 | 0.89 |
| Random Forest | 0.9350 | 0.9310 | 0.9303 | 0.9396 | 0.9353 |
| DNN | 0.9336 | 0.8476 | 0.9571 | 0.8502 | 0.8489 |
| LSTM | 0.9350 | 0.8201 | 0.9502 | 0.8762 | 0.8472 |
| RNN | 0.9336 | 0.7866 | 0.9419 | 0.8990 | 0.8390 |
| GRU | 0.9357 | 0.8354 | 0.9541 | 0.8671 | 0.8510 |

### CONUS
| Model | Accuracy | Precision | Specificity | Sensitivity | F1 |
|-------|:--------:|:---------:|:-----------:|:-----------:|:--:|
| SVC | 0.8380 | **0.0295** | 0.8433 | 0.4000 | **0.0549** |
| Random Forest | 0.8492 | 0.8623 | 0.8653 | 0.8330 | 0.8474 |
| DNN | 0.6500 | 0.5800 | 0.6674 | 0.6321 | 0.6070 |
| LSTM | 0.6600 | 0.5800 | 0.6700 | 0.6450 | 0.6130 |
| RNN | 0.6600 | 0.6100 | 0.6800 | 0.6400 | 0.6260 |
| GRU | 0.6600 | 0.6500 | 0.6900 | 0.6590 | 0.6549 |

**Two things this table settles for us:**

1. **It confirms our own baseline description.** Our docs (`../../docs/plans/2026-07-02-epa-cyano-forecast-as-baseline.md`,
   ACAD-050) say the INLA model "beat SVC/RF at 0.84–0.85 accuracy (CONUS)." Table S1 CONUS: **SVC 0.838,
   RF 0.849.** Exactly right — we quoted it faithfully.
2. **It makes the base-rate → precision mechanism visible.** Hold the model constant and change only the
   region, and **precision jumps from CONUS to Florida** for every model — most starkly SVC (0.03 → 0.91),
   also RF (0.86 → 0.93) and the neural nets (~0.58–0.65 → 0.79–0.85). Florida's much higher bloom prevalence
   is doing that work. The CONUS **SVC precision of 0.0295** (F1 0.055) is a near-total collapse — a plain SVC
   cannot handle the ~9% CONUS class imbalance, which is exactly why the authors chose INLA and why they note
   the ML/NN models "could not handle … unbalanced datasets … without significant data preparation."

---

## 2. Fidelity check — our FL evaluation of the deployed forecast vs EPA's reported numbers

This is the point of the review: **have we represented the EPA forecast faithfully as our baseline?**

**Three independent measurements**, none of them the same experiment, but all of the same underlying model
family on the same task:

| # | Measurement | Scope / timeframe | Accuracy | Precision | Sensitivity/Recall | AUC-ROC | Base rate |
|---|-------------|-------------------|:--------:|:---------:|:------------------:|:-------:|:---------:|
| **A** | **EPA INLA forecast** (main text) | CONUS, 2021 independent test | 0.90 | **0.49** | 0.88 | 0.95 | ~9.1% |
| **B** | EPA comparison models (Table S1, FL) | Florida, 2017–2021, **in-sample** | ~0.93 | **0.79–0.93** | 0.85–0.94 | — | high (FL) |
| **C** | **Our eval of the *deployed* forecast** | Florida, **2025**, out-of-sample | 0.861 † | **0.731** † | 0.821 † | **0.928** ‡ | 28.8% (seasonal) |

† Row C confusion-matrix figures are from `../../models/outputs/epa_headtohead.md`, operating-point table,
in-sample-tuned threshold (**optimistic** — an upper bound on operating-point skill). ‡ AUC-ROC is
threshold-free: 0.928, 95% week-block-bootstrap CI **[0.920, 0.936]** (also 0.931 on the wider shared window
in `exp_ablation.md`). Our shared test set is **4,527 FL lake-weeks** (132 lakes × 35 seasonal weeks).

**How to read the coherence (the confidence-building argument):**

- **Discrimination.** Our FL 2025 AUC-ROC **0.928** sits just below EPA's CONUS 2021 AUC of **0.95** — the
  small gap is what you'd expect scoring a **different year, out-of-sample, against independently-constructed
  labels**, in a single region the national model was not tuned to. Recovering AUC ≈ 0.93 is strong evidence
  we are scoring the *real* forecast, not something we have mangled.
- **Precision, via base rate.** EPA's headline precision **0.49** is depressed by the ~9% CONUS base rate —
  the authors say so outright ("if the prevalence was low, it would be harder for a model to achieve high
  precision"). Florida's bloom prevalence is far higher (our seasonal window ~28.8%), so the forecast's FL
  precision **should** be well above 0.49. Our eval finds **≈0.73** — above the CONUS 0.49 (as the mechanism
  predicts) and **below** the in-sample FL comparison models' 0.79–0.93 (as expected for an out-of-sample,
  different-year, different-label evaluation of a health-protective, deliberately over-predicting model). It
  lands **exactly where it should in the bracket** A < C < B.
- **Conclusion.** Across three independent measurements — EPA's CONUS INLA, EPA's in-sample FL comparison
  models, and our out-of-sample FL evaluation of the deployed product — the numbers cohere once the base-rate
  and in-sample/out-of-sample differences are accounted for. **We have neither flattered nor understated the
  baseline.** Our head-to-head represents the EPA forecast fairly.

**Caveats stated plainly (so the check is bounded, not oversold):**

1. **Not a like-for-like number.** Table S1 FL = *comparison* models, not the INLA forecast. No published
   INLA-in-Florida metric exists; the closest is **Myer et al. 2020** (ACAD-092), the Florida INLA precursor
   this study generalized. Our bracket argument is a consistency check, not an identity.
2. **In-sample vs out-of-sample.** Row B is fit and scored on the same 2017–2021 FL data; Row C scores the
   already-deployed model on unseen 2025 weeks. B is therefore an optimistic ceiling for FL.
3. **Different labels.** Our ground truth is our own realized WHO Alert Level 1 from raw CyAN; EPA trained on
   their internal labels. Same concept, not identical construction (see `epa_headtohead.md` caveat 2).
4. **Different operating cutoff — the one concrete refinement.** The appendix pins EPA's classification cutoff
   at **0.10** (Youden's index; §3 below). Our operating-point row uses an in-sample-tuned threshold, and
   `exp_ablation.md` uses a fixed 0.5 — **neither is 0.10.** To compare *confusion-matrix* metrics
   apples-to-apples with EPA's reported precision/recall we should also score the EPA probability **at 0.10**.
   → concrete next step for `../../models/model/eval_epa_headtohead.py`. (The primary comparison is the
   **threshold-free** AUC/AUC-PR/Brier, which is unaffected by cutoff choice, so this refines rather than
   corrects the finding.)

---

## 3. Salient methodological details harvested from `mmc1.docx`

New or sharper detail beyond what the ACAD-050 dossier already recorded (all trace to the supplement):

- **Lake-level value construction.** "The median of CIcyano pixel values was calculated to represent each
  lake's cyanobacteria bloom condition in each week," on the **weekly-maximum** satellite composite.
  → *Check our CyAN aggregation matches: weekly-max composite → median-of-pixels per lake.*
- **CyAN processing v4.0**, **300 m**, weekly maximum detections, **Jan 2017 – Dec 2021**, from Sentinel-3A/B
  OLCI via NASA OBPG (`l2gen` / SeaDAS).
- **Land mask:** SRTM-derived **60 m** mask; explicitly **static w.r.t. waterbody size** — does not adjust for
  drought/flood, a known edge/small-lake limitation.
- **Classification cutoff = 0.10**, chosen by **maximizing Youden's index** on the validation set (Fig. S2).
  This is the operating point behind the 0.49 precision — important for any apples-to-apples confusion matrix.
- **Study-area lineage.** This study **expanded from Myer et al. 2020's 103 Florida lakes** (ACAD-092) to all
  nine CONUS climate regions. Florida is the sub-tropical tail: Tropical Wet Forest + Temperate Sierras were
  ~0.5% of lakes; the study is dominated by Eastern Temperate Forest (39.5%), Northern Forest (22.8%), Great
  Plains (20.8%). → **The deployed model is temperate-dominated; its Florida behavior is an extrapolation to
  an under-represented regime**, which makes our Florida evaluation a genuinely informative test.
- **Florida winter/late-fall bloom gap.** The CONUS AR(1) seasonal trend (Fig. S5) initiates Apr–Jun, peaks
  Jul–Sep, declines Sep–Nov, with only a "small rise in January." The authors note this **differs from
  Florida** (Myer 2020): FL shows increased log-odds in May and a **strong secondary increase Nov–Dec**, and
  **Florida winter blooms were confirmed** (Coffer et al. 2020). They attribute the national model's missing
  secondary peak to "the signal being dampened by lakes in northern climate zones." → **A concrete place a
  Florida-tuned model could add value over the federal baseline: off-peak (late-fall/winter) onsets** —
  consistent with our head-to-head finding that the differentiator is on *flips/onsets*, not persistence-easy
  weeks.
- **Performance-metric definitions** (Eqs. 4–11): accuracy, sensitivity, specificity, precision, false
  omission rate, F1, Kappa, Brier score — standard, and the same set we report. AUC via ROC (Fig. S2).
- **"GRU," not "GNU."** ACAD-050's blind review flagged a possible model-name error ("Gneural Network (GNU)"
  vs "GRU"). **Table S1 labels the sixth model `GRU`** — resolving the flag: the six comparison models are
  **SVC, Random Forest, DNN, LSTM, RNN, GRU**.
- **Supplemental discussion** also covers cyanoHAB-weeks vs spatial extent (upper quantile ≥41 cyanoHAB weeks
  → median 100% spatial extent) and the spatial random effect as residual location error from unmeasured
  predictors (soil, slope, land use, nutrients, stratification) — the mechanism by which regional (e.g.
  Florida) idiosyncrasy is partly absorbed CONUS-wide rather than modeled explicitly.

---

## 4. Carry-forward for our build

- **Baseline fidelity: confirmed.** Cite the head-to-head as a *fair* representation of the EPA forecast;
  the bracket A < C < B and the AUC recovery are the evidence. (§2)
- **Score EPA at cutoff 0.10** in `eval_epa_headtohead.py` for an apples-to-apples confusion matrix vs EPA's
  own 0.49 precision / 0.88 sensitivity. (§2 caveat 4, §3)
- **Class imbalance is real for plain classifiers.** CONUS SVC precision 0.03 is the cautionary tale; our own
  SVC family needs explicit imbalance handling, and FL's higher base rate is *why* SVC is even viable here
  (FL SVC precision 0.91). (§1)
- **Where we might beat the federal baseline:** Florida late-fall/winter onsets that the temperate-dominated
  CONUS model dampens. (§3) A hypothesis to test honestly — not a claim.
- **Aggregation to confirm:** weekly-max composite → median-of-pixels per lake. (§3)

**Cross-references:** ACAD-050 source dossier (`../_sources/ACAD-050-forecasting-freshwater-cyanobacterial-harmful-algal-blooms-f.md`,
now carrying a "Supplemental materials review" section) · baseline strategy
(`../../docs/plans/2026-07-02-epa-cyano-forecast-as-baseline.md`) · our head-to-head
(`../../models/outputs/epa_headtohead.md`) · Florida INLA precursor Myer et al. 2020 (ACAD-092).
