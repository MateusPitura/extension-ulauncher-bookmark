import os
from src.utils.get_profile_path import get_profile_path
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction


def get_profiles_items(keyword, preferences):
    profiles = preferences.get("profiles", "")

    profiles_names = []
    for profile in profiles.split(";"):
        if "=" in profile:
            name = profile.split("=", 1)[0].strip()

            profile_path = get_profile_path(name, preferences)

            profiles_names.append({
                "icon": f"{profile_path}/Google Profile Picture.png",
                "name": name.strip(),
                "description": "Click to filter by this profile",
                "on_enter": SetUserQueryAction(f"{keyword} {name.strip()} "),
            })
    return profiles_names
