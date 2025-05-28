import psycopg2
from psycopg2.extras import DictCursor
from flask import current_app
from typing import Dict, List


class DBSingleton:
    _instance = None  # будет содержать инфу о существовании экземпляра класса (синглтон база)
    _connection = None  # будет содержать данные для коннекта к БД

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connect()
        return cls._instance  # создание экземпляра БД

    @classmethod  # декоратор на методы класса
    def _connect(cls):

        cls._connection = psycopg2.connect(
            dbname=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            cursor_factory=DictCursor
        )
        current_app.logger.info("Database connection established")  # данные для подключения бд и логгер

    @property  # декоратор для атрибутов, обращение не как к функции
    def connection(self):
        if self._connection is None or self._connection.closed:
            self._connect()
        return self._connection  # создание соединения с бд

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if cursor.description:
                return cursor.fetchall()
            return []  # настройка вывода для класса

    def get_film(self, title):
        return self.execute_query(
            """SELECT films.title, films.description, films.release_date, genres.genre_name, films.poster_link, 
    rating FROM film_genre
            JOIN films ON film_genre.film_id = films.film_id
            JOIN genres ON film_genre.genre_id = genres.genre_id
            WHERE films.title = %s""",
            (title,)
        )  # это и ниже - все функции с сервисов в прошлом, только реализованные как методы класса

    def get_director(self, title):

        return self.execute_query(
            """SELECT directors.first_name, directors.second_name FROM directors
            JOIN films ON directors.director_id = films.director_id
            WHERE films.title = %s""",
            (title,),

        )

    def get_comments(self, title):
        result = self.execute_query(
            """SELECT u.first_name, c.comment_text, c.created_at
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.film_id = %s
            ORDER BY c.created_at DESC""",
            (title,)
        )

        self.close()
        return result

    def get_genres(self):
        result = self.execute_query(
            """select *
                            from genres
                            """
        )
        self.close()
        return result

    def get_sessions(self, title) -> List[Dict]:
        result = self.execute_query("""
            SELECT sessions.session_id, sessions.time, sessions.price FROM sessions
            JOIN films ON sessions.film_id = films.film_id
            WHERE films.title = %s
            """, (title,))
        self.close()
        return result

    def get_ticket_info(self, user_id):
        result = self.execute_query("""
                SELECT sessions.date, sessions.time, seats.seat_number
                FROM tickets
                JOIN sessions ON tickets.session_id = sessions.session_id
                JOIN seats ON tickets.place_id = seats.seat_id
                WHERE tickets.user_id = %s        
                """, (user_id,))
        self.close()
        return result

    def get_user_id(self, user_name):
        result = self.execute_query("""
            SELECT users.user_id
            FROM users
            WHERE users.email = %s
            """, (user_name,))
        self.close()
        return result

    def get_user_info(self, user_name):
        result = self.execute_query("""
        SELECT users.first_name, users.second_name, users.age, users.email
        FROM users
        WHERE users.email = %s
        """, (user_name,))
        self.close()
        return result

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None  # функция закрытия соединения
