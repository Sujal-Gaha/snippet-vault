import os
import sqlite3
from config.settings import settings

try:
    import pymysql
except ImportError:
    pymysql = None

class DatabaseManager:
    """Manages database connection lifecycle and schema initializations for SQLite and MySQL."""
    
    def __init__(self):
        self.db_type = settings.db.db_type
        
        if self.db_type == "mysql":
            if pymysql is None:
                raise ImportError(
                    "pymysql is not installed. Please install pymysql to use MySQL backend."
                )
            self.host = settings.db.mysql_host
            self.port = settings.db.mysql_port
            self.db_name = settings.db.mysql_database
            self.user = settings.db.mysql_user
            self.password = settings.db.mysql_password
            self.placeholder = "%s"
        else:
            self.db_file = settings.db.sqlite_db_path
            self.placeholder = "?"

    def get_connection(self):
        """Creates and returns an active database connection."""
        if self.db_type == "mysql":
            return pymysql.connect(
                host=self.host,
                port=self.port,
                database=self.db_name,
                user=self.user,
                password=self.password
            )
        else:
            # If default db_file has a parent path, create it
            db_dir = os.path.dirname(self.db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            return sqlite3.connect(self.db_file)

    def init_db(self):
        """Performs initial schema setup and database migrations."""
        conn = self.get_connection()
        c = conn.cursor()
        
        if self.db_type == "mysql":
            # MySQL schema setup
            c.execute("""
                CREATE TABLE IF NOT EXISTS snippets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    description TEXT,
                    tags TEXT,
                    type VARCHAR(50) NOT NULL,
                    language VARCHAR(50) NOT NULL,
                    category VARCHAR(100) DEFAULT 'Uncategorized',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Migration check: check if category exists in mysql
            c.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = DATABASE() 
                  AND table_name = 'snippets' 
                  AND column_name = 'category'
            """)
            category_exists = bool(c.fetchone())
            if not category_exists:
                c.execute("ALTER TABLE snippets ADD COLUMN category VARCHAR(100) DEFAULT 'Uncategorized'")
        else:
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Migration check: check if category exists in SQLite
            c.execute("PRAGMA table_info(snippets)")
            columns = [col[1] for col in c.fetchall()]
            if "category" not in columns:
                c.execute("ALTER TABLE snippets ADD COLUMN category TEXT DEFAULT 'Uncategorized'")
                
        conn.commit()
        conn.close()


