# database.py
import sqlite3

def initialize_database():
    conn = sqlite3.connect("hotel_management.db")
    cursor = conn.cursor()

    # Create tables if not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room_number TEXT UNIQUE NOT NULL,
                        status TEXT NOT NULL
                    )''')

    conn.commit()
    conn.close()

def add_employee(username, password, role):
    try:
        conn = sqlite3.connect("hotel_management.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password, role):
    conn = sqlite3.connect("hotel_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE username = ? AND password = ? AND role = ?", (username, password, role))
    user = cursor.fetchone()
    conn.close()
    return user