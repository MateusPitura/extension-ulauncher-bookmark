from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction


def get_profiles_items(keyword, preferences):
    profiles = preferences.get("profiles", "")

    profiles_names = []
    for profile in profiles.split(";"):
        if "=" in profile:
            name = profile.split("=", 1)[0].strip()

            profiles_names.append({
                "icon": "images/logo.png",  # 🌠 try to get profile picture
                "name": name.strip(),
                "description": "Click to filter by this profile",
                "on_enter": SetUserQueryAction(f"{keyword} {name.strip()} "),
            })
    return profiles_names
