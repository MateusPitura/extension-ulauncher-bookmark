def get_profile_path(keyword, extension):
    profiles = extension.preferences.get("profiles", "")
    print(f"🌠 profiles: {profiles}")
    for profile in profiles.split(";"):
        print(f"🌠 profile: {profile}")
        if "=" in profile:
            name, path = profile.split("=", 1)
            print(f"🌠 name: {name}")
            print(f"🌠 path: {path}")
            print(f"🌠 keyword: {keyword}")
            print(f"🌠 name.strip(): {name.strip()}")
            if name.strip() == keyword:
                print(f"🌠 path.strip(): {path.strip()}")
                return path.strip()
    raise Exception("Profile not found for keyword: " + keyword)