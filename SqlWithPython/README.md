# SQL Server Database Connection with Python
This project demonstrates how to connect to a SQL Server database using Python and the pyodbc library. The Python script uses environment variables to securely manage database credentials. The project includes sample queries to interact with a SQL Server database.

# Features
Connect to SQL Server databases using Python.

Execute SQL queries to fetch and manipulate data.

Read credentials and connection details from a .env file.

# Prerequisites
Before running the project, make sure you have the following:

Python 3.13.3 installed.

SQL Server and SQL Server Management Studio (SSMS) installed.

AdventureWorks database installed in your SQL Server instance.

SQL Server ODBC driver installed on your machine (make sure to download the correct version based on your SQL Server version).

# Step 1: Install SQL Server and SSMS
Download and Install SQL Server:

Download SQL Server from the official Microsoft website: SQL Server Downloads.

Follow the installation steps and select the Developer edition.

Download and Install SQL Server Management Studio (SSMS):

Download SSMS from the official Microsoft website: SSMS Downloads.

SSMS is used to manage SQL Server instances and databases.

# Step 2: Install AdventureWorks Database
The AdventureWorks database is a sample database that is commonly used for learning SQL Server.

Download AdventureWorks Database:

Download the AdventureWorksDW2022 database for your SQL Server version from the Microsoft GitHub repository: AdventureWorks GitHub.

Select the appropriate .bak file for your version of SQL Server.

Restore the AdventureWorks Database:

Open SSMS and connect to your SQL Server instance.

In SSMS, right-click on the "Databases" folder and select "Restore Database".

Choose the AdventureWorks .bak file you downloaded and restore it to your SQL Server instance.

After restoring the database, the AdventureWorksDW2022 database will be available to use.

# Step 3: Clone the Repository
Clone the repository to your local machine:

git clone https://github.com/BhanuSri-infomagnus/Bootcamp.git
cd Bootcamp

# Step 4: Create a Virtual Environment
Create a virtual environment to manage dependencies:

python -m venv venv

Activate the virtual environment:

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

# Step 5: Install Dependencies
Install the required Python libraries:

pip install -r requirements.txt

# Step 6: Configure Environment Variables
Copy the .env.example file and rename it to .env.

cp .env.example .env

Open the .env file and replace the placeholder values with your actual database credentials:

UID=your_sql_username
password_value=your_sql_password
SERVER=your_sql_server_name\SQLEXPRESS
DATABASE=AdventureWorksDW2022

# Step 7: Run the Script
Run the Python script to test the connection to the SQL Server:

python sql_connection.py

# Step 8: Sample Queries
The script will execute the following SQL queries:

Count distinct employees:

Query: SELECT count(distinct EmployeeKey) FROM DimEmployee

Count employees by gender:

Query: SELECT gender, count(distinct EmployeeKey) FROM DimEmployee GROUP BY gender

Count currently active employees:

Query: SELECT count(distinct EmployeeKey) FROM DimEmployee WHERE Status='current'

Get the top 10 employees:

Query: SELECT TOP 10 concat(FirstName, LastName) FROM DimEmployee

# Example Output
When running the script, you should expect output similar to this:

Total distinct employees: 1000
Employees by gender:
('M', 600)
('F', 400)
Currently active employees: 800
Top 10 employees:
JohnDoe
JaneSmith
...
Database connection closed.

# Requirements
pyodbc – Python ODBC interface for connecting to SQL databases.

python-dotenv – Python library for reading .env files and managing environment variables.

You can install them using pip:

pip install pyodbc python-dotenv
