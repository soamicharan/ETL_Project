-- Create processed_files table to keep track of processed CSV file names.
-- It helps to avoid duplicate processing of CSV.
-- We maintain both raw and cleaned CSV files
CREATE TABLE IF NOT EXISTS processed_files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(100) NOT NULL,
    UNIQUE (filename)
);

-- Database table to load processed CSV retail data.
CREATE TABLE IF NOT EXISTS retail_sales (
    id SERIAL PRIMARY KEY,
    order_number INTEGER NOT NULL,
    quantity_ordered NUMERIC NOT NULL,
    price_each NUMERIC NOT NULL,
    order_line_number INTEGER NOT NULL,
    sales NUMERIC NOT NULL,
    order_date DATE,
    status INTEGER,
    qtr_id INTEGER,
    month_id INTEGER,
    year_id INTEGER,
    product_line INTEGER,
    msrp INTEGER,
    product_code INTEGER,
    deal_size INTEGER,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100)
)