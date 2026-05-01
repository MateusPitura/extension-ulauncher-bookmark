def sort_by_date_last_used(items):
    return sorted(
        items,
        key=lambda item: item.get("date_last_used", 0),
        reverse=True
    )