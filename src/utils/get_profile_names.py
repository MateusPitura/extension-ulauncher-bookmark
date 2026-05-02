def get_profile_names(extension):
    profiles = extension.preferences.get("profiles", "")

    profiles_names = []
    for profile in profiles.split(";"):
        if "=" in profile:
            name = profile.split("=", 1)[0].strip()

            profiles_names.append(name.strip())
    return profiles_names
