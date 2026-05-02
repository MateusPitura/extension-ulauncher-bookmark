from src.utils.remove_url_prefix import remove_url_prefix


def test_execute_successfully():
    result = remove_url_prefix("https://www.example.com/path/to/resource")
    assert result == "example.com/path/to/resource"
