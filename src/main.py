from src.api_airplanes import ApiAeroplanes
from src.api_coord import ApiCoord
from src.db_manager import DBManager


def creation_of_aircraft_database(countries:list[str]) -> None:
    """Создает базу данных о самолетах в воздушном пространстве указанных стран"""

    dbm = DBManager('airplanes', 'database.ini')

    for country in countries:
        api_coord = ApiCoord(country)
        api_aeroplanes = ApiAeroplanes(api_coord.coordinates).list_info

        dbm.creating_a_table(country,api_aeroplanes)





        # break
        a=1


if __name__ == "__main__":
    creation_of_aircraft_database(['germany','poland','italy','hungary'])