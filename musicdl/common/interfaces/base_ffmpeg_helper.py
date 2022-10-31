import abc
from pathlib import Path


class BaseFfmpegHelper(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'check_installed') and callable(subclass.check_installed) and 
            hasattr(subclass, 'get_local_path') and callable(subclass.get_local_path) and
            hasattr(subclass, 'download') and callable(subclass.download) or
            NotImplemented
        )


    @abc.abstractmethod
    def check_installed(self, ffmpeg: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_local_path(self) -> Path:
        raise NotImplementedError

    @abc.abstractmethod
    def download(self) -> None:
        raise NotImplementedError