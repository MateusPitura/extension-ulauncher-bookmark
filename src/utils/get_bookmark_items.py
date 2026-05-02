from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from src.utils.get_profiles_items import get_profiles_items
from src.utils.get_max_results import get_max_results
from src.utils.get_url_item import get_url_item
from src.utils.normalize_string import normalize_string
from src.utils.get_folder_item import get_folder_item
from src.utils.split_string import split_string
from src.utils.get_profile_names import get_profile_names


def get_bookmark_items(query, event, extension):
    query = normalize_string(query.strip())

    max_results = get_max_results(extension)

    profile_name, rest_query = split_string(query)

    url_items = extension.repository.search_by_url(
        rest_query, profile_name, max_results,
        get_profile_names(extension)
    )
    print(f"🌠 url_items: {url_items}")

    folder_items = extension.repository.search_by_folder(
        rest_query, profile_name, max_results,
        get_profile_names(extension)
    )
    print(f"🌠 folder_items: {folder_items}")

    url_items_formatted = [get_url_item(item, extension) for item in url_items]

    folder_items_formatted = [
        get_folder_item(item, event)
        for item in folder_items
    ]

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
