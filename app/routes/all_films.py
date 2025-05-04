from flask import Blueprint, render_template, request
#from app.db import get_db_connetction



all_films_bp = Blueprint('all_films', __name__)

@all_films_bp.route('/all_films')
def all_films():
    #genre = request.args.get('genre')

    #connection = get_db_connetction()
    #cur = connection.cursor()
    #TODO  сделать фильтрв рабочими
    #base_query = """select DISTINCT ON (films.film_id) films.title, films.description, genres.genre_name, films.release_date, films.poster_link FROM film_genre
    #JOIN genres ON film_genre.genre_id = genres.genre_id
    #JOIN films ON film_genre.film_id = films.film_id"""
    #conditions = []
   # params = []

    #if genre:
    #    conditions.append("genre_name = %s")
     #   params.append(genre)


    #if conditions:
    #    query = f"{base_query} WHERE " + " AND ".join(conditions)
    #else:
    #    query = base_query
  
    #cur.execute(query, params)
    #films = cur.fetchall()

   # #TODO исправить отображение режисёров
    #cur.execute("""select directors.first_name, directors.second_name from films
   #             join directors on films.director_id = directors.director_id""")
   # director = cur.fetchall()
   # cur.close()
   # connection.close()
    return render_template('all_films.html')#, films=films, director = director)

