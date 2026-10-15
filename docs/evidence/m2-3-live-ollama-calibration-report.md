# M2.3 Calibration — Live Ollama Seed Baseline

**Date:** 2026-10-15  
**Dataset:** `data/calibration/answer-dataset.json` (10 examples)  
**Model:** `gemma4:latest` via Ollama  
**Prompt:** `evaluation-v2`  
**Decision:** Do not release as a calibrated evaluator.

## Method

Human dimension ratings were compared with one live evaluation per example. The insufficient-answer guard produced the `cal-008` zero score deterministically; all other examples were scored by the configured Ollama model. The frozen `evaluation-v2` prompt requires a 0–5 scale, evidence-grounded feedback, and no inferred outcomes.

## Results

| Dimension | Examples | MAE | Adjacent agreement | Pearson correlation |
|---|---:|---:|---:|---:|
| Relevance | 10 | 0.90 | 100% | 0.99 |
| Structure | 10 | 0.35 | 100% | 0.96 |
| Specificity | 10 | 0.35 | 100% | 0.96 |
| Business Impact | 10 | 1.70 | 40% | 0.15 |
| Overall score | 10 | 0.44 | 100% | — |

## Interpretation

- The model meets the seed baseline thresholds for Relevance, Structure, and Specificity.
- It fails the Business Impact gate (target: MAE no greater than 1.0 and at least 70% adjacent agreement). The model still awards positive impact scores when human review identifies no demonstrated outcome.
- `cal-008` confirms the zero-score guard works for an insufficient answer. This one case is not enough to establish the plan’s 95% zero-score precision target.

## Release Decision and Next Work

Keep the product positioned as **AI-assisted practice feedback**, not an authoritative or calibrated interview score. M2.3 is complete as a seed-baseline milestone, but calibration release remains blocked until the following are completed:

1. Add a Business Impact-specific scoring constraint and retest against a new, untouched holdout set.
2. Expand to the planned 50–100 examples with category coverage and deliberately insufficient answers.
3. Obtain two independent human ratings per example and preserve adjudication records.
4. Re-run the release gates with a fixed prompt, model, and configuration.
