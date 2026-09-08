from unittest.mock import patch, MagicMock

import pytest

from src.db_manager import DBManager

@pytest.fixture
@patch('psycopg2.connect')
def fixture_for_object_construction(mock_connect):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    dbm = DBManager('db_name', 'database.ini', ['a'])

    return dbm
