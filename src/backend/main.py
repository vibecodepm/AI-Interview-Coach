"""
AI Interview Coach MVP backend.

MVP goals:
1. Credible, evidence-based scoring instead of a fixed/mock score.
2. One question at a time via the existing 3-question start contract.
3. Per-answer evaluation that is transparent and deterministic.
4. End-of-interview summary endpoint for the next frontend step.
5. Backward-compatible response fields used by the current UI.

Run:
    uvicorn src.backend.main:app --reload --port 8000
"""

from __future__ import annotations

import re
from statistics import mean
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="AI Interview Coach MVP",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

class StartInterviewRequest(BaseModel):
    resume_text: str = ""
    job_description: str = ""
    target_role: str = ""


class SubmitAnswerRequest(BaseModel):
    question_id: Optional[int] = None
    question_text: Optional[str] = None
    suggested_framework: Optional[str] = None
    user_answer: str = ""
    # Accept these aliases as well so the backend remains tolerant of the
    # current frontend payload.
    answer: Optional[str] = None
    target_role: Optional[str] = None


# ---------------------------------------------------------------------------
# Deterministic MVP question set
# ---------------------------------------------------------------------------

QUESTIONS = [
    {
        "question_id": 1,
        "question_text": (
            "Describe a time your prioritization changed due to external "
            "market factors. (STAR required)"
        ),
        "title": (
            "Describe a time your prioritization changed due to external "
            "market factors. (STAR required)"
        ),
        "rawText": (
            "Describe a time your prioritization changed due to external "
            "market factors. (STAR required)"
        ),
        "suggested_framework": "STAR with an external pivot variable",
        "follow_up_prompt": [
            "What is the change cost?",
            "How was stakeholder buy-in maintained?",
            "Did you need to de-prioritize X?",
        ],
    },
    {
        "question_id": 2,
        "question_text": (
            "Walk us through a product failure and what systemic process "
            "changes protected the organization later."
        ),
        "title": (
            "Walk us through a product failure and what systemic process "
            "changes protected the organization later."
        ),
        "rawText": (
            "Walk us through a product failure and what systemic process "
            "changes protected the organization later."
        ),
        "suggested_framework": "STAR with root-cause and learning",
        "follow_up_prompt": [
            "What was the quantitative loss?",
            "How difficult was root cause analysis?",
            "Did you integrate new monitoring tools?",
        ],
    },
    {
        "question_id": 3,
        "question_text": (
            "If given full ownership of our Digital Wallet, what is ONE "
            "metric you would move immediately and why?"
        ),
        "title": (
            "If given full ownership of our Digital Wallet, what is ONE "
            "metric you would move immediately and why?"
        ),
        "rawText": (
            "If given full ownership of our Digital Wallet, what is ONE "
            "metric you would move immediately and why?"
        ),
        "suggested_framework": "Metric → diagnosis → intervention → impact",
        "follow_up_prompt": [
            "Can you model the impact vs. current state?",
            "Who benefits the most from this change in metrics?",
            "What secondary risks are introduced by prioritizing this metric?",
        ],
    },
]


# In-memory MVP state. This is deliberately simple for a recruiter-demo MVP.
SESSIONS: Dict[str, Dict[str, Any]] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def has_any(text: str, phrases: List[str]) -> bool:
    lowered = text.lower()
    return any(p in lowered for p in phrases)


def clamp(value: float, low: float = 0.0, high: float = 5.0) -> float:
    return round(max(low, min(high, value)), 1)


def score_insufficient_answer(answer: str) -> Optional[Dict[str, Any]]:
    """
    Hard quality gate.

    A short/nonsense answer must never receive a high score merely because it
    happens to contain a keyword.
    """
    text = clean_text(answer)
    words = word_count(text)

    if not text or words < 5:
        return {
            "overall_score": 0.0,
            "detailed_scores": [
                {
                    "dimension": "Relevance",
                    "score_per_dimension": 0.0,
                    "justification": "The answer is too short to demonstrate relevance.",
                },
                {
                    "dimension": "Structure",
                    "score_per_dimension": 0.0,
                    "justification": "There is not enough content to establish a coherent response.",
                },
                {
                    "dimension": "Specificity",
                    "score_per_dimension": 0.0,
                    "justification": "The response contains insufficient evidence or personal actions.",
                },
                {
                    "dimension": "Business Impact",
                    "score_per_dimension": 0.0,
                    "justification": "No outcome or business/customer impact is demonstrated.",
                },
            ],
            "feedback": {
                "strengths": [],
                "improvements": [
                    "Provide a complete example rather than a fragment.",
                    "Explain what you personally did and why.",
                    "Include a concrete result or measurable outcome.",
                ],
            },
        }

    return None


def evaluate_answer(
    answer: str,
    question_text: str = "",
    framework: str = "",
) -> Dict[str, Any]:
    """
    Transparent heuristic rubric for the MVP.

    This is intentionally NOT a fake LLM score. Each dimension is based on
    observable evidence in the candidate's response.
    """
    answer = clean_text(answer)
    question_text = clean_text(question_text)
    framework = clean_text(framework)

    insufficient = score_insufficient_answer(answer)
    if insufficient:
        return insufficient

    lower = answer.lower()
    words = word_count(answer)

    # Evidence signals ------------------------------------------------------
    context = has_any(
        lower,
        [
            "previous company", "previous role", "at my", "when",
            "competitor", "market", "customer", "launch", "roadmap",
            "product", "team", "company",
        ],
    )

    ownership = has_any(
        lower,
        [
            "i ", "i'm", "i am", "i worked", "i analyzed", "i proposed",
            "i decided", "i led", "i owned", "i drove", "i worked with",
            "i quantified", "i negotiated", "i recommended",
        ],
    )

    reasoning = has_any(
        lower,
        [
            "because", "so that", "based on", "trade-off", "tradeoff",
            "risk", "impact", "analyzed", "evaluated", "compared",
            "prioritized", "de-prioritized", "deprioritized",
        ],
    )

    stakeholder = has_any(
        lower,
        [
            "stakeholder", "leadership", "engineering", "marketing",
            "sales", "finance", "executive", "customer", "cross-functional",
            "buy-in", "buy in", "aligned",
        ],
    )

    outcome = has_any(
        lower,
        [
            "increased", "decreased", "improved", "reduced", "grew",
            "saved", "launched", "delivered", "conversion", "revenue",
            "retention", "adoption", "six weeks", "weeks earlier",
            "%",
        ],
    )

    metric = bool(re.search(r"\b\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\s*(?:m|k|million|thousand)\b", lower))

    learning = has_any(
        lower,
        [
            "learned", "learning", "next time", "changed our process",
            "systemic", "monitoring", "root cause", "prevent",
            "would do differently",
        ],
    )

    # Relevance -------------------------------------------------------------
    relevance = 2.5
    if context:
        relevance += 0.5
    if reasoning:
        relevance += 0.5
    if the_question_is_directly_answered(answer, question_text):
        relevance += 0.7
    if ownership:
        relevance += 0.3
    relevance = clamp(relevance)

    # Structure -------------------------------------------------------------
    structure = 2.0
    if words >= 60:
        structure += 0.5
    if context:
        structure += 0.4
    if ownership:
        structure += 0.5
    if reasoning:
        structure += 0.4
    if outcome:
        structure += 0.4
    if framework and ("STAR" in framework.upper()) and (
        context and ownership and outcome
    ):
        structure += 0.4
    structure = clamp(structure)

    # Specificity -----------------------------------------------------------
    specificity = 2.0
    if words >= 60:
        specificity += 0.4
    if words >= 120:
        specificity += 0.3
    if ownership:
        specificity += 0.6
    if reasoning:
        specificity += 0.4
    if stakeholder:
        specificity += 0.3
    if metric:
        specificity += 0.4
    specificity = clamp(specificity)

    # Business impact -------------------------------------------------------
    impact = 1.5
    if outcome:
        impact += 1.0
    if metric:
        impact += 1.0
    if reasoning:
        impact += 0.4
    if stakeholder:
        impact += 0.2
    if learning:
        impact += 0.3
    impact = clamp(impact)

    # Strong-answer calibration --------------------------------------------
    # A complete answer with context + ownership + reasoning + outcome and
    # quantitative evidence should land in the interview-ready range.
    evidence_count = sum(
        [
            context,
            ownership,
            reasoning,
            stakeholder,
            outcome,
            metric,
        ]
    )

    if words >= 100 and evidence_count >= 5:
        relevance = max(relevance, 4.0)
        structure = max(structure, 4.0)
        specificity = max(specificity, 4.0)
        impact = max(impact, 4.0)

    # Prevent a long but empty answer from looking strong.
    if words >= 100 and evidence_count <= 2:
        specificity = min(specificity, 2.5)
        impact = min(impact, 2.0)

    overall = clamp(mean([relevance, structure, specificity, impact]))

    # A very short response can be relevant, but cannot credibly demonstrate
    # interview-level depth. Keep it in the weak-answer band unless it is
    # genuinely substantial enough to assess.
    if words < 40:
        overall = min(overall, 2.5)

    detailed_scores = [
        {
            "dimension": "Relevance",
            "score_per_dimension": relevance,
            "justification": relevance_feedback(relevance, context, reasoning),
        },
        {
            "dimension": "Structure",
            "score_per_dimension": structure,
            "justification": structure_feedback(structure, context, ownership, outcome),
        },
        {
            "dimension": "Specificity",
            "score_per_dimension": specificity,
            "justification": specificity_feedback(
                specificity, ownership, stakeholder, metric
            ),
        },
        {
            "dimension": "Business Impact",
            "score_per_dimension": impact,
            "justification": impact_feedback(impact, outcome, metric, learning),
        },
    ]

    improvements = []
    if relevance < 4:
        improvements.append("Tie the example more explicitly to the question being asked.")
    if structure < 4:
        improvements.append("Make the situation, decision/action, and result easier to distinguish.")
    if specificity < 4:
        improvements.append("Add more detail about your personal decisions, trade-offs, and stakeholders.")
    if impact < 4:
        improvements.append("Quantify the outcome and explain why it mattered to the business or customer.")

    strengths = []
    if ownership:
        strengths.append("Shows personal ownership rather than describing only the team's work.")
    if reasoning:
        strengths.append("Explains decision-making and trade-offs.")
    if metric:
        strengths.append("Uses quantitative evidence.")
    if outcome:
        strengths.append("Ends with a concrete outcome.")

    return {
        "overall_score": overall,
        "detailed_scores": detailed_scores,
        "feedback": {
            "strengths": strengths,
            "improvements": improvements,
        },
    }


def the_question_is_directly_answered(answer: str, question: str) -> bool:
    q = question.lower()

    if "prioritization" in q or "prioritisation" in q:
        return has_any(
            answer.lower(),
            ["prioritized", "prioritised", "roadmap", "de-prioritized",
             "deprioritized", "changed our priorities", "moved", "ahead"],
        )

    if "product failure" in q:
        return has_any(
            answer.lower(),
            ["failure", "failed", "incident", "root cause", "problem", "mistake"],
        )

    if "digital wallet" in q or "one metric" in q:
        return has_any(
            answer.lower(),
            ["metric", "retention", "conversion", "adoption", "activation",
             "transaction", "usage", "wallet"],
        )

    return True


def relevance_feedback(score: float, context: bool, reasoning: bool) -> str:
    if score >= 4.5:
        return "Directly answers the interview question with relevant context and decision reasoning."
    if score >= 4.0:
        return "Clearly addresses the core question with relevant professional context."
    if context and reasoning:
        return "The answer establishes relevant context and some decision reasoning."
    return "The response is related, but the connection to the question could be more explicit."


def structure_feedback(
    score: float, context: bool, ownership: bool, outcome: bool
) -> str:
    if score >= 4.5:
        return "Clear progression from context to personal action and measurable result."
    if score >= 4.0:
        return "The response has a clear story and decision flow."
    if context and ownership and outcome:
        return "A coherent story is present, but the interview framework could be made more explicit."
    return "The response would benefit from a clearer situation, action, and result sequence."


def specificity_feedback(
    score: float, ownership: bool, stakeholder: bool, metric: bool
) -> str:
    if score >= 4.5:
        return "Highly specific personal actions, stakeholders, trade-offs, and evidence are provided."
    if score >= 4.0:
        return "The response demonstrates personal actions and supporting reasoning."
    missing = []
    if not ownership:
        missing.append("personal ownership")
    if not stakeholder:
        missing.append("stakeholder detail")
    if not metric:
        missing.append("quantitative evidence")
    return "Add " + ", ".join(missing) + "." if missing else "More concrete evidence would strengthen the answer."


def impact_feedback(
    score: float, outcome: bool, metric: bool, learning: bool
) -> str:
    if score >= 4.5:
        return "The response includes strong measurable evidence and a concrete business outcome."
    if score >= 4.0:
        return "The response includes a concrete outcome with useful business evidence."
    if outcome and metric:
        return "A measurable outcome is present, but its business significance could be explained further."
    if learning:
        return "The response demonstrates learning or process impact, but needs a stronger measurable outcome."
    return "Add a concrete outcome and, where possible, quantify the business or customer impact."


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "service": "AI Interview Coach MVP", "version": "1.0.0"}


@app.post("/api/v1/start", response_model=List[dict])
async def start_interview(request: StartInterviewRequest):
    """
    Existing frontend-compatible contract.

    Returns exactly the list of questions expected by the current UI.
    """
    return QUESTIONS


@app.post("/api/v1/submit_answer")
async def submit_answer(request: SubmitAnswerRequest):
    answer = clean_text(request.user_answer or request.answer)

    question = ""
    if request.question_id:
        for item in QUESTIONS:
            if item["question_id"] == request.question_id:
                question = item["question_text"]
                break

    question = request.question_text or question
    framework = request.suggested_framework or ""

    result = evaluate_answer(answer, question, framework)

    # Store evaluation for the eventual summary page.
    session_key = request.target_role or "demo"
    SESSIONS.setdefault(session_key, {"evaluations": []})
    SESSIONS[session_key]["evaluations"].append(
        {
            "question_id": request.question_id,
            "question": question,
            "answer": answer,
            **result,
        }
    )

    return result


@app.post("/api/v1/summary")
async def interview_summary(payload: Dict[str, Any]):
    """
    End-of-interview summary endpoint.

    The current frontend does not need this endpoint yet, but it makes the MVP
    backend complete enough for a final results screen without changing the
    scoring contract.
    """
    session_key = clean_text(payload.get("target_role")) or "demo"
    evaluations = SESSIONS.get(session_key, {}).get("evaluations", [])

    if not evaluations:
        return {
            "completed": 0,
            "total_questions": len(QUESTIONS),
            "overall_score": 0.0,
            "dimension_averages": {},
            "top_strengths": [],
            "priority_improvements": ["Complete at least one interview answer."],
        }

    scores_by_dimension: Dict[str, List[float]] = {}
    strengths: List[str] = []
    improvements: List[str] = []

    for evaluation in evaluations:
        for item in evaluation["detailed_scores"]:
            scores_by_dimension.setdefault(item["dimension"], []).append(
                float(item["score_per_dimension"])
            )

        strengths.extend(evaluation.get("feedback", {}).get("strengths", []))
        improvements.extend(evaluation.get("feedback", {}).get("improvements", []))

    dimension_averages = {
        dimension: round(mean(values), 1)
        for dimension, values in scores_by_dimension.items()
    }

    overall = round(
        mean(
            float(evaluation["overall_score"])
            for evaluation in evaluations
        ),
        1,
    )

    # Preserve order while deduplicating.
    top_strengths = list(dict.fromkeys(strengths))[:3]
    priority_improvements = list(dict.fromkeys(improvements))[:3]

    return {
        "completed": len(evaluations),
        "total_questions": len(QUESTIONS),
        "overall_score": overall,
        "dimension_averages": dimension_averages,
        "top_strengths": top_strengths,
        "priority_improvements": priority_improvements,
    }