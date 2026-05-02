from .remove_url_prefix import remove_url_prefix
from .normalize_string import normalize_string
from .google_timestamp_now import google_timestamp_now

def parse_bookmarks(repository, node, profile_name, current_path):
    if "children" not in node:
        return

    for child in node["children"]:
        if child["type"] == "folder":
            new_path = f"{current_path}/{child['name']}" if current_path else child["name"]

            repository.insert_folder(
                name=child["name"],
                full_path=normalize_string(new_path),
                last_used=child.get('date_last_used', google_timestamp_now()),
                profile=profile_name
            )

            parse_bookmarks(
                repository,
                child,
                profile_name,
                new_path
            )

        elif child["type"] == "url":
            full_path = (
                f"{current_path}/{child['name']}"
                if current_path
                else f"{child['name']}"
            )

            repository.insert_bookmark(
                name=child["name"],
                url=child["url"],
                full_path=normalize_string(full_path),
                last_used=child.get('date_last_used', google_timestamp_now()),
                profile=profile_name
            )