from django.urls import path
from . import views

urlpatterns = [
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
]
