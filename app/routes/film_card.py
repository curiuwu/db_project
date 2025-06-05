from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app, request
from app.db import DBSingleton

film_card_bp = Blueprint('film_card', __name__)


@film_card_bp.route('/film_card/<title>', methods=['GET', 'POST'])
def film_card(title):
    db = DBSingleton()

    try:
        # Получаем информацию о фильме
        film = db.fetchone("""
            SELECT 
                f.film_id, 
                f.title, 
                f.description,
                f.release_date,
                g.genre_name,
                f.poster_link,
                f.rating,
                d.first_name || ' ' || d.second_name AS director
            FROM films f
            JOIN directors d ON f.director_id = d.director_id
            JOIN film_genre fg ON f.film_id = fg.film_id
            JOIN genres g ON fg.genre_id = g.genre_id
            WHERE f.title = %s
            LIMIT 1
        """, (title,))

        if not film:
            flash('Фильм не найден', 'error')
            return redirect(url_for('main.main_page'))

        # Получаем сеансы
        sessions = db.fetchall("""
            SELECT 
                session_id, 
                time, 
                price
            FROM sessions
            WHERE film_id = %s AND date >= CURRENT_DATE
            ORDER BY date, time
        """, (film['film_id'],))

        # Получаем комментарии
        comments = db.fetchall("""
            SELECT 
                u.first_name,
                c.comment_text,
                c.created_at
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.film_id = %s
            ORDER BY c.created_at DESC
        """, (film['film_id'],))

        # Обработка формы комментария
        if request.method == 'POST':
            if 'user_id' not in session:
                flash('Для комментирования необходимо авторизоваться', 'warning')
                return redirect(url_for('auth.login'))

            comment_text = request.form.get('comment_text', '').strip()
            if not comment_text:
                flash('Комментарий не может быть пустым', 'warning')
            else:
                db.execute("""
                    INSERT INTO comments (film_id, user_id, comment_text)
                    VALUES (%s, %s, %s)
                """, (film['film_id'], session['user_id'], comment_text))
                db.connection.commit()
                flash('Комментарий добавлен', 'success')
                return redirect(url_for('film_card.film_card', title=title))

        return render_template(
            'film_card.html',
            film=film,
            sessions=sessions,
            comments=comments
        )

    except Exception as e:
        current_app.logger.error(f"Error in film_card: {e}")
        flash('Произошла ошибка при загрузке страницы', 'error')
        return redirect(url_for('main.main_page'))
