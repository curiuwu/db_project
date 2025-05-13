from app.db import get_db_connetction


def get_sessions(title):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""
        SELECT sessions.session_id, sessions.time, sessions.price FROM sessions
        JOIN films ON sessions.film_id = films.film_id
        WHERE films.title = %s
        """, (title,))
    session = cur.fetchall()
    cur.close()
    connection.close()
    return session
