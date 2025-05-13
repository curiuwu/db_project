from flask import Blueprint, render_template
from app.db import get_db_connetction



main_page_bp = Blueprint('main', __name__)

@main_page_bp.route('/')
def main_page():
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""SELECT films.title, sessions.date, sessions.price
       FROM sessions
       JOIN films ON sessions.film_id = films.film_id
       WHERE sessions.date = CURRENT_DATE  """)

    films = cur.fetchall()
    return render_template(('main.html'), films=films)