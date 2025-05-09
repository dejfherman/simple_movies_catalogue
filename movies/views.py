from movies.models import Movie, Actor
from movies.services import find_by_name_match
from django.shortcuts import render, get_object_or_404

def search_view(request):
    query = request.GET.get("q") or ""
    query = query.strip()[:100]         # make sure maxlength is enforced
    actors = list(find_by_name_match(Actor, query)) if query else ()
    movies = list(find_by_name_match(Movie, query)) if query else ()
    return render(request, "movies/search.html", {
        "query": query,
        "actors": actors,
        "movies": movies,
    })

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    actors = movie.actors.all()
    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "actors": actors,
    })

def actor_detail(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    movies = actor.movies.all()
    return render(request, "movies/actor_detail.html", {
        "actor": actor,
        "movies": movies,
    })