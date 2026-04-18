import pandas as pd
from sqlalchemy import create_engine
import os

def export_to_csv():
    print("Exporting enriched data for Power BI...")
    
    engine = create_engine('sqlite:///job_market.db')
    
    try:
        df = pd.read_sql('SELECT * FROM stg_jobs', engine)
    except Exception as e:
        print("Could not read from database:", e)
        return
        
    if df.empty:
        print("No data to export.")
        return
        
    os.makedirs("./data/reporting", exist_ok=True)
    export_path = "./data/reporting/power_bi_feed.csv"
    
    df.to_csv(export_path, index=False)
    print(f"Data exported successfully to {export_path}")

if __name__ == "__main__":
    export_to_csv()
