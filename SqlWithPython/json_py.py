# Import required libraries
import pyodbc
import os
from dotenv import load_dotenv  # Used to load environment variables from a .env file

class DatabaseConnector:
    def __init__(self, env_file=".env"):
        """
        Initialize the database connection using environment variables.
        Reads server, database, username, and password from the .env file.
        """
        # Load environment variables from the specified .env file
        load_dotenv(env_file)
        
        # Retrieve database connection details from environment variables
        self.server = os.getenv("SERVER")
        self.database = os.getenv("DATABASE")
        self.username = os.getenv("USERID")
        self.password = os.getenv("PASSWORD")
        
        # Raise an error if any required environment variable is missing
        if not all([self.server, self.database, self.username, self.password]):
            raise ValueError("Missing required database connection parameters in environment")
            
        # Establish a connection to the SQL Server database using pyodbc
        self.conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'  # SQL Server ODBC driver
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password}'
        )
        # Create a cursor object to execute SQL queries
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query, params=None):
        """
        Execute a SQL query (e.g., INSERT, UPDATE, DELETE) with optional parameters.
        Commits changes to the database if successful.
        Rolls back in case of an error.
        """
        try:
            if params:
                self.cursor.execute(query, params)  # Execute with parameters
            else:
                self.cursor.execute(query)  # Execute without parameters
            self.conn.commit()  # Commit the transaction
            return True
        except pyodbc.Error as e:
            print(f"Query execution error: {e}")
            self.conn.rollback()  # Rollback in case of error
            return False
    
    def fetch_data(self, query, params=None):
        """
        Execute a SELECT query and return all fetched results.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()  # Fetch all rows
        except pyodbc.Error as e:
            print(f"Data fetch error: {e}")
            return None
    
    def close(self):
        """
        Close the cursor and the database connection to release resources.
        """
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
