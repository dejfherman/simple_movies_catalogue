# CSFD Top Movies Catalogue

## Description

A simple django app that fetches movie and actor data (names, mostly) from the csfd.cz site list of top-rated movies, limited to 300.

It was created as a coding exercise, so it's not production ready, with only a dev version of settings, no logging, no dedicated docs and no easy deployment strategy. Code itself should be sound though. 

## How to run
1. clone repo to a local folder
2. activate a python venv of choice. Development was done in python 3.13, but the app should do fine in versions 3.10 and higher.
3. install dependencies with `pip install -r requirements.txt`
4. run `python manage.py makemigrations` and `python manage.py migrate` to establish a DB
5. run `python manage.py scrape_csfd_best_movies` to populate the DB with data from the remote website
6. run `python manage.py runserver` to start the app

## Browser interface
As it is, the app will display a search bar GUI at http://127.0.0.1:8000/movies/ where you can input any string (length limited to 100 characters) to be matched against the names of the saved movies and actors. Simple detail views of movies or actors are available at http://127.0.0.1:8000/movies/movies/<movie_pk> and http://127.0.0.1:8000/movies/actors/<actor_pk> respectively, showing also any actors/movies related to the subject of the detail view. 