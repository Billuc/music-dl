import json

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

from .song_list import SongList


@dataclass()
class Song:
    """
    Song class. Contains all the information about a song.
    """

    name: str
    artists: List[str]
    artist: str
    album_name: str
    album_artist: str
    genres: List[str]
    disc_number: int
    disc_count: int
    duration: int
    year: int
    date: str
    track_number: int
    tracks_count: int
    song_id: str
    cover_url: Optional[str]
    explicit: bool
    publisher: str
    url: str
    isrc: Optional[str]
    copyright_text: Optional[str]
    download_url: Optional[str] = None
    song_list: Optional["SongList"] = None
    lyrics: Optional[str] = None

    @classmethod
    def from_data_dump(cls, data: str) -> "Song":
        """
        Create a Song object from a data dump.

        ### Arguments
        - data: The data dump.

        ### Returns
        - The Song object.
        """

        # Create dict from json string
        data_dict = json.loads(data)

        # Return product object
        return cls(**data_dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Song":
        """
        Create a Song object from a dictionary.

        ### Arguments
        - data: The dictionary.

        ### Returns
        - The Song object.
        """

        # Return product object
        return cls(**data)

    @property
    def display_name(self) -> str:
        """
        Returns a display name for the song.

        ### Returns
        - The display name.
        """

        return f"{self.artist} - {self.name}"

    @property
    def json(self) -> Dict[str, Any]:
        """
        Returns a dictionary of the song's data.

        ### Returns
        - The dictionary.
        """

        return asdict(self)

