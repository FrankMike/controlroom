from django.urls import path
from . import views

urlpatterns = [
    path("media/movies/", views.movies, name="movies"),
    path("media/tv/", views.tv, name="tv"),
]
