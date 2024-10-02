from django.contrib import admin
from .models import DiaryEntry


# @admin.register(DiaryEntry)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "content")
    ordering = "date"
    search_fields = ("date", "content")
