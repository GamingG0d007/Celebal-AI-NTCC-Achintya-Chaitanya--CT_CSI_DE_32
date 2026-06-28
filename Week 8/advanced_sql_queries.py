"""
Advanced SQL Queries for E-Commerce Analytics
Includes: Window Functions, CTEs, Subqueries, Cohort Analysis
"""

ADVANCED_SQL_QUERIES = {
    # Query 7: Running Totals with Window Functions
    "running_total_revenue_by_region": """
    SELECT 
        region_code,
        DATE(order_date) as order_date,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as daily_revenue,
        ROUND(
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100))
            OVER (PARTITION BY region_code ORDER BY DATE(order_date) ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
            2
        ) as running_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY region_code, DATE(order_date)
    ORDER BY region_code, order_date
    """,
    
    # Query 8: Ranking with DENSE_RANK
    "product_ranking_by_category": """
    SELECT 
        category,
        product_name,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as total_revenue,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)) DESC) as rank_in_category
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY category, product_name
    ORDER BY category, rank_in_category
    """,
    
    # Query 9: LAG/LEAD Analysis - Days between orders
    "customer_order_gaps": """
    SELECT 
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as previous_order_date,
        ROUND(
            (julianday(order_date) - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date))) 
        ) as days_gap
    FROM orders
    WHERE customer_id IS NOT NULL
    ORDER BY customer_id, order_date
    """,
    
    # Query to flag at-risk customers
    "at_risk_customers": """
    WITH customer_gaps AS (
        SELECT 
            customer_id,
            AVG(
                ROUND(
                    (julianday(order_date) - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date))) 
                )
            ) as avg_gap_days
        FROM orders
        WHERE customer_id IS NOT NULL
        GROUP BY customer_id
    )
    SELECT 
        c.customer_id,
        c.customer_name,
        ROUND(cg.avg_gap_days, 1) as avg_gap_days,
        CASE WHEN cg.avg_gap_days > 30 THEN 'At Risk' ELSE 'Healthy' END as risk_status
    FROM customer_gaps cg
    JOIN customers c ON cg.customer_id = c.customer_id
    ORDER BY avg_gap_days DESC
    """,
    
    # Query 10: CTE with Multiple Levels
    "customer_revenue_categorization": """
    WITH monthly_revenue AS (
        SELECT 
            strftime('%Y-%m', o.order_date) as month,
            o.customer_id,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as monthly_revenue
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.customer_id IS NOT NULL
        GROUP BY month, o.customer_id
    ),
    categorized_revenue AS (
        SELECT 
            month,
            customer_id,
            monthly_revenue,
            CASE 
                WHEN monthly_revenue > 10000 THEN 'High'
                WHEN monthly_revenue BETWEEN 5000 AND 10000 THEN 'Medium'
                ELSE 'Low'
            END as revenue_category
        FROM monthly_revenue
    )
    SELECT 
        month,
        revenue_category,
        COUNT(DISTINCT customer_id) as customer_count,
        ROUND(SUM(monthly_revenue), 2) as total_monthly_revenue
    FROM categorized_revenue
    GROUP BY month, revenue_category
    ORDER BY month, revenue_category
    """,
    
    # Query 11: NTILE for Segmentation
    "customer_lifetime_value_quartiles": """
    SELECT 
        c.customer_id,
        c.customer_name,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as total_lifetime_value,
        NTILE(4) OVER (ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100))) as quartile,
        CASE 
            WHEN NTILE(4) OVER (ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100))) = 4 THEN 'Platinum'
            WHEN NTILE(4) OVER (ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100))) = 3 THEN 'Gold'
            WHEN NTILE(4) OVER (ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100))) = 2 THEN 'Silver'
            ELSE 'Bronze'
        END as quartile_label
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.customer_id IS NOT NULL
    GROUP BY c.customer_id
    ORDER BY total_lifetime_value DESC
    """,
    
    # Query 12: Year-over-Year Comparison
    "year_over_year_revenue": """
    WITH monthly_revenue AS (
        SELECT 
            strftime('%Y', o.order_date) as year,
            strftime('%m', o.order_date) as month,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as revenue
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY year, month
    )
    SELECT 
        CAST(curr.year AS INTEGER) as year,
        CAST(curr.month AS INTEGER) as month,
        curr.revenue,
        COALESCE(prev.revenue, 0) as prev_year_revenue,
        ROUND(
            CASE 
                WHEN prev.revenue IS NULL OR prev.revenue = 0 THEN NULL
                ELSE ((curr.revenue - prev.revenue) / prev.revenue) * 100
            END, 2
        ) as yoy_growth_percent
    FROM monthly_revenue curr
    LEFT JOIN monthly_revenue prev ON curr.month = prev.month 
        AND CAST(curr.year AS INTEGER) = CAST(prev.year AS INTEGER) + 1
    ORDER BY year DESC, month
    """,
    
    # Query 13: First/Last Value Analysis
    "customer_category_shift": """
    WITH first_purchase AS (
        SELECT 
            o.customer_id,
            p.category as first_category,
            ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date) as rn
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.customer_id IS NOT NULL
    ),
    last_purchase AS (
        SELECT 
            o.customer_id,
            p.category as last_category,
            ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) as rn
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.customer_id IS NOT NULL
    )
    SELECT 
        c.customer_id,
        c.customer_name,
        fp.first_category,
        lp.last_category,
        CASE WHEN fp.first_category != lp.last_category THEN 'Yes' ELSE 'No' END as category_shift
    FROM customers c
    LEFT JOIN first_purchase fp ON c.customer_id = fp.customer_id AND fp.rn = 1
    LEFT JOIN last_purchase lp ON c.customer_id = lp.customer_id AND lp.rn = 1
    ORDER BY c.customer_id
    """,
    
    # Query 14: Cumulative Distribution
    "cumulative_revenue_distribution": """
    WITH customer_revenue AS (
        SELECT 
            c.customer_id,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as customer_revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.customer_id IS NOT NULL
        GROUP BY c.customer_id
    ),
    total_revenue AS (
        SELECT SUM(customer_revenue) as total_rev FROM customer_revenue
    )
    SELECT 
        cr.customer_id,
        cr.customer_revenue,
        ROUND(
            SUM(cr.customer_revenue) OVER (ORDER BY cr.customer_revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
            2
        ) as cumulative_revenue,
        ROUND(
            (SUM(cr.customer_revenue) OVER (ORDER BY cr.customer_revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / tr.total_rev) * 100,
            2
        ) as cumulative_percent
    FROM customer_revenue cr
    CROSS JOIN total_revenue tr
    ORDER BY cr.customer_revenue DESC
    """,
    
    # Query 15: Complex CTE - Cohort Analysis
    "cohort_analysis": """
    WITH customer_first_order AS (
        SELECT 
            c.customer_id,
            strftime('%Y-%m', c.registration_date) as cohort_month,
            strftime('%Y-%m', o.order_date) as order_month,
            (julianday(o.order_date) - julianday(c.registration_date)) / 30.0 as months_since_registration
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.order_id IS NOT NULL
    ),
    cohort_data AS (
        SELECT 
            cohort_month,
            ROUND(months_since_registration) as month_offset,
            COUNT(DISTINCT customer_id) as customers_active
        FROM customer_first_order
        WHERE months_since_registration >= 0 AND months_since_registration < 4
        GROUP BY cohort_month, ROUND(months_since_registration)
    ),
    cohort_sizes AS (
        SELECT 
            cohort_month,
            SUM(CASE WHEN month_offset = 0 THEN customers_active ELSE 0 END) as month_0
        FROM cohort_data
        GROUP BY cohort_month
    )
    SELECT 
        cd.cohort_month,
        cs.month_0,
        SUM(CASE WHEN cd.month_offset = 1 THEN cd.customers_active ELSE 0 END) as month_1,
        SUM(CASE WHEN cd.month_offset = 2 THEN cd.customers_active ELSE 0 END) as month_2,
        SUM(CASE WHEN cd.month_offset = 3 THEN cd.customers_active ELSE 0 END) as month_3
    FROM cohort_data cd
    JOIN cohort_sizes cs ON cd.cohort_month = cs.cohort_month
    GROUP BY cd.cohort_month
    ORDER BY cd.cohort_month
    """,
    
    # Query 16: Self-Join with Window Function
    "products_bought_together": """
    WITH product_pairs AS (
        SELECT 
            oi1.product_id as product_a,
            oi2.product_id as product_b,
            oi1.order_id
        FROM order_items oi1
        JOIN order_items oi2 ON oi1.order_id = oi2.order_id
        WHERE oi1.product_id < oi2.product_id
    )
    SELECT 
        p1.product_name as product_a,
        p2.product_name as product_b,
        COUNT(*) as times_bought_together,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT order_id) FROM orders), 2) as percentage_of_orders
    FROM product_pairs pp
    JOIN products p1 ON pp.product_a = p1.product_id
    JOIN products p2 ON pp.product_b = p2.product_id
    GROUP BY product_a, product_b
    HAVING COUNT(*) > 1
    ORDER BY times_bought_together DESC
    """,
    
    # Additional: Products with more returns than purchases
    "products_more_returns_than_sales": """
    SELECT 
        p.product_id,
        p.product_name,
        SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) as total_sales,
        SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) as total_returns
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_id
    HAVING total_returns > total_sales
    ORDER BY total_returns DESC
    """
}


def execute_query(db_connection, query_name):
    """Execute a query and return results"""
    if query_name not in ADVANCED_SQL_QUERIES:
        print(f"❌ Query '{query_name}' not found")
        return None
    
    try:
        cursor = db_connection.cursor()
        cursor.execute(ADVANCED_SQL_QUERIES[query_name])
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"❌ Error executing query: {str(e)}")
        return None


def print_query_results(query_name, results):
    """Pretty print query results"""
    if not results:
        print(f"❌ No results for query: {query_name}")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 {query_name.upper().replace('_', ' ')}")
    print(f"{'='*60}")
    
    # Print header
    if results:
        headers = [desc[0] for desc in results[0].keys()] if hasattr(results[0], 'keys') else []
        if headers:
            print(" | ".join(f"{h:^20}" for h in headers))
            print("-" * (len(headers) * 22))
        
        # Print rows
        for row in results[:10]:  # Limit to first 10 rows for readability
            if hasattr(row, 'keys'):
                values = [str(row[k]) for k in row.keys()]
            else:
                values = [str(v) for v in row]
            print(" | ".join(f"{v:^20}" for v in values))
        
        if len(results) > 10:
            print(f"\n... and {len(results) - 10} more rows")


if __name__ == "__main__":
    import sqlite3
    
    print("\n" + "="*60)
    print("ADVANCED SQL QUERIES MODULE")
    print("="*60)
    print("\nAvailable queries:")
    for i, query_name in enumerate(ADVANCED_SQL_QUERIES.keys(), 1):
        print(f"  {i}. {query_name}")
    
    # Example usage:
    try:
        conn = sqlite3.connect('orders_analytics.db')
        conn.row_factory = sqlite3.Row
        
        # Execute a few example queries
        for query_name in ['running_total_revenue_by_region', 'customer_lifetime_value_quartiles']:
            results = execute_query(conn, query_name)
            if results:
                print_query_results(query_name, results)
        
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Make sure to run ecommerce_analytics.py first to generate the database")
