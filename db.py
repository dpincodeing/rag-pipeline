import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("rag_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            chunks_used TEXT,
            response_time_ms INTEGER,
            created_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_query(question, answer, chunks, time_ms):
    conn = sqlite3.connect("rag_logs.db")
    cursor = conn.cursor()
    chunks_text = "\n---\n".join(chunks)
    cursor.execute("""
        INSERT INTO query_logs (question, answer, chunks_used, response_time_ms, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (question, answer, chunks_text, time_ms, datetime.now()))
    conn.commit()
    conn.close()