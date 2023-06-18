"""
Operator functions for loading cleaned CSV files.
"""
import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook

CLEANED_FILE_PATH_PREFIX = "data/retail/cleaned"

def load_dataset(**context):
    # Extract task_instance from provided context via airflow.
    task_instance = context['task_instance']
    
    # Extract unprocessed CSV file names from XCOM using key=unprocessed_file_names from task -> extract_dataset.
    dataset_file_names = task_instance.xcom_pull(task_ids='extract_dataset', key='unprocessed_file_names')
    
    # Get SQLAlchemy engine object from airflow postgresql connection.
    db_engine = PostgresHook(postgres_conn_id='postgres_retail').get_sqlalchemy_engine()
    
    # load each processed CSV files into database table.
    for filename in dataset_file_names:
        # Load processed CSV file into Pandas
        dataframe = pd.read_csv(f'{CLEANED_FILE_PATH_PREFIX}/{filename}.csv')
        
        # Using dataframe to_sql method to connect with database using sqlalchemy engine and load data in retail_sales table.
        dataframe.to_sql('retail_sales', con=db_engine, if_exists='append', index=False)
        
        # Insert processed file name in processed_files table to mark CSV file as processed.
        db_engine.execute("INSERT INTO processed_files (filename) VALUES (%(filename)s)", dict(filename=filename))