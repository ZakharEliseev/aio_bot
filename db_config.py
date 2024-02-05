from dotenv import load_dotenv
import os


def get_params():
    load_dotenv()
    db_params = {
        'dbname': "weather_data",
        'user': "user_admin",
        'password': os.getenv("POSTGRES_PASSWORD"),
        'host': "postgres",
        'port': "5432"
    }
    return db_params
