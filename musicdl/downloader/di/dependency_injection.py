from kink import di

from musicdl.providers.audio import init_di as add_audio_providers

from musicdl.downloader.interfaces import BaseProgressLogger
from musicdl.downloader.progress_handler import ProgressLoggerProxy


def init_di():
    add_audio_providers()
    
    di[BaseProgressLogger] = ProgressLoggerProxy