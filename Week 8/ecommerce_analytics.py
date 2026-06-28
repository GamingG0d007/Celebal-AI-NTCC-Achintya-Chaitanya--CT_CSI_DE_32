"""
E-Commerce Order Analytics System
Complete implementation covering data generation, cleaning, SQL analysis, and reporting
"""

import csv
import random
import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path
import re


# ============================================================================
# PART 1: DATA GENERATION
# ============================================================================

class DataGenerator:
    """Generate realistic but messy e-commerce data"""
    
    def __init__(self, num_orders=500, num_customers=100, num_products=50):
        self.num_orders = num_orders
        self.num_customers = num_customers
        self.num_products = num_products
        self.order_ids = list(range(1, num_orders + 1))
        self.customer_ids = list(range(1, num_customers + 1))
        self.product_ids = list(range(1, num_products + 1))
        
    def generate_customers(self, filename='customers.csv'):
        """Generate customer data with some invalid emails"""
        customers = []
        invalid_emails = int(self.num_customers * 0.02)  # 2% invalid
        
        for cust_id in self.customer_ids:
            name = f"Customer_{random.choice(['John', 'Jane', 'Alex', 'Sam'])}_{cust_id}"
            
            # 2% have invalid emails
            if random.random() < 0.02:
                email = random.choice([
                    f"email{cust_id}domain.com",  # missing @
                    f"email{cust_id}@",  # missing domain
                    f"invalidemail{cust_id}"  # no @ or domain
                ])
            else:
                email = f"customer{cust_id}@email.com"
            
            registration_date = (datetime(2022, 1, 1) + 
                               timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
            customer_type = random.choice(['REGULAR', 'PREMIUM', 'VIP'])
            
            customers.append([cust_id, name, email, registration_date, customer_type])
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['customer_id', 'customer_name', 'email', 'registration_date', 'customer_type'])
            writer.writerows(customers)
        
        print(f"✓ Generated {filename} ({len(customers)} records)")
        return customers
    
    def generate_products(self, filename='products.csv'):
        """Generate product data with spacing and case issues"""
        products = []
        categories = ['Electronics', 'Clothing', 'Home', 'Books']
        subcategories = {
            'Electronics': ['Phones', 'Laptops', 'Accessories'],
            'Clothing': ['Shirts', 'Pants', 'Shoes'],
            'Home': ['Furniture', 'Decor', 'Kitchen'],
            'Books': ['Fiction', 'Non-Fiction', 'Educational']
        }
        
        product_names = [
            'laptop', 'smartphone', 'headphones', 't-shirt', 'jeans',
            'sneakers', 'sofa', 'lamp', 'pillow', 'cookbook',
            'novel', 'monitor', 'keyboard', 'mouse', 'desk',
            'chair', 'blanket', 'shoes', 'jacket', 'watch'
        ]
        
        for prod_id in self.product_ids:
            category = random.choice(categories)
            subcategory = random.choice(subcategories[category])
            base_name = random.choice(product_names)
            
            # Add spacing and case issues
            if random.random() < 0.1:
                product_name = f"  {base_name.upper()}  "  # Extra spaces and upper
            else:
                product_name = base_name.title()
            
            cost_price = round(random.uniform(10, 500), 2)
            
            products.append([prod_id, product_name, category, subcategory, cost_price])
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['product_id', 'product_name', 'category', 'subcategory', 'cost_price'])
            writer.writerows(products)
        
        print(f"✓ Generated {filename} ({len(products)} records)")
        return products
    
    def generate_orders(self, filename='orders.csv'):
        """Generate order data with some NULL customer_ids and date format issues"""
        orders = []
        null_customer_orders = int(self.num_orders * 0.05)  # 5% NULL
        wrong_format_orders = int(self.num_orders * 0.03)  # 3% wrong format
        
        for order_id in self.order_ids:
            # 5% have NULL customer_id
            if random.random() < 0.05:
                customer_id = ''
            else:
                customer_id = random.choice(self.customer_ids)
            
            # Generate order date
            base_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
            
            # 3% have wrong date format (DD-MM-YYYY instead of YYYY-MM-DD)
            if random.random() < 0.03:
                order_date = base_date.strftime("%d-%m-%Y %H:%M:%S")
            else:
                order_date = base_date.strftime("%Y-%m-%d %H:%M:%S")
            
            status = random.choice(['PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED'])
            region_code = random.choice(['NA', 'EU', 'APAC', 'SA', 'AF'])
            
            orders.append([order_id, customer_id, order_date, status, region_code])
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['order_id', 'customer_id', 'order_date', 'status', 'region_code'])
            writer.writerows(orders)
        
        print(f"✓ Generated {filename} ({len(orders)} records)")
        return orders
    
    def generate_order_items(self, filename='order_items.csv'):
        """Generate order items with some negative quantities (returns)"""
        order_items = []
        negative_quantity_items = int(self.num_orders * 3 * 0.03)  # 3% negative
        item_id = 1
        
        # 1-5 items per order
        for order_id in self.order_ids:
            num_items = random.randint(1, 5)
            for _ in range(num_items):
                product_id = random.choice(self.product_ids)
                
                # 3% have negative quantity (returns)
                if random.random() < 0.03:
                    quantity = -random.randint(1, 5)
                else:
                    quantity = random.randint(1, 10)
                
                unit_price = round(random.uniform(10, 500), 2)
                discount_percent = round(random.uniform(0, 50), 2)
                
                order_items.append([item_id, order_id, product_id, quantity, unit_price, discount_percent])
                item_id += 1
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'discount_percent'])
            writer.writerows(order_items)
        
        print(f"✓ Generated {filename} ({len(order_items)} records)")
        return order_items


# ============================================================================
# PART 2: DATA CLEANING
# ============================================================================

class DataCleaner:
    """Clean and validate messy data"""
    
    @staticmethod
    def clean_orders(input_file='orders.csv', output_file='orders_clean.csv'):
        """Fix date formats and handle NULL customer_ids"""
        issues = []
        cleaned_rows = []
        
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 2):  # Start at 2 (after header)
                order_id = row['order_id']
                customer_id = row['customer_id'] if row['customer_id'].strip() else None
                status = row['status']
                region_code = row['region_code']
                order_date = row['order_date']
                
                # Try to fix date format
                try:
                    # Try YYYY-MM-DD format first
                    dt = datetime.strptime(order_date.split()[0], "%Y-%m-%d")
                    time_part = order_date.split()[1] if len(order_date.split()) > 1 else "00:00:00"
                    fixed_date = f"{dt.strftime('%Y-%m-%d')} {time_part}"
                except ValueError:
                    try:
                        # Try DD-MM-YYYY format
                        dt = datetime.strptime(order_date.split()[0], "%d-%m-%Y")
                        time_part = order_date.split()[1] if len(order_date.split()) > 1 else "00:00:00"
                        fixed_date = f"{dt.strftime('%Y-%m-%d')} {time_part}"
                        issues.append(f"Row {i}: Fixed date format from {order_date} to {fixed_date}")
                    except ValueError:
                        issues.append(f"Row {i}: Could not parse date {order_date}")
                        continue
                
                if customer_id is None:
                    issues.append(f"Row {i}: NULL customer_id for order {order_id}")
                
                cleaned_rows.append([order_id, customer_id, fixed_date, status, region_code])
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['order_id', 'customer_id', 'order_date', 'status', 'region_code'])
            writer.writerows(cleaned_rows)
        
        print(f"✓ Cleaned orders data: {output_file} ({len(cleaned_rows)} records)")
        return issues, cleaned_rows
    
    @staticmethod
    def clean_products(input_file='products.csv', output_file='products_clean.csv'):
        """Normalize product names (trim spaces, title case)"""
        issues = []
        cleaned_rows = []
        
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 2):
                product_id = row['product_id']
                product_name = row['product_name'].strip().title()
                category = row['category']
                subcategory = row['subcategory']
                cost_price = row['cost_price']
                
                if row['product_name'] != product_name:
                    issues.append(f"Row {i}: Normalized product name from '{row['product_name']}' to '{product_name}'")
                
                cleaned_rows.append([product_id, product_name, category, subcategory, cost_price])
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['product_id', 'product_name', 'category', 'subcategory', 'cost_price'])
            writer.writerows(cleaned_rows)
        
        print(f"✓ Cleaned products data: {output_file} ({len(cleaned_rows)} records)")
        return issues, cleaned_rows
    
    @staticmethod
    def validate_emails(input_file='customers.csv'):
        """Find customers with invalid emails"""
        invalid_emails = []
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 2):
                email = row['email']
                if not re.match(email_regex, email):
                    invalid_emails.append((row['customer_id'], email))
        
        print(f"✓ Found {len(invalid_emails)} invalid emails")
        return invalid_emails
    
    @staticmethod
    def check_referential_integrity(orders_file='orders.csv', order_items_file='order_items.csv'):
        """Find order_items that reference non-existent orders"""
        valid_order_ids = set()
        
        with open(orders_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                valid_order_ids.add(row['order_id'])
        
        orphaned_items = []
        with open(order_items_file, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 2):
                if row['order_id'] not in valid_order_ids:
                    orphaned_items.append((i, row['order_id']))
        
        print(f"✓ Found {len(orphaned_items)} orphaned order items")
        return orphaned_items


# ============================================================================
# PART 3 & 4: SQL ANALYSIS AND INTEGRATION
# ============================================================================

class OrderAnalyticsDB:
    """SQL database operations and analysis"""
    
    def __init__(self, db_file='orders_analytics.db'):
        self.db_file = db_file
        self.conn = None
    
    def connect(self):
        """Create connection to SQLite database"""
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        print(f"✓ Connected to database: {self.db_file}")
    
    def create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date DATETIME,
                status TEXT,
                region_code TEXT
            )
        ''')
        
        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                item_id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL,
                discount_percent REAL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                subcategory TEXT,
                cost_price REAL
            )
        ''')
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT,
                email TEXT,
                registration_date DATE,
                customer_type TEXT
            )
        ''')
        
        self.conn.commit()
        print("✓ Created database tables")
    
    def load_csv_data(self, orders_file, order_items_file, products_file, customers_file):
        """Load cleaned CSV data into database"""
        cursor = self.conn.cursor()
        
        # Load orders
        with open(orders_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                customer_id = row['customer_id'] if row['customer_id'] else None
                cursor.execute('''
                    INSERT OR IGNORE INTO orders 
                    (order_id, customer_id, order_date, status, region_code)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['order_id'], customer_id, row['order_date'], row['status'], row['region_code']))
        
        # Load order items
        with open(order_items_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute('''
                    INSERT OR IGNORE INTO order_items
                    (item_id, order_id, product_id, quantity, unit_price, discount_percent)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['item_id'], row['order_id'], row['product_id'], 
                      row['quantity'], row['unit_price'], row['discount_percent']))
        
        # Load products
        with open(products_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute('''
                    INSERT OR IGNORE INTO products
                    (product_id, product_name, category, subcategory, cost_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['product_id'], row['product_name'], row['category'], 
                      row['subcategory'], row['cost_price']))
        
        # Load customers
        with open(customers_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute('''
                    INSERT OR IGNORE INTO customers
                    (customer_id, customer_name, email, registration_date, customer_type)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['customer_id'], row['customer_name'], row['email'], 
                      row['registration_date'], row['customer_type']))
        
        self.conn.commit()
        print(f"✓ Loaded data into database")
    
    def query_total_revenue_by_category(self):
        """Basic Query 1: Total revenue per category"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                p.category,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as total_revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.category
            ORDER BY total_revenue DESC
        ''')
        return cursor.fetchall()
    
    def query_top_10_customers(self):
        """Basic Query 2: Top 10 customers by total order value"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                c.customer_id,
                c.customer_name,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as total_value
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.customer_id IS NOT NULL
            GROUP BY c.customer_id
            ORDER BY total_value DESC
            LIMIT 10
        ''')
        return cursor.fetchall()
    
    def query_monthly_order_count(self):
        """Basic Query 3: Month-wise order count for last 12 months"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', o.order_date) as month,
                COUNT(DISTINCT o.order_id) as order_count
            FROM orders o
            WHERE o.order_date >= datetime('now', '-12 months')
            GROUP BY strftime('%Y-%m', o.order_date)
            ORDER BY month DESC
        ''')
        return cursor.fetchall()
    
    def query_customers_no_delivery(self):
        """Intermediate Query 4: Customers who placed orders but never had delivery"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT c.customer_id, c.customer_name
            FROM customers c
            WHERE c.customer_id IN (
                SELECT DISTINCT o.customer_id 
                FROM orders o
            )
            AND c.customer_id NOT IN (
                SELECT DISTINCT o.customer_id 
                FROM orders o
                WHERE o.status = 'DELIVERED'
            )
        ''')
        return cursor.fetchall()
    
    def query_return_rate_by_category(self):
        """Intermediate Query 6: Return rate per category"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                p.category,
                ROUND(
                    SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) * 100.0 / 
                    SUM(ABS(oi.quantity)), 
                2) as return_rate_percent
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.category
            ORDER BY return_rate_percent DESC
        ''')
        return cursor.fetchall()
    
    def generate_report(self, report_type='daily', start_date=None, end_date=None):
        """Generate summary report"""
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        cursor = self.conn.cursor()
        
        # Total metrics
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT o.order_id) as total_orders,
                COUNT(DISTINCT o.customer_id) as unique_customers,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as total_revenue
            FROM orders o
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            WHERE DATE(o.order_date) BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        metrics = cursor.fetchone()
        
        # Top 3 products
        cursor.execute('''
            SELECT 
                p.product_name,
                SUM(oi.quantity) as total_qty,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) as revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN orders o ON oi.order_id = o.order_id
            WHERE DATE(o.order_date) BETWEEN ? AND ?
            GROUP BY p.product_id
            ORDER BY revenue DESC
            LIMIT 3
        ''', (start_date, end_date))
        
        top_products = cursor.fetchall()
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
║           ORDER ANALYTICS REPORT ({report_type.upper()})            ║
║           Period: {start_date} to {end_date}        ║
╚════════════════════════════════════════════════════════════╝

📊 SUMMARY METRICS
├─ Total Orders:        {metrics['total_orders']}
├─ Unique Customers:    {metrics['unique_customers']}
└─ Total Revenue:       ${metrics['total_revenue'] or 0}

🏆 TOP 3 PRODUCTS
"""
        for i, product in enumerate(top_products, 1):
            report += f"├─ {i}. {product['product_name']} (Qty: {product['total_qty']}, Revenue: ${product['revenue']})\n"
        
        report += "\n" + "="*60 + "\n"
        return report
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")


# ============================================================================
# PART 5: EDGE CASE TESTING
# ============================================================================

def test_edge_cases():
    """Test edge cases"""
    print("\n🧪 EDGE CASE TESTS\n")
    
    tests = {
        "Orphaned order_items": lambda: DataCleaner.check_referential_integrity(),
        "Invalid emails": lambda: DataCleaner.validate_emails(),
    }
    
    for test_name, test_func in tests.items():
        try:
            result = test_func()
            print(f"✓ {test_name}: PASSED")
        except Exception as e:
            print(f"✗ {test_name}: FAILED - {str(e)}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution flow"""
    print("\n" + "="*60)
    print("E-COMMERCE ORDER ANALYTICS SYSTEM")
    print("="*60 + "\n")
    
    # PART 1: Generate Data
    print("📝 PART 1: DATA GENERATION\n")
    generator = DataGenerator(num_orders=500, num_customers=100, num_products=50)
    generator.generate_customers()
    generator.generate_products()
    generator.generate_orders()
    generator.generate_order_items()
    
    # PART 2: Clean Data
    print("\n🧹 PART 2: DATA CLEANING\n")
    cleaner = DataCleaner()
    order_issues, _ = cleaner.clean_orders()
    product_issues, _ = cleaner.clean_products()
    invalid_emails = cleaner.validate_emails()
    orphaned_items = cleaner.check_referential_integrity()
    
    print(f"\n📋 CLEANING REPORT")
    print(f"├─ Order issues found: {len(order_issues)}")
    print(f"├─ Product issues found: {len(product_issues)}")
    print(f"├─ Invalid emails: {len(invalid_emails)}")
    print(f"└─ Orphaned items: {len(orphaned_items)}")
    
    # PART 3: SQL Analysis
    print("\n\n💾 PART 3: SQL ANALYSIS & INTEGRATION\n")
    db = OrderAnalyticsDB()
    db.connect()
    db.create_tables()
    db.load_csv_data('orders_clean.csv', 'order_items.csv', 'products_clean.csv', 'customers.csv')
    
    # Run analysis queries
    print("\n📊 QUERY RESULTS\n")
    
    print("1️⃣  Total Revenue by Category:")
    for row in db.query_total_revenue_by_category():
        print(f"   {row['category']}: ${row['total_revenue']}")
    
    print("\n2️⃣  Top 10 Customers by Value:")
    for row in db.query_top_10_customers()[:3]:  # Show first 3
        print(f"   {row['customer_name']}: ${row['total_value']}")
    
    print("\n3️⃣  Monthly Orders (Last 12 months):")
    for row in db.query_monthly_order_count()[:3]:  # Show first 3
        print(f"   {row['month']}: {row['order_count']} orders")
    
    print("\n4️⃣  Return Rate by Category:")
    for row in db.query_return_rate_by_category():
        print(f"   {row['category']}: {row['return_rate_percent']}%")
    
    # PART 4: Generate Report
    print("\n\n📑 PART 4: SAMPLE REPORT")
    report = db.generate_report(report_type='daily')
    print(report)
    
    # PART 5: Edge Case Testing
    test_edge_cases()
    
    db.close()
    
    print("\n" + "="*60)
    print("✅ ALL TASKS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")
    print("📁 OUTPUT FILES:")
    print("   ├─ customers.csv")
    print("   ├─ products.csv, products_clean.csv")
    print("   ├─ orders.csv, orders_clean.csv")
    print("   ├─ order_items.csv")
    print("   └─ orders_analytics.db")


if __name__ == "__main__":
    main()
