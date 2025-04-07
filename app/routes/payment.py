from flask import Blueprint, render_template, redirect, url_for, session
from app.db import get_db_connetction

payment_bp = Blueprint('payment', __name__)

@payment_bp.route("/payment_page/<int:booking_id>")
def confirme_payment(booking_id):
    if "user_id" not in session:
        return redirect(url_for('auth.login'))
    
    connection = get_db_connetction()
    cur = connection.cursor()
    
    try:
        # Проверяем существование бронирования и права доступа
        cur.execute("""
            SELECT t.ticket_id, t.session_id, s.price, f.title
            FROM tickets t
            JOIN sessions s ON t.session_id = s.session_id
            JOIN films f ON s.film_id = f.film_id
            WHERE t.ticket_id = %s AND t.user_id = %s
        """, (booking_id, session['user_id']))
        
        booking_info = cur.fetchone()
        if not booking_info:
            return "Бронирование не найдено или у вас нет прав доступа", 404
        
        return render_template('payment.html', booking_info=booking_info)
        
    finally:
        cur.close()
        connection.close()