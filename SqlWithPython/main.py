# Import custom DatabaseConnector class for DB operations
from json_py import DatabaseConnector  

# Import required libraries
import json
import os
from dotenv import load_dotenv  # Used to load environment variables from a .env file

# Main function to execute the database update and fetch operations
def main():
    # Load environment variables from the .env file (like DB credentials)
    load_dotenv()
    
    try:
        # Initialize the database connector
        db = DatabaseConnector()
        
        # Sample country data in JSON format to be inserted/updated into the database
        country_data = {
            "country": "Afghanistan",
            "capital": "Kabul",
            "currency": "AFA",
            "languages": ["Pashto", "Dari"]
        }
        
        # Update the DimCurrency table with the JSON data for a specific currency
        print("Updating JSON data...")
        update_success = db.execute_query(
            "UPDATE DimCurrency SET Country = ? WHERE CurrencyAlternateKey = ?",
            (json.dumps(country_data), "AFA")  # Serialize the dictionary into JSON string
        )
        
        # Check if the update was successful
        if update_success:
            print("Successfully updated JSON data")
        
        # Query the table to fetch records where Country (a JSON column) is not null
        print("\nFetching updated data:")
        result = db.fetch_data(
            "SELECT * FROM DimCurrency WHERE Country IS NOT NULL"
        )
        
        # Print the fetched records
        if result:
            for row in result:
                print(row)
        
    except Exception as e:
        # Catch and display any error that occurs during execution
        print(f"An error occurred: {e}")
    
    finally:
        # Ensure the database connection is closed gracefully
        if 'db' in locals():
            db.close()
            print("\nDatabase connection closed.")

# Entry point of the script
if __name__ == "__main__":
    main()
