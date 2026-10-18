# M2.4 Coaching Quality Evidence

**Status:** Implementation and live-provider validation complete; release gate blocked
**Date:** 2026-10-18
**Prompt version:** `evaluation-v3`

## Change delivered

The answer-evaluation contract now explicitly requires evidence-grounded coaching:

- Dimension justifications must cite observable answer evidence or state that evidence is missing.
- Business Impact must distinguish an actual customer, business, operational, or measurable outcome from a process or decision.
- Feedback must be actionable and specific to the submitted answer.
- Better-answer rewrites must preserve the candidate's stated facts, actions, stakeholders, and outcomes.
- Missing metrics or outcomes must be represented with a bracketed prompt such as `[the missing metric or outcome]`; the evaluator must not invent them.

The runner now records `evaluation-v3` so future calibration outputs cannot be confused with the earlier prompt version.

## Verification

| Check | Result |
|---|---|
| Python compilation | PASS |
| Existing contract tests | PASS — 3 tests |
| Coaching prompt contract test | PASS |
| Live Ollama validation | PASS — 10 examples evaluated with `gemma4:latest` |
| Rewrite persistence | PASS — all non-insufficient examples stored a rewrite |
| Rewrite evidence integrity | FAIL — manual review found unsupported causal/context additions |

## Live seed results

The updated `evaluation-v3` prompt was run against the existing 10-example seed set:

| Dimension | MAE | Adjacent agreement |
|---|---:|---:|
| Relevance | 0.90 | 100% |
| Structure | 0.20 | 100% |
| Specificity | 0.70 | 100% |
| Business Impact | 1.60 | 40% |

These are seed-baseline diagnostics, not a fresh holdout or a calibration release claim.

## Coaching finding

The model follows the placeholder instruction in some cases, especially for clearly generic answers such as `cal-007`, `cal-009`, and `cal-010`. However, it still paraphrases or adds unsupported context in other rewrites. Examples include inferring that a custom build would divert resources in `cal-001`, adding ownership and post-launch process details in `cal-002`, and asserting risk analysis or trade-offs not stated in `cal-005`.

## Release decision

This milestone is complete as an implementation and validation increment, but it is **not release-ready**. The live run confirms that prompt instructions alone do not guarantee evidence-preserving rewrites. The product must continue to be positioned as AI-assisted practice feedback.

## Next action

Add a deterministic rewrite-safety gate or a separate review-required state, then validate it on a fresh holdout with two independent human raters before making calibrated coaching claims.
