# Human Evaluation Rating Guide

**Dataset:** `data/calibration/answer-dataset.json`  
**Rubric:** `docs/Evaluation-Framework.md`  
**Purpose:** Ensure human ratings are consistent enough to serve as a calibration reference.

## Rating Procedure

For every answer:

1. Read the question and answer without assuming facts not stated.
2. Score Relevance, Structure, Specificity, and Business Impact independently from 0–5.
3. Write one short justification per dimension, citing observable evidence.
4. Record confidence as high, medium, or low.
5. Flag fabricated, contradictory, ambiguous, or insufficient evidence.

Do not score writing polish, length, confidence of tone, or use of popular frameworks by themselves.

## Score Anchors

| Score | Meaning |
|---:|---|
| 0 | No usable evidence; empty, nonsensical, or non-responsive answer |
| 1 | Weak attempt with minimal relevant evidence |
| 2 | Developing answer with some relevance but important gaps |
| 3 | Competent answer with credible reasoning and some evidence |
| 4 | Strong answer with clear ownership, reasoning, and outcome |
| 5 | Exceptional answer with precise reasoning, trade-offs, evidence, and meaningful impact |

## Dimension Questions

### Relevance

Does the answer directly address what the question asked? Do not award relevance merely because the answer contains related keywords.

### Structure

Is there a coherent progression appropriate to the question? Frameworks are helpful but must not be applied mechanically when the question does not require one.

### Specificity

Can a reviewer identify what the candidate personally did, decided, measured, or changed? Look for actions, stakeholders, constraints, trade-offs, and timeframes.

### Business Impact

Does the answer provide a credible customer, business, operational, or measurable outcome? Never infer an outcome that the candidate did not provide.

## Adjudication

Two raters should score each example independently. If any dimension differs by more than two points, discuss that dimension and record an adjudicated score while preserving both original ratings.

The dataset is not ready for calibration claims until all examples have two independent ratings or a documented adjudication exception.
