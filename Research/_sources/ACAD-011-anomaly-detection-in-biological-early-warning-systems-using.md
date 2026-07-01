---
key: ACAD-011
title: Anomaly Detection in Biological Early Warning Systems Using Unsupervised Machine Learning
authors_or_org: Grekov, Aleksandr N.; Kabanov, Aleksey A.; Vyshkvarkova, Elena V.; Trusevich, Valeriy V.
year: 2023
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10007031/
access_date: 2026-07-01
tier: ACAD
source_type: Peer-reviewed journal article (open access)
categories: [models-and-methods]
relevance: Medium
full_text_access: full
fetch_status: ok
review_severity: flagged
review_overall: flag
---

# Anomaly Detection in Biological Early Warning Systems Using Unsupervised Machine Learning

**What it is.** A peer-reviewed methods paper (Sensors, 2023, 23(5):2687) that benchmarks four unsupervised anomaly-detection algorithms — elliptic envelope, isolation forest, one-class SVM, and local outlier factor — for real-time detection of pollution-driven behavioral anomalies in a freshwater bivalve (Unio pictorum) biological early-warning system, using Hall-sensor valve-gap data from the Chernaya River, Crimea (Feb–Apr 2017).

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** The study benchmarks four classic unsupervised anomaly-detection algorithms — elliptic envelope, isolation forest (iForest), one-class SVM, and local outlier factor (LOF) — for detecting pollution-related behavioral anomalies in real-time bivalve-mollusk biomonitoring data.
  - *evidence:* Stated directly in the abstract as the paper's core method and stated objective ("to investigate the feasibility of using four traditional unsupervised machine learning algorithms for anomaly detection in the behavioral reactions of mollusks"). (Abstract; Introduction (objective statement))
  - *quote:* "Four traditional unsupervised machine learning techniques were implemented to detect emergency signals in the activity of bivalves: elliptic envelope, isolation forest (iForest), one-class support vector machine (SVM), and local outlier factor (LOF)."
- **[✓ verified]** With properly tuned hyperparameters, three of the four algorithms (elliptic envelope, iForest, LOF) achieved perfect classification (F1 score = 1) on the labeled anomalies, i.e. no false positives or false negatives.
  - *evidence:* Reported as the headline result in the abstract and conclusion, and detailed per-algorithm in Results with the specific averaging-window and contamination-rate ranges that reach F1=1 (e.g., elliptic envelope at 15-min averaging with contamination rate <0.0005; iForest at several T/n combinations with contamination rate <0.001; LOF at k=100, 1-min averaging, contamination rate=0.0001). (Abstract; Results (per-algorithm subsections); Conclusion)
  - *quote:* "the use of the elliptic envelope, iForest, and LOF methods with proper hyperparameter tuning can detect anomalies in mollusk activity data without false alarms, with an F1 score of 1."
- **[⚠ partial]** Among the three successful algorithms, isolation forest detected the labeled anomalies fastest, with a lead of about 45 minutes over LOF and almost 10 hours over elliptic envelope on the second anomaly event.
  - *evidence:* Derived from the paper's Table 1 comparison of per-algorithm detection timestamps for the three anomalies, with the timing gap explicitly quantified in the discussion text for anomaly 2. (Results (Table 1) and Discussion)
  - *quote:* "The LOF algorithm with hyperparameters data averaging 5 min, cr = 0.001, and k = 50 is 45 min behind the best result obtained by the iForest method... The best response time of the model and detection of the second anomaly using the elliptic envelope algorithm is almost 10 h behind the detection time by the iForest algorithm."
  - *reviewer:* The 45-minute LOF timing gap is not explicitly tied to anomaly 2 in the source; only the 10-hour elliptic envelope comparison is explicitly stated as referring to the second anomaly.
- **[✓ verified]** One-class SVM performed markedly worse than the other three algorithms: F1 stayed at or below 0.2 with the RBF kernel and reached only 0.55 at best with sigmoid or polynomial kernels under specific hyperparameters.
  - *evidence:* Explicit numeric F1 results reported per kernel type and hyperparameter combination in the results section, and summarized as "unsatisfactory." (Results (One-Class SVM subsection))
  - *quote:* "Unsatisfactory results (F1-score < 0.2)... F1 score values reach 0.55 with γ equal to 0.05, the poly kernel type with nu 0.001 and 0.005, and with the kernel type sigmoid and γ = 0.001 with nu 0.005."
- **[✓ verified]** The dataset comprised valve-gap displacement time series sampled every 10 seconds from 14 usable Unio pictorum mussels (of 16 installed) on the Chernaya River, Crimea, evaluated with a rolling 5-day-train/1-day-test scheme yielding 38 subsets, with 43,200 training points and 8,640 test points per mussel per subset.
  - *evidence:* Directly stated dataset and experimental-design description in the Methods section. (Methods (biomonitoring setup and data-processing description))
  - *quote:* "Each 5-day training subset was a 43,200-point time series for each of the 14 mussels... Each 1-day test subset was a time series of 8640 points for each of the 14 mussels."
- **[⚠ partial]** Ground truth for evaluation was limited to three anomalies over the roughly two-month study period (26 Feb–24 Apr 2017), identified only by expert review at day-level resolution, with no exact onset time known.
  - *evidence:* Authors state this explicitly as a scope constraint on their own evaluation. (Discussion/Limitations)
  - *quote:* "3 days of anomalies identified by experts during data analysis. The exact time (hour, minute, and second) of occurrence of the anomaly is unknown."
  - *reviewer:* The specific study-period dates (26 Feb–24 Apr 2017) do not appear in the source text and are hallucinated. The ground truth scope (3 anomalies, expert-identified, no exact timing) is supported.
- **[⚠ partial]** The anomalies coincided with heavy rain, a 2–4 °C water-temperature drop, and increased turbidity, and were attributed by the authors to probable agricultural runoff (fertilizers/pesticides) rather than to algal toxins — the paper does not address harmful algal blooms.
  - *evidence:* This is the authors' own interpretation of the likely cause of the observed mollusk behavioral anomaly, explicitly hedged as speculative ("quite likely"), not a confirmed causal finding. (Discussion)
  - *quote:* "a decrease in water temperature by 2–4 degrees and an increase in water turbidity were recorded, according to the data of the laboratory for water quality monitoring... It is quite likely that toxicants from adjacent agricultural fields, where fertilizers and pest control agents were used, entered the riverbed along with soil washouts, which explains such an intense reaction of mollusks."
  - *reviewer:* The term 'heavy rain' does not appear in the source text. The temperature drop (2–4°C), increased turbidity, agricultural runoff attribution, and absence of HAB discussion are all supported.
- **[✓ verified]** Performance was highly sensitive to the contamination-rate hyperparameter and to the temporal-averaging window, which differed by algorithm (best at 15 min for iForest and elliptic envelope, 1–5 min for LOF); too high a contamination rate caused false positives, too low caused missed anomalies.
  - *evidence:* Stated as an explicit methodological caveat/lesson in the discussion, directly tying hyperparameter choice to error type. (Discussion/Limitations)
  - *quote:* "If the contamination rate is set too high (e.g., >0.001 for iForest), it would force the model to misclassify points as anomalies. If it is set too low (e.g., <0.0001 for and elliptic envelope with some averages), the model might miss some anomalies."
- **[✓ verified]** The authors flag that other unsupervised methods (DBSCAN, autoencoders, PCA) were not tested in this study and are left to future work, along with clustering-based behavior-pattern identification.
  - *evidence:* Stated as an explicit scope limitation and future-work direction. (Discussion/Future work)
  - *quote:* "Other unsupervised machine learning algorithms, such as DBSCAN, autoencoders, and principal component analysis, among others...are also commonly used for this task by researchers. Our future research will focus on exploring the potential of these algorithms in resolving the problem of anomaly detection in experimental data on mollusk activity and identifying behavior patterns in the activity of bivalves using clustering methods of unsupervised machine learning algorithms."
- **[✓ verified]** The authors position the tuned anomaly-detection algorithms as software components for a real-time biological early-warning system meant to trigger alarms for pollution events, intended to support sustainable water-body management and monitoring.
  - *evidence:* Stated as the paper's applied conclusion/implication for deployment. (Conclusion)
  - *quote:* "The machine learning algorithms proposed and studied in the work can be used for anomaly detection in the experimental data of mollusk activity for inclusion in the software of biological early warning systems to receive an alarm in real time."

## Data / numbers
- F1 score = 1.0 (perfect precision & recall, no false positives/negatives) achieved by elliptic envelope, isolation forest, and LOF, each under specific tuned hyperparameters
- One-class SVM, RBF kernel: F1 score ≤ 0.2 ("unsatisfactory")
- One-class SVM, sigmoid kernel (γ=0.001, nu=0.005) or poly kernel (γ=0.05, nu=0.001 or 0.005): F1 score = 0.55 (best case)
- 16 mollusks installed; 14 yielded usable data (mollusks no. 1 and 16 failed)
- Valve-gap (Hall sensor) sampling interval: 10 seconds
- Training subset: 43,200 data points per mussel per 5-day window
- Test subset: 8,640 data points per mussel per 1-day window
- 38 total rolling 5-day-train/1-day-test subsets
- Study period: 26 Feb 2017 to 24 Apr 2017 (Chernaya River, Crimea)
- 3 expert-identified anomaly events used as ground truth for the whole study period
- Water temperature drop of 2–4 °C recorded around the anomaly period
- iForest detection lead over LOF: ~45 minutes (anomaly 2, best configurations of each)
- iForest detection lead over elliptic envelope: ~10 hours (anomaly 2, best configurations of each)
- Elliptic envelope F1=1 thresholds: contamination rate <0.0005 at 15-min averaging, or 0.0005–0.001 at 5-min averaging
- iForest F1=1 configurations (contamination rate <0.001): (T=5, n=256, 30-min avg); (T=5, n=150, 15-min avg); (T=50, n=70, 15-min avg)
- LOF F1=1 configuration: k=100 neighbors, 1-min averaging, contamination rate = 0.0001
- Software: Python 3.9.12, scikit-learn 1.0.2
- Anomaly-1 detection timestamps across tuned configurations ranged 17:15–19:51; anomaly-2 ranged 03:45–17:30; anomaly-3 ranged 18:15–18:45 (Table 1, as rendered — treat exact per-cell values as approximate)

## Methods
Compares four unsupervised anomaly-detection algorithms — elliptic envelope (Mahalanobis-distance/Gaussian covariance based), isolation forest, one-class SVM (rbf/sigmoid/poly kernels), and local outlier factor — implemented in Python 3.9.12 with scikit-learn 1.0.2, on real-time valve-gap displacement data (10-second Hall-sensor sampling) from 14 usable Unio pictorum freshwater mussels (of 16 installed) in the Chernaya River, Sevastopol region, Crimea, 26 Feb–24 Apr 2017. Evaluated with a rolling 5-day-train/1-day-test scheme (38 subsets: 43,200 training points and 8,640 test points per mussel per subset), sweeping temporal-averaging windows (none, 1, 5, 15, 30 min) and feature scaling (none, StandardScaler, MinMaxScaler), scored by F1 (harmonic mean of precision and recall) plus false-positive/false-negative counts against 3 expert-labeled anomaly days. Elliptic envelope, iForest, and LOF each reach F1=1 with algorithm-specific tuning of contamination rate and averaging window (iForest fastest to detect, and least sensitive of the three to hyperparameter choice per the authors); one-class SVM underperforms across all kernels tested (F1 0.2–0.55) and is characterized as unsatisfactory for this task.

## Stated limitations
Ground truth was limited to only 3 anomalies over the ~2-month study window, with exact onset time unknown (only the day identified by expert review), constraining the precision of any timing evaluation. The optimal temporal-averaging window differed by algorithm (LOF best at 1–5 min; iForest and elliptic envelope best at 15–30 min), and results were explicitly described as highly sensitive to the contamination-rate hyperparameter — set too high it causes false positives, too low it risks missed anomalies. The true cause of the anomalies (natural event such as heavy rain vs. technical/sensor malfunction) could not always be established with certainty. Two of 16 installed mollusks failed and were excluded from analysis. The authors state they deliberately avoided algorithm choices/configurations that would increase computational complexity or response latency, since the goal is integration into an existing real-time field device, which may trade off against detection accuracy. Other unsupervised methods (DBSCAN, autoencoders, PCA) were not tested and are left to future work. Data described as "available upon request" rather than openly archived, limiting independent reproducibility.

## Tensions with other findings
This is not a harmful-algal-bloom (HAB) paper: it studies general aquatic pollution/anomaly detection via bivalve behavior in a river, and the authors attribute the observed anomalies to suspected agricultural runoff (fertilizers/pesticides) plus rainfall/turbidity/temperature changes, not to algal toxins or blooms; no cyanobacteria, chlorophyll, or HAB terminology appears in the fetched text. Its relevance to a HAB early-warning tool is therefore at the methods/evaluation-design level (a rigorous, hyperparameter-swept, F1-based comparison of classical unsupervised anomaly detectors on noisy real-world environmental time series, with isolation forest emerging as fastest and least finicky) rather than as direct HAB evidence. It is also a useful cautionary analog for the "claim gate" in this project: the paper's F1=1 results, while genuine, rest on only 3 labeled anomaly-days over ~2 months, a small-N ground truth that should temper confidence when similar unsupervised-anomaly-detection/F1 framing is applied to sparse HAB bloom-onset labels. The source itself also flags a tension with prior literature, noting (via a citation to Russo et al., 2021) that supervised models have been found to outperform unsupervised ones in water-quality-monitoring contexts, which complicates any assumption that unsupervised anomaly detection is uniformly the best-performing approach for aquatic early-warning systems generally.

## Blind adversarial review
- **Overall:** flag
- **Unsupported claims:** 0
- **Possible hallucinated/misattributed numbers:**
  - 26 Feb–24 Apr 2017
  - heavy rain
- **Dropped caveats:**
  - The conclusion contradictorily claims one-class SVM showed 'good performance' despite results showing F1 ≤ 0.55
  - Design constraint to avoid increasing computational complexity and equipment load
- **Reviewer notes:** Two hallucinated details found: (1) Claim 6 invents the study-period dates 26 Feb–24 Apr 2017, which do not appear in the source text; (2) Claim 7 cites 'heavy rain' as part of the anomaly context, but this is not mentioned in the provided source excerpt. Claim 3 is loosely supported on magnitudes but lacks explicit confirmation that the 45-minute LOF–iForest gap applies specifically to anomaly 2 (only the 10-hour elliptic envelope gap is explicitly tied to anomaly 2). All other claims are well-supported by direct quotation or clear inference from the source."

## Provenance
- Canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10007031/
- Access date: 2026-07-01
- Full-text access: full | Fetch status: ok
- Fetch notes: WebFetch succeeded on the first try against the primary PMC URL (https://pmc.ncbi.nlm.nih.gov/articles/PMC10007031/) with no redirect, no binary/garbage content, and no need for a fallback WebSearch. Per instructions for a High-relevance source, I fetched it twice with differently-worded extraction prompts (one general "extract everything faithfully" prompt, one section-by-section citation/methods/results/discussion prompt) and reconciled the two. The two extractions were highly consistent on all substantive figures (F1 scores, sample sizes of 14/16 mussels, 43,200/8,640 data points, 38 subsets, contamination-rate thresholds, the 45-min and ~10-h detection-time gaps, study dates, funding/COI statements), which gives confidence the underlying full text (abstract, methods, results incl. Table 1, discussion, limitations, funding) was genuinely retrieved rather than hallucinated. The one place the two fetches diverged was granularity of the per-cell timestamps in Table 1 (one fetch gave a full per-configuration breakdown, the other only summary ranges) — the ranges matched perfectly, so I report the ranges plus the two figures that were given in direct-quote form in both extractions (45 min; ~10 h) as reliable, and flag the fully granular per-cell Table 1 timestamps as approximate/extraction-dependent rather than verbatim-quotable. No numbers were paraphrased/rounded beyond what is noted.
