from flask import Blueprint, render_template, request
from app.db import get_db_connetction



all_films_bp = Blueprint('all_films', __name__)

@all_films_bp.route('/all_films')
def all_films():
    genre = request.args.get('genre')
    year = request.args.get('year')

    connection = get_db_connetction()
    cur = connection.cursor()

    base_query = """select DISTINCT ON (films.film_id) films.title, films.description, geners.gener_name, films.release_date, films.poster_link FROM film_gener 
    JOIN geners ON film_gener.gener_id = geners.gener_id
    JOIN films ON film_gener.film_id = films.film_id"""
    conditions = []
    params = []

    if genre:
        conditions.append("gener_name = %s")
        params.append(genre)

#     if year:
#         conditions.append("release_date = %s")
#         params.append(year)

    if conditions:
        query = f"{base_query} WHERE " + " AND ".join(conditions)
    else:
        query = base_query
  
    cur.execute(query, params)
    films = cur.fetchall()


    cur.execute("""select directors.first_name, directors.second_name from films
                join directors on films.director_id = directors.director_id""")
    director = cur.fetchone()
    cur.close()
    connection.close()
    return render_template('all_films.html', films=films, director = director)

