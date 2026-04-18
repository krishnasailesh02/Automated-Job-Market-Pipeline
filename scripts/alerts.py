import pandas as pd
from sqlalchemy import create_engine

def check_and_alert():
    print("Checking for alerts...")
    engine = create_engine('sqlite:///job_market.db')
    
    try:
        df = pd.read_sql('SELECT * FROM stg_jobs', engine)
    except Exception as e:
        print("Could not read from database:", e)
        return
        
    if df.empty:
        print("No data found in database. Alerting!")
        print("[ALERT] Pipeline succeeded but no jobs were ingested.")
        return
        
    avg_salary_overall = df['avg_salary'].mean()
    print(f"Current overall average salary: ${avg_salary_overall:,.2f}")
    
    if avg_salary_overall < 100000:
        print("[ALERT] Average market salary has dropped below $100,000!")
    else:
        print("Metrics look normal. No alerts triggered.")

if __name__ == "__main__":
    check_and_alert()
