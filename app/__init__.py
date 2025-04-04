from flask import Flask
from config import Config
from app.routes.auth import auth_bp
from app.routes.main_page import main_page_bp
from app.routes.user_cabinet import user_cabinet_bp
from app.routes.all_films import all_films_bp
from app.routes.film_card import film_card_bp
from app.routes.session_select import select_bp
from app.routes.booking import booking_bp
from app.routes.payment import payment_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_page_bp)
    app.register_blueprint(user_cabinet_bp)
    app.register_blueprint(all_films_bp)
    app.register_blueprint(film_card_bp)
    app.register_blueprint(select_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(payment_bp)
    return app