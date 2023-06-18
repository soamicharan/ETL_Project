"""
Operator functions for extracting CSV files.
"""
import pandas as pd
from pathlib import Path
from airflow.hooks.postgres_hook import PostgresHook

# Retail raw dataset files are store in data/retail/raw folder.
RAW_FILE_PATH_PREFIX = "data/retail/raw"

def extract_dataset(encoding: str = "ISO-8859-1", **context):
    # Load postgresql connection
    pg_hook = PostgresHook(postgres_conn_id='postgres_retail') 
    
    # Extract CSV file names which are already processed.
    processed_dataset_filenames = [row[0] for row in pg_hook.get_records("SELECT filename FROM processed_files")]

    # Extract all CSV file names exist in data/retail/raw folder.
    dataset_filenames = [file_path.stem for file_path in Path(RAW_FILE_PATH_PREFIX).glob('*.csv')]
    
    # Find out which files are not processed by subtracting set of all file exists in data/retail/raw folder from set of processed files.
    unprocessed_filenames = list(set(dataset_filenames) - set(processed_dataset_filenames))
    
    # Push unprocessed CSV file names in XCOM on key=unprocessed_file_names
    task_instance = context['task_instance']
    task_instance.xcom_push(key='unprocessed_file_names', value=unprocessed_filenames)