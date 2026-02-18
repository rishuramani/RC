"""SQLite database connection manager."""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Optional


class Database:
    """Manages SQLite connections and schema initialization."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path == ":memory:":
            self._db_path = ":memory:"
        else:
            from src.config import DB_PATH
            self._db_path = str(db_path or DB_PATH)
            Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)

        self._connection: Optional[sqlite3.Connection] = None

    @property
    def db_path(self) -> str:
        return self._db_path

    def connect(self) -> sqlite3.Connection:
        """Create or return the database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA journal_mode=WAL")
            self._connection.execute("PRAGMA foreign_keys=ON")
        return self._connection

    def close(self):
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def initialize(self):
        """Create tables from schema.sql."""
        schema_path = Path(__file__).parent / "schema.sql"
        schema_sql = schema_path.read_text()
        conn = self.connect()
        conn.executescript(schema_sql)
        conn.commit()

    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a single SQL statement."""
        conn = self.connect()
        return conn.execute(sql, params)

    def executemany(self, sql: str, params_list: list) -> sqlite3.Cursor:
        """Execute a SQL statement for multiple parameter sets."""
        conn = self.connect()
        return conn.executemany(sql, params_list)

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Execute and fetch one result."""
        return self.execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Execute and fetch all results."""
        return self.execute(sql, params).fetchall()

    def commit(self):
        """Commit the current transaction."""
        if self._connection:
            self._connection.commit()
