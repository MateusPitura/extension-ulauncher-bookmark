from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction


def get_folder_item(item, keyword):
    folder_name = item.get("name", "Unknown")
    full_path = item.get("full_path", "")

    return {
        "icon": "images/folder.png",
        "name": folder_name,
        "description": "Click to filter by this folder",
        "on_enter": SetUserQueryAction(f"{keyword} {full_path}/")
    }
