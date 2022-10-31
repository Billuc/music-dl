"""
Central module that holds the downloader classes, interfaces exposed externally and data classes.
"""

from .data import DownloaderSettings, Song, Album, Artist, Playlist, Saved
from .interfaces import BaseAudioProvider, BaseLyricsProvider, BaseDownloadCoordinator
