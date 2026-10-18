# M2.4 Coaching Quality Evidence

**Status:** Rewrite-safety implementation and live seed validation complete; release gate blocked
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
| Numeric rewrite safety | PASS — no unsupported numeric tokens in 10 stored rewrites |
| Semantic rewrite evidence integrity | REVIEW REQUIRED — deterministic numeric safety does not prove every paraphrase is fact-preserving |

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

The deterministic gate now removes unsupported numeric claims from rewrites. The live seed run produced zero numeric leakage across all ten examples. The gate does not prove that every non-numeric paraphrase is fact-preserving; examples such as `cal-001`, `cal-002`, and `cal-005` still require semantic review on the fresh holdout.

## Release decision

This milestone is complete as an implementation and seed-validation increment, but it is **not release-ready**. Numeric rewrite safety is enforced; the product must continue to be positioned as AI-assisted practice feedback until semantic review and the fresh human-rated holdout pass.

## Next action

Validate semantic rewrite integrity on a fresh holdout with two independent human raters before making calibrated coaching claims.
