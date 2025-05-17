from flask import Blueprint, render_template, redirect, url_for
from services import *

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
