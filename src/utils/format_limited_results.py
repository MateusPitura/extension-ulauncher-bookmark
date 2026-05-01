from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

def format_limited_results(items, extension):
    max_results = extension.preferences.get("max_results")

    if not max_results.isdigit() or int(max_results) <= 0:
        raise Exception("Invalid max_results value: " + max_results)

    return [
        ExtensionResultItem(
            icon=item["icon"],
            name=item["name"],
            description=item["description"],
            on_enter=item["on_enter"]
        )
        for item in items[:int(max_results)]
    ]