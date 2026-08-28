
import React from 'react';

/**
 * InterviewQuestionCard: Presents the structured feedback and follow-up questions after a mock interview answer.
 * This component is designed to render rich, contextual data (question, framework, score) beautifully.
 * @param {object} props
 * @param {{ title: string, rawText: string}} props.question - The core question asked by the AI.
 * @param {string} props.suggestedFramework - The conceptual model or framework required for a strong answer (e.g., HEART, CIRCLE).
 * @param {Array<{ text: string, level: 'Low' | 'Medium' | 'Hard', score?: number}>} props.followUpQuestions - List of follow-ups with suggested difficulty levels.
 */
const InterviewQuestionCard = ({ question, suggestedFramework, followUpQuestions }) => {
    const normalizedFollowUpQuestions =
        followUpQuestions ||
        question?.follow_up_prompt?.map((text) => ({
            text,
            level: 'Medium'
        })) ||
        [];
    // Helper component for Follow-up Questions to keep the main card clean (optional refactoring)
    const FollowUpList = () => (
        <div className="mt-4 border-t pt-4">
            <h4 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
                🔍 Related Areas of Depth:
            </h4>
             {normalizedFollowUpQuestions.length > 0 ? (
                 <ul className="space-y-2">
                     {normalizedFollowUpQuestions.map((fq, index) => (
                         <li key={index} className={`p-3 rounded-lg bg-gray-50 shadow-sm text-sm ${
                            fq.level === 'Hard' ? 'border-l-4 border-red-400' : 
                            fq.level === 'Medium' ? 'border-l-2 border-yellow-400' : 
                            'border-l-1 border-green-400'
                         }`}>
                             <span className={`font-bold mr-2 ${fq.level === 'Hard' ? 'text-red-700' : fq.level === 'Medium' ? 'text-yellow-800' : 'text-green-800'}`}>[{fq.level}]</span>
                             {fq.text}
                         </li>
                     ))}
                 </ul>
             ) : (
                <p className="text-sm text-gray-500">No specific follow-up areas detected for this query.</p>
            )}
        </div>
    );

    return (
        <div className="bg-white border border-indigo-200 p-6 md:p-8 rounded-xl shadow-2xl max-w-4xl w-full">
            {/* 1. Core Question Presentation */}
            <h3 className="text-2xl font-extrabold text-gray-900 mb-2 border-b pb-2 flex items-center">
                <svg className="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a4 4 0 01-4-4V7a4 4 0 014-4 4 4m0 0V3" /></svg>
                Question: {question.title}
            </h3>
            

            {/* 2. Suggested Framework (High Rigor Area) */}
            {suggestedFramework && (
                <div className="mb-8 p-4 bg-indigo-50 border-l-4 border-indigo-500 shadow rounded-md">
                    <h4 className="text-lg font-bold text-indigo-800 flex items-center mb-1">
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Required Framework: {suggestedFramework}
                    </h4>
                    <p className="text-sm text-indigo-700 mt-1">
                        To score highly, structure your answer using this model.
                    </p>
                </div>
            )}

            {/* 3. Follow-up Questions */}
            <FollowUpList />
        </div>
    );
};

export default InterviewQuestionCard;