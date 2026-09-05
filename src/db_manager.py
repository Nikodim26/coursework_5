from configparser import ConfigParser
from pathlib import Path
import psycopg2


class DBManager():
    def __init__(self, db_name: str, filename: str) -> None:
        self.path = Path(__file__).resolve().parent.parent / filename
        self.db_name = db_name

        parser = ConfigParser()
        parser.read(self.path)

        if parser.has_section("postgresql"):
            params = parser.items("postgresql")
            self.params = {param[0]: param[1] for param in params}
        else:
            raise Exception('Section {0} is not found in the {1} file.'.format("postgresql", self.path))

        self.creating_a_database()

    def creating_a_database(self) -> None:
        """Создает базу данных"""

        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {self.db_name}")

        cur.close()
        conn.close()

    def creating_a_table(self, country: str) -> None:
        """Создает таблицу с характеристиками самолетов над страной"""

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS tb_{country} (
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
        cur.close()
        conn.close()
