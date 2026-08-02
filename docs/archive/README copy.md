# AI Interview Coach Portfolio Project

## 🚀 Startup Guide (Tech Stack)
This project follows a modern, decoupled stack architecture designed for extreme scalability and maintainability.
- **Frontend:** Next.js (React) - For the interactive client side and UI scaffolding.
- **Backend/API:** FastAPI (Python) - To expose the business logic endpoints (`/start`, `/evaluate`).
- **Database:** PostgreSQL + Alembic/SQLAlchemy - For persistent state management of sessions and metrics.

## 🏗️ Project Structure
You will find the following core modules:
- `frontend/`: Contains React components for UI presentation (e.g., `OnboardingPage.jsx`).
- `backend/`: Contains all Python logic, including FastAPI routers and service classes (e.g., `evaluation_system.py`).
- `schemas/`: Contains the JSON Schema definitions that enforce data contract rigor.

## 🧩 Key Steps to Run Locally
1.  **Project Setup:** `npm install` (in frontend directory) & `pip install fastapi[all] pydantic psycopg2` (in backend directory).
2.  **Database Initialization:** Use Alembic CLI commands generated through the FastAPI setup to create the database schema defined in `schemas/db_schema.sql`.
3.  **API Connection:** Implement API routing in your main FastAPI router, hooking into the services provided by `evaluation_system.py`.

## 💡 Pro Tip for PM Reviewers
When presenting this, emphasize the **separation of concerns**: The UI is simple (React), while the complexity lives entirely within the scoring logic and database contracts—a scalable architecture demonstrating engineering maturity alongside product sense.