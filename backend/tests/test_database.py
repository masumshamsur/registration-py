import os
import pytest
from unittest.mock import patch, MagicMock
from backend.src.database import create_database, create_users_table, get_db

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('POSTGRES_USER', 'test_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'test_password')
    monkeypatch.setenv('POSTGRES_HOST', 'localhost')
    monkeypatch.setenv('POSTGRES_PORT', '5432')
    monkeypatch.setenv('POSTGRES_DATABASE', 'test_database')

@patch('psycopg2.connect')
def test_create_database(mock_connect, mock_env_vars):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value

    mock_cursor.fetchone.return_value = None  # DB does not exist

    create_database()

    mock_connect.assert_called_once_with(
        dbname="postgres",
        user="test_user",
        password="test_password",
        host="localhost",
        port="5432",
    )

    mock_cursor.execute.assert_any_call("SELECT 1 FROM pg_database WHERE datname = 'test_database'")
    mock_cursor.execute.assert_any_call("CREATE DATABASE test_database")


@patch('backend.src.database.psycopg2.connect')
def test_create_users_table(mock_connect):
    # Create mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    # Call the function with mock connection
    create_users_table(mock_conn)

    # Check that cursor.execute() was called once with correct SQL
    mock_cursor.execute.assert_called_once_with("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        firstname VARCHAR(50) NOT NULL,
                        lastname VARCHAR(50) NOT NULL,
                        country VARCHAR(50) NOT NULL,
                        gender VARCHAR(10) NOT NULL
                    );
                """)

    # Optionally, check that connection was not closed inside the function
    mock_conn.close.assert_not_called()