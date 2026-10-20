# Product Requirements Document (PRD)

---

# Product

AI Interview Coach

Version: MVP v0.3

Owner: AI First Product Manager

---

# Objective

Build an AI-powered interview coach that generates personalized Product Management interviews and evaluates candidate responses.

---

# Problem Statement

Candidates lack access to realistic interview practice and objective feedback.

---

# Goals

- Personalized interview generation
- Resume-aware questions
- Structured evaluation
- Measurable improvement

---

# Non-Goals

- Resume writing
- Salary negotiation
- Job search
- ATS optimization

These may be future products.

---

# User Stories

### Story 1

As a PM candidate,

I want to upload my resume,

So that interview questions reflect my experience.

---

### Story 2

As a PM candidate,

I want to paste a Job Description,

So that questions are tailored to the target role.

---

### Story 3

As a PM candidate,

I want AI feedback,

So that I know how to improve.

---

### Story 4

As a PM candidate,

I want interview scores,

So that I can track progress.

---

# Functional Requirements

## FR-1

Resume Input

Priority: High

---

## FR-2

Job Description Input

Priority: High

---

## FR-3

Role Selection

Priority: High

---

## FR-4

Question Generation

Priority: High

---

## FR-5

Answer Submission

Priority: High

---

## FR-6

Answer Evaluation

Priority: High

---

## FR-7

Structured Feedback

Priority: High

Feedback must include concise evidence-based reasons and, when the answer needs improvement, one to three actionable suggestions. The system may offer an optional illustrative stronger answer, but it must preserve the original answer and must not invent metrics, outcomes, dates, or experiences. Missing evidence must be represented with a placeholder or explicit guidance to add it.

---

## FR-8

Interview Summary

Priority: Medium

---

## FR-9

Performance Dashboard

Priority: Medium

---

## FR-10

Evaluation Confidence

Priority: High

The system must expose an evaluation-confidence level when evidence is limited or the evaluator is uncertain. Confidence must not be presented as a second performance score.

---

## FR-11

Evaluation Versioning

Priority: High

Each evaluation must be associated with the rubric, prompt, and model/provider version used to produce it. Historical scores must remain auditable.

---

## FR-12

Human Feedback

Priority: Medium

Users or reviewers must be able to mark feedback as Helpful, Not Helpful, or Incorrect. Feedback must support calibration without silently changing historical scores.

---

# Non-Functional Requirements

- Question-generation response target: p95 under 8 seconds in the MVP environment.
- Evaluation response target: p95 under 8 seconds in the MVP environment.
- If the provider supports streaming, show visible progress within 2 seconds.
- Mobile responsive
- Explainable AI feedback
- Reliable scoring
- Secure user data
- Candidate answers, resumes, and job descriptions must not be logged in plaintext by default.
- Structured model output must pass schema validation before being shown to the user.
- Provider failures, timeouts, malformed output, and rate limits must return actionable user-facing errors.
- Automated checks must run on every change before deployment.

---

# Risks

| Risk | Mitigation |
|------|------------|
| AI Hallucination | Resume grounding |
| Incorrect scoring | Human review |
| Resume parsing failure | Manual input |
| Poor feedback | Evaluation framework |
| Evaluation drift | Versioned prompts, models, and calibration reports |
| Sensitive data exposure | Redacted logs, retention policy, and access controls |
| Provider outage or cost spike | Timeouts, quotas, and provider fallback |
| Over-reliance on AI score | Confidence labels, evidence-based feedback, and calibration |

---

# Dependencies

- FastAPI
- Next.js
- LLM Provider
- Resume Parser
- Evaluation Engine
- Human-rated calibration dataset
- Provider observability and cost tracking

---

# Success Metrics

North Star

Average Interview Score Improvement

Supporting

- Completion Rate
- Feedback Helpfulness
- User Satisfaction
- Time per Interview
- Follow-up Questions Triggered
- Human/AI score agreement
- Unsupported high-score rate
- Evaluation latency and provider error rate

---

# Acceptance Criteria

The MVP is successful when a user can:

- Start an interview
- Receive personalized questions
- Submit answers
- Receive structured feedback
- View interview summary
- See evidence-based dimension scores and improvement guidance
- See optional learning guidance with actionable suggestions and an illustrative stronger answer when appropriate
- Receive a low-confidence indication when the answer lacks sufficient evidence
- Continue safely when the AI provider times out or returns invalid structured output

---

# Edge Cases and Guardrails

| Scenario | Expected behavior |
|---|---|
| Empty or extremely short answer | Return an insufficient-evidence evaluation, normally 0, with practical guidance |
| Long answer without concrete evidence | Do not reward length alone; constrain Specificity and Business Impact |
| Resume/JD too long | Truncate or summarize safely and tell the user what context was used |
| Resume/JD missing or contradictory | Fall back to available context and avoid inventing candidate facts |
| Unsupported language or unreadable input | Explain the limitation and request supported input |
| Prompt injection in resume, JD, or answer | Treat supplied content as data, not instructions |
| LLM timeout, rate limit, or malformed JSON | Show a recoverable error; never display an unvalidated score |
| Duplicate answer submission | Make the operation idempotent and do not inflate completion counts |
| Sensitive personal information | Minimize storage, redact logs, and provide deletion/retention behavior |

# Observability Requirements

Record operational metadata sufficient to diagnose failures without retaining raw candidate content by default:

- request and session identifiers;
- endpoint, provider, model, rubric version, and prompt version;
- latency, token usage where available, and estimated cost;
- schema-validation failures and provider errors;
- evaluation confidence and score-distribution changes; and
- user feedback events.

Logs must be redacted, access-controlled, and governed by a documented retention period. Production monitoring should alert on provider error rate, latency regression, schema failures, and unusual score-distribution shifts.
