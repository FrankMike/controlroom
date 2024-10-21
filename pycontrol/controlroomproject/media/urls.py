from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.movies_view, name="movies"),
    path("get_movies/", views.get_movies, name="get_movies"),
    path("tv/", views.tv_view, name="tv"),
    path("update_movies/", views.update_movies, name="update_movies"),
    path("get_tvshows/", views.get_tvshows, name="get_tvshows"),
    path("update_tvshows/", views.update_tvshows, name="update_tvshows"),
]
