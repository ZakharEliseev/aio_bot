import psycopg
from db_config import get_params


class BotDB:

    def __init__(self):
        self.connection = psycopg.connect(**get_params())
        self.cursor = self.connection.cursor()

    def create_table_users(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(30) UNIQUE,
                    user_id INTEGER UNIQUE
                );
            """)
            self.connection.commit()
            print('Table "users" is created!!!')
        except Exception as e:
            print(f"Error creating table: {e}")

    def create_table_favorite_cities(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorite_cities (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
                    service_name VARCHAR(30),
                    city VARCHAR(30)
                );
            """)
            self.connection.commit()
            print('Table "favorite_cities" is created!!!')
        except Exception as e:
            print(f"Error creating table 'favorite_cities': {e}")

    def create_table_user_requests(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_requests (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
                    service_name VARCHAR(30),
                    city VARCHAR(30)
                );
            """)
            self.connection.commit()
            print('Table "user_requests" is created!!!')
        except Exception as e:
            print(f"Error creating table 'user_requests': {e}")

    def user_exists(self, user_id):
        self.cursor.execute("SELECT id \
                                    FROM users \
                                    WHERE user_id = %s",
                            (user_id,))
        return bool(self.cursor.fetchone())

    def get_user_id(self, user_id):
        try:
            result = self.cursor.execute("SELECT id \
                                                FROM users \
                                                WHERE user_id = %s",
                                         (user_id,))
            return result.fetchone()[0]
        except Exception as e:
            print(f'Error getting user_id: , {e}')

    def add_user(self, user_id, username):
        try:
            self.cursor.execute("INSERT INTO users (user_id, username) \
                                        VALUES (%s, %s)",
                                (user_id, username))
            self.connection.commit()
        except Exception as e:
            print(f'Error adding user: , {e}')

    def add_last_request(self, user_id, city, service_name):
        try:
            self.cursor.execute("INSERT INTO user_requests (user_id, city, service_name) \
                                        VALUES (%s, %s, %s)",
                                (user_id, city, service_name))
            self.connection.commit()
        except Exception as e:
            print(f'Error adding last query: , {e}')

    def get_last_request(self, user_id, service_name):
        self.cursor.execute("SELECT city \
                            FROM user_requests \
                            WHERE user_id = %s \
                            AND service_name = %s \
                            ORDER BY id \
                            DESC LIMIT 1",
                            (user_id, service_name))
        city_id = self.cursor.fetchone()
        return f'{str(city_id[0])}'

    def close(self):
        self.connection.close()
        print("Database connection closed.")
