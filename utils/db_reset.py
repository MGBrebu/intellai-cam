import os

DB_PATH = '/db/faces.db'

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