"SQLite persistence layer for subscriber preferences and digest history."""
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Dict, Iterator, List, Optional

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
CREATE TABLE IF NOT EXISTS digest_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subscriber_email TEXT NOT NULL,
    run_id TEXT NOT NULL,
    run_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('sent', 'no_articles', 'failed')),
    article_count INTEGER NOT NULL DEFAULT 0,
    subject TEXT,
    error TEXT
);
CREATE INDEX IF NOT EXISTS idx_digest_log_run_at ON digest_log(run_at);
CREATE INDEX IF NOT EXISTS idx_digest_log_subscriber ON digest_log(subscriber_email);
"""


def get_db_path() -> str:
    """Return the database file path (overridable through NEWS_DB_PATH)."""
    return os.environ.get("NEWS_DB_PATH", "news_emailer.db")


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Yield a connection that commits on success and rolls back on error."""
    db_path = get_db_path()
    if db_path != ":memory:":
        db_file = Path(db_path).expanduser()
        db_file.parent.mkdir(parents=True, exist_ok=True)
        db_path = str(db_file)
    conn = sqlite3.connect(db_path)
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
    """Create application tables idempotently, including Sprint 2 history."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def _load_topics(conn: sqlite3.Connection, user_id: int) -> List[str]:
    rows = conn.execute(
        "SELECT topic FROM topic_preferences WHERE user_id = ? ORDER BY id",
        (user_id,),
    ).fetchall()
    return [row["topic"] for row in rows]


def create_user(email: str, topics: List[str]) -> UserRecord:
    """Insert a new user with topics. Raises DuplicateUserError if email exists."""
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with get_connection() as conn:
        try:
            cursor = conn.execute(
                "INSERT INTO users (email, created_at) VALUES (?, ?)",
                (email, created_at),
            )
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
        row = conn.execute(
            "SELECT id, email, created_at FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        if row is None:
            return None
        topics = _load_topics(conn, row["id"])
    return UserRecord(email=row["email"], created_at=row["created_at"], topics=topics)


def update_topics(email: str, topics: List[str]) -> Optional[UserRecord]:
    """Replace a user's topics. Returns None if the user does not exist."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, email, created_at FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        if row is None:
            return None
        conn.execute(
            "DELETE FROM topic_preferences WHERE user_id = ?",
            (row["id"],),
        )
        conn.executemany(
            "INSERT INTO topic_preferences (user_id, topic) VALUES (?, ?)",
            [(row["id"], topic) for topic in topics],
        )
    return UserRecord(email=row["email"], created_at=row["created_at"], topics=list(topics))


def get_subscribers() -> List[Dict]:
    """Return every subscriber with their saved topics in deterministic order."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, email, created_at FROM users ORDER BY id"
        ).fetchall()
        return [
            {
                "email": row["email"],
                "created_at": row["created_at"],
                "topics": _load_topics(conn, row["id"]),
            }
            for row in rows
        ]


def record_digest_outcome(
    subscriber_email: str,
    run_id: str,
    run_at: str,
    status: str,
    article_count: int = 0,
    subject: Optional[str] = None,
    error: Optional[str] = None,
) -> int:
    """Persist one subscriber's digest outcome and return its history row ID."""
    if status not in ("sent", "no_articles", "failed"):
        raise ValueError("Unsupported digest status: " + status)
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO digest_log (
                subscriber_email, run_id, run_at, status,
                article_count, subject, error
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                subscriber_email,
                run_id,
                run_at,
                status,
                article_count,
                subject,
                error,
            ),
        )
        return int(cursor.lastrowid)


def get_digest_history(limit: int = 50) -> List[Dict]:
    """Return the newest digest outcomes, capped to protect the demo endpoint."""
    safe_limit = max(1, min(int(limit), 500))
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, subscriber_email, run_id, run_at, status,
                   article_count, subject, error
            FROM digest_log
            ORDER BY id DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()
    return [dict(row) for row in rows]
