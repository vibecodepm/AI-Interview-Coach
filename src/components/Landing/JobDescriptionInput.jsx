
import React from 'react';

/**
 * JobDescriptionInput: Dedicated component for handling the job description text input.
 * Includes advanced feedback like character counting for better user guidance.
 * @param {string} jobDescription - The current value of the JD textarea.
 * @param {(text: string) => void} setJobDescription - Function to update parent state.
 * @param {string | null} error - Error message to display (e.g., validation failure).
 */
const JobDescriptionInput = ({ jobDescription, setJobDescription, error }) => {

    // Calculate character count for user feedback
    const charCount = jobDescription ? jobDescription.trim().length : 0;
    const maxLength = 15000; // Using the API's assumed limit as a guide for best practice

    const handleChange = (e) => {
        setJobDescription(e.target.value);
    };

    return (
        <div className="col-span-full lg:col-span-2">
            <label htmlFor="jd" className="block text-xl font-bold text-gray-800 mb-3 flex items-start border-l-4 border-blue-500 pl-3 pt-1">
                <span role="img" aria-label="document">📄</span> 
                <span>2. Target Job Description (Domain Context)</span>
            </label>
             <div className={`border-2 ${error ? 'border-red-500 bg-red-50/70' : 'border-gray-300 bg-white'} rounded-xl p-6 transition duration-150 flex-col gap-4`}>
                {/* Textarea Input */}
                <textarea
                    id="jd"
                    rows="7"
                    className={`w-full p-3 text-base border ${error ? 'border-red-300' : 'border-gray-200'} rounded-lg focus:ring-blue-500 transition duration-150 resize-y`}
                    placeholder={jobDescription ? "" : "Paste the entire job posting here... Needs full company/role background."}
                    value={jobDescription}
                    onChange={handleChange}
                />
                 {/* Validation Error Display */}
                {error && (
                    <div role="alert" className="p-3 bg-red-100 text-red-700 border-l-4 border-red-500 rounded">
                        <strong className="font-bold block mb-1">🚨 Input Error:</strong> {error}
                    </div>
                )}

                {/* Character Counter */}
                 <div className="flex justify-between text-sm text-gray-500 pt-2 border-t mt-4">
                    <span>Character Count: <strong className="text-gray-800">{charCount.toLocaleString()}</strong></span>
                    <span>Max Recommended Input (API Limit): {maxLength.toLocaleString()}</span>
                </div>

            </div >
        </div>
    );
};

export default JobDescriptionInput;