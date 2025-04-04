import psycopg2
from flask import current_app

def get_db_connetction():
    connection = psycopg2.connect(
        dbname = current_app.config['DB_NAME'],
        user = current_app.config['DB_USER'],
        password = current_app.config['DB_PASSWORD'],
        host = current_app.config['DB_HOST'],
        port = current_app.config['DB_PORT']   
    )
    
    return connection