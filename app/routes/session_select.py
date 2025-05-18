from flask import Blueprint, session, render_template, url_for, redirect, request
from app.db import get_db_connetction
from services import get_session_info_by_id, get_hall, get_seats

select_bp = Blueprint("session_select", __name__)

@select_bp.route("/select_session/<int:session_id>")
def select_session(session_id):
    if "user_id" not in session:
        return redirect(url_for('auth.login', next=request.url))  # Добавлен параметр next
    
    connection = get_db_connetction()
    cur = connection.cursor()
    
    #Выбор информации о сеансе и фильме
    session_info = get_session_info_by_id(session_id)

    if session_info is None:
        cur.close()
        connection.close()
        return 'Такого сеанса нет', 404
    
    
    hall_id = get_hall(session_id)
    #Выбор всех мест
    seats = get_seats(hall_id)

    cur.close()
    connection.close()
    return render_template("select_session.html",
                            session_info = session_info,
                            seats = seats)