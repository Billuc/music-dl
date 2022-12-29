import abc

from typing import Optional, List

from musicdl.common.classes import Song

class BaseFormatHelper(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'create_search_query') and 
                callable(subclass.create_search_query) and 
                hasattr(subclass, 'create_song_title') and 
                callable(subclass.create_song_title)  or 
                NotImplemented)

    @abc.abstractmethod
    def create_search_query(
        self,
        song: Song,
        template: str,
        santitize: bool,
        file_extension: Optional[str] = None,
        short: bool = False,
    ) -> str:
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def create_song_title(self, song_name: str, song_artists: List[str]) -> str:
        raise NotImplementedError