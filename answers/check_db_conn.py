import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wx_data.db'
db = SQLAlchemy(app)

def check_database_connection():
    try:
        conn = sqlite3.connect('wx_data.db')
        print("Database connection successful!")
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return False

def check_tables_exist():
    table_names = ['WeatherAnalysis', 'WeatherData']
    conn = sqlite3.connect('wx_data.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]

        for table_name in table_names:
            if table_name not in existing_tables:
                print(f"Table '{table_name}' does not exist in the database.")
                return False

        print("All specified tables exist in the database.")
        return True
    except sqlite3.Error as e:
        print(f"Error checking tables: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    if check_database_connection():
        if check_tables_exist():
            print("Database setup is correct. You can proceed with running the application.")
        else:
            print("Please create the required tables before running the application.")
    else:
        print("Unable to connect to the database. Please check your database configuration.")