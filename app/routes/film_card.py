from flask import Blueprint, render_template, redirect, url_for
from app.db import get_db_connetction

film_card_bp = Blueprint('film_card', __name__)

@film_card_bp.route('/film_card/<title>')
def film_card(title):
    film = get_film(title)
    sessions = get_sessions(title)
    directors = get_director(title)
    if film and sessions and directors:
        return render_template('film_card.html', film=film, sessions=sessions, director=directors)
    else:
        return redirect(url_for('main.main_page'))
    
def get_sessions(title):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""
        SELECT sessions.session_id, sessions.time, sessions.price FROM sessions
        JOIN films ON sessions.film_id = films.film_id
        WHERE films.title = %s
        """, (title,))
    session = cur.fetchall()
    cur.close()
    connection.close()
    return session
    
def get_film(title):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""SELECT films.title, films.description, films.release_date, geners.gener_name, films.poster_link FROM film_gener
            JOIN films ON film_gener.film_id = films.film_id
            JOIN geners ON film_gener.gener_id = geners.gener_id
            WHERE films.title = %s""", (title,))
    film = cur.fetchone()
    cur.close()
    connection.close()
    return film

def get_director(title):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""SELECT directors.first_name, directors.second_name FROM directors
            JOIN films ON directors.director_id = films.director_id
            WHERE films.title = %s""", (title,))
    director = cur.fetchone()
    cur.close()
    connection.close()
    return director