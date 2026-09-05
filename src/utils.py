import json
from pathlib import Path
from typing import Any

from translate import Translator

from src.airplane import Airplane


def translate_text(text: str) -> Any:
    """Переводит текст"""

    translator_to_en = Translator(to_lang="en")

    if "а" <= text[0] <= "я" or "А" <= text[0] <= "Я":
        return translator_to_en.translate(text).title()
    return text.title()


def write_file(file: str, api_airplanes: list) -> None:
    """Производит запись о самолетах в файл"""

    path_file = Path(__file__).resolve().parent.parent / "data" / file
    aeroplanes_list = []

    for dt in api_airplanes:
        try:
            aeroplane = Airplane(dt[0], dt[2], dt[9], dt[13])

            aeroplanes_list.append(
                {
                    "ICAO24": aeroplane.ICAO24,
                    "Country": aeroplane.Country_of_registration,
                    "Velocity": aeroplane.velocity,
                    "Altitude": aeroplane.geo_altitude,
                }
            )
        except ValueError:
            print("Не добавлена информация о самолетах в файл")

    if aeroplanes_list:
        with open(path_file, "w", encoding="utf-8") as f:
            json.dump(aeroplanes_list, f, indent=4, ensure_ascii=False)

        print("Добавлена информация о самолетах в файл\n")
