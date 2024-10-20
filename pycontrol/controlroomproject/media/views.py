from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def movies(request):
    context = {
        "plex_token": settings.PLEX_TOKEN,
        "plex_url": settings.PLEX_URL,
    }
    return render(request, "media/movies.html", context)


@login_required
def tv(request):
    context = {
        "plex_token": settings.PLEX_TOKEN,
        "plex_url": settings.PLEX_URL,
    }
    return render(request, "media/tv.html", context)
