from movies_catalogue.lib.tmdb_client import films
import pytest, json
from unittest.mock import Mock
from movies_catalogue.main import app


# Przesłanianie kodu za pomocą Mock i Monkeypatch
def test_get_call_tmdb_api(monkeypatch):
   # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
   mock_movies_list = ['Movie 1', 'Movie 2']
   requests_mock = Mock()
   # Wynik wywołania zapytania do API
   response = requests_mock.return_value
   # Przysłaniamy wynik wywołania metody .json()
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("requests.get", requests_mock)
   movies_list = films.call_tmdb_api(endpoint="315162")
   assert movies_list == mock_movies_list


def test_get_single_movie(): 
   film = films.get_single_movie(movie_id = 315162)
   assert film["adult"]==False

def test_get_movie_images(): 
   image = films.get_movie_images(movie_id = 315162)
   assert image is not None

def test_get_single_movie_cast(): 
   movie_id = "315162"
   full_url = "https://api.themoviedb.org/3/movie/315162/credits"
   assert movie_id in full_url

def test_get_movies_list_type_popular():
   movies_list = films.get_movies_list(list_type="popular")
   assert movies_list is not None

@pytest.mark.parametrize("category, status", (
  ("popular", 200),
  ("top_rated", 200),
  ("upcoming", 200),
  ("now_playing", 200)
))

def test_homepage(monkeypatch, category, status):
    api_mock = Mock(return_value={"results": []})
    monkeypatch.setattr("movies_catalogue.lib.tmdb_client.films.get_movies", api_mock)

    with app.test_client() as client:
        response = client.get(f"/?list_type={category}")
        assert response.status_code == status
        api_mock.assert_called_once_with(how_many=12,list_type=category)
      