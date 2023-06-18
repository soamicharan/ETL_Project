"""
Operator functions for transforming CSV files.
"""
import pandas as pd
from sklearn import preprocessing

# Retail raw dataset files are store in data/retail/raw folder.
RAW_FILE_PATH_PREFIX = "data/retail/raw"

# Retail cleaned dataset files are store in data/retail/cleaned folder.
CLEANED_FILE_PATH_PREFIX = "data/retail/cleaned"

# List of columns in Dataframe need to drop
DROP_COLUMNS = [
    "PHONE",
    "ADDRESSLINE1",
    "ADDRESSLINE2",
    "POSTALCODE",
    "TERRITORY",
    "CONTACTLASTNAME",
    "CONTACTFIRSTNAME",
]

# Mapping of column old name and new name.
COLUMN_MAPPER = {
    "ORDERNUMBER": "order_number",
    "QUANTITYORDERED": "quantity_ordered",
    "PRICEEACH": "price_each",
    "ORDERLINENUMBER": "order_line_number",
    "SALES": "sales",
    "ORDERDATE": "order_date",
    "STATUS": "status",
    "QTR_ID": "qtr_id",
    "MONTH_ID": "month_id",
    "YEAR_ID": "year_id",
    "PRODUCTLINE": "product_line",
    "MSRP": "msrp",
    "PRODUCTCODE": "product_code",
    "CUSTOMERNAME": "customer_name",
    "CITY": "city",
    "STATE": "state",
    "COUNTRY": "country",
    "DEALSIZE": "deal_size",
}

# column names which holds categorical values.
CATEGORICAL_TRANSFORM_COLUMNS = [
    "status",
    "product_line",
    "product_code",
    "deal_size",
]

# column names on which if any NaN values are found then rows will be dropped.
STRICT_DROP_NA_COLUMNS = [
    "order_number",
    "quantity_ordered",
    "price_each",
    "order_line_number",
    "sales",
    "order_date",
    "status",
    "qtr_id",
    "month_id",
    "year_id",
    "product_line",
    "msrp",
    "product_code",
    "deal_size",
]

def transform_dataset(encoding="ISO-8859-1", **context):
    """
    Retail dataset CSV transformation operator function.
    Args:
        encoding (str, optional): _description_. Defaults to "ISO-8859-1".
    """
    # Extract task_instance from provided context via airflow.
    task_instance = context['task_instance']
    
    # Extract unprocessed CSV file names from XCOM using key=unprocessed_file_names from task -> extract_dataset.
    dataset_file_names = task_instance.xcom_pull(task_ids='extract_dataset', key='unprocessed_file_names')
    
    # Process each unprocessed CSV files.
    for filename in dataset_file_names:
        # Load CSV file into Pandas.
        dataframe = pd.read_csv(f'{RAW_FILE_PATH_PREFIX}/{filename}.csv', encoding=encoding)
        
        # Drop columns from dataframe.
        dataframe.drop(DROP_COLUMNS, axis=1, inplace=True)
        
        # Rename columns from dataframe.
        dataframe.rename(columns=COLUMN_MAPPER, inplace=True)
        
        # Drop NaN rows from specific subset of columns.
        dataframe.dropna(subset=STRICT_DROP_NA_COLUMNS, inplace=True)
        
        # Using LabelEncoder from scikit-learn to transform categorical values into integer.
        label_encoder = preprocessing.LabelEncoder()
        for categorical_column in CATEGORICAL_TRANSFORM_COLUMNS:
            dataframe[categorical_column] = label_encoder.fit_transform(
                dataframe[categorical_column]
            )
        
        # Storing cleaned CSV file in data/retail/cleaned folder.
        dataframe.to_csv(f'{CLEANED_FILE_PATH_PREFIX}/{filename}.csv', index=False)
