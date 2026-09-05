from typing import Any

import requests

from src.api_adapter import APIAdapter


class ApiAeroplanes(APIAdapter):
    """Класс объекта, отвечающего за получение информации о самолетах в заданном "квадрате\" """

    def __init__(self, coordinates: dict) -> None:
        super().__init__()
        self.coordinates = coordinates
        self.url = "https://opensky-network.org/api/states/all?"
        self.list_info = self.obtaining_information()

    def obtaining_information(self) -> list:
        """Получение информации о самолетах в координатах страны"""

        try:
            for i in range(3):
                response = requests.get(url=self.url, params=self.coordinates)
                if str(response.status_code)[0] == "2":
                    return response.json()["states"]

        except Exception as e:
            print(e)
            return []
