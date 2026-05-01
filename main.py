import json
import os
from pathlib import Path
import hashlib
import tempfile
import shutil
import sqlite3
import subprocess
from src.utils.get_profile_path import get_profile_path
from src.utils.get_profiles_items import get_profiles_items
from src.utils.get_max_results import get_max_results
from src.repository.BookmarkRepository import BookmarkRepository
from src.utils.populate_from_profiles import populate_from_profiles
from src.utils.get_url_item import get_url_item
from src.utils.google_timestamp_now import google_timestamp_now
from src.utils.normalize_string import normalize_string
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import ItemEnterEvent
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.event import PreferencesEvent

CACHE_DIR = os.path.expanduser(
    "~/.cache/ulauncher_luneta-browser-bookmark_favicons")

os.makedirs(CACHE_DIR, exist_ok=True)


class LunetaBrowserBookmark(Extension):
    def __init__(self):
        super(LunetaBrowserBookmark, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())

        self.repository = BookmarkRepository(dirname=os.path.dirname(__file__))

        clear_cache()


def append_folder(items, item, base_path, event):
    keyword = event.get_keyword()

    folder_name = item.get("name", "Unknown")

    items.append({
        "icon": "images/folder.png",
        "name": folder_name,
        "description": "Click to enter folder",
        "on_enter": SetUserQueryAction(f"{keyword} {base_path}{folder_name}/")
    })


def get_favicon(url, event, extension):
    safe_name = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{safe_name}.png")

    if os.path.exists(cache_file):
        return cache_file

    keyword = event.get_keyword()
    profile_path = get_profile_path(keyword, extension)
    favicon_path = os.path.expanduser(f"{profile_path.rstrip('/')}/Favicons")

    if not Path(favicon_path).exists():
        return "images/chrome.png"

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

    return "images/chrome.png"


def clear_cache():
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
        os.makedirs(CACHE_DIR, exist_ok=True)


def get_bookmarks_path(profile_path):
    return os.path.expanduser(
        f"{profile_path.rstrip('/')}/Bookmarks")


def get_bookmark_items(query="", event=None, extension=None):
    query = normalize_string(query.strip())

    max_results = get_max_results(extension)

    url_items = extension.repository.search_by_full_path(query, max_results)

    url_items_formatted = [get_url_item(item, event, extension) for item in url_items]

    profile_items = get_profiles_items(event, extension)

    if query == "":
        items = profile_items + url_items_formatted
    else:
        items = url_items_formatted

    return [
        ExtensionResultItem(
            icon=item["icon"],
            name=item["name"],
            description=item["description"],
            on_enter=item["on_enter"]
        )
        for item in items
    ]


def update_item_date(items, bookmark_id):
    for item in items:
        if item.get("id") == bookmark_id:
            item["date_last_used"] = google_timestamp_now()
            return True

        if item.get("type") == "folder":
            children = item.get("children", [])
            if update_item_date(children, bookmark_id):
                return True

    return False


def update_chrome_bookmark_date(
    bookmarks_path,
    bookmark_id,
    extension
):
    with open(bookmarks_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    base_bookmark_path = extension.preferences.get("base_bookmark_path")

    children = data.get("roots", {}).get(
        base_bookmark_path, {}).get("children", [])

    updated = update_item_date(children, bookmark_id)
    if not updated:
        return False

    dir_name = os.path.dirname(bookmarks_path)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=dir_name, delete=False
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    os.replace(tmp_path, bookmarks_path)
    return True


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()

        if data.get("action") != "open_bookmark":
            return

        profile = data["profile"]
        url = data["url"]
        bookmark_id = data.get("id")
        profile_path = data.get("profile_path")

        bookmarks_path = get_bookmarks_path(profile_path)

        if extension.preferences.get("update_last_used") == "true":
            update_chrome_bookmark_date(
                bookmarks_path,
                bookmark_id,
                extension
            )

        subprocess.Popen([
            "google-chrome",
            f"--profile-directory={profile}",
            url
        ])

        return HideWindowAction()


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        items = []

        try:
            items = get_bookmark_items(query, event, extension)

        except Exception as e:
            print(f"🌠 error", e)
            items.append(ExtensionResultItem(
                icon="images/logo.png",
                name="Luneta Browser Bookmark",
                description=str(e)
            ))

        return RenderResultListAction(items)

class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        populate_from_profiles(extension.repository, event.preferences)

if __name__ == "__main__":
    LunetaBrowserBookmark().run()
