"""
Lyrics providers for musicdl.
"""

from .interfaces import BaseLyricsProvider
from .data import DownloadLyricsCommand
from .di import init_di
