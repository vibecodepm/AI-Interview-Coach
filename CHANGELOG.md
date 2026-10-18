## M2.4 - Coaching Quality

### Added
- Evidence-grounded coaching constraints for feedback and improved-answer rewrites.
- Explicit placeholders for missing metrics or outcomes.
- Live `evaluation-v3` seed validation and persisted rewrite evidence.

### Status
- Implementation and seed validation complete; release remains blocked by rewrite-integrity findings and fresh-holdout requirements.

## M2.3 - Calibration Baseline

### Added
- Ten-example human-rated seed dataset and live Ollama comparison tooling.
- Per-dimension MAE and adjacent-agreement reporting.

### Status
- Diagnostic baseline only; not a calibrated release.

## v0.1.0 - Foundation

### Added
- Next.js frontend scaffold
- FastAPI backend scaffold
- Health endpoint
- Mock interview endpoints

### Status
- Frontend and backend independently operational.


## v0.2.0 - Interactive MVP

### Added
- Connected frontend to FastAPI interview endpoint
- Loading and error states
- First interview question rendered dynamically

## v0.3.0 - Contract Hardening

### Added
- Explicit FastAPI request and response contracts
- Stable question identifiers
- Structured evaluation confidence and feedback fields
- Insufficient-answer guardrail returning a zero score
- Contract tests for question generation and answer evaluation
- Verified frontend production build and API smoke tests

### Status
- M2.1 contract hardening complete.
- Next milestone: live provider validation.
