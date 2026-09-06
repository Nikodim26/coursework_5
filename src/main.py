from src.db_manager import DBManager


def creation_of_aircraft_database(countries:list[str]) -> None:
    """Работает с базой данных о самолетах в воздушном пространстве указанных стран"""

    dbm = DBManager('airplanes', 'database.ini', countries)

    data=dbm.get_countries_and_aeroplanes_count()
    for key,value in data.items():
        print(f'В пространстве {key} находится {value} самолет')

    # dbm.get_all_aeroplanes()

if __name__ == "__main__":
    creation_of_aircraft_database(['germany','poland','italy','hungary'])