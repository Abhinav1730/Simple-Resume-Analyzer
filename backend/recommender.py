import os
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as pt

Skill_Keywords = [
    "python",
    "java",
    "javascript",
    "c++",
    "sql",
    "react",
    "next.js",
    "mongodb",
    "node",
    "pandas",
    "numpy",
    "machine learning",
    "artificial intelligence",
    "tensorflow",
    "tailwind",
    "bootstrap",
    "typescript",
    "flask",
    "django",
    "scikit-learn",
    "git",
    "communication",
    "teamwork",
]

JOB_DATA_CSV = os.path.join(os.path.dirname(__file__), "job_data.csv")


def extract_skills_from_text(resume_text):
    """Extract known skills from plain resume text"""

    resume_text = resume_text.lower()
    found = [skill for skill in Skill_Keywords if skill in resume_text]
    return list(set(found))


def process_resume(resume_text):
    print("🔍 Resume text received:\n", resume_text[:500])
    """Process resume text to extract skills, match with job roles,
    and generate a matplotlib bar chart"""

    extracted_skills = extract_skills_from_text(resume_text)
    df = pd.read_csv(JOB_DATA_CSV)

    match_results = []
    for _, row in df.iterrows():
        role = row["role"]
        required_skills = [skill.strip().lower() for skill in row["skills"].split(",")]
        match_count = list(set(extracted_skills) & set(required_skills))
        match_percent = (
            (len(match_count) / len(required_skills)) * 100 if required_skills else 0
        )
        match_results.append((role, round(match_percent, 2)))

    top_matches = sorted(match_results, key=lambda x: x[1], reverse=True)[:5]

    roles, score = zip(*top_matches)
    pt.figure(figsize=(8, 5))
    bars = pt.barh(roles, score, color="skyblue")
    pt.xlabel("Match %")
    pt.title("Top Jobs Matches Based on your Resume")
    pt.xlim(0, 100)
    pt.gca().invert_yaxis()
    for bar in bars:
        pt.text(
            bar.get_width() + 2, bar.get_y() + 0.25, f"{bar.get_width()}%", va="center"
        )

    plot_dir = os.path.join(os.path.dirname(__file__), "static", "plots")
    os.makedirs(plot_dir, exist_ok=True)
    plot_path = os.path.join(plot_dir, "job_match.png")
    pt.tight_layout()
    pt.savefig(plot_path)
    pt.close()

    return extracted_skills, "/static/plots/job_match.png"
