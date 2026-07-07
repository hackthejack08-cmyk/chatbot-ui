import sqlite3
from pathlib import Path

MAX_HISTORY_MESSAGES = 10
DB_PATH = Path(__file__).with_name("bytebot.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def format_history(messages: list) -> str:
    if not messages:
        return "No previous conversation yet."

    lines = []
    for msg in messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def get_recent_messages(session_id: str, limit: int = MAX_HISTORY_MESSAGES):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT role, content
        FROM chat_messages
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (session_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()

    rows = list(reversed(rows))
    return [{"role": row["role"], "content": row["content"]} for row in rows]


def save_message(session_id: str, role: str, content: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO chat_messages (session_id, role, content)
        VALUES (?, ?, ?)
        """,
        (session_id, role, content),
    )
    conn.commit()
    conn.close()


def clear_session(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
