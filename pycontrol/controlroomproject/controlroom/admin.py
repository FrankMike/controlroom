from django.contrib import admin
from .models import DiaryEntry, Transaction


@admin.register(DiaryEntry)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "content")
    ordering = ("date",)
    search_fields = ("date", "content")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "description", "amount", "transaction_type", "date")
    ordering = ("date",)
    search_fields = ("description", "amount")
