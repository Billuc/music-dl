import abc
from typing import Optional
from spotipy import Spotify


class BaseSpotifyClientProvider(metaclass=abc.ABCMeta):
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
        client_id: str,
        client_secret: str,
        user_auth: bool = False,
        cache_path: Optional[str] = None,
        no_cache: bool = False,
        open_browser: bool = True
    ) -> None:
        raise NotImplementedError


    @abc.abstractmethod
    def get_client(self) -> Spotify:
        raise NotImplementedError
    