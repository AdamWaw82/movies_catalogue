import random

import requests

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZDVkNjUxMTZhMDFkMDNhZmRiNzMyNTA4ZmY4ZGY4MCIsIm5iZiI6MTcyMzQ0MzQ5Ny44MDk5NSwic3ViIjoiNjZiMzIwNDY3MTg1ODczN2YwNTk2ZjAzIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.F3NJ1GmzLNKhoTGOS_XolCj1Dcpf2Fz7MoxI73hcib0"


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()

    return response.json()


def get_list():
    return [{"key": "now_playing", "value": "Now Playing"}
        , {"key": "popular", "value": "Popular"}
        , {"key": "top_rated", "value": "Top Rated"}
        , {"key": "upcoming", "value": "Upcoming"}]


def get_movies_list(list_name):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_name}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_movies(how_many, list_name='popular'):
    if list_name not in [item.get("key") for item in get_list()]:
        list_name = 'popular'

    data = get_movies_list(list_name)
    data_results = data["results"]

    shuffle_list = random.sample(data_results, how_many)
    return shuffle_list


def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3//movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_image_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_random_image(movie_id):
    data = get_image_movie(movie_id)
    data_results = data["backdrops"]

    random_image = random.sample(data_results, 1)[0]
    return random_image


def search_movie(search_query):
    endpoint = f"https://api.themoviedb.org/3/search/movie?query={search_query}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(endpoint, headers=headers)

    return response.json()


def get_today():
    endpoint = f"https://api.themoviedb.org/3/tv/airing_today"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    print(response.json())
    return response.json()
