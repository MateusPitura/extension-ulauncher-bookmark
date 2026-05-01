def parse_bookmarks(repository, node, profile_name, current_path):
    if "children" not in node:
        return

    for child in node["children"]:
        if child["type"] == "folder":
            new_path = f"{current_path}/{child['name']}" if current_path else child["name"]

            parse_bookmarks(
                child,
                profile_name,
                new_path
            )

        elif child["type"] == "url":
            full_path = f"{profile_name} {current_path}/{child['name']}" if current_path else f"{profile_name} {child['name']}"

            repository.insert_bookmark(
                name=child["name"], # 🌠 format
                url=child["url"], # 🌠 format
                icon="", # 🌠 improve
                full_path=full_path
            )