from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "description", "amount", "transaction_type", "date")
    ordering = ("date",)
    search_fields = ("description", "amount")
