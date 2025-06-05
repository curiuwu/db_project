from flask import Blueprint, session, render_template, url_for, redirect, request
from app.db import DBSingleton

select_bp = Blueprint("session_select", __name__)


@select_bp.route("/select_session/<int:session_id>")
def select_session(session_id):
    cur = DBSingleton()
    if "user_id" not in session:
        return redirect(url_for('auth.login', next=request.url))  # Добавлен параметр next

    # Выбор информации о сеансе и фильме
    cur.execute_query(""" select sessions.session_id, sessions.date, sessions.time, 
                    sessions.price, films.title, films.description 
                    from sessions
                    join films on sessions.film_id = films.film_id
                    where sessions.session_id = %s""", (session_id,))
    session_info = cur.fetchone()

    if session_info is None:
        cur.close()
        return 'Такого сеанса нет', 404

    cur.execute_query("""select hall_id from sessions where session_id = %s""", (session_id,))
    hall_id = cur.fetchone()
    # Выбор всех мест
    cur.execute_query(""" select seat_id, row, seat_number
                    from seats
                    where hall_id = %s
                    order by row, seat_number""", (hall_id,))
    seats = cur.fetchall()

    cur.close()
    return render_template("select_session.html",
                           session_info=session_info,
                           seats=seats)
