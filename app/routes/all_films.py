from flask import Blueprint, render_template, request
from app.db import DBSingleton

all_films_bp = Blueprint('all_films', __name__)


@all_films_bp.route('/all_films')
def all_films():
    genre = request.args.get('genre')
    date = request.args.get('date')
    db = DBSingleton()

    # Базовый запрос для получения фильмов
    base_query = """SELECT DISTINCT
                    f.film_id, 
                    f.title, 
                    f.description,
                    d.first_name || ' ' || d.second_name AS director,
                    f.poster_link
                FROM films f
                JOIN directors d ON f.director_id = d.director_id
                LEFT JOIN film_genre fg ON f.film_id = fg.film_id
                LEFT JOIN genres g ON fg.genre_id = g.genre_id"""

    conditions = []
    params = []

    # Фильтр по жанру
    if genre:
        conditions.append("g.genre_id = %s")
        params.append(genre)

    # Фильтр по дате
    if date:
        conditions.append("EXISTS (SELECT 1 FROM sessions s WHERE s.film_id = f.film_id AND s.date = %s)")
        params.append(date)

    # Формируем окончательный запрос
    if conditions:
        query = f"{base_query} WHERE {' AND '.join(conditions)}"
    else:
        query = base_query

    # Выполняем запрос
    films = db.fetchall(query, tuple(params) if params else None)

    # Получаем жанры для фильтра
    genres = db.fetchall("SELECT genre_id, genre_name FROM genres")

    return render_template('all_films.html', films=films, genres=genres)
