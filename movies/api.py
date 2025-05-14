from ninja import Router, Query
from django.shortcuts import render
from movies.models import Actor, Movie
from movies.services import find_by_name_match
from movies.schemas import SearchResults
from movies.utils import limit_search_query

api_router = Router()

@api_router.get('/livesearch', response=SearchResults)
def live_search(request, q: str = Query("")):
    query = limit_search_query(q)
    actors = list(find_by_name_match(model=Actor, name=query)) if query else ()
    movies = list(find_by_name_match(model=Movie, name=query)) if query else ()
    return render(request, 'movies/search_results.html', {
        'actors': actors,
        'movies': movies,
    })
