from flask import Blueprint, render_template, request
from app.db import get_db_connetction

all_films_bp = Blueprint('all_films', __name__)

@all_films_bp.route('/all_films')
def all_films():
    genre = request.args.get('genre')  # Get the genre filter from the query parameters

    connection = get_db_connetction()
    cur = connection.cursor()

    # Base query to fetch films
    base_query = """SELECT DISTINCT ON (films.film_id) 
                        films.film_id, 
                        films.title, 
                        films.description, 
                        genres.genre_name, 
                        films.release_date, 
                        films.poster_link 
                    FROM film_genre
                    JOIN genres ON film_genre.genre_id = genres.genre_id
                    JOIN films ON film_genre.film_id = films.film_id"""
    conditions = []
    params = []

    # Add filter for genre if provided
    if genre:
        conditions.append("genres.genre_name = %s")
        params.append(genre)

    # Combine base query with conditions
    if conditions:
        query = f"{base_query} WHERE " + " AND ".join(conditions)
    else:
        query = base_query

    # Execute the query
    cur.execute(query, tuple(params))
    films = cur.fetchall()

    # Fetch directors for all films
    cur.execute("""SELECT films.film_id, directors.first_name, directors.second_name
                   FROM films
                   JOIN directors ON films.director_id = directors.director_id""")
    director = cur.fetchall()

    # Map directors to their respective films
    director_map = {
        film_id: f"{first_name} {second_name}"
        for film_id, first_name, second_name in director
    }

    # Prepare the films data for rendering
    films_data = []
    for film in films:
        film_id, title, description, genre, release_date, poster_link = film
        director = director_map.get(film_id, "Неизвестно")
        films_data.append({
            "title": title,
            "description": description,
            "genre": genre,
            "release_date": release_date,
            "poster": poster_link,
            "director": director
        })

    cur.close()
    connection.close()

    # Render the template with the filtered films
    return render_template('all_films.html', films=films_data)

