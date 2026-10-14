# Actual Runtime Architecture Validation (As Of: Current Execution Period)

**Repository Root:** `/Users/maccook/Desktop/Hermes Projects/AI-Interview-Coach`

## 1. Data Flow Diagram (Step-by-Step Trace)

**Frontend $\xrightarrow{\text{POST Request}}$ Backend Gateway $\xrightarrow{\text{API Call}}$ Evaluation Service $\xrightarrow{\text{Call}}$ LLM/Provider $\xrightarrow{\text{Structured JSON}}$ Frontend**

1.  **Frontend Component:** `OnboardingPage.jsx` (Next.js) is the entry point, handling state for R/JD/Role.
2.  **API Abstraction:** `src/services/interviewService.js` handles fetching via standardized `fetch` calls against `http://localhost:8000/api/v1/...`. This is a clean contract layer.
3.  **Backend API Gateway:** `src/backend/main.py` (FastAPI) acts as the router. It receives the payload, delegates to `interviewService.js`, and calls `evaluation_system.py`.
4.  **Evaluation Service:** `src/services/evaluation_system.py` receives the instruction. **This module is the single point of failure/success.** It contains the `MockLLMClient` which *simulates* the entire LLM process step for testing.
5.  **LLM/Provider:** **STATUS: BLOCKED.** The flow halts at the `MockLLMClient` within `evaluation_system.py`. **No real LLM/SDK/Credential is found or utilized.**

**Conclusion:** The flow structure is perfectly laid out. The only point preventing it from being a "real AI evaluation" is the reliance on the stubbed `MockLLMClient`.

## 2. Dependencies and Configuration
*   **Required SDK:** An actual LLM SDK (e.g., `openai`).
*   **Required Env Vars:** A credential (e.g., `OPENAI_API_KEY`) must be set in the environment for the `MockLLMClient` to be replaced with a real API call.

## 3. State of the Components
*   **Frontend:** Fully modular and ready for API binding.
*   **Backend:** API hooks are correctly placed (`main.py`, `interviewService.js`).
*   **Logic:** The `evaluation_system.py` schema (`Pydantic` models) is correctly defined to enforce the required JSON output structure, even when simulated.

**This report accurately reflects the CURRENT IMPLEMENTED ARCHITECTURE and the BLOCKER that prevents full execution.**