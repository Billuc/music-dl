"""
Central module that holds the downloader classes, interfaces exposed externally and data classes.
"""

from .classes import Song, Album, Artist, Playlist, Saved
from .interfaces import BaseAudioProvider, BaseDownloader, BaseLyricsProvider
