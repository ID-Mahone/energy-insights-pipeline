import os
from sqlalchemy import create_engine

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "energy_db")
DB_USER = os.getenv("DB_USER", "energy_user")
DB_PASS = os.getenv("DB_PASS", "energy_pass")

def get_engine():
    return create_engine(f"postgresl://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")
