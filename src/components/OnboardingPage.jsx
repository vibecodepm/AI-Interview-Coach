// /Desktop/Hermes Projects/AI-Interview-Coach/src/components/OnboardingPage.jsx

import React, { useState } from 'react';
import { startInterview } from '../services/interviewService'; // ⬅️ CONSUMING THE SERVICE LAYER
const LoadingSpinner = () => (
    <div className="flex items-center justify-center space-x-2 text-blue-600">
        <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path fill="currentColor" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12s12-6.627 12-12S18.627 0 12 0z"></path></svg>
        <span className="text-lg">Connecting to Interview Service...</span>
    </div >
);

const OnboardingPage = () => {
    // State for all required inputs
    const [resumeContent, setResumeContent] = useState(""); // Placeholder: Assume file processing will populate this text field
    const [jobDescription, setJobDescription] = useState("");
    const [targetRole, setTargetRole] = useState("PM");

    // New States for Feature #001 & #002
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [initialQuestion, setInitialQuestion] = useState(null); // Stores the first question object

    /**
     * Handles the submission of input data to start the mock interview sequence by calling FastAPI.
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!resumeContent || !jobDescription || !targetRole) {
            setError("Please fill all fields before starting the simulation.");
            setInitialQuestion(null); // Clear potential previous results on validation failure
            return;
        }

        setIsLoading(true);
        setError(null);
        setInitialQuestion(null); // Clear loading/previous content

        const payload = { 
            resume_text: resumeContent, 
            job_description: jobDescription, 
            target_role: targetRole 
        };

        try {
            // CORE IMPLEMENTATION CHANGE: Calling the service layer abstraction.
            console.log("Attempting to start interview via service layer...");
            const data = await startInterview(payload);
            
            // The API returns a list of questions; we take the first one.
            if (Array.isArray(data) && data[0]) {
                setInitialQuestion(data[0]); 
            } else {
                 setError("API returned successfully but no question list was found.");
            }

        } catch (err) {
            console.error("Submission Error:", err);
            // Display user-friendly connection error
            const displayError = `Unable to connect to interview service. ${typeof window !== 'undefined' ? new Error(err).message : err}`;
            setError(displayError);
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
                <div className="">
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
                </div >

                {/* 2. Job Description */}
                <div className="">
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
                <div className="">
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
                </div >

                {/* Submission Button Area */}
                <div className="pt-4">
                    <button 
                        type="submit"
                        className={`w-full py-4 px-6 text-xl font-bold rounded-lg shadow-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200 ${isLoading ? 'bg-blue-300 cursor-not-allowed' : 'hover:bg-blue-800'} text-white`}
                        disabled={!resumeContent || !jobDescription || isLoading}
                    >
                        {/* Reusing the LoadingSpinner component logic for accurate display */}
                        {isLoading ? (
                            <div className="flex items-center justify-center space-x-2">
                                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path fill="currentColor" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12s12-6.627 12-12S18.627 0 12 0z"></path></svg>
                                <span className="text-lg">Connecting to Interview Service...</span>
                            </div >
                        ) : (
                            "Start 🚀 Mock Interview Simulation"
                        )}
                    </button>

                    {/* Error Display Area */}
                    {error && (
                        <div role="alert" className="mt-4 p-3 bg-red-100 text-red-700 border-l-4 border-red-500 rounded">
                            <strong className="font-bold block mb-2 text-lg">⚡ Submission Error:</strong > {error}
                        </div >
                    )}
                </div >
            </form>

            {/* Initial Question Card / Output Display Area */}
            {initialQuestion && (
                <div className="mt-16 pt-8 border-t-4 border-gray-200">
                    <h2 className="text-3xl font-extrabold text-green-800 mb-4 flex items-center">
                        ✅ Simulation Started! Focus Question #1:
                    </h2>
                    <div className="bg-green-50 p-8 border-l-8 border-green-500 bg-white shadow-2xl rounded-lg transition duration-300 transform hover:shadow-xl">
                        <h3 className="text-2xl font-bold text-gray-900 mb-4">{initialQuestion.question_text}</h3>
                        <div className="mt-6 p-5 bg-green-100 border border-green-300 rounded-lg">
                            <h3 className="font-bold text-xl text-green-800 mb-2 flex items-center">
                                <span className="text-2xl mr-2">💡</span> Coach's Focus Guidance:
                            </h3>
                            <p className='text-md'>**Framework Required:** {initialQuestion.suggested_framework}</p>
                        </div>
                        <div className="mt-6 text-sm space-y-2 p-3 bg-gray-50 rounded border">
                            <h4 className='font-semibold text-gray-700'>Areas to Prepare For (Follow-Up Prompts):</h4>
                            <ul className='list-disc list-inside ml-4'>
                                {initialQuestion.follow_up_prompt.map((item, index) => (
                                    <li key={index} className="text-gray-700">{item}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div >
            )} {/* End Initial Question Card */}

        </div >
    );
};

export default OnboardingPage;