def remove_bookmark_name(path):
    parts = path.split("/")
    return "/".join(parts[:-1])
