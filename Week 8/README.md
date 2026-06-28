# E-Commerce Order Analytics System

A complete implementation of a data pipeline for cleaning, analyzing, and reporting on e-commerce order data. This project demonstrates Python data processing, SQL analysis, and business intelligence skills.

## 📋 Project Overview

This solution covers all phases of the intern mini project:

- **Part 1**: Generate realistic but intentionally messy data (4 CSV files)
- **Part 2**: Data cleaning and validation with detailed issue reporting
- **Part 3**: SQL analysis with basic, intermediate, and advanced queries
- **Part 4**: Python + SQL integration with CLI reporting tool
- **Part 5**: Edge case handling and test cases

## 📁 Files Included

### Main Files
- **ecommerce_analytics.py** - Main implementation file (Part 1-5)
- **advanced_sql_queries.py** - Advanced SQL queries module (Window functions, CTEs, etc.)
- **README.md** - This file

## 🚀 Quick Start

### Requirements
- Python 3.7+
- SQLite3 (included with Python)
- No external dependencies (uses only stdlib)

### Running the Project

```bash
# Run the complete pipeline
python ecommerce_analytics.py

# This will:
# 1. Generate 4 CSV files with sample data
# 2. Clean the data and generate reports
# 3. Load data into SQLite database
# 4. Run analysis queries
# 5. Generate summary reports
# 6. Test edge cases
```

### Output Files Generated

```
├── customers.csv                 # Raw customer data
├── products.csv                  # Raw product data
├── products_clean.csv            # Cleaned product data
├── orders.csv                    # Raw order data
├── orders_clean.csv              # Cleaned order data
├── order_items.csv               # Order items data
└── orders_analytics.db           # SQLite database with all tables
```

## 📊 Data Specifications

### CSV Files Generated

#### 1. **orders.csv**
- **Columns**: order_id, customer_id, order_date, status, region_code
- **Intentional Issues**:
  - 5% have NULL customer_id
  - 3% have date in wrong format (DD-MM-YYYY instead of YYYY-MM-DD)
- **Status Values**: PLACED, SHIPPED, DELIVERED, CANCELLED, RETURNED
- **Date Format**: YYYY-MM-DD HH:MM:SS
- **Region Codes**: NA, EU, APAC, SA, AF

#### 2. **order_items.csv**
- **Columns**: item_id, order_id, product_id, quantity, unit_price, discount_percent
- **Intentional Issues**:
  - 3% have negative quantity (returns)
  - Discount percentages between 0-100
- **Records**: ~2000-2500 items

#### 3. **products.csv**
- **Columns**: product_id, product_name, category, subcategory, cost_price
- **Intentional Issues**:
  - ~10% have extra spaces or mixed case
- **Categories**: Electronics, Clothing, Home, Books

#### 4. **customers.csv**
- **Columns**: customer_id, customer_name, email, registration_date, customer_type
- **Intentional Issues**:
  - 2% have invalid emails (missing @ or domain)
- **Customer Types**: REGULAR, PREMIUM, VIP

## 🧹 Data Cleaning Functions

### clean_orders()
- Fixes date format inconsistencies
- Handles NULL customer_ids
- Reports all issues found
- **Output**: orders_clean.csv

### clean_products()
- Trims whitespace from product names
- Converts to title case
- Reports all transformations
- **Output**: products_clean.csv

### validate_emails()
- Uses regex to validate email format
- Returns list of customer_ids with invalid emails
- **Pattern**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

### check_referential_integrity()
- Finds order_items with non-existent order_id
- Returns list of orphaned items
- Ensures data consistency

## 📈 SQL Queries Implemented

### Basic Queries
1. **Total Revenue by Category** - Sum of (quantity × unit_price × (1 - discount%))
2. **Top 10 Customers** - Ranked by total order value
3. **Monthly Order Count** - For last 12 months

### Intermediate Queries
4. **Customers with No Deliveries** - Placed orders but status never DELIVERED
5. **Products with More Returns** - More returned than purchased
6. **Return Rate by Category** - Percentage of items returned per category

### Advanced Queries (Window Functions, CTEs)
7. **Running Totals** - Cumulative revenue by region over time
8. **Dense Ranking** - Product ranking within each category
9. **LAG/LEAD Analysis** - Days between consecutive customer orders
10. **Multi-level CTE** - Customer revenue categorization per month
11. **NTILE Segmentation** - Customer quartiles (Platinum/Gold/Silver/Bronze)
12. **Year-over-Year Growth** - Monthly revenue comparison with previous year
13. **First/Last Values** - Customer category shift analysis
14. **Cumulative Distribution** - Revenue contribution percentage by customer
15. **Cohort Analysis** - Customer retention by registration month
16. **Self-Join** - Products frequently bought together

## 🛠️ Edge Case Handling

The system tests and handles:

```python
# Edge Case 1: Orphaned order_items
# What happens when order_items.order_id doesn't exist in orders?
# → check_referential_integrity() identifies these

# Edge Case 2: Invalid discounts
# What happens when discount_percent > 100?
# → Cleaned data ensures 0-100 range

# Edge Case 3: Zero quantity
# What happens when quantity is 0?
# → Handled in revenue calculations

# Edge Case 4: Future dates
# What happens when order_date is in the future?
# → Date validation catches these
```

## 📊 Sample Output

```
════════════════════════════════════════════════════════════
           ORDER ANALYTICS REPORT (DAILY)
           Period: 2024-05-29 to 2024-06-28
════════════════════════════════════════════════════════════

📊 SUMMARY METRICS
├─ Total Orders:        487
├─ Unique Customers:    85
└─ Total Revenue:       $1,234,567.89

🏆 TOP 3 PRODUCTS
├─ 1. Laptop (Qty: 45, Revenue: $45,000.00)
├─ 2. Smartphone (Qty: 78, Revenue: $39,000.00)
└─ 3. Headphones (Qty: 120, Revenue: $18,000.00)

════════════════════════════════════════════════════════════
```

## 🔧 Class Overview

### DataGenerator
Generates realistic CSV data with intentional issues for testing

**Methods**:
- `generate_customers(filename)` - Create customer data
- `generate_products(filename)` - Create product data
- `generate_orders(filename)` - Create order data
- `generate_order_items(filename)` - Create order items data

### DataCleaner
Cleans and validates messy data

**Methods**:
- `clean_orders(input_file, output_file)` - Fix date formats, handle NULLs
- `clean_products(input_file, output_file)` - Normalize product names
- `validate_emails(input_file)` - Find invalid email addresses
- `check_referential_integrity(orders_file, order_items_file)` - Find orphaned items

### OrderAnalyticsDB
SQLite database operations and analysis

**Methods**:
- `connect()` - Create database connection
- `create_tables()` - Create schema
- `load_csv_data(...)` - Load cleaned data
- `query_total_revenue_by_category()` - Revenue analysis
- `query_top_10_customers()` - Customer analysis
- `query_monthly_order_count()` - Time series analysis
- `query_customers_no_delivery()` - Customer segmentation
- `query_return_rate_by_category()` - Quality metrics
- `generate_report(report_type, start_date, end_date)` - Create reports
- `close()` - Close connection

## 🧪 Testing

Edge cases are tested automatically:

```bash
python ecommerce_analytics.py
```

The script will:
1. Generate data with known issues
2. Clean the data
3. Report issues found (should match generation percentages)
4. Validate referential integrity
5. Test all edge cases

## 📝 Key Metrics Calculated

### Revenue Metrics
- Total revenue per category
- Customer lifetime value
- Monthly/yearly revenue
- Year-over-year growth %

### Customer Metrics
- Top customers by value
- Customer segmentation (quartiles)
- Repeat purchase gaps
- At-risk customers (gap > 30 days)

### Product Metrics
- Product ranking by revenue
- Return rates by category
- Products frequently bought together
- Products with negative ROI (more returns than sales)

### Operational Metrics
- Order status distribution
- Regional revenue breakdown
- Delivery performance
- Discount effectiveness

## 🔍 Database Schema

```sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATETIME,
    status TEXT,
    region_code TEXT
);

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    discount_percent REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    subcategory TEXT,
    cost_price REAL
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    registration_date DATE,
    customer_type TEXT
);
```

## 💡 Usage Examples

### Generate Report for Specific Date Range
```python
from ecommerce_analytics import OrderAnalyticsDB

db = OrderAnalyticsDB()
db.connect()
report = db.generate_report(
    report_type='weekly',
    start_date='2024-05-01',
    end_date='2024-05-31'
)
print(report)
db.close()
```

### Query Specific Analysis
```python
db = OrderAnalyticsDB()
db.connect()

# Get top customers
results = db.query_top_10_customers()
for row in results:
    print(f"{row['customer_name']}: ${row['total_value']}")

db.close()
```

### Run Advanced Queries
```python
from advanced_sql_queries import execute_query, print_query_results
import sqlite3

conn = sqlite3.connect('orders_analytics.db')
conn.row_factory = sqlite3.Row

results = execute_query(conn, 'customer_lifetime_value_quartiles')
print_query_results('Customer Quartiles', results)

conn.close()
```

## 📈 Performance Notes

- Dataset: ~500 orders, ~100 customers, ~50 products, ~2000 items
- Database: SQLite (suitable for analysis, not production)
- Processing time: ~2-3 seconds for full pipeline
- All queries optimized for readability and educational purposes

## 🎓 Learning Outcomes

This project demonstrates:

1. **Python Skills**
   - Data generation and manipulation
   - CSV file handling
   - Regular expressions for validation
   - Object-oriented programming

2. **SQL Skills**
   - Window functions (LAG, LEAD, ROW_NUMBER, DENSE_RANK, NTILE)
   - Common Table Expressions (CTEs)
   - Subqueries and self-joins
   - Aggregate and analytical functions
   - Date/time operations

3. **Data Engineering Skills**
   - ETL pipeline design
   - Data quality checks
   - Referential integrity validation
   - Error handling and logging

4. **Business Analysis Skills**
   - Revenue analysis
   - Customer segmentation
   - Cohort analysis
   - Trend analysis (YoY)

## 🐛 Troubleshooting

### Database locked error
**Solution**: Delete `orders_analytics.db` and regenerate

### Import errors
**Solution**: Make sure you're using Python 3.7+, no external packages needed

### CSV not found
**Solution**: Run from the directory where CSVs are generated

## 📚 Additional Resources

### SQL Window Functions
- ROW_NUMBER() - Sequential numbering
- DENSE_RANK() - Ranking with ties
- LAG() / LEAD() - Access previous/next rows
- NTILE() - Divide into quantiles
- SUM() OVER() - Running totals

### Common Table Expressions
Used for:
- Breaking down complex queries
- Recursive data (hierarchies)
- Multiple aggregation levels
- Readability and maintainability

## 🎯 Next Steps

To extend this project:

1. Add customer segmentation RFM analysis
2. Implement predictive churn modeling
3. Add inventory management
4. Create dashboards with visualization libraries
5. Migrate to PostgreSQL for production use
6. Add web API layer with Flask/FastAPI
7. Implement data quality monitoring
8. Add automated scheduling (cron/Airflow)

## 📄 License

Educational project - Free to use and modify

## ✅ Verification Checklist

Run through this to verify all components work:

- [ ] `python ecommerce_analytics.py` executes without errors
- [ ] All 4 CSV files generated (customers, products, orders, order_items)
- [ ] Cleaned versions created (orders_clean, products_clean)
- [ ] SQLite database created (orders_analytics.db)
- [ ] Sample queries return results
- [ ] Cleaning report shows expected issue percentages
- [ ] Edge case tests pass
- [ ] Sample report generates successfully

---

**Total Implementation**: ~500+ lines of code
**Time to Complete**: 2-3 hours
**Difficulty Level**: Intermediate to Advanced
