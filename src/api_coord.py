from typing import Any

import requests

from src.api_adapter import APIAdapter


class ApiCoord(APIAdapter):
    """Класс объекта, отвечающего за получение координат "квадрата" определенной страны"""

    def __init__(self, country: str) -> None:
        super().__init__()
        self.url = "https://nominatim.openstreetmap.org/search"
        self.country = country
        self.coordinates = self.obtaining_information()

    def obtaining_information(self) -> Any:
        """Получает из api-ресурса координаты "квадрата" определенной страны"""

        headers_nominatim = {"User-Agent": "test-app/1.0"}
        params_nominatim = {"country": self.country, "format": "json", "limit": 1}

        try:
            for i in range(3):
                response = requests.get(url=self.url, params=params_nominatim, headers=headers_nominatim, timeout=10)
                if str(response.status_code)[0] == "2":
                    geo_coordinates = response.json()[0].get("boundingbox")

                    result = {
                        "lamin": geo_coordinates[0],
                        "lamax": geo_coordinates[1],
                        "lomin": geo_coordinates[2],
                        "lomax": geo_coordinates[3],
                    }
                    return result

        except Exception as e:
            print(e)
            return {}


if __name__ == "__main__":
    a = ApiCoord("германия")
    print(a.coordinates)
