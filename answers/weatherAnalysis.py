import sqlite3
import sqlite3
from datetime import datetime

# Desired database name
db_path = 'wx_data.db'

# Establish a connection to the database.
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor method of the connection object.
cursor = conn.cursor()

# SQL statement to create a table
create_table_sql = '''
CREATE TABLE WeatherAnalysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id TEXT NOT NULL,
    year INTEGER NOT NULL,
    avg_max_temp REAL, -- Average max temperature
    avg_min_temp REAL, -- Average min temperature
    total_precipitation REAL, -- Total precipitation
    UNIQUE(station_id, year)
);

'''

# Execute the SQL statement to create the table
cursor.execute(create_table_sql)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database initialized with WeatherAnalysis table at {db_path}")


def calculate_weather_statistics(db_path):
    # Connect to the SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Perform the analysis
        cursor.execute('''
            SELECT station_id,
                   strftime('%Y', record_date) as year,
                   AVG(CASE WHEN max_temp != -9999 THEN max_temp END) / 10 as avg_max_temp,
                   AVG(CASE WHEN min_temp != -9999 THEN min_temp END) / 10 as avg_min_temp,
                   SUM(CASE WHEN precipitation != -9999 THEN precipitation END) / 100 as total_precipitation
            FROM WeatherData
            GROUP BY station_id, year
        ''')

        rows = cursor.fetchall()

        # Insert the results into the WeatherAnalysis table
        for row in rows:
            cursor.execute('''
                INSERT OR REPLACE INTO WeatherAnalysis (station_id, year, avg_max_temp, avg_min_temp, total_precipitation)
                VALUES (?, ?, ?, ?, ?)
            ''', row)

        conn.commit()

    except sqlite3.DatabaseError as e:
        # Handle a database error
        print(f"Database error: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred during the analysis: {e}")
    finally:
        # This block will run whether or not an exception occurred
        if 'conn' in locals():
            conn.close()

    print("WeatherAnalysis table created and updated statistics calculation complete.")

# Usage
calculate_weather_statistics('wx_data.db')