def remove_url_prefix(url):
    prefixes = ["http://www.", "https://www.", "http://", "https://"]
    for prefix in prefixes:
        if url.startswith(prefix):
            return url[len(prefix):]
    return url