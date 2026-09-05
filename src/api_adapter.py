from abc import ABC
from abc import abstractmethod
from typing import Any


class APIAdapter(ABC):
    """Шаблон для классов, работающих с api"""

    def __init__(self) -> None:
        self.url = ""

    @abstractmethod
    def obtaining_information(self) -> Any:
        """Получает информацию из api"""
        pass
