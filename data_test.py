import psycopg2
import mysql.connector
import sys

# Database connection configurations
SOURCE_DB_CONFIG = {
    'host': '172.27.232.4',
    'user': 'dms_user',
    'password': 'post0253',
    'database': 'postgres',
    'post':'1194'
}

TARGET_DB_CONFIG = {
    'host': 'mysql-db.c3s2sg2mo7cc.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'mysql0253',
    'database': 'mysql'
}

# Table and columns to validate
TABLE_NAME = 'orders'
KEY_COLUMNS = ['transaction_id', 'customer_id', 'product_id', 'transaction_date']

def fetch_psql_data(cursor, table_name, key_columns):
    query = f"SELECT {', '.join(key_columns)} FROM {table_name} ORDER BY {', '.join(key_columns)}"
    cursor.execute(query)
    return cursor.fetchall()

def fetch_mysql_data(cursor, table_name, key_columns):
    query = f"SELECT {', '.join(key_columns)} FROM {table_name} ORDER BY {', '.join(key_columns)}"
    cursor.execute(query)
    return cursor.fetchall()

def validate_data():
    try:
        # Connect to source (PostgreSQL) and target (MySQL) databases
        source_conn = psycopg2.connect(**SOURCE_DB_CONFIG)
        target_conn = mysql.connector.connect(**TARGET_DB_CONFIG)
        source_cursor = source_conn.cursor()
        target_cursor = target_conn.cursor()

        # Fetch data from source and target
        source_data = fetch_psql_data(source_cursor, TABLE_NAME, KEY_COLUMNS)
        target_data = fetch_mysql_data(target_cursor, TABLE_NAME, KEY_COLUMNS)

        # Check row counts
        if len(source_data) != len(target_data):
            print(f"Row count mismatch: Source({len(source_data)}) vs Target({len(target_data)})")
            sys.exit(1)  # Exit with error code 1

        # Compare data row by row
        for src_row, tgt_row in zip(source_data, target_data):
            if src_row != tgt_row:
                print(f"Data mismatch found: Source{src_row} vs Target{tgt_row}")
                sys.exit(1)  # Exit with error code 1

        print("Data validation successful: All rows match!")
    
    except (psycopg2.Error, mysql.connector.Error) as err:
        print(f"Error: {err}")
        sys.exit(1)  # Exit with error code 1

    finally:
        # Close connections
        if source_cursor: source_cursor.close()
        if source_conn: source_conn.close()
        if target_cursor: target_cursor.close()
        if target_conn: target_conn.close()

if __name__ == "__main__":
    validate_data()
