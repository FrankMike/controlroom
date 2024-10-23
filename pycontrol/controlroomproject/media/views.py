from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import logging
from media.management.commands.update_plex_movies import Command as update_plex_movies
from media.management.commands.update_plex_tvshows import Command as update_plex_tvshows
from .models import Movie, TVShow
from rest_framework import generics, permissions
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response

logger = logging.getLogger(__name__)


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


@login_required
@require_POST
def update_movies(request):
    try:
        # Delete all existing movies
        Movie.objects.all().delete()

        # Fetch movies again
        update_plex_movies().handle()

        # Get the updated movie data
        movies = Movie.objects.all().order_by("title")
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

        return JsonResponse(response_data)
    except Exception as e:
        logger.error(f"Error updating movies: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
def tv_view(request):
    return render(request, "media/tv.html")


@login_required
def get_tvshows(request):
    logger.info("Fetching TV shows from database")
    tvshows = TVShow.objects.all().order_by("title")

    if tvshows.count() == 0:
        update_plex_tvshows().handle()
        tvshows = TVShow.objects.all().order_by("title")

    total_size = TVShow.objects.aggregate(total=Sum("file_size_gb"))["total"] or 0

    tvshow_list = [
        {
            "title": show.title,
            "year": show.year,
            "seasons": show.seasons,
            "episodes": show.episodes,
            "fileSizeGB": show.file_size_gb,
            "seasonDetails": show.season_details,
        }
        for show in tvshows
    ]

    response_data = {
        "tvshows": tvshow_list,
        "totalShows": len(tvshow_list),
        "totalSize": round(total_size / 1024, 2) if total_size else 0,
    }
    logger.info(f"Returning {len(tvshow_list)} TV shows")
    return JsonResponse(response_data)


@login_required
@require_POST
def update_tvshows(request):
    try:
        # Delete all existing TV shows
        TVShow.objects.all().delete()

        # Fetch TV shows again
        update_plex_tvshows().handle()

        # Get the updated TV show data
        return get_tvshows(request)
    except Exception as e:
        logger.error(f"Error updating TV shows: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class TVShowSerializer(ModelSerializer):
    class Meta:
        model = TVShow
        fields = "__all__"


class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"movies": serializer.data})


class TVShowListAPIView(generics.ListAPIView):
    queryset = TVShow.objects.all().order_by("title")
    serializer_class = TVShowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"tvshows": serializer.data})
