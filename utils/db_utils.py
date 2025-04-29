import sqlite3
import os
from datetime import datetime

DB_PATH = 'db/faces.db'

# DEF: Initialize the database and create the table if it doesn't exist
def init_db(db_path='db/faces.db'):
    if not os.path.exists(db_path):
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        except Exception as e:
            print("DB Directory Creation Error:", e)
            return
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print("Database Connection Error:", e)
        return

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

# DEF: Clear the database by deleting all entries
# Only clears entires, DB file remains and IDs are not reset
def clear_db(db_path='db/faces.db'):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print("Database Connection Error:", e)
        return

    cursor.execute('DELETE FROM face_data')
    conn.commit()
    conn.close()

# DEF: Reset the database by deleting the DB file
def reset_db(db_path=DB_PATH):
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Database reset: {db_path} has been deleted.")
            return True
        except Exception as e:
            print(f"Error deleting database: {e}")
            return False
    else:   
        print(f"Database does not exist: {db_path}")
        return False

if __name__ == "__main__":
    reset_db()

# DEF: Save analysis results to the database
# An entry includes its own ID, the camera's ID, age, gender, race, timestamp, and an image path (if available)
def save_analysis_db(attributes, image_path=None, db_path=DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print("Database Connection Error:", e)
        return

    timestamp = str(datetime.now().isoformat())

    try:
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
        print("Database Insertion Success.")
    except sqlite3.Error as e:
        print("Database Insert Error:", e)
        return

    conn.commit()
    conn.close()

# DEF: Grab all database entries
def get_all_entries(db_path=DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, age, gender, race, timestamp FROM face_data ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print("Database error:", e)
        return []

# DEF: Filter database entries by specified attribute
def filter_entries(gender=None, race=None, min_age=None, max_age=None, db_path=DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT id, age, gender, race, timestamp FROM face_data"
        filters = []
        params = []

        if gender and gender.lower() != "all":
            filters.append("gender = ?")
            params.append(gender)

        if race and race.lower() != "all":
            filters.append("race = ?")
            params.append(race)

        if min_age is not None:
            filters.append("age >= ?")
            params.append(min_age)

        if max_age is not None:
            filters.append("age <= ?")
            params.append(max_age)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY timestamp DESC"

        cursor.execute(query, params)
        results = cursor.fetchall()

        conn.close()
        return results

    except sqlite3.Error as e:
        print("Database error:", e)
        return []

