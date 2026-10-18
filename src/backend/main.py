"""FastAPI contract for the AI Interview Coach MVP."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.backend.evaluation_system import (
    AnswerScoreSchema,
    InterviewEvaluator,
    StartInterviewRequest,
    SubmitAnswerRequest,
    get_llm_client_by_config,
)

app = FastAPI(title="AI Interview Coach MVP", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_evaluator_instance: InterviewEvaluator | None = None


@app.on_event("startup")
async def startup_event() -> None:
    global _evaluator_instance
    try:
        _evaluator_instance = InterviewEvaluator(get_llm_client_by_config())
    except Exception:
        _evaluator_instance = None


def evaluator_or_503() -> InterviewEvaluator:
    if _evaluator_instance is None:
        raise HTTPException(status_code=503, detail="Interview service is not ready")
    return _evaluator_instance


@app.get("/api/health")
def read_health() -> dict[str, str]:
    evaluator = evaluator_or_503()
    return {"status": "Operational", "service": "AI Interview Coach API", "provider": type(evaluator._llm).__name__}


@app.post("/api/v1/start")
async def start_interview(request: StartInterviewRequest) -> dict:
    evaluator = evaluator_or_503()
    try:
        questions = evaluator.generate_questions(request.resume_text, request.job_description, request.target_role)
        return {"success": True, "questions": questions}
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to generate interview questions") from exc


@app.post("/api/v1/submit_answer")
async def submit_answer_endpoint(request: SubmitAnswerRequest) -> dict[str, bool | AnswerScoreSchema]:
    evaluator = evaluator_or_503()
    try:
        score = evaluator.score_answer(
            question=request.question_text,
            user_answer=request.user_answer,
            resume_text=request.resume_text,
            jd_text=request.job_description,
            target_role=request.target_role,
        )
        return {"success": True, "score_report": score}
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to evaluate the answer") from exc
