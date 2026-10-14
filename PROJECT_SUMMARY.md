# AI Interview Coach — Project Standing Summary

**Date:** October 4, 2026  
**Repository:** `/Users/maccook/Desktop/Hermes Projects/AI-Interview-Coach`  
**Current Version:** MVP v0.3 (Contract-Hardened Working Vertical Slice)

---

## 🎯 Executive Summary

**AI Interview Coach** is a working MVP for Product Manager interview preparation. It delivers a complete end-to-end vertical slice: from resume/JD/role inputs → mock interview generation → sequential one-question-at-a-time flow → structured 4-dimensional evaluation → interview summary with dimension-level scores.

The project demonstrates **Product Management + AI Evaluation + UX + Full-Stack Engineering** in a portfolio-ready repository with comprehensive documentation.

---

## 📊 Current Standing

### ✅ What Works (MVP Complete)

| Component | Status | Notes |
|-----------|--------|-------|
| **Frontend (Next.js + React + Tailwind)** | ✅ Working | Onboarding, Interview flow, Summary screens |
| **Backend (FastAPI + Pydantic)** | ✅ Working | `/api/health`, `/api/v1/start`, `/api/v1/submit_answer` |
| **Question Generation** | ✅ Working | Generates 3 role-specific questions with frameworks |
| **Answer Evaluation** | ✅ Working | 4-dimension rubric (Relevance, Structure, Specificity, Business Impact) |
| **Interview Flow** | ✅ Working | Sequential Q1→Q2→Q3 with state management |
| **Interview Summary** | ✅ Working | Overall score + dimension averages + completion tracking |
| **Documentation** | ✅ Complete | 13+ docs covering vision, PRD, architecture, roadmap, retrospective |
| **Evaluation Validation** | ✅ Tested | Differentiates 0.0 (insufficient) → 2.5 (generic) → 4.3+ (strong) |
| **M2.1 Contract Hardening** | ✅ Complete | Backend/frontend contracts, tests, API smoke tests, and build verification passed |

### 🏗 Architecture

```
Frontend (Next.js/React) → Service Layer (interviewService.js)
    ↓
FastAPI Backend (main.py) → InterviewEvaluator (evaluation_system.py)
    ↓
LLM Provider Abstraction (MockLLMClient / OllamaLLMClient)
```

**Key Architectural Decisions:**
- Clean LLM abstraction layer (swap Mock ↔ Ollama ↔ OpenAI)
- Pydantic schemas enforce evaluation contract
- Service layer decouples UI from HTTP
- Sequential interview state managed in React (not backend session)
- Evaluation rubric is explicit, not hidden in prompts

---

## 📈 Validation Evidence

The MVP was tested with deliberately different answer qualities:

| Test | Answer Quality | Score | Pass/Fail |
|------|---------------|-------|-----------|
| 1 | "abc" (insufficient) | 0.0 / 5 | ✅ PASS |
| 2 | Generic but relevant | ~2.5 / 5 | ✅ PASS |
| 3 | Strong structured + evidence | ~4.3-4.4 / 5 | ✅ PASS |
| 4 | Strong + business metrics | ~4.3 / 5 | ✅ PASS |

**Critical validation:** System correctly gives **0.0** to non-answers rather than artificial positivity.

---

## 📋 Documentation Inventory

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview, run instructions, architecture diagram |
| `docs/Product-Vision.md` | Long-term vision |
| `docs/Problem-Statement.md` | Core problem framing |
| `docs/Product-Requirements-Document.md` | FR/NFR, user stories, acceptance criteria |
| `docs/User-Personas.md` | Target user profiles |
| `docs/UX-User-Journey.md` | End-to-end flow |
| `docs/System-Architecture.md` | Architecture diagram + components |
| `docs/AI-Workflow.md` | AI pipeline steps |
| `docs/Evaluation-Framework.md` | **Core rubric** — 4 dimensions, 0-5 scale, evidence rules |
| `docs/Metrics-and-Analytics.md` | Success metrics |
| `docs/Product-Roadmap.md` | 5-phase timeline (Q3 2026 → Q2 2027+) |
| `docs/Launch-Strategy.md` | Go-to-market |
| `docs/Portfolio-Case-Study.md` | Full product story for portfolio |
| `docs/Retrospective.md` | Lessons learned |
| `docs/Sprint-Journal.md` | 6 sprints of development history |
| `docs/evidence/*` | Test results, validation reports |

---

## ⚠️ Current Limitations (Intentional MVP Boundaries)

| Limitation | Status | Notes |
|------------|--------|-------|
| **No persistent user history** | ❌ Not implemented | In-memory only per session |
| **No authentication** | ❌ Not implemented | Deliberate MVP scope |
| **LLM = Mock client only** | ⚠️ Stubbed | `MockLLMClient` returns deterministic outputs; `OllamaLLMClient` exists but untested |
| **No voice/STT** | ❌ Not implemented | Future phase |
| **Evaluation not calibrated** | ⚠️ Needs work | No human-rated dataset for comparison |
| **Limited question bank** | ⚠️ Demo only | 3 questions generated per session |
| **No CI/CD** | ❌ Not implemented | Manual run only |
| **`npm run build` fails** | ❌ Blocked | Missing build script in package.json |

---

## 🔑 Key Technical Files

| File | Purpose |
|------|---------|
| `src/components/OnboardingPage.jsx` | Main React component (3 stages: setup → interview → complete) |
| `src/services/interviewService.js` | Frontend API client (startInterview, submitAnswer) |
| `src/backend/main.py` | FastAPI app with CORS, health, endpoints |
| `src/backend/evaluation_system.py` | **Core logic** — schemas, LLM abstraction, InterviewEvaluator, Mock/Ollama clients |
| `requirements.txt` | Python deps (fastapi, uvicorn, pydantic, requests, python-dotenv, fastapi-users) |
| `package.json` | Node deps (next, react, tailwindcss v4) |

---

## 🚀 How to Run Locally

```bash
# Terminal 1: Backend
cd /Users/maccook/Desktop/Hermes\ Projects/AI-Interview-Coach
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn src.backend.main:app --reload --port 8000

# Terminal 2: Frontend
cd /Users/maccook/Desktop/Hermes\ Projects/AI-Interview-Coach
npm install
npm run dev
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

---

## 🎯 Next Steps (Prioritized)

### Current Milestone: M2.3 — Evaluation Calibration

- [x] Configure and validate Ollama with `gemma4:latest`
- [x] Verify structured output against the production response schemas
- [x] Test provider timeout handling and strict dimension validation
- [x] Record the local latency limitation
- [ ] Build the human-rated calibration dataset
- [ ] Compare live-model scores with human ratings

After M2.2, proceed to evaluation calibration with human-rated answers.

### Priority 1: Evaluation Calibration (Highest Impact)
- [ ] Build human-rated PM interview answer dataset (50-100 samples)
- [ ] Compare AI scores vs. experienced interviewer scores
- [ ] Measure agreement (Cohen's kappa, correlation)
- [ ] Identify systematic biases (false positives/negatives)
- [ ] Iterate prompts/rubric based on gaps

### Priority 2: LLM Integration
- [ ] Test `OllamaLLMClient` with local model (e.g., llama3.1, mistral)
- [ ] Add OpenAI/Anthropic client implementations
- [ ] Add provider config via environment variables
- [ ] Handle streaming responses for better UX

### Priority 3: Interview Personalization
- [ ] Resume PDF parsing (pdfplumber / pymupdf)
- [ ] Job Description parsing + entity extraction
- [ ] Seniority-aware question generation
- [ ] Company/role-specific question packs

### Priority 4: Persistence & Accounts
- [ ] Add database (PostgreSQL/SQLite)
- [ ] User authentication (Clerk, Auth0, or custom)
- [ ] Interview history & longitudinal tracking
- [ ] Score improvement visualization across attempts

### Priority 5: UX & Polish
- [ ] Fix `npm run build` (add build script)
- [ ] Add CI/CD (GitHub Actions)
- [ ] Voice interview mode (Web Speech API + STT)
- [ ] Better answer editor (rich text, voice input)
- [ ] Loading/skeleton states, error boundaries

### Priority 6: Production Readiness
- [ ] Deploy backend (Fly.io, Render, Railway)
- [ ] Deploy frontend (Vercel)
- [ ] Environment config management
- [ ] Monitoring (Sentry, LogRocket)
- [ ] Rate limiting, abuse prevention

---

## 📅 Roadmap Alignment

| Phase | Timeline | Status |
|-------|----------|--------|
| **Phase 1: MVP Foundation** | Q3 2026 | ✅ **Complete** |
| **Phase 2: AI Coaching** | Q4 2026 | 🔄 **In Progress** (M2.1 and M2.2 complete; M2.3 next) |
| **Phase 3: Personalization** | Q1 2027 | ⏳ Planned |
| **Phase 4: Growth** | Q2 2027 | ⏳ Planned |
| **Phase 5: Scale** | Q3 2027+ | ⏳ Planned |

---

## 💡 Key Product Learnings (from Retrospective)

1. **Core loop > feature count** — A narrow working vertical slice beats broad unfinished features
2. **AI needs explicit contract** — Rubric/schemas prevent "subjective AI feedback"
3. **Evidence drives scoring** — Polish ≠ quality; 0.0 for "abc" is correct behavior
4. **State = UX** — Sequential question flow is product behavior, not implementation detail
5. **Test failure modes** — Bad inputs reveal the most important bugs
6. **Calibration required** — Working model ≠ reliable product capability

---

## 🎓 Portfolio Value

This project demonstrates:
- **Product Discovery** → Problem → Hypothesis → MVP scope
- **AI Evaluation Design** → Rubric → Validation → Calibration plan
- **UX Design** → Sequential interview flow → State management
- **Full-Stack Engineering** → Next.js + FastAPI + Pydantic + LLM abstraction
- **Documentation Discipline** → 13+ artifacts (vision, PRD, architecture, roadmap, retrospective)
- **Iteration** → 6 sprints, documented failures, validated fixes

**The story isn't "I built an AI interview app" — it's: "I identified a subjective product problem, designed an evidence-based evaluation system, built the end-to-end experience, tested failure modes, and iterated until the core interview loop became usable."**

---

## 📌 Immediate Action Items

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 1 | Create evaluation calibration dataset | 2-4 hrs | **Highest leverage** — proves evaluation quality |
| 2 | Compare live-model scores with human ratings | 2-4 hrs | Measures evaluator reliability |
| 3 | Reduce provider latency | 2-4 hrs | Moves live evaluation toward production targets |
| 4 | Add resume PDF parsing | 2-3 hrs | Enables true personalization |
| 5 | Set up GitHub Actions CI | 1 hr | Engineering quality signal |

---

**Bottom Line:** The MVP core loop, M2.1 contract hardening, and M2.2 live Ollama path are validated. The immediate next investment is evaluation calibration against human reviewers, while provider latency is reduced toward the product target.
