import sqlite3
from datetime import datetime

DB_PATH = "../scan_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            snippet TEXT,
            prediction TEXT,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()

def log_scan(text, prediction, confidence):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snippet = text[:100].replace('\n', ' ') + "..." if len(text) > 100 else text.replace('\n', ' ')
    cursor.execute(
        "INSERT INTO scan_logs (timestamp, snippet, prediction, confidence) VALUES (?, ?, ?, ?)",
        (timestamp, snippet, prediction, confidence)
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, snippet, prediction, confidence FROM scan_logs ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return rows
