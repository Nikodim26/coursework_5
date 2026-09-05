from src.api_airplanes import ApiAeroplanes
from src.api_coord import ApiCoord
from src.db_manager import DBManager


def creation_of_aircraft_database(countries:list[str]) -> None:
    """Создает базу данных о самолетах в воздушном пространстве указанных стран"""

    a=[]
    for country in countries:
        api_coord = ApiCoord(country)
        api_aeroplanes = ApiAeroplanes(api_coord.coordinates).list_info

        dbm = DBManager('airplanes', 'database.ini')

        dbm.working_with_the_base(f'''CREATE TABLE IF NOT EXISTS tb_{country} (
                                airplane_id SERIAL PRIMARY KEY,
                                ICAO24 VARCHAR(10) NOT NULL,
                                Callsign  VARCHAR(10) NOT NULL,
                                Country_of_reg VARCHAR(20) NOT NULL,
                                Velocity REAL,
                                Geo_altitude REAL,
                                Longitude REAL,
                                Latitude REAL,
                                True_track REAL,
                                On_ground BOOLEAN                                
                            )
                            ''')
        # break



if __name__ == "__main__":
    creation_of_aircraft_database(['germany','poland','italy','hungary'])