import xml.etree.ElementTree as ET
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from media.models import TVShow


class Command(BaseCommand):
    help = "Fetch and update TV show data from Plex"

    def handle(self, *args, **options):
        plex_url = settings.PLEX_URL
        plex_token = settings.PLEX_TOKEN

        # Fetch library sections
        sections_url = f"{plex_url}/library/sections?X-Plex-Token={plex_token}"
        response = requests.get(sections_url)
        sections_xml = ET.fromstring(response.content)

        # Find the TV show library
        tv_library = next(
            (
                section
                for section in sections_xml.findall(".//Directory")
                if section.get("type") == "show"
            ),
            None,
        )

        if not tv_library:
            self.stdout.write(self.style.ERROR("No TV show library found"))
            return

        library_key = tv_library.get("key")

        # Fetch all TV shows
        shows_url = (
            f"{plex_url}/library/sections/{library_key}/all?X-Plex-Token={plex_token}"
        )
        response = requests.get(shows_url)
        shows_xml = ET.fromstring(response.content)

        for show in shows_xml.findall(".//Directory"):
            rating_key = show.get("ratingKey")

            # Fetch detailed metadata for each show
            metadata_url = (
                f"{plex_url}/library/metadata/{rating_key}?X-Plex-Token={plex_token}"
            )
            metadata_response = requests.get(metadata_url)
            metadata_xml = ET.fromstring(metadata_response.content)

            show_data = self.parse_show_data(metadata_xml, plex_url, plex_token)

            # Update or create TV show in database
            TVShow.objects.update_or_create(
                plex_rating_key=rating_key, defaults=show_data
            )

        self.stdout.write(self.style.SUCCESS("Successfully updated TV show data"))

    def parse_show_data(self, metadata_xml, plex_url, plex_token):
        show = metadata_xml.find(".//Directory")
        rating_key = show.get("ratingKey")

        seasons_url = f"{plex_url}/library/metadata/{rating_key}/children?X-Plex-Token={plex_token}"
        seasons_response = requests.get(seasons_url)
        seasons_xml = ET.fromstring(seasons_response.content)

        seasons = []
        total_episodes = 0
        total_size_bytes = 0

        for season in seasons_xml.findall(".//Directory"):
            season_number = season.get("index")
            season_title = season.get("title")
            season_key = season.get("ratingKey")

            if season_title == "All episodes":
                continue

            episodes_url = f"{plex_url}/library/metadata/{season_key}/children?X-Plex-Token={plex_token}"
            episodes_response = requests.get(episodes_url)
            episodes_xml = ET.fromstring(episodes_response.content)

            episodes = []
            for episode in episodes_xml.findall(".//Video"):
                episode_title = episode.get("title")
                episode_index = episode.get("index")
                media = episode.find("Media")
                part = media.find("Part")

                file_size_bytes = int(part.get("size", 0))
                total_size_bytes += file_size_bytes
                file_size_gb = round(file_size_bytes / (1024 * 1024 * 1024), 2)

                video_resolution = media.get("videoResolution", "").upper()
                video_resolution += "p" if video_resolution == "1080" else ""

                video_codec = media.get("videoCodec", "").upper()

                episodes.append(
                    {
                        "title": episode_title,
                        "index": episode_index,
                        "fileSizeGB": file_size_gb,
                        "videoResolution": video_resolution,
                        "videoCodec": video_codec,
                    }
                )

                total_episodes += 1

            seasons.append(
                {"number": season_number, "title": season_title, "episodes": episodes}
            )

        total_size_gb = round(total_size_bytes / (1024 * 1024 * 1024), 2)

        return {
            "title": show.get("title"),
            "year": int(show.get("year", 0)),
            "seasons": len(seasons),
            "episodes": total_episodes,
            "file_size_gb": total_size_gb,
            "season_details": seasons,
        }
