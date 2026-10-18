"""Run the configured Ollama evaluator over the calibration dataset.

The script preserves human ratings and overwrites only AI evaluations. It must
be run on a machine where Ollama is reachable at OLLAMA_BASE_URL.
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "backend"))

from evaluation_system import (  # noqa: E402
    EVALUATION_PROMPT_VERSION,
    InterviewEvaluator,
    get_llm_client_by_config,
    insufficient_answer,
)


def serialize_evaluation(result, provider="ollama"):
    return {
        "provider": provider,
        "model": os.getenv("OLLAMA_MODEL", "llama3.1") if provider == "ollama" else None,
        "prompt_version": EVALUATION_PROMPT_VERSION,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "overall_score": result.overall_score,
        "detailed_scores": {
            item.dimension: item.score_per_dimension for item in result.detailed_scores
        },
        "justifications": {
            item.dimension: item.justification for item in result.detailed_scores
        },
        "feedback": {
            "strengths": result.feedback.strengths,
            "improvements": result.feedback.improvements,
        },
        "improved_answer_rewrite": result.improved_answer_rewrite,
        "confidence": result.confidence,
    }


def write_atomically(path, contents):
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(contents, handle, indent=2)
        handle.write("\n")
        temporary_path = Path(handle.name)
    temporary_path.replace(path)


def main():
    parser = argparse.ArgumentParser(description="Evaluate calibration examples with Ollama.")
    parser.add_argument(
        "dataset",
        nargs="?",
        type=Path,
        default=PROJECT_ROOT / "data" / "calibration" / "answer-dataset.json",
    )
    parser.add_argument("--limit", type=int, help="Evaluate only the first N examples.")
    parser.add_argument("--example-id", help="Evaluate one example ID (for resumable runs).")
    args = parser.parse_args()

    if os.getenv("LLM_PROVIDER", "ollama").lower() != "ollama":
        raise SystemExit("Set LLM_PROVIDER=ollama before running this script.")

    dataset = json.loads(args.dataset.read_text(encoding="utf-8"))
    examples = dataset.get("examples", [])
    if args.example_id:
        examples = [example for example in examples if example["id"] == args.example_id]
        if not examples:
            raise SystemExit(f"Unknown example ID: {args.example_id}")
    elif args.limit:
        examples = examples[: args.limit]
    evaluator = InterviewEvaluator(get_llm_client_by_config())

    for index, example in enumerate(examples, start=1):
        print(f"[{index}/{len(examples)}] Evaluating {example['id']}…", flush=True)
        result = evaluator.score_answer(
            question=example["question"],
            user_answer=example["answer"],
            resume_text="",
            jd_text="",
            target_role=example["target_role"],
        )
        provider = "deterministic_insufficient_answer_guard" if insufficient_answer(example["answer"]) else "ollama"
        example["ai_evaluation"] = serialize_evaluation(result, provider=provider)
        write_atomically(args.dataset, dataset)

    dataset["status"] = "awaiting_calibration_analysis"
    write_atomically(args.dataset, dataset)
    print(f"Saved {len(examples)} Ollama evaluations to {args.dataset}")


if __name__ == "__main__":
    main()
