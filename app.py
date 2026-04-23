from flask import Flask, render_template, request, jsonify     # javascript object notation
import PyPDF2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['resume']
    role = request.form['role'].lower().strip()

    # Extract Text From PDF
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    # convert to lowercase text
    resume_text = text.lower()

    # Job roles dictionary
    job_skills_input = {
    "frontend developer": {
        "mandatory": {
            "all": ["html", "css", "javascript"],
            "one_of": ["react", "angular", "vue"]
        },
        "core": ["responsive design", "api integration", "git", "state management"],
        "bonus": ["typescript", "next.js", "deployment"]
    },
    "data analyst": {
        "mandatory": {
            "all": ["sql", "excel", "statistics"],
            "one_of": ["python", "r"]
        },
        "core": ["pandas", "numpy", "data cleaning", "data visualization", "exploratory data analysis"],
        "bonus": ["power bi", "tableau", "a/b testing", "business intelligence"]
    },
    "backend developer": {
        "mandatory": {
            "all": ["sql", "rest api"],
            "one_of": ["python", "java", "node.js"]
        },
        "core": ["django", "flask", "spring boot", "express", "authentication", "database management"],
        "bonus": ["docker", "aws", "redis", "microservices", "ci/cd"]
    },
    "full stack developer": {
        "mandatory": {
            "all": ["html", "css", "javascript", "sql", "rest api"],
            "one_of": ["python", "java", "node.js", "react", "angular", "vue"]
        },
        "core": ["frontend framework", "backend framework", "authentication", "git", "database integration"],
        "bonus": ["docker", "aws", "deployment", "web security", "performance optimization"]
    },
    "machine learning engineer": {
        "mandatory": {
            "all": ["python", "machine learning", "linear algebra", "statistics"],
            "one_of": ["scikit-learn", "tensorflow", "pytorch"]
        },
        "core": ["pandas", "numpy", "data preprocessing", "model evaluation", "feature engineering"],
        "bonus": ["deep learning", "nlp", "computer vision", "mlops", "model deployment"]
    }
}
    if role not in job_skills_input:
        return jsonify({"error": "Role not available"}), 400

    selected_role = job_skills_input[role]

    # Mandatory check
    mandatory_all = selected_role["mandatory"]["all"]
    mandatory_one = selected_role["mandatory"]["one_of"]
    matched_all = [s for s in mandatory_all if s in resume_text]
    missing_all = [s for s in mandatory_all if s not in resume_text]
    matched_one = [s for s in mandatory_one if s in resume_text]
    all_match = len(missing_all) == 0
    one_match = len(matched_one) > 0

    # Core check
    core_skills = selected_role["core"]
    matched_core = [s for s in core_skills if s in resume_text]
    missing_core = [s for s in core_skills if s not in resume_text]
    core_percentage = round((len(matched_core) / len(core_skills)) * 100, 1)

    # Bonus check
    bonus_skills = selected_role["bonus"]
    matched_bonus = [s for s in bonus_skills if s in resume_text]
    missing_bonus = [s for s in bonus_skills if s not in resume_text]
    bonus_percentage = round((len(matched_bonus) / len(bonus_skills)) * 100, 1)

    # Score calculation
    if all_match and one_match:
        mandatory_score = 1.0
    elif all_match or one_match:
        mandatory_score = 0.5
    else:
        mandatory_score = 0.0

    overall = (mandatory_score * 0.5) + (core_percentage/100 * 0.3) + (bonus_percentage/100 * 0.2)
    score_percent = round(overall * 100, 1)

    if score_percent >= 75:
        verdict = "Highly Ready"
        verdict_msg = "You're an excellent candidate! Apply with confidence."
        verdict_color = "green"
    elif score_percent >= 50:
        verdict = "Fairly Prepared"
        verdict_msg = "Good base! Improve a few skills to stand out."
        verdict_color = "yellow"
    elif score_percent >= 30:
        verdict = "Needs Improvement"
        verdict_msg = "You're on right track but need more relevant skills."
        verdict_color = "orange"
    else:
        verdict = "Not Ready Yet"
        verdict_msg = "Focus on missing skills before applying."
        verdict_color = "red"

    return jsonify({
        "role": role.title(),
        "score": score_percent,
        "verdict": verdict,
        "verdict_msg": verdict_msg,
        "verdict_color": verdict_color,
        "mandatory": {
            "matched_all": matched_all,
            "missing_all": missing_all,
            "matched_one_of": matched_one,
            "required_one_of": mandatory_one,
            "all_match": all_match,
            "one_match": one_match
        },
        "core": {
            "matched": matched_core,
            "missing": missing_core,
            "percentage": core_percentage
        },
        "bonus": {
            "matched": matched_bonus,
            "missing": missing_bonus,
            "percentage": bonus_percentage
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
