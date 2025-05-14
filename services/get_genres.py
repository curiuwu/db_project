from app.db import get_db_connetction


def get_genres():
    conn = get_db_connetction()
    cur = conn.cursor()
    cur.execute("""select *
                from genres
                """)
    genres = cur.fetchall()
    return genres
