from kink import inject
from rich import Console

from musicdl.common import LoggingLevel

from musicdl.downloader.classes import DownloaderSettings
from musicdl.downloader.consts import RICH_THEME
from musicdl.downloader.interfaces import BaseProgressLogger


@inject
class RichProgressLogger(BaseProgressLogger):
    _console: Console
    _log_level: LoggingLevel

    def __init__(self):
        is_legacy = detect_legacy_windows()
        self._console = Console(
            theme=RICH_THEME, color_system="truecolor" if not is_legacy else None
        )


    def update_settings(self, settings: DownloaderSettings):
        self._log_level = settings.log_level

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warn(self, message: str) -> None:
        self._logger.warn(message)

    def error(self, message: str) -> None:
        self._logger.error(message)