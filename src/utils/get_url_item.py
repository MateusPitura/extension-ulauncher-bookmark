import os
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from src.utils.get_profile_path import get_profile_path
from src.utils.get_favicon import get_favicon
from src.utils.remove_url_prefix import remove_url_prefix
from src.utils.split_string import split_string


def remove_last_part(path): # 🌠 maybe move to a folder
    parts = path.split("/")
    return "/".join(parts[:-1])


def format_description(profile_name, rest_path, url): # 🌠 maybe move to a folder
    path = remove_last_part(rest_path)

    prefix = f"({profile_name})"

    if path:
        prefix += f" {path}"

    return f"{prefix} • {remove_url_prefix(url)}"


def get_url_item(item, preferences):
    full_path = item.get("full_path", "")

    profile_name, rest_path = split_string(full_path)
    profile_path = get_profile_path(profile_name, preferences)
    chrome_profile = os.path.basename(profile_path)

    bookmark_name = item.get("name", "Unknown")
    bookmark_url = item.get("url", "www.example.com")

    return {
        "icon": get_favicon(bookmark_url, profile_path),
        "name": bookmark_name,
        "description": format_description(profile_name, rest_path, bookmark_url),
        "on_enter": ExtensionCustomAction(
            {
                "action": "open_bookmark",
                "chrome_profile": chrome_profile,
                "url": bookmark_url,
                "id": item.get("id"),
            },
            keep_app_open=False
        ),
    }
