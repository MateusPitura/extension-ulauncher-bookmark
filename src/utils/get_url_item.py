from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from .get_profile_path import get_profile_path
import os
from .get_favicon import get_favicon
from .remove_url_prefix import remove_url_prefix

def get_url_item(item, extension):
    profile_name = item.get("full_path", "").split(" ")[0].strip() # 🌠 improve this
    normalized_profile_name = os.path.normpath(get_profile_path(profile_name, extension))
    chrome_profile = os.path.basename(normalized_profile_name)

    bookmark_name = item.get("name", "Unknown")
    bookmark_url = item.get("url", "www.example.com")

    return {
        "icon": get_favicon(bookmark_url, normalized_profile_name),
        "name": bookmark_name,
        "description": remove_url_prefix(bookmark_url),
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