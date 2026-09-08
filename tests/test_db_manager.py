from pathlib import WindowsPath

import psycopg2


def test_object_construction(fixture_for_object_construction) -> None:
    dbm = fixture_for_object_construction
    assert dbm.db_name == 'db_name'
    assert dbm.countries == ['a']
    assert dbm.path == WindowsPath('E:/Учеба питон/коды/5 курс/coursework/database.ini')
    assert dbm.tables == [('tb_a',)]
    assert dbm.params['host'] == 'localhost'


def test_config(fixture_for_object_construction) -> None:
    dbm = fixture_for_object_construction
    assert dbm.config(dbm.path) == dbm.params


def test_creating_a_database(fixture_for_object_construction) -> None:
    dbm = fixture_for_object_construction
    dbm.creating_a_database(dbm.params, 'base')

    conn = psycopg2.connect(dbname='postgres', **dbm.params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database;")
    tables = cur.fetchall()
    assert ('base',) in tables
    cur.execute('DROP DATABASE base WITH (FORCE);')
    cur.close()
    conn.close()

def test_creating_a_table(fixture_for_object_construction)->None:
    dbm = fixture_for_object_construction
    dbm.creating_a_database(dbm.params, 'base')
    dbm.creating_a_table('a', [], 'base', dbm.params)

    conn = psycopg2.connect(dbname='base', **dbm.params)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables "
                "WHERE table_type = 'BASE TABLE' AND table_schema = 'public';")
    tables = cur.fetchall()
    assert tables==[('tb_a',)]
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname='postgres', **dbm.params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('DROP DATABASE base WITH (FORCE);')
    cur.close()
    conn.close()

def test_get_countries_and_aeroplanes_count(fixture_for_dbm_functions)->None:
    assert 1==1