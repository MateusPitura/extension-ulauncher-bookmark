import os
import subprocess
from src.repository.BookmarkRepository import BookmarkRepository
from src.utils.populate_from_profiles import populate_from_profiles
from src.utils.google_timestamp_now import google_timestamp_now
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import ItemEnterEvent
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import PreferencesEvent
from src.constants.cache import CACHE_DIR
from src.utils.clear_favicon_cache import clear_cache
from src.utils.get_bookmark_items import get_bookmark_items


class LunetaBrowserBookmark(Extension):
    def __init__(self):
        super(LunetaBrowserBookmark, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())

        self.repository = BookmarkRepository(dirname=os.path.dirname(__file__))

        os.makedirs(CACHE_DIR, exist_ok=True)
        clear_cache()


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()

        if data.get("action") != "open_bookmark":
            return

        chrome_profile = data["chrome_profile"]
        url = data["url"]
        bookmark_id = data.get("id")

        extension.repository.update_url_last_used_by_id(
            bookmark_id,
            google_timestamp_now()
        )

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
            print("🌠 error", e)
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
