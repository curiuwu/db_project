from app.db import get_db_connetction


def get_film(title):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""SELECT films.title, films.description, films.release_date, genres.genre_name, films.poster_link FROM film_genre
            JOIN films ON film_genre.film_id = films.film_id
            JOIN genres ON film_genre.genre_id = genres.genre_id
            WHERE films.title = %s""", (title,))
    film = cur.fetchone()
    cur.close()
    connection.close()
    return film
