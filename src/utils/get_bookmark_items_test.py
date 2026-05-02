import os
import sys
from unittest.mock import MagicMock
import pytest
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

@pytest.fixture(scope="session")
def before_all():
    dirname = os.path.dirname(__file__)

    personal_path = os.path.abspath(
        os.path.join(dirname, "../test/mock/Default/")
    )

    work_path = os.path.abspath(os.path.join(
        dirname, "../test/mock/Profile 1")
    )

    preferences = {
        "max_results": "10",
        "profiles": f"personal={personal_path}; work={work_path}",
        "base_bookmark_path": "other"
    }

    repository = BookmarkRepository(
        "com.github.mateuspitura.extension-ulauncher-bookmark-test"
    )

    populate_from_profiles(repository, preferences)

    return {
        "repository": repository,
        "preferences": preferences
    }


def test_search_all_profiles(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "gm",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "Gmail"
    assert result[0]["description"] == "(personal) • example.com"

    assert result[1]["name"] == "Figma"
    assert result[1]["description"] == "(personal) • example.com"

    assert result[2]["name"] == "Gmail"
    assert result[2]["description"] == "(work) • example.com"

def test_partial_search_in_subfolders(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "ocean",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "DigitalOcean"
    assert result[0]["description"] == "(work) mashable • example.com"

    assert result[1]["name"] == "DigitalOcean"
    assert result[1]["description"] == "(personal) • example.com"

    assert result[2]["name"] == "DigitalOcean"
    assert result[2]["description"] == "(work) mashable/rotten tomatoes • example.com"

def test_filter_by_profile(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "personal ",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "Indeed"
    assert result[0]["description"] == "Click to filter by this folder"

    assert result[1]["name"] == "Archive.org"
    assert result[1]["description"] == "Click to filter by this folder"

    assert result[2]["name"] == "Scribd"
    assert result[2]["description"] == "Click to filter by this folder"

    assert result[3]["name"] == "TinyURL"
    assert result[3]["description"] == "Click to filter by this folder"

    assert result[4]["name"] == "Proton Mail"
    assert result[4]["description"] == "(personal) • example.com"

    assert result[5]["name"] == "Glitch"
    assert result[5]["description"] == "(personal) scribd • example.com"

    assert result[6]["name"] == "Slack"
    assert result[6]["description"] == "(personal) indeed • example.com"

    assert result[7]["name"] == "Pastebin"
    assert result[7]["description"] == "(personal) archive.org • example.com"

    assert result[8]["name"] == "Overleaf"
    assert result[8]["description"] == "(personal) • example.com"

    assert result[9]["name"] == "Mendeley"
    assert result[9]["description"] == "(personal) • example.com"

def test_filter_by_profile_and_partial_search(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "personal gm",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "Gmail"
    assert result[0]["description"] == "(personal) • example.com"

    assert result[1]["name"] == "Figma"
    assert result[1]["description"] == "(personal) • example.com"

def test_filter_by_profile_and_folder(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "personal tinyurl/",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "Memrise"
    assert result[0]["description"] == "(personal) tinyurl • example.com"

    assert result[1]["name"] == "WordPress"
    assert result[1]["description"] == "(personal) tinyurl • example.com"

    assert result[2]["name"] == "W3Schools"
    assert result[2]["description"] == "(personal) tinyurl • example.com"

def test_filter_by_profile_and_folder_and_partial_search(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "personal tinyurl/press",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "WordPress"
    assert result[0]["description"] == "(personal) tinyurl • example.com"

def test_show_subfolders(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "work ",
        "bm",
        preferences,
        repository
    )

    count_folders = sum(1 for item in result if item["description"] == "Click to filter by this folder")
    assert count_folders == 5

def test_search_subfolder(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "work glitch",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "Glitch"
    assert result[0]["description"] == "Click to filter by this folder"

def test_filter_folder_without_profile(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "mashable/",
        "bm",
        preferences,
        repository
    )

    assert len(result) == 10

def test_filter_subfolder_without_profile(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "glitch/",
        "bm",
        preferences,
        repository
    )

    assert len(result) == 5

def test_search_subfolder_without_profile(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "glitch",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "Glitch"
    assert result[0]["description"] == "Click to filter by this folder"

def test_no_folders_empty_query(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "",
        "bm",
        preferences,
        repository
    )

    count_folders = sum(1 for item in result if item["description"] == "Click to filter by this folder")
    assert count_folders == 0

def test_show_profiles_empty_query(before_all):
    preferences = before_all['preferences']
    repository = before_all['repository']

    result = get_bookmark_items(
        "",
        "bm",
        preferences,
        repository
    )

    assert result[0]["name"] == "personal"
    assert result[0]["description"] == "Click to filter by this profile"

    assert result[1]["name"] == "work"
    assert result[1]["description"] == "Click to filter by this profile"
