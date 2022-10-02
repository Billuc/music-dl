import abc
from pathlib import Path
from typing import List, Optional, Tuple

from musicdl.downloader.classes.Song import Song


class BaseProgressLogger(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'close') and 
                callable(subclass.close) and
                NotImplemented)

    @abc.abstractmethod
    def init(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError
