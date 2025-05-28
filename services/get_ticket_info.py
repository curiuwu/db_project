
def get_ticket_info(user_id):
    cur = connection.cursor()
    cur.execute("""
        SELECT sessions.date, sessions.time, seats.seat_number
        FROM tickets
        JOIN sessions ON tickets.session_id = sessions.session_id
        JOIN seats ON tickets.place_id = seats.seat_id
        WHERE tickets.user_id = %s        
        """, (user_id,))  # Ensure user_id is passed as a tuple

    ticket = cur.fetchall()
    cur.close()
    connection.close()
    return 0
