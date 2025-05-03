from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.db import get_db_connetction

user_cabinet_bp = Blueprint('user_cabinet', __name__, template_folder='templates')

@user_cabinet_bp.route('/personal_account')
def personal_account():
    if 'user_id' not in session:
        flash('Для доступа к кабинету необходимо войти в систему')
        return redirect(url_for('auth.login', next=request.url))  # Добавлен параметр next
    
    user = get_user_info(session.get('username'))
    if not user:
        flash('Пользователь не найден')
        return redirect(url_for('auth.login'))

    user_id = get_user_id(session.get('username'))
    if not user_id:
        flash('Ошибка получения данных пользователя')
        return redirect(url_for('auth.login'))

    ticket = get_ticket_info(user_id)
    return render_template('personal_account.html', user=user, ticket=ticket)


def get_user_id(user_name):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""
        SELECT users.user_id
        FROM users
        WHERE users.email = %s
        """, (user_name,))  # Ensure parameter is a tuple
    
    result = cur.fetchone()
    cur.close()
    connection.close()
    return result[0] if result else None  # Extract user_id or return None


def get_user_info(user_name):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""
        SELECT users.first_name, users.second_name, users.age, users.email
        FROM users
        WHERE users.email = %s
        """, (user_name,))
    
    user = cur.fetchone()
    cur.close()
    connection.close()
    return user  # Return user info or None if not found


def get_ticket_info(user_id):
    connection = get_db_connetction()
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
    return ticket  # Return ticket info or an empty list if none found