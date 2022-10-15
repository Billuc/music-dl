from kink import di

from musicdl.downloader.interfaces import BaseProgressLogger
from musicdl.downloader.progress_handler import ProgressLoggerProxy


def init_di():
    di[BaseProgressLogger] = ProgressLoggerProxy