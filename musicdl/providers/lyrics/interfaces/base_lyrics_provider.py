import abc
from typing import List, Optional

from musicdl.common import BasePipeline
from musicdl.providers.lyrics.data import DownloadLyricsCommand


class BaseLyricsProvider(BasePipeline[DownloadLyricsCommand, str]):
    def __init__(self) -> None:
        super().__init__()
