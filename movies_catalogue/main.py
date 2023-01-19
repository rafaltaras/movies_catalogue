from flask import Flask, render_template, request, url_for, redirect, flash
from movies_catalogue.lib.tmdb_client import films
import random
import datetime

app = Flask(__name__)

FAVORITES = set()

TYPE_OF_FILM = { 
    'now_playing':'Now Playing', 
    'popular':'Popular',
    'top_rated' : 'Top rated',
    'upcoming': 'Upcoming'
    }

app.secret_key = b'qwertqwert'

@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', 'popular')
    if selected_list not in TYPE_OF_FILM:
        selected_list = "top_rated"
    movies = films.get_movies(how_many=12, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, type_of_film = TYPE_OF_FILM)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return films.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = films.get_single_movie(movie_id)
    cast = films.get_single_movie_cast(movie_id)
    movie_images = films.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details, cast = cast, selected_backdrop = selected_backdrop )

@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = films.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)

@app.route('/today')
def today():
    movies = films.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)

@app.route('/actors_details/<person_id>')
def actors_details(person_id):
    person_details = films.people(person_id)
    return render_template("actors_details.html", person_details = person_details)

@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))

@app.route("/favorites")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = films.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("homepage.html", movies=movies, type_of_film = TYPE_OF_FILM)

if __name__ == "__main__":
    app.run(debug=True)

