from app.db import get_db_connetction

def get_ticket_id(user_id):
    connection = get_db_connetction()
    cur = connection.cursor()

    cur.execute("""
        select ticket_id from tickets
        where user_id = %s
    """, (user_id))

    ticket_ids = cur.fetchall()
    return ticket_ids