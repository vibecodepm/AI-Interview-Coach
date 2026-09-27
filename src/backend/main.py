"""
AI Interview Coach MVP backend using FastAPI.

Dependencies: fastapi, uvicorn, pydantic, python-dotenv, fastapi-users, requests
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel # Ensure BaseModel is available

# Local imports must point to the modified library structure
from src.backend.evaluation_system import (
    InterviewEvaluator, 
    get_llm_client_by_config, 
    LLMClientAbstract,
    ScoreCriteriaItem,
    AnswerScoreSchema,
    QuestionResultSchema,
    StartInterviewRequest,
    SubmitAnswerRequest
)

# --- CONFIGURATION ---

app = FastAPI(title="AI Interview Coach MVP", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DEPENDENCY INJECTION LAYER ---

@app.on_event("startup")
async def startup_event():
    """Initializes the core application service layer on startup."""
    try:
        # 1. Get the dynamically configured LLM Client (Mock or Ollama)
        llm_client = get_llm_client_by_config()
        
        # 2. Create the reusable evaluator instance
        global _evaluator_instance
        _evaluator_instance = InterviewEvaluator(llm_client=llm_client)
        print(f"✅ API Startup: Evaluator initialized with {type(llm_client).__name__} client.")
    except Exception as e:
        print(f"❌ FATAL API Startup Error: Could not initialize LLM Client. {e}")
        # Crash the startup or set a global failure flag if the LLM layer is mandatory
        global _evaluator_instance
        _evaluator_instance = None


# --- ENDPOINTS ---

@app.get("/api/health")
def read_root():
    """Basic health check to confirm FastAPI is running."""
    if _evaluator_instance is None:
        raise HTTPException(status_code=503, detail="Service Unavailable: Core LLM service failed to initialize.")
    return {"status": "Operational", "service": "AI Interview Coach API", "provider": type(_evaluator_instance._llm).__name__}

@app.post("/api/v1/start")
async def start_interview(request: StartInterviewRequest):
    """Endpoint to generate the initial set of questions."""
    try:
        if _evaluator_instance is None:
             raise HTTPException(status_code=503, detail="Service not ready.")
             
        questions = _evaluator_instance.generate_questions(
            resume_text=request.resume_text, 
            jd_text=request.job_description, 
            target_role=request.target_role
        )
        return {"success": True, "questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")

@app.post("/api/v1/submit_answer")
async def submit_answer_endpoint(request: SubmitAnswerRequest):
    """Endpoint to submit an answer for scoring."""
    if _evaluator_instance is None:
         raise HTTPException(status_code=503, detail="Service not ready.")

    try:
        # SECURITY CHECK: Attempt to verify question context using the known list
        # In a real system, we'd validate question_id against QUESTIONS list.
        
        score = _evaluator_instance.score_answer(
            question=request.question_text or \"Missing Question Context\",
            user_answer=request.user_answer,
            resume_text=\"(Missing Context)\", # Should ideally come from session state
            jd_text=\"(Missing Context)\",
            target_role=request.target_role or \"PM\"
        )
        return {"success": True, "score_report": score}

    except Exception as e:
        # Catches ALL errors (network, schema, heuristic, etc.)
        raise HTTPException(status_code=500, detail=f"Failed to process answer: {str(e)}")

# Global instance used to store and access the runtime-configured evaluator
_evaluator_instance = None