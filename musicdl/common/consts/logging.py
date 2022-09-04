import logging
from typing import Dict


# https://github.com/python/cpython/blob/3.10/Lib/logging/__init__.py
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

LEVEL_TO_NAME: Dict[int, str] = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
    NOTSET: "NOTSET",
}

NAME_TO_LEVEL: Dict[str, int] = {
    "CRITICAL": CRITICAL,
    "FATAL": FATAL,
    "ERROR": ERROR,
    "WARN": WARNING,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}

# logging formatters

EXHAUSTIVE_FORMATTER = logging.Formatter(
    fmt="%(asctime)s - %(module)s - %(funcName)s:%(lineno)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

STANDARD_FORMATTER = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

MINIMAL_FORMATTER = logging.Formatter(
    fmt="%(message)s",
)

DEFAULT_LOGGING_LEVEL = DEBUG
DEFAULT_FORMATTER = EXHAUSTIVE_FORMATTER
CONSOLE_FORMATTER = MINIMAL_FORMATTER