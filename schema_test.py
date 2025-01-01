import mysql.connector
import sys

# Database connection configuration
DB_CONFIG = {
    'host': 'mysql-db.c3s2sg2mo7cc.us-east-1.rds.amazonaws.com',
    'port': '3306',
    'user': 'dms_user',
    'password': 'mysql0253',
    'database': 'devops'
}

# Expected schema for the table
EXPECTED_SCHEMA = {
    'orders': {
        'columns': {
            'transaction_id': 'text',
            'customer_id': 'varchar(255)',
            'product_id': 'varchar(255)',
            'transaction_date': 'date',
            'units_sold': 'decimal(10,2)',
            'discount_applied': 'decimal(5,2)',
            'revenue': 'decimal(10,2)',
            'clicks': 'int',
            'impressions': 'int',
            'conversion_rate': 'decimal(5,2)',
            'ad_cpc': 'decimal(5,2)',
            'ad_spend': 'decimal(10,2)'
        }
    }
}

def test_schema():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'orders'")
        if not cursor.fetchone():
            print("Table 'orders' does not exist!")
            sys.exit(1)  # Exit with error code 1 to stop the pipeline

        # Check columns and types
        cursor.execute("DESCRIBE orders")
        columns = {col[0]: col[1].decode('utf-8') if isinstance(col[1], bytes) else col[1] for col in cursor.fetchall()}

        for column, expected_type in EXPECTED_SCHEMA['orders']['columns'].items():
            if column not in columns:
                print(f"Column '{column}' is missing!")
                sys.exit(1)  # Exit with error code 1 to stop the pipeline
            elif not columns[column].startswith(expected_type):
                print(f"Column '{column}' type mismatch: expected '{expected_type}', found '{columns[column]}'")
                sys.exit(1)  # Exit with error code 1 to stop the pipeline
            else:
                print(f"Column '{column}' is correct.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)  # Exit with error code 1 to stop the pipeline
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    test_schema()
