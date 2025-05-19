from flask import Blueprint, render_template
from services import get_film_by_date




main_page_bp = Blueprint('main', __name__)

@main_page_bp.route('/')
def main_page():
    films = get_film_by_date()
    return render_template(('main.html'), films=films)