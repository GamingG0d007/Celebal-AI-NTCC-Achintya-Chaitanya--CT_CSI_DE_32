-- ==========================================================
-- 1. Create Database and Tables (Schema)
-- ==========================================================

-- Create the database (adjust name if needed)
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- ------------------------------------------------------------
-- Table: customers
-- ------------------------------------------------------------
CREATE TABLE customers (
    customer_id   INT           PRIMARY KEY,
    first_name    VARCHAR(50)   NOT NULL,
    last_name     VARCHAR(50)   NOT NULL,
    email         VARCHAR(100)  UNIQUE NOT NULL,
    city          VARCHAR(50)   NOT NULL,
    state         VARCHAR(50)   NOT NULL,
    join_date     DATE          NOT NULL,
    is_premium    TINYINT(1)    DEFAULT FALSE
);

-- Indexes for customers
CREATE INDEX idx_customers_city   ON customers(city);
CREATE INDEX idx_customers_state  ON customers(state);


-- ------------------------------------------------------------
-- Table: products
-- ------------------------------------------------------------
CREATE TABLE products (
    product_id    INT           PRIMARY KEY,
    product_name  VARCHAR(100)  NOT NULL,
    category      VARCHAR(50)   NOT NULL,
    brand         VARCHAR(50)   NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    stock_qty     INT           NOT NULL DEFAULT 0 CHECK (stock_qty >= 0)
);

-- Index for products
CREATE INDEX idx_products_category ON products(category);


-- ------------------------------------------------------------
-- Table: orders
-- ------------------------------------------------------------
CREATE TABLE orders (
    order_id      INT           PRIMARY KEY,
    customer_id   INT           NOT NULL,
    order_date    DATE          NOT NULL,
    status        VARCHAR(20)   NOT NULL DEFAULT 'Pending'
                    CHECK (status IN ('Pending','Shipped','Delivered','Cancelled')),
    total_amount  DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Indexes for orders
CREATE INDEX idx_orders_date    ON orders(order_date);
CREATE INDEX idx_orders_status  ON orders(status);


-- ------------------------------------------------------------
-- Table: order_items
-- ------------------------------------------------------------
CREATE TABLE order_items (
    item_id       INT           PRIMARY KEY,
    order_id      INT           NOT NULL,
    product_id    INT           NOT NULL,
    quantity      INT           NOT NULL CHECK (quantity > 0),
    unit_price    DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    discount_pct  DECIMAL(5,2)  DEFAULT 0 CHECK (discount_pct BETWEEN 0 AND 100),

    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ------------------------------------------------------------
-- 2. Insert Sample Data
-- ------------------------------------------------------------

-- Insert customers
INSERT INTO customers VALUES
(101, 'Aarav',  'Sharma', 'aarav.s@email.com',  'Mumbai',    'Maharashtra', '2024-01-15', TRUE),
(102, 'Priya',  'Patel',  'priya.p@email.com',  'Ahmedabad', 'Gujarat',     '2024-02-20', FALSE),
(103, 'Rohan',  'Gupta',  'rohan.g@email.com',  'Delhi',     'Delhi',       '2024-03-10', TRUE),
(104, 'Sneha',  'Reddy',  'sneha.r@email.com',  'Hyderabad', 'Telangana',   '2024-04-05', FALSE),
(105, 'Vikram', 'Singh',  'vikram.s@email.com', 'Jaipur',    'Rajasthan',   '2024-05-12', TRUE),
(106, 'Ananya', 'Iyer',   'ananya.i@email.com', 'Chennai',   'Tamil Nadu',  '2024-06-18', FALSE),
(107, 'Karan',  'Mehta',  'karan.m@email.com',  'Pune',      'Maharashtra', '2024-07-22', TRUE),
(108, 'Divya',  'Nair',   'divya.n@email.com',  'Kochi',     'Kerala',      '2024-08-30', FALSE);

-- Insert products
INSERT INTO products VALUES
(201, 'Wireless Earbuds',      'Electronics', 'BoAt',          1499.00, 250),
(202, 'Cotton T-Shirt',        'Clothing',    'Levis',         799.00,  500),
(203, 'Smart Watch',           'Electronics', 'Noise',         2999.00, 150),
(204, 'Running Shoes',         'Clothing',    'Nike',          4599.00, 120),
(205, 'Bluetooth Speaker',     'Electronics', 'JBL',           3499.00, 200),
(206, 'Bedsheet Set',          'Home',        'Spaces',        1299.00, 300),
(207, 'Laptop Stand',          'Electronics', 'AmazonBasics',  899.00,  180),
(208, 'Cushion Covers (Set)',  'Home',        'HomeCenter',    599.00,  400);

-- Insert orders
INSERT INTO orders VALUES
(1001, 101, '2024-08-01', 'Delivered',  4498.00),
(1002, 102, '2024-08-03', 'Delivered',  799.00),
(1003, 103, '2024-08-05', 'Shipped',    7498.00),
(1004, 101, '2024-08-10', 'Delivered',  3499.00),
(1005, 104, '2024-08-12', 'Cancelled',  2999.00),
(1006, 105, '2024-08-15', 'Delivered',  5898.00),
(1007, 106, '2024-08-18', 'Pending',    1299.00),
(1008, 103, '2024-08-20', 'Delivered',  899.00),
(1009, 107, '2024-08-25', 'Shipped',    6098.00),
(1010, 108, '2024-08-28', 'Delivered',  1598.00);

-- Insert order_items
INSERT INTO order_items VALUES
(5001, 1001, 201, 2, 1499.00, 0),
(5002, 1001, 207, 1,  899.00, 10),
(5003, 1002, 202, 1,  799.00,  0),
(5004, 1003, 203, 1, 2999.00,  0),
(5005, 1003, 204, 1, 4599.00,  5),
(5006, 1004, 205, 1, 3499.00,  0),
(5007, 1005, 203, 1, 2999.00,  0),
(5008, 1006, 201, 1, 1499.00, 10),
(5009, 1006, 204, 1, 4599.00,  5),
(5010, 1007, 206, 1, 1299.00,  0),
(5011, 1008, 207, 1,  899.00,  0),
(5012, 1009, 205, 1, 3499.00,  0),
(5013, 1009, 208, 2,  599.00, 15),
(5014, 1010, 206, 1, 1299.00,  0),
(5015, 1010, 208, 1,  599.00,  0);

-- ==========================================================
-- 3. Section‑wise Solutions to All Questions
-- ==========================================================

-- Section A – SQL Basics
-- Q1. Display all columns and rows from the customer's table.
SELECT * FROM customers;

-- Q2. Retrieve only the first_name, last_name, and city of all customers.
SELECT first_name, last_name, city FROM customers;

-- Q3. List all unique categories available in the products table.
SELECT DISTINCT category FROM products;

-- Q4. Identify the Primary Key of each table in the schema.
SELECT 'customers'   AS table_name, customer_id AS primary_key FROM customers LIMIT 1
UNION ALL
SELECT 'products',    product_id      FROM products    LIMIT 1
UNION ALL
SELECT 'orders',      order_id        FROM orders      LIMIT 1
UNION ALL
SELECT 'order_items', item_id         FROM order_items LIMIT 1;

-- Q5. What constraints are applied to the email column in the customers table?
--    Explanation: The email column is defined as UNIQUE NOT NULL, so it must contain
--    a non‑NULL value and all values must be distinct.
--    Example of error if duplicate is attempted:
--    INSERT INTO customers (customer_id, first_name, last_name, email, city, state, join_date, is_premium)
--    VALUES (109, 'Test', 'User', 'aarav.s@email.com', 'Test', 'City', '2024-09-01', FALSE);
--    -- ERROR: Duplicate entry 'aarav.s@email.com' for key 'email'

-- Q6. Try inserting a product with unit_price = -50.
--    The CHECK (unit_price > 0) constraint will reject the insert.
--    Example:
--    INSERT INTO products (product_id, product_name, category, brand, unit_price, stock_qty)
--    VALUES (209, 'Test Product', 'Electronics', 'TestBrand', -50.00, 10);
--    -- ERROR: CHECK constraint 'products_chk_1' is violated


-- Section B – Filtering & Optimization
-- Q7. Retrieve all orders with status = 'Delivered'.
SELECT * FROM orders WHERE status = 'Delivered';

-- Q8. Find all products in the 'Electronics' category with a unit_price greater than ₹2000.
SELECT * FROM products WHERE category = 'Electronics' AND unit_price > 2000;

-- Q9. List all customers who joined in the year 2024 and belong to the state 'Maharashtra'.
SELECT * FROM customers
WHERE YEAR(join_date) = 2024 AND state = 'Maharashtra';

-- Q10. Find all orders placed between '2024-08-10' and '2024-08-25' (inclusive) that are NOT cancelled.
SELECT * FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
  AND status <> 'Cancelled';

-- Q11. Explain what the index idx_orders_date does. How would it improve the performance of a query that filters orders by order_date?
--     The index idx_orders_date speeds up queries that filter or sort on order_date, such as:
--     SELECT * FROM orders WHERE order_date = '2024-08-15';
--     Because the index allows the engine to locate the relevant rows without scanning the whole table.

-- Q12. If you run: SELECT * FROM customers WHERE YEAR(join_date) = 2024;
--     -- would the index on join_date be used? Explain why or why not, and rewrite the query to be index-friendly (SARGable).
--     The function YEAR() prevents the use of the index because it makes the predicate non‑SARGable.
--     Rewritten index‑friendly query:
SELECT * FROM customers WHERE join_date >= '2024-01-01' AND join_date < '2025-01-01';

-- Section C – Aggregation (GROUP BY, SUM, COUNT, AVG, MIN, MAX)
-- Q13. Count the total number of orders in the orders table.
SELECT COUNT(*) AS total_orders FROM orders;

-- Q14. Find the total revenue (SUM of total_amount) from all 'Delivered' orders.
SELECT SUM(total_amount) AS total_revenue_delivered
FROM orders
WHERE status = 'Delivered';

-- Q15. Calculate the average unit_price of products in each category.
SELECT category, AVG(unit_price) AS avg_price
FROM products
GROUP BY category;

-- Q16. For each order status, find the count of orders and the total revenue. Sort the result by total revenue in descending order.
SELECT status,
       COUNT(*) AS orders_count,
       SUM(total_amount) AS total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC;

-- Q17. Find the most expensive (MAX) and cheapest (MIN) product in each category.
SELECT category,
       MAX(unit_price) AS most_expensive,
       MIN(unit_price) AS cheapest
FROM products
GROUP BY category;

-- Q18. List all product categories where the average unit_price is greater than ₹2000.
SELECT category
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;

-- Section D – Joins & Relationships
-- Q19. Write an INNER JOIN query to display each order along with the customer's first_name and last_name.
--     Show: order_id, order_date, first_name, last_name, total_amount.
SELECT o.order_id,
       o.order_date,
       c.first_name,
       c.last_name,
       o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- Q20. Using a LEFT JOIN, list ALL customers and their orders (if any).
--     Customers with no orders should still appear with NULL values for order columns.
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       o.order_id,
       o.order_date,
       o.status,
       o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- Q21. Write a query using JOINs across three tables (orders → order_items → products)
--     to show: order_id, product_name, quantity, unit_price, and discount_pct for each order item.
SELECT oi.order_id,
       p.product_name,
       oi.quantity,
       oi.unit_price,
       oi.discount_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id;

-- Q22. Explain the difference between LEFT JOIN and RIGHT JOIN with an example from this schema.
--     LEFT JOIN returns all rows from the left table and matching rows from the right table;
--     RIGHT JOIN returns all rows from the right table and matching rows from the left table.
--     Example difference:
--     -- LEFT JOIN (customers left, orders right) keeps all customers even if they have no orders.
--     -- RIGHT JOIN (orders left, customers right) keeps all orders even if the customer_id is missing (which cannot happen due to FK, but conceptually).
--     FULL OUTER JOIN would return all rows from both tables, filling with NULLs when there is no match.
--     It is useful when you need to see unmatched rows from both sides (e.g., orders without customers or customers without orders).

-- Q23. Identify all Foreign Key relationships in the schema.
--     • orders.customer_id references customers.customer_id
--     • order_items.order_id references orders.order_id
--     • order_items.product_id references products.product_id
--     Attempting to insert an order with customer_id = 999 (non‑existent) would fail with a foreign‑key violation,
--     because the value does not exist in the referenced customers table.


-- Section E – Advanced Concepts (CASE, ACID, Transactions)
-- Q24. Write a query using CASE to classify products into price tiers:
--     • 'Budget'    → unit_price < 1000
--     • 'Mid-Range' → unit_price BETWEEN 1000 AND 3000
--     • 'Premium'   → unit_price > 3000
--     Display: product_name, unit_price, price_tier.
SELECT product_name,
       unit_price,
       CASE
           WHEN unit_price < 1000               THEN 'Budget'
           WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
           ELSE                                 'Premium'
       END AS price_tier
FROM products;

-- Q25. Using a CASE statement inside an aggregate function, count how many orders are 'Delivered' vs 'Not Delivered' (all other statuses).
--     Display the result in a single row.
SELECT
    SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_count,
    SUM(CASE WHEN status <> 'Delivered' THEN 1 ELSE 0 END) AS not_delivered_count
FROM orders;

-- Q26. Explain each letter of ACID:
--     • A – Atomicity: Transactions are all‑or‑nothing; they either fully commit or fully roll back.
--     • C – Consistency: The database remains in a valid state before and after the transaction.
--     • I – Isolation: Concurrent transactions do not interfere with each other.
--     • D – Durability: Once committed, changes are permanent even in case of a crash.
--     Real‑world example (bank transfer):
--        * Atomicity ensures both debit and credit succeed or neither does.
--        * Consistency ensures account balances stay non‑negative.
--        * Isolation prevents one transfer from seeing another’s intermediate state.
--        * Durability guarantees the transfer record persists after commit.

-- Q27. Write a SQL transaction that does the following atomically:
--      1. Insert a new order (order_id=1011, customer_id=102, today's date, 'Pending', 1598.00)
--      2. Insert two order items for that order
--      3. Update the stock_qty of the purchased products
--      4. If any step fails, ROLLBACK the entire transaction. Otherwise, COMMIT.
--      Write the complete BEGIN...COMMIT/ROLLBACK block.
BEGIN;
    INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
    VALUES (1011, 102, CURDATE(), 'Pending', 1598.00);

    -- Insert two order items (assuming product_id 202 and 203)
    INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price, discount_pct)
    VALUES (5016, 1011, 202, 1, 799.00, 0),
           (5017, 1011, 203, 1, 2999.00, 5);

    -- Update stock quantities (decrease stock_qty)
    UPDATE products
    SET stock_qty = stock_qty - CASE product_id
        WHEN 202 THEN 1
        WHEN 203 THEN 1
        ELSE 0 END
    WHERE product_id IN (202, 203);
COMMIT;
-- If any error occurs before COMMIT, issue ROLLBACK to undo all changes.