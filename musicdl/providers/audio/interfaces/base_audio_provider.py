import abc
from typing import Optional

from musicdl.downloader.classes.Song import Song


class BaseAudioProvider(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'search') and 
                callable(subclass.search) and 
                hasattr(subclass, 'get_results') and 
                callable(subclass.get_results) and
                hasattr(subclass, 'order_results') and 
                callable(subclass.order_results)  or 
                NotImplemented)

    @abc.abstractmethod
    def search(self, song: Song) -> Optional[str]:
        """
        Search for a song and return best match.

        ### Arguments
        - song: The song to search for.

        ### Returns
        - The url of the best match or None if no match was found.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_results(self, search_term: str, **kwargs):
        """
        Get results from audio provider.

        ### Arguments
        - search_term: The search term to use.
        - kwargs: Additional arguments.

        ### Returns
        - A list of results.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def order_results(self, results, song: Song):
        """
        Order results.

        ### Arguments
        - results: The results to order.
        - song: The song to order for.

        ### Returns
        - The ordered results.
        """

        raise NotImplementedError