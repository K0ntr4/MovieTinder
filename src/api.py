import os
import requests
import requests_cache

# Install a cache for API requests with an expiration time of 3600 seconds (1 hour)
requests_cache.install_cache('api_cache', expire_after=3600)


class ApiWrapper:
    """A wrapper class for interacting with The Movie Database (TMDb) API."""

    def __init__(self):
        """Initialize the ApiWrapper with base URL and headers."""
        self.base_url = "https://api.themoviedb.org/3/"
        self.image_base_url = "https://image.tmdb.org/t/p/w500/"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
        }

    def fetch_movies(self, page=1):
        """
        Fetch a list of movies from TMDb.

        Args:
            page (int, optional): The page number to fetch. Defaults to 1.

        Returns:
            list: A list of movie dictionaries if the request is successful, None otherwise.
        """
        url = (
            f"{self.base_url}discover/movie"
            f"?include_adult=false&include_video=false&language=de-DE"
            f"&page={page}&primary_release_date.gte=2010-01-01"
            f"&sort_by=primary_release_date.asc&vote_average.gte=6&vote_count.gte=100"
        )
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return None

        return response.json().get('results', [])

    def fetch_movie_genres(self):
        """
        Fetch a list of movie genres from TMDb.

        Returns:
            list: A list of genre dictionaries if the request is successful, None otherwise.
        """
        url = f"{self.base_url}genre/movie/list?language=de"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return None

        return response.json().get('genres', [])

    def fetch_image(self, path):
        """
        Fetch an image from TMDb.

        Args:
            path (str): The path to the image.

        Returns:
            bytes: The image content if the request is successful, None otherwise.
        """
        url = f"{self.image_base_url}{path}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.content
        return None
