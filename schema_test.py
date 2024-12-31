import psycopg2
import sys

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': '1194',
    'user': 'dms_user',
    'password': 'post0253',
    'database': 'postgres'
}

# Expected schema for the table
EXPECTED_SCHEMA = {
    'orders': {
        'columns': {
            'transaction_id': 'text',
            'customer_id': 'character varying',
            'product_id': 'character varying',
            'transaction_date': 'date',
            'units_sold': 'numeric',
            'discount_applied': 'numeric',
            'revenue': 'numeric',
            'clicks': 'numeric',
            'impressions': 'numeric',
            'conversion_rate': 'numeric',
            'ad_cpc': 'numeric',
            'ad_spend': 'numeric'
        }
    }
}


def test_schema():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Check if table exists
        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'orders')")
        if not cursor.fetchone()[0]:
            print("Table 'orders' does not exist!")
            sys.exit(1)  # Exit with error code 1 to stop the pipeline

        # Check columns and types
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'orders'")
        columns = {col[0]: col[1] for col in cursor.fetchall()}
        for column, expected_type in EXPECTED_SCHEMA['orders']['columns'].items():
            if column not in columns:
                print(f"Column '{column}' is missing!")
                sys.exit(1)  # Exit with error code 1 to stop the pipeline
            elif columns[column] != expected_type:
                print(f"Column '{column}' type mismatch: expected '{expected_type}', found '{columns[column]}'")
                sys.exit(1)  # Exit with error code 1 to stop the pipeline
            else:
                print(f"Column '{column}' is correct.")
    
    except psycopg2.Error as err:
        print(f"Error: {err}")
        sys.exit(1)  # Exit with error code 1 to stop the pipeline
    
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    test_schema()
