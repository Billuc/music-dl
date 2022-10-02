from logging import Logger
from musicdl.downloader.classes import DownloaderSettings
from musicdl.downloader.interfaces import BaseProgressLogger


class LoggingProgressLogger(BaseProgressLogger):
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger


    def update_settings(self, settings: DownloaderSettings):
        # self._logger.setLevel()