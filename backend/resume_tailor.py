from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import json
import openai
import os
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow requests from your frontend

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Load the API key from the .env file

def load_resume_json():
    """Load the current resume from the JSON file."""
    with open("resume.json", "r") as file:
        return json.load(file)

def create_prompt(resume, job_description):
    """
    Build a prompt that includes the current resume JSON and instructions.
    
    Instructions:
    - The contact, education, awards, and achievements remain constant.
    - In work experience, the companies, titles, and durations remain the same.
    - Update the responsibilities to be ATS friendly and optimized using keywords
      from the job description. Use the existing responsibilities as a basis and
      tailor them without adding random jargon.
    - Tailor the 'about', 'skills', and 'projects' sections accordingly.
    - In the 'skills' section, add any relevant skills and technologies from the job description.
    - For each job in the experience section, update the "technologies" list to include any additional relevant technologies mentioned in the job description, while preserving the existing ones.
    - Return the final resume in the exact same JSON model.
    
    Please return the output as a valid JSON object without any additional text or explanations.
    """
    prompt = f"""
You are an expert resume generator. Your task is to modify the following resume JSON:
{json.dumps(resume, indent=2)}

Follow these rules to tailor the resume for the job description:
1. The contact information, education, awards, and achievements must remain unchanged.
2. For the work experience section, keep the company names, positions, and employment periods as they are.
3. Update only the responsibilities in work experience, making them ATS-friendly by incorporating relevant keywords from the job description.
4. Ensure each job has at least 5 bullet points for responsibilities, and for the Amazon role, include at least 8 to 10 bullet points.
5. Additionally, adjust the 'about', 'skills', and 'projects' sections to align with the job requirements.
6. In the 'skills' section, add any relevant skills and technologies mentioned in the job description that are not already present. Merge them appropriately with the existing skills.
7. For each job in the "experience" section, update the "technologies" list to include any additional relevant technologies mentioned in the job description, while preserving the existing entries.
8. Do not introduce any random jargon; only refine the existing details.

IMPORTANT: Return ONLY the modified JSON object. Do not include any explanation or markdown formatting.

Job Description:
{job_description}

Remember: Return ONLY the JSON object, nothing else.
"""
    return prompt


# def clean_json_response(response_str):
#     # Remove markdown code fences if present
#     if response_str.startswith("```"):
#         response_str = response_str.strip("`")
#     return response_str.strip()

# # Then in your endpoint, after getting the response:
# tailored_resume_str = response['choices'][0]['message']['content'].strip()
# tailored_resume_str = clean_json_response(tailored_resume_str)


@app.route('/')
def home():
    return "Welcome to the Resume Tailor API!"  # Or render a template if you have one

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    # Extract the job description from the POST request.
    data = request.get_json()
    job_description = data.get("description", "")
    
    if not job_description:
        return jsonify({"error": "Job description not provided."}), 400

    try:
        # Load the existing resume JSON
        resume = load_resume_json()
    except Exception as e:
        return jsonify({"error": "Could not load resume.json", "message": str(e)}), 500

    # Create the prompt for ChatGPT
    prompt = create_prompt(resume, job_description)

    try:
        # Call the OpenAI API with the constructed prompt
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=4000  # Increased from 1000 to 4000
        )
    except Exception as e:
        return jsonify({"error": "Error calling OpenAI API", "message": str(e)}), 500

    tailored_resume_str = response['choices'][0]['message']['content'].strip()
    
    # Clean up the response if it contains markdown formatting
    if tailored_resume_str.startswith('```json'):
        tailored_resume_str = tailored_resume_str.replace('```json', '').replace('```', '').strip()
    
    try:
        tailored_resume = json.loads(tailored_resume_str)
    except json.JSONDecodeError as e:
        return jsonify({
            "error": "Invalid JSON output from OpenAI",
            "output": tailored_resume_str,
            "message": f"JSONDecodeError: {str(e)}"
        }), 500

    # Return the tailored resume JSON as the response.
    return jsonify(tailored_resume)

if __name__ == "__main__":
    app.run(debug=True)
