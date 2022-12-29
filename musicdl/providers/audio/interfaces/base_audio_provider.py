from typing import Dict

from musicdl.common import BasePipeline
from musicdl.providers.audio.data import DownloadSongCommand


class BaseAudioProvider(BasePipeline[DownloadSongCommand, Dict]):
    def __init__(self) -> None:
        super().__init__()