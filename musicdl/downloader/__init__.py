"""
Central module that holds the downloader classes, interfaces exposed externally and data classes.
"""

from .data import DownloaderSettings
from .di import init_di
from .interfaces import BaseDownloadCoordinator
