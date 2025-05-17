from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from services import *

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
