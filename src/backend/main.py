# src/backend/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from starlette.middleware.cors import CORSMiddleware # Import the necessary middleware

# ===============================================================
# 1. INITIALIZATION & DEPENDENCY SETUP
# ===============================================================

app = FastAPI(title="AI Interview Coach API", version="1.0.0-mvp")

# ⚡️ FEATURE INTEGRATION: Apply CORS Middleware (Feature #005)
origins = [
    "http://localhost:3000",   # Frontend development origin
    "http://127.0.0.1:3000",   # Common local alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     # Allows GET, POST, etc.
    allow_headers=["*"],     # Allows any header (e.g., Content-Type)
)


# Initialize shared components (simulating dependency injection)
from .evaluation_system import InterviewEvaluator, MockLLMClient # Import the core engine logic

mock_llm_client = MockLLMClient()
evaluator_service = InterviewEvaluator(llm_client=mock_llm_client)


# ... [The rest of the file content remains unchanged] ...

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "AI Interview Coach MVP", "version": "1.0.0"}


# ===============================================================
# 2. API REQUEST MODELS (Data Contract)
# ===============================================================

class StartInterviewRequest(BaseModel):
    """Input payload for starting a new interview session."""
    resume_text: str | None = None 
    job_description: str
    target_role: str


@app.post("/api/v1/start", response_model=List[dict])
async def start_interview(request: StartInterviewRequest):
    """
    Endpoint to initialize a new interview session by mock-generating 3 questions.
    REPLACES the complex LLM call with deterministic, runnable mock data for MVP testing.
    """
    print("--- API HIT: Running /api/v1/start endpoint ---")
    # MOCK DATA GENERATION: Hardcoding deterministic output that satisfies the type contract
    mock_questions = [
        {
            "question_text": "Describe a time your prioritization changed due to external market factors. (STAR required)",
            "suggested_framework": "CIRCLES with an external pivot variable", 
            "follow_up_prompt": ["What is the change cost?", "How was stakeholder buy-in maintained?", "Did you need to de-prioritize X?"]
        },
        {
            "question_text": "Walk us through a product failure and what systemic process changes protected the organization later.",
            "suggested_framework": "STAR (Failure focus)", 
            "follow_up_prompt": ["What was the quantitative loss?", "How difficult was root cause analysis?", "Did you integrate new monitoring tools?"]
        },
        {
            "question_text": "If given full ownership of our Digital Wallet, what is ONE metric you would move immediately and why?",
            "suggested_framework": "Aha Moment/Metric Analysis", 
            "follow_up_prompt": ["Can you model the impact vs. current state?", "Who benefits the most from this change in metrics?", "What secondary risks are introduced by prioritizing this metric?"]
        }
    ]
    return mock_questions


@app.post("/api/v1/submit_answer")
async def submit_answer(request: dict): 
    """
    Endpoint that receives a user answer and processes it through the full scoring lifecycle.
    Returns the detailed score report using hardcoded, representative data.
    """
    print("--- API HIT: Running /api/v1/submit_answer endpoint ---")
    # MOCK DATA GENERATION: Hardcoding one perfect, demonstrable score report
    return {
        "overall_score": 4.2,
        "detailed_scores": [
            {
                "dimension": "Relevance", 
                "score_per_dimension": 4, 
                "justification": "Highly relevant to the JD's focus on Digital Wallet retention."
            },
             {
                "dimension": "Structure", 
                "score_per_dimension": 3, 
                "justification": "Close adherence to STAR, but needs explicit naming of phases (Action)."
            }
        ],
        "structured_feedback": "The answer was strong and quantified. Focus next time on explicitly labeling your achievements with the technical metrics provided in the job description.",
        "improved_answer_rewrite": "Reframing my experience: I achieved a quantifiable 20% uplift in transaction volume by implementing a phased A/B test that validated X metric improvement, aligning directly with retention goals."
    }