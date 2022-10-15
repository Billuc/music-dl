import abc
from pathlib import Path
from typing import List, Optional, Tuple

from musicdl.downloader.classes.Song import Song


class BaseDownloadCoordinator(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'download_song') and 
                callable(subclass.download_song) and 
                hasattr(subclass, 'download_multiple_songs') and 
                callable(subclass.download_multiple_songs)  or 
                NotImplemented)

    @abc.abstractmethod
    def download_song(self, song: Song) -> Tuple[Song, Optional[Path]]:
        """
        Download a single song.

        ### Arguments
        - song: The song to download.

        ### Returns
        - tuple with the song and the path to the downloaded file if successful.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def download_multiple_songs(
        self, songs: List[Song]
    ) -> List[Tuple[Song, Optional[Path]]]:
        """
        Download multiple songs to the temp directory.

        ### Arguments
        - songs: The songs to download.

        ### Returns
        - list of tuples with the song and the path to the downloaded file if successful.
        """

        raise NotImplementedError
