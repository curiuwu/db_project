from app.db import get_db_connetction



def get_hall(session_id):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""select hall_id from sessions where session_id = %s""", (session_id,))
    hall_id = cur.fetchone()
    cur.close()
    connection.close()
    return hall_id
