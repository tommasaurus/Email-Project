import sqlite3
import os
from os import path

class DatabaseManager:
    current_directory = os.getcwd()
    relative_path = 'email-project/schedule.db'
    absolute_path = path.join(current_directory, relative_path)
    conn = sqlite3.connect(absolute_path)

def main():
    current_directory = os.getcwd()
    relative_path = 'email-project/schedule.db'
    absolute_path = path.join(current_directory, relative_path)
    conn = sqlite3.connect(absolute_path)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY,
        Day TEXT NOT NULL,
        Times TEXT NOT NULL
    )
    ''')

    
    conn.commit()
    conn.close()
    print("hello2")

if __name__ == "__main__":
    main()