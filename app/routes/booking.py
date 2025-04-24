from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for, make_response
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
            SELECT 
                sessions.session_id,
                sessions.date,
                sessions.time,
                sessions.price,
                films.title
            FROM sessions
            JOIN films ON sessions.film_id = films.film_id
            WHERE session_id = %s
    """, (session_id,))
    print('Session query result:', cur.statusmessage)
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

    total_price = len(selected_seats) * session_info[3]  # session_info[3] is the price (int)
    return render_template("confirme_booking.html", 
                            session_info=session_info, 
                            selected_seats=selected_seats,
                            total_price=total_price)

@booking_bp.route("/booking/process", methods=["POST"])
def process_booking():
    connection = None
    cur = None
    
    try:
        # Проверка авторизации
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        print('Processing booking...')
        print('Form data:', dict(request.form))
        
        # Парсим параметры
        session_id = request.form.get('session_id')
        seat_ids = request.form.getlist('seat_ids')
        
        if not session_id or not seat_ids:
            return jsonify({'error': 'Missing parameters'}), 400
        
        try:
            session_id = int(session_id)
            seat_ids = [int(seat_id) for seat_id in seat_ids]
        except ValueError as e:
            print('Error converting IDs:', str(e))
            return jsonify({'error': 'Invalid ID format'}), 400
            
        print('Session ID:', session_id)
        print('Seat IDs:', seat_ids)
        
        # Подключаемся к БД
        connection = get_db_connetction()
        cur = connection.cursor()
        
        # Начинаем транзакцию
        cur.execute("BEGIN")
        
        # Проверяем, не заняты ли места
        cur.execute("""
            SELECT COUNT(*)
            FROM seats
            WHERE seat_id = ANY(%s::int[]) AND session_id = %s AND is_occupied
        """, (seat_ids, session_id))
        
        if cur.fetchone()[0] > 0:
            cur.execute("ROLLBACK")
            return jsonify({'error': 'Некоторые места уже заняты'}), 400
        
        # Создаем бронирование
        booking_time = datetime.now()
        ticket_id = None
        
        for seat_id in seat_ids:
            cur.execute("""
                INSERT INTO tickets (session_id, user_id, seat_id)
                VALUES (%s, %s, %s)
                RETURNING ticket_id
            """, (session_id, session['user_id'], seat_id))
            ticket_id = cur.fetchone()[0]
            
            cur.execute("""
                INSERT INTO ticket_status (ticket_id, status_id, date)
                VALUES (%s, 2, %s)
            """, (ticket_id, booking_time))
        
        # Обновляем статус мест
        cur.execute("""
            update seats
            set is_occupied = true
            where seat_id = any(%s)
        """, (seat_ids,))
        
        # Завершаем транзакцию
        cur.execute("COMMIT")
        
        # Возвращаем URL страницы оплаты
        payment_url = url_for('payment.confirme_payment', booking_id=ticket_id)
        result = {'redirect_url': payment_url}
        print('Success response:', result)
        return jsonify(result)
        
    except Exception as e:
        print('Error during booking:', str(e))
        if cur is not None:
            cur.execute("ROLLBACK")
        return jsonify({'error': str(e)}), 500
        
    finally:
        if cur is not None:
            cur.close()
        if connection is not None:
            connection.close()