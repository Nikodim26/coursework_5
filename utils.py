from typing import Any

from translate import Translator

def translate_text(text: str) -> Any:
    """Переводит текст"""

    translator_to_en = Translator(to_lang="en")

    if "а" <= text[0] <= "я" or "А" <= text[0] <= "Я":
        return translator_to_en.translate(text).title()
    return text.title()

def end(number)->str:


    if 10 <= number % 100 <= 14: return 'ов'
    else:
        last_digit = number % 10
        if last_digit == 1: return ''
        elif last_digit in (2, 3, 4): return 'a'
        else: return 'ов'