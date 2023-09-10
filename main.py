import time
import psutil
import mysql.connector
from pynput import keyboard
import pygetwindow as gw

db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
}

def create_database_if_not_exists():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        cursor.execute(f"USE {db_config['database']}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def create_table_if_not_exists():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS window_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp INT NOT NULL,
                window_title VARCHAR(255) NOT NULL
            )
        """)
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def create_index_if_not_exists():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SHOW INDEX FROM window_logs WHERE Key_name = 'idx_timestamp'")
        
        if cursor.fetchone() is None:
            cursor.execute("CREATE INDEX idx_timestamp ON window_logs (timestamp)")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error creating index: {err}")

def get_active_window_title():
    try:
        active_window = gw.getActiveWindow()
        if active_window is not None:
            return active_window.title
    except Exception as e:
        print(f"Error getting active window title: {e}")
    return None

def log_active_window():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        active_window_title = get_active_window_title()
        if active_window_title:
            timestamp = int(time.time())
            sql = "INSERT INTO window_logs (timestamp, window_title) VALUES (%s, %s)"
            values = (timestamp, active_window_title)
            cursor.execute(sql, values)
            conn.commit()

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data into the database: {err}")

def on_key_release(key):
    if key == keyboard.Key.esc:
        listener.stop()

if __name__ == "__main__":
    create_database_if_not_exists()
    create_table_if_not_exists()
    create_index_if_not_exists()

    with keyboard.Listener(on_release=on_key_release) as listener:
        while True:
            log_active_window()
            time.sleep(3600)  # <--Change time here