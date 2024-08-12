import random

import requests


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZDVkNjUxMTZhMDFkMDNhZmRiNzMyNTA4ZmY4ZGY4MCIsIm5iZiI6MTcyMzQ0MzQ5Ny44MDk5NSwic3ViIjoiNjZiMzIwNDY3MTg1ODczN2YwNTk2ZjAzIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.F3NJ1GmzLNKhoTGOS_XolCj1Dcpf2Fz7MoxI73hcib0"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()

    return response.json()


def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_movies(how_many):
    data = get_popular_movies()
    data_results = data["results"]

    shuffle_list = random.sample(data_results, how_many)
    return shuffle_list
