from app.db import get_db_connetction


def get_ticket_info(user_id):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""
        SELECT sessions.date, sessions.time, seats.seat_number, films.title
        FROM tickets
        INNER JOIN sessions ON tickets.session_id = sessions.session_id
        INNER JOIN films on sessions.film_id = films.film_id
        JOIN seats ON tickets.place_id = seats.seat_id
        WHERE tickets.user_id = %s        
        """, (user_id,))  # Ensure user_id is passed as a tuple

    ticket = cur.fetchall()
    cur.close()
    connection.close()
    return ticket  # Return ticket info or an empty list if none found
