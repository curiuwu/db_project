from flask import Blueprint, session, render_template, redirect, request, url_for
from app.db import get_db_connetction
from datetime import datetime

booking_bp = Blueprint("booking", __name__)

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
    cur.execute("""
            select sessions.session_id, sessions.time, sessions.price, films.title
            from sessions
            join films on sessions.film_id = films.film_id
            where session_id = %s
          """, (session_id,))
    session_info = cur.fetchone()
    
    if not session_info:
        cur.close()
        connection.close()
        return "Сеанс не найден", 404
    
    #Выбираем информацию о всех наших местах местах

    cur.execute("""
            select seat_id, row_number, seat_number
            from seats
            where seat_id = any(%s::int[]) and not is_occupied 
            """, (seats_ids,))
    
    selected_seats = cur.fetchall()
    if len(selected_seats) != len(seats_ids):
        cur.close()
        connection.close()
        return "Некоторые из выбранных мест уже заняты", 400
    
    cur.close()
    connection.close()

    total_price = len(selected_seats) * session_info[2]
    return render_template("confirme_booking.html", 
                            session_info=session_info, 
                            selected_seats=selected_seats,
                            total_price=total_price)

@booking_bp.route("/booking/process", methods=["POST"])
def process_booking():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    session_id = request.form.get('session_id')
    seat_ids = request.form.getlist('seat_ids')
    
    if not session_id or not seat_ids:
        return "Не указаны необходимые параметры", 400
    
    connection = get_db_connetction()
    cur = connection.cursor()

    try:
        cur.execute("BEGIN")

        cur.execute("""
            SELECT COUNT(*)
            FROM seats
            WHERE seat_id = ANY(%s) AND session_id = %s AND is_occupied
        """, (seat_ids, session_id))
        
        if cur.fetchone()[0] > 0:
            cur.execute("ROLLBACK")
            return "Некоторые места уже заняты", 400
        
        booking_time = datetime.now()

        for i in range(len(seat_ids)):
            cur.execute("""
                        INSERT INTO tickets (session_id, user_id, seat_id)
                        VALUES (%s, %s, %s)
                        RETURNING ticket_id
                        """, (session_id, session['user_id'], seat_ids[i]))
            ticket_id = cur.fetchone()[0]
        

            cur.execute("""
                        INSERT INTO ticket_status (ticket_id, status_id, date)
                        values (%s, 2, %s)
                            """, (ticket_id, booking_time))

        cur.execute("""
            update seats
            set is_occupied = true
            where seat_id = any(%s)
        """, (seat_ids,))

        cur.execute("COMMIT")
        
        return redirect(url_for('user_cabinet.personal_account'))
    
    except Exception as e:
        cur.execute("ROLLBACK")
        return f"Произошла ошибка при бронировании: {str(e)}", 500
        
    finally:
        cur.close()
        connection.close()