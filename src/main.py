from src.db_manager import DBManager
from src.utils import end, translate_text


def creation_of_aircraft_database(countries:list[str]) -> None:
    """Работает с базой данных о самолетах в воздушном пространстве указанных стран"""

    dbm = DBManager('airplanes', 'database.ini', countries)

    # # Самолеты по странам
    # data=dbm.get_countries_and_aeroplanes_count()
    # for key,value in data.items():
    #     print(f'В пространстве "{translate_text(key)}" находится {value} самолет{end(value)}')
    #
    # # Всего самолетов
    # data=dbm.get_all_aeroplanes()
    # counter = 0
    # countries = [translate_text(country.title()) for country in countries]
    # for dt in data:
    #     counter+=len(dt)
    # print(f'\nВсего в пространствах {', '.join(countries).title()} находятся {counter} самолет{end(counter)}')

    # Средняя скорость самолетов
    print(dbm.get_avg_speed())

if __name__ == "__main__":
    creation_of_aircraft_database(['germany','poland','italy','hungary'])