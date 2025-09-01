import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read credentials and settings from environment variables
USERID = os.getenv("USERID")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
# Create the connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERID};"
    f"PWD={PASSWORD};"
)

try:
    # Attempt to connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Query 1: Count distinct EmployeeKey
    cursor.execute("SELECT count(distinct EmployeeKey) FROM DimEmployee")
    for row in cursor.fetchall():
        print("Total distinct employees:", row[0])

    # Query 2: Count by gender
    cursor.execute("SELECT gender, count(distinct EmployeeKey) FROM DimEmployee GROUP BY gender")
    print("Employees by gender:")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")

    # Query 3: Count where status = 'current'
    cursor.execute("SELECT count(distinct EmployeeKey) FROM DimEmployee WHERE Status='current'")
    for row in cursor.fetchall():
        print("Currently active employees:", row[0])

    # Query 4: Top 10 full names
    cursor.execute("SELECT TOP 10 CONCAT(FirstName, ' ', LastName) FROM DimEmployee")
    print("Top 10 employees:")
    for row in cursor.fetchall():
        print(row[0])

    # Query 5: Employees and their managers
    cursor.execute("""
        SELECT a.EmployeeFullName as Employee, b.EmployeeFullName as Manager
        FROM DimEmployee as a
        JOIN DimEmployee as b ON a.ParentEmployeeKey = b.EmployeeKey
    """)
    print("Employees and their managers:")
    for row in cursor.fetchall():
        print(f"{row.Employee} reports to {row.Manager}")

except pyodbc.Error as e:
    print("Database error occurred:", e)
except Exception as ex:
    print("An unexpected error occurred:", ex)
finally:
    # Close the connection
    if(conn):
        conn.close()
        print("Database connection closed.")
