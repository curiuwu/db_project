from flask import Blueprint, render_template
from app.db import DBSingleton

main_page_bp = Blueprint('main', __name__)


@main_page_bp.route('/')
def main_page():
    db = DBSingleton()

    try:
        # Получаем фильмы с сеансами на сегодня
        films = db.fetchall("""
            SELECT 
                f.title, 
                f.description,
                MIN(s.price) as min_price,
                f.poster_link
            FROM films f
            JOIN sessions s ON f.film_id = s.film_id
            WHERE s.date = CURRENT_DATE
            GROUP BY f.title, f.description, f.poster_link
            ORDER BY f.title
            LIMIT 6
        """)

        return render_template('main.html', films=films)

    except Exception as e:
        # В реальном приложении здесь должно быть логирование ошибки
        return render_template('main.html', films=[])
