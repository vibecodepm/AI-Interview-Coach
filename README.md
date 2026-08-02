# AI Interview Coach MVP Project Setup (Live)
... [Omitted README content] ...

## 🚀 Tech Stack
*   **Client:** React/Next.js (SPA)
*   **API:** Python 3.11+
*   **Backend Framework:** FastAPI
*   **Database Mock:** PostgreSQL via SQL Schema definition

## 🧱 Environment Configuration (**CRITICAL**)
The application relies on environment variables to know where the API backend is running. The default address is set in `.env.local.example`. During development, you must ensure this variable points correctly.

- **Local Development:** Set `NEXT_PUBLIC_API_URL=http://localhost:8000`
- **Production Deployment:** Update this key to your production API gateway URL (e.g., `https://api.yourcompany.com/v1`).
... [Rest of README content] ...