from flask import Blueprint, render_template, session, redirect, url_for, flash, request

user_cabinet_bp = Blueprint('user_cabinet', __name__, template_folder='templates')

@user_cabinet_bp.route('/personal_account')
def personal_account():
    if 'user_id' not in session:
        flash('Для доступа к кабинету необходимо войти в систему')
        return redirect(url_for('auth.login', next=request.url))  # Добавлен параметр next
    return render_template('personal_account.html', username=session.get('username'))


