import pytest

from src.db_manager import DBManager
import psycopg2


@pytest.fixture
def fixture_for_object_construction() -> DBManager:
    dbm = DBManager('db_name', 'database.ini', ['a'])

    conn = psycopg2.connect(dbname='postgres', **dbm.params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('DROP DATABASE db_name WITH (FORCE);')
    cur.close()
    conn.close()

    return dbm


@pytest.fixture
def fixture_for_dbm_functions(fixture_for_object_construction) -> None:
    dbm = fixture_for_object_construction
    dbm.creating_a_database(dbm.params, 'base')

    dt = [
        ["a", "b", "c", 1, 1, -0.0168, 51.0888, 4267.2, 'false', 189.7, 129.39, 14.63, 'null', 4282.44, "d", 'false', 0],
        ["a", "b", "c", 1, 1, -0.0168, 51.0888, 4267.2, 'false', 189.7, 129.39, 14.63, 'null', 4282.44, "d", 'false', 0],
        ["a", "b", "c", 1, 1, -0.0168, 51.0888, 4267.2, 'false', 189.7, 129.39, 14.63, 'null', 4282.44, "d", 'false', 0],
        ["a", "b", "c", 1, 1, -0.0168, 51.0888, 4267.2, 'false', 189.7, 129.39, 14.63, 'null', 4282.44, "d", 'false', 0],
        ["a", "b", "c", 1, 1, -0.0168, 51.0888, 4267.2, 'false', 189.7, 129.39, 14.63, 'null', 4282.44, "d", 'false', 0]
    ]

    dbm.creating_a_table('a', dt, 'base', dbm.params)
