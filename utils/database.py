# FaceNetAttendanceSystem/utils/database.py
import sqlite3
import os
import pandas as pd

# Database file path (stored under data/)
DB_PATH = os.path.join("data", "database.db")

def init_db():
    """Initialize the SQLite database and create tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create table for student details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment TEXT NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            image_count INTEGER NOT NULL
        )
    """)
    # Create table for attendance records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment TEXT NOT NULL,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_student_detail(enrollment, name, date, time_str, image_count):
    """Insert a new student detail record into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_details (enrollment, name, date, time, image_count)
        VALUES (?, ?, ?, ?, ?)
    """, (enrollment, name, date, time_str, image_count))
    conn.commit()
    conn.close()

def get_student_details():
    """Return all student detail records as a pandas DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT enrollment, name, date, time, image_count FROM student_details", conn)
    conn.close()
    return df

def insert_attendance(enrollment, name, subject, date, time_str):
    """Insert an attendance record into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance (enrollment, name, subject, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (enrollment, name, subject, date, time_str))
    conn.commit()
    conn.close()

def get_all_attendance():
    """Return all attendance records as a pandas DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT enrollment, name, subject, date, time FROM attendance", conn)
    conn.close()
    return df
