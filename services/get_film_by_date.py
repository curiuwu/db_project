from app.db import get_db_connetction

def get_film_by_date():
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""SELECT films.title, sessions.date, sessions.price
       FROM sessions
       JOIN films ON sessions.film_id = films.film_id
       WHERE sessions.date = CURRENT_DATE  """)

    films = cur.fetchall()
    connection.close()
    return films