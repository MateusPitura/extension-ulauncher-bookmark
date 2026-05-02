from src.utils.remove_url_prefix import remove_url_prefix
from src.utils.remove_bookmark_name import remove_bookmark_name

def format_description(profile_name, rest_path, url):
    path = remove_bookmark_name(rest_path)

    prefix = f"({profile_name})"

    if path:
        prefix += f" {path}"

    return f"{prefix} • {remove_url_prefix(url)}"
