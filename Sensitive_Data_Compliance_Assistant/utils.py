import sqlite3
import pandas as pd
from datetime import datetime
from config import LOGS_DIR
import os

DB_PATH = os.path.join(LOGS_DIR, "audit_logs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_time TEXT,
            sensitive_items_count INTEGER,
            risk_level TEXT,
            risk_score INTEGER,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_scan(filename: str, items_count: int, risk_level: str, risk_score: int, summary: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO logs (filename, upload_time, sensitive_items_count, risk_level, risk_score, summary)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (filename, upload_time, items_count, risk_level, risk_score, summary))
    conn.commit()
    conn.close()

def get_all_logs() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()
    return df

# Initialize DB on load
init_db()
