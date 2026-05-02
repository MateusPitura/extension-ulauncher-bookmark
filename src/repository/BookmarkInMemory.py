class BookmarkInMemory:
    def __init__(self, _dirname):
        pass

    def insert_bookmark(self, name, url, full_path, last_used, profile):
        raise Exception("Not implemented")

    def search_by_url(self, _query, _profile, _limit, _profiles):
        return [
            {
                "id": 1,
                "name": "Documents",
                "url": "https://www.example.com/path/to/resource",
                "full_path": "school/documents",
                "last_used": 13421001641019048,
                "profile": "personal"
            }
        ]

    def search_by_folder(self, _query, _profile, _limit, _profiles):
        return [
            {
                "id": 1,
                "name": "School",
                "full_path": "school",
                "last_used": 13421001641019048,
                "profile": "personal"
            }
        ]

    def insert_folder(self, name, full_path, last_used, profile):
        raise Exception("Not implemented")

    def update_url_last_used_by_id(self, item_id, last_used):
        raise Exception("Not implemented")

    # 🌠 not implemented
    def update_folder_last_used_by_id(self, item_id, last_used):
        raise Exception("Not implemented")
