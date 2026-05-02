from pathlib import Path
import hashlib
import tempfile
import sqlite3
import os
import shutil
from .constants import CACHE_DIR

DEFAULT_FAVICON = "images/chrome.png"

def get_favicon(url, profile_path):
    safe_name = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{safe_name}.png")

    if os.path.exists(cache_file):
        return cache_file

    favicon_path = os.path.expanduser(f"{profile_path}/Favicons")

    if not Path(favicon_path).exists():
        return DEFAULT_FAVICON

    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        shutil.copy(favicon_path, tmpfile.name)
        temp_db = tmpfile.name

    conn = sqlite3.connect(temp_db)
    cur = conn.cursor()
    cur.execute("""
        SELECT fb.image_data
        FROM icon_mapping im
        JOIN favicon_bitmaps fb ON im.icon_id = fb.icon_id
        WHERE im.page_url LIKE ?
        ORDER BY fb.width DESC, fb.last_updated DESC
        LIMIT 1
    """, (f"%{url}%",))
    row = cur.fetchone()
    conn.close()

    os.unlink(temp_db)

    if row:
        with open(cache_file, "wb") as f:
            f.write(row[0])
        return cache_file

    return DEFAULT_FAVICON