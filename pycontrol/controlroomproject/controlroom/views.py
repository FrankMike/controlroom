from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

from media.models import Movie, TVShow


# Create your views here.
def home(request):
    context = {}
    if request.user.is_authenticated:
        total_movies = Movie.objects.count()
        total_movies_size = sum(movie.file_size_gb for movie in Movie.objects.all())
        total_tv_shows = TVShow.objects.count()
        total_tv_shows_size = sum(show.file_size_gb for show in TVShow.objects.all())

        context.update(
            {
                "total_movies": total_movies,
                "total_movies_size": f"{total_movies_size / 1024:.2f} TB",
                "total_tv_shows": total_tv_shows,
                "total_tv_shows_size": f"{total_tv_shows_size / 1024:.2f} TB",
            }
        )

    return render(request, "home.html", context)
