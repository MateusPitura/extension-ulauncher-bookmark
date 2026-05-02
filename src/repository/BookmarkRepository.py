import os
import sqlite3
from src.utils.get_preferences_path import get_preferences_path


class BookmarkRepository:
    def __init__(self, dirname):
        db_path = f'{get_preferences_path(dirname)}/data.db'
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            full_path TEXT,
            last_used INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS folders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            full_path TEXT,
            last_used INTEGER
        )
        """)

        self.cursor.execute("DELETE FROM bookmarks")

        self.cursor.execute("DELETE FROM folders")

        self.conn.commit()

    def insert_bookmark(self, name, url, full_path, last_used):
        self.cursor.execute("""
            INSERT OR REPLACE INTO bookmarks (name, url, full_path, last_used)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            url,
            full_path,
            last_used
        ))

    def insert_folder(self, name, full_path, last_used):
        self.conn.execute("""
            INSERT INTO folders (name, full_path, last_used)
            VALUES (?, ?, ?)
        """, (name, full_path, last_used))

    def search_by_url(self, query, limit):
        self.cursor = self.conn.execute("""
            SELECT id, name, url, full_path, last_used
            FROM bookmarks
            WHERE full_path LIKE ?
            ORDER BY last_used DESC
            LIMIT ?
        """, (query, limit))

        return [dict(row) for row in self.cursor.fetchall()]

    def search_by_folder(self, query, limit):
        self.cursor = self.conn.execute("""
            SELECT id, name, full_path, last_used
            FROM folders
            WHERE full_path LIKE ?
            ORDER BY last_used DESC
            LIMIT ?
        """, (query, limit))

        return [dict(row) for row in self.cursor.fetchall()]

    def update_url_last_used_by_id(self, item_id, last_used):
        self.conn.execute("""
            UPDATE bookmarks
            SET last_used = ?
            WHERE id = ?
        """, (last_used, item_id))

        self.conn.commit()

    def update_folder_last_used_by_id(self, item_id, last_used): # 🌠 not implemented
        self.conn.execute("""
            UPDATE folders
            SET last_used = ?
            WHERE id = ?
        """, (last_used, item_id))

        self.conn.commit()
