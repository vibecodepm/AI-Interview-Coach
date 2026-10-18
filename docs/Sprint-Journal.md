# Sprint Journal

This document records every sprint completed during the development of AI Interview Coach.

---

# Sprint 1

## Goal

Build the project foundation.

### Completed

- GitHub Repository
- Next.js setup
- FastAPI setup
- Project structure

### Learnings

Starting with a clean architecture significantly reduces technical debt.

---

# Sprint 2

## Goal

Connect frontend and backend.

### Completed

- Interview API
- Mock interview generation
- Initial UI

### Challenges

API integration.

---

# Sprint 3

## Goal

Improve engineering quality.

### Completed

- Environment variables
- Service layer
- Better project organization

### Learnings

Separating networking logic from UI improves maintainability.

---

# Sprint 4

## Goal

Resolve runtime issues.

### Issues Found

- JavaScript syntax error
- Python import issue
- CORS failure

### Resolution

- Fixed imports
- Added CORS middleware
- Verified end-to-end communication

### Learnings

Runtime validation is as important as code generation.

---

# Sprint 5

## Goal

Complete the MVP vertical slice.

### Completed

- Resume input
- JD input
- Role selection
- Backend communication
- Question rendering

### Milestone

First successful end-to-end product flow.

---

# Sprint 6

## Goal

Product documentation.

### Completed

- README
- Product Vision
- PRD
- User Personas
- AI Workflow
- Roadmap
- Metrics

### Outcome

Repository transformed into a Product Management portfolio project.

---

# Sprint 7 — Evaluation foundation and contract hardening

### Completed

- Stable question and answer contracts
- Insufficient-answer zero-score guardrail
- Structured confidence, feedback, and dimension scores
- Contract tests, API smoke tests, and frontend build verification

### Evidence

- M2.1 contract-hardening report
- Commit `fa51372`

# Sprint 8 — Live provider path

### Completed

- Ollama provider integration with JSON-schema validation
- Provider timeout and failure handling
- End-to-end browser flow validation

### Decision

The live path works, but local answer-evaluation latency remains above the target. The product should not be positioned as production-grade solely on provider connectivity.

### Evidence

- M2.2 live-provider report
- Commit `4300d15`

# Sprint 9 — Calibration baseline

### Completed

- Ten-example PM calibration seed dataset
- Human-rating structure and comparison tooling
- Live `gemma4:latest` baseline with per-dimension MAE and adjacent-agreement reporting

### Decision

The seed baseline is diagnostic only. Business Impact agreement is insufficient for calibrated scoring, and the dataset does not yet meet the 50–100-example, two-rater holdout requirement.

### Evidence

- M2.3 live calibration report
- Commit `8ef3338`

# Sprint 10 — Evidence-grounded coaching

### Completed

- `evaluation-v3` coaching constraints
- Explicit prohibition on invented metrics, outcomes, dates, and business results
- Bracketed placeholders for missing evidence
- Persisted improved-answer rewrites in calibration artifacts
- Live validation of the updated prompt against the seed set

### Decision

The implementation is complete, but live review found unsupported contextual additions in several rewrites. A deterministic rewrite-safety gate and fresh holdout review are required before release.

### Evidence

- M2.4 coaching-quality report
- Commits `15b89a6` and `e7332cf`

# Upcoming Sprints

Sprint 11

- Deterministic numeric rewrite-safety gate — complete
- Fresh holdout set with two independent human raters
- Adjudication and release-gate decision

Sprint 12

- Resume/JD personalization only after evaluation reliability is acceptable

Later

- Voice interviews
- Analytics dashboard
- User testing at broader scale
- Production deployment
