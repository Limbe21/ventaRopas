# models/database.py
import psycopg2
from config import Config

class Database:
    @staticmethod
    def get_connection():
        try:
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT
            )
            return conn
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None