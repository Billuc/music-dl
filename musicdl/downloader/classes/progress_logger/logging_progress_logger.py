from logging import Logger

from kink import inject
from musicdl.downloader.classes import DownloaderSettings
from musicdl.downloader.interfaces import BaseProgressLogger


@inject
class LoggingProgressLogger(BaseProgressLogger):
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger


    def update_settings(self, settings: DownloaderSettings):
        self._logger.setLevel(settings.log_level.value)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warn(self, message: str) -> None:
        self._logger.warn(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def close(self) -> None:
        return None