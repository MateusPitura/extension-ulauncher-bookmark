from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


def get_max_results(extension):
    max_results = extension.preferences.get("max_results")

    if not max_results.isdigit() or int(max_results) <= 0:
        raise Exception("Invalid max_results value: " + max_results)

    return int(max_results)
