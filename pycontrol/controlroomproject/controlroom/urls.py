from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movies, name="movies"),
    path("tv/", views.tv, name="tv"),
    path("diary/", views.diary, name="diary"),
    path("finance/", views.finance, name="finance"),
    path("diary/add/", views.add_entry, name="add_entry"),
    path("diary/edit/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    path("diary/delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
]
