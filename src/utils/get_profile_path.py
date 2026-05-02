from src.utils.normalize_path import normalize_path


def get_profile_path(keyword, preferences):
    profiles = preferences.get("profiles", "")
    for profile in profiles.split(";"):
        if "=" in profile:
            name, path = profile.split("=", 1)
            if name.strip() == keyword:
                return normalize_path(path)
    raise Exception("Profile not found for keyword: " + keyword)
