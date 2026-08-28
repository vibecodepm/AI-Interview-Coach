
import React from 'react';

/**
 * RoleSelector: Manages the selection of target role, providing an accurate dropdown UI.
 * Props expected: { role, setRole }.
 */
const RoleSelector = ({ role, setRole }) => {
    const rolesArray = [
        { value: "PM", label: "Product Manager (Generalist PM)" },
        { value: "APM", label: "Associate Product Manager (Early Career Focus)" },
        { value: "AI PM", label: "AI Product Manager (ML Ops & LLM Guardrails)" },
        { value: "SPM", label: "Senior Product Manager (GPM/Domain Lead)" },
    ];

    const handleRoleChange = (event) => {
        setRole(event.target.value);
    };

    return (
        <div className="col-span-full lg:col-span-2">
            <label htmlFor="role" className="block text-xl font-bold text-gray-800 mb-3 flex items-start border-l-4 border-blue-500 pl-3 pt-1">
                <span role="img" aria-label="select role">👥</span> 
                <span>3. Select Target Persona / Consulting Focus</span>
            </label>
             <div className="relative">
                <select 
                    id="role"
                    value={role} 
                    onChange={handleRoleChange} 
                    className="w-full p-4 text-lg border-2 border-gray-200 rounded-xl appearance-none focus:ring-blue-500 focus:border-blue-500 transition duration-150 bg-white cursor-pointer"
                >
                    <option value="" disabled className="text-gray-500">-- Select your role to configure interview deep-dive --</option>
                    {rolesArray.map((roleItem) => (
                        <option key={roleItem.value} value={roleItem.value}>{roleItem.label}</option>
                    ))}
                </select>
                 {/* Custom indicator for better UX */}
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 pointer-events-none">
                    <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.917L15.892 6.212l-6.603 6.603z"/></svg>
                </div >
            </div>
        </div >
    );
};

export default RoleSelector;