from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from src.utils.get_profiles_items import get_profiles_items
from src.utils.get_max_results import get_max_results
from src.utils.get_url_item import get_url_item
from src.utils.normalize_string import normalize_string
from src.utils.get_folder_item import get_folder_item


def get_bookmark_items(query, keyword, preferences, repository):
    query = normalize_string(query.strip())

    max_results = get_max_results(preferences)

    url_items = repository.search_by_url(query, max_results,)

    folder_items = repository.search_by_folder(query, max_results)

    url_items_formatted = [get_url_item(item, preferences) for item in url_items]

    folder_items_formatted = [
        get_folder_item(item, keyword)
        for item in folder_items
    ]

    items = folder_items_formatted + url_items_formatted
    if query == "":
        profile_items = get_profiles_items(keyword, preferences)
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
