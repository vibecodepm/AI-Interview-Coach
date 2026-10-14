# M2.2 Live Provider Path — Verification Report

**Date:** October 15, 2026  
**Status:** Passed with performance limitation  
**Provider:** Ollama  
**Model:** `gemma4:latest`

## Verification Results

| Check | Result | Evidence |
|---|---|---|
| Ollama installation | PASS | Local Ollama binary available |
| Model availability | PASS | `gemma4:latest` listed locally |
| Provider adapter reachability | PASS | Ollama `/api/generate` responded successfully |
| Question generation | PASS | Live model returned three schema-valid questions with IDs and follow-ups |
| Answer evaluation | PASS | Live model returned a schema-valid score report |
| Dimension contract | PASS | Returned exactly Relevance, Structure, Specificity, and Business Impact |
| Structured output enforcement | PASS | Ollama JSON-schema format plus Pydantic validation enabled |
| Provider timeout configuration | PASS | `OLLAMA_TIMEOUT_SECONDS` is configurable; local default is 90 seconds |

## Contract Confirmed

The live provider returns the same shapes consumed by the frontend:

- question objects contain `question_id`, `question_text`, `suggested_framework`, and `follow_up_prompt`;
- evaluation objects contain `overall_score`, four approved `detailed_scores`, `feedback`, `improved_answer_rewrite`, and `confidence`.

## Performance Finding

The local `gemma4:latest` model can take longer than the product target for answer evaluation. The initial 30-second timeout caused a provider failure; the timeout is now configurable and was increased to 90 seconds for local validation.

This means the provider path is functionally validated but is **not yet within the target p95 response time**. Before production use, the team should evaluate a smaller/faster model, response streaming, prompt reduction, or asynchronous evaluation UX.

## Configuration

Supported environment variables:

```text
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma4:latest
OLLAMA_TIMEOUT_SECONDS=90
```

`OLLAMA_API_URL` is also supported for callers that provide the complete `/api/generate` URL.

## Next Milestone

**M2.3 — Evaluation calibration:** compare live-model scores with a human-rated PM answer dataset and measure agreement, error, and evidence integrity.
