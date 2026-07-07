import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "bytebot.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_notes_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_note(session_id: str, content: str, title: str | None = None):
    init_notes_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (session_id, title, content) VALUES (?, ?, ?)",
        (session_id, title, content),
    )
    conn.commit()
    conn.close()


def get_recent_notes(session_id: str, limit: int = 5) -> list[dict]:
    init_notes_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT title, content, created_at
        FROM notes
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (session_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
