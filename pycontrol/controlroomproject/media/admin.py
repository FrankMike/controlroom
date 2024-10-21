from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "duration", "file_size_gb")
    ordering = ("title",)
    search_fields = ("title", "year")
