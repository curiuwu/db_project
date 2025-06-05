from typing import Optional

import psycopg2
from psycopg2.extras import DictCursor
from flask import current_app


class DBSingleton:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connect()
        return cls._instance

    @classmethod
    def _connect(cls):
        """Устанавливает соединение с базой данных"""
        cls._connection = psycopg2.connect(
            dbname=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            cursor_factory=DictCursor
        )

    @property
    def connection(self):
        """Возвращает активное соединение"""
        if self._connection is None or self._connection.closed:
            self._connect()
        return self._connection

    def execute(self, query: str, params=None):
        """Выполняет SQL-запрос и возвращает курсор"""
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return cursor

    def fetchall(self, query: str, params=None):
        """Выполняет запрос и возвращает все результаты"""
        cursor = self.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def fetchone(self, query: str, params=None):
        """Выполняет запрос и возвращает одну строку"""
        cursor = self.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def close(self):
        """Закрывает соединение с базой данных"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None

    def get_film(self, title: str) -> Optional[dict]:
        cursor = self.execute(
            """SELECT films.film_id, films.title, films.description, 
                      films.release_date, genres.genre_name,
                      films.poster_link, films.rating
               FROM film_genre
               JOIN films ON film_genre.film_id = films.film_id
               JOIN genres ON film_genre.genre_id = genres.genre_id
               WHERE films.title = %s
               LIMIT 1""",
            (title,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result
        # это и ниже - все функции с сервисов в прошлом, только реализованные как методы класса

    def get_director(self, title):

        cursor = self.execute(
            """SELECT directors.first_name, directors.second_name FROM directors
            JOIN films ON directors.director_id = films.director_id
            WHERE films.title = %s""",
            (title,),

        )
        cursor.close()
        return cursor

    def get_comments(self, film_id: int):
        cursor = self.execute("""
            SELECT u.first_name, c.comment_text, c.created_at
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.film_id = %s
            ORDER BY c.created_at DESC""",
                              (film_id,)
                              )
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_genres(self):
        cursor = self.execute(
            """select *
                            from genres
                            """
        )
        cursor.close()
        return cursor

    def get_sessions(self, title):
        cursor = self.execute("""
            SELECT sessions.session_id, sessions.time, sessions.price FROM sessions
            JOIN films ON sessions.film_id = films.film_id
            WHERE films.title = %s
            """, (title,))
        cursor.close()
        return cursor

    def get_ticket_info(self, user_id):
        cursor = self.execute("""
                SELECT sessions.date, sessions.time, seats.seat_number
                FROM tickets
                JOIN sessions ON tickets.session_id = sessions.session_id
                JOIN seats ON tickets.place_id = seats.seat_id
                WHERE tickets.user_id = %s        
                """, (user_id,))
        cursor.close()
        return cursor

    def get_user_id(self, user_name):
        cursor = self.execute("""
            SELECT users.user_id
            FROM users
            WHERE users.email = %s
            """, (user_name,))
        cursor.close()
        return cursor

    def get_user_info(self, user_name):
        cursor = self.execute("""
        SELECT users.first_name, users.second_name, users.age, users.email
        FROM users
        WHERE users.email = %s
        """, (user_name,))
        cursor.close()
        return cursor
