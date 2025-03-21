from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import openai
import os
from dotenv import load_dotenv
from resume_stitcher import generate_latex  # Import the generate_latex function

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://resume-tailor-amber.vercel.app"}})
# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_resume_json():
    """Load the current resume from the JSON file."""
    with open("resume.json", "r", encoding="utf-8") as file:
        return json.load(file)

def create_prompt(resume, job_description):
    """
    Build a prompt that includes the current resume JSON and instructions.
    
    Follow these rules to tailor the resume for the job description:
    1. The contact information, education, awards, and achievements remain unchanged.
    2. In work experience, keep the company names, positions, and employment periods the same.
    3. Update only the responsibilities in work experience to be ATS-friendly using keywords from the job description.
    4. Don't change the responsibilities of the work experience completely, just tailor them to be more relevant to the job description and add more points if needed.
    5. Ensure each job has at least 5 bullet points for responsibilities (Amazon should have 8–10).
    6. Tailor the 'about', 'skills', and 'projects' sections to align with the job requirements.
    7. In the 'skills' section, add any relevant skills and technologies from the job description that are not already present.
    8. For each job, update the "technologies" list to include any additional relevant technologies from the job description.
    9. Do not introduce any random jargon.
    
    IMPORTANT: Return ONLY the modified JSON object without any additional text.
    """
    prompt = f"""
You are an expert resume generator. Your task is to modify the following resume JSON:
{json.dumps(resume, indent=2)}

Follow these rules to tailor the resume for the job description:
1. The contact information, education, awards, and achievements must remain unchanged.
2. For the work experience section, keep the company names, positions, and employment periods as they are.
3. Update only the responsibilities in work experience, making them ATS-friendly by incorporating relevant keywords from the job description.
4. Don't change the responsibilities of the work experience completely, just tailor them to be more relevant to the job description and add more points if needed.
5. Ensure each job has at least 5 bullet points for responsibilities, and for the Amazon role, include at least 8 to 10 bullet points.
6. Additionally, adjust the 'about', 'skills', and 'projects' sections to align with the job requirements.
7. In the 'skills' section, add any relevant skills and technologies mentioned in the job description that are not already present. Merge them appropriately with the existing skills.
8. For each job in the "experience" section, update the "technologies" list to include any additional relevant technologies mentioned in the job description, while preserving the existing entries.
9. Do not introduce any random jargon; only refine the existing details.

IMPORTANT: Return ONLY the modified JSON object. Do not include any explanation or markdown formatting.

Job Description:
{job_description}

Remember: Return ONLY the JSON object, nothing else.
"""
    return prompt

@app.route('/')
def home():
    return "Welcome to the Resume Tailor API!"

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    # Extract job description from the POST request.
    data = request.get_json()
    job_description = data.get("description", "")
    
    if not job_description:
        return jsonify({"error": "Job description not provided."}), 400

    try:
        # Load the existing resume JSON.
        resume = load_resume_json()
    except Exception as e:
        return jsonify({"error": "Could not load resume.json", "message": str(e)}), 500

    # Create the prompt for ChatGPT.
    prompt = create_prompt(resume, job_description)

    try:
        # Call the OpenAI API with the constructed prompt.
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=4000
        )
    except Exception as e:
        return jsonify({"error": "Error calling OpenAI API", "message": str(e)}), 500

    tailored_resume_str = response['choices'][0]['message']['content'].strip()
    
    # Remove markdown code fences if present.
    if tailored_resume_str.startswith('```json'):
        tailored_resume_str = tailored_resume_str.replace('```json', '').replace('```', '').strip()
    
    try:
        # Parse the JSON response from ChatGPT
        tailored_resume = json.loads(tailored_resume_str)
        
        # Generate LaTeX using the resume_stitcher
        latex_resume = generate_latex(tailored_resume)
        print(latex_resume)
        
        # Return both JSON and LaTeX versions
        return jsonify({
            "json": tailored_resume,
            "latex": latex_resume
        })
    except json.JSONDecodeError as e:
        return jsonify({
            "error": "Invalid JSON output from OpenAI",
            "output": tailored_resume_str,
            "message": f"JSONDecodeError: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Error generating LaTeX",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
