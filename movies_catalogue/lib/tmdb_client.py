import requests
import os

apiToken = os.environ.get("TMDB_API_TOKEN", "")

class Movies:
    def __init__(self) -> None:
        pass

    def call_tmdb_api(self, endpoint):
        full_url = f"https://api.themoviedb.org/3/{endpoint}"
        headers = {
            "Authorization": f"Bearer {apiToken}"
        }
        response = requests.get(full_url, headers=headers)
        response.status_code
        return response.json()  

    def get_movies_list(self, list_type):
        return self.call_tmdb_api(f"movie/{list_type}")

    def get_popular_movies(self):
        return self.call_tmdb_api(f"movie/popular")

    def get_poster_url(self, poster_api_path, size):
        base_url = "https://image.tmdb.org/t/p/"
        return f"{base_url}{size}/{poster_api_path}"

    def get_movies(self, how_many=12, list_type='popular'):
        data = films.get_movies_list(list_type)
        return data["results"][:how_many]

    def get_single_movie(self, movie_id):
        return self.call_tmdb_api(f"movie/{movie_id}")

    def get_single_movie_cast(self, movie_id):
        return self.call_tmdb_api(f"movie/{movie_id}/credits")['cast']

    def get_movie_images(self, movie_id):
        return self.call_tmdb_api(f"movie/{movie_id}/images")

    def search(self, search_query):
        endpoint = f"https://api.themoviedb.org/3/search/movie/?query={search_query}"
        headers = {
            "Authorization": f"Bearer {apiToken}"
        }
        response = requests.get(endpoint, headers=headers)
        return response.json()['results']

    def get_airing_today(self):
        endpoint = f"https://api.themoviedb.org/3/tv/airing_today"
        headers = {
            "Authorization": f"Bearer {apiToken}"
        }
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        response = response.json()
        return response['results']

    def people(self, person_id):
        endpoint = f"https://api.themoviedb.org/3/person/{person_id}"
        headers = {
            "Authorization": f"Bearer {apiToken}"
        }
        response = requests.get(endpoint, headers=headers)
        return response.json()

films = Movies()

