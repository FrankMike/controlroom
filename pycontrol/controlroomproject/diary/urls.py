from django.urls import path
from . import views

urlpatterns = [
    path("diary/", views.diary, name="diary"),
    path("diary/add/", views.add_entry, name="add_entry"),
    path("diary/edit/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    path("diary/delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
]
