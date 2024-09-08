import random

import requests

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZDVkNjUxMTZhMDFkMDNhZmRiNzMyNTA4ZmY4ZGY4MCIsIm5iZiI6MTcyMzQ0MzQ5Ny44MDk5NSwic3ViIjoiNjZiMzIwNDY3MTg1ODczN2YwNTk2ZjAzIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.F3NJ1GmzLNKhoTGOS_XolCj1Dcpf2Fz7MoxI73hcib0"


def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {API_TOKEN}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   return response.json()


def get_popular_movies():
    return call_tmdb_api(f"movie/popular")



def get_list():
    return [{"key": "now_playing", "value": "Now Playing"}
        , {"key": "popular", "value": "Popular"}
        , {"key": "top_rated", "value": "Top Rated"}
        , {"key": "upcoming", "value": "Upcoming"}]


def get_movies_list(list_name):
    return call_tmdb_api(f"movie/{list_name}")

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_movies(how_many, list_name='popular'):
    if list_name not in [item.get("key") for item in get_list()]:
        list_name = 'popular'

    data = get_movies_list(list_name)
    data_results = data["results"]

    return data_results


def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")



def get_single_movie_cast(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/credits")


def get_image_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/images")


def get_random_image(movie_id):
    data = get_image_movie(movie_id)
    data_results = data["backdrops"]

    random_image = random.sample(data_results, 1)[0]
    return random_image


def search_movie(search_query):
    return call_tmdb_api(f"search/movie?query={search_query}")


def get_today():
    return call_tmdb_api(f"tv/airing_today")
