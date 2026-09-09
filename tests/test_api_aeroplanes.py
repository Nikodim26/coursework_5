from unittest.mock import patch

from src.api_airplanes import ApiAeroplanes


@patch("requests.get")
def test_obtaining_information(mock_get) -> None:
    api_aeroplanes = ApiAeroplanes({})
    mock_get.return_value.json.return_value = {"states": ["aa9300", "UAL47", "United States", 178758, 178758]}
    mock_get.return_value.status_code = 200
    assert api_aeroplanes.obtaining_information() == ["aa9300", "UAL47", "United States", 178758, 178758]


@patch("requests.get")
def test_obtaining_information_err(mock_get) -> None:
    api_aeroplanes = ApiAeroplanes({})
    mock_get.return_value.json.return_value = {"states": ["aa9300", "UAL47", "United States", 178758, 178758]}
    mock_get.return_value.status_code = 400
    assert api_aeroplanes.obtaining_information() is None
