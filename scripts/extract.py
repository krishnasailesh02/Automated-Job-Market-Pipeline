import json
import os
import random
import datetime

def extract_jobs():
    print("Starting enriched mock extraction for a beautiful dashboard...")
    job_titles = ["Data Engineer", "Data Scientist", "Software Engineer", "Machine Learning Engineer", "DevOps Engineer", "Analytics Engineer", "Cloud Architect"]
    companies = ["TechCorp", "DataSystems", "AI Innovations", "CloudNet", "FinTech Solutions", "GlobalBank", "HealthPlus", "EcoEnergy"]
    
    # Richer locations mapping for better geographic drill-downs in Power BI
    # Format: City, State/Region, Country
    locations = [
        "New York, NY, USA", 
        "San Francisco, CA, USA", 
        "Austin, TX, USA", 
        "Chicago, IL, USA",
        "London, ENG, UK", 
        "Manchester, ENG, UK",
        "Berlin, BE, Germany",
        "Munich, BY, Germany",
        "Toronto, ON, Canada",
        "Sydney, NSW, Australia",
        "Remote, Remote, Remote"
    ]
    
    experience_levels = ["Entry Level", "Mid Level", "Senior", "Executive"]
    job_types = ["Full-Time", "Contract", "Part-Time"]
    industries = ["Technology", "Finance", "Healthcare", "Energy", "Retail"]
    
    extracted_data = []
    # Generating a MASSIVE amount of data (500+ jobs) to make the dashboard look full and professional
    num_jobs = random.randint(450, 600) 
    
    for i in range(num_jobs):
        loc = random.choice(locations)
        salary_base = random.randint(60000, 150000)
        
        # Adjust salary based on experience
        exp = random.choice(experience_levels)
        if exp == "Senior": salary_base += 40000
        elif exp == "Executive": salary_base += 80000
        
        job = {
            "id": f"job_{datetime.datetime.now().strftime('%Y%m%d')}_{i}",
            "title": random.choice(job_titles),
            "company": random.choice(companies),
            "location": loc,
            "industry": random.choice(industries),
            "experience_level": exp,
            "job_type": random.choice(job_types),
            "salary_min": salary_base,
            "salary_max": salary_base + random.randint(20000, 50000),
            "posted_date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            "remote_allowed": "Yes" if "Remote" in loc else random.choice(["Yes", "No"])
        }
        extracted_data.append(job)
        
    os.makedirs("./data/raw", exist_ok=True)
    file_path = f"./data/raw/jobs_{datetime.datetime.now().strftime('%Y%m%d')}.json"
    
    with open(file_path, "w") as f:
        json.dump(extracted_data, f, indent=4)
        
    print(f"Extracted {num_jobs} highly detailed mock jobs and saved to {file_path}")
    return file_path

if __name__ == "__main__":
    extract_jobs()
