import os
import requests
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path=".env")


def clean_skills(skills):
    # Replace problematic skills and URL encoding of them
    return [quote_plus(skill.replace("c++", "cpp")) for skill in skills]


def get_job_matches(skills, max_jobs=5, pages_to_try=2):
    api_key = os.getenv("RAPID_API_KEY")
    headers = {"x-rapidapi-key": api_key, "x-rapidapi-host": "jsearch.p.rapidapi.com"}

    def fetch_jobs(query_skills, page):
        query = "+".join(query_skills)
        url = f"https://jsearch.p.rapidapi.com/search?query={query}&page={page}&num_pages=1"
        print("📡 Querying JSearch:", url)
        response = requests.get(url, headers=headers)
        print("🔢 Status Code:", response.status_code)
        print("📥 Raw Response:", response.text[:300])

        jobs = []
        if response.status_code == 200:
            data = response.json()
            for item in data.get("data", []):
                job = {
                    "title": item.get("job_title", "N/A"),
                    "company_name": item.get("employer_name", "N/A"),
                    "location": (item.get("job_city") or "Unknown")
                    + ", "
                    + (item.get("job_country") or "Unknown"),
                    "description": (item.get("job_description") or "")[:200] + "...",
                    "job_link": item.get("job_apply_link", "#"),
                }
                jobs.append(job)
        return jobs

    all_jobs = []
    skill_batches = [skills[i : i + 3] for i in range(0, len(skills), 3)]

    for batch in skill_batches:
        cleaned = clean_skills(batch)
        for page in range(1, pages_to_try + 1):
            jobs = fetch_jobs(cleaned, page)
            for job in jobs:
                if job not in all_jobs:
                    all_jobs.append(job)
            if len(all_jobs) >= max_jobs:
                return all_jobs[:max_jobs]  # early return if we got enough

    return all_jobs[:max_jobs]
