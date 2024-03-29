import sqlite3
import csv
from datetime import datetime
import os
import glob
import time

def ingest_data(files_pattern, db_path):
    start_time = time.time()

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        records_ingested = 0

        # Find all files matching the pattern (e.g., 'wx_data/*.txt')
        for file_path in glob.glob(files_pattern):
            station_id = os.path.splitext(os.path.basename(file_path))[0]

            with open(file_path, 'r') as file:
                reader = csv.reader(file, delimiter='\t')
                for row in reader:
                    date = datetime.strptime(row[0], '%Y%m%d').date() if row[0] != '-9999' else None
                    max_temp = int(row[1]) if row[1] != '-9999' else None
                    min_temp = int(row[2]) if row[2] != '-9999' else None
                    precipitation = int(row[3]) if row[3] != '-9999' else None

                    cursor.execute('''
                        INSERT OR IGNORE INTO WeatherData (station_id, record_date, max_temp, min_temp, precipitation)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (station_id, date, max_temp, min_temp, precipitation))

                    if cursor.rowcount > 0:
                        records_ingested += 1

            conn.commit()

    except sqlite3.DatabaseError as e:
        # Handle a database error
        print(f"Database error: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
    finally:
        # This block will run whether or not an exception occurred
        if 'conn' in locals():  # Check if 'conn' was successfully defined
            conn.close()

        end_time = time.time()
        
        # Log output
        print(f"Data ingestion started at {datetime.fromtimestamp(start_time)}")
        print(f"Data ingestion ended at {datetime.fromtimestamp(end_time)}")
        
        if records_ingested > 0:
            print(f"Total records ingested: {records_ingested}")
        else:
            print("No new records were ingested.")

# Example usage
ingest_data('../wx_data/*.txt', 'wx_data.db')
