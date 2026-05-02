import sys
from unittest.mock import MagicMock
from src.repository.BookmarkRepository import BookmarkRepository
from src.utils.populate_from_profiles import populate_from_profiles

mock_module = MagicMock()
mock_class = MagicMock()
mock_class.side_effect = lambda **kwargs: kwargs
mock_module.ExtensionResultItem = mock_class

sys.modules["ulauncher.api.shared.item.ExtensionResultItem"] = mock_module
sys.modules["ulauncher.api.shared.action.SetUserQueryAction"] = MagicMock()
sys.modules["ulauncher.api.shared.action.ExtensionCustomAction"] = MagicMock()

from src.utils.get_bookmark_items import get_bookmark_items

def test_execute_successfully():
    preferences = {
        "max_results": "10",
        "profiles": "personal=~/.config/google-chrome/Default/; work=~/.config/google-chrome/Profile 1/",
        "base_bookmark_path": "other"
    }

    repository = BookmarkRepository("com.github.mateuspitura.extension-ulauncher-bookmark-test")

    populate_from_profiles(repository, preferences)

    result = get_bookmark_items(
        "personal gm",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "Gmail"
    assert result[0]["description"] == "(gmail) • mail.google.com/mail/u/0/"

    assert result[1]["name"] == "Figma"
    assert result[1]["description"] == "(figma) • figma.com/files/drafts"
