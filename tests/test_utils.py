import pytest

from src.utils import end
from src.utils import translate_text


def test_translate_text() -> None:
    assert translate_text("germany") == "Германия"
    assert translate_text("poland") == "Польша"


@pytest.mark.parametrize("x, expected", [(1, ""), (2, "а"), (5, "ов"), (134, "а"), (241, ""), (1056, "ов")])
def test_end(x: int, expected: str) -> None:
    assert end(x) == expected
