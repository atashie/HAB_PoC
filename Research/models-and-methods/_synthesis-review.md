# Synthesis-review verdict — models-and-methods

Blind synthesis-level review of the category README against the evidence pack (catches cross-source/aggregate claims the per-source review can't). Findings here should be reconciled into README.md before final assembly.

- **Overall:** flag
- **Synthesis claims checked:** 22
- **Unsupported synthesis claims:** 2
- **Keys cited but not in pack:** 0 
- **Miscited claims:** 0

## Unsupported synthesis claims
- **Claim:** Tree-based/gradient-boosted models are frequently competitive with, or beat, deep learning on these tabular-style tasks
  - problem: The README's supporting citation ACAD-068 reports the opposite at aggregate scale: 'deep learning models (particularly LSTM-based) showed the strongest reported performance: median R²=0.89 and >90% accuracy in many applications.' While the README later acknowledges this pattern (single-site studies favor trees; aggregate reviews favor deep learning), the headline claim overstates tree-method superiority. The subheading's own final sentence admits 'the largest cross-study review reports deep learning ahead in aggregate,' which contradicts the opening assertion.
  - suggested fix: Soften the headline to: 'Tree-based/gradient-boosted models match or occasionally exceed deep learning in single-site comparisons, though aggregate cross-study reviews report deep learning (especially LSTM) as superior on median reported performance.' Or move the reconciliation into the headline itself to avoid the contradiction.
- **Claim:** The most directly comparable published analog...reached 90% accuracy, 88% sensitivity, 91% specificity, AUC=0.95, but only 49% precision
  - problem: The underlying source (ACAD-050) contains an unresolved internal arithmetic discrepancy: stated total lake-week observations (432,030) does not match the sum of reported subsets (training 308,204 + validation 132,688 + test 113,984 ≈ 554,876). The pack itself flags this as 'an unresolved arithmetic mismatch.' The README cites the accuracy figures without disclosing this inconsistency, potentially misleading readers about the rigor of the underlying data.
  - suggested fix: Add a footnote or caveat: 'Note: The underlying paper (ACAD-050) reports an unresolved arithmetic discrepancy between stated total sample size and the sum of reported train/validation/test subsets; the 90% accuracy should be considered with this caveat pending clarification from the authors.'

## Reviewer notes
The README demonstrates strong adherence to the claim-gate principle: nearly all cross-source claims are traceable and supported by the pack. The two flagged issues are (1) a headline claim about tree-method superiority that contradicts the aggregated evidence cited in support, and (2) an undisclosed arithmetic inconsistency in a key methodological paper underlying the 90% accuracy headline. Neither is a fabrication, but both undercut the transparency standard. The README's treatment of contested findings (ACAD-037 vs. ACAD-110) is exemplary; the Gaps section is thorough and appropriately hedged. No missing keys or miscited claims were detected. Recommend resolving the two flagged issues before final publication."

---

## Resolution (applied 2026-07-01)
All flagged synthesis claims above were reconciled into README.md by the lead (main-loop edits): attributions narrowed to the single supporting source, an over-broad headline softened, and the ACAD-050 arithmetic-discrepancy caveat surfaced inline. No flag was left unaddressed.
