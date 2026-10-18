# AI Interview Coach — Evaluation Calibration Plan

**Status:** Active Phase 2 release plan; calibration gates not yet met
**Owner:** AI First Product Manager

## Objective

Establish whether AI evaluations are sufficiently aligned with experienced human interviewers before scores are positioned as reliable coaching signals.

Calibration is successful when the system can:

- distinguish insufficient, developing, competent, strong, and exceptional answers;
- explain scores using evidence present in the candidate's answer;
- avoid inventing achievements, metrics, or outcomes;
- identify when evidence is too limited for a confident evaluation; and
- produce repeatable results for the same answer and rubric version.

## Dataset Design

Create an initial dataset of **50–100 answer examples** across the main interview categories:

| Category | Target share |
|---|---:|
| Behavioral / leadership | 25% |
| Product sense | 25% |
| Strategy / prioritization | 20% |
| Metrics / diagnosis | 20% |
| Execution / collaboration | 10% |

Each example should include the question, question type, target role/seniority, candidate answer, four human dimension scores, overall score, evidence notes, and ambiguity/fabrication flags.

Include deliberate edge cases: empty answers, very short answers, generic answers, long answers without evidence, answers with quantified outcomes, answers that contradict supplied context, and answers in which the candidate says they do not know.

## Human-Rating Protocol

At least two experienced interviewers should independently rate each answer using `docs/Evaluation-Framework.md`.

Raters must:

1. score each dimension from 0–5;
2. write a short evidence-based justification;
3. distinguish missing evidence from negative evidence;
4. avoid inferring achievements not stated by the candidate; and
5. mark low-confidence ratings rather than forcing false precision.

Resolve disagreements above **two points on any dimension** through adjudication. Preserve both original ratings and the adjudicated result for analysis.

## Evaluation Metrics

Track metrics by dimension and answer category:

| Metric | Use |
|---|---|
| Mean absolute error | Average distance from the human score |
| Pearson/Spearman correlation | Score alignment and ranking quality |
| Weighted Cohen's kappa | Agreement for ordinal score bands |
| Exact / adjacent agreement | Percentage within 0 and 1 point |
| Zero-score precision | Ensures insufficient answers are not over-scored |
| High-score precision | Detects unsupported 4–5 ratings |
| Repeatability | Same-input consistency across runs |

Initial release targets:

- at least **80% adjacent agreement** overall;
- at least **70% adjacent agreement** on each dimension;
- zero-score precision of at least **95%** for deliberately insufficient answers;
- no dimension with mean absolute error above **1.0**; and
- no material evidence-hallucination findings in manual review.

These are release gates for the calibrated evaluator, not claims about the current MVP.

## Test and Release Process

1. Freeze a versioned evaluation prompt, rubric, and model configuration.
2. Split the dataset into calibration and holdout sets.
3. Run the evaluator without exposing human labels to the model.
4. Compare scores, justifications, and missing-evidence flags with human ratings.
5. Review disagreements by dimension and failure mode.
6. Update prompts or scoring rules and rerun the holdout set.
7. Record results in `docs/evidence/` with prompt/model versions.
8. Approve, reject, or limit the evaluator's release scope based on the thresholds.

Do not tune repeatedly against the holdout set. Any changes influenced by holdout results require a new holdout split.

## Human Feedback Loop

The product should eventually allow users or reviewers to mark feedback as **Helpful**, **Not Helpful**, or **Incorrect**. Store feedback with the evaluation version and use it to identify systematic issues.

User feedback must not silently rewrite historical scores. Corrections should be explicit, versioned, and auditable.

## Deliverables

- Versioned answer dataset (JSON or CSV)
- Human-rating guide and adjudication log
- Automated comparison script
- Calibration report with metrics and error analysis
- Updated evaluation prompt/rubric version
- Release decision and known limitations

## Product Decision Rule

Until calibration thresholds are met, position output as **AI-assisted practice feedback**, not an authoritative measure of interview ability. The UI should communicate low confidence when the answer contains insufficient evidence or the evaluator is uncertain.
