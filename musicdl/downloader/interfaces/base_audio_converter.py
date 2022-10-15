import abc
from pathlib import Path

from musicdl.downloader.classes import DownloaderSettings


class BaseAudioConverter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'configure') and
            callable(subclass.configure) and
            hasattr(subclass, 'convert') and
            callable(subclass.convert) or
            NotImplemented
        )

    @abc.abstractmethod
    def configure(self, settings: DownloaderSettings):
        raise NotImplementedError

    @abc.abstractmethod
    def convert(self, src_file: Path, output_file: Path):
        raise NotImplementedError