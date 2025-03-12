import React, { useState } from 'react';
import './App.css'; // Ensure you have some basic styles

function App() {
    const [jobDescription, setJobDescription] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Call your backend API here
        try {
            const res = await fetch('http://127.0.0.1:5000/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ description: jobDescription }), // This handles escaping
            });
            const data = await res.json();
            setResponse(data); // Adjust based on your response structure
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="app-container" style={{ display: 'flex' }}>
            <div className="form-section" style={{ flex: 1, padding: '20px' }}>
                <h2>Job Description Form</h2>
                <form onSubmit={handleSubmit}>
                    <textarea
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        placeholder="Paste job description here..."
                        rows="10"
                        style={{ width: '100%' }}
                    />
                    <button type="submit">Submit</button>
                </form>
            </div>
            <div className="response-section" style={{ flex: 1, padding: '20px' }}>
                <h2>Response</h2>
                <pre>{JSON.stringify(response, null, 2)}</pre>
            </div>
        </div>
    );
}

export default App;