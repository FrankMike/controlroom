import xml.etree.ElementTree as ET
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from media.models import Movie


class Command(BaseCommand):
    help = "Fetch and update movie data from Plex"

    def handle(self, *args, **options):
        plex_url = settings.PLEX_URL
        plex_token = settings.PLEX_TOKEN

        # Fetch library sections
        sections_url = f"{plex_url}/library/sections?X-Plex-Token={plex_token}"
        response = requests.get(sections_url)
        sections_xml = ET.fromstring(response.content)

        # Find the movie library
        movie_library = next(
            (
                section
                for section in sections_xml.findall(".//Directory")
                if section.get("type") == "movie"
            ),
            None,
        )

        if not movie_library:
            self.stdout.write(self.style.ERROR("No movie library found"))
            return

        library_key = movie_library.get("key")

        # Fetch all movies
        movies_url = (
            f"{plex_url}/library/sections/{library_key}/all?X-Plex-Token={plex_token}"
        )
        response = requests.get(movies_url)
        movies_xml = ET.fromstring(response.content)

        for video in movies_xml.findall(".//Video"):
            rating_key = video.get("ratingKey")

            # Fetch detailed metadata for each movie
            metadata_url = (
                f"{plex_url}/library/metadata/{rating_key}?X-Plex-Token={plex_token}"
            )
            metadata_response = requests.get(metadata_url)
            metadata_xml = ET.fromstring(metadata_response.content)

            movie_data = self.parse_movie_data(metadata_xml)

            # Update or create movie in database
            Movie.objects.update_or_create(
                plex_rating_key=rating_key, defaults=movie_data
            )

        self.stdout.write(self.style.SUCCESS("Successfully updated movie data"))

    def parse_movie_data(self, metadata_xml):
        video = metadata_xml.find(".//Video")
        media = video.find("Media")
        part = media.find("Part")

        audio_streams = [
            {
                "language": stream.get("language"),
                "codec": stream.get("codec").upper(),
                "channels": stream.get("channels"),
            }
            for stream in part.findall("Stream[@streamType='2']")
            if stream.get("languageCode") in ["eng", "ita"]
        ]

        video_resolution = media.get("videoResolution", "").upper()
        video_resolution += "p" if video_resolution == "1080" else ""

        return {
            "title": video.get("title"),
            "year": int(video.get("year")),
            "duration": int(
                int(video.get("duration", 0)) / 60000
            ),  # Convert ms to minutes
            "file_size_gb": round(int(part.get("size", 0)) / (1024 * 1024 * 1024), 2),
            "video_resolution": video_resolution,
            "dimensions": f"{media.get('width')}x{media.get('height')}",
            "video_codec": media.get("videoCodec", "").upper(),
            "audio_streams": audio_streams,
        }
