from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from psycopg2.extras import execute_values
from app.db import get_db_connetction
from datetime import datetime
from services import get_session_info_by_id, get_user_id
from datetime import date

booking_bp = Blueprint("booking", __name__)

#TODO Разобраться с кодом и переписать модуль с работающей БД
@booking_bp.route("/booking/confirme")
def confirme_booking():
    if "user_id" not in session:
        return redirect(url_for('auth.login', next=request.url))
    
    session_id = request.args.get("session_id")
    seats_ids = request.args.get("seats")

    if not session_id or not seats_ids:
        return 'Таких параметров нет', 400
    
    seats_ids = seats_ids.split(',')
    seats_ids = [int(seat_id) for seat_id in seats_ids]  # Explicit type casting

    connection = get_db_connetction()
    cur = connection.cursor()

    #Выбираем информацию о сеансе
    session_info = get_session_info_by_id(session_id)
    
    if not session_info:
        cur.close()
        connection.close()
        return "Сеанс не найден", 404
    
    #Выбираем информацию о всех наших местах местах

    cur.execute("""
            select seat_id, row, seat_number
            from seats
            where seat_id = any(%s::int[]) and not is_occupied 
            """, (seats_ids,))
    
    selected_seats = cur.fetchall()
    if len(selected_seats) != len(seats_ids):
        cur.close()
        connection.close()
        return "Некоторые из выбранных мест уже заняты", 400
    
    
    total_price = len(selected_seats) * session_info[3] 
    ticket_data = []
    base_ticket_query = "INSERT INTO tickets (user_id, session_id, place_id) VALUES %s"
    base_status_query = "INSERT INTO ticket_status (status_id, ticket_id, date) VALUES %s"
    user_id = get_user_id(session['username'])

    for i in selected_seats:
        ticket_data.append((user_id, int(session_id), i[0]))
    
    try:
        execute_values(cur, base_ticket_query, ticket_data)
        cur.executemany(
            "UPDATE seats SET is_occupied = %s WHERE seat_id = %s",
            [(True, seat_id) for seat_id in seats_ids]
        )
        connection.commit()
    except Exception as e:
        flash(f"Произошла ошибка {e} при бронировании")
    
    # Получаем только что созданные ticket_id для выбранных мест
    cur.execute(
        "SELECT ticket_id FROM tickets WHERE user_id = %s AND session_id = %s AND place_id = ANY(%s::int[]) ORDER BY ticket_id DESC LIMIT %s",
        (user_id, int(session_id), seats_ids, len(seats_ids))
    )
    ticket_ids = [row[0] for row in cur.fetchall()]
    status_data = []
    for ticket_id in ticket_ids:
        status_data.append((2, ticket_id, date.today()))
    execute_values(cur, base_status_query, status_data)
    connection.commit()

    cur.close()
    connection.close()
    return render_template("confirme_booking.html", 
                            session_info=session_info, 
                            selected_seats=selected_seats,
                            total_price=total_price)