from django.db import models
from django.db.models import JSONField


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    duration = models.IntegerField()  # in minutes
    file_size_gb = models.FloatField()
    video_resolution = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=50)
    video_codec = models.CharField(max_length=50)
    audio_streams = JSONField()
    plex_rating_key = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
