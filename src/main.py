from src.api_airplanes import ApiAeroplanes
from src.api_coord import ApiCoord


def creation_of_aircraft_database(countries:list[str]) -> None:
    """Создает базу данных о самолетах в воздушном пространстве указанных стран"""

    a=[]
    for country in countries:
        api_coord = ApiCoord(country)
        api_aeroplanes = ApiAeroplanes(api_coord.coordinates).list_info
        





if __name__ == "__main__":
    creation_of_aircraft_database(['germany','poland','italy','hungary'])