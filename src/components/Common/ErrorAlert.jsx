import React from 'react';

const ErrorAlert = ({ message }) => {
    if (!message) return null;

    return (
        <div
            role="alert"
            className="mb-4 rounded-lg border border-red-300 bg-red-50 p-4 text-red-700"
        >
            <div className="font-semibold">Something went wrong</div>
            <div className="mt-1 text-sm">{message}</div>
        </div>
    );
};

export default ErrorAlert;