from configparser import ConfigParser
from typing import Any

from translate import Translator
import psycopg2


def translate_text(text: str) -> Any:
    """Переводит текст"""

    translator_to_ru = Translator(to_lang="ru")

    return translator_to_ru.translate(text).title()


def end(number) -> str:
    """Определяет окончание слова, обозначающего число"""

    if 10 <= number % 100 <= 14:
        return "ов"
    else:
        last_digit = number % 10
        if last_digit == 1:
            return ""
        elif last_digit in (2, 3, 4):
            return "а"
        else:
            return "ов"


def config(path) -> dict:
    """Выдает параметры подключения к базе данных"""

    parser = ConfigParser()
    parser.read(path)

    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        params = {param[0]: param[1] for param in params}
    else:
        raise Exception("Section {0} is not found in the {1} file.".format("postgresql", path))

    return params


def conn_decorator(func):
    """Создает и закрывает соединение с базой данных"""

    def wrapper(*args):
        try:
            conn = psycopg2.connect(dbname=args[0].db_name, **args[0].params)
            cur = conn.cursor()

            result = func(args[0], cur, args[1]) if len(args)>1 else func(args[0], cur)

            cur.close()
            conn.close()
            return result

        except Exception:
            print('Ошибка получения данных')

    return wrapper
