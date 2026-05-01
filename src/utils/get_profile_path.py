def get_profile_path(keyword, extension):
    profiles = extension.preferences.get("profiles", "")
    for profile in profiles.split(";"):
        if "=" in profile:
            name, path = profile.split("=", 1)
            if name.strip() == keyword:
                return path.strip()
    raise Exception("Profile not found for keyword: " + keyword)