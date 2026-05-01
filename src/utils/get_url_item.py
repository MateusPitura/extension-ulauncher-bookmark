from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from .get_profile_path import get_profile_path
import os
from ...main import get_favicon
from .remove_url_prefix import remove_url_prefix

def get_url_item(item, event, extension):
    profile_name = item.get("full_path", "").split(" ")[0]
    profile_path = get_profile_path(profile_name, extension)
    profile_path_formatted = os.path.basename(os.path.normpath(profile_path))

    bookmark_name = item.get("name", "Unknown")
    bookmark_url = item.get("url", "www.example.com")

    return {
        "icon": get_favicon(bookmark_url, event, extension),
        "name": bookmark_name,
        "description": remove_url_prefix(bookmark_url),
        "on_enter": ExtensionCustomAction(
            {
                "action": "open_bookmark",
                "profile": profile_path_formatted,
                "url": bookmark_url,
                "id": item.get("id"),
                "profile_path": profile_path
            }, 
            keep_app_open=False
        ),
    }