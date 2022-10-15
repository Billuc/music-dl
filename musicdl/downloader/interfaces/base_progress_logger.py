import abc

from musicdl.downloader.classes import DownloaderSettings


class BaseProgressLogger(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'update_settings') and 
            callable(subclass.update_settings) and
            hasattr(subclass, 'debug') and 
            callable(subclass.debug) and
            hasattr(subclass, 'info') and 
            callable(subclass.info) and
            hasattr(subclass, 'warn') and 
            callable(subclass.warn) and
            hasattr(subclass, 'error') and 
            callable(subclass.error) and
            hasattr(subclass, 'close') and 
            callable(subclass.close) and
            NotImplemented
        )

    @abc.abstractmethod    
    def update_settings(self, settings: DownloaderSettings) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def debug(self, message: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def info(self, message: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def warn(self, message: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def error(self, message: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError
