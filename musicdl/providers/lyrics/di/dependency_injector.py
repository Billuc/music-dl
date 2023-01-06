from kink import di

from musicdl.common import PipelineFactory
from musicdl.providers.lyrics.data import DownloadLyricsCommand
from musicdl.providers.lyrics.classes import AZLyricsLyricsProvider, GeniusLyricsProvider, MusixmatchLyricsProvider
from musicdl.providers.lyrics.interfaces import BaseLyricsProvider

def init_di():
    di[BaseLyricsProvider] = lambda di: (
        PipelineFactory[DownloadLyricsCommand, str]()
            .add(di[MusixmatchLyricsProvider])
            .add(di[GeniusLyricsProvider])
            .add(di[AZLyricsLyricsProvider])
            .build()
    )