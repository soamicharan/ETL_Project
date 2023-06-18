import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator

from scripts.retail.extract_dataset import extract_dataset
from scripts.retail.transform_dataset import transform_dataset
from scripts.retail.load_dataset import load_dataset


# Default arguments for DAGs.
DEFAULT_ARGS = {
    "owner": "retail_user",     # One of airflow user name
    "start_date": airflow.utils.dates.days_ago(2),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

"""
Create a DAG named -> retail_etl_pipeline
Scheduled for run daily.
Tasks performes -
    Create tables for loading CSV processed data >> 
        Extract CSV file names need to process >>
            Load CSV file into Pandas and transform dataset >>
                Load processed data into Database Table
"""
with DAG(
    dag_id="retail_etl_pipeline",   
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    description="Retail Dataset ETL Pipeline",
    start_date=airflow.utils.dates.days_ago(1),
    catchup=False,
) as retail_dag:
    
    # Create tables for loading CSV data.
    create_tables = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="postgres_retail",
        sql="sql/create_tables.sql",
    )

    # Extract CSV file names need to process
    extraction = PythonOperator(
        task_id="extract_dataset",
        python_callable=extract_dataset,
        provide_context=True,
    )

    # Load CSV file into Pandas and transform dataset.
    transformation = PythonOperator(
        task_id="transform_dataset",
        python_callable=transform_dataset,
        provide_context=True,
    )

    # Load processed data into database table.
    load_dataset = PythonOperator(
        task_id="load_dataset",
        python_callable=load_dataset,
        provide_context=True,
    )
    
    # Upstream definition
    create_tables >> extraction >> transformation >> load_dataset
