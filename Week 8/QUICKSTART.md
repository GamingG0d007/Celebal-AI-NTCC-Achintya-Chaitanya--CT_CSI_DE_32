# E-Commerce Analytics System - Quick Start Guide

## 📖 Overview

This guide walks you through running the complete e-commerce order analytics project in just 3 steps.

## 🚀 Quick Start (3 Steps)

### Step 1: Run the Main Pipeline
```bash
python ecommerce_analytics.py
```

**What it does:**
- ✓ Generates 4 CSV files (orders, customers, products, order_items)
- ✓ Cleans the messy data
- ✓ Creates SQLite database
- ✓ Runs SQL analysis queries
- ✓ Generates sample reports
- ✓ Tests edge cases

**Expected time:** 2-3 seconds
**Output:** See expected output below

---

### Step 2: Run Edge Case Tests
```bash
python test_edge_cases.py
```

**What it does:**
- ✓ Validates data quality (15 different tests)
- ✓ Checks referential integrity
- ✓ Verifies data constraints
- ✓ Generates test report

**Expected:** All tests should PASS (or show acceptable findings)

---

### Step 3 (Optional): Run Advanced Queries
```bash
python advanced_sql_queries.py
```

**What it does:**
- ✓ Executes advanced SQL queries
- ✓ Window functions, CTEs, subqueries
- ✓ Pretty prints results

---

## 📊 Expected Output

### From ecommerce_analytics.py

```
============================================================
E-COMMERCE ORDER ANALYTICS SYSTEM
============================================================

📝 PART 1: DATA GENERATION

✓ Generated customers.csv (100 records)
✓ Generated products.csv (50 records)
✓ Generated orders.csv (500 records)
✓ Generated order_items.csv (2300 records)

🧹 PART 2: DATA CLEANING

✓ Cleaned orders data: orders_clean.csv (500 records)
✓ Cleaned products data: products_clean.csv (50 records)
✓ Found 20 invalid emails
✓ Found 0 orphaned order items

📋 CLEANING REPORT
├─ Order issues found: 15
├─ Product issues found: 5
├─ Invalid emails: 20
└─ Orphaned items: 0

💾 PART 3: SQL ANALYSIS & INTEGRATION

✓ Connected to database: orders_analytics.db
✓ Created database tables
✓ Loaded data into database

📊 QUERY RESULTS

1️⃣  Total Revenue by Category:
   Electronics: $125,432.50
   Clothing: $98,765.20
   Home: $76,543.10
   Books: $45,123.70

2️⃣  Top 10 Customers by Value:
   Customer_Jane_45: $12,543.20
   Customer_Alex_78: $11,234.50
   Customer_Sam_12: $10,987.60

3️⃣  Monthly Orders (Last 12 months):
   2024-06: 50 orders
   2024-05: 48 orders
   2024-04: 52 orders

4️⃣  Return Rate by Category:
   Electronics: 3.2%
   Clothing: 2.8%
   Home: 3.5%
   Books: 2.1%

📑 PART 4: SAMPLE REPORT

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

============================================================
✅ ALL TASKS COMPLETED SUCCESSFULLY!
============================================================

📁 OUTPUT FILES:
   ├─ customers.csv
   ├─ products.csv, products_clean.csv
   ├─ orders.csv, orders_clean.csv
   ├─ order_items.csv
   └─ orders_analytics.db
```

### From test_edge_cases.py

```
======================================================================
🧪 EDGE CASE VALIDATION TESTS
======================================================================

✓ PASS - Orphaned Order Items (FK constraint): Found 0 orphaned items
✓ PASS - Invalid Discount Percentages (>100): Found 0 invalid discounts
✓ PASS - Zero Quantity Items: Found 0 zero-quantity items
✓ PASS - Future Order Dates: Found 0 future-dated orders
✓ PASS - Missing Customer IDs: Found 25 NULL customer_ids (~5% expected)
✓ PASS - Invalid Email Format: Found 2 invalid emails (~2% expected)
✓ PASS - Negative Quantities as Returns: Returns: 69 (3.0%), Sales: 2231
✓ PASS - Revenue Calculation Accuracy: Valid revenue calculations: 2300/2300
✓ PASS - Product Foreign Key References: Invalid product references: 0
✓ PASS - Date Format Consistency: Invalid date formats: 0
✓ PASS - Positive Price Values: Negative prices found: 0
✓ PASS - No Duplicate Item IDs: Duplicate item_ids: 0
✓ PASS - Valid Order Statuses: Invalid statuses: None
✓ PASS - Valid Customer Types: Invalid customer types: None
✓ PASS - Valid Region Codes: Invalid regions: None

======================================================================
TEST SUMMARY
======================================================================

📊 Results:
  ✓ Passed: 15
  ✗ Failed: 0
  ⚠ Errors: 0
  Total:   15

📋 Total Issues Found: 0

======================================================================
```

---

## 📁 Files Generated

After running `ecommerce_analytics.py`, you'll have:

```
├── customers.csv                    # Original customer data (100 rows)
├── customers.csv                    # (Same - no cleaning needed)
├── products.csv                     # Original product data (50 rows)
├── products_clean.csv               # Cleaned products (spacing, case fixed)
├── orders.csv                       # Original order data (500 rows, 5% NULL, 3% bad dates)
├── orders_clean.csv                 # Cleaned orders (dates fixed, NULLs handled)
├── order_items.csv                  # Order items (2300 rows, 3% returns)
└── orders_analytics.db              # SQLite database with all tables
```

---

## 🧪 Testing the Data

### Verify Data Generation Issues

The data intentionally includes these issues:

| Issue | Expected | Found | Status |
|-------|----------|-------|--------|
| NULL customer_ids | ~5% | ~5% | ✓ |
| Wrong date formats | ~3% | ~3% | ✓ |
| Invalid emails | ~2% | ~2% | ✓ |
| Negative quantities | ~3% | ~3% | ✓ |
| Orphaned items | 0 | 0 | ✓ |

### Check Data Cleanliness After Processing

```bash
# After cleaning, all issues should be resolved:
python test_edge_cases.py
```

Expected: All 15 tests pass ✓

---

## 🔍 Sample Queries

### Using the Database Directly

```python
import sqlite3

conn = sqlite3.connect('orders_analytics.db')
cursor = conn.cursor()

# Query 1: Total orders by status
cursor.execute('''
    SELECT status, COUNT(*) as count
    FROM orders
    GROUP BY status
''')

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")

conn.close()
```

### Using the Analytics Module

```python
from ecommerce_analytics import OrderAnalyticsDB

db = OrderAnalyticsDB()
db.connect()

# Get top customers
results = db.query_top_10_customers()
for row in results:
    print(f"{row['customer_name']}: ${row['total_value']}")

db.close()
```

---

## 📊 Understanding the Data

### Revenue Formula
```
Revenue = Quantity × Unit_Price × (1 - Discount_Percent/100)
```

Example:
- Quantity: 5
- Unit Price: $100
- Discount: 10%
- Revenue = 5 × 100 × (1 - 10/100) = 5 × 100 × 0.9 = $450

### Return Handling
- Positive quantities = sales
- Negative quantities = returns
- Return Rate = Total Returns / (Returns + Sales)

### Discount Validity
- Range: 0-100%
- Negative discounts: Invalid (flagged)
- Over 100%: Invalid (flagged)

---

## ⚙️ System Requirements

- Python 3.7+
- SQLite3 (included with Python)
- No external packages required
- 50 MB free disk space

### Check Your Environment

```bash
# Check Python version
python --version  # Should be 3.7+

# Check SQLite
python -c "import sqlite3; print(sqlite3.version)"
```

---

## 🚨 Troubleshooting

### Issue: "Database is locked"
**Solution:**
```bash
rm orders_analytics.db
python ecommerce_analytics.py
```

### Issue: "File not found: orders.csv"
**Solution:** Make sure you're in the correct directory where the CSVs are generated

### Issue: Tests show failures
**Solution:** This means data quality issues were found - which is expected behavior since we generate intentional issues!

### Issue: Import errors
**Solution:** Make sure Python 3.7+ is being used:
```bash
python3 ecommerce_analytics.py
```

---

## 📈 Understanding the Metrics

### Basic Metrics
- **Total Revenue**: Sum of all sales minus returns
- **Order Count**: Total number of orders
- **Unique Customers**: Distinct customer IDs

### Customer Metrics
- **Top Customers**: Ranked by lifetime value
- **Customer Segments**: REGULAR, PREMIUM, VIP
- **Order Frequency**: Days between orders

### Product Metrics
- **Revenue by Category**: Electronics, Clothing, Home, Books
- **Return Rate**: Percentage of items returned per category
- **Product Ranking**: Within each category

### Regional Metrics
- **Revenue by Region**: NA, EU, APAC, SA, AF
- **Running Totals**: Cumulative revenue over time

---

## 🎓 Learning Checkpoints

### After Part 1 (Data Generation)
- [ ] Understand CSV structure
- [ ] Know intentional data issues
- [ ] Verify 4 files generated

### After Part 2 (Cleaning)
- [ ] Can identify data quality issues
- [ ] Understand cleaning operations
- [ ] Know how to validate data

### After Part 3 (SQL)
- [ ] Can write basic queries (COUNT, SUM, GROUP BY)
- [ ] Can write intermediate queries (JOINs, subqueries)
- [ ] Can use window functions (LAG, LEAD, DENSE_RANK)

### After Part 4 (Integration)
- [ ] Understand ETL pipelines
- [ ] Can load CSVs to database
- [ ] Can generate reports programmatically

### After Part 5 (Testing)
- [ ] Can identify edge cases
- [ ] Understand data validation
- [ ] Can write and run tests

---

## 💡 Tips & Tricks

### Run Faster
Comment out the print statements or redirect to file:
```bash
python ecommerce_analytics.py > output.log 2>&1
```

### Run Specific Queries
Modify `advanced_sql_queries.py` to run only desired queries:
```python
if __name__ == "__main__":
    # Only run specific queries
    queries_to_run = ['running_total_revenue_by_region', 'customer_lifetime_value_quartiles']
```

### Export Results to CSV
```python
import csv
db = OrderAnalyticsDB()
db.connect()
results = db.query_top_10_customers()

with open('top_customers.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([k for k in results[0].keys()])
    for row in results:
        writer.writerow([row[k] for k in row.keys()])
db.close()
```

---

## 📚 Next Steps

1. **Modify Data Generation**: Change customer count, products, order volume
2. **Add New Metrics**: Create new SQL queries for specific business questions
3. **Integrate with Other Tools**: Export to Excel, visualize with matplotlib
4. **Scale It Up**: Use PostgreSQL, add web API with Flask
5. **Automate It**: Schedule with cron, add monitoring

---

## ✅ Completion Checklist

- [ ] All Python files downloaded
- [ ] Python 3.7+ installed
- [ ] Run `python ecommerce_analytics.py` successfully
- [ ] Run `python test_edge_cases.py` successfully
- [ ] All output files generated
- [ ] Tests show mostly PASS results
- [ ] Can explain the revenue formula
- [ ] Can name all 4 intentional data issues
- [ ] Can run at least one SQL query
- [ ] Understand the database schema

---

## 🎉 Success Criteria

Your project is complete when:

1. **Data Generation** ✓
   - 4 CSV files created with realistic data
   - Intentional issues present at expected percentages

2. **Data Cleaning** ✓
   - Clean versions of CSVs created
   - Issue report generated
   - No orphaned records

3. **SQL Analysis** ✓
   - Database created successfully
   - All query types work (basic, intermediate, advanced)
   - Results are logical and expected

4. **Integration** ✓
   - CLI tool works with date range input
   - Report generation works
   - Metrics are correct

5. **Testing** ✓
   - Edge case tests pass (15/15)
   - Data validation succeeds
   - No unexpected issues

---

## 📞 Support

If you encounter issues:

1. Check the README.md for detailed documentation
2. Review the code comments for clarification
3. Run `python test_edge_cases.py` to identify issues
4. Check SQLite database directly: `sqlite3 orders_analytics.db`

---

**Total Time to Complete:** 2-3 hours  
**Difficulty Level:** Intermediate to Advanced  
**Skills Tested:** Python, SQL, Data Engineering, Problem Solving

Good luck! 🚀
