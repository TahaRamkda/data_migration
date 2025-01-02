import pandas as pd
from sqlalchemy import create_engine
import sys  # Required for exiting with a specific exit code

# PostgreSQL connection
pg_engine = create_engine('postgresql://dms_user:post0253@openvpn-ip:1194/postgres')

# MySQL connection
mysql_engine = create_engine('mysql+pymysql://admin:target-endpoint:3306/dbname')

try:
    # Fetch data from PostgreSQL
    print("Fetching data from PostgreSQL 'orders' table...")
    df = pd.read_sql('SELECT * FROM orders', pg_engine)

    # Verify data is loaded
    if df.empty:
        raise ValueError("No data found in the 'orders' table!")

    print(f"Data fetched successfully! Rows fetched: {len(df)}")

    # Insert data into MySQL
    print("Appending data to MySQL 'orders' table...")
    df.to_sql('orders', mysql_engine, if_exists='append', index=False)

    print("Data transfer completed successfully!")

except Exception as e:
    print(f"An error occurred during the migration: {e}")
    sys.exit(1)  # Exit with status code 1 to indicate failure
