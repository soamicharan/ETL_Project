# ETL_Project
## Project structure

```
ETL_Project
├── dags  # folder contain project wise DAG files and SQL files.
│   └── retail  # folder contains Retail project multiple DAG files and SQL files.
│       ├── sql  # folder contains SQL files require for Retail project.
│       └── dag.py  # DAG script for retail project.
├── data  # folder contain project wise CSV (or any other kind) dataset files.
│   └── retail  # folder contains Retail project dataset files.
│       ├── cleaned  # folder contains processed dataset files.
│       └── raw  # folder contains raw dataset files.
├── logs  # This folder contains log files for airflow DAG executions.
├── plugins  # This folder contains plugins for airflow.
│   └── scripts  # folder contains project wise scripts required for operators.
│       └──retail  # folder contains scripts related to Retail project.
│           ├── extact_dataset.py  # contains python functions to extract CSV files.
│           ├── load_dataset.py   # contains python functions to load processed CSV files into database table.
│           └── transform_dataset.py  # contains python functions to transform/process raw CSV files.
├── .env  # Contains Environment variables to configure airflow (airflow DB, airflow admin user) and postgresql connection credentials.
├── docker-compose.yml  # Docker compose to run project in docker.
├── Dockerfile  # Dockerfile to create container for airflow to run.
└── requirements.txt  # Contains required python packages for this project.
```

## Configuration

Use `.env` file to configure environment.
Provide `POSTGRES_USER` , `POSTGRES_PASSWORD`, `POSTGRES_DB` and `POSTGRES_HOST` variable to run airflow locally.
This values are preconfigured for running in docker container.

Default Admin Username - `retail_user`
Default Admin Password - `retail_password`

## Prerequisites

- Require `docker` command to run project.

## Run Project

To start the project, run following command - 
```bash
sudo docker compose up
```
This will build Dockerfile image and download PostgreSQL image and start the project.
Airflow Web UI will available on `http://localhost:8080/`
Use Default admin username and password to login.

## Project Description

The dataset is picked from https://www.kaggle.com/datasets/kyanyoga/sample-sales-data 
Read about CSV dataset schema here - https://www.kaggle.com/datasets/kyanyoga/sample-sales-data 

### Data Source

- We are assuming that all unprocessed CSV dataset files are stored OR uploaded to `data/retail/raw` folder.
- We store OR uploaded processed CSV dataset file in `data/retail/cleaned` folder.
- We have 2 tables in a PostgreSQL database `retail_db`
    - `processed_files` - It contains raw CSV dataset file names which are processed successfully.
    - `retail_sales` - It contains processed CSV dataset data.

### Extraction Procedure Steps

1. Read all CSV dataset file names from `data/retail/raw` folder.
2. From `processed_files` database table to extract all dataset file names which are processed successfully.
3. Filter dataset file names which are not processed.
4. Send unprocessed dataset file names for transformation.

### Transformation Procedure Steps

1. Retrieve unprocessed dataset file names.
2. Load CSV file into Pandas Dataframe.
3. Drop `PHONE`, `ADDRESSLINE1`, `ADDRESSLINE2`, `POSTALCODE`, `TERRITORY`, `CONTACTLASTNAME`, `CONTACTFIRSTNAME` columns as part of processing dataset, these are not required.
4. Rename all Dataframe columns to database table column names. So this will helps to directly load dataframe data into database table.
5. Drop rows which have Null values in following columns - `order_number`, `quantity_ordered`, `price_each`, `order_line_number`, `sales`, `order_date`, `status`, `qtr_id`, `month_id`, `year_id`, `product_line`, `msrp`, `product_code`, `deal_size`
6. Transform the columns `status`, `product_line`, `product_code` and `deal_size`, which has categorical type values. Use Label Encoding method to transform categorical values into integer.
7. Store OR upload processed Pandas Dataframe as CSV in `data/retail/cleaned` folder with same file name.

### Dataset Loading Procedure Steps

1. Retrieve unprocessed dataset file names.
2. Load processed CSV file into Pandas Dataframe from `data/retail/cleaned` folder using same name.
3. Load CSV data into `retail_sales` database table.
4. Insert dataset file name into `processed_files` database table.