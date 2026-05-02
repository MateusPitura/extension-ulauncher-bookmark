from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from src.utils.get_profiles_items import get_profiles_items
from src.utils.get_max_results import get_max_results
from src.utils.get_url_item import get_url_item
from src.utils.normalize_string import normalize_string
from src.utils.get_folder_item import get_folder_item
from src.utils.get_profile_names import get_profile_names
from src.utils.split_string import split_string


def get_bookmark_items(query, keyword, preferences, repository):
    query = normalize_string(query.strip())

    max_results = get_max_results(preferences)

    count_slashs = False
    if "/" in query:
        prefix, bookmark_name_query = split_string(query, "/", True)
        count_slashs = True if bookmark_name_query == "" else False
        query = f"%{prefix}/%{bookmark_name_query}%"
    else:
        profile_name, rest_query = split_string(query, " ")
        profile_names = get_profile_names(preferences)
        if profile_name in profile_names:
            count_slashs = True if rest_query == "" else False
            query = f"{profile_name} %{rest_query}%"
        else:
            query = f"%{query}%"

    url_items = repository.search_by_url(query, max_results,)

    folder_items = repository.search_by_folder(query, max_results)

    url_items_formatted = [get_url_item(item, preferences) for item in url_items]

    folder_items_formatted = []
    for item in folder_items:
        if count_slashs:
            slash_count = query.count("/")
            if item.get("full_path", "").count("/") > slash_count:
                continue
        folder_items_formatted.append(get_folder_item(item, keyword))

    if query == "%%":
        profile_items = get_profiles_items(keyword, preferences)
        items = profile_items + url_items_formatted
    else:
        items = folder_items_formatted + url_items_formatted

    return [
        ExtensionResultItem(
            icon=item["icon"],
            name=item["name"],
            description=item["description"],
            on_enter=item["on_enter"]
        )
        for item in items[:max_results]
    ]
