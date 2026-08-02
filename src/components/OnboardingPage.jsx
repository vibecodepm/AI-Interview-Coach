// /Users/maccook/Desktop/Hermes Projects/AI-Interview-Coach/src/components/OnboardingPage.jsx

import React, { useState } from 'react';
// Assuming a LoadingSpinner component exists in the actual global scope or needs to be mocked
const LoadingSpinner = () => (
    <div className="flex items-center justify-center space-x-2 text-blue-600">
        <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path fill="currentColor" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12s12-6.627 12-12S18.627 0 12 0z"></path></svg>
        <span>Analyzing credentials... Please wait.</span>
    </div>
);

const OnboardingPage = () => {
    // State for all required inputs
    const [resumeContent, setResumeContent] = useState(""); // Placeholder: Assume file processing will populate this text field
    const [jobDescription, setJobDescription] = useState("");
    const [targetRole, setTargetRole] = useState("PM");

    // New States for Feature #001
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [initialQuestion, setInitialQuestion] = useState(null); // Stores the first question object

    /**
     * Handles the submission of input data to start the mock interview sequence.
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!resumeContent || !jobDescription || !targetRole) {
            setError("Please fill all fields before starting the simulation.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setInitialQuestion(null); // Clear previous results

        const payload = { 
            resume_text: resumeContent, 
            job_description: jobDescription, 
            target_role: targetRole 
        };

        try {
            // Placeholder for the actual API call to /api/v1/start
            // In a real app, you would use fetch or axios here.
            console.log("Attempting to connect to backend...");
            
            // --- MOCK API CALL SIMULATION (REPLACING ACTUAL FETCH) ---
            await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate network latency

            // Mock successful response matching the expected structure from FastAPI: list of question objects
            const mockResponse = [
                {
                    "question_text": "Describe a time your prioritization changed due to external market factors. (STAR required)",
                    "suggested_framework": "CIRCLES with an external pivot variable", 
                    "follow_up_prompt": ["What is the change cost?", "How was stakeholder buy-in maintained?", "Did you need to de-prioritize X?"]
                }
            ];

            // Update state with results only if successful
            setInitialQuestion(mockResponse[0]); 

        } catch (err) {
            console.error("API Error:", err);
            setError("Could not connect to the backend service. Please ensure FastAPI is running on port 8000.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="p-8 bg-white shadow-2xl rounded-xl max-w-5xl mx-auto border border-gray-100">
            <h1 className="text-4xl font-extrabold text-gray-900 mb-3">AI Interview Coach MVP</h1>
            <p className="text-lg text-blue-600 mb-8 border-b pb-4">
                Your objective, metric-driven practice for PM/Product roles.
            </p>

            <form onSubmit={handleSubmit} className="space-y-12">
                {/* 1. Resume Upload/Text Area */}
                <div>
                    <label htmlFor="resume" className="block text-xl font-bold text-gray-800 mb-3 border-l-4 border-blue-500 pl-3">
                        1. Your Professional History (Source Material)
                    </label>
                    <textarea
                        id="resume"
                        rows="9"
                        className={`w-full p-4 text-lg border-2 rounded-xl focus:ring-blue-500 transition duration-150 resize-y ${error ? 'border-red-300' : 'border-gray-200'}`}
                        placeholder="Paste the full, raw text of your resume here. The system will rely on this for all context and validation."
                        value={resumeContent}
                        onChange={(e) => setResumeContent(e.target.value)}
                    />
                </div>

                {/* 2. Job Description */}
                <div>
                    <label htmlFor="jd" className="block text-xl font-bold text-gray-800 mb-3 border-l-4 border-blue-500 pl-3">
                        2. Target Job Description (Domain Context)
                    </label>
                    <textarea
                        id="jd"
                        rows="7"
                        className={`w-full p-4 text-lg border-2 rounded-xl focus:ring-blue-500 transition duration-150 resize-y ${error ? 'border-red-300' : 'border-gray-200'}`}
                        placeholder="Paste the entire job posting here. This defines the required competencies and domain vocabulary."
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                    />
                </div >

                {/* 3. Role Selector */}
                <div>
                    <label className="block text-xl font-bold text-gray-800 mb-4 border-l-4 border-blue-500 pl-3">
                        3. Select Target Persona / Consulting Focus
                    </label>
                    <select 
                        value={targetRole} 
                        onChange={(e) => setTargetRole(e.target.value)} 
                        className="w-full p-4 text-lg border-2 border-gray-200 rounded-xl appearance-none focus:ring-blue-500 focus:border-blue-500 transition duration-150 bg-white"
                    >
                        <option value="" disabled className="text-gray-500">-- Select your role to configure interview deep-dive --</option>
                        <option value="PM">Product Manager (Generalist PM)</option>
                        <option value="APM">Associate Product Manager (Early Career Focus)</option>
                        <option value="AI PM">AI Product Manager (ML Ops & LLM Guardrails)</option>
                        <option value="SPM">Senior Product Manager (GPM/Domain Lead)</option>
                    </select>
                </div>

                {/* Submission Button Area */}
                <div>
                    <button 
                        type="submit"
                        className={`w-full py-4 px-6 text-xl font-bold rounded-lg shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition duration-200 ${isLoading ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-700 hover:bg-blue-800'} text-white`}
                        disabled={!resumeContent || !jobDescription || isLoading}
                    >
                        {isLoading ? (
                            <div className="flex items-center justify-center space-x-2">
                                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path fill="currentColor" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12s12-6.627 12-12S18.627 0 12 0z"></path></svg>
                                <span>Awaiting Backend Analysis...</span>
                            </div>
                        ) : (
                            "Start 🚀 Mock Interview Simulation"
                        )}
                    </button>

                    {/* Error Display Area */}
                    {error && (
                        <div className="mt-4 p-3 bg-red-100 text-red-700 border-l-4 border-red-500 rounded">
                            <strong>Error:</strong> {error}
                        </div>
                    )}
                </div >
            </form>

            {/* Initial Question Card / Output Display Area */}
            {initialQuestion && (
                <div className="mt-16 pt-8 border-t border-gray-200">
                    <h2 className="text-3xl font-extrabold text-green-700 mb-4 flex items-center">
                        ✅ Simulation Started! Focused Question:
                    </h2>
                    <div className="bg-green-50 p-8 border-l-8 border-green-500 bg-white shadow-md rounded-lg transition duration-300 transform hover:shadow-xl">
                        <p className="text-2xl font-semibold text-gray-900 mb-4">{initialQuestion.question_text}</p>
                        <div className="mt-4 p-4 bg-green-100 rounded border border-green-200/70">
                            <h3 className="font-bold text-lg text-green-800 mb-2 flex items-center">
                                <span className="text-xl mr-2">💡</span> Focus Guidance:
                            </h3>
                            <p className='text-sm'>**Framework Required:** {initialQuestion.suggested_framework}</p>
                        </div>
                        <div className="mt-4 text-sm text-gray-600 space-y-1">
                            <p font-weight="bold" className="flex items-center">🔥 Follow-ups expected on:</p>
                            <ul className='list-disc list-inside ml-4'>
                                {initialQuestion.follow_up_prompt.map((item, index) => (
                                    <li key={index} className="text-gray-700">{item}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            )} {/* End Initial Question Card */}

        </div >
    );
};

export default OnboardingPage;