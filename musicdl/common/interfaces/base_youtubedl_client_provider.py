import abc
from typing import Optional
from yt_dlp import YoutubeDL


class BaseYoutubeDLClientProvider(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'init') and callable(subclass.init) and 
            hasattr(subclass, 'get_client') and callable(subclass.get_client) and
            NotImplemented
        )


    @abc.abstractmethod
    def init(
        self,
        output_format: str = "mp3",
        cookie_file: Optional[str] = None,
    ) -> None:
        raise NotImplementedError


    @abc.abstractmethod
    def get_client(self) -> YoutubeDL:
        raise NotImplementedError
    