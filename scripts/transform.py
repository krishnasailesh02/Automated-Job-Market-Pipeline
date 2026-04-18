import json
import os
import datetime
import pandas as pd
from sqlalchemy import create_engine
import random

# --- 🛡️ DATA QUALITY TESTING FRAMEWORK ---
def run_data_quality_checks(df):
    print("Running strict Data Quality Checks...")
    errors = 0
    
    # Check 1: No null job titles
    if df['title'].isnull().any():
        print("[FAIL] Found null job titles!")
        errors += 1
        
    # Check 2: Salaries must be positive
    if (df['salary_min'] < 0).any() or (df['salary_max'] < 0).any():
        print("[FAIL] Found negative salaries!")
        errors += 1
        
    # Check 3: Max salary >= Min salary
    if (df['salary_max'] < df['salary_min']).any():
        print("[FAIL] Found max salary lower than min salary!")
        errors += 1
        
    if errors > 0:
        raise ValueError(f"Data Quality Validation Failed with {errors} errors. Pipeline halted.")
    print("[PASS] All Data Quality Checks passed cleanly!")

# --- 🧠 NLP SKILL EXTRACTION ---
def extract_skills(title):
    title = title.lower()
    skills = []
    
    # Keyword extraction logic mimicking basic NLP
    if "data" in title: skills.extend(["SQL", "Python", "Tableau", "Snowflake"])
    if "engineer" in title: skills.extend(["AWS", "Docker", "Kubernetes", "Airflow"])
    if "scientist" in title: skills.extend(["Machine Learning", "Pandas", "TensorFlow", "Databricks"])
    if "cloud" in title: skills.extend(["AWS", "Azure", "Terraform", "CI/CD"])
    if "analytics" in title: skills.extend(["Excel", "Power BI", "SQL", "Looker"])
    
    if not skills:
        skills = random.sample(["Agile", "Jira", "Communication", "Git", "REST APIs"], 3)
        
    # Pick top 3 skills to keep it clean
    selected_skills = random.sample(skills, min(3, len(skills)))
    return ", ".join(list(set(selected_skills)))

def transform_and_load():
    print("Starting transformation and load...")
    raw_dir = "./data/raw"
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    file_path = f"{raw_dir}/jobs_{date_str}.json"
    
    if not os.path.exists(file_path):
        print(f"No raw data found at {file_path}")
        return
        
    with open(file_path, "r") as f:
        data = json.load(f)
        
    if not data:
        print("No data to transform.")
        return
        
    df = pd.DataFrame(data)
    
    # Transformation
    df['avg_salary'] = (df['salary_min'] + df['salary_max']) / 2
    
    def parse_location(loc):
        parts = [p.strip() for p in loc.split(',')]
        if len(parts) == 3: return pd.Series([parts[0], parts[1], parts[2]])
        return pd.Series(["Unknown", "Unknown", "Unknown"])
        
    df[['city', 'state', 'country']] = df['location'].apply(parse_location)
    df.loc[df['country'] == 'Remote', 'country'] = 'Worldwide'
    df['is_remote'] = df['remote_allowed'].apply(lambda x: True if x == "Yes" else False)
    
    # 🧠 Apply NLP Skill Extraction
    print("Applying NLP Skill Extraction to Job Titles...")
    df['key_skills'] = df['title'].apply(extract_skills)
    
    # 🛡️ Run Quality Checks
    run_data_quality_checks(df)
    
    # Reorder columns and include key_skills
    original_cols = ['id', 'title', 'company', 'location', 'salary_min', 'salary_max', 'posted_date', 'avg_salary', 'is_remote']
    new_cols = ['industry', 'experience_level', 'job_type', 'remote_allowed', 'city', 'state', 'country', 'key_skills']
    df = df[original_cols + new_cols]
    
    # Load to DB
    engine = create_engine('sqlite:///job_market.db')
    df.to_sql('stg_jobs', engine, if_exists='replace', index=False)
    print(f"Loaded {len(df)} enriched rows into SQLite database table 'stg_jobs'.")

if __name__ == "__main__":
    transform_and_load()
