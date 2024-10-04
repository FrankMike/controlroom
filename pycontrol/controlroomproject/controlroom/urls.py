from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movies, name="movies"),
    path("tv/", views.tv, name="tv"),
    path("diary/", views.diary, name="diary"),
    path("finance/", views.finance, name="finance"),
    path("finance/add/", views.add_transaction, name="add_transaction"),
    path(
        "finance/edit/<int:transaction_id>/",
        views.edit_transaction,
        name="edit_transaction",
    ),
    path(
        "finance/delete/<int:transaction_id>/",
        views.delete_transaction,
        name="delete_transaction",
    ),
    path("diary/add/", views.add_entry, name="add_entry"),
    path("diary/edit/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    path("diary/delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
]
