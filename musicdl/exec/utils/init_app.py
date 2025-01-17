import os
import logging
import sys
from kink import di
from rich.traceback import install

from musicdl.exec.di import init_di
from musicdl.common.consts.config import ERRORS_PATH, LOG_PATH, MUSICDL_PATH, TEMP_PATH
from musicdl.common.consts.logging import CONSOLE_FORMATTER, LoggingLevel, DEFAULT_FORMATTER, DEFAULT_LOGGING_LEVEL


def init_app():
    init_di()
    _check_folders()
    _init_default_logger()
    _set_loggers()
    _init_rich()


def _check_folders():
    if not MUSICDL_PATH.exists():
        print("MusicDL folder not found: creating...")
        os.mkdir(MUSICDL_PATH)
        print("MusicDL folder created")

    if not TEMP_PATH.exists():
        print("Temp folder not found: creating...")
        os.mkdir(TEMP_PATH)
        print("Temp folder created")

    if not ERRORS_PATH.exists():
        print("Errors folder not found: creating...")
        os.mkdir(ERRORS_PATH)
        print("Errors folder created")


def _init_default_logger():
    default_logger: logging.Logger = di[logging.Logger]
    default_logger.setLevel(DEFAULT_LOGGING_LEVEL.value)

    file_handler = logging.FileHandler(LOG_PATH, mode="w", encoding="utf8")
    file_handler.setLevel(LoggingLevel.DEBUG.value)
    file_handler.setFormatter(DEFAULT_FORMATTER)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LoggingLevel.INFO.value)
    console_handler.setFormatter(CONSOLE_FORMATTER)

    default_logger.addHandler(file_handler)
    default_logger.addHandler(console_handler)


def _set_loggers():
    logging.getLogger("requests").setLevel(DEFAULT_LOGGING_LEVEL.value)
    logging.getLogger("urllib3").setLevel(DEFAULT_LOGGING_LEVEL.value)
    logging.getLogger("spotipy").setLevel(DEFAULT_LOGGING_LEVEL.value)
    logging.getLogger("asyncio").setLevel(DEFAULT_LOGGING_LEVEL.value)


def _init_rich():
    # rich: install traceback handler
    install(show_locals=False, extra_lines=1)

