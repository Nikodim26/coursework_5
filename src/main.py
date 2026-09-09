from src.db_manager import DBManager
from src.utils import end
from src.utils import translate_text


def creation_of_aircraft_database(countries: list[str]) -> None:
    """Работает с базой данных о самолетах в воздушном пространстве указанных стран"""

    dbm = DBManager("airplanes", "database.ini", countries)

    # Самолеты по странам
    data = dbm.get_countries_and_aeroplanes_count()
    for key, value in data.items():
        print(f'В пространстве "{translate_text(key)}" находится {value} самолет{end(value)}')

    # Всего самолетов
    data = dbm.get_all_aeroplanes()
    countries = [translate_text(country.title()) for country in countries]
    print(f"\n{data}")
    print(f"Всего в пространствах {', '.join(countries).title()} находятся {len(data)} самолет{end(len(data))}\n")

    # Средняя скорость самолетов
    print(f"Средняя скорость самолетов {round(dbm.get_avg_speed(), 2)} м/с")

    # Самолеты со скоростью выше средней
    print("\nСамолеты со скоростью выше средней")
    print(dbm.get_aeroplanes_with_higher_speed())

    # Самолеты с позывным, содержащим заданные символы
    symbols = "PGT"
    print(f'\nСамолеты с позывным, содержащим символы "{symbols}"')
    print(dbm.get_aeroplanes_with_keyword(symbols))


if __name__ == "__main__":
    creation_of_aircraft_database(["germany", "poland", "italy", "hungary"])
