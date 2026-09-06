from configparser import ConfigParser
from pathlib import Path
import psycopg2

from src.api_airplanes import ApiAeroplanes
from src.api_coord import ApiCoord


class DBManager:

    def __init__(self, db_name: str, filename: str, countries: list) -> None:
        self.path = Path(__file__).resolve().parent.parent / filename
        self.db_name = db_name
        self.countries = countries
        self.params = DBManager.config(self.path)

        # self.creating_a_database(self.params, self.db_name)

        # aaa = [{'lamin': '47.2701114', 'lamax': '55.0991610', 'lomin': '5.8663153', 'lomax': '15.0419309'},
        #        {'lamin': '49.0020468', 'lamax': '55.0360500', 'lomin': '14.0696389', 'lomax': '24.1457830'},
        #        {'lamin': '35.2889616', 'lamax': '47.0921485', 'lomin': '6.6272658', 'lomax': '18.7844746'},
        #        {'lamin': '45.7371280', 'lamax': '48.5852570', 'lomin': '16.1138866', 'lomax': '22.8965048'}]
        # i=0
        # for country in countries:
        #     # api_coord = ApiCoord(country)
        #     # api_aeroplanes = ApiAeroplanes(api_coord.coordinates).list_info
        #     api_aeroplanes = ApiAeroplanes(aaa[i]).list_info
        #     i+=1
        #
        #     DBManager.creating_a_table(country, api_aeroplanes, self.db_name, self.params)

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()

        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_type = 'BASE TABLE' AND table_schema = 'public';")
        self.tables = cur.fetchall()

        cur.close()
        conn.close()

    @staticmethod
    def config(path):
        parser = ConfigParser()
        parser.read(path)

        if parser.has_section("postgresql"):
            params = parser.items("postgresql")
            params = {param[0]: param[1] for param in params}
        else:
            raise Exception('Section {0} is not found in the {1} file.'.format("postgresql", path))

        return params

    @staticmethod
    def creating_a_database(params, db_name) -> None:
        """Создает базу данных"""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {db_name}")

        cur.close()
        conn.close()

    @staticmethod
    def creating_a_table(country: str, data: list, db_name: str, params: dict) -> None:
        """Создает таблицу с характеристиками самолетов над страной"""

        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS tb_{country} (
                    airplane_id SERIAL PRIMARY KEY,
                    ICAO24 VARCHAR(10),
                    Callsign  VARCHAR(10),
                    Country_of_reg VARCHAR(50),
                    Velocity REAL,
                    Geo_altitude REAL,
                    Longitude REAL,
                    Latitude REAL,
                    True_track REAL,
                    On_ground BOOLEAN                                
                    )
                    ''')

        cur.execute(f'TRUNCATE TABLE public.tb_{country} RESTART IDENTITY')

        for dt in data:
            cur.execute(f"""INSERT INTO public.tb_{country} 
            (ICAO24,Callsign,Country_of_reg,Velocity,Geo_altitude,Longitude,Latitude,True_track,On_ground)             
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (dt[0], dt[1].strip(), dt[2], dt[9], dt[13], dt[5], dt[6], dt[10], dt[8]))

        cur.close()
        conn.close()

    def get_countries_and_aeroplanes_count(self) -> dict:
        """Получает список всех стран и количество самолетов в их воздушных пространствах."""

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()

        result = {}
        tables = self.tables
        for table in tables:
            cur.execute(f'select count(*) from {table[0]}')
            result[table[0][3:].title()] = cur.fetchall()[0][0]

        return result

    def get_all_aeroplanes(self) -> list:
        """получает список всех воздушных судов."""

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()

        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_type = 'BASE TABLE' AND table_schema = 'public';")
        result = []
        tables = cur.fetchall()
        for table in tables:
            cur.execute(f"SELECT ICAO24, Callsign, Country_of_reg FROM public.{table[0]};")
            result.extend(cur.fetchall())

        cur.close()
        conn.close()
        return result

    def get_avg_speed(self)-> float:
        """получает среднюю скорость по самолетам."""

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()

        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_type = 'BASE TABLE' AND table_schema = 'public';")
        result = 0
        tables = cur.fetchall()
        for table in tables:
            cur.execute(f"SELECT AVG(Velocity) FROM public.{table[0]};")
            result+= cur.fetchall()[0][0]

        cur.close()
        conn.close()
        return result/len(tables)

    def get_aeroplanes_with_higher_speed(self)->list:
        """получает список всех самолетов, у которых скорость выше средней."""

        velocity_avg=self.get_avg_speed()

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()

        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_type = 'BASE TABLE' AND table_schema = 'public';")
        result = []
        tables = cur.fetchall()
        for table in tables:
            cur.execute(f"SELECT ICAO24, Callsign, Country_of_reg, Velocity FROM public.{table[0]}"
                        f" WHERE Velocity > {velocity_avg};")
            result.extend(cur.fetchall())

        cur.close()
        conn.close()
        return result


    def get_aeroplanes_with_keyword(self, symbols:str)->list:
        """ получает список всех самолетов, в позывном которых содержатся переданные в метод символы."""

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()

        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_type = 'BASE TABLE' AND table_schema = 'public';")
        result = []
        tables = cur.fetchall()
        for table in tables:
            cur.execute(f"SELECT ICAO24, Callsign, Country_of_reg, Velocity FROM public.{table[0]}"
                        f" WHERE Callsign LIKE '%{symbols}%';")
            result.extend(cur.fetchall())

        cur.close()
        conn.close()
        return result
