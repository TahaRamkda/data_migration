import psycopg2
import mysql.connector

# PostgreSQL connection details
pg_host = "172.27.232.2"
pg_db = "postgres"
pg_user = "dms_user"
pg_password = "post0253"
port = "1194"

# MySQL connection details
mysql_host = "mysql-db.c3s2sg2mo7cc.us-east-1.rds.amazonaws.com"  # Example: 'your-aws-mysql-endpoint'
mysql_db = "mysql"
mysql_user = "admin"
mysql_password = "mysql0253"

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
    database=mysql_db
)
mysql_cursor = mysql_conn.cursor()

pg_cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'orders';")
columns = pg_cursor.fetchall()

create_table_sql = "CREATE TABLE IF NOT EXISTS orders ("

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

    
    create_table_sql += f"{column_name} {column_type}, "

# Remove the last comma and add the closing parenthesis
create_table_sql = create_table_sql.rstrip(', ') + ");"

# Step 3: Execute the SQL query to create the table in MySQL
mysql_cursor.execute(create_table_sql)
mysql_conn.commit()

# Step 4: Close connections
pg_cursor.close()
pg_conn.close()
mysql_cursor.close()
mysql_conn.close()

print("Table 'orders' successfully created in MySQL.")
