# AI Interview Coach — Evaluation Framework

## 1. Purpose

The AI Interview Coach evaluates a candidate's interview response using a transparent, repeatable rubric.

The goal is not to reward polished language or generic positivity. The evaluator should assess whether the candidate provides sufficient evidence to demonstrate:

- relevance to the question
- clear reasoning and structure
- specific personal actions and evidence
- measurable business or customer impact

The evaluation is designed to provide a score that a candidate can understand and act on.

---

## 2. Evaluation Dimensions

The MVP evaluates every answer across four dimensions.

| Dimension | What it measures |
|---|---|
| Relevance | Whether the response directly answers the interview question and uses relevant context |
| Structure | Whether the response has a coherent decision/story flow and follows the requested framework where applicable |
| Specificity | Whether the candidate explains what they personally did, why they did it, and provides concrete evidence |
| Business Impact | Whether the response demonstrates a credible customer, business, operational, or measurable outcome |

Each dimension is scored from **0 to 5**.

The overall answer score is the average of the four dimension scores.

```text
Answer Score =
(Relevance + Structure + Specificity + Business Impact) / 4
```

The final displayed score is rounded to one decimal place.

---

## 3. Score Interpretation

### 0 — Insufficient Evidence

Use when the response is empty, extremely short, irrelevant, or provides no meaningful evidence to evaluate.

Examples:

```text
"abc"
"yes"
"not sure"
```

A response at this level must **not receive artificial positive credit** simply because it contains words related to the question.

---

### 1 — Weak

The candidate attempts to answer but provides very limited evidence.

Typical characteristics:

- generic statements
- little or no personal ownership
- unclear reasoning
- no meaningful outcome

---

### 2 — Developing

The answer is relevant enough to evaluate but remains incomplete.

Typical characteristics:

- some context
- basic decision or action
- limited specificity
- weak or missing measurable outcome

---

### 3 — Competent

The candidate provides a credible interview answer.

Typical characteristics:

- clear relevance
- recognizable structure
- personal actions are present
- some supporting evidence
- outcome is reasonably explained

---

### 4 — Strong

The response demonstrates strong product or leadership thinking.

Typical characteristics:

- directly answers the question
- clear decision-making process
- strong personal ownership
- concrete evidence and metrics
- credible business/customer impact

---

### 5 — Exceptional

The response is highly interview-ready.

Typical characteristics:

- precise and directly relevant
- excellent structure
- strong reasoning and trade-offs
- clear personal ownership
- quantified or otherwise compelling evidence
- meaningful business/customer impact
- concise without losing important context

---

# 4. Dimension Rubrics

## Relevance

### 0
The answer does not meaningfully address the question.

### 1
The answer is mostly unrelated or consists of generic statements.

### 2
The answer has some connection to the question but the connection is weak.

### 3
The answer addresses the question with generally relevant context.

### 4
The answer directly addresses the question and demonstrates relevant decision-making.

### 5
The answer directly and precisely addresses the question with highly relevant context and reasoning.

---

## Structure

Structure depends on the question type and any framework explicitly requested.

### Behavioral Questions

Expected structure may include:

```text
Situation
→ Task
→ Action
→ Result
```

### Product Questions

Expected structure may include:

```text
Problem
→ Diagnosis
→ Options / Trade-offs
→ Decision
→ Execution
→ Impact
```

### Strategy / Metrics Questions

Expected structure may include:

```text
Metric
→ Diagnosis
→ Intervention
→ Expected Impact
→ Risks / Trade-offs
```

The evaluator should not require a framework mechanically when the question does not call for one.

---

## Specificity

Strong responses should make the candidate's contribution observable.

Look for:

- specific actions
- decisions
- stakeholders
- trade-offs
- metrics
- timeframes
- examples
- experiments
- constraints

Weak responses often rely on phrases such as:

```text
"I worked with the team."
"We improved the product."
"We launched a feature."
"We changed the roadmap."
```

These statements can be relevant but do not establish sufficient personal ownership or evidence on their own.

---

## Business Impact

Evaluate the outcome demonstrated by the candidate.

Possible evidence includes:

- revenue
- conversion
- acquisition
- retention
- engagement
- customer experience
- cost reduction
- operational efficiency
- risk reduction
- adoption
- quality
- delivery speed

A strong score requires an actual outcome or credible evidence of impact.

Do not invent impact that the candidate did not provide.

---

# 5. Evidence Integrity Rules

The evaluator must follow these principles.

### Rule 1 — Do not invent achievements

If the candidate did not provide a metric, the evaluator must not create one.

Bad:

> "This resulted in a 20% improvement."

when the candidate never mentioned 20%.

Good:

> "The response does not provide a measurable outcome."

---

### Rule 2 — Do not reward length by itself

A 1,000-character response is not automatically better than a 100-character response.

Score evidence quality, not word count.

---

### Rule 3 — Do not reward generic confidence

Statements such as:

> "I successfully led the team."

should not receive high Specificity or Business Impact scores without supporting evidence.

---

### Rule 4 — Very short answers must be scoreable

A response such as:

```text
"abc"
```

should result in a **0-level evaluation**, with feedback explaining that there is insufficient evidence.

This behavior was explicitly tested in the MVP.

---

### Rule 5 — Stay grounded in the candidate's answer

The evaluator may use the supplied resume, job description, role context, question and requested framework to assess relevance.

It must not use those inputs to manufacture achievements that are absent from the candidate's response.

---

# 6. Feedback Generation

Every evaluation should provide:

1. Overall score
2. Score for each dimension
3. Short evidence-based justification
4. Practical improvement guidance

Example:

```text
Overall: 2.5 / 5

Relevance: 3.3 / 5
The response is related to the question, but the connection could be more explicit.

Structure: 3.7 / 5
A coherent story is present, but the requested framework could be made more explicit.

Specificity: 2.6 / 5
Add stakeholder detail and quantitative evidence.

Business Impact: 2.5 / 5
Add a concrete outcome and quantify the business or customer impact where possible.
```

---

# 7. Interview-Level Aggregation

The interview contains multiple questions.

Only **completed/evaluated questions** should contribute to the interview summary.

```text
Interview Score =
Average of unique completed question scores
```

A question must not be counted twice.

Example:

```text
Question 1 = 0.0
Question 2 = 2.5
Question 3 = 4.3

Overall =
(0.0 + 2.5 + 4.3) / 3
= 2.3 / 5
```

The UI should display:

```text
3 of 3 questions completed
```

rather than counting multiple evaluation events for the same question.

---

# 8. Confidence

The evaluation model may expose an evaluation-confidence level:

- **High**
- **Medium**
- **Low**

When confidence is low, the product should make the limitation visible:

> This evaluation may be less reliable.

Confidence should reflect evidence quality and evaluation certainty, not be used as another performance score.

---

# 9. Known Failure Modes

## Hallucinated Evidence

### Risk
The evaluator assumes achievements or metrics that the candidate did not state.

### Mitigation
Ground evaluation in the candidate's actual response and explicitly distinguish missing evidence from inferred context.

---

## False Praise

### Risk
Weak answers receive overly generous scores.

### Mitigation
Use explicit 0–5 anchors and insufficient-evidence handling.

---

## Overly Harsh Evaluation

### Risk
A strong answer receives an unnecessarily low score because the evaluator expects a single rigid framework.

### Mitigation
Evaluate the quality of reasoning and evidence first. Treat frameworks as guidance rather than keyword checklists.

---

## Score Inflation

### Risk
Long answers or answers containing many business terms receive high scores without proving impact.

### Mitigation
Require evidence for high Specificity and Business Impact scores.

---

## Duplicate Interview Scores

### Risk
Repeated submission or state updates cause the same question to be counted more than once in the final interview score.

### Mitigation
Aggregate using unique question identity/index rather than raw evaluation-event count.

---

# 10. Human Review

The product is designed to support future evaluation calibration through human feedback.

Users may classify feedback as:

- Helpful
- Not Helpful
- Incorrect

This feedback can later be used to:

- identify systematic scoring errors
- improve prompts
- calibrate score boundaries
- create an evaluation dataset
- compare model versions

Human feedback should not silently change a candidate's historical score without an explicit product decision.

---

# 11. MVP Validation

The evaluation system was tested with responses of different quality levels.

Observed behavior included:

| Test | Response quality | Observed score |
|---|---|---:|
| Test 1 | Extremely short / insufficient evidence | 0.0 |
| Test 2 | Relevant but generic and incomplete | 2.2–2.5 |
| Test 3 | Strong structured answer with evidence | 4.3–4.4 |
| Test 4 | Strong answer with business context and measurable outcome | ~4.3 |

These tests demonstrated an important MVP requirement:

> **The system must distinguish between insufficient, developing and strong answers rather than returning a uniformly positive score.**

---

# 12. Product Principle

The evaluation engine should answer one core question:

> **"What evidence did the candidate provide that would make an interviewer believe they can perform at this level?"**

The product should optimize for **evidence-based coaching**, not for making the candidate feel good.

That distinction is central to the AI Interview Coach product.
