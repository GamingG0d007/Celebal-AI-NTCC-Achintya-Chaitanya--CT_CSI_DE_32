-- Subqueries

-- 1. Customers with sales above average
SELECT DISTINCT c.customer_id, c.customer_name, c.segment
FROM customers c
JOIN superstore_raw sr ON c.customer_id = sr.Customer_ID
WHERE sr.Sales > (SELECT AVG(Sales) FROM superstore_raw);

-- 2. Highest order per customer
SELECT o.order_id, o.customer_id, s.Sales
FROM orders o
JOIN superstore_raw s ON o.order_id = s.Order_ID
WHERE s.Sales = (
    SELECT MAX(s2.Sales)
    FROM superstore_raw s2
    WHERE s2.Customer_ID = o.customer_id
);

-- CTEs

-- 3. Total sales per customer
WITH customer_sales AS (
    SELECT DISTINCT Customer_ID, Customer_Name, Segment,
           SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY Customer_ID, Customer_Name, Segment
)
SELECT * FROM customer_sales ORDER BY total_sales DESC;

-- 4. Customer segments with average sales
WITH segment_avg AS (
    SELECT Segment, AVG(Sales) AS avg_sales
    FROM superstore_raw
    GROUP BY Segment
)
SELECT * FROM segment_avg;

-- Window Functions

-- 5. Rank customers by total sales
WITH customer_totals AS (
    SELECT DISTINCT Customer_ID, Customer_Name, Segment,
           SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY Customer_ID, Customer_Name, Segment
)
SELECT *,
       ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS row_num,
       RANK() OVER (ORDER BY total_sales DESC) AS rank
FROM customer_totals;

-- 6. Assign row numbers to each order within a custome
SELECT
    Order_ID,
    Customer_ID,
    Sales,
    ROW_NUMBER() OVER (
       PARTITION BY Customer_ID 
       ORDER BY Order_Date ASC 
    )AS order_row_num
FROM
    superstore_raw
ORDER BY
    Customer_ID,
    order_row_num;

-- 7.  Display top 3 customers based on total sales.
SELECT
    c.Customer_ID,
    c.Customer_Name,
    SUM(s.Sales) AS total_sales
FROM
    customers c
JOIN
    superstore_raw s ON c.Customer_ID = s.Customer_ID
GROUP BY
    c.Customer_ID, c.Customer_Name
ORDER BY
    total_sales DESC
LIMIT 3;



-- 8. Customer, total sales, and rank
WITH customer_totals AS (
    SELECT DISTINCT Customer_ID, Customer_Name, Segment,
           SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY Customer_ID, Customer_Name, Segment
)
SELECT *,
       ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS row_num,
       RANK() OVER (ORDER BY total_sales DESC) AS rank
FROM customer_totals;

-- Business Queries

-- 9. Top customers (top 5)
WITH customer_totals AS (
    SELECT DISTINCT Customer_ID, Customer_Name, Segment,
           SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY Customer_ID, Customer_Name, Segment
)
SELECT * FROM customer_totals
ORDER BY total_sales DESC
LIMIT 5;

-- 10. Low customers (bottom 5)
WITH customer_totals AS (
    SELECT DISTINCT Customer_ID, Customer_Name, Segment,
           SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY Customer_ID, Customer_Name, Segment
)
SELECT * FROM customer_totals
ORDER BY total_sales ASC
LIMIT 5;

-- 11. Single-order customers
SELECT DISTINCT c.customer_id, c.customer_name, c.segment,
       COUNT(DISTINCT s.Order_ID) AS order_count
FROM customers c
JOIN superstore_raw s ON c.customer_id = s.Customer_ID
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING COUNT(DISTINCT s.Order_ID) = 1;

-- 12. Above-average sales by region
WITH region_sales AS (
    SELECT DISTINCT Region, AVG(Sales) AS avg_region_sales
    FROM superstore_raw
    GROUP BY Region
)
SELECT sr.Region, AVG(sr.Sales) AS actual_avg_sales,
       rs.avg_region_sales AS overall_avg,
       CASE WHEN AVG(sr.Sales) > rs.avg_region_sales THEN 'Above Average'
            ELSE 'Below Average' END AS comparison
FROM superstore_raw sr
JOIN region_sales rs ON sr.Region = rs.Region
GROUP BY sr.Region, rs.avg_region_sales;

-- 13. Highest order value
SELECT
      Customer_ID,
      MAX(Sales) AS highest_order_value
  FROM
      superstore_raw
  GROUP BY
      Customer_ID
  ORDER BY
      highest_order_value DESC;