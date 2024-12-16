import requests
from dotenv import load_dotenv
import os

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')


def movie_fetcher_omdb(title):
    """Fetching movie details from OMDb API"""
    api_url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        movie_data = response.json()
        if movie_data.get("Response") == "False":
            print(f"Movie '{title}' not found in OMDb.")
            return None

        movie_details = {
            "title": movie_data.get("Title", ''),
            "release_year": movie_data.get("Year", ''),
            "rating": float(movie_data.get("imdbRating", 0)),
            "poster": movie_data.get("Poster"),
            "director": movie_data.get("Director", ''),
            "link": movie_data.get("imdbID")
        }
        return movie_details

    except requests.exceptions.RequestException as h:
        print(f"Error! {h}")
        return None
