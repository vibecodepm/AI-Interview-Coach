
import React from 'react';

/**
 * ResumeUpload: Manages resume content input, supporting both file drag/drop simulation and direct text paste.
 * It communicates its state changes back to the parent component via props.
 */
const ResumeUpload = ({ resume, setResume, error }) => {
    // Handler for manual text input change (the functional equivalent of pasting)
    const handleContentChange = (e) => {
        setResume(e.target.value);
    };

    /**
     * Simulates the logic for dropping content into the area (UI only).
     */
    /* eslint-disable no-console */
    const handleDrop = (e) => {
        e.preventDefault();
        // In a real app, we'd read files here and extract text via OCR/PDF parsing service. 
        console.log("Simulated file drop detected. Waiting for manual content update.");
        alert("File dropped successfully! Please paste the extracted raw text into the box below to simulate final data entry.");
    };

    return (
        <div className="col-span-full lg:col-span-2">
            <label htmlFor="resume" className="block text-xl font-bold text-gray-800 mb-3 flex items-start border-l-4 border-blue-500 pl-3 pt-1">
                <span role="img" aria-label="document">📄</span> 
                <span>1. Professional History (Source Material)</span>
            </label>
             {/* Dropzone Area */}
             <div 
                className={`border-2 ${error ? 'border-red-500 bg-red-50/70' : 'border-gray-300 bg-white'} rounded-xl p-6 transition duration-150 cursor-pointer flex-col gap-4`}
                onDragOver={(e) => e.preventDefault()} // Required for drag visualization
                onDrop={handleDrop} 
            >
                <p className="text-sm text-gray-600">🚀 Drag & Drop Resume PDF/DOCX here, or paste raw text manually.</p>
                {/* Textarea for manual input */}
                <textarea
                    id="resume"
                    rows="8"
                    className={`w-full p-3 text-base border ${error ? 'border-red-300' : 'border-gray-200'} rounded-lg focus:ring-blue-500 transition duration-150 resize-y`}
                    placeholder={resume ? "" : "Paste the full, raw text of your resume here..."}
                    value={resume}
                    onChange={handleContentChange}
                />
            </div >
        </div>
    );
};

export default ResumeUpload;