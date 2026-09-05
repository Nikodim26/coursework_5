from configparser import ConfigParser
from pathlib import Path
import psycopg2


class DBManager():
    def __init__(self, db_name, filename):
        self.db_name = db_name
        self.path = Path(__file__).resolve().parent.parent / filename

    def config(self, section="postgresql") -> dict:
        """Считывает параметры подключения к postgresql"""

        parser = ConfigParser()
        parser.read(self.path)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                'Section {0} is not found in the {1} file.'.format(section, self.path))
        return db

    def creating_a_database(self) -> None:

        params = self.config()
        conn = psycopg2.connect(dbname='postgres', **params)
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {self.db_name}")

        cur.close()
        conn.close()

    def working_with_the_base(self, request: str) -> None:
        """Работает с базой данных"""

        params = self.config()
        conn = psycopg2.connect(dbname=self.db_name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(request)

        cur.close()
        conn.close()


dbm = DBManager('aaa', 'database.ini')
dbm.creating_a_database()
dbm.working_with_the_base('''CREATE TABLE IF NOT EXISTS channels (
                            channel_id SERIAL PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            views INTEGER,
                            subscribers INTEGER,
                            videos INTEGER,
                            channel_url TEXT
                        )
                        ''')
