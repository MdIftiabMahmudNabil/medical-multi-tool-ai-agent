import pandas as pd
import sqlite3
import os
from pathlib import Path
from utils.load_config import LoadConfig

class DatabaseSetup:
    """
    A class to set up SQLite databases from CSV files for medical datasets.
    Follows the patterns from the learning materials for database management.
    """
    
    def __init__(self):
        self.config = LoadConfig()
    
    def create_heart_disease_db(self):
        """Create SQLite database from heart disease CSV"""
        try:
            # Load the CSV file
            csv_path = os.path.join(self.config.datasets_directory, "heart.csv")
            if not os.path.exists(csv_path):
                print(f"Error: {csv_path} not found. Please ensure the heart.csv file exists in the Datasets folder.")
                return False
            
            df = pd.read_csv(csv_path)
            print(f"Loaded heart disease data with {len(df)} records and {len(df.columns)} columns")
            
            # Ensure data directory exists
            os.makedirs(self.config.data_directory, exist_ok=True)
            
            # Create SQLite connection
            conn = sqlite3.connect(self.config.heart_disease_db)
            
            # Create table with proper data types
            df.to_sql(
                name=self.config.heart_disease_config["table_name"],
                con=conn,
                if_exists='replace',
                index=False
            )
            
            conn.close()
            print(f"✅ Heart disease database created successfully at {self.config.heart_disease_db}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating heart disease database: {str(e)}")
            return False
    
    def create_cancer_db(self):
        """Create SQLite database from cancer CSV"""
        try:
            # Load the CSV file
            csv_path = os.path.join(self.config.datasets_directory, "The_Cancer_data_1500_V2.csv")
            if not os.path.exists(csv_path):
                print(f"Error: {csv_path} not found. Please ensure the cancer CSV file exists in the Datasets folder.")
                return False
            
            df = pd.read_csv(csv_path)
            print(f"Loaded cancer data with {len(df)} records and {len(df.columns)} columns")
            
            # Ensure data directory exists
            os.makedirs(self.config.data_directory, exist_ok=True)
            
            # Create SQLite connection
            conn = sqlite3.connect(self.config.cancer_db)
            
            # Create table with proper data types
            df.to_sql(
                name=self.config.cancer_config["table_name"],
                con=conn,
                if_exists='replace',
                index=False
            )
            
            conn.close()
            print(f"✅ Cancer database created successfully at {self.config.cancer_db}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating cancer database: {str(e)}")
            return False
    
    def create_diabetes_db(self):
        """Create SQLite database from diabetes CSV"""
        try:
            # Load the CSV file  
            csv_path = os.path.join(self.config.datasets_directory, "diabetes.csv")
            if not os.path.exists(csv_path):
                print(f"Error: {csv_path} not found. Please ensure the diabetes.csv file exists in the Datasets folder.")
                return False
            
            df = pd.read_csv(csv_path)
            print(f"Loaded diabetes data with {len(df)} records and {len(df.columns)} columns")
            
            # Ensure data directory exists
            os.makedirs(self.config.data_directory, exist_ok=True)
            
            # Create SQLite connection
            conn = sqlite3.connect(self.config.diabetes_db)
            
            # Create table with proper data types
            df.to_sql(
                name=self.config.diabetes_config["table_name"],
                con=conn,
                if_exists='replace',
                index=False
            )
            
            conn.close()
            print(f"✅ Diabetes database created successfully at {self.config.diabetes_db}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating diabetes database: {str(e)}")
            return False
    
    def setup_all_databases(self):
        """Set up all medical databases"""
        print("🏥 Setting up medical databases...")
        print("=" * 50)
        
        results = {
            "heart_disease": self.create_heart_disease_db(),
            "cancer": self.create_cancer_db(), 
            "diabetes": self.create_diabetes_db()
        }
        
        success_count = sum(results.values())
        total_count = len(results)
        
        print("=" * 50)
        print(f"📊 Database setup complete: {success_count}/{total_count} successful")
        
        if success_count == total_count:
            print("🎉 All databases created successfully!")
        else:
            print("⚠️  Some databases failed to create. Please check the error messages above.")
        
        return results

if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.setup_all_databases()