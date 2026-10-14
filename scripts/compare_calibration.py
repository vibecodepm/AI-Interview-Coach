"""Compare AI evaluations with human ratings in the calibration dataset.

The script intentionally uses only the Python standard library so it can run
before the model-specific calibration tooling is selected.
"""

import json
import math
import sys
from pathlib import Path

DIMENSIONS = ("Relevance", "Structure", "Specificity", "Business Impact")


def mean_absolute_error(pairs):
    return sum(abs(ai - human) for ai, human in pairs) / len(pairs) if pairs else None


def adjacent_agreement(pairs):
    return sum(abs(ai - human) <= 1 for ai, human in pairs) / len(pairs) if pairs else None


def pearson(pairs):
    if len(pairs) < 2:
        return None
    ai_values = [ai for ai, _ in pairs]
    human_values = [human for _, human in pairs]
    ai_mean = sum(ai_values) / len(ai_values)
    human_mean = sum(human_values) / len(human_values)
    numerator = sum((ai - ai_mean) * (human - human_mean) for ai, human in pairs)
    ai_denominator = math.sqrt(sum((ai - ai_mean) ** 2 for ai in ai_values))
    human_denominator = math.sqrt(sum((human - human_mean) ** 2 for human in human_values))
    return numerator / (ai_denominator * human_denominator) if ai_denominator and human_denominator else None


def main(dataset_path):
    dataset = json.loads(Path(dataset_path).read_text())
    examples = dataset.get("examples", [])
    reports = {}
    rated_count = 0

    for dimension in DIMENSIONS:
        pairs = []
        for example in examples:
            human = (example.get("human_ratings") or {}).get(dimension)
            ai = (example.get("ai_evaluation") or {}).get(dimension)
            if human is not None and ai is not None:
                pairs.append((float(ai), float(human)))
        reports[dimension] = {
            "n": len(pairs),
            "mae": mean_absolute_error(pairs),
            "adjacent_agreement": adjacent_agreement(pairs),
            "pearson": pearson(pairs),
        }
        rated_count = max(rated_count, len(pairs))

    print(json.dumps({"dataset_id": dataset.get("dataset_id"), "rated_examples": rated_count, "dimensions": reports}, indent=2))
    if rated_count == 0:
        print("No paired human/AI ratings found; dataset is ready for human annotation.", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/calibration/answer-dataset.json")
