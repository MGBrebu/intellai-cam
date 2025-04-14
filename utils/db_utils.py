import sqlite3
from datetime import datetime

DB_PATH = 'db/faces.db'

# Initialize the database and create the table if it doesn't exist
def init_db(db_path='db/faces.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            age INTEGER,
            gender TEXT,
            race TEXT,
            image_path TEXT
        )
    ''')

    conn.commit()
    conn.close()

def clear_db(db_path='db/faces.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM face_data')
    conn.commit()
    conn.close()

# Save analysis results to the database
# An entry includes its own ID, the camera's ID, age, gender, race, timestamp, and an image path (if available)
def save_analysis_db(attributes, image_path=None, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    timestamp = str(datetime.now().isoformat())

    cursor.execute('''
        INSERT INTO face_data (timestamp, age, gender, race, image_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        timestamp,
        attributes.get("age"),
        attributes.get("dominant_gender"),
        attributes.get("dominant_race"),
        image_path
    ))

    conn.commit()
    conn.close()

# Grab all database entries
def get_all_entries(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM face_data')
    entries = cursor.fetchall()

    conn.close()
    return entries

# Filter database entries by specified attribute
def filter_by_attribute(attribute, value, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f'SELECT * FROM face_data WHERE {attribute} = ?'
    cursor.execute(query, (value,))
    entries = cursor.fetchall()

    conn.close()
    return entries