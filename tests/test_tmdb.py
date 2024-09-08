from tmdb_client import get_movies_list, get_poster_url, get_single_movie, get_image_movie, get_single_movie_cast, call_tmdb_api
from unittest.mock import Mock
from main import app
import pytest

def test_get_movies_list(monkeypatch):
   mock_movies_list = ['Movie 1', 'Movie 2']

   requests_mock = Mock()
   response = requests_mock.return_value
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movies_list = get_movies_list(list_name="popular")
   assert movies_list == mock_movies_list



def test_get_poster_url_uses_default_size():
   poster_api_path = "some-poster-path"
   expected_default_size = 'w342'
   poster_url = get_poster_url(poster_api_path=poster_api_path)
   assert poster_url == "https://image.tmdb.org/t/p/w342/some-poster-path"
   assert expected_default_size in poster_url



def test_get_single_movie(monkeypatch):
   mock_movie_data = {
      "id": 1,
      "title": "Matrix",
      "overview": "Haker komputerowy Neo dowiaduje się od tajemniczych rebeliantów, że świat, w którym żyje, jest tylko obrazem przesyłanym do jego mózgu przez roboty.",
      "release_date": "24 marca 1999"
   }

   movie_id = 1

   requests_mock = Mock()
   response = requests_mock.return_value
   response.raise_for_status = Mock()
   response.json.return_value = mock_movie_data
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   
   result = get_single_movie(movie_id)
      
   assert result["id"] == mock_movie_data["id"]
   assert result["title"] == mock_movie_data["title"]


def test_get_movie_images(monkeypatch):
   mock_movie_images = {
      "id": 1,
      "backdrops": [
         {"file_path": "/path1.jpg"},
         {"file_path": "/path2.jpg"}
      ]
   }

   movie_id = 1

   requests_mock = Mock()
   response = requests_mock.return_value
   response.raise_for_status = Mock()
   response.json.return_value = mock_movie_images
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movie_id = 1
   result = get_image_movie(movie_id)

   assert len(result["backdrops"]) == 2
   assert result["backdrops"][0]["file_path"] == mock_movie_images["backdrops"][0]["file_path"]
   assert result["backdrops"][1]["file_path"] == mock_movie_images["backdrops"][1]["file_path"]


def test_get_single_movie_cast(monkeypatch):
   mock_movie_cast = {
    "id": 1,
    "cast": [
        {"name": "Keanu Reeves", "character": "Neo"},
        {"name": "Carrie-Anne Moss", "character": "Trinity"}
    ]
}

   movie_id = 1

   requests_mock = Mock()
   response = requests_mock.return_value
   response.raise_for_status = Mock()
   response.json.return_value = mock_movie_cast
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movie_id = 1
   result = get_single_movie_cast(movie_id)

   assert len(result["cast"]) == 2
   assert result["cast"][0]["name"] == mock_movie_cast["cast"][0]["name"]
   assert result["cast"][1]["name"] == mock_movie_cast["cast"][1]["name"]


def test_movie_url(monkeypatch):
   id = 1
   def mock_get(url, headers):
      assert url == f"https://api.themoviedb.org/3/movie/{id}"
      class MockResponse:
         def json(self):
               return {"id": id, "title": "Matrix"}
         def raise_for_status(self):
            return None
      return MockResponse()

   monkeypatch.setattr("tmdb_client.requests.get", mock_get)
   call_tmdb_api(f"movie/{id}")


@pytest.mark.parametrize("list_type", [
    ("popular"),
    ("top_rated"),
    ("upcoming"),
    ("now_playing")
])


def test_homepage(monkeypatch, list_type):
   api_mock = Mock(return_value={'results': []})
   monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

   with app.test_client() as client:
       response = client.get(f"/?list_type={list_type}")
       assert response.status_code == 200
       api_mock.assert_called_once_with(f"movie/{list_type}")