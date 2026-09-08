from typing import Any

from translate import Translator

def translate_text(text: str) -> Any:
    """Переводит текст"""

    translator_to_ru = Translator(to_lang="ru")

    return translator_to_ru.translate(text).title()

def end(number)->str:
    """Определяет окончание слова, обозначающего число"""

    if 10 <= number % 100 <= 14: return 'ов'
    else:
        last_digit = number % 10
        if last_digit == 1: return ''
        elif last_digit in (2, 3, 4): return 'а'
        else: return 'ов'