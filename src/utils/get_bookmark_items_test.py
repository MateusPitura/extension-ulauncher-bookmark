import sys
from unittest.mock import MagicMock
from src.repository.BookmarkInMemory import BookmarkInMemory

mock_module = MagicMock()
mock_class = MagicMock()
mock_class.side_effect = lambda **kwargs: kwargs
mock_module.ExtensionResultItem = mock_class

sys.modules["ulauncher.api.shared.item.ExtensionResultItem"] = mock_module
sys.modules["ulauncher.api.shared.action.SetUserQueryAction"] = MagicMock()
sys.modules["ulauncher.api.shared.action.ExtensionCustomAction"] = MagicMock()

from src.utils.get_bookmark_items import get_bookmark_items

def test_execute_successfully():
    result = get_bookmark_items(
        "personal bookma",
        "bm",
        {
            "max_results": "10",
            "profiles": "personal=~/.config/google-chrome/Default/; work=~/.config/google-chrome/Profile 1/"
        },
        BookmarkInMemory("__dirname__")
    )

    assert result[0]["icon"] == "images/folder.png"
    assert result[0]["name"] == "School"
    assert result[0]["description"] == "Click to filter by this folder"

    assert result[1]["icon"] == "images/chrome.png"
    assert result[1]["name"] == "Documents"
    assert result[1]["description"] == "(school/documents) • example.com/path/to/resource"
