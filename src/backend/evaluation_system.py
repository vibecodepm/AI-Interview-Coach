# evaluation_system.py

import json
from typing import List, Dict, Any, TypedDict
from pydantic import BaseModel, Field, validator # Assuming Pydantic is used for schema validation

# ===============================================================
# 1. SCHEMA DEFINITIONS (Enforcing Rigor - The Contract)
# These classes define the exact JSON output structure required from the LLM.
# In a real system, these would be generated using proper Pydantic/JSON Schema tooling.
# ===============================================================

class ScoreCriteriaItem(BaseModel):
    """Scores one dimension (e.g., Specificity). Uses 1-5 scale."""
    dimension: str = Field(..., description="The criterion being assessed (e.g., Relevance, Structure).")
    score: int = Field(..., ge=1, le=5, description="Score on a 1 to 5 scale.")
    justification: str = Field(..., description="Brief analysis supporting the assigned score.")

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
# 2. CORE EVALUATION ENGINE CLASS
# This class encapsulates the complex logic that calls the LLM endpoint with structured prompts.
# ===============================================================

class InterviewEvaluator:
    def __init__(self, llm_client):
        """Initializes the evaluator with a trained LLM client instance."""
        self._llm = llm_client # Dependency injection for testing/mocking

    def generate_questions(self, resume_text: str, jd_text: str, target_role: str) -> List[QuestionResultSchema]:
        """
        Generates a set of role-specific behavioral and product questions.

        Args:
            resume_text: Parsed text from user's resume.
            jd_text: Job description text.
            target_role: The astronautics role (PM, AI PM, etc.).

        Returns:
            A list of QuestionResultSchema objects.
        """
        print(f"Executing Engine: Generating {target_role}-specific questions...")
        # Pseudocode for the complex LLM call that enforces structured output
        prompt = f"""Act as a Series A Tech Recruiter specializing in {target_role} hiring. 
        Based on this JD ({jd_text[:200]}...) and Resume ({resume_text[:200]}...), generate 3 core interview questions. 
        Each question MUST be tied to a specific best-practice framework (STAR, RICE etc.) 
        and include 2 logical follow-up prompts."""
        
        # Simulated LLM call
        questions = self._llm.call_structured(prompt, target_schema=List[QuestionResultSchema])
        print("Q Generation Complete.")
        return questions

    def score_answer(self, question: str, user_answer: str, resume_text: str, jd_text: str, target_role: str) -> AnswerScoreSchema:
        """
        Scores the user's answer against the defined 5-dimensional rubric.

        Args:
            question: The prompt asked to the candidate.
            user_answer: The raw text of the candidate's response.
            resume_text, jd_text, target_role: Context for deep evaluation grounding.

        Returns:
            An AnswerScoreSchema object containing detailed feedback and score breakdown.
        """
        print("Executing Engine: Scoring answer...")
        # Pseudocode for the complex LLM call that enforces structured output
        prompt = f"""You are a ruthless, expert Product Manager Interview interviewer. 
        Evaluate the following user response against the question, using these inputs as full context: [JD] {jd_text} | [Resume] {resume_text}.
        Question: "{question}" 
        User Answer: "{user_answer}"
        REQUIRED OUTPUT FORMAT MUST ADHERE TO THE ANSWER SCORE SCHEMA. Ensure the improved answer rewrite directly ties back to facts in the provided resume/JD."""

        # Simulated LLM call
        score_data = self._llm.call_structured(prompt, target_schema=AnswerScoreSchema)
        print("Scoring Complete.")
        return score_data


# ===============================================================
# 3. MOCK IMPLEMENTATION 
# This class simulates the external LLM service access using structured types.
# We must assume this capability exists to make the code runnable for demonstration.
# ===============================================================

class MockLLMClient:
    """Mocks the interaction with an advanced, schema-guaranteed LLM API."""
    def __init__(self):
        print("Logger: Initialized Mock LLM Client.")
    
    def call_structured(self, prompt: str, target_schema: type) -> Any:
        """Simulates calling the LLM and retrieving a structured object instance."""
        # In reality, this would involve API calls (OpenAI/Anthropic).
        if issubclass(target_schema, list): # Check if mock needs to handle List[Schema]
            print("Mock Client: Simulating batch output...")
            return []
        
        try:
            field_name = target_schema.__name__
            # Simulate successful structured JSON parsing
            if "QuestionResultSchema" in str(target_schema):
                from types import MethodType
                mock_result = QuestionResultSchema(
                    question_text="Describe a time your prioritization changed due to external market factors.", 
                    suggested_framework="CIRCLES with an external pivot variable", 
                    follow_up_prompt=["What is the change cost?", "How was stakeholder buy-in maintained?", "Did you need to de-prioritize X?"]
                )
                return [mock_result]
            
            elif "AnswerScoreSchema" in str(target_schema):
                print("Mock Client: Simulating detailed scoring output...")
                # Simulate populating the complex AnswerScoreSchema instance
                from datetime import date
                mock_score = ScoreCriteriaItem(dimension="Relevance", score=4, justification="Directly addressed market shift.")
                list_of_scores = List[ScoreCriteriaItem]([mock_score]) # Requires type coercion if not running live
                
                # For demonstration purposes, we instantiate the complex structure
                return AnswerScoreSchema(
                    overall_score=4.1,
                    scores=[
                        ScoreCriteriaItem(dimension="Relevance", score=4, justification="Directly addressed market shift."),
                        ScoreCriteriaItem(dimension="Structure", score=3, justification="Used a general narrative but needed STAR for improvement."),
                        ScoreCriteriaItem(dimension="Specificity", score=5, justification="Mentioned '20% uplift' and '$1.2M revenue goal', highly specific."),
                        ScoreCriteriaItem(dimension="Business impact", score=4, justification="Tied outcome to retention metrics."),
                        ScoreCriteriaItem(dimension="Clarity", score=4, justification="Clear flow, though slightly verbose.")
                    ],
                    structured_feedback="Overall excellent answer. The specificity on uplift combined with the business metric anchors your narrative powerfully. Key improvement: Always structure failure/success stories using STAR to maximize impact.",
                    improved_answer_rewrite="During a key market pivot, our original goal of Feature X was invalidated by regulatory changes... (Structured to show Action -> Result)."
                )

        except Exception as e:
            print(f"Mock LLM Error on {target_schema.__name__}: {e}")
            return None


# ===============================================================
# DEMONSTRATION BLOCK
# ===============================================================

if __name__ == "__main__":
    print("="*80)
    print("               *** AI Interview Coach System Initialized ***")
    print(f"             Loaded Core Logic from: {__file__}")
    print("="*80)

    mock_client = MockLLMClient()
    evaluator = InterviewEvaluator(llm_client=mock_client)

    # --- STEP 1: QUESTION GENERATION SIMULATION ---
    SAMPLE_RESUME = "Experienced PM in FinTech with background in fraud loss prevention and payments optimization. Achieved 20% uplift in annual transaction volume (ATL)."
    SAMPLE_JD = "Seeking a Product Manager to own the Digital Wallet experience, focusing on maximizing user retention via premium features."
    TARGET_ROLE = "PM"

    try:
        print("\n>>> EXECUTING STEP 1: QUESTION GENERATION <<<")
        questions = evaluator.generate_questions(SAMPLE_RESUME, SAMPLE_JD, TARGET_ROLE)
        if questions and isinstance(questions, list):
            first_question = questions[0] # Assuming the first result is the main one for demo
            print("\n✅ STEP 1 SUCCESS:")
            print(f"   Generated Question: {first_question.question_text}")
            print(f"   Required Framework: {first_question.suggested_framework}")
        else:
            print("❌ WARNING: Could not generate questions (Skipping Step 2).")


    except Exception as e:
        print(f"\n🔴 FATAL ERROR in Question Generation: {e}")

    # --- STEP 2: ANSWER SCORING SIMULATION ---
    USER_ANSWER = "I think we should just focus on making the payment process faster. It's about user experience and reducing friction points for users."

    if 'questions' in locals() and questions:
        print("\n\n>>> EXECUTING STEP 2: ANSWER SCORING <<<")
        try:
            score_report = evaluator.score_answer(first_question.question_text, USER_ANSWER, SAMPLE_RESUME, SAMPLE_JD, TARGET_ROLE)

            print("\n=========================================================")
            print("               ✨ INTERVIEW SCORE REPORT ✨           ")
            print("=========================================================")
            print(f"👑 Overall Readiness Score: {score_report.overall_score:.1f} / 5.0")
            print("\n--- Structured Feedback ---")
            print(f"📝 Summary Coach Insight: {score_report.structured_feedback}")
            print(f"\n✨ Recommended Rewrite: \"{score_report.improved_answer_rewrite[:80]}...\" (Use this structure next time.)")

            print("\n--- Detailed Scoring Breakdown ---")
            for score in score_report.scores:
                print(f"  - {score.dimension:<25} | Score: {score.score}/5 | Justification: {score.justification}")

        except Exception as e:
            print(f"\n🔴 FATAL ERROR in Scoring: {e}")