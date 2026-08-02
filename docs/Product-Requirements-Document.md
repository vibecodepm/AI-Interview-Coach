# Product Requirements Document (PRD)

---

# Product

AI Interview Coach

Version: MVP v0.2

Owner: 

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

---

## FR-8

Interview Summary

Priority: Medium

---

## FR-9

Performance Dashboard

Priority: Medium

---

# Non-Functional Requirements

- Response time < 3 seconds
- Mobile responsive
- Explainable AI feedback
- Reliable scoring
- Secure user data

---

# Risks

| Risk | Mitigation |
|------|------------|
| AI Hallucination | Resume grounding |
| Incorrect scoring | Human review |
| Resume parsing failure | Manual input |
| Poor feedback | Evaluation framework |

---

# Dependencies

- FastAPI
- Next.js
- LLM Provider
- Resume Parser
- Evaluation Engine

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

---

# Acceptance Criteria

The MVP is successful when a user can:

- Start an interview
- Receive personalized questions
- Submit answers
- Receive structured feedback
- View interview summary