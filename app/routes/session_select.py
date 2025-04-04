from flask import Blueprint, session, render_template, url_for, redirect, request
from app.db import get_db_connetction

select_bp = Blueprint("session_select", __name__)

@select_bp.route("/select_session/<int:session_id>")
def select_session(session_id):
    if "user_id" not in session:
        return redirect(url_for('auth.login', next= request.url))
    
    connection = get_db_connetction()
    cur = connection.cursor()
    
    #Выбор информации о сеансе и фильме
    cur.execute(""" select sessions.session_id, sessions.date, sessions.time, sessions.price, films.title, films.description 
                    from sessions
                    join films on sessions.film_id = films.film_id
                    where sessions.session_id = %s""", (session_id,))
    session_info = cur.fetchone()

    if session_info is None:
        cur.close()
        connection.close()
        return 'Такого сеанса нет', 404
    
    cur.execute("""select hall_id from sessions where session_id = %s""", (session_id,))
    hall_id = cur.fetchone()
    #Выбор всех мест
    cur.execute(""" select seat_id, row_number, seat_number
                    from seats
                    where hall_id = %s
                    order by row_number, seat_number""", (hall_id,))
    seats = cur.fetchall()

    cur.close()
    connection.close()
    return render_template("select_session.html",
                            session_info = session_info,
                            seats = seats)