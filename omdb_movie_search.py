# import libraries
import os
import requests
from dotenv import load_dotenv

# get api key
# load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

def get_movie_details(movie_title=None, movie_id=None):
    """
    Query the OMDb API with a movie title to get the movie's details
    """
    # request url
    url = r"http://www.omdbapi.com/"

    # params
    params = {
        "apikey": API_KEY,
        "t": movie_title,
        "i": movie_id,
        "plot": "full"
    }

    # get request
    response = requests.get(url, params=params)

    return response

def search_for_movie(search_string):
    """
    Search for a movie using a search string (only returns the first page)
    """
    # request url
    url = r"http://www.omdbapi.com/"

    # params
    params = {
        "apikey": API_KEY,
        "s": search_string
    }

    # get request
    response = requests.get(url, params=params)

    return response

def compile_movie_details_response_to_string(response_json):
    """
    Converts an OMDb json response into a string for printing in Discord
    """
    # categorized dict keys
    basic_info_keys = ["Title", "Released", "Runtime"]
    genre_and_plot_keys = ["Genre", "Plot"]
    ratings_and_awards_keys = ["Awards", "imdbRating", "imdbVotes", "Metascore"]
    cast_and_producers_keys = ["Director", "Writer", "Actors", "Production"]
    other_information_keys = ["imdbID", "BoxOffice", "Website", "Country", "Rated"]

    # basic info section
    compiled = "=====**BASIC INFORMATION**=====\n"
    for key in basic_info_keys:
        compiled += f"**{key}**: {response_json.get(key)}\n"

    # genre and plot section
    compiled += "\n=====**GENRE AND PLOT**=====\n"
    for key in genre_and_plot_keys:
        if key == "Plot":
            compiled += f"**{key} (Click to Reveal)**: ||{response_json.get(key)}||\n"
        else:
            compiled += f"**{key}**: {response_json.get(key)}\n"

    # ratings and awards section
    compiled += "\n=====**RATINGS AND AWARDS**=====\n"
    for key in ratings_and_awards_keys:
        compiled += f"**{key}**: {response_json.get(key)}\n"

    # add the other ratings that are stored in a list in the response dict
    if response_json.get("Ratings"):
        for item in response_json.get("Ratings"):
            compiled += f"**{item.get('Source')}**: {item.get('Value')}\n"

    # cast and producers section
    compiled += "\n=====**CAST AND PRODUCERS**=====\n"
    for key in cast_and_producers_keys:
        compiled += f"**{key}**: {response_json.get(key)}\n"

    # other information section
    compiled += "\n=====**OTHER INFORMATION**=====\n"
    for key in other_information_keys:
        compiled += f"**{key}**: {response_json.get(key)}\n"

    return compiled

def compile_movie_search_response_to_string(response_json):
    """
    Converts an OMDb json response for movie search into a string for printing in Discord
    """
    compiled = ""

    for pos, result in enumerate(response_json["Search"]):
        compiled += f"**{pos}**: {result.get('Title')} ({result.get('Year')}, {result.get('Type')}) `IMDb ID: {result.get('imdbID')}`\n"
    
    return compiled