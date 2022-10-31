from dataclasses import dataclass
from typing import Any, Dict, List

from .song import Song


@dataclass(frozen=True)
class SongList:
    """
    SongList class. Base class for all other song lists subclasses.
    """

    name: str
    url: str
    urls: List[str]
    songs: List[Song]

    @property
    def length(self) -> int:
        """
        Get list length (number of songs).

        ### Returns
        - The list length.
        """

        return len(self.songs)

    @classmethod
    def create_basic_list(cls, url: str):
        """
        Create a basic list with only the required metadata and urls.

        ### Arguments
        - url: The url of the list.

        ### Returns
        - The SongList object.
        """

        metadata = cls.get_metadata(url)
        urls = cls.get_urls(url)

        return cls(**metadata, urls=urls, songs=[])

    @classmethod
    def from_url(cls, url: str) -> "SongList":
        """
        Initialize a SongList object from a URL.

        ### Arguments
        - url: The URL of the list.
        """

        raise NotImplementedError

    @staticmethod
    def get_urls(url: str) -> List[str]:
        """
        Get urls for all songs in url.

        ### Arguments
        - url: The URL of the list.

        ### Returns
        - The list of urls.
        """

        raise NotImplementedError

    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:
        """
        Get metadata for list.

        ### Arguments
        - url: The URL of the list.

        ### Returns
        - The metadata.
        """

        raise NotImplementedError