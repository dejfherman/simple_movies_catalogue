from django.urls import path
from movies import views

urlpatterns = [
    path("search/", views.search_view, name="search"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("actors/<int:pk>/", views.actor_detail, name="actor_detail"),
]
