from enum import Enum
import logging
from typing import Dict, List


# https://github.com/python/cpython/blob/3.10/Lib/logging/__init__.py
class LoggingLevel(Enum):
    CRITICAL = 50
    FATAL = 50
    ERROR = 40
    WARNING = 30
    WARN = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    
    @classmethod
    def level_names(cls) -> List[str]:
        return cls.__members__.keys()

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

DEFAULT_LOGGING_LEVEL = LoggingLevel.DEBUG
DEFAULT_FORMATTER = EXHAUSTIVE_FORMATTER
CONSOLE_FORMATTER = MINIMAL_FORMATTER