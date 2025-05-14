# CSFD Top Movies Catalogue

## Description

A simple django app that fetches movie and actor data (names, mostly) from the csfd.cz site list of top-rated movies, limited to 300.

It was created as a coding exercise, so it's not production ready, with only a dev version of settings, no logging, no dedicated docs and no easy deployment strategy. Code itself should be sound though. 

## How to run
1. clone repo to a local folder
2. activate a python venv of choice. Use python 3.10 or higher.
3. install dependencies with `pip install -r requirements.txt`
4. run `python manage.py makemigrations` and `python manage.py migrate` to establish a DB
5. run `python manage.py scrape_csfd_best_movies` to populate the DB with data from the remote website
6. run `python manage.py runserver` to start the app

## Interface
 - `{BASE_URL}/movies/search` - search view where you can input a string and get a list of matching actor and movies names
 - `{BASE_URL}/movies/movies/<movie_pk>` - movie detail with name and a list of starring actors
 - `{BASE_URL}/movies/actors/<actor_pk>` - actor detail with name and a list of movies they starred in

 - `{BASE_URL}/api/movies/livesearch` GET endpoint facilitating live search with same behaviour as the synchronous search view 

## Behaviour
Searching is case and accents insensitive and always returns all matches, since the searched population is limited to 300 movies.

Live search capability has also been added, so the results will be displayed continuously as you type. Fetching results via the "Search" button still works, but is now mostly used as fallback for when Javascript isn't available on the client side.
 