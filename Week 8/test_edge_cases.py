"""
Edge Case Testing and Data Quality Validation
Tests for Part 5 of the e-commerce analytics project
"""

import sqlite3
import csv
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any


class EdgeCaseValidator:
    """Validate edge cases and data quality"""
    
    def __init__(self, db_file='orders_analytics.db'):
        self.db_file = db_file
        self.conn = None
        self.test_results = []
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
    
    def run_test(self, test_name: str, test_func):
        """Run a single test and record result"""
        try:
            result = test_func()
            status = "✓ PASS" if result['passed'] else "✗ FAIL"
            self.test_results.append({
                'name': test_name,
                'status': status,
                'details': result.get('message', ''),
                'issues_found': result.get('count', 0)
            })
            print(f"{status} - {test_name}: {result.get('message', '')}")
            return result
        except Exception as e:
            self.test_results.append({
                'name': test_name,
                'status': '✗ ERROR',
                'details': str(e),
                'issues_found': 0
            })
            print(f"✗ ERROR - {test_name}: {str(e)}")
            return {'passed': False, 'message': str(e), 'count': 0}
    
    # ========== TEST CASE 1: Orphaned order_items ==========
    def test_orphaned_order_items(self) -> Dict[str, Any]:
        """What happens when order_items has an order_id not in orders?"""
        cursor = self.conn.cursor()
        
        # Find order_items with order_id not in orders
        cursor.execute('''
            SELECT COUNT(*) as orphaned_count
            FROM order_items oi
            WHERE oi.order_id NOT IN (SELECT order_id FROM orders)
        ''')
        
        result = cursor.fetchone()
        orphaned_count = result['orphaned_count'] if result else 0
        
        return {
            'passed': orphaned_count == 0,
            'message': f"Found {orphaned_count} orphaned items (expected 0)",
            'count': orphaned_count
        }
    
    # ========== TEST CASE 2: Invalid discount percentages ==========
    def test_invalid_discount_percent(self) -> Dict[str, Any]:
        """What happens when discount_percent > 100?"""
        cursor = self.conn.cursor()
        
        # Find invalid discounts
        cursor.execute('''
            SELECT COUNT(*) as invalid_count
            FROM order_items
            WHERE discount_percent < 0 OR discount_percent > 100
        ''')
        
        result = cursor.fetchone()
        invalid_count = result['invalid_count'] if result else 0
        
        return {
            'passed': invalid_count == 0,
            'message': f"Found {invalid_count} invalid discounts (expected 0)",
            'count': invalid_count
        }
    
    # ========== TEST CASE 3: Zero or negative quantity ==========
    def test_invalid_quantity(self) -> Dict[str, Any]:
        """What happens when quantity is 0?"""
        cursor = self.conn.cursor()
        
        # Find zero quantity items
        cursor.execute('''
            SELECT COUNT(*) as zero_count
            FROM order_items
            WHERE quantity = 0
        ''')
        
        result = cursor.fetchone()
        zero_count = result['zero_count'] if result else 0
        
        # Note: Negative quantities are valid (returns)
        # Zero is questionable - an item that wasn't ordered?
        
        return {
            'passed': zero_count == 0,
            'message': f"Found {zero_count} zero-quantity items",
            'count': zero_count
        }
    
    # ========== TEST CASE 4: Future order dates ==========
    def test_future_order_dates(self) -> Dict[str, Any]:
        """What happens when order_date is in the future?"""
        cursor = self.conn.cursor()
        
        # Find orders with dates in future
        cursor.execute('''
            SELECT COUNT(*) as future_count
            FROM orders
            WHERE order_date > datetime('now')
        ''')
        
        result = cursor.fetchone()
        future_count = result['future_count'] if result else 0
        
        return {
            'passed': future_count == 0,
            'message': f"Found {future_count} future-dated orders (expected 0)",
            'count': future_count
        }
    
    # ========== Additional Test Cases ==========
    
    def test_missing_customer_id(self) -> Dict[str, Any]:
        """Check for NULL customer_ids in orders"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as null_count
            FROM orders
            WHERE customer_id IS NULL
        ''')
        
        result = cursor.fetchone()
        null_count = result['null_count'] if result else 0
        
        # Some NULL customer_ids are expected (5% in generation)
        is_valid = 0 <= null_count <= (500 * 0.05 * 1.5)  # Allow 50% margin
        
        return {
            'passed': is_valid,
            'message': f"Found {null_count} NULL customer_ids (~5% expected)",
            'count': null_count
        }
    
    def test_invalid_email_format(self) -> Dict[str, Any]:
        """Check for invalid email addresses"""
        import re
        cursor = self.conn.cursor()
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        cursor.execute('SELECT email FROM customers')
        rows = cursor.fetchall()
        
        invalid_count = 0
        for row in rows:
            if not re.match(email_regex, row['email']):
                invalid_count += 1
        
        # ~2% invalid emails expected
        is_valid = 0 <= invalid_count <= (100 * 0.02 * 1.5)  # Allow 50% margin
        
        return {
            'passed': is_valid,
            'message': f"Found {invalid_count} invalid emails (~2% expected)",
            'count': invalid_count
        }
    
    def test_negative_quantities_are_returns(self) -> Dict[str, Any]:
        """Verify negative quantities are properly identified"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN quantity < 0 THEN 1 END) as return_count,
                COUNT(CASE WHEN quantity > 0 THEN 1 END) as sales_count
            FROM order_items
        ''')
        
        result = cursor.fetchone()
        return_count = result['return_count']
        sales_count = result['sales_count']
        
        # Returns should be ~3% of items
        return_percent = (return_count / (return_count + sales_count) * 100) if (return_count + sales_count) > 0 else 0
        is_valid = 0 <= return_percent <= 5  # 3% expected, allow up to 5%
        
        return {
            'passed': is_valid,
            'message': f"Returns: {return_count} ({return_percent:.1f}%), Sales: {sales_count}",
            'count': return_count
        }
    
    def test_revenue_calculation_accuracy(self) -> Dict[str, Any]:
        """Verify revenue calculations are correct"""
        cursor = self.conn.cursor()
        
        # Check for any invalid revenue values (NaN, infinite, etc.)
        cursor.execute('''
            SELECT 
                COUNT(*) as total_items,
                COUNT(CASE WHEN 
                    (quantity * unit_price * (1 - discount_percent/100.0)) >= 0 
                    OR quantity < 0
                THEN 1 END) as valid_revenues
            FROM order_items
        ''')
        
        result = cursor.fetchone()
        total = result['total_items']
        valid = result['valid_revenues']
        
        is_valid = total == valid
        
        return {
            'passed': is_valid,
            'message': f"Valid revenue calculations: {valid}/{total}",
            'count': total - valid
        }
    
    def test_order_item_product_fk(self) -> Dict[str, Any]:
        """Check for invalid product_id references"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as invalid_count
            FROM order_items oi
            WHERE oi.product_id NOT IN (SELECT product_id FROM products)
        ''')
        
        result = cursor.fetchone()
        invalid_count = result['invalid_count'] if result else 0
        
        return {
            'passed': invalid_count == 0,
            'message': f"Invalid product references: {invalid_count}",
            'count': invalid_count
        }
    
    def test_date_format_consistency(self) -> Dict[str, Any]:
        """Check if all dates are in proper format"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT order_date FROM orders')
        rows = cursor.fetchall()
        
        invalid_count = 0
        for row in rows:
            try:
                datetime.strptime(row['order_date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    datetime.strptime(row['order_date'].split()[0], '%Y-%m-%d')
                except ValueError:
                    invalid_count += 1
        
        return {
            'passed': invalid_count == 0,
            'message': f"Invalid date formats: {invalid_count}",
            'count': invalid_count
        }
    
    def test_price_values_positive(self) -> Dict[str, Any]:
        """Check that prices are positive"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as negative_count
            FROM order_items
            WHERE unit_price <= 0
        ''')
        
        result = cursor.fetchone()
        negative_count = result['negative_count'] if result else 0
        
        return {
            'passed': negative_count == 0,
            'message': f"Negative prices found: {negative_count}",
            'count': negative_count
        }
    
    def test_no_duplicate_order_items(self) -> Dict[str, Any]:
        """Check for duplicate item_ids"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as dup_count
            FROM (
                SELECT item_id, COUNT(*) as cnt
                FROM order_items
                GROUP BY item_id
                HAVING cnt > 1
            )
        ''')
        
        result = cursor.fetchone()
        dup_count = result['dup_count'] if result else 0
        
        return {
            'passed': dup_count == 0,
            'message': f"Duplicate item_ids: {dup_count}",
            'count': dup_count
        }
    
    def test_order_status_values(self) -> Dict[str, Any]:
        """Check that all order statuses are valid"""
        valid_statuses = {'PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED'}
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT status
            FROM orders
        ''')
        
        rows = cursor.fetchall()
        invalid_statuses = set()
        for row in rows:
            if row['status'] not in valid_statuses:
                invalid_statuses.add(row['status'])
        
        return {
            'passed': len(invalid_statuses) == 0,
            'message': f"Invalid statuses: {invalid_statuses if invalid_statuses else 'None'}",
            'count': len(invalid_statuses)
        }
    
    def test_customer_type_values(self) -> Dict[str, Any]:
        """Check that customer types are valid"""
        valid_types = {'REGULAR', 'PREMIUM', 'VIP'}
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT customer_type
            FROM customers
        ''')
        
        rows = cursor.fetchall()
        invalid_types = set()
        for row in rows:
            if row['customer_type'] not in valid_types:
                invalid_types.add(row['customer_type'])
        
        return {
            'passed': len(invalid_types) == 0,
            'message': f"Invalid customer types: {invalid_types if invalid_types else 'None'}",
            'count': len(invalid_types)
        }
    
    def test_region_code_values(self) -> Dict[str, Any]:
        """Check that region codes are valid"""
        valid_regions = {'NA', 'EU', 'APAC', 'SA', 'AF'}
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT region_code
            FROM orders
        ''')
        
        rows = cursor.fetchall()
        invalid_regions = set()
        for row in rows:
            if row['region_code'] not in valid_regions:
                invalid_regions.add(row['region_code'])
        
        return {
            'passed': len(invalid_regions) == 0,
            'message': f"Invalid regions: {invalid_regions if invalid_regions else 'None'}",
            'count': len(invalid_regions)
        }
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for r in self.test_results if 'PASS' in r['status'])
        failed = sum(1 for r in self.test_results if 'FAIL' in r['status'])
        errors = sum(1 for r in self.test_results if 'ERROR' in r['status'])
        
        print(f"\n📊 Results:")
        print(f"  ✓ Passed: {passed}")
        print(f"  ✗ Failed: {failed}")
        print(f"  ⚠ Errors: {errors}")
        print(f"  Total:   {len(self.test_results)}")
        
        total_issues = sum(r['issues_found'] for r in self.test_results)
        print(f"\n📋 Total Issues Found: {total_issues}")
        
        if failed > 0 or errors > 0:
            print("\n⚠️  Failed/Error Tests:")
            for r in self.test_results:
                if 'FAIL' in r['status'] or 'ERROR' in r['status']:
                    print(f"  - {r['name']}: {r['details']}")
        
        print("\n" + "="*70)
    
    def run_all_tests(self):
        """Run all edge case tests"""
        print("\n" + "="*70)
        print("🧪 EDGE CASE VALIDATION TESTS")
        print("="*70 + "\n")
        
        tests = [
            ("Orphaned Order Items (FK constraint)", self.test_orphaned_order_items),
            ("Invalid Discount Percentages (>100)", self.test_invalid_discount_percent),
            ("Zero Quantity Items", self.test_invalid_quantity),
            ("Future Order Dates", self.test_future_order_dates),
            ("Missing Customer IDs", self.test_missing_customer_id),
            ("Invalid Email Format", self.test_invalid_email_format),
            ("Negative Quantities as Returns", self.test_negative_quantities_are_returns),
            ("Revenue Calculation Accuracy", self.test_revenue_calculation_accuracy),
            ("Product Foreign Key References", self.test_order_item_product_fk),
            ("Date Format Consistency", self.test_date_format_consistency),
            ("Positive Price Values", self.test_price_values_positive),
            ("No Duplicate Item IDs", self.test_no_duplicate_order_items),
            ("Valid Order Statuses", self.test_order_status_values),
            ("Valid Customer Types", self.test_customer_type_values),
            ("Valid Region Codes", self.test_region_code_values),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        self.print_summary()


def main():
    """Main execution"""
    validator = EdgeCaseValidator()
    validator.connect()
    validator.run_all_tests()
    validator.close()


if __name__ == "__main__":
    main()
