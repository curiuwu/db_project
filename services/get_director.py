from app.db import get_db_connetction


def get_director(title):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""SELECT directors.first_name, directors.second_name FROM directors
            JOIN films ON directors.director_id = films.director_id
            WHERE films.title = %s""", (title,))
    director = cur.fetchone()
    cur.close()
    connection.close()
    return director
