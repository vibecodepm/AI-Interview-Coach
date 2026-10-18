# M2.4 Coaching Quality Evidence

**Status:** Implementation complete; live-provider validation pending
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
| Live Ollama validation | PENDING — Ollama was not reachable at `localhost:11434` during this run |

## Release decision

This milestone is complete as a code and contract hardening increment, but it is **not** evidence of calibrated coaching quality. Before treating it as release-ready, run the live provider on a fresh holdout and review rewrite evidence integrity, especially for answers without quantified impact.

## Next action

Start Ollama with the pinned evaluation model, run the calibration/holdout workflow, and capture examples where the rewrite uses a placeholder instead of inventing an outcome. Keep the product positioned as AI-assisted practice feedback until that review is complete.
