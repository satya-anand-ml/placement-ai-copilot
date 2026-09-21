import sqlite3
import uuid
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "chat_history.db"


def get_connection():
    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT UNIQUE NOT NULL,
            title TEXT DEFAULT 'New Chat',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,

            FOREIGN KEY (thread_id)
            REFERENCES chats(thread_id)
        )
    """)

    connection.commit()
    connection.close()


def create_chat(title="New Chat"):
    thread_id = str(uuid.uuid4())

    now = datetime.now().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO chats (
            thread_id,
            title,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            thread_id,
            title,
            now,
            now
        )
    )

    connection.commit()
    connection.close()

    return thread_id


def save_message(
    thread_id,
    role,
    content
):
    now = datetime.now().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            thread_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            thread_id,
            role,
            content,
            now
        )
    )

    cursor.execute(
        """
        UPDATE chats
        SET updated_at = ?
        WHERE thread_id = ?
        """,
        (
            now,
            thread_id
        )
    )

    # Automatically create a useful title
    if role == "user":

        cursor.execute(
            """
            SELECT title
            FROM chats
            WHERE thread_id = ?
            """,
            (thread_id,)
        )

        row = cursor.fetchone()

        if row and row["title"] == "New Chat":

            title = content.strip()

            if len(title) > 40:
                title = title[:40] + "..."

            cursor.execute(
                """
                UPDATE chats
                SET title = ?
                WHERE thread_id = ?
                """,
                (
                    title,
                    thread_id
                )
            )

    connection.commit()
    connection.close()


def get_chat_messages(thread_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE thread_id = ?
        ORDER BY id ASC
        """,
        (thread_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "role": row["role"],
            "content": row["content"]
        }
        for row in rows
    ]


def get_chats(limit=20):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            thread_id,
            title,
            created_at,
            updated_at
        FROM chats
        ORDER BY updated_at DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "thread_id": row["thread_id"],
            "title": row["title"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
        for row in rows
    ]


def delete_chat(thread_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM messages
        WHERE thread_id = ?
        """,
        (thread_id,)
    )

    cursor.execute(
        """
        DELETE FROM chats
        WHERE thread_id = ?
        """,
        (thread_id,)
    )

    connection.commit()
    connection.close()


def get_chat(thread_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            thread_id,
            title,
            created_at,
            updated_at
        FROM chats
        WHERE thread_id = ?
        """,
        (thread_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "thread_id": row["thread_id"],
        "title": row["title"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }    