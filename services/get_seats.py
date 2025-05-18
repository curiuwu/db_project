from app.db import get_db_connetction

def get_seats(hall_id):
    connection = get_db_connetction()
    cur = connection.cursor()

    cur.execute(""" select seat_id, row, seat_number
                    from seats
                    where hall_id = %s
                    order by row, seat_number""", (hall_id,))
    seats = cur.fetchall()

    cur.close()
    connection.close()
    return seats 