CREATE TABLE customers (
    customer_id VARCHAR(255),
    customer_name VARCHAR(255),
    segment VARCHAR(255)
);

CREATE TABLE orders (
    order_id VARCHAR(255),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(255),
    customer_id VARCHAR(255)
);

CREATE TABLE products (
    product_id VARCHAR(255),
    product_name VARCHAR(255),
    category VARCHAR(255),
    sub_category VARCHAR(255)
);