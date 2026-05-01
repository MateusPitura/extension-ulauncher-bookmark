import sqlite3
from ..utils.get_preferences_path import get_preferences_path
import os

class BookmarkRepository:
    def __init__(self, dirname):
        db_path = f'{get_preferences_path(dirname)}/data.db'
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            icon TEXT,
            full_path TEXT,
            last_used INTEGER
        )
        """)

        self.cursor.execute("DELETE FROM bookmarks")

        self.conn.commit()

    def insert_bookmark(self, name, url, icon, full_path, last_used):
        self.cursor.execute("""
            INSERT OR REPLACE INTO bookmarks (name, url, icon, full_path, last_used)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            url,
            icon,
            full_path,
            last_used
        ))

    def search_by_full_path(self, query, limit):
        self.cursor = self.conn.execute("""
            SELECT id, name, url, icon, full_path, last_used
            FROM bookmarks
            WHERE full_path LIKE ?
            ORDER BY last_used DESC
            LIMIT ?
        """, (f"%{query}%", limit))

        return [dict(row) for row in self.cursor.fetchall()]