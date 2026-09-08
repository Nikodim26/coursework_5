def test_object_construction(fixture_for_object_construction) -> None:
    dbm = fixture_for_object_construction
    assert dbm.db_name == "db_name"
    assert dbm.countries == ["a"]
    assert dbm.path.name == "database.ini"
    assert dbm.tables.call_count == 0
    assert dbm.params["host"] == "localhost"


def test_config(fixture_for_object_construction) -> None:
    dbm = fixture_for_object_construction
    assert dbm.config(dbm.path) == dbm.params
