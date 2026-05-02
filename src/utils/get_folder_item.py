from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction

def get_folder_item(item, event):
    keyword = event.get_keyword()

    folder_name = item.get("name", "Unknown")
    full_path = item.get("full_path", "")

    profile_name = full_path.split(" ")[0].strip()

    return {
        "icon": "images/folder.png",
        "name": f"({profile_name}) • {folder_name}",
        "description": "Click to filter by this folder",
        "on_enter": SetUserQueryAction(f"{keyword} {full_path}/")
    }
