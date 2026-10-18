"""Validate the calibrated-evaluator release gate for a holdout dataset.

The validator intentionally fails closed. A release dataset must contain at
least 50 examples, two independent rater maps, an adjudicated rating map, and
AI scores for every required dimension.
"""

import json
import sys
from pathlib import Path

DIMENSIONS = ("Relevance", "Structure", "Specificity", "Business Impact")
MIN_EXAMPLES = 50
MIN_ADJACENT_AGREEMENT = 0.70
MAX_MAE = 1.0


def metrics(pairs):
    if not pairs:
        return {"n": 0, "mae": None, "adjacent_agreement": None}
    return {
        "n": len(pairs),
        "mae": sum(abs(ai - human) for ai, human in pairs) / len(pairs),
        "adjacent_agreement": sum(abs(ai - human) <= 1 for ai, human in pairs) / len(pairs),
    }


def validate(dataset):
    examples = dataset.get("examples", [])
    failures = []
    if dataset.get("split") != "holdout":
        failures.append("dataset split must be 'holdout'")
    if len(examples) < MIN_EXAMPLES:
        failures.append(f"need at least {MIN_EXAMPLES} examples; found {len(examples)}")

    reports = {}
    for dimension in DIMENSIONS:
        pairs = []
        for example in examples:
            ratings = example.get("human_ratings") or {}
            rater_maps = ratings.get("raters") or {}
            adjudicated = (ratings.get("adjudicated") or {}).get(dimension)
            ai_score = (example.get("ai_evaluation", {}).get("detailed_scores") or {}).get(dimension)
            if len(rater_maps) < 2:
                continue
            if adjudicated is None or ai_score is None:
                continue
            pairs.append((float(ai_score), float(adjudicated)))
        report = metrics(pairs)
        reports[dimension] = report
        if report["n"] != len(examples):
            failures.append(f"{dimension}: every example needs two raters, adjudication, and AI score")
        elif report["mae"] > MAX_MAE:
            failures.append(f"{dimension}: MAE {report['mae']:.2f} exceeds {MAX_MAE:.2f}")
        elif report["adjacent_agreement"] < MIN_ADJACENT_AGREEMENT:
            failures.append(
                f"{dimension}: adjacent agreement {report['adjacent_agreement']:.0%} "
                f"is below {MIN_ADJACENT_AGREEMENT:.0%}"
            )

    return {"passed": not failures, "failures": failures, "dimensions": reports}


def main(path):
    dataset = json.loads(Path(path).read_text(encoding="utf-8"))
    result = validate(dataset)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "data/calibration/answer-dataset.json"))
