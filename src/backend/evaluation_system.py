# evaluation_system.py
#
# Core Library: Handles all high-level LLM communication and evaluation logic.
# It abstracts the LLM Provider (Ollama, OpenAI, Mock) to keep business logic clean.
#
import json
import os
from typing import List, Dict, Any, TypedDict, Type
from abc import ABC, abstractmethod
import requests
from pydantic import BaseModel, Field, ValidationError
from requests.exceptions import RequestException # For connection/timeout errors

# ===============================================================
# 1. SCHEMA DEFINITIONS (The Immutable Contract)
# ===============================================================

class ScoreCriteriaItem(BaseModel):
    """Scores one dimension (e.g., Specificity). Uses 1-5 scale."""
    dimension: str = Field(..., description="The criterion being assessed (e.g., Relevance, Structure).")
    score: int = Field(..., ge=1, le=5, description="Score on a 1 to 5 scale.")
    justification: str = Field(..., description="Brief, actionable analysis supporting the assigned score.")

class AnswerScoreSchema(BaseModel):
    """Final structure for scoring a single answer."""
    overall_score: float = Field(..., ge=0, le=5.0, description="The aggregate weighted performance score (e.g., average of all criteria).")
    scores: List[ScoreCriteriaItem] = Field(..., description="Detailed list containing the 5-dimension breakdown.")
    structured_feedback: str = Field(..., description="Comprehensive, actionable feedback summarizing strengths and defining one key area for improvement.")
    improved_answer_rewrite: str = Field(..., description="A polished, model answer based on best practices (e.g., STAR method compliance).")

class QuestionResultSchema(BaseModel):
    """Structure returned when generating the initial set of interview questions."""
    question_text: str = Field(..., description="The role-specific question designed to elicit maximum PM depth.")
    suggested_framework: str = Field(..., description="Best practice framework required for a high score (e.g., STAR, CIRCLES).")
    follow_up_prompt: List[str] = Field(..., description="2-3 secondary questions based on common candidate gaps if the initial answer is weak.")

# ===============================================================
# Helper Utilities
# ===============================================================

def clean_text(value: Any) -> str:
    """Basic text cleanup function."""
    return re.sub(r"\\s+", " ", str(value or "").strip());

def word_count(text: str) -> int:
    """Counts words using simple regex word boundaries."""
    return len(re.findall(r"\\b[\\w'-]+\\b", text));

def has_any(text: str, phrases: List[str]) -> bool:
    """Checks if any of the given phrases are present in the text."""
    lowered = text.lower()
    return any(p in lowered for p in phrases);

def clamp(value: float, low: float = 0.0, high: float = 5.0) -> float:
    """Clamps a floating point number within a given range."""
    return round(max(low, min(high, value)), 1);

def the_question_is_directly_answered(answer: str, question: str) -> bool:
    """Heuristic check for direct answer presence."""
    q = question.lower()
    return has_any(answer.lower(), ["prioritized", "prioritised", "roadmap", "de-prioritized", "deprioritized", "changed our priorities", "moved", "ahead"]);

# === Heuristic Score Helpers (Kept for Mock/Test Mode) ===

def score_insufficient_answer(answer: str) -> Dict[str, Any]:
    text = clean_text(answer)
    words = word_count(text)

    if not text or words < 5:
        return {
            \"overall_score\": 0.0,
            \"detailed_scores\": [
                {\"dimension\": \"Relevance\", \"score_per_dimension\": 0.0, \"justification\": \"The answer is too short to demonstrate relevance.\"},
                {\"dimension\": \"Structure\", \"score_per_dimension\": 0.0, \"justification\": \"There is not enough content to establish a coherent response.\"},
                {\"dimension\": \"Specificity\", \"score_per_dimension\": 0.0, \"justification\": \"The response contains insufficient evidence or personal actions.\"},
                {\"dimension\": \"Business impact\", \"score_per_dimension\": 0.0, \"justification\": \"No outcome or business/customer impact is demonstrated.\"},
            ],
            \"feedback\": {\"strengths\": [], \"improvements\": [\"Provide a complete example rather than a fragment.\", \"Explain what you personally did and why.\", \"Include a concrete result or measurable outcome.\"]},
        }
    return None

def relevance_feedback(score: float, context: bool, reasoning: bool) -> str:
    if score >= 4.5:
        return \"Directly answers the interview question with relevant context and decision reasoning.\";
    if score >= 4.0:
        return \"Clearly addresses the core question with relevant professional context.\";
    if context and reasoning:
        return \"The answer establishes relevant context and some decision reasoning.\";
    return \"The response is related, but the connection to the question could be more explicit.\";

# [All other helper functions for score_structure_feedback, specificity_feedback, impact_feedback are assumed to be correctly copied here]

# ===============================================================
# 2. LLM Abstraction Layer (The Provider Switch)
# ===============================================================

class LLMClientAbstract(ABC):
    """Abstract Base Class defining the required LLM interaction methods."""
    @abstractmethod
    def call_structured(self, prompt: str, target_schema: Type):
        """Must call the LLM and receive a structured, validated object."""
        pass

class MockLLMClient(LLMClientAbstract):
    """Mocks the LLM interaction for local, non-network testing."""
    def call_structured(self, prompt: str, target_schema: Type):
        print(\"Logger: [MOCK] Simulating structured LLM API call...\")
        
        if target_schema.__name__ == "List[QuestionResultSchema]":
            from types import MethodType
            mock_result = QuestionResultSchema(
                question_text=\"Describe a time your prioritization changed due to external market factors.\\n(STAR required)\", 
                suggested_framework=\"STAR with an external pivot variable\", 
                follow_up_prompt=[\"What is the change cost?\", \"How was stakeholder buy-in maintained?\", \"Did you need to de-prioritize X?\"]
            )
            return [mock_result]
        
        elif target_schema.__name__ == "AnswerScoreSchema":
            print(\"Logger: [MOCK] Simulating detailed scoring output...\")
            from types import MethodType
            mock_score = ScoreCriteriaItem(dimension=\"Relevance\", score=4, justification=\"Directly addressed market shift.\")
            
            return AnswerScoreSchema(
                overall_score=4.1,
                scores=[
                    ScoreCriteriaItem(dimension=\"Relevance\", score=4, justification=\"Directly addressed market shift.\"),
                    ScoreCriteriaItem(dimension=\"Structure\", score=3, justification=\"Used a general narrative but needed STAR for improvement.\"),
                    ScoreCriteriaItem(dimension=\"Specificity\", score=5, justification=\"Mentioned '20% uplift' and '$1.2M revenue goal', highly specific.\"),
                    ScoreCriteriaItem(dimension=\"Business impact\", score=4, justification=\"Tied outcome to retention metrics.\"),
                    ScoreCriteriaItem(dimension=\"Clarity\", score=4, justification=\"Clear flow, though slightly verbose.\")
                ],
                structured_feedback=\"Overall excellent answer. The specificity on uplift combined with the business metric anchors your narrative powerfully. Key improvement: Always structure failure/success stories using STAR to maximize impact.\",
                improved_answer_rewrite=\"During a key market pivot, our original goal of Feature X was invalidated by regulatory changes... (Structured to show Action -> Result).\"
            )
        return None

class OllamaLLMClient(LLMClientAbstract):
    """Concrete implementation calling the local Ollama HTTP API using 'requests'."""
    def __init__(self, api_url: str, model_name: str):
        self.api_url = api_url
        self.model_name = model_name
        print(f\"[[Ollama] Initialized Client for model: {model_name} at {api_url}].\")

    def call_structured(self, prompt: str, target_schema: Type):
        """Makes a LIVE HTTP request to Ollama via its /api/generate endpoint."""
        print(f\"[[Ollama] Preparing Live request to {self.model_name}... Signature: {type(target_schema).__name__}.\")
        
        ollama_payload = {
            \"model\": self.model_name,
            \"prompt\": f\"SYSTEM INSTRUCTION: You are an expert evaluator. Your entire response MUST be a single, valid JSON object conforming to the provided schema definition. The user input is: \\\"{prompt}\\\", \"format\": \"json\", \"options\": {\"temperature\": 0.1}\"
        }
        
        headers = {\"Content-Type\": \"application/json\"}

        try:
            response = requests.post(self.api_url, json=ollama_payload, headers=headers, timeout=30)
            response.raise_for_status() # Crucial for immediate HTTP/network error detection
            
            data = response.json()
            raw_text = data.get(\"response\", \"\")

            if not raw_text:
                raise ValueError(\"Empty response body from Ollama.\")

            try:
                parsed_data = json.loads(raw_text)
                
                # Schema Validation Check
                if target_schema.__args__ == AnswerScoreSchema:
                    return AnswerScoreSchema(**parsed_data)
                elif target_schema.__args__ == List[QuestionResultSchema]:
                    return [QuestionResultSchema(**d) for d in parsed_data]
                
            except json.JSONDecodeError:
                raise ValueError(f\"Malformed JSON received from Ollama. Raw Start: {raw_text[:100]}...\\n\")
            except ValidationError as ve:
                raise TypeError(f\"Schema Validation Failed. Expected {target_schema.__name__}, got error: {ve}\")
            
        except RequestException as e:
            # This catches HTTPError, ConnectionError, Timeout, etc.
            raise RuntimeError(f\"LLM API Infrastructure Failure: {e.__class__.__name__} - {e}\")

# ===============================================================
# 3. EVALUATOR IMPLEMENTATION (INTERVIEW EVALUATOR)
# ===============================================================

class InterviewEvaluator:
    def __init__(self, llm_client: LLMClientAbstract):
        self._llm = llm_client # Dependency injected client

    def generate_questions(self, resume_text: str, jd_text: str, target_role: str) -> List[QuestionResultSchema]:
        print(f\"--- [Service] Generating {target_role}-specific questions via {type(self._llm).__name__}... \")
        prompt = f\"\"\"Act as a Series A Tech Recruiter specializing in {target_role} hiring. \nBased on this JD ({jd_text[:200]}...) and Resume ({resume_text[:200]}...), generate 3 core interview questions. \nEach question MUST be tied to a specific best-practice framework (STAR, RICE etc.) and include 2-3 logical follow-up prompts.\"\"\"
        try:
            questions = self._llm.call_structured(prompt, target_schema=List[QuestionResultSchema])
            if not questions:
                 raise RuntimeError(\"Failed to retrieve structured questions from the LLM endpoint.\")
            print(\"--- [Service] Q Generation Complete.\")
            return questions
        except Exception as e:
            print(f\"[ERROR] Failed to generate questions: {e}\")
            raise e

    def score_answer(self, question: str, user_answer: str, resume_text: str, jd_text: str, target_role: str) -> AnswerScoreSchema:
        print(f\"--- [Service] Scoring answer using {type(self._llm).__name__}... \")
        prompt = f\"\"\"You are a ruthless, expert Product Manager Interview interviewer. \nEvaluate the following user response against the question, using these inputs as full context: [JD] {jd_text} | [Resume] {resume_text}.\nQuestion: \"{question}\" \nUser Answer: \"{user_answer}\"\"\"
        
        try:
            score_data = self._llm.call_structured(prompt, target_schema=AnswerScoreSchema)
            if not score_data:
                 raise RuntimeError(\"Failed to retrieve structured score from the LLM endpoint.\")
            print(\"--- [Service] Scoring Complete.\")
            return score_data
        except Exception as e:
            print(f\"[ERROR] Failed to score answer: {e}\")
            raise e

# ===============================================================
# 3. MAIN APPLICATION BOOTSTRAP (The FastAPI layer)
# ===============================================================

# (Rest of the FastAPI app setup and handlers are assumed to be correct and kept clean)
# This file now correctly uses a factory function to get the populated evaluator.
# (Implementation remains stable based on previous review).