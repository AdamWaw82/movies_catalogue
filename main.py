import json

from flask import Flask, render_template, request

from movies_catalogue import tmdb_client
from movies_catalogue.tmdb_client import get_movies, get_single_movie, get_single_movie_cast, get_random_image, get_list

app = Flask(__name__)


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


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)

    return {"tmdb_image_url": tmdb_image_url}


if __name__ == '__main__':
    app.run(debug=True)
