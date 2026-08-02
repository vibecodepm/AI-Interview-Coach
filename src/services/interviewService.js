// /Users/maccook/Desktop/Hermes Projects/AI-Interview-Coach/src/services/interviewService.js

/**
 * API Service Layer for all Interview Coach communications.
 * Encapsulates networking logic, ensuring the component remains clean and decoupled from HTTP communication protocols.
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Initiates a new interview session by calling the backend API.
 * @param {object} payload - Contains resume_text, job_description, and target_role.
 * @returns {Promise<Array>} A promise resolving to the list of generated questions from the backend.
 */
export async function startInterview(payload) {
    const endpointUrl = `${BASE_URL}/api/v1/start`;

    try {
        // Standard Fetch Call
        const response = await fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
             // Attempt to read error text for better user feedback
            const errorText = await response.text();
            throw new Error(`HTTP error ${response.status}. Backend message parsed: ${errorText}`);
        }

        return await response.json();

    } catch (err) {
        console.error("Interview Service Failure:", err);
        // Re-throw the error so the calling component can catch and display a user-friendly message.
        throw new Error(`Failed to connect to service: ${err.message}. Check if FastAPI is running on port 8000.`);
    }
}

/**
 * Submits an answer for scoring against a specific question ID.
 * @param {object} payload - Contains question_id and user_answer.
 * @returns {Promise<Object>} A promise resolving to the structured score report.
 */
export async function submitAnswer(payload) {
    const endpointUrl = `${BASE_URL}/api/v1/submit_answer`;

    try {
        // Implementation placeholder for future use:
        const response = await fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}. Check backend logs.`);
        }
        return await response.json();

    } catch (err) {
         console.error("Answer Submission Failure:", err);
        throw new Error(`Failed to submit answer score: ${err.message}`);
    }
}