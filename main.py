from flask import Flask, render_template, request, redirect, url_for, flash

import tmdb_client
from tmdb_client import get_movies, get_single_movie, get_single_movie_cast, get_random_image, \
    get_list, search_movie, get_today

app = Flask(__name__)
app.secret_key = b'my-secret'
FAVORITES = []


@app.route('/')
def homepage():
    lists = get_list()
    selected_list = request.args.get('list_type', 'popular')
    movies = get_movies(how_many=8, list_name=selected_list)
    return render_template("homepage.html", movie_lists=lists, movies=movies, current_list=selected_list)


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = get_single_movie(movie_id)
    d_credits = get_single_movie_cast(movie_id)
    image = get_random_image(movie_id)
    print(image)
    return render_template("movie_details.html", movie_image=image, movie=details, credits=d_credits["cast"])


@app.route("/search")
def search():
    search_query = request.args.get("q", "")
    movies = search_movie(search_query)['results']
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route("/today")
def today():
    import datetime
    movies = get_today()['results']
    curr_date = datetime.date.today()
    return render_template("today.html", movies=movies, today=curr_date)


@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id:
        FAVORITES.append(movie_id)
    flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))


@app.route("/favorites", methods=['GET'])
def show_favorites():
    movies = []
    for movie_id in FAVORITES:
        movies.append(get_single_movie(movie_id))

    return render_template("favorites.html", movies=movies)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)

    return {"tmdb_image_url": tmdb_image_url}


if __name__ == '__main__':
    app.run(debug=True)
