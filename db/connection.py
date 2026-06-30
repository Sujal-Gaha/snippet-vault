import os
import sqlite3

from config.settings import settings


class DatabaseManager:
    """Manages database connection lifecycle and schema initializations for SQLite."""

    def __init__(self):
        self.db_file = settings.db.sqlite_db_path
        self.placeholder = "?"

    def get_connection(self):
        """Creates and returns an active database connection."""
        # If default db_file has a parent path, create it
        db_dir = os.path.dirname(self.db_file)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        return sqlite3.connect(self.db_file)

    def init_db(self):
        """Performs initial schema setup and database migrations."""
        conn = self.get_connection()
        c = conn.cursor()

        # SQLite schema setup
        c.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                description TEXT,
                tags TEXT,
                type TEXT NOT NULL,
                language TEXT NOT NULL,
                category TEXT DEFAULT 'Uncategorized',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL
            )
        """)

        # Migration check: check if columns exist in SQLite
        c.execute("PRAGMA table_info(snippets)")
        columns = [col[1] for col in c.fetchall()]
        if "category" not in columns:
            c.execute(
                "ALTER TABLE snippets ADD COLUMN category TEXT DEFAULT 'Uncategorized'"
            )
        if "updated_at" not in columns:
            c.execute("ALTER TABLE snippets ADD COLUMN updated_at TIMESTAMP")

        conn.commit()
        conn.close()
