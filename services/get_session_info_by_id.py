from app.db import get_db_connetction

def get_session_info_by_id(session_id):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute(""" select sessions.session_id, sessions.date, sessions.time, sessions.price, films.title, films.description 
                    from sessions
                    join films on sessions.film_id = films.film_id
                    where sessions.session_id = %s""", (session_id,))
    session_info = cur.fetchone()
    cur.close()
    connection.close()
    return session_info