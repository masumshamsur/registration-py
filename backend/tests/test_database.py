import os
import pytest
from unittest.mock import patch
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

@patch('psycopg2.connect')
def test_create_users_table(mock_connect, mock_env_vars):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value

    create_users_table()

    mock_cursor.execute.assert_called_once_with("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(50) NOT NULL,
            lastname VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            gender VARCHAR(10) NOT NULL
        );
    """)