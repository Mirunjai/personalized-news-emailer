"""SQLite persistence layer (built-in sqlite3) for users and topic preferences."""
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator, List, Optional

from app.models import DuplicateUserError, UserRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS topic_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic TEXT NOT NULL,
    UNIQUE (user_id, topic)
);
"""


def get_db_path() -> str:
    """Return the database file path (overridable through NEWS_DB_PATH)."""
    return os.environ.get("NEWS_DB_PATH", "news_emailer.db")


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Yield a connection that commits on success and rolls back on error."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create the tables if they do not exist yet."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def _load_topics(conn: sqlite3.Connection, user_id: int) -> List[str]:
    rows = conn.execute("SELECT topic FROM topic_preferences WHERE user_id = ? ORDER BY id", (user_id,)).fetchall()
    return [row["topic"] for row in rows]


def create_user(email: str, topics: List[str]) -> UserRecord:
    """Insert a new user with topics. Raises DuplicateUserError if the email exists."""
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with get_connection() as conn:
        try:
            cursor = conn.execute("INSERT INTO users (email, created_at) VALUES (?, ?)", (email, created_at))
        except sqlite3.IntegrityError as exc:
            raise DuplicateUserError(email) from exc
        conn.executemany(
            "INSERT INTO topic_preferences (user_id, topic) VALUES (?, ?)",
            [(cursor.lastrowid, topic) for topic in topics],
        )
    return UserRecord(email=email, created_at=created_at, topics=list(topics))


def get_user(email: str) -> Optional[UserRecord]:
    """Return the user with their topics, or None if not found."""
    with get_connection() as conn:
        row = conn.execute("SELECT id, email, created_at FROM users WHERE email = ?", (email,)).fetchone()
        if row is None:
            return None
        topics = _load_topics(conn, row["id"])
    return UserRecord(email=row["email"], created_at=row["created_at"], topics=topics)


def update_topics(email: str, topics: List[str]) -> Optional[UserRecord]:
    """Replace a user's topics. Returns None if the user does not exist."""
    with get_connection() as conn:
        row = conn.execute("SELECT id, email, created_at FROM users WHERE email = ?", (email,)).fetchone()
        if row is None:
            return None
        conn.execute("DELETE FROM topic_preferences WHERE user_id = ?", (row["id"],))
        conn.executemany(
            "INSERT INTO topic_preferences (user_id, topic) VALUES (?, ?)",
            [(row["id"], topic) for topic in topics],
        )
    return UserRecord(email=row["email"], created_at=row["created_at"], topics=list(topics))
