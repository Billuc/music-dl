import abc
from pathlib import Path
from typing import List, Optional, Tuple

from musicdl.downloader.data.song import Song
from musicdl.downloader.data.downloader_settings import DownloaderSettings


class BaseDownloadCoordinator(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'download_song') and 
                callable(subclass.download_song) and 
                hasattr(subclass, 'download_multiple_songs') and 
                callable(subclass.download_multiple_songs)  or 
                NotImplemented)


    @abc.abstractmethod
    def download(
        self, options: DownloaderSettings
    ) -> List[Tuple[Song, Optional[Path]]]:
        raise NotImplementedError
