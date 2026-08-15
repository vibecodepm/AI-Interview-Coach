// /Desktop/Hermes Projects/AI-Interview-Coach/src/components/Landing/HeroSection.jsx

import React from 'react';

/**
 * HeroSection: Polished SaaS component providing the main landing page branding and value proposition 
 * for an AI Product Management Interview Coach. This section aims to communicate high technical rigor 
 * and professional polish immediately upon load.
 */
const HeroSection = () => {
    return (
        <div className="min-h-[60vh] flex items-center bg-gray-50 border-b border-slate-100 py-20 md:py-32">
            <div className="container mx-auto px-4 max-w-7xl text-center lg:text-left">
                {/* 1. Headline - Strong and technical */}
                <h1 className="text-6xl sm:text-7xl lg:text-[3.5rem] font-extrabold tracking-tighter mb-4 leading-tight">
                    Interview Performance <span className='text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-700'>Engine</span>.
                </h1>
                {/* 2. Value Proposition Subtitle */}
                <p className="mt-4 text-xl md:text-3xl lg:text-3xl text-gray-600 max-w-4xl mb-12">
                    Achieve job readiness through objective, fully structured mock interviews that score you on metrics. Say goodbye to subjective preparation.
                </p>

                {/* 3. Visual Hierarchy / Key Differentiators */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-5xl mx-auto pt-6">

    {/* Improvement Card 1 - Rigor Focus */}
    <div className="p-6 bg-white border-b-4 border-indigo-500 rounded-xl shadow-xl transition duration-300 hover:scale-[1.02] flex flex-col items-center">
        <div className="text-4xl mb-3">🎯</div>
        <h3 className="text-xl font-bold text-gray-900 mb-1">
            Metrics-Driven Scoring
        </h3>
        <p className="text-sm text-gray-500 mt-2">
            Scores generated based on Relevance, Specificity in [0, 5], and documented Business Impact.
        </p>
    </div>

    {/* Improvement Card 2 - Workflow Focus */}
    <div className="p-6 bg-white border-b-4 border-blue-500 rounded-xl shadow-xl transition duration-300 hover:scale-[1.02] flex flex-col items-center">
        <div className="text-4xl mb-3">⚡</div>
        <h3 className="text-xl font-bold text-gray-900 mb-1">
            AI Feedback & Rewrite
        </h3>
        <p className="text-sm text-gray-500 mt-2">
            Receive both a structured critique and an expert-refactored, better answer immediately.
        </p>
    </div>

    {/* Improvement Card 3 - Data Focus */}
    <div className="p-6 bg-white border-b-4 border-green-500 rounded-xl shadow-xl transition duration-300 hover:scale-[1.02] flex flex-col items-center">
        <div className="text-4xl mb-3">📋</div>
        <h3 className="text-xl font-bold text-gray-900 mb-1">
            Resume Context Grounding
        </h3>
        <p className="text-sm text-gray-500 mt-2">
            All questions are grounded in your resume content, ensuring hyper-personalized evaluation.
        </p>
    </div>

</div>
            </div >
        </div>
    );
};

export default HeroSection;