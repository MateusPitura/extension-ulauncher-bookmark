import sqlite3
from ..utils.get_preferences_path import get_preferences_path

import os
import time

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
        print(f"🌠 deled all")

        self.conn.commit()

    def insert_bookmark(self, name, url, icon, full_path):
        print(f"🌠 insert")
        self.cursor.execute("""
            INSERT OR REPLACE INTO bookmarks (name, url, icon, full_path, last_used)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            url,
            icon,
            full_path,
            int(time.time())
        ))