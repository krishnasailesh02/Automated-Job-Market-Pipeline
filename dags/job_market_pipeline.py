from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime
import sys
import os

# Add scripts directory to path so we can import our modules
sys.path.insert(0, '/opt/airflow/scripts')

from extract import extract_jobs
from transform import transform_and_load
from alerts import check_and_alert

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime.datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

with DAG(
    'job_market_pipeline',
    default_args=default_args,
    description='A daily pipeline for job market intelligence',
    schedule_interval=datetime.timedelta(days=1),
    catchup=False,
) as dag:

    # Task 1: Extract
    t1_extract = PythonOperator(
        task_id='extract_jobs_data',
        python_callable=extract_jobs,
    )

    # Task 2: Transform & Load
    t2_transform_load = PythonOperator(
        task_id='transform_and_load_data',
        python_callable=transform_and_load,
    )
    
    # Task 3: Alerts
    t3_alerts = PythonOperator(
        task_id='check_alerts',
        python_callable=check_and_alert,
    )

    t1_extract >> t2_transform_load >> t3_alerts
