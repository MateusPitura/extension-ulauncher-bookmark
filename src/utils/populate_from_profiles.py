from .parse_bookmarks import parse_bookmarks
import os
import json
from .normalize_path import normalize_path

def populate_from_profiles(repository, preferences):
    profiles = preferences.get("profiles", "")
    base_path = preferences.get("base_bookmark_path")

    for profile in profiles.split(";"):
        if "=" not in profile:
            continue

        profile_name, profile_path = profile.split("=", 1)
        profile_name = profile_name.strip()
        profile_path = os.path.expanduser(normalize_path(profile_path))

        bookmarks_file = os.path.join(profile_path, "Bookmarks")

        if not os.path.exists(bookmarks_file):
            continue

        with open(bookmarks_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        root = data["roots"].get(base_path)
        if not root:
            continue

        parse_bookmarks(repository, root, profile_name, "")

    repository.conn.commit()