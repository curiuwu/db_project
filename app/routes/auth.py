from flask import Blueprint, redirect, render_template, flash, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connetction
from urllib.parse import urlparse, urljoin
auth_bp = Blueprint('auth', __name__)



def is_safe_url(target):
    """Проверяет, что URL безопасен для редиректа."""
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        age = request.form.get('age')
        email = request.form.get('email')
        password = request.form.get('password')

        if not first_name or not second_name or not age or not email or not password:
            flash('Для регистрации необходимо ввести данные во все поля')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        connection = get_db_connetction()
        cur = connection.cursor()

        cur.execute('SELECT user_id FROM users where first_name = %s AND second_name = %s', (first_name, second_name,))

        if cur.fetchone():
             flash('Такой пользователь уже существует')
             cur.close()
             connection.close()
             return redirect(url_for('auth.register'))
        

        cur.execute("""INSERT INTO users (first_name, second_name, age, email, hashed_password)
                     VALUES(%s, %s, %s, %s, %s)""", (first_name, second_name, age, email, hashed_password))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next')  # Получаем параметр next из запроса
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        if not email or not password:
            flash('Введите данные во все поля')
            return redirect(url_for('auth.login', next=next_url))
        
        connection = get_db_connetction()
        cur = connection.cursor()
        cur.execute("SELECT user_id, hashed_password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        connection.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = email

            # Редирект на next_url, если он безопасен
            if next_url and is_safe_url(next_url):
                return redirect(next_url)
            return redirect(url_for('main.main_page'))   
        else:
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('auth.login', next=next_url))
    
    return render_template('login.html', next=next_url)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы')
    return redirect(url_for('auth.login'))