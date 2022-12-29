import logging
from logging import Logger
from kink import di

from musicdl.common.classes import ProcessExecutor, FfmpegHelper, SpotifyClientProvider, FormatHelper, YoutubeDLClientProvider
from musicdl.common.interfaces import BaseProcessExecutor, BaseFfmpegHelper, BaseSpotifyClientProvider, BaseFormatHelper, BaseYoutubeDLClientProvider

def init_di():
    di[Logger] = logging.getLogger("musicdl")
    di[BaseProcessExecutor] = ProcessExecutor()
    di[BaseFfmpegHelper] = FfmpegHelper()
    di[BaseSpotifyClientProvider] = SpotifyClientProvider()
    di[BaseFormatHelper] = FormatHelper()
    di[BaseYoutubeDLClientProvider] = YoutubeDLClientProvider()
