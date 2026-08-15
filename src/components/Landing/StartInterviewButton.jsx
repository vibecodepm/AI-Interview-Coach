// /Desktop/Hermes Projects/AI-Interview-Coach/src/components/Landing/StartInterviewButton.jsx

import React from 'react';

/**
 * StartInterviewButton: Primary Call-to-Action button that manages loading and disability states.
 * @param {object} props
 * @param {boolean} props.loading - If true, shows spinner and disables further clicks.
 * @param {function} props.onClickHandler - The callback function to execute when clicked.
 * @param {boolean} props.disabled - Controlled disabling state passed from the parent component.
 */
const StartInterviewButton = ({ loading, onClickHandler, disabled }) => {

    // Use a standard React useCallback pattern for optimization, even if simplified here.
    const handleClick = React.useCallback(() => {
        if (!disabled && !loading) {
            onClickHandler();
        }
    }, [disabled, loading, onClickHandler]);

    return (
        <button
            onClick={handleClick}
            disabled={disabled || loading}
            className={`w-full py-4 px-6 text-xl font-bold rounded-lg transition duration-300 shadow-2xl 
                        ${disabled ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 
                         loading ? 'animate-pulse bg-blue-100 border-4 border-blue-500 text-blue-700 cursor-wait' : 
                         'bg-gradient-to-r from-indigo-600 to-blue-700 hover:shadow-xl shadow-lg transform hover:scale-[1.01]'}
                        disabled:cursor-not-allowed`}
            aria-label={loading ? 'Processing Interview' : (disabled ? `Cannot start interview.` : 'Start Mock Interview')}
        >
            {loading ? (
                <div className="flex items-center justify-center">
                    {/* Standard animated spinner pattern */}
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-80" d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 16a6 6 0 110-12 6 6 0 010 12z" fill="currentColor"></path>
                    </svg>
                    Assessing Readiness...
                </div>
            ) : (
                `Start Mock Interview`
            )}
        </button>
    );
};

export default StartInterviewButton;