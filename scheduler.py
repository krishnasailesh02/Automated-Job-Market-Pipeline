import schedule
import time
import sys
import os

sys.path.insert(0, os.path.abspath('./scripts'))

from extract import extract_jobs
from transform import transform_and_load
from alerts import check_and_alert
from export_for_powerbi import export_to_csv
from cloud_backup import backup_to_s3

def run_pipeline():
    print("\n--- Starting Data Pipeline Run ---")
    extract_jobs()
    transform_and_load()
    check_and_alert()
    export_to_csv()
    backup_to_s3()
    print("--- Pipeline Run Completed ---\n")

if __name__ == "__main__":
    run_pipeline()
    schedule.every().day.at("08:00").do(run_pipeline)
    print("Scheduler is active. Waiting for the next scheduled run...")
    while True:
        schedule.run_pending()
        time.sleep(60)
