import sqlite3

# Desired database name
db_path = 'wx_data.db'

# Establish a connection to the database.
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor method of the connection object.
cursor = conn.cursor()

# SQL statement to create a table
create_table_sql = '''
CREATE TABLE IF NOT EXISTS WeatherData (
    station_id TEXT NOT NULL,
    record_date DATE NOT NULL,
    max_temp INTEGER,
    min_temp INTEGER,
    precipitation INTEGER,
    PRIMARY KEY (station_id, record_date)
);
'''

# Execute the SQL statement to create the table
cursor.execute(create_table_sql)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database initialized with WeatherData table at {db_path}")
