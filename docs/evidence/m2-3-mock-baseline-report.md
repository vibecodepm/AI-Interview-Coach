# M2.3 Calibration — Mock Baseline

**Date:** 2026-10-15  
**Dataset:** `data/calibration/answer-dataset.json`  
**Evaluator:** `MockLLMClient` (deterministic test double)  
**Decision:** Not eligible for a calibration release.

## Scope

Ten seed examples received dimension-level human ratings. The mock evaluator was then compared with those ratings using `scripts/compare_calibration.py`.

## Results

| Dimension | Examples | MAE | Adjacent agreement | Pearson correlation |
|---|---:|---:|---:|---:|
| Relevance | 10 | 0.40 | 80% | 0.80 |
| Structure | 10 | 0.80 | 90% | 0.71 |
| Specificity | 10 | 1.15 | 70% | 0.62 |
| Business Impact | 10 | 3.10 | 10% | 0.25 |

## Findings

- The insufficient-answer guard correctly returned zero scores for `cal-008` (`"abc"`).
- The mock evaluator returned the same non-zero dimension scores for every other answer. It therefore over-scored generic answers and answers without demonstrated impact.
- Business Impact is the critical failure: the mock assigned `4.0` where human reviewers assigned `0.0–2.0` for answers without a measurable or credible outcome.

## Release Decision

Do not position scores from the mock evaluator as calibrated coaching signals. It remains appropriate for local development and API-contract tests only.

## Next Required Run

Run the exact same frozen dataset against a live Ollama model, then rerun the comparison:

```bash
cd "/Users/maccook/Desktop/Hermes Projects/AI-Interview-Coach"
LLM_PROVIDER=ollama OLLAMA_MODEL=<installed-model> \
  venv/bin/python scripts/run_ollama_calibration.py
venv/bin/python scripts/compare_calibration.py data/calibration/answer-dataset.json
```

The live run overwrites only `ai_evaluation`; the human ratings remain intact. Review the resulting agreement before any prompt changes. This dataset is a 10-example seed baseline, not the 50–100-example release-calibration set specified in the plan.
