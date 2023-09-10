import mysql.connector

db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
}

def retrieve_window_logs():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT timestamp, window_title FROM window_logs")
        
        # Fetch all records
        records = cursor.fetchall()
        
        for record in records:
            timestamp, window_title = record
            print(f"Timestamp: {timestamp}, Window Title: {window_title}")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error retrieving data from the database: {err}")

if __name__ == "__main__":
    retrieve_window_logs()
