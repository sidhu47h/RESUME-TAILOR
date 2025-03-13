import React, { useState } from 'react';
import './App.css'; // Ensure you have some basic styles
import MockData from './MockData';


function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const res = await fetch('https://resume-tailor-backend.vercel.app/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ description: jobDescription }), // This handles escaping
            });
            const data = await res.json();
      // For testing, we're using mock data. Replace with your API call as needed.
    //   const data = MockData;
      setResponse(data); // Adjust based on your response structure
    } catch (error) {
      console.error('Error:', error);
    }
  };

//   const generatePDF = async () => {
//     if (!response?.latex) return;
  
//     // Start with the raw LaTeX content from the response.
//     let latexContent = response.latex;
  
//     // Remove problematic package imports.
//     const packagesToRemove = [
//       'fullpage',
//       'titlesec',
//       'enumitem',
//       'fancyhdr',
//       'babel',
//       'tabularx',
//       'fontawesome5'
//     ];
//     packagesToRemove.forEach(pkg => {
//       const regex = new RegExp(`\\\\usepackage(?:\\[[^\\]]*\\])?\\{[^}]*${pkg}[^}]*\\}`, 'g');
//       latexContent = latexContent.replace(regex, '');
//     });
//     // Remove problematic length definitions.
//     latexContent = latexContent.replace(/\\setlength\{\\multicolsep\}\{[^}]*\}/g, '');
  
//     // If the LaTeX does not include a document class, wrap it in a minimal document.
//     if (!/\\documentclass/.test(latexContent)) {
//       latexContent = `\\documentclass{article}
//   \\usepackage[utf8]{inputenc}
//   \\begin{document}
//   ${latexContent.trim()}
//   \\end{document}`;
//     }
  
//     console.log('Cleaned & Wrapped LaTeX Content:', latexContent);
  
//     try {
//       // Convert the (now wrapped) LaTeX into HTML using latex.js.
//       const generator = new latex.HtmlGenerator({ hyphenate: false });
//       latex.parse(latexContent, { generator });
//       const htmlFragment = generator.documentFragment();
  
//       // Create an off-screen container to render the HTML.
//       const container = document.createElement('div');
//       container.style.position = 'absolute';
//       container.style.left = '-9999px';
//       container.appendChild(htmlFragment);
//       document.body.appendChild(container);
  
//       // Use html2canvas to capture the rendered HTML as an image.
//       const canvas = await html2canvas(container);
//       const imgData = canvas.toDataURL('image/png');
  
//       // Create a PDF using jsPDF.
//       const pdf = new jsPDF({
//         orientation: 'portrait',
//         unit: 'pt',
//         format: 'a4'
//       });
//       const pageWidth = pdf.internal.pageSize.getWidth();
//       const canvasWidth = canvas.width;
//       const canvasHeight = canvas.height;
//       const imgWidth = pageWidth;
//       const imgHeight = (canvasHeight * imgWidth) / canvasWidth;
  
//       pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
//       pdf.save('resume.pdf');
  
//       // Clean up the temporary container.
//       document.body.removeChild(container);
//     } catch (error) {
//       console.error('Error generating PDF:', error);
//     }
//   };
  
  
  
  

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
          {/* <div className="latex-header">
            <button 
              onClick={generatePDF}
              disabled={!response?.latex}
              className="generate-pdf-btn"
            >
              Generate PDF
            </button>
          </div> */}
          <pre className="latex-content">
            {response?.latex ? String(response.latex) : 'No LaTeX content yet'}
          </pre>
        </div>
      </div>
    </div>
  );
}

export default App;


// const res = await fetch('http://127.0.0.1:5000/generate-resume', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify({ description: jobDescription }), // This handles escaping
            // });
            // const data = await res.json();