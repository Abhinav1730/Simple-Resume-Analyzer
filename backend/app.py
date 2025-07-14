from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import process_resume
from jsearch_api import get_job_matches
import pdfplumber  #to extract text from PDFs

app = Flask(__name__, static_url_path="/static")
CORS(app)


@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files["file"]
    resume_text = ""

    # Handle PDF files properly
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.stream) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
    else:
        # fallback for .txt or other plain text formats
        resume_text = file.read().decode("utf-8", errors="ignore")

    print("🔍 Extracted Resume Text:", resume_text[:300])

    skills, plot_path = process_resume(resume_text)
    jobs = get_job_matches(skills)

    print({"skills": skills, "plot": plot_path, "jobs": jobs})
    return jsonify({"skills": skills, "plot": plot_path, "jobs": jobs})


if __name__ == "__main__":
    app.run(debug=True)
