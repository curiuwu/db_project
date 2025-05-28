from app.db import DBSingleton
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

film_card_bp = Blueprint('film_card', __name__)


@film_card_bp.route('/film_card/<title>', methods=['GET', 'POST'])
def film_card(title):
    db = DBSingleton()

    film = db.get_film(title)
    if not film:
        flash('Фильм не найден', 'error')
        return redirect(url_for('main.main_page'))

        # Обработка POST-запроса
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Для комментирования необходимо авторизоваться', 'warning')
            return redirect(url_for('auth.login'))

        comment_text = request.form.get('comment_text', '').strip()
        if not comment_text:
            flash('Комментарий не может быть пустым', 'warning')
        elif db.save_comment(film['film_id'], session['user_id'], comment_text):
            flash('Ваш комментарий успешно сохранён!', 'success')
        else:
            flash('Ошибка при сохранении комментария', 'error')

    comments = db.get_comments(film['film_id'])

    return render_template(
        'film_card.html',
        film=film,
        comments=comments,

    )
