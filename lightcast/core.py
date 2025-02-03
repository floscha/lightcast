from __future__ import annotations

import json
import sys
from datetime import date, datetime
from typing import Any, Optional
from urllib.request import urlopen, urlretrieve
from xml.dom import minidom


class Episode:
    """A single podcast episode."""

    def __init__(self, title: str, audio_url: str, publication_date: date, duration: int) -> None:
        """Instantiate a new episode object.
        
        Args:
            title: Title of the episode
            audio_url: URL from which the episode's audio can be downloaded
            publication_date: Date when the episode was published
            duration: Play time in seconds
        """
        self.title = title
        self.audio_url = audio_url
        self.publication_date = publication_date
        self.duration = duration

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def parse_publication_date(date_string: str) -> datetime:
        date_format = "%a, %d %b %Y %H:%M:%S %z"
        return datetime.strptime(date_string, date_format)

    @staticmethod
    def from_xml(xml_item: minidom.Element) -> Episode:
        return Episode(
            xml_item.getElementsByTagName("title")[0].firstChild.nodeValue.strip("\n"),
            xml_item.getElementsByTagName("enclosure")[0].attributes["url"].value.strip("\n"),
            Episode.parse_publication_date(
                xml_item.getElementsByTagName("pubDate")[0].firstChild.nodeValue.strip("\n")
            ),
            int(xml_item.getElementsByTagName("itunes:duration")[0].firstChild.nodeValue.strip("\n")),
        )

    def download(self, file_name: Optional[str] = None) -> None:
        urlretrieve(self.audio_url, file_name or f"{self.title}.mp3")


class Podcast:
    """A podcast consisting of various episodes."""

    def __init__(self, id: int, name: str, feed_url: str) -> None:
        self.id = id
        self.name = name
        self.feed_url = feed_url

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def from_dict(podcast_dict: dict[str, Any]) -> Podcast:
        return Podcast(
            podcast_dict["trackId"],
            podcast_dict["trackName"],
            podcast_dict.get("feedUrl", ""),
        )

    @property
    def episodes(self) -> list[Episode]:
        """Get a full list of episodes for the given podcast."""
        try:
            xml_str = urlopen(self.feed_url).read()
        except IOError:
            print("There was an error retrieving the data. Check your internet connection and try again.")

        xmldoc = minidom.parseString(xml_str)
        episode_items = xmldoc.getElementsByTagName("item")
        episode_objects = [Episode.from_xml(item) for item in episode_items]

        return episode_objects


def search_podcasts(query: str) -> list[Podcast]:
    """Search for podcasts based on the given query string."""
    query = query.replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={query}&entity=podcast"
    try:
        response = urlopen(url)
    except IOError:
        print("There was an error retrieving the data. Check your internet connection and try again.")
        sys.exit(0)

    search_results = json.loads(response.read())["results"]
    podcasts = [Podcast.from_dict(e) for e in search_results]
    return podcasts
