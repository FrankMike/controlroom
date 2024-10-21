from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging
from media.management.commands.update_plex_movies import Command as update_plex_movies

logger = logging.getLogger(__name__)


@login_required
def tv(request):
    context = {
        "plex_token": settings.PLEX_TOKEN,
        "plex_url": settings.PLEX_URL,
    }
    return render(request, "media/tv.html", context)


@login_required
def movies_view(request):
    return render(request, "media/movies.html")


@login_required
def get_movies(request):
    logger.info("Fetching movies from database")
    movies = Movie.objects.all().order_by("title")

    if movies.count() == 0:
        update_plex_movies().handle()
    total_size = Movie.objects.aggregate(total=Sum("file_size_gb"))["total"] or 0

    movie_list = [
        {
            "title": movie.title,
            "year": movie.year,
            "duration": movie.duration,
            "durationFormatted": f"{movie.duration // 60}h {movie.duration % 60}m",
            "fileSizeGB": movie.file_size_gb,
            "videoResolution": movie.video_resolution,
            "dimensions": movie.dimensions,
            "videoCodec": movie.video_codec,
            "audioStreams": movie.audio_streams,
        }
        for movie in movies
    ]

    response_data = {
        "movies": movie_list,
        "totalMovies": len(movie_list),
        "totalSize": round(total_size / 1024, 2) if total_size else 0,
    }
    logger.info(f"Returning {len(movie_list)} movies")
    return JsonResponse(response_data)
