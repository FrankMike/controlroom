from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.movies_view, name="movies"),
    path("get_movies/", views.get_movies, name="get_movies"),
    path("tv", views.tv, name="tv"),
]
