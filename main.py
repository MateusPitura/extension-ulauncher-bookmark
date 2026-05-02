import os
import subprocess
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
from ulauncher.api.shared.event import PreferencesEvent
from src.utils.constants import CACHE_DIR
from src.utils.clear_favicon_cache import clear_cache
from src.utils.get_folder_item import get_folder_item
from src.utils.split_string import split_string


class LunetaBrowserBookmark(Extension):
    def __init__(self):
        super(LunetaBrowserBookmark, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())

        os.makedirs(CACHE_DIR, exist_ok=True)

        self.repository = BookmarkRepository(dirname=os.path.dirname(__file__))

        clear_cache()


def get_bookmark_items(query, event, extension):
    query = normalize_string(query.strip())

    max_results = get_max_results(extension)

    profile_name = split_string(query)[0]

    url_items = extension.repository.search_by_url(query, profile_name, max_results)

    folder_items = extension.repository.search_by_folder(query, max_results)

    url_items_formatted = [get_url_item(item, extension) for item in url_items]

    folder_items_formatted = [get_folder_item(item, event) for item in folder_items]

    items = folder_items_formatted + url_items_formatted
    if query == "":
        profile_items = get_profiles_items(event, extension)
        items = profile_items + items

    return [
        ExtensionResultItem(
            icon=item["icon"],
            name=item["name"],
            description=item["description"],
            on_enter=item["on_enter"]
        )
        for item in items[:max_results]
    ]


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()

        if data.get("action") != "open_bookmark":
            return

        chrome_profile = data["chrome_profile"]
        url = data["url"]
        bookmark_id = data.get("id")

        extension.repository.update_url_last_used_by_id(bookmark_id, google_timestamp_now())

        subprocess.Popen([
            "google-chrome",
            f"--profile-directory={chrome_profile}",
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
