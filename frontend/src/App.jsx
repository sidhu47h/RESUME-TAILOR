import React, { useState } from 'react';
import './App.css'; // Ensure you have some basic styles
// import MockData  from './MockData';

function App() {
    const [jobDescription, setJobDescription] = useState('');
    const [response, setResponse] = useState(null);

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
            
            // const data = MockData;
            setResponse(data); // Adjust based on your response structure
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="app-container">
            <div className="form-section">
                <h2>Job Description Form</h2>
                <form onSubmit={handleSubmit}>
                    <textarea
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        placeholder="Paste job description here..."
                        rows="10"
                    />
                    <button type="submit">Generate Resume</button>
                </form>
            </div>
            <div className="response-container">
                <div className="response-section">
                    <h2>JSON Response</h2>
                    <pre>{response?.json ? JSON.stringify(response.json, null, 2) : 'No response yet'}</pre>
                </div>
                <div className="response-section">
                    <h2>Raw LaTeX</h2>
                    <pre className="latex-content">{response?.latex ? String(response.latex) : 'No LaTeX content yet'}</pre>
                </div>
            </div>
        </div>
    );
}

export default App;