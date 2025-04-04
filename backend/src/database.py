import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="./.env")

# Establish database connection and create the database if not exists
def create_database():
    conn = psycopg2.connect(
        dbname="postgres",  # Connect to the default system database
        user=os.getenv('POSTGRES_USER', 'myUser'),
        password=os.getenv('POSTGRES_PASSWORD', 'myPass'),
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', 5432),
    )
    conn.autocommit = True
    cursor = conn.cursor()

    database_name = os.getenv('POSTGRES_DATABASE', 'mydatabase')
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
    if not cursor.fetchone():
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"✅ Database '{database_name}' created successfully!")
    else:
        print(f"✅ Database '{database_name}' already exists.")

    cursor.close()
    conn.close()

create_database()  # Ensure the database exists before proceeding

# Connect to the newly created database
try:
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DATABASE', 'mydatabase'),
        user=os.getenv('POSTGRES_USER', 'myUser'),
        password=os.getenv('POSTGRES_PASSWORD', 'myPass'),
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', 5432),
        cursor_factory=RealDictCursor
    )
    conn.autocommit = True
    print("✅ Successfully connected to PostgreSQL!")
except Exception as e:
    print(f"❌ Error connecting to PostgreSQL: {e}")
    conn = None

# Ensure users table exists
def create_users_table():
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        firstname VARCHAR(50) NOT NULL,
                        lastname VARCHAR(50) NOT NULL,
                        country VARCHAR(50) NOT NULL,
                        gender VARCHAR(10) NOT NULL
                    );
                """)
                print("✅ 'users' table checked/created successfully!")
        except Exception as e:
            print(f"❌ Error creating 'users' table: {e}")

create_users_table()  # Ensure table exists

def get_db():
    return conn
