from django.urls import path
from . import views

urlpatterns = [
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/change_password/", views.change_password, name="change_password"),
    path("profile/delete_account/", views.delete_account, name="delete_account"),
]
