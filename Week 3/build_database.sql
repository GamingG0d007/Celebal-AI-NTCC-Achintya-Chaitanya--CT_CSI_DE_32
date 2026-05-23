-- Create database if not exists
CREATE DATABASE IF NOT EXISTS superstore_db;
USE superstore_db;

-- Create superstore_raw table to hold the raw CSV data
CREATE TABLE superstore_raw (
    Row_ID INT,
    Order_ID VARCHAR(255),
    Order_Date DATE,
    Ship_Date DATE,
    Ship_Mode VARCHAR(255),
    Customer_ID VARCHAR(255),
    Customer_Name VARCHAR(255),
    Segment VARCHAR(255),
    Country VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(255),
    Postal_Code VARCHAR(255),
    Region VARCHAR(255),
    Product_ID VARCHAR(255),
    Category VARCHAR(255),
    Sub_Category VARCHAR(255),
    Product_Name VARCHAR(255),
    Sales DECIMAL(10,2),
    Quantity INT,
    Discount DECIMAL(10,2),
    Profit DECIMAL(10,2)
);

-- Load data from CSV file into superstore_raw
-- Make sure the CSV file is in the MySQL server's data directory or use a secure path
-- Adjust the file path as needed
LOAD DATA INFILE '/d/GamingG0d007/Studies/Amity/NTCC/2026/Celebal-AI-NTCC-Achintya-Chaitanya- CT_CSI_DE_32/Week 3/Superstore.csv'
INTO TABLE superstore_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Create customers table
CREATE TABLE customers (
    customer_id VARCHAR(255),
    customer_name VARCHAR(255),
    segment VARCHAR(255)
);

-- Insert distinct customers from superstore_raw
INSERT INTO customers (customer_id, customer_name, segment)
SELECT DISTINCT Customer_ID, Customer_Name, Segment
FROM superstore_raw;

-- Create orders table
CREATE TABLE orders (
    order_id VARCHAR(255),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(255),
    customer_id VARCHAR(255)
);

-- Insert distinct orders from superstore_raw
INSERT INTO orders (order_id, order_date, ship_date, ship_mode, customer_id)
SELECT DISTINCT Order_ID, Order_Date, Ship_Date, Ship_Mode, Customer_ID
FROM superstore_raw;

-- Create products table
CREATE TABLE products (
    product_id VARCHAR(255),
    product_name VARCHAR(255),
    category VARCHAR(255),
    sub_category VARCHAR(255)
);

-- Insert distinct products from superstore_raw
INSERT INTO products (product_id, product_name, category, sub_category)
SELECT DISTINCT Product_ID, Product_Name, Category, Sub_Category
FROM superstore_raw;

-- Additional queries as per the task list can be added here
-- For example, using subqueries, CTEs, window functions, etc.