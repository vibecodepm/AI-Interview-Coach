# AI Interview Coach MVP Project Setup

This project is structured as a decoupled Full-Stack application using Next.js for the frontend UI and FastAPI for the machine intelligence backend.

## 🚀 Tech Stack
*   **Client:** React/Next.js (SPA)
*   **API:** Python 3.11+
*   **Backend Framework:** FastAPI
*   **Database Mock:** PostgreSQL via SQL Schema definition

## 📦 Setup Instructions (Must be followed in order)

1.  **Install Dependencies:**
    ```bash
    # Navigate to /ai-interview-coach
    npm install 
    pip install -r requirements.txt
    ```

2.  **Database Initialization (Initial State)**
    *This step uses the defined schema but requires a local Postgres instance.*
    ```bash
    # You must create your database manually first: CREATE DATABASE ai_interview_db;
    # Run your initialization script using Alembic/SQLAlchemy tooling to apply schemas/db_schema.sql
    python manage.py migrate
    ```

3.  **Running the Services (Concurrent)**
    *(You MUST open two separate terminal windows)*

    *   **Terminal 1 (Backend API):**
        ```bash
        uvicorn src.backend.main:app --reload --port 8000
        ```
    *   **Terminal 2 (Frontend UI):**
        ```bash
        npm run dev # Runs the Next.js server on port 3000 by default
        ```

## 🛣️ End-to-End Flow Goal
The goal is to hit `http://localhost:3000`, which calls the API endpoint (`/api/v1/start`) on port **8000**. The UI must correctly consume the mock JSON response and display it without failure.
