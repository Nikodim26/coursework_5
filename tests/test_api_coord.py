from unittest.mock import patch

from src.api_coord import ApiCoord


@patch("requests.get")
def test_obtaining_information(mock_get) -> None:
    api_coord = ApiCoord("Germany")
    mock_get.return_value.json.return_value = [{"boundingbox": ["1", "2", "3", "4"]}]
    mock_get.return_value.status_code = 200
    assert api_coord.obtaining_information() == {"lamin": "1", "lamax": "2", "lomin": "3", "lomax": "4"}


@patch("requests.get")
def test_obtaining_information_err(mock_get) -> None:
    api_coord = ApiCoord("Germany")
    mock_get.return_value.json.return_value = [{"boundingbox": ["1", "2", "3", "4"]}]
    mock_get.return_value.status_code = 400
    assert api_coord.obtaining_information() is None
