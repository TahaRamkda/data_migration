import psycopg2
import mysql.connector

# PostgreSQL connection details
pg_host = "172.27.236.3"
pg_db = "postgres"
pg_user = "dms_user"
pg_password = "post0253"
port = "1194"

# MySQL connection details
mysql_host = "mysql-db.c3s2sg2mo7cc.us-east-1.rds.amazonaws.com"  # Example: 'your-aws-mysql-endpoint'
mysql_db = "mysql"
mysql_user = "admin"
mysql_password = "mysql0253"
mysql_port= "3306"

try:
    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(
        host=pg_host,
        database=pg_db,
        user=pg_user,
        password=pg_password,
        port=port
    )
    pg_cursor = pg_conn.cursor()

    # Connect to MySQL
    mysql_conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db,
        port=mysql_port
    )
    mysql_cursor = mysql_conn.cursor()

    # Get column details from PostgreSQL table 'orders'
    pg_cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'orders';")
    columns = pg_cursor.fetchall()

    if not columns:
        raise Exception("No columns found for the 'orders' table in PostgreSQL.")

    create_table_sql = "CREATE TABLE IF NOT EXISTS orders ("

    # Convert PostgreSQL column types to MySQL types
    for column in columns:
        column_name = column[0]
        column_type = column[1]

        if column_type == "character varying":
            column_type = "VARCHAR(255)"
        elif column_type == "integer":
            column_type = "INT"
        elif column_type == "date":
            column_type = "DATE"
        elif column_type == "numeric":
            column_type = "DECIMAL(10, 2)"
        elif column_type == "text":
            column_type = "TEXT"
        elif column_type == "double precision":
            column_type = "DOUBLE"
        else:
            # Handle any types that aren't explicitly mapped
            column_type = "TEXT"  # Default fallback

        create_table_sql += f"{column_name} {column_type}, "

    # Remove the last comma and add the closing parenthesis
    create_table_sql = create_table_sql.rstrip(', ') + ");"

    # Execute the SQL query to create the table in MySQL
    mysql_cursor.execute(create_table_sql)
    mysql_conn.commit()

    print("Table 'orders' successfully created in MySQL.")

except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    # Close connections
    if 'pg_cursor' in locals():
        pg_cursor.close()
    if 'pg_conn' in locals():
        pg_conn.close()

    if 'mysql_cursor' in locals():
        mysql_cursor.close()
    if 'mysql_conn' in locals():
        mysql_conn.close()
